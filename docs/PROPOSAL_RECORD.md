# Research Proposal Record

**Predictive Threat Detection and Threat-Intelligence Maturation for Health Monitoring Wearables and Remote Patient Hubs**

Dataset: CICIoMT2024 · Baseline: Mohammadi et al. (2024), ICIS, arXiv:2410.23306

---

## Document status

Every quantitative claim below is either (a) reproduced from an executed notebook and
verified against its saved output, or (b) quoted from a source document. Items that
have **not** been verified are collected in Section 12 and are flagged inline as
`[UNVERIFIED]`. Nothing in this record should be cited until its verification status
is resolved.

---

## 1. What we have

### 1.1 A completed, faithful replication

The Mohammadi et al. CNN was rebuilt from the authors' published GitHub repository and
executed on CICIoMT2024 across all three classification tasks. The replication
reproduces the paper's headline figures, which is the precondition for any claim about
them.

**Verified results (executed notebook, `Phase0_Original_Executed_Replication`):**

| Task | Test Accuracy | Weighted F1 | **Macro F1** | Test Loss |
|---|---|---|---|---|
| 2-class | 0.9965 | 1.00 | 0.96 | 0.0063 |
| 6-class | 0.9950 | 1.00 | 0.87 | 0.0195 |
| 19-class | 0.9870 | 0.98 | **0.75** | 0.1425 |

Scalar metrics for the 19-class task: accuracy 0.98700, precision 0.98796,
recall 0.98700, F1 0.98467.

**Comparison against the paper's Table 1, 19-class row** (Accuracy 0.99, Precision 0.98,
Recall 0.99, F1 0.98): the replication's *weighted* row rounds to exactly these values.
The macro row does not. This establishes that the paper's reported figures are weighted
averages.

### 1.2 Verified per-class performance, 19-class task

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Benign | 0.91 | 0.96 | 0.93 | 37,607 |
| DDoS-ICMP | 1.00 | 1.00 | 1.00 | 349,699 |
| DDoS-SYN | 1.00 | 0.99 | 1.00 | 172,397 |
| DDoS-TCP | 0.99 | 1.00 | 1.00 | 182,598 |
| DDoS-UDP | 1.00 | 1.00 | 1.00 | 362,070 |
| DoS-ICMP | 1.00 | 0.99 | 1.00 | 98,432 |
| DoS-SYN | 1.00 | 1.00 | 1.00 | 98,595 |
| DoS-TCP | 1.00 | 1.00 | 1.00 | 82,096 |
| DoS-UDP | 1.00 | 1.00 | 1.00 | 137,553 |
| MQTT-DDoS-Connect_Flood | 1.00 | 1.00 | 1.00 | 41,916 |
| **MQTT-DDoS-Publish_Flood** | 0.89 | **0.12** | **0.20** | 8,416 |
| MQTT-DoS-Connect_Flood | 1.00 | 0.94 | 0.97 | 3,131 |
| **MQTT-DoS-Publish_Flood** | **0.53** | 1.00 | 0.69 | 8,505 |
| **MQTT-Malformed_Data** | 0.93 | 0.36 | 0.52 | 1,747 |
| **Recon-OS_Scan** | 0.59 | **0.01** | **0.03** | 3,834 |
| Recon-Ping_Sweep | 0.57 | 0.62 | 0.60 | 186 |
| Recon-Port_Scan | 0.86 | 0.95 | 0.90 | 22,622 |
| **Recon-VulScan** | **0.00** | **0.00** | **0.00** | 1,034 |
| **Spoofing** | 0.31 | 0.56 | 0.40 | 1,744 |
| **macro avg** | **0.82** | **0.76** | **0.75** | 1,614,182 |
| weighted avg | 0.99 | 0.99 | 0.98 | 1,614,182 |

**Six-class task, verified:** Spoofing achieves precision 0.27, recall 0.63,
**F1 0.38** on 1,744 samples, while overall accuracy reads 0.9950 and weighted F1
reads 1.00. This single pair of numbers is the clearest available demonstration of
what weighted averaging conceals.

### 1.3 Failure-mode diagnosis from the confusion matrix

The 19-class confusion matrix shows the weak classes fail for **three distinct
reasons**. This matters operationally: a single remedy applied to all three will
succeed on at most one.

