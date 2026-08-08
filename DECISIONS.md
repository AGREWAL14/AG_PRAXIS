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

---

## 2026-08-07 — Dadkhah et al. (2024) read against the paper itself

**Decision:** The baseline figures, split protocol and forest settings this project
attributes to Dadkhah et al. are taken from the source — "CICIoMT2024: A benchmark
dataset for multi-protocol security assessment in IoMT", *Internet of Things*
28:101351 — rather than from Mohammadi et al.'s secondhand transcription of it.

**Evidence:** Four things were read off the source. Table 7's 19-class baselines are
Logistic Regression F1 0.432, AdaBoost 0.141, DNN 0.522, Random Forest 0.551. No
averaging method is stated for those figures anywhere in Section 5 or in the
equations defining F1, so whether they are macro, micro or weighted is unresolved in
the source itself rather than unrecorded here. Section 5 confirms the shipped
train/test split is file-level 80/20 by PCAP file, not row-level and not
capture-disjoint. Table 8 gives their forest as n_estimators 100,
min_samples_leaf 1, bootstrap True. Table 5's 39 listed features were reconciled
against the 45 columns of the released data, and the result is recorded in
`config/feature_families.yaml` under `table5_reconciliation` on the same date: 38 of
the 39 match under name normalisation, Time-To-Live has no column in the data at
all, and the seven extra columns are attributed to the CICIoT2023 pipeline on
Dadkhah et al.'s stated claim alone, unverified against Neto et al.'s own feature
table.

**Consequence:** H1, H2 and H3 are unchanged, as are their comparators and their
thresholds. What changes is the grounding. RO2/RQ2's motivating claim, and the
Chapter 2 and Chapter 4 comparisons against Dadkhah et al.'s reported baselines,
now rest on the paper rather than on a reading of a reading. Three confounds have to
be stated wherever their 0.551 forest is set against ours. First, the split
protocol: theirs is file-level 80/20, ours is the two-tier capture-disjoint protocol
fixed on 2026-08-02. Second, the feature count: our comparator uses the 44 columns
that remain after Drate is dropped, while the paper lists 39 in Table 5 and ships
45, and does not say which set its own models were trained on. Third, the forest
settings, which differ by less than they appear. Table 8's forest is a stock
scikit-learn forest: n_estimators 100, min_samples_leaf 1 and bootstrap True are all
that library's defaults. `results/NB05/forest_19class` is the same stock forest with
one parameter changed, `min_samples_leaf` 20; its `fitted_params` block records
bootstrap True and every other setting at the default, and its specified 100 trees
and sqrt max_features are the defaults rather than choices. Leaf size is therefore
the whole of the difference. That run is the one reporting 0.8418 macro-F1, and it
is the forest any comparison against their 0.551 is about.

---

## 2026-08-07 — Dadkhah et al. (2024): three claims checked against the PDF

**Decision:** Three claims in the entry above were read off the source PDF rather than
carried on report: Table 7's four 19-class figures, the Section 5 split description,
and Table 8's forest parameters. All three hold as written. This is appended rather
than folded into that entry, because the log is append-only.

**Evidence:** Table 7's 19-class block gives F1-Score 0.432 for Logistic Regression,
0.141 for AdaBoost, 0.522 for the Deep Neural Network and 0.551 for Random Forest,
matching the four figures recorded. Section 5 describes the division as "defining a
group of PCAP files comprising 80% ('train') and 20% ('test') of all PCAP files
available", which is file-level and not row-level. Table 8 lists the forest as
n_estimators=100, criterion='gini', min_samples_split=2, min_samples_leaf=1,
min_weight_fraction_leaf=0.0, max_features='sqrt', min_impurity_decrease=0.0,
bootstrap=True, oob_score=False, warm_start=False, ccp_alpha=0.0.

On the averaging question the check is firmer than the earlier entry could be. The
words "macro", "micro" and "weighted" do not appear anywhere in the paper's 22 pages.
F1 is defined once, by equation (4) in Section 5, as twice precision times recall over
precision plus recall, with precision and recall given by equations (3) and (2) in
their two-class form, and nothing anywhere states how those are aggregated across 19
classes. One placement in the earlier entry is wrong: Table 7 and Table 8 sit in
Section 7, "Machine Learning (ML) evaluation", not Section 5, which is "Methodology"
and carries the split description and the four equations. The substance of that entry
is unaffected.

