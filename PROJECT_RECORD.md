# AG_PRAXIS — Project Record

**Sequence-Based Intrusion Detection and Threat Modeling for Internet of Medical
Things Networks**

Doctoral praxis · GWU SEAS/EMSE
Dataset: CICIoMT2024 · Foundation model: Mohammadi et al. (2024), arXiv:2410.23306
Structural exemplars: Bogan (2025), the prior praxis in this program; NeCamp (2026)

**Version 1.10 · 16 August 2026**

---

> **This file is the single source of truth for the project.**
> Attach it and PREREGISTRATION.md when starting a new chat. This file states the
> current position; the pre-registration holds the class sets, thresholds and
> exclusion rules that the hypotheses depend on. Files marked superseded in
> Section 10 must not be used as reference.

---

## 1. Thesis statement

A sequence-based detection model detects attacks on medical device networks that
single-record models miss, at an observation cost that differs by attack class, and
its explanations can be translated into a standard threat model. Reading consecutive
records gives the model temporal context that quiet attacks reveal only over time, and
matching the features that drove each detection to published attack patterns turns a
class label into threat information a security team can act on. *(74 words)*

| Field | Value |
|---|---|
| Research Product | ML-driven threat modeling pipeline: a sequence-based IoMT detector whose explanations resolve to CAPEC attack patterns and STRIDE threat categories |
| Format | Git repository: Python modules, notebooks, versioned result artifacts, CAPEC/STRIDE mapping tables |
| Deliverable Usage | Converts detection events into structured CAPEC/STRIDE threat records, and sizes the traffic needed to detect each attack class |
| Industry | Biotech / medical devices |
| Scope | The mapping method applies to any attack corpus with published attack semantics; the observation-budget method applies to any per-class labelled traffic benchmark |
| Deliverable | Per-class threat model table: attack class, features that drove detection, CAPEC attack pattern, STRIDE threat category. Chapter 4, numbered table |

---

## 2. Problem statement

Threat models for connected medical devices are built once at design time against
assumed adversaries, while the attack surface moves: IoT devices carrying
vulnerabilities grew 136% in one year, and 80% of IoMT vulnerabilities are critical
(Forescout, 2024). Twenty-eight percent of healthcare organizations attacked reported
increased patient mortality (Ponemon & Proofpoint, 2024), and Section 524B now mandates
postmarket monitoring, yet no automated route runs from detection output to a structured
threat record.

**Elaboration 1.** Detection models trained on single network records catch volumetric
attacks but score below F1 0.50 on five of the nineteen CICIoMT2024 classes, including
the reconnaissance classes that mark the stage before damage is done. Reading records in
sequence is the obvious remedy, but which classes it helps and what it costs on the
classes already detected are open questions.

**Elaboration 2.** Detectors report a class label without saying what threat it
represents, leaving security teams to map output to CAPEC and STRIDE by hand, and FDA
postmarket surveillance has no cybersecurity category under which the result could be
recorded.

**References**
- Forescout Technologies. (2024). *The Riskiest Connected Devices in 2024.*
- Ponemon Institute & Proofpoint. (2024). *Cyber Insecurity in Healthcare 2024.*
- Section 524B, Federal Food, Drug, and Cosmetic Act (2022).

---

## 3. Objectives, questions, hypotheses

| | Research Objective | Research Question | Hypothesis | Metric | Notebooks |
|---|---|---|---|---|---|
| **1** | Build a sequence-based intrusion detection model for medical device networks and establish which attack classes it detects that single-record models miss. | Does a sequence-based model detect attack classes that a single-record model fails to detect? | A sequence-based model will detect attack classes that the published single-record model fails to detect, raising them above an F1 score of 0.50. | Per-class F1 change, sequence against single-record; classes recovered against lost across the F1 0.50 detection floor. Macro-F1 reported as context (near-flat, +0.0028 against the published CNN — the aggregate that conceals the per-class trade) | 05, 06, 07, 08 |
| **2** | Measure how much network traffic must be observed before each attack class can be detected. | How much traffic must be observed before detection of each attack class stops improving with further observation, and does this differ between quiet and loud attacks? | Quiet, low-rate attack classes will require more observed traffic than loud, volumetric attack classes before detection stops improving. | Observation budget to reach each class's saturation point, within epsilon = 0.02 of its achievable ceiling; low-rate against volumetric group medians compared | 04, 06, 08 |
| **3** | Translate the model's explanations into a standard threat model that a security team can act on. | Do the features driving the model's detections match published attack patterns closely enough to produce a threat model? | For at least fifteen of the eighteen attack classes (80%), the top-10 features of the timing-excluded sequence model will match a published CAPEC attack pattern, and each matched pattern will resolve to a STRIDE threat category. | Proportion of the 18 attack classes receiving a CAPEC assignment; pass mark 15 of 18. Semantic agreement with documented attack semantics reported alongside, against a majority-class baseline | 09a, 09b |

The runs H1 compares are scored on different units and different splits, 49,159 windows
against 1,614,182 and 1,229,711 records, so they are four runs' own scores rather than a
paired comparison. Two of the classes recovered across the detection floor carry the
thin-class caveat fixed in `PREREGISTRATION.md` Amendment 4: Recon-VulScan rests on 18
test sequences and MQTT-Malformed_Data on 40.

Saturation marks where a class stops improving, not where it becomes reliably detectable.
Eight of nineteen classes saturate at an F1 below 0.80. The budget grid is {5, 10, 25,
50}, so a group median can take only one of those values or a midpoint between two, and
the resolution of any comparison between medians is limited by the grid. Epsilon is 0.02,
recorded here and in `RESULTS_LEDGER.md`, and recoverable from
`data/processed/NB08/tables/saturation.csv` as the difference between `best_f1` and
`f1_there`.

### Group definitions — fixed by the benchmark taxonomy, not by measurement

- **Volumetric:** DDoS-ICMP, DDoS-SYN, DDoS-TCP, DDoS-UDP, DoS-ICMP, DoS-SYN,
  DoS-TCP, DoS-UDP
- **Low-rate:** Recon-OS_Scan, Recon-Port_Scan, Recon-VulScan, Spoofing,
  MQTT-Malformed_Data
- **Within-family pairs:** any two classes sharing a family prefix (Recon, MQTT,
  DDoS, DoS)

Recon-Ping_Sweep is excluded from the low-rate median under `PREREGISTRATION.md`
Amendment 4: at window 50 and stride 25 its 926 records yield 2 validation and 4 test
sequences, too few for a per-class metric to be interpretable. Its per-class figures are
reported, marked as resting on too few sequences to interpret. The same exclusion
applies to the H1 class set under Amendment 6.

### Reported results — not hypothesis tests

| Result | Notebook | Role |
|---|---|---|
| Capture identifiability | 03 | Justifies running SHAP on a timing-excluded model |
| Duration ablation, capture identification with the TTL column removed | 03b | Measures Duration's contribution to the NB03 figures, under `PREREGISTRATION.md` Amendment 13 |
| Baseline reproduction, macro vs weighted | 05 | Comparison point |
| Class-imbalance interventions, per-class costs | 07 | Per-class benefit, which classes gain most from intervention |
| Attribution stability, Kendall's tau | 09b | Reported with the mapping |
| Semantic agreement of the resolved STRIDE category | 09b | Whether the category the pipeline resolves matches the attack semantics documented in the benchmark paper. 9 of 18 for the sequence model, 0.500, against a majority-class baseline of 0.667; 6 of 18 for the forest, 0.333 |
| MAUDE cyber-attributable share | 09b | Surveillance coverage |
| DoS and DDoS pair separability under window aggregation | 06d | What the sequence model's volumetric losses are. Diagnostic of a reported result; tests no hypothesis and moves no comparator |
| Dadkhah et al. published baselines (RF 0.551, DNN 0.522, etc.) | 05 | Shared published-baseline anchor; also the comparator Mohammadi et al. cite. Context, not an H1 test. |
| RF ablation: Dadkhah Table 8 config on capture-disjoint split (macro-F1 0.8680) | 05 | Isolates split protocol from Dadkhah's published 0.551; context, not an H1 test. |

Dadkhah et al.'s own baselines are context rather than a result of this project. Verified
against the source PDF on 2026-08-07: 19-class Random Forest F1 0.551 from their Table 7, a
file-level 80/20 split by PCAP file from their Section 5, and no averaging method stated
anywhere in the paper. H1's comparator remains the published CNN. These figures position the
work; they do not test it. Section 6 carries the detail.

### Scope exclusions and their basis

- **Graph modelling** — graph approaches have been applied to this benchmark by
  constructing edges from feature similarity above a fixed threshold rather than from
  observed communication (Chethan et al., 2026). The 45 released columns contain no
  source or destination identifiers, so any graph built over them is imposed by the
  similarity rule chosen rather than observed. This work models temporal structure
  rather than topological structure.
- **Lookahead prediction** — each capture holds a single class throughout, so the label
  at *t+L* equals the label at *t* almost everywhere.