| Failure mode | Evidence | Implication |
|---|---|---|
| **Confusable pair** | MQTT-DDoS-Publish_Flood: 7,408 of 8,416 samples predicted as MQTT-DoS-Publish_Flood | Feature separability problem. Rebalancing will not help. |
| **Confusable pair** | Recon-OS_Scan: 3,157 of 3,834 predicted as Recon-Port_Scan; 490 as Benign | Same. |
| **Class never predicted** | Recon-VulScan: 542 → Benign, 413 → Recon-Port_Scan, precision 0.00 | Model emits this class essentially never. Requires direct investigation before any remedy. |
| **Genuine boundary overlap** | Spoofing: 767 of 1,744 → Benign; and 1,355 Benign → Spoofing | Bidirectional confusion. ARP spoofing resembles benign traffic. Rebalancing and threshold tuning most likely to help here. |

### 1.4 Dataset structure, verified from the executed notebook

- 51 CSV files in `train/`, 21 CSV files in `test/` (72 total under those directories;
  73 CSVs found in the dataset tree overall).
- Filenames follow the pattern `ARP_Spoofing_test.pcap.csv`,
  `TCP_IP-DDoS-ICMP1_test.pcap.csv` — i.e. **each capture is split into a `_train`
  and a `_test` half**, and some attack families are chunked further (`ICMP1`, `ICMP2`).
- Test set size: 1,614,182 records.
- Consequence: **the split shipped with the benchmark is within-capture, not
  capture-disjoint.** Both halves of every recording session are present at training
  and test time.

---

## 2. The dataset

**CICIoMT2024** (Dadkhah et al., *Internet of Things* 28:101351, 2024). Network traffic
from 40 IoMT devices, real and simulated, over Wi-Fi, MQTT, and Bluetooth. 18 attack
types in five categories: DDoS, DoS, Reconnaissance, MQTT-specific, and Spoofing.

**Class distribution as published by Mohammadi et al. (Section III.C):**

- Benign: 230,339
- Spoofing: 17,791
- Reconnaissance: 926 – 106,603
- MQTT attacks: 6,877 – 214,952
- DoS/DDoS: 15,904 – 1,998,026

The majority-to-minority ratio is approximately **112:1** (DoS/DDoS maximum against
Spoofing).

### 2.1 Parts in scope

| Component | Status | Rationale |
|---|---|---|
| Wi-Fi / MQTT CSVs | **In scope** | Core corpus; all three class configurations |
| Raw pcaps | **Conditional** | Only if timestamp/endpoint recovery proves necessary — see §12.1 |
| Bluetooth subset | **Out of scope** | Different capture setup; does not share the feature schema |

### 2.2 A field-wide structural property

Each attack class was recorded in its own capture session and stored in its own file.
Any feature that correlates with recording conditions — particularly inter-arrival
timing — can therefore act as a proxy for **which file a record came from** rather than
**what the attack did**.

Because the shipped split divides each capture across train and test, both partitions
share those recording-condition signatures. A model can score highly by identifying
capture provenance without learning attack behaviour at all.

This is a property of the benchmark, not of any one paper. All work in this project
uses capture-disjoint splits.

---

## 3. Critical assessment of Mohammadi et al. (2024)

Re-read in full. Weaknesses are grouped by severity. Each is tied to specific text in
the paper or to a verified replication output.

### 3.1 Fundamental: the temporal claim is architecturally impossible

The paper asserts a temporal capability in at least four places:

- Abstract: the model "leverages the capabilities of CNNs to effectively analyze the
  temporal characteristics of network traffic data."
- Introduction: "CNNs excel at processing time-series data."
- Section IV: "we have designed a CNN model optimized for analyzing time-series network
  traffic data."
- Section IV.A.1: "The input layer receives preprocessed time-series network traffic
  data."

Section IV.A.1 also specifies the input tensor: reshaped to **(samples, features, 1)**,
with each sample "represented by a one-dimensional array of features."

With that shape, a Conv1D kernel of size 3 slides along the **feature axis**. Each
sample is a single flow record. **There is no time axis in the model at any point.**
The architecture cannot analyse temporal characteristics because it never receives a
temporal sequence.

