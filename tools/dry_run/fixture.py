"""A miniature copy of the project: structurally exact, tiny in rows.

The notebooks assert a lot about structure — nineteen classes, forty-four features,
forty-five capture groups over training windows, fifty-seven in the corpus, twelve
the objective never sees. All of that is cheap to reproduce with a handful of
windows per capture, and the fixture reproduces it exactly so those asserts run for
real rather than being skipped.

What is not reproduced is scale. The real test partition is 49,159 windows and the
real training partition is 249,061, and materialising either would make a dry run
cost what the thing it is checking costs. The asserts that pin those two numbers
are the only place this diverges, they are listed in each profile, and they are
checked against the real manifest instead.

The shadow root is a directory holding symlinks to the real `src`, `baselines` and
`notebooks`, a rewritten `config/base.yaml` pointing at the fixture, and fixture
`data/processed`, `results` and `artifacts` trees. A notebook's first cell walks up
from the working directory looking for `config/base.yaml`, so running from inside
the shadow root is all it takes for every path in it to resolve here.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
from pathlib import Path

import numpy as np
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

MULTI = {"DDoS-ICMP": 8, "DDoS-SYN": 3, "DDoS-TCP": 3, "DDoS-UDP": 8,
         "DoS-ICMP": 3, "DoS-SYN": 3, "DoS-TCP": 3, "DoS-UDP": 3}
SINGLE = ["Benign", "MQTT-DDoS-Connect_Flood", "MQTT-DDoS-Publish_Flood",
          "MQTT-DoS-Connect_Flood", "MQTT-DoS-Publish_Flood", "MQTT-Malformed_Data",
          "Recon-OS_Scan", "Recon-Ping_Sweep", "Recon-Port_Scan", "Recon-VulScan",
          "Spoofing"]
SINGLE_RECORDING = {"Spoofing": "ARP_Spoofing"}
LABELS = sorted(list(MULTI) + SINGLE)
NB07_RUNS = ["class_weighted_loss", "focal_loss", "logit_adjustment",
             "threshold_tuning", "window_resampling"]


def _recording(label, index=None):
    """A recording name that the project's own parse_capture reads back correctly."""
    if label in MULTI:
        return f"TCP_IP-{label}{index}"
    return SINGLE_RECORDING.get(label, label)


def _plan():
    """Which capture contributes to which partition.

    Training holds the 34 captures of the eight classes recorded more than once plus
    the eleven recorded once, which is 45. Twelve more appear only in validation or
    test, which is what makes the corpus 57 and leaves twelve the objective cannot see.
    """
    train, val, test = [], [], []
    for label, n in MULTI.items():
        for i in range(1, n + 1):
            train.append((_recording(label, i), label))
        test.append((_recording(label, 100), label))
    for label in list(MULTI)[:4]:
        val.append((_recording(label, 200), label))
    for label in list(MULTI)[4:]:
        val.append((_recording(label, 1), label))
    for label in SINGLE:
        train.append((_recording(label), label))
        val.append((_recording(label), label))
        test.append((_recording(label), label))
    return {"train": train, "val": val, "test": test}


def _arrays(rows, per_capture, window, features, seed):
    rng = np.random.default_rng(seed)
    recordings = sorted({name for name, _ in rows})
    index = {name: i for i, name in enumerate(recordings)}
    n = len(rows) * per_capture
    X = rng.normal(size=(n, window, features)).astype("float32")
    y = np.empty(n, dtype="int16")
    recording = np.empty(n, dtype="int16")
    at = 0
    for name, label in rows:
        X[at : at + per_capture] += index[name] * 0.05
        y[at : at + per_capture] = LABELS.index(label)
        recording[at : at + per_capture] = index[name]
        at += per_capture
    return {"X": X, "y": y, "recording": recording, "recordings": recordings}