- **Zero-day detection** — 19 labelled classes; nothing is unseen at training time.
- **Real-time operation and edge deployment** — no latency measurement, no edge
  hardware. Training and inference time recorded as a feasibility observation only.
- **CVE and the MITRE chain as mapping inputs** — CVE identifies vulnerabilities in
  named software products; the evidence here is network behaviour. CVE identifiers are
  attached where a CAPEC pattern already carries them, as complementary enrichment only.
  MITRE's CWE-CAPEC-ATT&CK chain is attached on the same footing, as secondary reference
  alongside CVE, and is not a mapping input for H3.
- **Ontology-based NLP** — the mapping operates on SHAP attributions against structured
  CAPEC fields. No text corpus.
- **Dashboard, ISO/IEC 42001 conformance** — not built, not assessed.
- **Cross-dataset transfer** — zero-shot transfer between CICIoMT2024 and a second IoMT
  corpus was tested and did not generalise: macro-F1 0.477 and 0.410 across the two
  directions, with one direction failing to beat a majority-class baseline. Protocol
  encodings differ substantially between the corpora. No substitute generalisation test
  is claimed in its place, and no hypothesis rests on one.
- **Conformal prediction** — run as a feasibility probe in `NB06b_cp_scores` and
  `NB06c_cp_feasibility`, whose executed copies are in `runs/`. The probe returned a
  negative and conformal prediction was dropped. `DECISIONS.md` under 2026-08-09
  records the outcome.

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
| Constant across dataset | Drate only — dropped |

The 45 released columns were reconciled on 2026-08-07 against Dadkhah et al.'s Table 5 and
against the CICIoT2023 schema it cites (Neto et al., *Sensors* 23(13):5941, 2023). All 39
Table 5 features are present: 38 match by name, and the thirty-ninth, Time-To-Live, is the
column named Duration, which CICIoT2023 lists with the description "Time-to-Live (ttl)". The
six columns beyond Table 5 are CICIoT2023 features checked against Neto et al.'s Table 4.
`config/feature_families.yaml` holds the full reconciliation.

### Feature extraction windows differ by class

Every row is a summary of a window of packets, and the window is not the same size for
every class. The dataset's authors extracted features over 100-packet windows for DDoS
and DoS traffic and over 10-packet windows for everything else. Doménech et al. (2025)
record this in their Section 5.1.1, argue that it alters the feature distribution across
classes, and recommend a uniform window. Read on 2026-08-15.

A row is therefore not a constant quantity of traffic. It summarises ten packets in one
part of the corpus and a hundred in another, and the boundary between the two falls
exactly on the boundary between the volumetric and low-rate groups defined in Section 3:
the volumetric group is the eight DDoS and DoS classes, which are the 100-packet classes,
and the low-rate group is drawn from the 10-packet remainder. Any observation budget
counted in records or in windows is therefore counted in units that differ in size
between the two groups, and the H2 group comparison carries that as a confound. No figure
in Section 5 changes and no hypothesis is restated; what changes is what a record means
when the two groups are read against each other. `NOTES_FOR_WRITING.md` carries the entry
for Chapter 3 and Chapter 5.

### Device inventory by protocol

From the testbed diagram in Dadkhah et al. (2024). The split by protocol decides what
the modelled data can support.

**Wi-Fi — 7 real devices, none a wearable.** Sense-U Baby Monitor, SOS Multifunctional
Pager, SINGCALL SOS Button, M1T laxihub, Owltron, Blink mini, Ecobee Camera.

**MQTT — 15 simulated devices, several of them wearables.** Lookee Ring Pro Sleep
Monitor, Wellue Visual Oxy Wrist Pulse Oximeter, Wellue EKG, an EMG sensor and a GSR
sensor, among others.

**Bluetooth — the remaining real devices, almost all wearables.** Checkme O2 wrist
oximeters, COOSPO armband heart rate monitors, Rhythm+ armband, Powrlabs chest strap,
LIVLOV heart rate sensor, Pulsebit EX EKG tracker, SleepU, Lookee Sleep Ring.

The 72 CSVs cover Wi-Fi and MQTT only. Bluetooth is released as pcap with no extracted
features, so no real wearable contributed a row to the data modelled here. Wearable
traffic in this subset is simulated MQTT traffic.

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

From the NB02 reference run: a full pass over all 8,775,013 rows, using the 44 features
that remain after Drate is dropped. Those 44 are the reconciled set described in Section 4,
in which Duration is the TTL header field rather than a measure of time.

| Finding | Value |
|---|---|
| Median best single-feature AUC, 171 class pairs | 0.9985 |
| Pairs separable at AUC 0.90 by one feature | 160 of 171 |
| Least separable pair | Recon-OS_Scan / Recon-Port_Scan, 0.6850 on Rate |
| Top feature by mutual information, 19-class | IAT, 2.1500 nats of 2.1940 available |
| Top feature, four weakest classes | IAT, 0.9703 of 1.1777 |
| Features zero in more than 90% of rows | 15 of 44 — reproduced by NB01 on 2026-08-08 |
| Feature pairs above r 0.95 | 14 |
| Largest between-recording shift | Protocol Type, ratio 0.23 on DoS-UDP |

**Eleven pairs below AUC 0.90**, all within Tier B:
Recon-OS_Scan/Recon-Port_Scan 0.6850 · Recon-Port_Scan/Recon-VulScan 0.7368 ·
Recon-OS_Scan/Recon-VulScan 0.7442 · MQTT-Malformed_Data/Spoofing 0.7847 ·
Benign/Spoofing 0.8010 · MQTT-DoS-Publish_Flood/MQTT-Malformed_Data 0.8514 ·
Benign/MQTT-Malformed_Data 0.8664 · Recon-VulScan/Spoofing 0.8671 ·
MQTT-DoS-Publish_Flood/Spoofing 0.8733 · MQTT-DDoS-Publish_Flood/MQTT-Malformed_Data
0.8753 · MQTT-DDoS-Publish_Flood/Spoofing 0.8930

An earlier screen put IAT's mutual information at 2.6074 nats. That figure is above the
label entropy, which is impossible, and it came from computing the score on a balanced
sample of 2,000 rows per class rather than on the data as recorded. The figures above use
the real class distribution.

### Feature provenance

From the NB03 reference run: RandomForest, 50 trees, `min_samples_leaf` 100, 30% of rows
held out for test, on the 44 features that remain after Drate is dropped. Every model is
trained on 8,000 rows drawn equally from each of the 50 recordings belonging to the 8
classes recorded more than once, so no recording can be identified by being larger than the
others and chance is one over the number of recordings.

| Test | Accuracy |
|---|---|
| Capture identification, all 44 features, 50 recordings (chance 0.0200) | 0.8010 |
| Capture identification, attack class held fixed (mean chance 0.1750) | **0.8280** |
| Timing family only: Duration, Rate, Srate, IAT | 0.9301 |
| The five features named by prior work | 0.9285 |
| IAT, Rate, Srate | 0.8935 |
| Protocol family, 28 features | 0.1802 |
| Statistical family, 12 features | 0.1198 |
| Attack macro-F1, whole recording held out | 0.9985 |
| Attack macro-F1, rows pooled | 0.9982 |
| Difference, pooled minus held out | -0.0003 |

**Duration is the TTL header field, and it was inside every figure above.** It sits within
the timing family for the 0.9301 row and among all 44 for 0.8010 and 0.8280. A full scan of
all 72 files and 8,775,013 rows puts its global maximum at exactly 255 and 93.57% of its
values at 64, so the column carries Time-To-Live and the timing family contains one header
field. With 93.57% of rows at the modal value, 6.4% of them vary. What that is worth is
measured rather than reasoned: NB03b ran the NB03 protocol again with Duration removed and
nothing else changed. On the fifty-way task, removing it costs 0.0366 on the timing
family, 0.9301 down to 0.8935, and 0.0515 across all features, 0.8010 down to 0.7495.
Duration alone identifies the recording at 0.0299 against a chance rate of 0.0200. With
the attack class held fixed, removing it raises the mean accuracy to 0.8504 from 0.8280,
up on five of the eight classes and down on three, one of them by 0.0001, and the five
increases sum to +0.2173 against -0.0376 for the three decreases. Every figure there is a
single run at seed 42 with no seed replicates, so what is measured is one run rather than
an estimate carrying a spread. The figure the timing-excluded SHAP design rests on is the
one with the attack class held fixed, and it does not fall when Duration is removed, so
the capture identifiability NB03 reports is not carried by the header field. The column
stays in the timing family and in the 44 by deliberate decision, for comparability with
runs already executed, and NB03b measures its contribution rather than changing the
feature set. `DECISIONS.md` under 2026-08-07 and 2026-08-10, and
`config/feature_families.yaml` under `duration_family_placement`, carry the decision.