The model is a permutation-sensitive fully-connected network with weight sharing across
adjacent feature *columns* — columns whose ordering is an artefact of the CSV schema
and carries no semantic adjacency.

**Consequence for this project:** an LSTM cannot be appended to this architecture to
obtain temporal modelling. The LSTM would recur over feature positions. Any sequence
model must restructure the input tensor first, which makes it a different model at the
data level, not an extension.

### 3.2 Fundamental: the headline comparison is between incompatible metrics

Table 1 reports the proposed model's 19-class scores as Accuracy 0.99, Precision 0.98,
Recall 0.99, F1 0.98, and compares them directly against baselines drawn from Dadkhah
et al. [15]: Logistic Regression at Precision 0.144 / F1 0.432, AdaBoost at 0.141 /
0.141, DNN at 0.649 / 0.522, Random Forest at 0.691 / 0.551.

A 19-class precision of 0.144 alongside an accuracy of 0.727 is arithmetically possible
only under **macro** averaging. The baselines are therefore macro-averaged.

The replication confirms the proposed model's figures are **weighted**: weighted
precision 0.99, recall 0.99, F1 0.98 — matching Table 1 exactly — against macro
precision 0.82, recall 0.76, F1 0.75.

**The paper compares its own weighted scores against other authors' macro scores.**
The stated margin (0.98 against 0.432) is an artefact of the mismatch. The correct
comparison is 0.75 macro against 0.432–0.551 macro, which is a real but far smaller
improvement.

### 3.3 Severe: minority-class failure is mischaracterised

Section V.B.3 states that "classes like Spoofing and Recon-VulScan presented more
challenges for the model, with **slightly lower** precision and recall values compared
to the DDoS and DoS classes."

Verified replication values:

- Recon-VulScan: precision **0.00**, recall **0.00**, F1 **0.00** — the model never
  predicts this class
- Recon-OS_Scan: recall **0.01**, F1 **0.03**
- MQTT-DDoS-Publish_Flood: recall **0.12**, F1 **0.20**
- Spoofing: F1 **0.40**

Four classes are effectively or entirely undetected. "Slightly lower" is not an
accurate description of a class with zero recall.

### 3.4 Severe: no per-class results are published

The paper provides confusion matrix figures but **no per-class precision/recall/F1
table** for any task. A reader cannot determine that four classes are failing without
independently re-running the model. This is what makes the mischaracterisation in §3.3
consequential rather than merely imprecise.

### 3.5 Severe: class imbalance is documented and then ignored

Section III.C explicitly lists the class distribution, including the 112:1 ratio. The
method section specifies categorical cross-entropy with no class weighting, no
resampling, no focal loss, and no macro-averaged reporting. The imbalance is
acknowledged as a dataset property and never treated as a modelling problem.

### 3.6 Significant: internal contradictions in reported results

**Binary task.** Section V.B.1: "The accuracy was 100%, with a precision of 0.91 for
benign traffic and 1.00 for attack traffic." Table 1, 2-class row: accuracy 0.99,
precision 0.99. These are inconsistent with each other. The replication gives accuracy
0.9965 and benign precision 0.92 — neither 100% nor 0.91.

**Abstract.** "achieving a perfect accuracy of 99%" — 99% is not perfect accuracy.

**Six-class task description.** Section V.B.2 states the task "involved distinguishing
between five types of Distributed Denial of Service (DDoS) and Denial of Service (DoS)
attacks, alongside benign traffic." This is incorrect: the six classes are Benign,
DDoS, DoS, MQTT, Recon, and Spoofing. The same paragraph then cites
"MQTT-DDoS-Publish Flood and MQTT-Malformed Data" as six-class categories — these are
19-class labels.

**Spoofing omitted from the six-class discussion entirely**, despite the replication
showing it as by far the weakest class at that granularity (F1 0.38).

**Figure references.** Section V.B.2 refers the reader to both Fig 3 and Fig 4 for the
six-class confusion matrix; Fig 4 is captioned as the 19-class matrix.

### 3.7 Significant: methodological gaps

