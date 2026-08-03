# AG_PRAXIS — Project Record

**Grounding Medical Device Threat Models in Observed Network Behaviour**

Doctoral praxis · GWU SEAS/EMSE
Dataset: CICIoMT2024 · Foundation model: Mohammadi et al. (2024), arXiv:2410.23306
Prior praxis in program: Bogan (2025)

**Version 1.0 · 3 August 2026**

---

> **This file is the single source of truth for the project.**
> Attach it, and only it, when starting a new chat. Everything a parallel
> conversation needs is here. Files marked superseded in Section 10 must not be
> used as reference.

---

## 1. Thesis statement

Threat models for connected medical devices are built at design time against assumed
adversaries. This research grounds them in observed traffic, establishing how early
each threat class becomes identifiable, whether sequence context improves detection of
similar attacks, and whether model explanations can be translated into structured
threat intelligence. *(48 words)*

| Field | Value |
|---|---|
| Research Product | ML-driven threat modeling pipeline |
| Format | Git repository: Python modules, notebooks, versioned artifacts, CAPEC/STRIDE mapping tables |
| Deliverable Usage | Security teams convert detection events into structured CAPEC/STRIDE threat records; researchers evaluate IoMT detectors under capture-aware protocols |
| Industry | Biotech / medical devices |
| Scope | The evaluation protocol applies to any intrusion-detection benchmark built from per-class capture sessions. The mapping method applies to any attack corpus with published attack semantics |

---

## 2. Problem statement

Threat models for connected medical devices are built once at design time against
assumed adversaries, while the attack surface moves: IoT devices carrying
vulnerabilities grew 136% in one year, and 80% of IoMT vulnerabilities are critical
(Forescout, 2024). Twenty-eight percent of healthcare organizations attacked reported
increased patient mortality (Ponemon & Proofpoint, 2024), and Section 524B now mandates
postmarket monitoring, yet nothing converts an observed attack into a threat record.

**Elaboration 1.** Operating over Wi-Fi, Bluetooth, and mobile apps in home networks
the manufacturer does not control, these devices face conditions no design-time model
anticipated.

**Elaboration 2.** Detection models that could close that loop are evaluated on
benchmarks whose recording structure lets features identify the session rather than the
attack, and FDA postmarket surveillance has no cybersecurity category.

**References**
- Forescout Technologies. (2024). *The Riskiest Connected Devices in 2024.*
- Ponemon Institute & Proofpoint. (2024). *Cyber Insecurity in Healthcare 2024.*
- Section 524B, Federal Food, Drug, and Cosmetic Act (2022).

---

## 3. Objectives, questions, hypotheses

| | Research Objective | Research Question | Hypothesis | Metric | Notebooks |
|---|---|---|---|---|---|
| **1** | Develop and validate a sequence-based neural architecture that models the temporal structure of IoMT network traffic, and determine how much observation each threat class requires before it becomes reliably identifiable. | How accurately can a model identify cyber threats targeting health monitoring wearables and remote patient hubs from partial observations, and how many records must be observed before each threat class becomes reliably identifiable? | Reconnaissance and low-rate attack classes will require at least twice as many observed records to reach F1 >= 0.80 as volumetric flooding classes. | Records observed to reach F1 >= 0.80, per class | 04, 06, 08 |
| **2** | Determine whether modelling traffic as sequences of records rather than single records improves detection of the attack variants that flow-level features do not separate. | Does modelling traffic as sequences rather than single records improve threat detection in RPH networks, and which threat classes benefit most? | Sequence-based detection will achieve mean pairwise F1 at least 0.05 above single-record classification on attack pairs within the same family. | Mean pairwise F1, within-family pairs | 05, 06, 07, 08 |
| **3** | Develop an automated pipeline that assigns SHAP-based feature explanations to CAPEC attack patterns and STRIDE threat categories, and corroborate the resulting threat records against FDA MAUDE adverse events. | Can model explanations be mapped to STRIDE threat categories via a CAPEC ontology pipeline linked to MAUDE signals, to produce actionable threat intelligence for health monitoring wearables and RPH? | For at least 70% of attack classes, the deterministic mapping will assign a STRIDE category consistent with that class's documented attack semantics in the CICIoMT2024 benchmark paper. | Proportion of classes with a consistent STRIDE assignment | 09 |

