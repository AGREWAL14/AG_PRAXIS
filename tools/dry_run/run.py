"""Run a notebook's real code locally, against a miniature copy of the project.

The point is to fail here rather than in a paid Colab session. Every code cell of
the notebook is executed, in order, in one namespace, against a fixture that is
structurally exact where the notebook asserts structure and tiny everywhere else.
Asserts run, configs are built, `assert_single_change` runs, the model is fitted,
the artefacts are written and read back, and the ledger block is formatted.

Nothing here checks a result. A dry run's figures are noise by construction. What
it claims is narrower: this code runs to the end, and writes what it says it does.

Three things are checked that no amount of reading catches. Whether the training
path is compiled, because an uncompiled loop is invisible to every other check and
costs hours to find. Whether the notebook's own asserts pass against a fixture
built to satisfy them. And whether the versions this ran under are the versions
Colab last ran under, which is reported as a failure rather than a note, because
that gap has already cost a session once.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import linecache
import os
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))


# --------------------------------------------------------------------------
# the report
# --------------------------------------------------------------------------


class Report:
    """Lines, and whether any of them was a failure."""

    def __init__(self):
        self.sections = []
        self.failures = 0

    def section(self, title):
        self.sections.append((title, []))

    def line(self, text, *, ok=None):
        mark = "     " if ok is None else ("PASS " if ok else "FAIL ")
        if ok is False:
            self.failures += 1
        self.sections[-1][1].append(f"{mark}{text}")

    def render(self):
        out = []
        for title, lines in self.sections:
            out.append("")
            out.append(title)
            out.append("-" * max(len(title), 78))
            out.extend(lines or ["     nothing to report"])
        out.append("")
        out.append("=" * 78)
        out.append(f"{'DRY RUN FAILED' if self.failures else 'DRY RUN CLEAN'}"
                   f"   {self.failures} failure(s)")
        out.append("=" * 78)
        return "\n".join(out)


# --------------------------------------------------------------------------
# environment, and the version gap
# --------------------------------------------------------------------------


def local_environment() -> dict:
    """What this machine has, for the packages a run depends on."""
    found = {}
    for name in ("tensorflow", "keras", "numpy", "pandas", "sklearn"):
        try:
            found[name] = getattr(importlib.import_module(name), "__version__", "unknown")
        except Exception as error:
            found[name] = f"MISSING ({type(error).__name__})"
    return found


def recorded_environment() -> tuple[dict | None, str]:
    """The environment the most recent executed run recorded, and where it came from.

    Read out of committed run configs rather than remembered. A run that did not
    record its environment is not evidence about anything, so the absence is
    reported rather than filled in.
    """
    best, source = None, "nothing found"
    for path in sorted(REPO_ROOT.glob("**/config.json")):
        if ".git" in path.parts:
            continue
        try:
            config = json.loads(path.read_text())
        except Exception:
            continue
        environment = (config.get("observed") or {}).get("environment")
        if not environment:
            continue
        date = str((config.get("observed") or {}).get("run_date", ""))
        if best is None or date >= best[0]:
            best = (date, environment)
            source = f"{path.relative_to(REPO_ROOT)} ({date or 'no run date'})"
    return (best[1] if best else None), source


def check_versions(report: Report) -> None:
    report.section("ENVIRONMENT — local against what Colab last recorded")
    here = local_environment()
    there, source = recorded_environment()

    for name, version in here.items():
        report.line(f"local {name:<12} {version}")
    report.line(f"recorded from: {source}")

    if there is None:
        report.line(
            "no executed run records the versions it ran under, so there is nothing to "
            "compare against. This clears the first time a notebook is run with the "
            "environment cell in its setup.",
            ok=False,
        )
        return

    for name in ("tensorflow", "keras"):
        mine, theirs = here.get(name), there.get(name)
        if theirs is None:
            report.line(f"{name}: the recorded run does not name it", ok=False)
        elif mine != theirs:
            report.line(
                f"{name}: local {mine} against {theirs} in Colab. Every API check below "
                f"is against {mine}, so a behaviour that only exists in {theirs} is "
                "invisible to this dry run.",
                ok=False,
            )
        else:
            report.line(f"{name}: {mine}, the same as the recorded run", ok=True)


# --------------------------------------------------------------------------
# the static layer
# --------------------------------------------------------------------------


def cells(path: Path) -> list[dict]:
    return json.loads(path.read_text())["cells"]


def check_notebook_shape(report: Report, path: Path) -> list[str]:
    """The newline invariant, that every cell parses, and cell-order dependencies."""
    report.section(f"STATIC — {path.name}")
    every = cells(path)
    code = []

    # Two ways a cell's source can be wrong. Lines that have lost their newlines, which
    # is what Colab reads as one long line and refuses to parse. And a source collapsed
    # into a single string, which runs but makes a one-line edit show as a hundred-line
    # diff, so a review cannot see what changed.
    broken = [
        i for i, cell in enumerate(every)
        if len(cell["source"]) > 1 and any(not line.endswith("\n") for line in cell["source"][:-1])
    ]
    collapsed = [
        i for i, cell in enumerate(every)
        if len(cell["source"]) == 1 and "\n" in cell["source"][0]
    ]
    report.line(
        "newline invariant: every line of every cell ends in a newline except the last"
        if not broken else f"newline invariant violated in cells {broken}; Colab will read "
        "each of those cells as one line",
        ok=not broken,
    )
    report.line(
        "no cell holds its whole source as one string"
        if not collapsed else f"cells {collapsed} hold their source as a single string; "
        "they run, but a one-line edit to them shows as a whole-cell diff",
        ok=not collapsed,
    )

    parsed_ok = True
    for i, cell in enumerate(every):
        if cell["cell_type"] != "code":
            continue
        text = "".join(cell["source"])
        code.append(text)
        try:
            ast.parse(text)
        except SyntaxError as error:
            report.line(f"cell {i} does not parse: {error}", ok=False)
            parsed_ok = False
    if parsed_ok:
        report.line(f"{len(code)} code cells parse", ok=True)

    report.line(f"{len(every)} cells, {len(every) - len(code)} markdown, {len(code)} code")
    return code


BUILTINS = set(dir(__builtins__)) | {"__name__", "__file__"}


def check_cell_order(report: Report, code: list[str]) -> None:
    """Names read before anything defines them, which is a cell-order bug."""
    defined, problems = set(BUILTINS) | set(dir(__builtins__)), []
    for i, text in enumerate(code):
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in defined:
                    problems.append((i, node.lineno, node.id))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
                defined.add(node.id)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defined.add(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    defined.add((alias.asname or alias.name).split(".")[0])
            elif isinstance(node, ast.comprehension):
                for name in ast.walk(node.target):
                    if isinstance(name, ast.Name):
                        defined.add(name.id)
            elif isinstance(node, (ast.For, ast.With, ast.ExceptHandler)):
                # `except X as name` binds a plain string on the handler, not a Name node,
                # so walking for Name/Store misses it and the name reads as undefined.
                if isinstance(node, ast.ExceptHandler) and node.name:
                    defined.add(node.name)
                for name in ast.walk(node):
                    if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store):
                        defined.add(name.id)
            elif isinstance(node, ast.arg):
                defined.add(node.arg)
    unresolved = [p for p in problems if p[2] not in defined]
    if unresolved:
        for i, line, name in unresolved[:12]:
            report.line(f"cell {i} line {line}: {name} is read before anything defines it",
                        ok=False)
    else:
        report.line("no name is read before a cell that defines it", ok=True)


def check_api(report: Report, code: list[str]) -> None:
    """Every keras.* and tf.* attribute the notebooks touch, resolved here."""
    wanted = {}
    for text in code:
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.Attribute):
                continue
            parts, cursor = [], node
            while isinstance(cursor, ast.Attribute):
                parts.append(cursor.attr)
                cursor = cursor.value
            if isinstance(cursor, ast.Name) and cursor.id in ("keras", "tf", "np", "pd"):
                wanted.setdefault(cursor.id, set()).add(".".join(reversed(parts)))

    modules = {"keras": "keras", "tf": "tensorflow", "np": "numpy", "pd": "pandas"}
    missing = []
    for short, attributes in sorted(wanted.items()):
        try:
            module = importlib.import_module(modules[short])
        except Exception as error:
            report.line(f"cannot import {modules[short]}: {error}", ok=False)
            continue
        for attribute in sorted(attributes):
            cursor = module
            for part in attribute.split("."):
                cursor = getattr(cursor, part, None)
                if cursor is None:
                    missing.append(f"{short}.{attribute}")
                    break
        report.line(f"{short} ({modules[short]}): {len(attributes)} attributes checked")
    for name in missing:
        report.line(f"{name} does not resolve against the installed version", ok=False)
    if not missing:
        report.line("every keras, tf, numpy and pandas attribute resolves", ok=True)


# --------------------------------------------------------------------------
# the compiled-training-path check
# --------------------------------------------------------------------------


@contextmanager
def openfda_stub(profile):
    """Answer openFDA from canned counts instead of the live service.

    A dry run that reached the real API would not be a dry run, and it would spend
    requests against a limit of a thousand a day per IP. The canned set covers the three
    paths that can silently produce a wrong number: an ordinary count, a 404, which is
    what openFDA returns for a search matching nothing, and an overlap where the
    de-duplicated union comes out below the sum of the per-term counts.
    """
    spec = profile.fixture
    if not spec.get("stub_openfda"):
        yield None
        return

    import urllib.error
    import urllib.parse
    import urllib.request

    counts = spec["canned_counts"]
    original = urllib.request.urlopen
    calls = []

    class Answer:
        def __init__(self, total):
            self.body = json.dumps({"meta": {"results": {"total": int(total)}}}).encode()

        def read(self):
            return self.body

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def stub(url, *args, **kwargs):
        text = url if isinstance(url, str) else url.full_url
        calls.append(text)
        hit = [name for name in counts
               if f'device.generic_name:"{urllib.parse.quote(name.replace("+", " "))}"' in text]
        if "mdr_text.text" in text:
            return Answer(spec["canned_keyword"])
        if len(hit) > 1:
            return Answer(spec["canned_union"])
        if len(hit) == 1 and counts[hit[0]] is None:
            raise urllib.error.HTTPError(text, 404, "NOT FOUND", None, None)
        if len(hit) == 1:
            return Answer(counts[hit[0]])
        return Answer(0)

    urllib.request.urlopen = stub
    try:
        yield calls
    finally:
        urllib.request.urlopen = original


@contextmanager
def function_spy():
    """Watch tf.function while the notebook runs, and count what it traced and called.

    A source grep would pass on a decorator that is defined and never entered, which
    is exactly the failure this is here to catch, so the check is on what ran.
    """
    import tensorflow as tf

    seen = {"functions": []}
    original = tf.function

    def note(func, made):
        # The object is handed back untouched. Wrapping it would count calls but would
        # also hide the polymorphic API that Keras uses internally, and the tracing count
        # already says what is needed: a function is only traced when it is called.
        seen["functions"].append({"module": getattr(func, "__module__", "?"),
                                  "name": getattr(func, "__qualname__", "?"), "fn": made})
        return made

    def spy(*args, **kwargs):
        made = original(*args, **kwargs)
        if args and callable(args[0]):
            return note(args[0], made)

        def decorator(func):
            return note(func, made(func))

        return decorator

    tf.function = spy
    try:
        yield seen
    finally:
        tf.function = original


def check_training_path(report: Report, seen: dict, profile) -> None:
    report.section("COMPILED TRAINING PATH")
    import tensorflow as tf

    report.line(
        f"tf.config.functions_run_eagerly() is {tf.config.functions_run_eagerly()}",
        ok=not tf.config.functions_run_eagerly(),
    )

    if profile.training_path == "keras_fit":
        report.line("the run trains through keras Model.fit, which compiles its own step",
                    ok=True)
        return

    # Only the project's own training steps are reported. Keras compiles a thousand
    # functions of its own during a fit and counting those says nothing about whether
    # the loop this project wrote is compiled.
    ours = [f for f in seen["functions"] if str(f["module"]).startswith("src.")]
    report.line(
        f"compiled steps defined under src/: {len(ours) or 'none'}"
        + ("" if ours else "; the training loop is running eagerly"),
        ok=bool(ours),
    )
    for found in ours:
        counting = getattr(found["fn"], "experimental_get_tracing_count", None)
        traces = counting() if counting is not None else None
        report.line(
            f"{found['module']}.{found['name']}: traced {traces} time(s). A step that is "
            "never traced was never called, and more than two is a retracing storm",
            ok=traces is not None and 1 <= traces <= profile.max_traces,
        )


# --------------------------------------------------------------------------
# running the cells
# --------------------------------------------------------------------------


def neutralise(text: str, allowlist: list[str], filename: str, record: list) -> ast.Module:
    """Replace the allowlisted scale asserts with nothing, and record every one.

    The fixture is small, so an assert pinning the real number of windows cannot
    hold. Those asserts are checked against the real manifest in the static layer
    instead. Rewriting them here rather than catching the failure means the rest of
    the cell still runs, and nothing else in it is treated leniently.
    """
    tree = ast.parse(text, filename=filename)

    class Strip(ast.NodeTransformer):
        def visit_Assert(self, node):
            segment = ast.get_source_segment(text, node) or ""
            flat = " ".join(segment.split())
            for wanted in allowlist:
                if " ".join(wanted.split()) in flat:
                    record.append((filename, node.lineno, flat[:90]))
                    return ast.copy_location(ast.Pass(), node)
            return node

    return ast.fix_missing_locations(Strip().visit(tree))


def execute(report: Report, code: list[str], profile, shadow: Path) -> dict:
    """Run every code cell in order in one namespace, from inside the shadow root."""
    report.section(f"EXECUTING — {profile.notebook}")
    stripped = []
    namespace = {"__name__": "__main__"}
    here = Path.cwd()
    os.chdir(shadow)
    os.environ["FAST"] = profile.fast_env

    try:
        with function_spy() as seen, openfda_stub(profile) as api_calls:
            for i, text in enumerate(code):
                filename = f"<{profile.name} cell {i}>"
                linecache.cache[filename] = (len(text), None, text.splitlines(True), filename)
                try:
                    tree = neutralise(text, profile.scale_asserts, filename, stripped)
                    exec(compile(tree, filename, "exec"), namespace)
                except Exception:
                    report.line(f"cell {i} raised:", ok=False)
                    for line in traceback.format_exc().splitlines()[-12:]:
                        report.line(f"    {line}")
                    return {"namespace": namespace, "spy": seen, "stripped": stripped,
                            "failed_at": i}
            report.line(f"all {len(code)} code cells ran to the end", ok=True)
            if api_calls is not None:
                report.line(f"openFDA was stubbed; the notebook made {len(api_calls)} calls "
                            "against canned counts and never reached the live service", ok=True)
    finally:
        os.chdir(here)

    return {"namespace": namespace, "spy": seen, "stripped": stripped, "failed_at": None}


def report_allowlist(report: Report, profile, stripped: list) -> None:
    report.section("SCALE ASSERTS — not exercised here, checked against the real metadata")
    for wanted in profile.scale_asserts:
        report.line(f"allowlisted: {' '.join(wanted.split())}")
    for filename, line, text in stripped:
        report.line(f"neutralised at {filename} line {line}: {text}")
    if len(stripped) != len(profile.scale_asserts):
        report.line(
            f"{len(stripped)} of {len(profile.scale_asserts)} allowlisted asserts were found "
            "in the notebook. An allowlist entry that matches nothing is stale, and an "
            "assert that changed wording is no longer covered.",
            ok=False,
        )
    else:
        report.line("every allowlisted assert was found exactly once", ok=True)
    for check, ok, detail in profile.check_scale(REPO_ROOT):
        report.line(f"{check}: {detail}", ok=ok)


# --------------------------------------------------------------------------
# entry
# --------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--notebook", required=True, help="the profile to run, e.g. NB07b")
    parser.add_argument("--keep", action="store_true", help="leave the fixture on disk")
    args = parser.parse_args(argv)

    profile = importlib.import_module(f"profiles.{args.notebook.lower()}").PROFILE
    report = Report()

    check_versions(report)
    path = REPO_ROOT / "notebooks" / profile.notebook
    if not path.exists():
        report.section("STATIC")
        report.line(f"{path} does not exist", ok=False)
        print(report.render())
        return 1

    code = check_notebook_shape(report, path)
    check_cell_order(report, code)
    check_api(report, code)

    import fixture

    shadow = fixture.build(profile, keep=args.keep)
    report.section("FIXTURE")
    for line in fixture.describe(shadow):
        report.line(line)

    outcome = execute(report, code, profile, shadow)
    report_allowlist(report, profile, outcome["stripped"])
    if outcome["failed_at"] is None:
        check_training_path(report, outcome["spy"], profile)
        report.section("ARTEFACTS")
        for check, ok, detail in profile.check_artefacts(shadow, outcome["namespace"]):
            report.line(f"{check}: {detail}", ok=ok)

    print(report.render())
    if not args.keep:
        fixture.clean(shadow)
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