| Gap | Evidence |
|---|---|
| **Early stopping claimed but not applied** | Section IV.C: "enabling early stopping if overfitting is detected." Epochs fixed at 10; replication ran all 10 with no callback. |
| **No random seed** | Not specified in the paper; not present in the repository code path exercised by the replication. Results are not reproducible bit-for-bit. |
| **Single run, no variance** | No repeated seeds, no confidence intervals, no significance testing. |
| **No hyperparameter search reported** | Section IV.C attributes choices to "preliminary experimentation" without presenting it. |
| **No architecture ablation** | The contribution of each layer is asserted, never measured. |
| **Feature-order sensitivity untested** | Since convolution operates over the feature axis, results depend on column ordering. Never acknowledged or ablated. |
| **Capture provenance unaddressed** | Uses the shipped within-capture split; leakage is neither tested for nor discussed. |

### 3.8 Minor: novelty claim contradicted by the paper's own references

The abstract positions the work as distinct from "previous studies that predominantly
utilized traditional machine learning (ML) models or simpler Deep Neural Networks
(DNNs)." Reference [9] in the same paper is Rbah et al. (2024), *Deep Learning for
Enhanced IoMT Security: A GNN-BiLSTM Intrusion Detection System* — neither traditional
ML nor a simpler DNN. References [16] and [18] are also CNN-based IoMT intrusion
detection work.

### 3.9 What the paper gets right

For balance, and because the project depends on it:

- The code is **publicly available and runs**, which is why replication was possible
  at all. This is better practice than much of the surrounding literature.
- The architecture is **clearly and completely specified** — layer counts, filter
  sizes, activations, optimizer, batch size, epochs. There was no guesswork in
  reproducing it.
- The Discussion **acknowledges** difficulty distinguishing closely related attack
  variants and identifies feature engineering as the needed direction. That
  observation is correct and is where this project begins.

---

## 4. How this paper is used

The paper is a **baseline to be reproduced, not a foundation to be extended.**

| Role | Notebooks | Purpose |
|---|---|---|
| Faithful reproduction, shipped split | NB09 | Confirm the published result is obtainable. **Complete.** |
| Same model, capture-disjoint split | NB10 | Measure the leakage effect |
| Own architecture | NB12 onward | Sequence model, developed independently |

**Rule: the baseline is never improved, tuned, or corrected.** Its flaws are reproduced
intact. If the architecture is modified, any observed performance drop can be
attributed to the modification rather than to the evaluation protocol, and the central
claim collapses.

Code separation is enforced at the directory level: `baselines/mohammadi/` (pinned to a
commit hash, minimally adapted only to read project split files) and `src/` (own
pipeline). No shared model code.

**Comparisons are always like-for-like.** The project's capture-disjoint results are
never compared against the paper's published 0.98. That figure is cited separately as
the claim under examination.

---

## 5. Research objectives

**Objective 1 — Establish an honest performance baseline.**
Quantify the effect of capture-file leakage on reported detection performance for
CICIoMT2024, and develop a sequence-based detector evaluated under capture-disjoint
splits using macro-averaged metrics.

**Objective 2 — Recover the underrepresented attack classes.**
Diagnose why minority classes fail, evaluate class-imbalance interventions
independently, and document the resulting gains alongside their cost to majority-class
performance.

**Objective 3 — Translate detection into actionable threat intelligence.**
Map model explanations to established attack patterns (CAPEC) and threat categories
(STRIDE), validate the mappings computationally, and assess whether postmarket
surveillance can capture the threats identified.

---

## 6. Research questions and hypotheses

### Objective 1

**RQ1.** To what extent does capture-file leakage inflate reported detection performance
on CICIoMT2024, and does sequence-based modelling improve detection once that leakage
is removed?

- **H1.** Under capture-disjoint evaluation, macro-F1 will fall below the value obtained
  under the shipped within-capture split by more than 0.05.
- **H1b.** Under capture-disjoint evaluation, the sequence model will achieve higher
  macro-F1 than the single-record baseline, by more than the across-seed standard
  deviation.

### Objective 2

**RQ2.** Can class-imbalance interventions recover the attack classes that
macro-averaged evaluation reveals as failing, and what is the cost to majority-class
performance?

- **H2.** At least one intervention will raise macro-F1 above baseline by more than the
  across-seed standard deviation, with a proportionally smaller decrease in
  majority-class F1.