**Consequence:** All eleven parameters Table 8 lists for the forest are scikit-learn
defaults, so the earlier reading of their model as a stock forest is confirmed from the
source, and `max_features` sqrt now matches ours as well as the tree count, leaving
`min_samples_leaf` as the only difference. Two errors in the source are recorded here
because they bear on how much its own metric definitions can be asked to carry.
Equation (4) is the harmonic mean of precision and recall, and the text calls it the
geometric average. Section 5 announces "five widely used ML techniques" and then names
four, which is the number evaluated throughout. Separately, Table 5's caption
attributes the feature list to reference [28], which is Neto et al.'s CICIoT2023 paper,
so the CICIoT2023 lineage recorded in `config/feature_families.yaml` is an explicit
citation rather than an inference from the methodology text. That does not close the
open item there: the seven extra columns are precisely the ones absent from Table 5,
and checking them still needs Neto et al.'s own feature table. H1, H2 and H3 are
unchanged.

---

## 2026-08-07 — Superseded wording in 7c4b790 on the CICIoT2023 lineage

**Correction:** The entry committed at 7c4b790 describes the seven extra columns as
"attributed to the CICIoT2023 pipeline on Dadkhah et al.'s stated claim alone". That
phrasing is superseded. Section 5, the methodology, never mentions CICIoT2023; it
describes extraction as TCPDUMP and DPKT with window averaging. The only link in the
paper is the caption of Table 5, "Features extracted from PCAP files [28]", where [28]
is Neto et al.'s CICIoT2023 paper, confirmed against the source PDF. The correct
account is in `config/feature_families.yaml` under `table5_reconciliation`, in
`provenance_of_extras`, updated the same day. This entry exists to mark the wording in
7c4b790 as outdated on that one point. The substance is unchanged and is not reopened
here: the seven columns remain cited but unverified.

---

## 2026-08-07 — Time-To-Live is not missing from the data; it is the column named Duration

**Correction:** Neto et al. (2023), "CICIoT2023: A Real-Time Dataset and Benchmark for
Large-Scale Attacks in IoT Environment", Sensors 23(13):5941, was read directly. It
reverses the gap recorded earlier today. Time-To-Live is not absent from the released
CICIoMT2024 data. It is the column named Duration, so all 39 of Dadkhah et al.'s
Table 5 features are present, 38 by name and one by equivalence. The six remaining
extras are verified against Neto et al.'s own feature table, which closes the open
item that stood on a citation alone.

**Evidence:** Neto et al. Table 4 gives feature 5 as the name "Duration" with the
description "Time-to-Live (ttl)", so the source equates the two: Dadkhah et al.'s
Table 5 uses the descriptive name, the CSV keeps CICIoT2023's column name. Two further
lines agree. The absences are complementary, Table 5 listing Time-To-Live and no
Duration while the released CSVs carry Duration and no Time-To-Live. And the values are
those of a header field, not a time: our Duration runs 0 to 250 over 590 distinct
values in the reference file, under the 255 ceiling of an eight-bit TTL, while Neto et
al.'s Table 5 gives their Duration a median of 64, the common default TTL, and a
maximum of exactly 255. Their flow duration is a separate column reaching 394,357, so
Duration cannot be that. The six extras all appear in Table 4: Srate at 7, Drate at 8,
Magnitude at 43, Radius at 44, Covariance at 45 and Weight at 47. The released schema
is fully accounted for — our 45 columns are Neto et al.'s 47 less ts, flow duration and
urg count, plus IGMP, which CICIoMT2024 adds.

**Consequence:** `config/feature_families.yaml` was updated: `matched` now reads 39 of
39, `missing_from_data` records that nothing is missing and why the earlier reading was
wrong, `extra_in_data` drops to six, and `provenance_of_extras` is verified rather than
cited. The spelling note is corrected in the opposite direction to what was expected.
Neto et al. spell Magnitude correctly in Table 4 but write "Magnitue" in Table 5, which
reports statistics under the released column names and uses CSV spellings throughout,
so CICIoMT2024 inherited the misspelling from the CICIoT2023 release rather than
introducing it. One thing is opened rather than closed, and is recorded in the same
file under `duration_family_placement`: the families block assigns Duration to timing
by a name rule, which is wrong if the column is Time-To-Live. NB09 excludes the timing
family and NB03 measured that family at 0.9301 for capture identification, both with
Duration in it. No family assignment has been changed, because moving the column would
alter what NB09 excludes and break comparability with the NB03 figure. H1, H2 and H3
are unchanged, and the 44-feature working set is unchanged.

---

## 2026-08-07 — Duration confirmed as Time-To-Live by full scan

**Decision:** Duration holds the TTL header field. This is settled on the whole
dataset rather than on the reference file, and it confirms the reading taken from
Neto et al. earlier today rather than revising it. Two decisions that follow from it,
where Duration belongs among the families and whether it belongs in the modelling set
at all, are left open. This entry records evidence, not a resolution.