NB01's near-constancy table, re-run on 2026-08-08, reproduces the modal share as 93.5743%
at 64.0 and flags it as a lower bound rather than an exact figure. The scan keeps exact
value counts only for columns taking fewer than 200 distinct values, and Duration exceeds
that cap, so the share it reports is at least 93.5743% and could be higher. The recorded
93.57% is consistent with that bound. Nineteen columns are more constant than Duration and
fourteen of those sit above 99%, so any rule that dropped a column for near-constancy would
reach those before it reached this one. `data/processed/near_constancy.json` holds the
table.

**Per class, attack held fixed:** DDoS-ICMP 0.8532 (chance 0.100) · DDoS-SYN 0.8784 (0.200)
· DDoS-TCP 0.8232 (0.200) · DDoS-UDP 0.6869 (0.100) · DoS-ICMP 0.7863 (0.200) · DoS-SYN
0.9177 (0.200) · DoS-TCP 0.8291 (0.200) · DoS-UDP 0.8489 (0.200). Across the eight, the
within-class models close 0.7915 of the distance between chance and being right every time.

An earlier run under the previous numbering, using 100 trees with no leaf constraint,
reached 0.9427 with the class held fixed. The constrained model here gives a lower bound on
the same effect.

**Consequence:** four timing features identify the source recording better than all 44
together, and three of them get most of the way there. SHAP therefore runs on a
timing-excluded model, which NB09a trains, so the threat mapping describes attack
behaviour rather than recording conditions. That model did not exist before NB09a: every
run executed up to it uses the 44 features, or 43 for the NB03b ablation. The identifiable
session is not being used to score points on these eight classes, where the two attack
protocols agree to within 0.0003 macro-F1, but it remains available to any model trained
on these columns and to any explanation read off one.

**No column is constant within a capture while varying across captures**, so provenance
is carried by distributional shift, not by any column acting as a label.

The full-scale scan in NB01 read all 8,775,013 rows and found one column constant across
the whole dataset, Drate, and no column constant within a recording while varying between
recordings. The two readings, one file per recording and one recording name per
recording, agree, so the finding does not depend on how files were grouped.

### Preprocessing and splits

From the NB04 reference run: every row of every file read once, the two-tier protocol,
window 50 and stride 25.

| Partition | Rows | Share | Sequences |
|---|---|---|---|
| Train | 6,228,288 | 71.0% | 249,061 |
| Validation | 1,317,014 | 15.0% | 52,637 |
| Test | 1,229,711 | 14.0% | 49,159 |

A sequence never crosses a file boundary. All 19 classes are present in all three
partitions.

**Fewest sequences, train / validation / test:** Recon-Ping_Sweep 24 / 2 / 4 ·
Recon-VulScan 86 / 18 / 18 · MQTT-Malformed_Data 191 / 38 / 40 ·
MQTT-DoS-Connect_Flood 444 / 92 / 94.

The timing-excluded input is defined in the manifest as a column slice rather than
written as a second array: drop Duration, Rate, Srate and IAT, leaving 40 features.

### Baseline models

From the NB05 reference run: seven runs, full pass, 303 minutes. Seed 42, and the 44
features that remain after Drate is dropped.

| run | model | task | split | accuracy | weighted F1 | macro F1 |
|---|---|---|---|---|---|---|
| ours_cnn_19class | mohammadi_cnn | 19-class | two_tier | 0.9852 | 0.9831 | 0.7356 |
| published_cnn_19class | mohammadi_cnn | 19-class | shipped | 0.9863 | 0.9840 | 0.7110 |
| forest_19class | random_forest | 19-class | two_tier | 0.9923 | 0.9906 | 0.8418 |
| ours_cnn_6class | mohammadi_cnn | 6-class | two_tier | 0.9945 | 0.9947 | 0.9006 |
| published_cnn_6class | mohammadi_cnn | 6-class | shipped | 0.9929 | 0.9931 | 0.8786 |
| forest_6class | random_forest | 6-class | two_tier | 0.9980 | 0.9980 | 0.9681 |
| published_cnn_2class | mohammadi_cnn | 2-class | shipped | 0.9968 | 0.9968 | 0.9651 |

The split protocol costs nothing. The same architecture with the same settings scores
0.7356 macro-F1 on the two-tier split against 0.7110 on the shipped split at nineteen
classes, and 0.9006 against 0.8786 at six. The two-tier figure is higher in both cases.
The test partitions differ in size and composition, so this is not evidence the two-tier
split is better, only that holding recording sessions apart does not cost performance.
This is the third measurement pointing the same way, after the 0.0003 difference NB03
measured on Tier A.

A random forest on single records beats both convolutional runs. 0.8418 macro-F1 against
0.7356 and 0.7110, trained on 999,998 rows in 21 seconds against 65 minutes,
cross-validated at 0.8958 plus or minus 0.0049. Per class the difference is largest where
the convolution fails: Recon-OS_Scan 0.7241 against 0.0519, Spoofing 0.8605 against
0.4167, Recon-Ping_Sweep 0.6884 against 0.5018.

Five classes are below F1 0.50 in both convolutional runs: Recon-VulScan,
Recon-OS_Scan, MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data. The forest
resolves three of them, Recon-OS_Scan from 0.0519 to 0.7241, Spoofing from 0.4167 to
0.8605, and MQTT-Malformed_Data from 0.4021 to 0.6752. It still fails
MQTT-DDoS-Publish_Flood at 0.1186 and Recon-VulScan at 0.2536, and those two are the
only classes no model reaches F1 0.50 on.

The weighted minus macro gap is 0.2474 on the two-tier nineteen-class run and 0.2730 on
the shipped one. Accuracy reads 0.985 and 0.986 on the same predictions.

Dadkhah et al.'s own published random forest, F1 0.551 at nineteen classes on their
file-level split with the averaging method unstated, sits alongside `forest_19class` at
0.8418 macro on the capture-disjoint split as the published anchor for this task. It is
the same anchor Mohammadi et al. cite, which is why it is recorded here rather than only
in the literature section. Reading the two numbers against each other carries three
confounds. Their averaging method is unknown, so 0.551 may not be a macro figure at all.
The split protocol differs, theirs by PCAP file and ours by capture session. The feature
count differs, since the paper lists 39, ships 45 and never says which its models used,
against the 44 used here. The comparison is a benchmark reference showing where this work
sits under a more rigorous protocol, not a controlled head-to-head win. Section 6 under
"Benchmark baselines — Dadkhah et al. (2024)" carries the verification detail.

An ablation run, `forest_19class_dadkhah_leaf1`, puts Dadkhah et al.'s own Table 8 forest
settings on the capture-disjoint split. It reaches 0.8680 macro-F1. The single change from
`forest_19class` is `min_samples_leaf` from 20 to 1, which is their exact Table 8 value.
The 44 features, seed 42, the two-tier split and the same 1,229,711 test rows are all
unchanged, so what the run varies is the leaf constraint and nothing else. Three numbers
now sit together: Dadkhah's published 0.551, their model configuration on their file-level
split; this ablation's 0.8680, their model configuration on the capture-disjoint split; and
`forest_19class` at 0.8418, the leaf setting chosen here on the same split. The leaf
constraint accounts for almost none of the distance between the published figure and the
runs here. It moves the score by 0.0262, 0.8680 at leaf 1 against 0.8418 at leaf 20, where
the distance from 0.551 is 0.3170 and 0.2911 respectively. What the ablation supports is
that the random forest configuration Dadkhah published, run under a capture-disjoint split,
scores far above the 0.551 their table reports, which places the difference in how the
result was evaluated rather than in what the model is capable of. The split protocol is one
half of that and the averaging method is the other, since the paper states no averaging
method and 0.551 may not be a macro figure at all. Neither the feature set nor the
averaging method is controlled by this run. The paper lists 39 features and ships 45
against the 44 used here, and the averaging remains unstated, so those two confounds stand
exactly where they stood before. This is a reported result and not a hypothesis test. It is
not a controlled comparison between two models, and it changes nothing about H1, whose
comparator remains the published CNN under Amendment 5.

### Reproduced baseline — Mohammadi et al., shipped split

| Task | Accuracy | Weighted F1 | Macro F1 |
|---|---|---|---|
| 2-class | 0.9965 | 1.00 | 0.96 |
| 6-class | 0.9950 | 1.00 | 0.87 |
| 19-class | 0.9870 | 0.98 | **0.75** |

Four classes effectively undetected at 19-class: Recon-VulScan 0.00, Recon-OS_Scan 0.03,
MQTT-DDoS-Publish_Flood 0.20, Spoofing 0.40. In the six-class task Spoofing scores 0.38
while accuracy reads 0.995.

These figures come from an earlier reproduction whose artifacts are not in
`results/NB05/`. The nearest run on disk, `published_cnn_19class`, reads macro-F1
0.7110 against 0.75 and Spoofing 0.3438 against 0.40. The six-class Spoofing figure
moves the opposite way, 0.38 recorded against 0.4094 on disk, so this is not a
rounding difference. The block is retained as a record of what was run; every figure
cited in Chapter 4 comes from the artifacts in `results/NB05/`.

### Sequence model