### Objective 3

**RQ3.** Can model explanations be systematically linked to established attack patterns
and threat categories, and does postmarket surveillance capture the threats so
identified?

- **H3a.** SHAP profiles will differ significantly between attack classes mapped to
  different STRIDE categories (permutation test, α = 0.05).
- **H3b.** Feature attributions will be stable across seeds (Kendall's τ ≥ 0.7 on top-10
  features).
- **H3c.** The proportion of MAUDE records attributable to cyberattack will be
  negligible relative to documented incident rates.

### 6.1 Revision history and rationale

| Original RQ | Revised RQ | Evidence prompting the change |
|---|---|---|
| How accurately can a hybrid GAT-LSTM **predict** cyber threats **before those threats fully manifest**? | How accurately can the model **identify** threats **from partial observations**, and how many records must be observed before each class becomes reliably identifiable? | Each capture file contains one attack class throughout; the label at *t+L* equals the label at *t* almost everywhere. A persistence baseline saturates, making the original hypothesis unfalsifiable. Reframing preserves the operational value (early alerting) while measuring a property the data contains. |
| Does adding **graph-based spatial context** improve predictions, and which threat classes are more accurately predicted? | Does modelling traffic as **sequences rather than single records** improve detection, and which threat classes benefit most? | Conditional on §12.1. If the CSVs carry no endpoint identifiers, no observed topology exists; a constructed graph derived from the same features the model already reads gives attention no additional information. The second clause is retained unchanged and becomes the primary minority-class objective. |
| Can **predictions** be mapped to STRIDE via CVE/CAPEC linked to MAUDE? | Can model **explanations** be mapped to STRIDE via CVE/CAPEC linked to MAUDE? | The mapping operates on SHAP attributions, not raw class predictions — a precision correction. Validation moves from expert inter-rater agreement to computational tests, as expert raters are unavailable. The computational tests are also stronger: they assess whether structure is present in the data rather than whether a small panel concurred. |

---

## 7. Prerequisites

### 7.1 Environment

- Python 3.10+, dedicated conda environment
- TensorFlow (matching the replication) and/or PyTorch — commit to one for own work
- scikit-learn, pandas, numpy, SHAP, matplotlib, seaborn, statsmodels (McNemar), PyYAML
- GPU: the 19-class replication took **~104 minutes on A100** and **~7 hours on T4**.
  Budget accordingly.
- Storage: 100 GB+ if pcap reprocessing proves necessary

Pin exact versions. Colab upgrades TensorFlow without notice:

```bash
conda env export --no-builds > environment.yml
pip freeze > requirements-lock.txt
```

### 7.2 Access, confirmed before work begins

- CICIoMT2024 full download (CSVs; pcaps conditional)
- Mohammadi repository, cloned and **pinned to a commit hash**
- MITRE CAPEC and CVE data
- FDA MAUDE bulk download files

### 7.3 Governance artefacts, created before any experiment

| File | Contents |
|---|---|
| `PREREGISTRATION.md` | RQs, hypotheses, numeric failure thresholds |
| `RESULTS_LEDGER.md` | Append-only. Corrections appended, never overwritten |
| `config/base.yaml` | Frozen constants: seed, split ratios, window, stride, metric |
| `config/feature_families.yaml` | Exact column lists per family |
| `DECISIONS.md` | Each decision, its evidence, and its date |

---

## 8. Data decisions

Decisions are grouped by whether the evidence already determines them.

### 8.1 Determined by evidence

| # | Decision | Basis |
|---|---|---|
| 1 | **19-class as primary task** | Macro-F1 collapses to 0.75 there; four classes fail; 2-class is saturated at 0.96 macro and uninformative |
| 2 | **Capture-disjoint splits throughout** | Shipped split verified as within-capture (`X_train` / `X_test` halves of the same recording) |
| 3 | **Macro-F1 as primary metric** | Weighted averaging demonstrably conceals four failing classes |
| 4 | **Timing family isolated and droppable** | Timing features are the most plausible carriers of capture provenance; must be ablatable as a group |
| 5 | **Scalers fit on training data only** | Fitting before splitting is itself a leak, and would undermine the leakage argument being made about others |
| 6 | **Baseline reproduced, never modified** | Required for the leakage delta to be attributable |

