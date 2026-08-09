# AG_PRAXIS — Project Record

**A Proactive Threat Modeling Framework for Connected Medical Devices Using
Sequence-Based Detection and Explainable AI**

Doctoral praxis · GWU SEAS/EMSE
Dataset: CICIoMT2024 · Foundation model: Mohammadi et al. (2024), arXiv:2410.23306
Prior praxis in program: Bogan (2025)

**Version 1.5 · 8 August 2026**

---

> **This file is the single source of truth for the project.**
> Attach it and PREREGISTRATION.md when starting a new chat. This file states the
> current position; the pre-registration holds the class sets, thresholds and
> exclusion rules that the hypotheses depend on. Files marked superseded in
> Section 10 must not be used as reference.

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
| **1** | Determine, using a sequence-based detector, how much observation each threat class requires before it becomes reliably identifiable. | How many records of IoMT device traffic must be observed before each threat class becomes reliably identifiable? | The median number of observed records that low-rate attack classes require to reach F1 >= 0.80 will be at least twice the median for volumetric flooding classes. | Records observed to reach F1 >= 0.80, per class | 04, 06, 08 |
| **2** | Determine whether modelling traffic as sequences of records rather than single records improves detection of the attack classes the published CNN model fails to detect. | Does modelling traffic as sequences rather than single records improve threat detection in remote patient hub (RPH) networks? | Sequence-based detection improves macro-averaged F1 on the attack classes the published CNN model fails to detect. | Macro-F1, and per-class F1 change on the classes the published CNN fails to detect | 05, 06, 07, 08 |
| **3** | Develop an automated pipeline that assigns SHAP-based feature explanations to CAPEC attack patterns and STRIDE threat categories, and assess whether postmarket surveillance captures the threats so identified. | Can model explanations be mapped to STRIDE threat categories consistent with documented attack semantics? | For at least 70% of attack classes, SHAP explanations of the detection model will map to a STRIDE category consistent with that class's documented attack semantics in the CICIoMT2024 benchmark paper. | Proportion of classes with a consistent STRIDE assignment | 09 |

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
applies to the H2 class set under Amendment 6.

### Reported results — not hypothesis tests

| Result | Notebook | Role |
|---|---|---|
| Capture identifiability | 03 | Justifies running SHAP on a timing-excluded model |
| Baseline reproduction, macro vs weighted | 05 | Comparison point |
| Class-imbalance interventions, per-class costs | 07 | Per-class benefit, which classes gain most from intervention |
| Leave-one-family-out generalisation | 08 | Robustness |
| Attribution stability, Kendall's tau | 09 | Reported with the mapping |
| MAUDE cyber-attributable share | 09 | Surveillance coverage |
| Dadkhah et al. published baselines (RF 0.551, DNN 0.522, etc.) | 05 | Shared published-baseline anchor; also the comparator Mohammadi et al. cite. Context, not an H2 test. |
| RF ablation: Dadkhah Table 8 config on capture-disjoint split (macro-F1 0.8680) | 05 | Isolates split protocol from Dadkhah's published 0.551; context, not an H2 test. |

Dadkhah et al.'s own baselines are context rather than a result of this project. Verified
against the source PDF on 2026-08-07: 19-class Random Forest F1 0.551 from their Table 7, a
file-level 80/20 split by PCAP file from their Section 5, and no averaging method stated
anywhere in the paper. H2's comparator remains the published CNN. These figures position the
work; they do not test it. Section 6 carries the detail.

### Scope exclusions and their basis

- **Graph modelling** — the 45 released columns contain no source or destination
  identifiers. No topology is recoverable.
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
| Constant across dataset | Drate only — dropped |

The 45 released columns were reconciled on 2026-08-07 against Dadkhah et al.'s Table 5 and
against the CICIoT2023 schema it cites (Neto et al., *Sensors* 23(13):5941, 2023). All 39
Table 5 features are present: 38 match by name, and the thirty-ninth, Time-To-Live, is the
column named Duration, which CICIoT2023 lists with the description "Time-to-Live (ttl)". The
six columns beyond Table 5 are CICIoT2023 features checked against Neto et al.'s Table 4.
`config/feature_families.yaml` holds the full reconciliation.

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
field. With 93.57% of rows at the modal value, 6.4% of them vary, so its contribution to
these figures is likely small rather than near zero — reasoned, not measured; an NB08
timing-minus-Duration probe would settle it. The column stays in the timing family and in
the 44 by deliberate decision, for comparability with runs already executed.
`DECISIONS.md` under 2026-08-07 and `config/feature_families.yaml` under
`duration_family_placement` carry the reasoning.

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
timing-excluded model in NB09, so the threat mapping describes attack behaviour rather than
recording conditions. The identifiable session is not being used to score points on these
eight classes, where the two attack protocols agree to within 0.0003 macro-F1, but it
remains available to any model trained on these columns and to any explanation read off one.

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
not a controlled comparison between two models, and it changes nothing about H2, whose
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
the same split, that is -0.0218. Against `published_cnn_19class`, the comparator H2 names,
it is +0.0028. The random forest on single records remains the highest macro-F1 recorded
in this project at 0.8418. Accuracy falls from 0.9852 on the parent to 0.8197, and the
weighted minus macro gap falls from 0.2474 to 0.0926.

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
No H2 clause sets a limit on this quantity, since `PREREGISTRATION.md` Amendment 10 records
that Amendment 2's cost clause did not survive the Amendment 5 replacement, so these are
reported without a pass mark. The per-run detail is in `RESULTS_LEDGER.md`.

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