def build(profile, *, keep=False) -> Path:
    """Write the shadow root and everything in it, and return where it is."""
    spec = profile.fixture
    window, features = int(spec["window"]), int(spec["features"])
    shadow = Path(tempfile.mkdtemp(prefix=f"agpraxis_dryrun_{profile.name}_"))

    for name in ("src", "baselines", "notebooks"):
        (shadow / name).symlink_to(REPO_ROOT / name)
    (shadow / "config").mkdir()
    (shadow / "config" / "feature_families.yaml").symlink_to(
        REPO_ROOT / "config" / "feature_families.yaml")

    artifacts = shadow / "artifacts"
    base = yaml.safe_load((REPO_ROOT / "config" / "base.yaml").read_text())
    base["paths"] = {**base["paths"], "artifacts": str(artifacts),
                     "data_root": str(shadow / "csv"), "train_dir": str(shadow / "csv" / "train"),
                     "test_dir": str(shadow / "csv" / "test"), "repo": str(shadow)}
    (shadow / "config" / "base.yaml").write_text(yaml.safe_dump(base, sort_keys=False))

    plan = _plan()
    counts = {"train": int(spec["train_windows_per_capture"]),
              "val": int(spec["val_windows_per_capture"]),
              "test": int(spec["test_windows_per_capture"])}
    real = json.loads((REPO_ROOT / "data" / "processed" / "NB04_manifest.json").read_text())
    feature_names = list(real["columns"]["kept"])[:features]

    processed = shadow / "data" / "processed"
    processed.mkdir(parents=True)
    (artifacts / "NB04").mkdir(parents=True)

    manifest = json.loads(json.dumps(real))
    blocks = []
    for partition, rows in plan.items():
        built = _arrays(rows, counts[partition], window, features,
                        seed={"train": 11, "val": 22, "test": 33}[partition])
        np.savez(artifacts / "NB04" / f"sequences_{partition}.npz",
                 X=built["X"], y=built["y"], recording=built["recording"],
                 source_file=built["recording"],
                 start_row=np.arange(len(built["y"]), dtype="int32"),
                 classes=np.asarray(LABELS, dtype=str),
                 recordings=np.asarray(built["recordings"], dtype=str),
                 files=np.asarray([f"{r}.pcap.csv" for r in built["recordings"]], dtype=str),
                 features=np.asarray(feature_names, dtype=str),
                 window=np.asarray(window), stride=np.asarray(int(spec["stride"])))
        manifest["arrays"][f"sequences_{partition}"] = {
            "file": f"sequences_{partition}.npz",
            "shape": [int(len(built["y"])), window, features],
            "n_features": features, "window": window, "stride": int(spec["stride"]),
            "by_class": {label: int((built["y"] == LABELS.index(label)).sum())
                         for label in LABELS}}
        for name, label in rows:
            suffix = "_test" if partition == "test" else "_train"
            blocks.append({"label": label, "tier": "A" if label in MULTI else "B",
                           "partition": partition, "recording": f"{name}{suffix}",
                           "file": f"{name}{suffix}.pcap.csv", "start": 0,
                           "stop": counts[partition] * int(spec["stride"])})
    manifest["split"]["blocks"] = blocks
    manifest["columns"]["kept"] = feature_names
    (processed / "NB04_manifest.json").write_text(json.dumps(manifest, indent=1))

    per_class = {label: round(0.40 + 0.02 * i, 4) for i, label in enumerate(LABELS)}
    parent_config = json.loads(
        (REPO_ROOT / "data" / "processed" / "NB06" / "config.json").read_text())
    parent_metrics = {"n_test": 49159, "n_classes": 19, "labels": LABELS, "accuracy": 0.8197,
                      "macro_f1": 0.713792, "weighted_f1": 0.8064, "per_class_f1": per_class,
                      "per_class_precision": per_class, "per_class_recall": per_class,
                      "support": {label: 100 for label in LABELS}, "n_parameters": 214227,
                      "n_train": 249061, "train_seconds": 2427.7, "inference_seconds": 7.0}
    for where in (processed / "NB06", artifacts / "NB06" / "sequence_cnn_lstm_19class"):
        where.mkdir(parents=True, exist_ok=True)
        (where / "config.json").write_text(json.dumps(parent_config, indent=1))
        (where / "metrics.json").write_text(json.dumps(parent_metrics, indent=1))

    if spec.get("needs_parent_model", True):
        import sys

        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        from src import sequence as sq

        sq.build_model(features, len(LABELS), window=window).save(
            artifacts / "NB06" / "sequence_cnn_lstm_19class" / "model.keras")

    (processed / "NB03_verdict.json").write_text(json.dumps({
        "generated_on": "2026-08-04", "git_sha": "fixture", "seed": 42, "is_fast_pass": False,
        "n_features": features, "n_recordings": 50, "rows_per_recording": 8000,
        "features": feature_names, "families": {"timing": ["Duration", "Rate", "Srate", "IAT"]},
        "forest": {"n_estimators": 50, "min_samples_leaf": 100, "test_fraction": 0.30,
                   "random_state": 42},
        "capture_identification": [{"name": "capture_all_features", "scope": "all 44 features",
                                    "n_features": features, "n_classes": 50, "chance": 0.02,
                                    "accuracy": 0.8010, "macro_f1": 0.7952}],
        "within_class_mean_accuracy": 0.8280, "within_class_mean_chance": 0.175}, indent=1))

    for run in NB07_RUNS:
        directory = shadow / "results" / "NB07" / run
        directory.mkdir(parents=True)
        (directory / "metrics.json").write_text(json.dumps(
            {"macro_f1": 0.70, "per_class_f1": per_class, "n_test": 49159}, indent=1))

    for k, macro in ((5, 0.6295), (10, 0.6837), (25, 0.7323)):
        directory = processed / "NB08" / f"sequence_budget_{k:02d}"
        directory.mkdir(parents=True)
        (directory / "metrics.json").write_text(json.dumps(
            {"macro_f1": macro, "n_test": 49159, "n_parameters": 214227}, indent=1))

    return shadow


def describe(shadow: Path) -> list[str]:
    manifest = json.loads((shadow / "data" / "processed" / "NB04_manifest.json").read_text())
    lines = [f"shadow root: {shadow}"]
    for partition in ("train", "val", "test"):
        shape = manifest["arrays"][f"sequences_{partition}"]["shape"]
        lines.append(f"  sequences_{partition:<5} {shape[0]:>6,} windows of {shape[1]}x{shape[2]}")
    blocks = manifest["split"]["blocks"]
    captures = {re.sub(r"_(train|test)$", "", b["recording"]) for b in blocks}
    train = {re.sub(r"_(train|test)$", "", b["recording"])
             for b in blocks if b["partition"] == "train"}
    lines.append(f"  captures: {len(captures)} in the corpus, {len(train)} in training, "
                 f"{len(captures - train)} never seen by a training objective")
    return lines


def clean(shadow: Path) -> None:
    shutil.rmtree(shadow, ignore_errors=True)
