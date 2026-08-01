# AG_PRAXIS — Project Rules

Read this before writing any notebook or module in this repository.

---

## 1. Naming

| Thing | Name |
|---|---|
| Project root (Mac) | `~/Documents/AG_PRAXIS/` |
| GitHub repository | `AG_PRAXIS` |
| Drive artefacts | `MyDrive/AG_PRAXIS_artifacts/` |
| Conda environment | `ag_praxis` |
| Notebook files | `AG_PRAXIS_NB01_load_inventory.ipynb` |
| Run records | `runs/AG_PRAXIS_NB01_2026-08-05.ipynb` |
| Artefact folders | `AG_PRAXIS_artifacts/NB04_seed42/` |

Every notebook is numbered and titled. Numbers are never reused, and never
renumbered once a notebook has been run.

---

## 2. Writing style for markdown cells

This is the rule that matters most and the one most often broken.

Markdown cells are written in the voice of a student explaining their own
experiment to someone reading over their shoulder. Plain, direct, and sequential.
The notebook should read as a account of work being done, not as documentation of
a finished system.

### What each markdown cell does

- **Opening cell**: what this notebook is for and what it will produce. A short
  paragraph, not a specification.
- **Before each code block**: what this block does and why it comes at this point.
  One or two sentences. Explain the reasoning, not the syntax.
- **After a result**: what the output shows and what it means for the next step.

### Voice

Write like this:

> Before I can build any model I need to know what is actually in these files. The
> paper describes the dataset, but I want to see the columns myself rather than
> take the description on trust. This first block reads one file and prints every
> column with its type and range.

And this:

> The next thing to check is whether the timing columns are doing what I think they
> are. If a model can tell the attack classes apart using only those columns, that
> tells me something important about what the model is really learning.

Not like this:

> This notebook leverages a comprehensive data inventory methodology to
> systematically interrogate the underlying schema, thereby enabling robust
> downstream architectural decisions.

Not like this either:

> **Purpose:** Schema validation.
> **Inputs:** CSV files.
> **Outputs:** schema.json.
> **Dependencies:** pandas, numpy.

The first is inflated. The second is a form, not an explanation.

### Specific prohibitions

- No "leverage", "robust", "comprehensive", "seamless", "delve", "underscore",
  "it is worth noting", "it is important to note", "furthermore", "moreover".
- No em-dash-heavy constructions or triads ("not X, but Y, and certainly Z").
- No section headers inside a cell that only contains two sentences.
- No bullet lists where a sentence works.
- No closing summary cell that restates what the notebook did.
- No "Next steps" cells listing hypothetical future work.
- No emoji, no decorative separators.

### Self-containment

Each notebook explains itself from first principles. It does not refer to earlier
projects, prior attempts, archived results, or findings that are not produced
inside this repository.

Write:

> Each attack class was recorded in its own capture session. That means anything
> which varies between recording sessions could act as a shortcut, so I want to
> test for that before I trust any result.

Do not write:

> As established in previous work, this dataset suffers from capture-provenance
> leakage which inflated earlier results to 0.99.

The reasoning is stated. The history is not. If a concern is worth raising, it is
worth deriving in the notebook that raises it.

---

## 3. Non-negotiable technical rules

- Every notebook sets `SEED` from `config/base.yaml` before constructing any model.
- Every training run calls `save_run()` as the **last statement in the training
  cell**, never in a separate cell. A Colab disconnect loses separate cells.
- `save_run()` writes five files: `config.json`, `metrics.json`, `y_true.npy`,
  `y_pred.npy`, `model.keras`.
- Scalers and encoders are fitted on training data only.
- Macro-F1 is the primary metric. Macro and weighted are always reported together.
- Notebooks import from `src/`. Logic that lives only in a cell cannot be tested
  or reused.
- The `FAST` environment variable toggles a 1% stratified subsample. Default is
  `FAST=1`. Runs entered in the ledger require `FAST=0`.
- Cell 1 of every notebook mounts Drive, clones the repo, and captures the git SHA.
- The final cell prints a ledger entry block ready to paste into
  `RESULTS_LEDGER.md`.
- Long runs include a per-epoch `ModelCheckpoint` writing to Drive.

---

## 4. Experimental discipline

- One change per run. Two changes and a moved score teaches nothing about either.
- Hyperparameters are tuned on validation. The test set is evaluated once per
  configuration.
- Every run is logged, including runs that made things worse.
- `RESULTS_LEDGER.md` is append-only. Corrections are appended as new entries.

---

## 5. Repository boundaries

- Never create or delete files outside this repository without asking first.
- `baselines/` contains reproduced published work and is never modified.
- `notebooks/` is authored on the Mac only.
- `runs/` receives executed copies from Colab only and is never re-edited.
- Large artefacts (`.npy`, `.keras`) live on Drive, not in git. Only
  `metrics.json` is committed.

---

## 6. Notebook skeleton

Every notebook follows this shape:

1. Title and opening paragraph
2. Setup: Drive, repo clone, git SHA
3. Config block
4. Seeding
5. Body, alternating markdown explanation and code
6. Results, reported in full
7. Ledger entry block

The title is `# AG_PRAXIS NB0X — Short Descriptive Title`.