From the NB06 reference run: one run, full pass, 41 minutes. Seed 42, window 50 and
stride 25, the two-tier split, and the 44 features that remain after Drate is dropped.
The published convolutional encoder is applied to each record of the window with its
softmax head removed, one LSTM of 128 units reads across the 50 results, and a softmax
head sits on top. 214,227 parameters. The parent is `ours_cnn_19class` and the one
change is the model.

| run | input | test items | accuracy | weighted F1 | macro F1 | gap |
|---|---|---|---|---|---|---|
| sequence_cnn_lstm_19class | 50 records, two_tier | 49,159 windows | 0.8197 | 0.8064 | **0.7138** | 0.0926 |
| ours_cnn_19class | 1 record, two_tier | 1,229,711 rows | 0.9852 | 0.9831 | 0.7356 | 0.2474 |
| published_cnn_19class | 1 record, shipped | 1,614,182 rows | 0.9863 | 0.9840 | 0.7110 | 0.2730 |
| forest_19class | 1 record, two_tier | 1,229,711 rows | 0.9923 | 0.9906 | 0.8418 | 0.1488 |

The rows of that table are scored on different items. A window and a record are not the
same unit, and the shipped and two-tier splits hold out different rows, so these are four
runs' own scores rather than a paired comparison.

Macro-F1 is 0.7138. Against the parent, the same encoder reading one record at a time on
the same split, that is -0.0218. Against `published_cnn_19class`, the comparator H1 names,
it is +0.0028. The random forest on single records remains the highest macro-F1 recorded
in this project at 0.8418. Accuracy falls from 0.9852 on the parent to 0.8197, and the
weighted minus macro gap falls from 0.2474 to 0.0926.

NB08 places this figure in a cross-seed distribution: 0.7373 plus or minus 0.0233 over
five seeds at k = 50, of which 0.7138 is one. The +0.0028 difference against
`published_cnn_19class` is an order of magnitude inside that spread and is not reported
as a gain.

**The five classes the published run scores below F1 0.50:**

| class | published_cnn | ours_cnn | forest | sequence |
|---|---|---|---|---|
| Recon-VulScan | 0.0000 | 0.0144 | 0.2536 | **0.5385** |
| Recon-OS_Scan | 0.0343 | 0.0519 | 0.7241 | **0.6061** |
| MQTT-DDoS-Publish_Flood | 0.1858 | 0.0875 | 0.1186 | 0.0796 |
| Spoofing | 0.3438 | 0.4167 | 0.8605 | **0.7653** |
| MQTT-Malformed_Data | 0.4883 | 0.4021 | 0.6752 | **0.8421** |

Four of the five reach F1 0.50 or above, the threshold fixed in `PREREGISTRATION.md`
Amendment 5. MQTT-DDoS-Publish_Flood does not, and falls further, 0.1858 to 0.0796. It
and Recon-VulScan were the two classes no earlier model reached 0.50 on; Recon-VulScan is
now above it and MQTT-DDoS-Publish_Flood is not.

Across all nineteen classes against the published run, nine classes gained F1 and ten
lost. The gains sum to +2.0566 and the losses to -2.0033, a net of +0.0533 over nineteen
classes, which is the +0.0028 macro-F1 difference. One class crosses below 0.50:
DoS-ICMP, 0.9960 to 0.3178, a loss larger in magnitude than any single class's gain among
the five. The five largest losses are all volumetric classes, DoS-ICMP, DoS-TCP,
DDoS-ICMP, DoS-SYN and DDoS-TCP, summing -1.7662, which is 88% of the total negative
movement. The per-class table is in `RESULTS_LEDGER.md`.

Three classes sit below F1 0.50: DoS-ICMP 0.3178, MQTT-DDoS-Publish_Flood 0.0796 and
Recon-Ping_Sweep 0.0000. Recon-Ping_Sweep's figure rests on four test sequences and is
reported without being interpreted, under Amendment 4. Recon-VulScan at 18 test sequences
and MQTT-Malformed_Data at 40 carry the same caveat, and both are among the four classes
that cross the threshold.

**What the DoS-ICMP fall is.** The errors are not spread across the class set. Of 3,936
true DoS-ICMP windows, 2,996 are predicted DDoS-ICMP, 936 are correct, and four land
anywhere else, three on DDoS-UDP and one on Benign. So 2,996 of the 3,000 errors go to a
single class, and it is the other ICMP class. The confusion runs both ways: 1,017 of 7,826
true DDoS-ICMP windows are predicted DoS-ICMP, which is what holds DoS-ICMP's precision to
0.4790 against a recall of 0.2378, and DDoS-ICMP falls to 0.7721 alongside it. The traffic
is found in both cases; what the model cannot do is say which of the two it is. The same
pattern holds for the TCP and SYN pairs and not for the UDP pair, and the diagnosis is in
Section 11 under the DoS-ICMP row.

Almost all of the separability that survives averaging is carried by one feature, the
inter-arrival time. On the mean of a window it separates the two members of the ICMP pair
at 0.9601, the TCP pair at 0.9650, the SYN pair at 0.9711 and the UDP pair at 0.9649, and
on a single record it reads 0.9985 in all four. Set that one column aside and the ICMP
pair has nothing above 0.6877 left on the window mean, on Variance, and the UDP pair
nothing above 0.7380, on Rate and Srate. It is also one of the four timing features held
out of the models the explanations are read off, on the grounds that those four identify
the recording session rather than the attack. So the input that tells these pairs apart is
not one a detector should be built on, and the model is not simply declining to use a
signal that was there for the taking. Nothing measured here separates a session marker
from an attack property that happens to behave the same way. What can be said is that four
unrelated protocol pairs are separated by the same column at almost the same figure, and
that the column separates them by its level rather than by how much it moves inside a
window: on the window's standard deviation it reads 0.5496, 0.8035, 0.6799 and 0.5650,
below its figure on the mean in every pair.

Training took 2,427.7 seconds and inference 7.0 seconds over 49,159 windows, 6,985 windows
a second, recorded as a feasibility observation.

### Class balancing

From the NB07 reference run: five runs, full pass, 212 minutes. Seed 42, window 50 and
stride 25, the two-tier split, and the 44 features that remain after Drate is dropped. Each
run is one key from `sequence_cnn_lstm_19class`, which is the parent throughout, and all six
rows are scored on the same 49,159 test windows, so every difference below is a difference
on the same items. No significance test is computed here; that is NB08's.

| run | Recon-VulScan | Recon-OS_Scan | MQTT-DDoS-Publish_Flood | Spoofing | MQTT-Malformed_Data | volumetric mean | macro F1 |
|---|---|---|---|---|---|---|---|
| sequence_cnn_lstm_19class (parent) | 0.5385 | 0.6061 | 0.0796 | 0.7653 | 0.8421 | 0.7613 | 0.7138 |
| class_weighted_loss | 0.3729 | 0.6667 | 0.0717 | 0.4295 | 0.6000 | 0.6614 | 0.6481 |
| focal_loss | 0.3333 | 0.3377 | 0.0631 | 0.6667 | 0.9500 | 0.7524 | 0.6838 |
| logit_adjustment | 0.4746 | 0.5730 | 0.0631 | 0.7442 | 0.8706 | 0.7720 | 0.7238 |
| threshold_tuning | 0.3902 | 0.8193 | 0.0804 | 0.8406 | 0.8732 | 0.7643 | 0.7320 |
| window_resampling | 0.3768 | 0.8142 | 0.0541 | 0.8547 | 0.9756 | 0.7788 | 0.7699 |

Window resampling gives the largest gain on both quantities, 0.7699 macro-F1 against the
parent's 0.7138 and 0.7788 volumetric mean against 0.7613. Logit adjustment and threshold
tuning also raise both by smaller margins. Class-weighted loss and focal loss lower both.
Window resampling is the highest macro-F1 any sequence model has reached in this project
and remains below `forest_19class` at 0.8418 on single records.

**No intervention raises the count of the five detected at F1 0.50.** The parent detects
four of the five. Every intervention detects three or two. The cause is Recon-VulScan,
which falls under all five, from 0.5385 to somewhere between 0.3333 and 0.4746. It is the
class NB06 lifted across the threshold, and every balancing method pushes it back under.
It rests on 18 test sequences and carries the Amendment 4 caveat, so the direction is
consistent across five runs while the magnitude is not interpretable.

**MQTT-DDoS-Publish_Flood does not respond to any intervention**, scoring 0.0541 to 0.0804
against a parent of 0.0796, with no run reaching a tenth of the threshold. Five different
treatments of class imbalance produce no movement. `PREREGISTRATION.md` Objective 2 fixed
the reading of this outcome before any of it was run: evidence that the failure is not
caused by imbalance, directing attention to feature separability instead. NB02 is
consistent, placing the class in two of the eleven pairs below AUC 0.90.

**DoS-ICMP against the parent's 0.3178:** focal_loss 0.1594, window_resampling 0.2995,
class_weighted_loss 0.3516, logit_adjustment 0.3769, threshold_tuning 0.4590. No
intervention returns it above 0.50 and two leave it lower. These figures measure whether
balancing recovers the class, not what caused the regression.