### 8.2 Open, requiring a decision

| # | Decision | Options | Note |
|---|---|---|---|
| 7 | **Benign split strategy** | Benign appears to originate from a single capture, so it cannot be capture-disjoint in the way attacks can. Contiguous-block splitting with the limitation declared is the defensible choice. | Unavoidable asymmetry. Must be declared, not discovered by an examiner. |
| 8 | **Session definition for chunked families** | `ICMP1` / `ICMP2` — two sessions, or one session in two chunks? | Changes what "disjoint" means for that family. Resolve against CIC documentation. |
| 9 | **Window and stride** | Fix before any sequence experiment | Observation-budget values must be ≤ window length |
| 10 | **Second dataset for cross-corpus transfer** | Recommend **out of scope** | Adding a corpus reintroduces provenance learning one level up. Leave-one-family-out within CICIoMT2024 tests generalisation and is tractable. List cross-dataset transfer as future work. |

---

## 9. Methodology and pipeline

### Stage 1 — Confirm the leakage mechanism
Train a simple model on **timing features only**, capture-disjoint. Near-perfect
performance indicates those features encode capture provenance rather than attack
behaviour.
*Supports RQ1. Gate: a negative result here requires reframing before proceeding.*

### Stage 2 — Rebuild the evaluation
Construct splits where no capture session contributes to both training and test.
Validation must also be capture-disjoint from training, or hyperparameter selection
leaks.
*Produces the protocol all subsequent results use.*

### Stage 3 — Establish the honest baseline
Run the reproduced Mohammadi CNN under the capture-disjoint split. Compare against the
verified within-capture result (macro-F1 0.75).
*The difference is the first substantive finding.*

### Stage 4 — Build the sequence detector
Restructure input from `(samples, features, 1)` to `(samples, T, features)`, ordered by
capture-internal sequence. Conv1D over the **time** axis, then LSTM.
*Supports H1b. Note this is a new model, not an extension of the baseline.*

### Stage 5 — Recover the weak classes
Diagnose first (§1.3 already provides this), then apply remedies matched to each
failure mode, **one at a time**:

1. Post-hoc logit adjustment — no retraining, τ tuned on validation
2. Class-weighted loss
3. Focal loss (γ swept from 2.0)
4. Window-level resampling, applied strictly after splitting
5. Per-class threshold tuning for macro-F1

*Supports RQ2. Trade-off against majority classes reported explicitly.*

### Stage 6 — Ablation
CNN-only / LSTM-only / hybrid; with and without rebalancing; with and without the
timing family.
*Establishes whether the hybrid earns its complexity.*

### Stage 7 — Generalisation
- **Leave-one-family-out:** train without an attack family, test on it
- **Observation budget:** restrict to the first *k* records, sweep *k*, plot macro-F1
  and per-class F1 against *k*

*Produces a per-class curve regardless of outcome — this stage cannot return empty.*

### Stage 8 — Explainability
SHAP on the **timing-excluded** model only. Explaining a model that reads capture
provenance yields an explanation of file identity.
*Feeds Stage 9.*

### Stage 9 — Threat-intelligence mapping
Map SHAP attributions to CAPEC patterns, then to STRIDE categories, using a
**deterministic rule fixed in advance** and drawn from published sources:

- CAPEC entries provide structured Prerequisites, Indicators, and Execution Flow fields
- CAPEC→STRIDE correspondence is documented in existing threat-modelling literature
- CICIoMT2024's own paper defines each attack's behaviour

Validation is computational (H3a, H3b), not judgmental. The claim is **linkability**,
not causality: SHAP describes what the model used, not what the attacker did.

### Stage 10 — MAUDE gap analysis
Assess what proportion of MAUDE records are attributable to cyberattack.
*The expected finding is a documented surveillance blind spot rather than a validation
corpus. This is publishable independently.*

---

## 10. Experimental sequence