### Group definitions — fixed by the benchmark taxonomy, not by measurement

- **Volumetric:** DDoS-ICMP, DDoS-SYN, DDoS-TCP, DDoS-UDP, DoS-ICMP, DoS-SYN,
  DoS-TCP, DoS-UDP
- **Low-rate:** Recon-OS_Scan, Recon-Ping_Sweep, Recon-Port_Scan, Recon-VulScan,
  Spoofing, MQTT-Malformed_Data
- **Within-family pairs:** any two classes sharing a family prefix (Recon, MQTT,
  DDoS, DoS)

### Reported results — not hypothesis tests

| Result | Notebook | Role |
|---|---|---|
| Capture identifiability | 03 | Justifies running SHAP on a timing-excluded model |
| Baseline reproduction, macro vs weighted | 05 | Comparison point |
| Class-imbalance interventions, per-class costs | 07 | Second route to "which classes benefit most" |
| Leave-one-family-out generalisation | 08 | Robustness |
| Attribution stability, Kendall's tau | 09 | Reported with the mapping |
| MAUDE cyber-attributable share | 09 | Corroboration and surveillance coverage |

### Scope exclusions and their basis

- **Graph modelling** — the 45 released columns contain no source or destination
  identifiers. No topology is recoverable.
- **Lookahead prediction** — each capture holds a single class throughout, so the label
  at *t+L* equals the label at *t* almost everywhere.
- **Zero-day detection** — 19 labelled classes; nothing is unseen at training time.
- **Real-time operation and edge deployment** — no latency measurement, no edge
  hardware. Training and inference time recorded as a feasibility observation only.
- **CVE as a mapping input** — CVE identifies vulnerabilities in named software
  products; the evidence here is network behaviour. CVE identifiers are attached where a
  CAPEC pattern already carries them, as complementary enrichment only.
- **Ontology-based NLP** — the mapping operates on SHAP attributions against structured
  CAPEC fields. No text corpus.
- **Dashboard, ISO/IEC 42001 conformance** — not built, not assessed.
- **Cross-dataset transfer** — zero-shot transfer between CICIoMT2024 and a second IoMT
  corpus was tested and did not generalise: macro-F1 0.477 and 0.410 across the two
  directions, with one direction failing to beat a majority-class baseline. Protocol
  encodings differ substantially between the corpora. Leave-one-family-out within
  CICIoMT2024 is the generalisation test.

---

## 4. Dataset

**CICIoMT2024** (Dadkhah et al., *Internet of Things* 28:101351, 2024). 40 IoMT devices,
25 real and 15 simulated, across Wi-Fi, MQTT, and Bluetooth. 18 attack types.

| Property | Value |
|---|---|
| Files | 72 CSVs — 51 train, 21 test |
| Columns | 45 |
| Rows | 8,775,013 |
| Classes | 19 |
| Captures | 57 |
| Imbalance, 19-class | 2,157.7 : 1 |
| Imbalance, 6-class / 2-class | 328.6 : 1 / 37.1 : 1 |
| Largest class | DDoS-UDP, 1,998,026 rows |
| Smallest class | Recon-Ping_Sweep, 926 rows |
| Timestamp column | **None** |
| Endpoint identifiers | **None** |
| Constant across dataset | DHCP, Drate — dropped |

### Capture structure

**Tier A — 8 classes, multiple captures each.** DDoS-ICMP, DDoS-SYN, DDoS-TCP,
DDoS-UDP, DoS-ICMP, DoS-SYN, DoS-TCP, DoS-UDP. Chunk numbering restarts per partition,
so the shipped split is already capture-disjoint for these classes.

**Tier B — 11 classes, one capture each.** Benign, Spoofing, five MQTT classes, four
Recon classes. The shipped split divides one recording roughly 80/20, so it is
within-capture. Splits are rebuilt by contiguous block.

### Label parsing rule