The volumetric mean moves -0.1000, -0.0090, +0.0030, +0.0106 and +0.0174 across the five.
No H1 clause sets a limit on this quantity, since `PREREGISTRATION.md` Amendment 10 records
that Amendment 2's cost clause did not survive the Amendment 5 replacement, so these are
reported without a pass mark. The per-run detail is in `RESULTS_LEDGER.md`.

### Observation budgets and cross-seed variation

From the NB08 reference run: seven runs trained here, plus the NB06 parent loaded
without retraining. Seed 42 for the budget runs, seeds 43 to 46 at k = 50, window 50
and stride 25, the two-tier split, and the 44 features that remain after Drate is
dropped. Observation budget k in {5, 10, 25, 50} taken as prefixes of the NB04
windows, so all runs score the same 49,159 test windows. Parameters 214,227 in every
run, unchanged by the budget.

| budget | macro F1 | classes at F1 >= 0.80 |
|---|---|---|
| k = 5 | 0.6295 | 9 |
| k = 10 | 0.6837 | 9 |
| k = 25 | 0.7323 | 11 |
| k = 50 | 0.7138 | 10 |

**Records to threshold, a reported result.** This was the measurement the observation
hypothesis was stated on until `PREREGISTRATION.md` Amendment 12 moved H2 onto
saturation. It is retained and reported. Eight of nineteen classes do not reach F1 0.80
within 50 records and are recorded as right-censored under Amendment 11, reported as
"> 50" and never as 50.

Low-rate: Recon-Port_Scan 5, MQTT-Malformed_Data 25, Recon-OS_Scan > 50,
Recon-VulScan > 50, Spoofing > 50. Median not reached within 50 records, three of five
censored.

Volumetric: DDoS-SYN 5, DDoS-TCP 5, DDoS-UDP 5, DoS-SYN 5, DoS-UDP 5, DDoS-ICMP > 50,
DoS-ICMP > 50, DoS-TCP > 50. Median 5, three of eight censored. The even-sized group
reading is recorded in `DECISIONS.md` under 2026-08-09.

The twofold comparison the earlier statement of the hypothesis required is not
evaluated, since the low-rate median is not determinate. The direction is reported
instead: the low-rate median sits above the budget ceiling while the volumetric median
is 5, so low-rate classes require more observed records. The size of the difference is
not measurable on a grid that stops at 50. Amendment 12 states H2 with no numeric
multiple, so no comparison here carries a pass mark.

Two figures qualify that reading. DDoS-ICMP is censored at a best F1 of 0.7998, short
of the threshold by 0.0002 against a cross-seed standard deviation of 0.0075 on that
class. Recon-Port_Scan reaches 0.8878 at k = 5, so the fastest class in the study is a
low-rate one. The group definitions are fixed by the benchmark taxonomy in Section 3
and were not derived from these measurements.

Censoring marks two different situations. Of the censored classes in the two named
groups, DoS-ICMP, DoS-TCP and Recon-VulScan sit at their maximum F1 at k = 50, so
their "> 50" records a ceiling rather than an unmet observation requirement.
DDoS-ICMP, Recon-OS_Scan and Spoofing peak at a smaller budget and score lower at 50.
Two classes outside both groups follow the same two patterns: MQTT-DoS-Publish_Flood
sits at its maximum at 50, and MQTT-DDoS-Publish_Flood peaks at 10 and scores lower
at 50.

**Saturation (H2).** The smallest budget within 0.02 of each class's own best score
across the four budgets, following Silvey & Liu (JMIR 2024) and Mohr et al. (arXiv
2201.12150). This is the metric H2 is stated on under Amendment 12. Seven of nineteen
classes stop improving at k = 5. Eight saturate at an F1 below 0.80, so saturation
marks where a class stops improving and not where it becomes reliably detectable.
Per-class figures are in `RESULTS_LEDGER.md`.

Group medians, read from `data/processed/NB08/tables/saturation.csv`. Low-rate:
Spoofing 10, MQTT-Malformed_Data 25, Recon-OS_Scan 25, Recon-Port_Scan 50,
Recon-VulScan 50, median 25. Volumetric: DDoS-ICMP 5, DDoS-SYN 5, DDoS-TCP 5,
DoS-SYN 5, DDoS-UDP 25, DoS-UDP 25, DoS-ICMP 50, DoS-TCP 50, median 15, the mean of
the fourth and fifth values under the even-sized group reading recorded in
`DECISIONS.md` on 2026-08-09. Nothing is censored on this scale, since every class has
a best score across the grid and so has a budget at which it reaches it, so both
medians are determinate.

The low-rate median is 25 against a volumetric 15, a ratio of 1.67. H2 states the
direction only, so this is reported as an observed figure with no pass mark. The budget
grid is {5, 10, 25, 50}, so a median can take only one of those four values or a
midpoint between two of them. The ratio is therefore as much a property of the grid as
of the classes, and a finer grid would move it.

**Cross-seed variation.** Macro-F1 0.7373 plus or minus 0.0233 across five seeds at
k = 50. The NB06 figure of 0.7138 is one seed of those five and sits about one standard
deviation below the mean.

**Significance.** Eleven McNemar tests with Holm-Bonferroni correction, applied within
each family of six budget pairs and five intervention pairs, and again across all
eleven. Five of six budget pairs and three of five intervention pairs are significant at
alpha 0.05. The k = 25 against k = 50 pair is significant favouring k = 25, but only
k = 50 carries replicates and its cross-seed spread of 0.0233 exceeds the 0.0185 gap
between the two, so the curve is read as flat from k = 25 rather than declining.

No McNemar test is computed against `published_cnn_19class`. The two are scored on
different units, 49,159 windows against 1,614,182 rows, and on different splits, so no
item-level pairing exists. No substitute test was computed.

### Timing-excluded models

From the NB09a run of 2026-08-12, partial: the five sequence seeds and the forest fit
completed and the forest's attribution pass did not. Seeds 42 to 46, window 50 and stride
25, the two-tier split, and the 40 features that remain when Duration, Rate, Srate and IAT
are dropped from the 44.

| model | 44 features | 40 features | fall |
|---|---|---|---|
| forest_19class | 0.8418 | 0.5910 | 0.2508 |
| sequence_cnn_lstm_19class | 0.7138 | 0.6901 plus or minus 0.0236 over five seeds | 0.0237 |

The same four columns removed cost the two models very differently.

The sequence model at 40 features has 206,035 parameters against the parent's 214,227, the
encoder flattening over a narrower feature axis. Per seed the macro-F1 is 0.6747, 0.6714,
0.6947, 0.6805 and 0.7292. The forest figure is on 1,229,711 records and the sequence
figures on 49,159 windows, so the two rows are not scored on the same items.

---

## 6. Relation to prior work

### Foundation model — Mohammadi et al. (2024)

Reproduced without modification as the baseline. Their input tensor is
`(samples, features, 1)`, so the convolution slides across the feature axis and each
sample is a single record. Restructuring to `(samples, T, features)` implements the
temporal modelling their paper describes. Their Discussion identifies difficulty
distinguishing closely related attack variants and names feature engineering as the
needed direction — which is the gap RQ1 addresses.

**Rule: the baseline is never tuned, corrected, or improved.** Code lives in
`baselines/mohammadi/`, pinned to a commit hash, separate from `src/`.

### Prior praxis — Bogan (2025)

Cited as prior work to extend, never critiqued. Four positive anchors:

1. His future-work section names the nineteen-class imbalance problem as open — the
   warrant for RQ1.
2. He recommends alternative resampling methods — the warrant for the intervention set.
3. He established macro-averaged evaluation on this dataset — credited as prior
   adoption, not claimed as novel.
4. He observed different top-five SHAP features between Random Forest and Extra Trees —
   the motivation for measuring attribution stability with Kendall's tau.

**Verified 2026-08-04:** his Table 3-1 labels models `SGKF`, which appears nowhere in his
abbreviations list where every other reference is `SKF`, defined as Stratified K-Fold. The
labelling is a typographical error confined to that table, and plain stratified k-fold is
what was used. Section 11 records the checks the finding rests on.

### Structural exemplar — NeCamp (2026)

*AI-Based Intrusion Detection Systems for IoMT Devices*, GWU SEAS/EMSE, praxis
director Ould Vadel, final examination passed 1 April 2026. Verified against the
source PDF on 2026-08-16. Two research questions, two hypotheses, one dataset
(WUSTL-EHMS-2020), four models — Random Forest, XGBoost, Support Vector Machine and
an autoencoder — and binary classification. NeCamp uses Shapley values for feature
selection — choosing which features to train on. This work uses SHAP for explanation
— what the trained model relied on — and then translates those attributions into
CAPEC and STRIDE. The distinction is stated explicitly in Chapter 2 so the two are
not read as the same method.

### Benchmark baselines — Dadkhah et al. (2024)