| # | Notebook | Purpose | Supports |
|---|---|---|---|
| 01 | Load and inventory | Record counts, schema, dtypes, missing values | All |
| 02 | Class and capture distribution | Class-to-file mapping table | §8.2 #8 |
| 03 | EDA and feature distributions | Publication figures | Ch. 4 |
| 04 | **Leakage diagnostic** | Timing-only model | RQ1 **[GATE]** |
| 05 | Weak-class feature inspection | Are Spoofing's protocol markers intact? | RQ2 |
| 06 | Preprocessing pipeline | Encoders, scalers, feature families | All |
| 07 | Split builder | Both protocols saved to disk | RQ1 |
| 08 | Sequence windowing | `(samples, T, features)`, capture-bounded | H1b |
| 09 | **Mohammadi reproduction, shipped split** | **Complete — macro-F1 0.75** | RQ1 |
| 10 | Same model, capture-disjoint | The leakage delta | H1 |
| 11 | Single-record baseline | Does sequence modelling matter? | H1b |
| 12 | Sequence hybrid | Own architecture | H1b |
| 13 | Ablation | Layer and feature-family contribution | H1b |
| 14 | Frozen baseline + metric switch | Saved predictions, confusion matrix | RQ2 |
| 15 | Logit adjustment | Cheapest intervention | H2 |
| 16 | Class-weighted loss | | H2 |
| 17 | Focal loss | | H2 |
| 18 | Window-level resampling | | H2 |
| 19 | Per-class threshold tuning | | H2 |
| 20 | Best combination | Final configuration | H2 |
| 21 | Seed stability | 5 seeds, mean ± sd | H2 |
| 22 | Significance testing | McNemar, Holm-Bonferroni | H1, H2 |
| 23 | Leave-one-family-out | Attack vs. capture memorisation | RQ1 |
| 24 | Observation budget sweep | macro-F1 vs. *k* | RQ1 |
| 25 | SHAP | Timing-excluded model only | RQ3 |
| 26 | CAPEC mapping | Deterministic rule | RQ3 |
| 27 | STRIDE categorisation | | RQ3 |
| 28 | Computational validation | Permutation test, Kendall's τ | H3a, H3b |
| 29 | MAUDE gap analysis | | H3c |
| 30 | Consolidated results | Generated from saved artefacts | Ch. 4 |
| 31 | Final figures | | Ch. 4 |

---

## 11. Practical guidance

### 11.1 Artefact preservation — the recurring failure

The completed replication saved **no model checkpoints and no per-sample predictions**,
only stdout and confusion matrices. McNemar testing against it is therefore impossible
without a full retrain.

**Standing rule: every training run writes five files before it prints anything.**

```python
def save_run(outdir, config, y_true, y_pred, model, metrics):
    os.makedirs(outdir, exist_ok=True)
    json.dump(config,  open(f"{outdir}/config.json", "w"),  indent=2)
    json.dump(metrics, open(f"{outdir}/metrics.json", "w"), indent=2)
    np.save(f"{outdir}/y_true.npy", y_true)
    np.save(f"{outdir}/y_pred.npy", y_pred)
    model.save(f"{outdir}/model.keras")
```

Place this **inside the training function**, and on Colab call it at the end of the
training cell — never in a separate cell. Separate cells do not execute if the session
disconnects, which is precisely how checkpoints are lost.

### 11.2 Determinism

No seed was set in the replication; it is not reproducible bit-for-bit. Set one before
any model construction:

```python
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED); np.random.seed(SEED); tf.random.set_seed(SEED)
```

Add `tf.config.experimental.enable_op_determinism()` for runs that appear in the
dissertation; omit while exploring, for speed.

### 11.3 Development subsampling

The 19-class task runs 179,021 steps per epoch. Build a stratified 1% subsample once
and default to it:

```python
FAST = os.environ.get("FAST", "1") == "1"
data = load_subsample() if FAST else load_full()
```

Every notebook then runs end to end in under two minutes, catching shape errors, label
mismatches, and broken save paths before committing GPU hours. Set `FAST=0` only for
ledger runs. This is the single largest time saving available.

### 11.4 Config-driven experiments

Each intervention is a config diff rather than a separate notebook:

```yaml
# config/exp_focal.yaml
run_id: NB17_focal_g2_seed42
base: config/base.yaml
loss: focal
focal_gamma: 2.0
```

The "one change per run" rule then enforces itself — two configs can be diffed — and
the config file doubles as the ledger entry.