**Evidence:** Duration was read from all 72 CSVs, 8,775,013 rows, matching the
inventory total exactly, with no nulls. The global minimum is 0 and the global maximum
is 255 exactly. No row anywhere exceeds 255, and 702 rows sit on it across 11 files,
which is the ceiling of an eight-bit field rather than a value a duration would happen
to stop at. The distribution is the stronger evidence: 8,211,161 values, 99.57% of the
column, are exactly 64, the Linux default TTL, and the tail falls on the other standard
defaults — 60 for older macOS, 128 for Windows, 255 for network equipment, 32 for
legacy stacks. The 527,983 non-integer values, 6.02%, are what window averaging
predicts, since CICIoMT2024 averages packets in windows of 10 and 100 and a window
spanning hosts of different TTLs yields a fractional mean. The lowest per-file maximum
is 67.44, a fraction just above 64.

**Consequence:** The two consequences recorded under `duration_family_placement` in
`config/feature_families.yaml` now rest on the full dataset. NB09 excludes the timing
family, which contains this header field, and NB03's 0.9301 capture-identification
figure for that family was measured with Duration in it. The scan adds a third point
that bears on both. At 99.57% constant the column carries almost no information
wherever it is filed, so the question is not only which family it belongs to but
whether it earns a place in the modelling set. Nothing has been changed. The family
assignment stands as it is, Duration remains among the 44 modelling features, and both
decisions are deliberately unmade pending a call, because either one alters what NB09
excludes or what the models are trained on. H1, H2 and H3 are unchanged.

---

## 2026-08-07 — Duration stays in the timing family and in the modelling set

**Decision:** Duration remains where it is, in the timing family and among the 44
modelling features. Both questions left open by the full scan above are answered by
changing nothing.

**Reasoning:** NB03, NB05 and NB06 were all executed with Duration where it is.
Moving a family boundary or altering the feature set now would break those banked
results against anything run afterwards, which is the comparability the
one-change-per-run rule protects. The column is confirmed as the Time-To-Live header
field by the full scan recorded above, so this is a deliberate choice made against
the evidence rather than an assignment left standing by oversight: a header field is
knowingly kept in the timing family, and a column that is 99.57% constant is knowingly
kept in the modelling set.

**Consequence:** One inaccuracy travels with the decision and must be stated wherever
the timing family is used. That family contains a header field, and NB03's 0.9301
capture-identification figure for it was measured with Duration included. At 99.57%
constant the column's contribution to that figure should be near zero, but that is
reasoned and not measured. A timing-family-minus-Duration robustness probe in NB08
would settle it, and is optional rather than required. The item is marked resolved in
`config/feature_families.yaml` under `duration_family_placement`, which carries the
same terms. H1, H2 and H3 are unchanged.

---

## 2026-08-07 — Duration's constancy figure corrected from 99.57% to 93.57%

**Correction:** The earlier entries of this date record Duration as 99.57% constant. The
figure is 93.57%. The error was a conditional share reported as an unconditional one:
99.57% was computed over integer-valued rows only, 8,211,161 of 8,247,030, and labelled
as a share of the column. Against all 8,775,013 rows the modal value 64 covers
8,211,161, which is 93.57%. So 563,974 rows carry a value other than 64, not the
36,000 or so the earlier number implies.

**Evidence:** A near-constancy scan of all 44 modelling features over the full 8,775,013
rows, run after the entries above. Two independent checks say the scan is sound: Drate
returns exactly 100.0000% with no non-modal row, matching NB01's finding that it is the
only constant column, and the fifteen features whose zero-share exceeds 90% reproduce
NB02's existing count of 15 of 44 in Section 5 of `PROJECT_RECORD.md`.

**What this does not change:** The identification of Duration as Time-To-Live stands
untouched, resting on the global maximum of exactly 255, the modal value of 64 and a
tail falling on the standard default TTLs, none of which depend on the share. Option C
stands: it rests on comparability with NB03, NB05 and NB06, not on how constant the
column is. The 0.9301 figure itself, the 44-feature count, H1, H2 and H3 are all
unaffected.

**What this does change:** The reasoning that Duration's contribution to NB03's 0.9301
is near zero is less emphatic than recorded. Six point four percent of rows vary, not
zero point four. The contribution is still likely small, but it is reasoned rather than
measured and it is not as airtight as the earlier wording implies. A
timing-family-minus-Duration probe in NB08 remains what would settle it. The same scan
strengthens option C from another direction: Duration ranks eleventh of the 44 in
constancy, with eighteen features more single-valued than it and eight of those above
99.9% — IGMP varies in 299 rows of 8.77 million, DHCP in 535, cwr_flag_number in 602,
ece_flag_number in 610. Any rule that drops a column for near-constancy reaches those
eight well before it reaches Duration. `config/feature_families.yaml` and
`PROJECT_RECORD.md` were corrected in place in the same commit as this entry.