**Verified 2026-08-07** against the source PDF rather than through Mohammadi et al.'s
transcription of it. Table 7 gives 19-class F1 of 0.432 for Logistic Regression, 0.141 for
AdaBoost, 0.522 for the DNN and 0.551 for Random Forest. Section 5 defines the shipped split
as 80% of all PCAP files for training and 20% for test, at file level rather than row level.
No averaging method is stated anywhere in the paper's 22 pages — "macro", "micro" and
"weighted" do not appear in it, and F1 is defined once, in its two-class form — so whether
their figures are macro, micro or weighted is unresolved in the source. Any comparison
against their 0.551 carries that ambiguity, the split difference, and a feature-count
difference the paper does not settle, since it lists 39 features and ships 45 without saying
which its own models used. `DECISIONS.md` under 2026-08-07 records the checks.

### Benchmark context — Chethan et al. (2026)

Chethan, G. S., Patil, N. S., Prakash, G. L., and Muneshwara, M. S. (2026). Adaptive
graph-based intrusion detection for Internet of Medical Things (IoMT) networks.
*Engineering, Technology & Applied Science Research*, 16(3), 36934-36941. DOI
10.48084/etasr.17590. Read against the PDF on 2026-08-14.

Two figures in it are independent confirmations this project can use. Their Table III
class counts agree with the dataset figures recorded in Section 4: 8,775,013 rows in
total, Recon-Ping_Sweep at 926 and DDoS-UDP at 1,998,026. Their Table V reproduces
Dadkhah et al.'s 19-class Random Forest F1 of 0.551, so that anchor is now confirmed by
a second reading of the source rather than by this project's alone.

### Benchmark context — published feature-importance rankings

Two further applications of this benchmark were read against their PDFs on 2026-08-14.

Gencturk, E., Ustubioglu, B., Ulutas, G., and Symeonidis, I. (2026). Class imbalance in
IoMT datasets: evaluating balancing strategies for learning-based attack detection.
*Applied Sciences*, 16(10), 4921. DOI 10.3390/app16104921. Four balancing methods across
ECU-IoHT, WUSTL and CICIoMT2024, five classical models and two deep models, seeds 42, 52
and 62.

Alkhodaidi, T., Alhalabi, W., and Almasre, M. (2026). Enhancing IoMT network threat
detection with data balancing for multi-class attack classification on CICIoMT2024
dataset. *Computers, Materials & Continua*, 88(2), 87. DOI 10.32604/cmc.2026.081665.

Both publish random forest feature importance on the 19-class task and both rank the same
timing features at the top. Gencturk et al. place IAT first by a wide margin with Rate and
Srate next. Alkhodaidi et al. give IAT 0.21, Rate 0.05 and AVG 0.04, and advise security
teams to monitor IAT and packet rate. Each reads the ranking as network-behaviour
signature, which is attack signal.

Those are the features the provenance results in Section 5 are measured on. The timing
family — Duration, Rate, Srate, IAT — identifies the source recording at 0.9301 on the
fifty-way task against a chance rate of 0.0200, and IAT, Rate and Srate alone, which is
Gencturk et al.'s top three, reach 0.8935 on the same task. Two independent rankings
therefore place at the top of a detector exactly the columns this project measures
carrying recording provenance. Neither paper measures provenance and neither is in
disagreement with anything recorded here; what the agreement supplies is external evidence
that these columns are the ones the literature relies on, which is what makes the
provenance measurement worth reporting.

Both also confirm the dataset figures in Section 4. Their class counts match, and
Gencturk et al.'s Table 5 gives Recon-Ping_Sweep an imbalance ratio of 2157.70 against the
2,157.7 : 1 recorded here. With Chethan et al. that is three published sources agreeing
with this project's counts.

### Positioning against the literature

| RQ | What exists | The gap filled |
|---|---|---|
| 1 | CNN-LSTM for IoMT exists (SafetyMed; UNet++/LSTM) | Applied to the specific attack variants the foundation paper names as unresolved, with per-pair results |
| 2 | Early detection on CICIDS-2017, CICIoT23-WEB, MQTT-IoT-IDS2020, IoTID20. "Earliness" is the established metric. Per-class earliness and minimum-number-of-packets on CICIDS-2017 is reported in arXiv 2201.11628, which is the named prior work this project's earliness measurement is adapted from | No earliness study on CICIoMT2024; none per class. The gap is stated against arXiv 2201.11628 specifically: that measurement exists on CICIDS-2017 and is adapted here to CICIoMT2024. The partial-flow study names single-dataset reliance as future work |
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
| 03 | Feature Provenance Check | Tests whether the measurements identify the recording session rather than the attack | Justifies 09a |
| 03b | Timing Feature Ablation | Measures how much of the recording-identification result comes from the TTL column | Premise for 07b |
| 04 | Preprocessing and Splits | Cleans the data, builds train and test splits, groups records into sequences | All |
| 05 | Baseline Models | Rebuilds the published model and a simple comparison model | H1 |
| 06 | Sequence Model | Builds the model that reads sequences of records instead of single ones | **H1, H2** |
| 06d | DoS and DDoS Pair Diagnosis | Works out what the model reading sequences actually gets wrong on the flooding classes, and whether averaging a window is what loses the distinction. Trains nothing | No hypothesis; diagnostic |
| 07 | Class Balancing | Tests five ways of making the rare attacks visible, one at a time | H1 |
| 07b | Capture-Invariant Training | Trains the model so it cannot tell the recordings apart, and checks which attacks come back. **Designed and not executed**, withdrawn under `DECISIONS.md` 2026-08-11 | H1 |
| 08 | Evaluation and Significance | Repeats runs across seeds, tests whether differences are real, measures how few records are needed | **H1, H2** |
| 08b | Adaptive Earliness | Lets the model decide when it has seen enough, instead of fixing the budget in advance. **Written and not executed**, parked under `DECISIONS.md` 2026-08-13 | RO2 |
| 09a | Attribution on Timing-Excluded Models | Trains the models that cannot see the timing measurements, and works out which of the remaining measurements each one used | **H3** |
| 09b | Threat Mapping and Surveillance | Turns those measurements into attack patterns and threat categories, checks them against the benchmark paper's own descriptions, measures how much the explanations move between seeds, and counts adverse event reports. Needs no GPU | **H3** |
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

- **Labels are never category dtype.** Pandas carries a categorical through groupby
  into the aggregation, and arithmetic on the result raises. Every frame that will
  be divided, averaged, or fed to a model asserts all columns numeric at
  construction.

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
├── config/                <- base.yaml, feature_families.yaml, runs/, and the four
│                             files the threat mapping reads: stride_ground_truth.yaml,
│                             shap_capec_map.yaml, capec_stride.yaml, maude_keywords.yaml
├── notebooks/             <- authored on Mac, outputs stripped
├── runs/                  <- executed copies from Colab, never re-edited
├── src/                   <- importable modules
├── baselines/mohammadi/   <- pinned, never modified
├── data/processed/        <- splits, schema, inventories
├── results/               <- metrics JSONs, figures
└── tools/dry_run/         <- runs a notebook locally against a miniature fixture
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

These are superseded and **must not be used as reference**. Three of the four are no
longer in the repository; only `PROPOSAL_RECORD.md` remains, at `archive/docs/`. All four
rows are kept, because what this section records is what existed and what replaced it, and
that does not depend on the file still being here.

| File | In the repository | Superseded because |
|---|---|---|
| `RESEARCH_DESIGN_CONSOLIDATED.md` | no | Framed around benchmark leakage; objectives have since been restated as timeliness, sequence benefit, and threat mapping |
| `TEN_DAY_PLAN.md` | no | Built for a 31-notebook programme, replaced by the 10 in Section 7 |
| `PROPOSAL_RECORD.md` | `archive/docs/` | Baseline critique retained as background; RQ and hypothesis content superseded |
| `MID_PROJECT_REVIEW.md` | no | Its recommendations are incorporated here |

`PREREGISTRATION.md` is **not** superseded. It holds the dated amendment history and its
value is that it was written before results. Section 3 of this file states the current
position; the pre-registration states how it was reached.

---

## 11. Open items