### 11.5 Cached intermediates

Preprocessing and windowing are computed once and written to disk. Hash the artefacts
and record the hash in every config, so input mismatches are detectable rather than
silent.

### 11.6 Automated results assembly

```python
df = collect_runs("results/")   # run_id, seed, config diff, macro_f1, per-class F1
```

Chapter 4 tables regenerate on demand. No transcribed numbers.

### 11.7 Colab workflow

- Two-tier repository: `notebooks/` (authored, outputs stripped) and `runs/` (executed,
  committed from Colab, never re-edited). Nothing is edited in two places.
- Install `nbstripout` on the source tier.
- Disable Colab's automatic Drive save, or Drive silently becomes a competing copy.
- Open notebooks via `File → Open notebook → GitHub`, not from Drive.
- SSH host aliases defined in local `~/.ssh/config` do not resolve in Colab; use
  Colab's GitHub authorization or HTTPS with a token.
- Capture the git SHA in cell 1 of every GPU notebook.
- Add a per-epoch `ModelCheckpoint` writing to Drive. A 7-hour T4 run that disconnects
  at hour six loses everything otherwise.

### 11.8 Standing methodological rules

- **One change per run.** Two changes and a moved score teaches nothing about either.
- **Tune on validation; touch test once.** Repeated test-set consultation converts it
  into training data.
- **Log every run, including failures.** The record of what was rejected is part of the
  result.
- **Ledger is append-only.**
- **Notebooks import from `src/`.** Logic living only in a cell cannot be tested or
  reused.
- **Re-run the full chain before writing Chapter 4.** Consolidation surfaces
  discrepancies against exploratory numbers; find them while they remain fixable.

---

## 12. Open verification items

These block downstream decisions and are **not** yet established. They are listed
explicitly because assuming any of them would compromise the record.

### 12.1 CSV feature schema `[UNVERIFIED — BLOCKING]`

**Question:** do the released CSVs contain (a) a timestamp column, and (b) source or
destination identifiers?

**Not verified.** The executed notebook never printed the column schema.

**Why it blocks:**
- No timestamp → sequence ordering must rely on row order as a proxy for capture order.
  Defensible, but must be declared as an assumption, not assumed silently.
- No endpoint identifiers → no observed device topology, and the graph-based direction
  in the original RQ2 cannot be supported from CSVs.

**Resolution:** print `df.columns.tolist()` and `df.head()` from one train CSV. One
command. Do this first.

### 12.2 Validation/test separation in the baseline `[UNVERIFIED]`

**Question:** in `src/main.py`, is `validation_data` the test set?

The replication logs show per-epoch `val_accuracy` and a separate final test
evaluation over 50,444 batches (≈1,614,182 records, matching the test set exactly). If
validation and test are the same partition, the baseline performed model selection on
its test set.

**Resolution:** inspect `main.py` directly. This affects how the baseline is described,
not whether it is used.

### 12.3 Session structure of chunked families `[UNVERIFIED]`

51 train files and 21 test files against 19 classes means some families are split
across multiple captures (`ICMP1`, `ICMP2`). Whether these are independent sessions
determines what capture-disjoint means for those families.

**Resolution:** CIC documentation plus pcap metadata.

### 12.4 Benign capture provenance `[UNVERIFIED]`

Whether benign traffic originates from one capture or several determines whether §8.2
#7 is a constraint or a non-issue.

---

## 13. Summary of position

**Established:** the published baseline has been faithfully reproduced; its reported
figures are weighted averages; recomputed macro-F1 for the 19-class task is 0.75
against a reported 0.98; four classes are effectively undetected; the benchmark's
shipped split is within-capture.

**Argued:** reported performance in this area has outrun its evaluation, and the
correction is measurable.

**To be measured:** the size of the leakage effect, whether sequence modelling helps
once leakage is removed, how far the weak classes can be recovered and at what cost,
how much observation each class requires, and whether model explanations carry
structure that maps onto established threat taxonomies.

**Constraint accepted:** the project's own evaluation must be beyond reproach, because
its central argument is about the evaluation practices of others. Every hypothesis
carries a stated failure condition fixed in advance, and a result that contradicts
expectation is reported rather than reframed.