```python
def parse_capture(filename):
    n = os.path.basename(filename).replace('.pcap.csv', '')
    partition = 'test' if n.endswith('_test') else 'train'
    n = re.sub(r'_(train|test)$', '', n)
    capture_id = n
    label = re.sub(r'\d+$', '', n).replace('TCP_IP-', '')
    if label == 'ARP_Spoofing':
        label = 'Spoofing'
    return {'capture_id': capture_id, 'label': label, 'partition': partition}
```

---

## 5. Findings to date

All figures below are from full-data reference runs unless marked.

### Feature separability

| Finding | Value |
|---|---|
| Median best single-feature AUC, 171 class pairs | 0.9987 |
| Pairs separable at AUC 0.90 by one feature | 160 of 171 |
| Least separable pair | Recon-OS_Scan / Recon-Port_Scan, 0.6585 on Rate |
| Top feature by mutual information, 19-class | IAT, 2.6074 nats |
| Features zero in more than 90% of rows | 14 of 43 |
| Feature pairs above 0.95 correlation | 14 |

**Eleven pairs below AUC 0.90**, all within Tier B:
Recon-OS_Scan/Recon-Port_Scan 0.6585 · Recon-Port_Scan/Recon-VulScan 0.7394 ·
Recon-OS_Scan/Recon-VulScan 0.7395 · MQTT-Malformed_Data/Spoofing 0.7934 ·
Benign/Spoofing 0.7958 · MQTT-DDoS-Publish_Flood/MQTT-Malformed_Data 0.8182 ·
MQTT-DDoS-Publish_Flood/Spoofing 0.8256 · Benign/MQTT-Malformed_Data 0.8438 ·
MQTT-DoS-Publish_Flood/MQTT-Malformed_Data 0.8503 · Recon-VulScan/Spoofing 0.8708 ·
MQTT-DoS-Publish_Flood/Spoofing 0.8730

### Feature provenance

| Test | Accuracy |
|---|---|
| Capture identification, all 43 features, 50 captures (chance 0.02) | 0.9340 |
| Capture identification, attack class held fixed | **0.9427** |
| Timing family only: Duration, Rate, Srate, IAT | 0.9364 |
| The five features named by prior work | 0.9444 |
| Protocol family, 27 features | 0.2471 |
| Statistical family, 12 features | 0.1280 |
| Attack macro-F1, whole capture held out (Tier A) | 0.9993 |
| Attack macro-F1, rows pooled (Tier A) | 0.9995 |

**Consequence:** four timing features identify the source recording nearly as well as
all 43. SHAP therefore runs on a timing-excluded model in NB09, so the threat mapping
describes attack behaviour rather than recording conditions.

**No column is constant within a capture while varying across captures**, so provenance
is carried by distributional shift, not by any column acting as a label. *(Screen run at
1% sampling; repeat at full scale in NB01.)*

### Reproduced baseline — Mohammadi et al., shipped split

| Task | Accuracy | Weighted F1 | Macro F1 |
|---|---|---|---|
| 2-class | 0.9965 | 1.00 | 0.96 |
| 6-class | 0.9950 | 1.00 | 0.87 |
| 19-class | 0.9870 | 0.98 | **0.75** |

Four classes effectively undetected at 19-class: Recon-VulScan 0.00, Recon-OS_Scan 0.03,
MQTT-DDoS-Publish_Flood 0.20, Spoofing 0.40. In the six-class task Spoofing scores 0.38
while accuracy reads 0.995.

---

## 6. Relation to prior work

### Foundation model — Mohammadi et al. (2024)

Reproduced without modification as the baseline. Their input tensor is
`(samples, features, 1)`, so the convolution slides across the feature axis and each
sample is a single record. Restructuring to `(samples, T, features)` implements the
temporal modelling their paper describes. Their Discussion identifies difficulty
distinguishing closely related attack variants and names feature engineering as the
needed direction — which is the gap RQ2 addresses.

**Rule: the baseline is never tuned, corrected, or improved.** Code lives in
`baselines/mohammadi/`, pinned to a commit hash, separate from `src/`.

### Prior praxis — Bogan (2025)