**Verified 2026-08-04:** his Table 3-1 labels models `SGKF`, which appears nowhere in his
abbreviations list where every other reference is `SKF`, defined as Stratified K-Fold. The
labelling is a typographical error confined to that table, and plain stratified k-fold is
what was used. Section 11 records the checks the finding rests on.

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
| `config/feature_families.yaml`, resolved | Reviewed and marked on 2026-08-04. The twelve columns ambiguous between protocol and statistical stay in protocol; the rationale, the evidence for it and the one open point are recorded in the file itself |
| `SGKF` labels in Bogan's Table 3-1, resolved | A typographical error. `SGKF` appears six times, all within that one table. `SKF` appears throughout the abbreviations list, the research questions, all of Chapter 4 and both confusion matrix captions, and is defined as Stratified K-Fold. No `SGKF` entry exists in the abbreviations list. The prose immediately below the table describes plain stratified k-fold cross-validation, five folds with no reserved validation portion, and no grouping variable is defined anywhere in the methodology. Plain `StratifiedKFold` is therefore the correct comparison |
| Benign split boundaries, resolved | Tier B classes concatenate their train and test files and cut at 70 and 85 percent of the whole, so a partition can span the file boundary. Benign trains on `Benign_train` rows 0 to 161,237, validates on `Benign_train` rows 161,237 to 192,732 plus `Benign_test` rows 0 to 3,056, and tests on the remainder of `Benign_test`. Stated as a design choice in Chapter 3 |
| Recon-Ping_Sweep sequence counts | 24 train, 2 validation, 4 test at window 50 and stride 25, from 926 records. Excluded from the low-rate median in H1 by `PREREGISTRATION.md` Amendment 4. The same exclusion rule is applied to the H2 class set in Amendment 6, which drops it from the classes the published CNN fails to detect despite its F1 of 0.0107 on that run |
| H3 reference standard, resolved | H3 tests STRIDE consistency against the attack semantics documented in the CICIoMT2024 benchmark paper. MITRE's CWE-CAPEC-ATT&CK chain is in scope as a secondary reference, attached to the mapping output as enrichment in the same way CVE identifiers are, and is not part of what H3 tests |
| Wearable and RPH framing, resolved | The testbed splits by protocol: 7 real Wi-Fi devices, none a wearable; 15 simulated MQTT devices including several wearables; the remaining real devices on Bluetooth, almost all wearables. The 72 CSVs are Wi-Fi and MQTT only and Bluetooth is pcap-only, so no real wearable contributed a row to the modelled data. RQ1 no longer names wearables. Remote patient hub framing is retained: the Wi-Fi set includes a hub, an SOS pager, an SOS button and a baby monitor. Wearables remain in the dataset description in Section 4 |
| `MedSec-25.csv` and the cross-dataset transfer artefacts | Archived under `archive/data/` and excluded from git by size |
| H2's single-record baseline, resolved | H2 names the published CNN as its comparator. The five classes it fails to detect — Recon-VulScan, Recon-OS_Scan, MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data — and the 0.50 F1 threshold that defines both set membership and improvement are fixed in `PREREGISTRATION.md`, Amendments 5 and 6. The single-record random forest at 0.8418 macro-F1 is reported alongside as a third comparison, because it beats the published CNN |
| Row order and the sequence premise | H2 assumes CSV row order preserves capture order. Tested in NB04 before sequences are built |
| Low-rate group listing in Section 3, resolved | Section 3's low-rate bullet no longer lists Recon-Ping_Sweep, matching the group fixed by `PREREGISTRATION.md` Amendment 4, and the exclusion and its basis are now stated beneath the bullets. H1 names the median again in the same edit, restoring the aggregation Amendment 3 stated and v1.0 dropped. Both changes are recorded in Amendment 8 |
| Section 5 sentence on classes below F1 0.50, resolved | Both statements re-derived from `results/NB05/*/metrics.json` and corrected. First: five classes, not three, are below F1 0.50 in both convolutional runs — Spoofing and MQTT-Malformed_Data were missing — and the forest resolves three of the five, MQTT-Malformed_Data reaching 0.6752. Second: no run on disk produces the "Reproduced baseline" figures, so that block now carries a note recording that it comes from an earlier reproduction and that every figure cited in Chapter 4 comes from the artifacts in `results/NB05/` |
| DoS-ICMP regression under the sequence model | NB06 shows DoS-ICMP falling from 0.9960 (published CNN) to 0.3178, crossing below the F1 0.50 line — a loss larger in magnitude than any single class's gain among the five H2 classes. Whether this is a seed-42 artifact or a stable property of window-based sequencing is unresolved. NB07 has now measured whether the five balancing interventions recover it: none returns it above 0.50, the five values being 0.1594, 0.2995, 0.3516, 0.3769 and 0.4590 against the parent's 0.3178, and two of the five leave it lower than the parent. That measures recovery under balancing, not cause; the interventions were not designed to diagnose the regression and this run does not diagnose it. NB08's five-seed runs will show if it holds across seeds. |
| RF comparator naming, resolved | Two random forests exist in this project and are easy to conflate. `results/NB05/forest_19class`, at 0.8418 macro-F1, is the classifier that serves as H2's third comparison and is the correct forest to cite against Dadkhah et al.'s published baseline of F1 0.551, recorded in `DECISIONS.md` under 2026-08-07. The NB03 capture-identification probe is a separate forest that tests whether recording provenance is recoverable from features; it does not classify attack classes and is not a comparator for H1 or H2. The two were conflated while the primary-source verification entry in `DECISIONS.md` was being drafted, and corrected before that entry was committed. Recorded here so they are not mixed up again |
