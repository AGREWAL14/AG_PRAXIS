# AG_PRAXIS — Decision Log

Each entry records a decision, the evidence behind it, and the date. Append only.

---

## 2026-08-01 — Primary classification task: 19-class

**Decision:** The 19-class task is primary. The 2-class and 6-class tasks are
reported as secondary.

**Reasoning:** The finer granularity is where minority classes are visible and where
macro-averaged evaluation differs most from weighted. Binary classification on this
dataset is close to saturated and offers little to measure.

---

## 2026-08-01 — Primary metric: macro-F1

**Decision:** Macro-F1 is the primary metric. Macro and weighted are always reported
together.

**Reasoning:** The class distribution spans roughly two orders of magnitude. Weighted
averaging allows a model to score highly while failing entirely on the smallest
classes, because those classes contribute in proportion to their size.

---

## 2026-08-01 — Evaluation protocol: capture-disjoint splits

**Decision:** All model evaluation uses splits in which no capture file contributes to
more than one partition. The split distributed with the dataset is retained only for
the baseline reproduction.

**Reasoning:** Each attack class was recorded in a separate session and stored in its
own file. The distributed split divides each recording into a training half and a
testing half, so both partitions share the conditions of the same session. Any feature
that varies between sessions can act as a shortcut.

---

## 2026-08-01 — RQ2 formulation: sequences, not graphs

**Decision:** RQ2 tests whether modelling traffic as sequences of records improves
detection over single-record classification. Graph-based spatial modelling is out of
scope.

**Reasoning:** Constructing a communication graph requires endpoint identifiers to
define nodes and edges. Whether the released CSVs contain them is confirmed in NB01.
A graph built from the same features the model already reads would give attention no
information the model does not already have.

**Status:** Confirmed by NB01. Update this entry with the result.

---

## 2026-08-01 — Baseline treatment: reproduced without modification

**Decision:** The published CNN baseline is reproduced exactly as specified and is
never tuned, corrected, or improved.

**Reasoning:** The comparison between the shipped split and the capture-disjoint split
is only interpretable if the model is identical across both. Any change to the
architecture would make an observed difference attributable to the change rather than
to the evaluation protocol.

---

## 2026-08-01 — Explainability validation: computational, not expert-rated

**Decision:** The mapping from feature attributions to attack patterns and threat
categories is validated by permutation testing and cross-seed stability rather than
by expert inter-rater agreement.

**Reasoning:** Expert raters are not available. A deterministic mapping rule fixed in
advance, tested for whether it separates classes in attribution space, assesses
whether the structure is present in the data. Rater agreement would only establish
that a small panel concurred.

---

## 2026-08-01 — Cross-dataset transfer: out of scope

**Decision:** Generalisation is tested by holding out entire attack families within
CICIoMT2024. A second corpus is not introduced.

**Reasoning:** Combining datasets risks a model learning which corpus a record came
from rather than which attack it represents, reproducing the same problem at a higher
level. Leave-one-family-out tests generalisation within a controlled setting and is
achievable in the available time. Cross-dataset transfer is listed as future work.

---

## 2026-08-01 — Six-class task added to NB09 and NB10

**Decision:** The baseline reproduction and capture-disjoint comparison run the
six-class task in addition to the nineteen-class task.

**Reasoning:** Prior work in this program (Bogan, 2025) reports macro-averaged
precision and recall for the six-class categorisation task only. A like-for-like
comparison requires results at that granularity. The nineteen-class task remains
primary.

---

## 2026-08-01 — NB11 baseline specified as stratified k-fold Random Forest

**Decision:** The non-sequence baseline is a Random Forest with stratified k-fold
cross-validation, evaluated under capture-disjoint splits.

**Reasoning:** This matches the best-performing model reported in prior work in this
program, allowing that approach to be evaluated under the split protocol adopted here.

---

## 2026-08-01 — Timing measurements recorded for all runs

**Decision:** Training time and inference time are recorded in metrics.json for every
run.

**Reasoning:** Supports comparison of deployment feasibility. Instrumenting now avoids
re-running experiments to obtain the measurement later.