Cited as prior work to extend, never critiqued. Four positive anchors:

1. His future-work section names the nineteen-class imbalance problem as open — the
   warrant for RQ2.
2. He recommends alternative resampling methods — the warrant for the intervention set.
3. He established macro-averaged evaluation on this dataset — credited as prior
   adoption, not claimed as novel.
4. He observed different top-five SHAP features between Random Forest and Extra Trees —
   the motivation for measuring attribution stability with Kendall's tau.

**Open verification:** his Table 3-1 labels models `SGKF`, undefined in his
abbreviations list where every other reference is `SKF`. Verify before NB05.

### Positioning against the literature

| RQ | What exists | The gap filled |
|---|---|---|
| 1 | Early detection on CICIDS-2017, CICIoT23-WEB, MQTT-IoT-IDS2020, IoTID20. "Earliness" is the established metric | No earliness study on CICIoMT2024; none per class. The partial-flow study names single-dataset reliance as future work |
| 2 | CNN-LSTM for IoMT exists (SafetyMed; UNet++/LSTM) | Applied to the specific attack variants the foundation paper names as unresolved, with per-pair results |
| 3 | SHAP on CICIoMT2024 is well populated. CAPEC mapping exists for IoT logs via LLM. STRIDE exists for device risk assessment | No pipeline connects SHAP attributions from IoMT network traffic to CAPEC and STRIDE. An April 2026 IoMT XAI review names inconsistent explainability metrics as a key gap |

### Not claimed as novel

- Macro-averaging on this dataset — Bogan's
- SHAP on this dataset — Bogan's and several others'
- The CAPEC-to-STRIDE correspondence — published, cited not derived

---

## 7. Experimental programme

| # | Notebook | What it does, plainly | Serves |
|---|---|---|---|
| 01 | Dataset Inventory | Reads every file, counts what is in them, works out how the recordings are organised | Setup |
| 02 | Exploratory Analysis | Looks at what the measurements contain and which attacks are hard to tell apart | Setup |
| 03 | Feature Provenance Check | Tests whether the measurements identify the recording session rather than the attack | Justifies 09 |
| 04 | Preprocessing and Splits | Cleans the data, builds train and test splits, groups records into sequences | All |
| 05 | Baseline Models | Rebuilds the published model and a simple comparison model | H2 |
| 06 | Sequence Model | Builds the model that reads sequences of records instead of single ones | **H1, H2** |
| 07 | Class Balancing | Tests five ways of making the rare attacks visible, one at a time | H2 |
| 08 | Evaluation and Significance | Repeats runs across seeds, tests whether differences are real, measures how few records are needed | **H1, H2** |
| 09 | Explainability and Threat Mapping | Explains what the model used, maps it to CAPEC and STRIDE, checks against MAUDE | **H3** |
| 10 | Results Consolidation | Builds every table and figure for the results chapter | Chapter 4 |

Notebooks 01 to 03 have been run in an earlier numbering scheme. Their results are in
Section 5. Notebook 01 is rebuilt as a merge and re-run at full scale to confirm
reproduction and finalise the constancy screen.

---

## 8. Working rules

### Experimental discipline

- **One change per run.** Enforced mechanically, not by intention:

```python
def assert_single_change(cfg, parent):
    diff = {k for k in cfg if cfg[k] != parent.get(k)} - {'parent', 'run_id'}
    assert len(diff) <= 1, f"Two changes in one run: {diff}"
    return diff
```

  Called at the top of every training cell. The run will not start otherwise.

- **Every run is a config file** inheriting from a parent and overriding one key.
  The config is the ledger entry.

- **Every training run writes five files** as the last statement of the training cell,
  never in a separate cell — a Colab disconnect loses separate cells:
  `config.json`, `metrics.json`, `y_true.npy`, `y_pred.npy`, and the model.

- **Tune on validation. Evaluate test once per configuration.**

- **Seed 42** set before any model construction. Five seeds for reported results.

- **Macro-F1 is primary.** Macro and weighted always reported together.

- **Log every run, including failures.** `RESULTS_LEDGER.md` is append-only.

### Notebook writing style

