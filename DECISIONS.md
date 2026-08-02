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

---

## 2026-08-02 — Two-tier split protocol

**Decision:** Splits are constructed per class according to how many captures exist.

Tier A, eight classes with multiple captures (DDoS-ICMP, DDoS-SYN, DDoS-TCP,
DDoS-UDP, DoS-ICMP, DoS-SYN, DoS-TCP, DoS-UDP): whole capture chunks are held out.

Tier B, eleven classes with a single capture (Benign, Spoofing, five MQTT, four
Recon): contiguous block split within the capture, 70/15/15 by row position. The
shipped test file is discarded for these classes as it is the second half of the
same recording.

**Evidence:** NB01 capture inventory. Eight classes have 4 to 8 training captures;
eleven classes have exactly one training and one test file bearing the same base
name.

**Consequence:** Full capture-disjoint evaluation is not achievable for eleven of
nineteen classes. This is a property of the dataset and is reported as a limitation.
Results are reported separately by tier, and the difference between tiers serves as
a within-experiment measure of residual leakage.

---

## 2026-08-02 — Label parsing rule

**Decision:** The class label is the capture filename with the partition suffix
removed, trailing chunk digits stripped, the TCP_IP prefix removed, and ARP_Spoofing
mapped to Spoofing. This yields nineteen classes from seventy-two files.

**Evidence:** NB01 filename inventory. No class name ends in a digit, so stripping
trailing digits is unambiguous.

**Consequence:** capture_id is retained separately from label, as capture identity is
required for split construction and for the leakage diagnostic.

---

## 2026-08-02 — Tier A split construction

**Decision:** For DDoS-ICMP and DDoS-UDP the shipped test files are discarded, and
splits are built from the eight training chunks alone. For DDoS-TCP, DDoS-SYN, and
the four DoS classes, one training chunk is held out and the unnumbered shipped test
capture is retained as an additional held-out capture.

**Evidence:** NB02 found fifteen capture identifiers present in both partitions.
Eleven are Tier B classes, where train and test are halves of a single recording.
Four are Tier A chunks — ICMP1, ICMP2, UDP1, UDP2 — whose shipped test portions
carry the same chunk number as their training portions.

**Consequence:** Tier A remains capture-disjoint for all eight classes. No class is
lost from Tier A.

---

## 2026-08-02 — Imbalance ratio measured

**Decision:** The nineteen-class imbalance ratio is recorded as 2,157.7 to 1, not the
figure implied by the published class distribution.

**Evidence:** NB02 counted 1,998,026 rows for DDoS-UDP against 926 for
Recon-Ping_Sweep across 8,775,013 total rows. Six-class ratio is 328.6 to 1;
two-class is 37.1 to 1.

**Consequence:** Recon-Ping_Sweep has too few rows for resampling-based remedies to
be meaningful. Reported as a limitation on H2.

---

## 2026-08-02 — No capture-constant columns found

**Decision:** No feature column is constant within a capture while varying across
captures.

**Evidence:** NB02 per-capture constancy screen, run at FAST=1. Two columns are
constant across the entire dataset.

**Consequence:** The crudest form of capture-identity encoding is ruled out. If
provenance signal exists it is carried in distributions rather than constants, which
is what the NB04 timing diagnostic tests. The screen is repeated at FAST=0 before
this is treated as final.

---

## 2026-08-02 — Tier A shipped split is already capture-disjoint

**Decision:** No modification is made to the shipped split for the eight Tier A
classes. Chunk numbering restarts per partition, so ICMP1_test is an independent
recording from ICMP1_train despite the shared name.

**Evidence:** Two lines of evidence agree. Row counts: Tier A test files match the
standard chunk size of their family (ICMP2_test 195,692 against ICMP2_train 194,818),
which a percentage split cannot produce. Distributions: ICMP1_test is not closer to
ICMP1_train than to ICMP5_train on Header_Length or Rate.

**Consequence:** Tier A requires no reconstruction. The two-tier protocol stands, but
its basis changes: Tier A was never leaking, and Tier B always was, within the same
shipped split used throughout the published literature.

---

## 2026-08-02 — Tier B shipped split confirmed within-capture

**Decision:** For the eleven Tier B classes, the shipped test file is the held-out
portion of a single recording and is discarded. Splits are built by contiguous block
within the training capture.

**Evidence:** Every Tier B pair sits near 80/20 — Benign 192,732 / 37,607 at 16.3%;
Recon-Port_Scan 83,981 / 22,622 at 21.2%; Recon-Ping_Sweep 740 / 186 at 20.1%.

---

## 2026-08-02 — Provenance signal is distributional, not constant

**Decision:** NB04 measures between-capture variance relative to within-capture
variance for every feature, and ranks features by that ratio. This replaces the
constancy screen.

**Evidence:** NB02 found no capture-constant columns and no near-misses. However,
Header_Length varies from 59.60 to 225.98 across three captures of the same attack
class, and Rate from 15,887 to 26,882, while IAT is flat at approximately 84.69
million across all three.

**Consequence:** Provenance, if present, is carried by distributional shift rather
than by any column acting as a capture label. Header_Length is the leading candidate.
IAT, identified as the top SHAP feature by prior work on this dataset and on
CICIoT2023, shows no between-capture variation in this sample and is unlikely to be
the carrier.