| Item | Action |
|---|---|
| `config/feature_families.yaml`, resolved | Reviewed and marked on 2026-08-04. The twelve columns ambiguous between protocol and statistical stay in protocol; the rationale, the evidence for it and the one open point are recorded in the file itself |
| `SGKF` labels in Bogan's Table 3-1, resolved | A typographical error. `SGKF` appears six times, all within that one table. `SKF` appears throughout the abbreviations list, the research questions, all of Chapter 4 and both confusion matrix captions, and is defined as Stratified K-Fold. No `SGKF` entry exists in the abbreviations list. The prose immediately below the table describes plain stratified k-fold cross-validation, five folds with no reserved validation portion, and no grouping variable is defined anywhere in the methodology. Plain `StratifiedKFold` is therefore the correct comparison |
| Benign split boundaries, resolved | Tier B classes concatenate their train and test files and cut at 70 and 85 percent of the whole, so a partition can span the file boundary. Benign trains on `Benign_train` rows 0 to 161,237, validates on `Benign_train` rows 161,237 to 192,732 plus `Benign_test` rows 0 to 3,056, and tests on the remainder of `Benign_test`. Stated as a design choice in Chapter 3 |
| Recon-Ping_Sweep sequence counts | 24 train, 2 validation, 4 test at window 50 and stride 25, from 926 records. Excluded from the low-rate median in H2 by `PREREGISTRATION.md` Amendment 4. The same exclusion rule is applied to the H1 class set in Amendment 6, which drops it from the classes the published CNN fails to detect despite its F1 of 0.0107 on that run |
| H3 reference standard, superseded | H3 no longer tests STRIDE consistency; it tests whether the top-10 features resolve to a CAPEC pattern. Semantic agreement against the attack semantics documented in the CICIoMT2024 benchmark paper is retained as a reported result, and `config/stride_ground_truth.yaml` remains the standard it is measured against. As originally recorded: MITRE's CWE-CAPEC-ATT&CK chain is in scope as a secondary reference, attached to the mapping output as enrichment in the same way CVE identifiers are, and is not part of what H3 tests |
| Wearable and RPH framing, resolved | The testbed splits by protocol: 7 real Wi-Fi devices, none a wearable; 15 simulated MQTT devices including several wearables; the remaining real devices on Bluetooth, almost all wearables. The 72 CSVs are Wi-Fi and MQTT only and Bluetooth is pcap-only, so no real wearable contributed a row to the modelled data. RQ2 no longer names wearables. Remote patient hub framing is retained: the Wi-Fi set includes a hub, an SOS pager, an SOS button and a baby monitor. Wearables remain in the dataset description in Section 4 |
| `MedSec-25.csv` and the cross-dataset transfer artefacts | Archived under `archive/data/` and excluded from git by size |
| H1's single-record baseline, resolved | H1 names the published CNN as its comparator. The five classes it fails to detect — Recon-VulScan, Recon-OS_Scan, MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data — and the 0.50 F1 threshold that defines both set membership and improvement are fixed in `PREREGISTRATION.md`, Amendments 5 and 6. The single-record random forest at 0.8418 macro-F1 is reported alongside as a third comparison, because it beats the published CNN |
| Row order and the sequence premise | H1 assumes CSV row order preserves capture order. Tested in NB04 before sequences are built |
| Low-rate group listing in Section 3, resolved | Section 3's low-rate bullet no longer lists Recon-Ping_Sweep, matching the group fixed by `PREREGISTRATION.md` Amendment 4, and the exclusion and its basis are now stated beneath the bullets. H2 names the median again in the same edit, restoring the aggregation Amendment 3 stated and v1.0 dropped. Both changes are recorded in Amendment 8 |
| Section 5 sentence on classes below F1 0.50, resolved | Both statements re-derived from `results/NB05/*/metrics.json` and corrected. First: five classes, not three, are below F1 0.50 in both convolutional runs — Spoofing and MQTT-Malformed_Data were missing — and the forest resolves three of the five, MQTT-Malformed_Data reaching 0.6752. Second: no run on disk produces the "Reproduced baseline" figures, so that block now carries a note recording that it comes from an earlier reproduction and that every figure cited in Chapter 4 comes from the artifacts in `results/NB05/` |
| DoS-ICMP regression under the sequence model, resolved | NB06 shows DoS-ICMP falling from 0.9960 (published CNN) to 0.3178, crossing below the F1 0.50 line — a loss larger in magnitude than any single class's gain among the five H1 classes. NB07 measured whether the five balancing interventions recover it: none returns it above 0.50, the five values being 0.1594, 0.2995, 0.3516, 0.3769 and 0.4590 against the parent's 0.3178, and two of the five leave it lower than the parent. That measures recovery under balancing, not cause. NB08 settled that it is not a seed artifact: across seeds 42 to 46 the class scores 0.3178, 0.3099, 0.3450, 0.2690 and 0.2938, so it is a stable property of window-based sequencing. NB06d diagnoses it. The regression is a within-pair confusion and not a failure to detect: of 3,936 true DoS-ICMP windows, 2,996 are predicted DDoS-ICMP and four go anywhere else, so 2,996 of 3,000 errors land on the other ICMP class, and 1,017 of 7,826 true DDoS-ICMP windows come back the other way, which takes DDoS-ICMP down to 0.7721 with it. The same pattern holds in the TCP and SYN pairs and not in UDP: within-pair confusion runs 0.001924 to 0.341183 for ICMP, 0.000650 to 0.268424 for TCP, 0.000790 to 0.136305 for SYN and 0.000837 to 0.011398 for UDP, record model against window model on the same split. Averaging is not the cause. Separability between the two members of a pair was scored per feature on pooled records and on the window mean, and the mean AUC lost is negative for all four pairs, -0.067768, -0.042848, -0.008505 and -0.053102, so the window mean separates these pairs better than a single record does. What separates the pairs after averaging is almost entirely one feature. IAT reads 0.9601 on the window mean for ICMP, 0.9650 for TCP, 0.9711 for SYN and 0.9649 for UDP, and 0.9985 per record in all four, which is near-identical across four unrelated protocol pairs. With IAT set aside the best that remains on the window mean is Variance at 0.6877 for ICMP, Header_Length at 0.8035 for TCP, Variance at 0.9840 for SYN, and Rate and Srate at 0.7380 for UDP, so neither the ICMP nor the UDP pair has anything above 0.74 left. IAT is one of the four timing features dropped for the timing-excluded models on provenance grounds, that family identifying which of fifty recordings a row came from at 0.9301 against a chance rate of 0.0200, so the input that separates these pairs is not one a detector should rely on and the open question is not why the model ignores a legitimate signal. Nothing measured here distinguishes a session marker from an attack property behaving the same way. What is observed is that IAT separates on level rather than on variation: on the window's standard deviation it reads 0.5496, 0.8035, 0.6799 and 0.5650, below its figure on the mean in every pair. `DECISIONS.md` under 2026-08-15 records the diagnosis and `data/processed/NB06d/pair_separability.json` carries the per-feature tables. No amendment was written because nothing in the design changed |
| RF comparator naming, resolved | Two random forests exist in this project and are easy to conflate. `results/NB05/forest_19class`, at 0.8418 macro-F1, is the classifier that serves as H1's third comparison and is the correct forest to cite against Dadkhah et al.'s published baseline of F1 0.551, recorded in `DECISIONS.md` under 2026-08-07. The NB03 capture-identification probe is a separate forest that tests whether recording provenance is recoverable from features; it does not classify attack classes and is not a comparator for H1 or H2. The two were conflated while the primary-source verification entry in `DECISIONS.md` was being drafted, and corrected before that entry was committed. Recorded here so they are not mixed up again |
| NB07b withdrawn | Designed, specified and costed, and not executed. `PREREGISTRATION.md` Amendment 16 established that 11 of the 45 training groups are single-capture classes where the group and the class are the same set of windows, and that all five classes fixed in Amendment 6 are among them; Amendment 17 established that the weights start uniform, so that coincidence is operative from the first update. On the class set the first dependent variable is evaluated over, the intervention is therefore class weighting, which NB07 already tested through five interventions, and what survives is the capture-invariance question on the 8 classes recorded more than once. `DECISIONS.md` under 2026-08-11 records the withdrawal and that no figure from the aborted run is recorded. Amendments 14, 16 and 17 stand as written and are not withdrawn |
| H2's twofold comparison not evaluable on the NB08 grid, superseded | NB08 measured records to threshold at k in {5, 10, 25, 50}. Three of five low-rate classes do not reach F1 0.80 within 50 records, so the low-rate median is not determinate and the twofold comparison the hypothesis then stated is not evaluated. The direction is reported instead, under `PREREGISTRATION.md` Amendment 11, which fixed this handling before the run. Extending the grid past 50 would require rebuilding the sequences at a longer window and is ruled out by the same amendment. The hypothesis is now H2 and Amendment 12 measures it on saturation, where both group medians are determinate, and states no numeric multiple. Records to threshold is retained as a reported result. Section 5 carries the figures |
| Conformal prediction scope, resolved | Run as a feasibility probe in `NB06b_cp_scores` and `NB06c_cp_feasibility`. The probe returned a negative and conformal prediction was dropped. Recorded in `DECISIONS.md` under 2026-08-09 and in Section 3 under scope exclusions |
| NB09a and NB09b executed, resolved | Both are run. NB09a completed across two sessions, the five sequence models and their explainer passes on an A100 on 2026-08-12 and the forest's TreeExplainer pass on a CPU runtime on 2026-08-13, which also wrote `attributions.json`; its artefacts are in `data/processed/NB09a/` and `results/NB09a/`. NB09b ran on 2026-08-13: H3 measured 18 of 18 classes resolving to a CAPEC pattern against a pass mark of 15, semantic agreement 9 of 18 for the sequence model and 6 of 18 for the forest against a majority-class baseline of 0.667, Kendall's tau 0.4560 across 19 classes, and MAUDE 1 keyword match in 829 reports; its artefact is `data/processed/NB09b/threat_mapping.json`. `RESULTS_LEDGER.md` carries both, the NB09a completion entry of 2026-08-13 superseding its partial entry of 2026-08-12. H3 is restated as chain resolution by `PREREGISTRATION.md` Amendment 20, which followed the run. The rules they run under are fixed in `PREREGISTRATION.md` Amendments 18 and 19: the sequence model at 40 features is what H3 is scored on, the forest at 40 features is an exactness check on its approximate attributions, the aggregation is mean absolute, k is 10, the SHAP background is 200 windows held fixed across seeds, and nsamples is 50. The mapping rule and the reference standard are `config/stride_ground_truth.yaml`, `config/shap_capec_map.yaml`, `config/capec_stride.yaml` and `config/maude_keywords.yaml`, all committed before either notebook trains anything. 09a trains five sequence models and the forest and writes attributions per seed as each pass completes; 09b maps, counts assignment and agreement separately, computes Kendall's tau and queries openFDA, and runs on a CPU |
| NB08b parked | Written, committed and dry-run clean, and not run. RO2 is answered by the saturation result in Section 5, the per-class budgets and the group medians of 25 against 15, on which H2 is measured under `PREREGISTRATION.md` Amendment 12. The earliness curve NB08b would produce is not load-bearing for any hypothesis. `DECISIONS.md` under 2026-08-13 records the parking. Amendment 15 stands as written and is not withdrawn |
| Graph modelling exclusion, resolved | The exclusion stood on recoverability: no topology could be built from the released columns. A published application of Graph Attention Networks and a hybrid GCN to CICIoMT2024 exists — Chethan et al. (2026), DOI 10.48084/etasr.17590 — and its PDF was read on 2026-08-14. Their Section II.C and equation (1) establish an edge where two nodes share a communication protocol, broker, topic or MAC address, or where feature similarity exceeds 0.6. The released CSVs carry no MAC address, broker or topic column, so only protocol sharing and feature similarity are implementable and what is built is a similarity graph over feature vectors rather than observed network topology. The Section 3 exclusion is restated on that basis rather than withdrawn: a graph can be built, and the edges in it come from the similarity rule chosen rather than from observed communication. `DECISIONS.md` under 2026-08-14 records the check |
| Citations awaiting PDF review, closed | All seven were read against their primary sources on 2026-08-15 and the row closes. Doménech, J., León, O., Siddiqui, M. S., and Pegueroles, J. (2025), *Internet of Things* 32:101631, DOI 10.1016/j.iot.2025.101631. Chikezie, C. I., Usman, A. U., David, M., Zubair, S., Ohize, H. O., and Ojeniyi, J. (2026), *Future Internet* 18(6):287, DOI 10.3390/fi18060287, the split governance paper. Abo-Haat, M., and Zuhair, H. (2026), *International Journal of Intelligent Engineering and Systems* 19(3):338-359, DOI 10.22266/ijies2026.0331.21, the device-disjoint paper, whose reference was not located until this reading. Ahmad, T., Truscan, D., Vain, J., and Porres, I. (2022), 2022 IEEE ICSTW 30-39, DOI 10.1109/icstw55395.2022.00020, which is the published form of arXiv 2201.11628 and is cited in place of the preprint. Djaidja, T. E. T., Brik, B., Senouci, S. M., Boualouache, A., and Ghamri-Doudane, Y. (2024), IEEE TIFS 19:7783-7793, DOI 10.1109/TIFS.2024.3441862. Panopoulos, I., Bartsioka, M. L. A., Nikolaidis, S., Venieris, S. I., Kaklamani, D. I., and Venieris, I. S. (2026), A-THENA, arXiv:2604.21623, accepted to *ACM Transactions on AI Security and Privacy*, DOI 10.1145/3811033. Goldschmidt, P., and Chudá, D. (2025), *Computers & Security* 156:104510, DOI 10.1016/j.cose.2025.104510, no longer a preprint, and the outstanding TTL sentence is located to their Section 6.3. What each verification changed, narrowed or contradicted is recorded in `DECISIONS.md` under 2026-08-15 and positioned in `NOTES_FOR_WRITING.md`. Two findings from Doménech et al. are promoted out of this row because they are dataset facts rather than pending citations: their Table A.9 gives the Duration feature's description as TTL, which is carried in the Duration entries in `DECISIONS.md` and in `config/feature_families.yaml`, and their Section 5.1.1 records the differing extraction windows, which is carried in Section 4 above |
| "Detection ceiling", resolved | The phrase sat in two places, the Section 1 thesis statement and the RO2 row of Section 3, and described neither: saturation marks where a class stops improving with more observation, not where it becomes reliably detectable, and eight of nineteen classes saturate at an F1 below 0.80. Both were restated on 2026-08-14. The thesis statement now reads as how much observation each threat class needs before further observation stops improving detection. The RO2 research question now asks how much traffic must be observed before each attack class stops improving with further observation, and whether that differs across classes, which matches the saturation point its own metric column already named. The objective, hypothesis, metric and notebook columns of that row are unchanged, as is H2, whose statement and comparator sit in `PREREGISTRATION.md` Amendment 12. The phrase appears nowhere else in this file. `NOTES_FOR_WRITING.md` carries the entry under Chapter 5, which records the wording as unresolved and is superseded on that point by this row |
| Packets per row: Section 4's extraction windows against this project's own reading | Section 4 records, from Doménech et al. (2025) Section 5.1.1 read against the primary PDF, that the dataset's authors extracted features over 100-packet windows for DDoS and DoS traffic and 10-packet windows for everything else. The pair diagnosis read the Number column back through the split's scaler and did not reproduce that division. Seventeen of the nineteen classes return a median of 9.500000, all eight DDoS and DoS classes among them; Benign returns 5.499998 and Recon-OS_Scan 8.250000, and the artefact records `separates_the_pair_classes` as false. Section 4 stands as written and is not edited. A published appendix and one column read on standardised values are different kinds of evidence, and the likelier account is that Number does not measure the extraction window rather than that the division is absent: a 100-packet extraction window and a Number median near 10 only conflict if Number counts the packets a row was built from, which nothing here establishes. Which reading governs is unresolved and has to be settled before either statement reaches a chapter, because the two cannot both describe what a row summarises. `data/processed/NB06d/pair_separability.json` under `packets_per_row` carries the per-class figures |
| Framing restated to a threat-model deliverable | On 2026-08-16 the project's stated contribution moved from an account of evaluation protocol to a per-class threat model table linking detector explanations to CAPEC patterns and STRIDE categories. The session-provenance result is not withdrawn or downgraded in evidential status; it moves from thesis to methods justification, and remains the stated reason H3 is scored on the timing-excluded model at 40 features. Section 3's reported-results table already records it in that role under notebook 03. Chapter 3 must state that timing features were excluded before explanations were computed, or "grounded in observed traffic" claims more than the design supports |
| Cost-asymmetric threshold analysis, deferred | Considered on 2026-08-16 and deferred to future work rather than run. It would test how detection thresholds should be set when the cost of a missed attack differs from the cost of a false alarm in a clinical setting. It fits none of RO1, RO2 or RO3 and would require a fourth research question, a new notebook, fresh inference against the saved models to recover predicted probabilities, and a committed cost-weight config. Recorded in Chapter 5 as a future-work recommendation. No artifact exists and none is promised |
| Recon-VulScan status, recorded | Stated here because it was misreported in conversation on 2026-08-16 and the H1 claim rests on it. Recon-VulScan reaches F1 0.5385 under the sequence model, from 0.0000 in the published run, and is one of the four of five classes that cross the 0.50 threshold. The class that is not recovered is MQTT-DDoS-Publish_Flood, 0.1858 to 0.0796. The two are not interchangeable and any chapter text pairing them as jointly undetected is wrong. Section 5's table at the five-class comparison is correct as written and is the reference |
| Title and thesis statement, resolved | Settled on 2026-08-16. The title is *Sequence-Based Intrusion Detection and Threat Modeling for Internet of Medical Things Networks*. "Proactive" is dropped: it promised prediction ahead of impact, which the lookahead exclusion rules out. "Framework" is dropped: it promised a built artifact where the deliverable is a per-class threat model table. The thesis statement in Section 1 is restated to match, and the RO/RQ/H table in Section 3 is restated in the plain register of the NeCamp exemplar. No measured quantity moves: H1's class set and 0.50 threshold, H2's saturation comparator and epsilon, and H3's pass mark of 15 of 18 are unchanged and remain fixed in `PREREGISTRATION.md` |
| Abstract | Section 1a to be added. Handled outside this pass |
| Hypothesis approval marking | Sign-off obtained from the advisory committee. Section 3 records no approval status; the approval marking and its date are added in a later pass |
| Leave-one-family-out generalisation, resolved | Dropped on 2026-08-16 rather than run. It was not load-bearing for any hypothesis, and under the restated framing nothing depends on it. The Section 3 reported-results row is deleted and the cross-dataset scope exclusion is reworded so it no longer offers a substitute generalisation test that does not exist |