Markdown cells are written in the voice of a student explaining their own experiment.
Plain, direct, sequential. No jargon, no inflated phrasing, no specification-form
templates. Each notebook explains itself from first principles and does not refer to
earlier projects or archived results.

Prohibited: "leverage", "robust", "comprehensive", "seamless", "delve", "underscore",
"it is worth noting", "furthermore", "moreover". No closing summary cells, no "next
steps" cells, no emoji.

### Fixed parameters

| Parameter | Value |
|---|---|
| Seed | 42 |
| Split | 70 / 15 / 15, two-tier |
| Window | 50 records |
| Stride | 25 records |
| Batch size | 32 |
| Epochs | 10 |
| Primary metric | macro-F1 |
| Significance test | McNemar, Holm-Bonferroni |
| Seeds for reported results | 5 |

---

## 9. Environment and workflow

### Locations

| Thing | Path |
|---|---|
| Repository (Mac) | `~/Documents/AG_PRAXIS/` |
| GitHub | `AGREWAL14/AG_PRAXIS`, SSH alias `github-agrewal14` |
| Data | `MyDrive/AG_PRAXIS_data/csv/` — 51 train, 21 test |
| Artifacts | `MyDrive/AG_PRAXIS_artifacts/NB0X/` |
| Compute | Google Colab, A100 for full runs |

### Repository layout

```
AG_PRAXIS/
├── PROJECT_RECORD.md      <- this file, single source of truth
├── PREREGISTRATION.md     <- append-only, holds the amendment history
├── RESULTS_LEDGER.md      <- append-only
├── DECISIONS.md           <- append-only
├── CLAUDE.md              <- rules read by Claude Code
├── config/                <- base.yaml, feature_families.yaml, runs/
├── notebooks/             <- authored on Mac, outputs stripped
├── runs/                  <- executed copies from Colab, never re-edited
├── src/                   <- importable modules
├── baselines/mohammadi/   <- pinned, never modified
├── data/processed/        <- splits, schema, inventories
└── results/               <- metrics JSONs, figures
```

### The loop

1. Claude Code writes the notebook into `notebooks/`
2. Mac: `git add . && git commit && git push`
3. Colab: File > Open notebook > GitHub, run
4. Colab: File > Save a copy in GitHub, path `runs/AG_PRAXIS_NB0X_title_executed.ipynb`
   — change the path before clicking OK or the clean source is overwritten
5. Drive: download the JSON artifacts from `AG_PRAXIS_artifacts/NB0X/`
6. Mac: `git pull`, move files into `data/processed/`, commit, push

Colab cannot push from a code cell, so notebooks write to Drive, never to the cloned
repo. Files reach the repo from the Mac.

---

## 10. Superseded documents

These remain in the repository for history and **must not be used as reference**:

| File | Superseded because |
|---|---|
| `docs/RESEARCH_DESIGN_CONSOLIDATED.md` | Framed around benchmark leakage; objectives have since been restated as timeliness, sequence benefit, and threat mapping |
| `docs/TEN_DAY_PLAN.md` | Built for a 31-notebook programme, replaced by the 10 in Section 7 |
| `docs/PROPOSAL_RECORD.md` | Baseline critique retained as background; RQ and hypothesis content superseded |
| `docs/MID_PROJECT_REVIEW.md` | Its recommendations are incorporated here |

`PREREGISTRATION.md` is **not** superseded. It holds the dated amendment history and its
value is that it was written before results. Section 3 of this file states the current
position; the pre-registration states how it was reached.

---

## 11. Open items

| Item | Action |
|---|---|
| Per-capture constancy screen at full scale | Run in NB01 |
| `config/feature_families.yaml` empty | Fill and mark reviewed before NB04 |
| `SGKF` labels in Bogan's Table 3-1 | Verify before NB05 |
| Benign contiguous-block boundaries | Fix in NB04, declare as a limitation |
| H3 reference standard | Confirm whether MITRE's published CWE-CAPEC-ATT&CK chain is in scope |
| Wearable and RPH framing | Verify the device inventory supports a wearable-specific claim, or move that framing to motivation |
