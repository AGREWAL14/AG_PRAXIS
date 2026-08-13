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

---

## 2026-08-08 — Dadkhah et al.'s baselines reported as a shared benchmark anchor

**Decision:** The published baselines from Dadkhah et al. (2024) Table 7, 19-class F1 of
0.432 for Logistic Regression, 0.141 for AdaBoost, 0.522 for the DNN and 0.551 for Random
Forest, are reported as a benchmark anchor in NB05, NB08 and NB10. They are a reported
reference point, not a hypothesis comparator.

**Reasoning:** Mohammadi et al. (2024), the foundation model this work reproduces, already
cites these same Dadkhah figures as its own point of comparison. Reporting them here puts
this work and the CNN paper on one shared anchor, so a reader can place both against the
dataset's originating baselines without a second translation step.

**Consequence:** This adds a second reported comparator and alters no hypothesis. H2's
comparator remains the published CNN under Amendment 5, with its threshold and class set
untouched. Any reading of Dadkhah's 0.551 against `forest_19class` at 0.8418 macro carries
three confounds that must travel with it: their averaging method is not stated anywhere in
the paper, their split is file-level by PCAP where ours is capture-disjoint, and their
feature count is unsettled at 39 listed against 45 shipped against the 44 used here. The
comparison is a benchmark reference under a more rigorous protocol, not a controlled
head-to-head result. The 2026-08-07 entries above record the source checks these figures
rest on. `PROJECT_RECORD.md` Sections 3 and 5 were updated in the same commit as this
entry. H1, H2 and H3 are unchanged.

---

## 2026-08-08 — Correction: NB07 follow-up note overstated window resampling's uniqueness

**What was written:** The first draft of the NB07 follow-up note in `RESULTS_LEDGER.md`
stated that window resampling was "the only intervention that raises macro-F1 and the
volumetric mean together".

**What is true:** Three of the five do. Window resampling raises macro-F1 by +0.0561 and
the volumetric mean by +0.0174; logit adjustment raises them by +0.0100 and +0.0106; and
threshold tuning by +0.0182 and +0.0030. What is true of window resampling alone is that
its gain on each of the two is the largest of any intervention. The claim as drafted named
a property three runs share and attributed it to one.

**How it was caught:** Re-reading every claim in the note against the five
`results/NB07/*/metrics.json` files before the file was committed. The figure that
contradicts it — the per-run volumetric mean, +0.0106 for logit adjustment and +0.0030 for
threshold tuning — was already stated correctly two paragraphs below in the same note,
under the cost-to-volumetric-classes paragraph. The note contradicted itself and read
fluently either way.

**Scope:** The error was confined to one sentence of drafted prose. It reached no commit,
so no file, chapter or downstream claim carried it. The tables in the same entry were
written by the notebook from `metrics.json` and gate-checked at 9 of 9, and every figure in
them verified correct on the same pass. Corrected before the entry was committed. In the
same pass the DoS-ICMP figures in that paragraph were widened from two decimals to four:
0.1594, 0.2995, 0.3516, 0.3769, 0.4590.

**Why it is recorded:** The failure mode is the one the 2026-08-07 correction to the
Duration modal share already demonstrated — a summary statement written from memory of the
numbers rather than from the numbers, plausible enough to survive a read-through. Catching
it required going back to the artifacts, which is the same discipline that produced the
99.57% to 93.57% correction. Recording it keeps the count of such errors honest rather than
resetting it each time one is caught early.

**What this does not change:** No hypothesis, threshold, class set or comparator. All
NB07 tables, all per-class figures and all five macro-F1 values stand as written and as
verified against the artifacts on disk.

---

## 2026-08-08 — Dadkhah's own forest configuration run under the capture-disjoint split

**Decision:** The ablation `forest_19class_dadkhah_leaf1` is recorded as a reported result
in `PROJECT_RECORD.md` Sections 3 and 5 and in `RESULTS_LEDGER.md`. It takes the random
forest settings from Dadkhah et al. (2024) Table 8, of which `min_samples_leaf` 1 is the
only one that differs from `forest_19class`, and scores them on the capture-disjoint
two-tier split. Macro-F1 0.8680 against the parent's 0.8418. Same 44 features, seed 42,
same 1,229,711 test rows.

**Reasoning:** Dadkhah et al. publish 0.551 for their nineteen-class random forest and this
project's forest reads 0.8418. Two things differ between those numbers at once, the model
configuration and the evaluation protocol, and without separating them the distance is
uninterpretable. Running their configuration under this project's split holds the model
fixed and leaves the protocol as the thing that changed.

**Consequence:** The leaf constraint accounts for 0.0262 of the 0.3170 between 0.551 and
0.8680, so it explains almost none of the distance. What the run supports is that Dadkhah's
own configuration, evaluated under a capture-disjoint split, scores far above their
published figure, which locates the difference in evaluation protocol rather than model
capacity. Protocol here means the split and the averaging method together, since the paper
states no averaging method and 0.551 may not be a macro figure. The run does not control
the feature set, the paper listing 39 and shipping 45 against the 44 used here, and does
not control the averaging method either. Those two confounds are unchanged. This is a
reported result, not a hypothesis test, and it is not a controlled win over published work.
H1, H2 and H3 are unchanged, and H2's comparator remains the published CNN under Amendment
5, with its threshold and class set untouched.

---

## 2026-08-08 — Open item: prediction arrays saved as label strings, 113 MB each

**What happened:** `forest_19class_dadkhah_leaf1` wrote `y_true.npy` and `y_pred.npy` at
113,133,540 bytes each, against 1,229,839 bytes for `forest_19class` on the identical
1,229,711-row nineteen-class test set. Both exceed GitHub's 100 MB file limit, so the run
is committed as `config.json` and `metrics.json` only, with the two arrays left on Drive at
`/content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/forest_19class_dadkhah_leaf1`.

**Cause, verified from the npy headers:** the ablation's arrays carry dtype `<U23` and the
parent's carry `|i1`. The ablation saved the class-name strings, padded to the width of the
longest label, `MQTT-DDoS-Connect_Flood` at 23 characters, which is 92 bytes per element
against one. It is not a float or object dtype; it is fixed-width unicode. The 92-fold size
ratio matches the byte counts exactly.

**Why it is logged rather than fixed now:** the metrics were computed inside the run and
are unaffected, so nothing about the reported figures depends on this. The arrays are
needed for later per-class and paired analysis, and the copies on Drive serve that.

**What to watch:** NB08 runs five seeds. On the current save path that is ten arrays at
113 MB each, all of them over the limit, hitting the same wall five times instead of once.
Before NB08 runs, the save path must map the labels through the class list to integer class
codes and save those, which is what `forest_19class` did. It is not a dtype cast. Calling
`astype` on an array of class-name strings does not produce class codes; it either raises
or produces something meaningless, because the strings are names and not numerals. The
encoding step is the fix and the narrow dtype follows from it: nineteen classes fit `int8`,
`int16` if a later notebook grows the class set. The class list in `metrics.json` under
`labels` is the ordering to encode against, so the existing Drive copies can be encoded on
read without re-running anything.

**What this does not change:** no metric, no hypothesis, no comparator. The figures in
`results/NB05/forest_19class_dadkhah_leaf1/metrics.json` stand as written.

---

## 2026-08-09 — Conformal prediction feasibility-tested and dropped

**Decision:** Conformal prediction is dropped. It was evaluated as a possible supporting
analysis by a feasibility probe, NB06c, which ran class-conditional split-conformal on the
NB06 sequence model's saved probabilities. No further CP work is planned.

**Reasoning:** Basic set sizes, under the nonconformity score 1 - p_true, did not track
per-class difficulty. The rank correlation between mean set size and per-class F1 was
-0.46. They also did not corroborate the pre-registered MQTT-DDoS-Publish_Flood
feature-separability finding: that class ranked 15th of 19 by set size, placing it among
the least ambiguous rather than the most. The ordering chosen before the probe ran, easy
below hard, did not hold.

**Consequence:** CP was an optional supporting layer and not a core contribution. On this
evidence it does not support the findings and mildly contradicts them on the separability
class, so it is dropped rather than built out. A more sophisticated CP variant, adaptive
prediction sets for instance, was not pursued, because the effort is better spent on the
two unbuilt core pillars, observation budgets and threat mapping. NB06b's saved
probabilities remain on Drive as intermediate artifacts.

**What this does not change:** The four core contributions stand without it.

## 2026-08-09 — Amendment 11's median position, read for an even-sized group

Amendment 11 states that a group median is reported as a number only when the value
at the median position is uncensored. The low-rate group has five classes, so the
median position is a single value and the rule reads directly. The volumetric group
has eight, so the median falls between the fourth and fifth ordered values and there
is no single value at that position.

Read as: both middle values must be uncensored, and the median is their mean. If
either is censored the group median is reported as not reached within 50 records,
on the same footing as the odd-sized case.

This interprets the rule rather than changing it. No threshold, class set or metric
moves. The reading follows the ordinary definition of a median for an even-sized
group, and the censoring condition is the same one Amendment 11 states — that the
value the median is read from must be known.

Recorded before NB08 was run. In practice the volumetric classes are expected to
reach F1 >= 0.80 at small budgets, so the even case is likely to be moot; it is
recorded because that expectation is not a result.

Implemented in `notebooks/AG_PRAXIS_NB08_evaluation_and_significance.ipynb`.

---

## 2026-08-10 — Goldschmidt & Chudá citation not yet verified

**Decision:** The reference cited in `PREREGISTRATION.md` Amendment 13 — Goldschmidt, J.
and Chudá, D., *Network Intrusion Datasets: A Survey, Limitations, and Recommendations*,
arXiv:2502.06688 — is not yet verified against the primary PDF. Verification is required
before the claim enters Chapter 2.

---

## 2026-08-10 — Conformal prediction reading, clarified

The 2026-08-09 entry records the rank correlation between mean set size and per-class
F1 as -0.46 and states that set size did not track per-class difficulty. NB06c's own
reading bands place -0.46 in the range it labels as tracking difficulty weakly, not as
not tracking it.

The decision to drop conformal prediction is unchanged. It rests additionally on two
unambiguous results recorded in the same entry: the pre-registered ordering did not
hold, and MQTT-DDoS-Publish_Flood ranked 15th of 19 by set size.

This clarifies the wording and changes no decision.

---

## 2026-08-10 — Conformal prediction and the capture-disjoint split

NB06c records that its calibration and evaluation windows come from different capture
sessions, so the exchangeability condition that split-conformal coverage rests on does
not hold under the two-tier protocol.

This is recorded as a property of the protocol, not as a reason for the NB06c result.
It is retained for Chapter 5.

NB06c also records that four of nineteen classes calibrate on fewer than 100 windows,
and that Recon-Ping_Sweep, at two calibration windows, has no finite threshold at
either target coverage NB06c ran and is admitted to every prediction set by
construction. Both properties travel with the exchangeability note wherever the
coverage caveat is used.

---

## 2026-08-10 — duration_family_placement, reasoned on 2026-08-07 and now measured

**Decision:** Unchanged. Duration stays in the timing family and stays among the 44
modelling features.

**What was reasoned and is now measured:** The 2026-08-07 entry recorded the column's
contribution to NB03's capture-identification figures as reasoned rather than measured.
NB03b measured it, under the NB03 protocol with Duration removed and nothing else changed.
Duration alone identifies the recording at 0.0299 against a chance rate of 0.0200. With the
attack class held fixed, removing it raises the mean accuracy to 0.8504 from 0.8280, so
identification does not fall when the column is removed. On the fifty-way task removing it
takes the timing family from 0.9301 to 0.8935 and all 44 features to 0.7495 from 0.8010.

Single runs at seed 42, no seed replicates. Figures in
`data/processed/NB03b/duration_ablation.json` and `results/NB03b/`, from
`notebooks/AG_PRAXIS_NB03b_timing_ablation.ipynb`, run at 8beebb7.

**What this does not change:** No metric, no hypothesis, no comparator and no feature set.
The 44 features stand as executed.

---

## 2026-08-10 — Goldschmidt & Chudá citation, verification status narrowed

**Decision:** The earlier entry under this date, "Goldschmidt & Chudá citation not yet
verified", is narrowed. The reference is verified; one sentence in it is not.

**Verified against the primary PDF:** Patrik Goldschmidt (Brno University of Technology and
the Kempelen Institute of Intelligent Technologies) and Daniela Chudá (the Kempelen
Institute of Intelligent Technologies and the Slovak University of Technology).
arXiv:2502.06688v3 [cs.CR], 22 May 2025. Submitted to *Computers & Security* in April 2025,
so cited as a preprint unless later publication is confirmed. A systematic review of 89
public NIDS datasets across 13 properties, covering datasets published to 2023 inclusive.

**Outstanding:** The TTL sentence. It sits in Section 6 and has not been located to a
section or page.

**What this does not change:** The claim in `PREREGISTRATION.md` Amendment 13 is unchanged,
and Amendment 13's "Not yet verified against the primary PDF" stands as written. No
amendment is made: a citation's verification status is not a design change, and Amendment
13's claim, warrant and metric are unchanged. The narrowing is carried by this entry and by
`NOTES_FOR_WRITING.md`.

---

## 2026-08-10 — NB07b's group-DRO objective: exponentiated gradient, eta fixed at 1e-4

**Decision:** The worst-group objective is exponentiated-gradient group DRO with one
hyperparameter, `eta`, fixed at 1e-4 before the run. Weights start uniform over the 45
training groups. No group-size floor, no weight cap and no warmup. Implemented in
`src/interventions.py` as `GroupWeights` and trained by `src/sequence.py fit_group_dro`.

**The update:** `q_g <- q_g * exp(eta * L_g)` over the groups present in a batch,
followed by renormalising the whole vector. A group absent from a batch keeps its
unnormalised weight, so nothing about it is inferred from a batch it did not appear in.
The renormalisation then rescales every group by the same constant, which leaves absent
groups unchanged relative to each other and moves them relative to the groups that were
updated. No renormalisation avoids that.

**Weights persist across batches, and that is a smoother.** Carrying `q` from one batch
to the next is not the same as taking the worst group in each batch independently, and
it is not accurate to describe the run as unstabilised. The persistence is the
stabiliser, and it is the only one.

**Why eta is 1e-4.** Derived from the arithmetic of this training set rather than taken
from a published default. 249,061 training windows at batch 32 over 10 epochs is about
77,800 batches. Group presence is very unequal: the largest group is 3.33% of the
windows and appears in roughly 65% of batches, about 50,000 updates, while
Recon-Ping_Sweep's 24 windows are 0.0096% and appear in about 0.3% of batches, about 240
updates. A group with a persistent loss excess of Delta gains eta * Delta * n of
log-weight over the n batches it appears in. Taking Delta = 0.5 nats as a working
assumption about the spread of group losses, and not as a measurement, a well-represented
group accumulates 25 nats at eta 1e-3, which is complete collapse inside the first epoch;
2.5 nats at 1e-4, which moves it from 1/45 = 0.022 to about 0.22; and 0.25 nats at 1e-5,
which barely leaves uniform. 1e-4 is the value at which the weights can traverse the
range over the run.

**Not tuned.** No validation search was run. Tuning eta would make NB07b a
hyperparameter study rather than one intervention, and the one-change-per-run rule fixes
it as one run. The weight trajectory is what the reader reads in place of a search: the
weights are written to `metrics.json` at the end of every epoch, with the heaviest
groups, the minimum and maximum weight, the effective number of groups and the number of
batches each group appeared in.

**A group-size floor was considered and rejected.** The largest training group holds
8,290 windows and the smallest 24, a ratio of 345 to 1, and at batch 32 across 45 groups
most groups are absent from any given batch. A floor would reduce the chance that the
objective collapses onto the smallest groups. It was rejected because collapse is the
failure mode the trajectory exists to expose, and a floor would prevent the artifact from
recording it. If the weights collapse, that is a result about this objective on this
corpus and is reported as one.

**The weights start uniform, which is already an objective change.** The parent
minimises the mean loss over the windows. Uniform weights minimise the unweighted mean
of the group means, so the run departs from the parent by group balancing from the first
update, before any worst-group weighting. `PREREGISTRATION.md` Amendment 17 records what
that means on the Amendment 6 class set.

**The loop is checked before the result is read.** `GroupWeights` also takes
`start="batch_share"`, which takes its weights from the batch in front of it and makes
the objective exactly the mean loss over the batch. NB07b runs the loop that way with eta
at 0 before it runs the intervention. If it does not reproduce the parent, the loop
differs from `model.fit` in some way not yet found and every figure in the notebook
carries that difference.

**The interval the check uses, fixed here before the run.** The run passes if its
macro-F1 falls in [0.690480, 0.737104]. The centre is 0.713792, the NB06 parent's own
macro-F1 read from `data/processed/NB06/metrics.json`, because what the check asks is
whether the loop reproduces the parent. The half-width is 0.023312, the cross-seed
standard deviation of this configuration measured in NB08 over seeds 42 to 46, whose
macro-F1 values are 0.713792, 0.755196, 0.765181, 0.737731 and 0.714422. That spread is
the right width because the loop shuffles with its own seeded generator and is therefore
a different draw from `model.fit` even at seed 42, so another run of the same
configuration is the reference class.

An interval of one standard deviation centred on the cross-seed mean of 0.737264 was
considered and rejected: it is [0.713952, 0.760576], and the parent's 0.713792 falls
below it by 0.00016, so a loop that reproduced the parent exactly would fail the check.
The parent is the smallest of the five seeds, so no interval of one standard deviation
centred on their mean can contain it.

**The check is weak by construction.** An interval a full cross-seed standard deviation
wide will not catch a subtle error in the loop. It catches an error large enough to move
the result outside the spread of runs of the same configuration, and nothing finer. It is
recorded as a check on the plumbing, not as evidence that the loop is correct.

**What this does not change:** No class set, no threshold, no comparator and no feature
set. The per-sample loss is still categorical cross-entropy, and the run's config records
`loss` unchanged from the parent with `training_objective` as the single changed key.

---

## 2026-08-11 — NB07b's training loop compiled; the arithmetic is unchanged

**Decision:** `fit_group_dro` compiles its per-batch step and does its per-group
bookkeeping with counts rather than a Python loop. Nothing else changes.

**What was wrong:** The loop ran eagerly. Every operation in the forward pass, the tape,
the gradient and the optimizer update was dispatched from Python one at a time, and every
batch ended with a blocking read of the per-window losses back from the device. On a
confirmed A100-SXM4-40GB with TensorFlow 2.20.0 built with CUDA, and with the device
visible to `tf.config.list_physical_devices`, epoch 1 did not finish in fifteen minutes
and GPU memory sat at 0.7 of 40 GB for the whole period. NB06 trained the same model on
the same windows for ten epochs in 41 minutes through `model.fit`, which compiles its
train step. The device was idle because the work was in Python, not because of the
hardware or the data.

**The fix:** the batch step is wrapped in `tf.function` with the tape inside it, so it is
traced once and reused; the optimizer's slot variables are built before the first trace,
since creating variables inside a traced call raises; `reduce_retracing` is on because the
last batch of an epoch is short; and the per-group epoch totals are accumulated with
`np.bincount` instead of a per-window Python loop that ran to about two and a half million
dictionary operations an epoch. The bincount accumulation was checked against the loop it
replaces and agrees to 2.8e-16.

**What is unchanged:** the objective, `eta` at 1e-4, the uniform start, the update rule,
the handling of groups absent from a batch, the group variable, the class sets and the
thresholds. This is how the arithmetic is scheduled, not what it is. No amendment is made,
because nothing `PREREGISTRATION.md` Amendments 14, 16 or 17 fix is touched.

**One read back per batch stays.** The weights a batch produces are what the next batch is
weighted by, so the dependency is serial and a device-to-host read cannot be removed by
compilation. Inside a compiled step it is 128 bytes after work the device was going to do
anyway.

**`q` stays in float64 numpy on the host.** Moving it to a device variable would remove
that last read, and it was rejected: the exponentiated-gradient arithmetic would move from
float64 on the host to device floats, which changes the arithmetic Amendment 14 fixes.
That is not worth the last few percent of a training run.

**The batch_share check now reads twice.** It was registered under the 2026-08-10 entry as
a check that the loop reproduces the parent, against the interval [0.690480, 0.737104]. It
now also reads as a check that compiling the loop did not change what the loop computes,
because the loop it is run against is the compiled one and not the eager one it was
specified for. Same measurement, same interval, second reading. It is recorded here so
that a reader who finds the check described against an eager loop and run against a
compiled one knows why.

---

## 2026-08-11 — NB08b's prefix lengths: one length per batch, uniform from 1 to 50

**Decision:** The model is trained on prefixes whose length is drawn uniformly from 1 to 50,
one length per batch. No length is weighted. Implemented in `src/sequence.py` as
`PrefixBatches` and `fit_mixed_length`, and recorded in the run's metrics as the lengths
actually drawn.

**Why every length.** The halting rule fixed in `PREREGISTRATION.md` Amendment 15 steps
through a window one record at a time and can stop at any record from 1 to 50. A model asked
to answer after any number of records has to have been trained after any number of records,
so the training distribution covers the same range the rule can select from.

**Per batch, not per window.** A batch is one array with one shape, so mixing lengths within
a batch requires padding the shorter windows out to the longest. Under StandardScaler a
padded zero is the training mean, so an unobserved record would read as an average record
rather than as an absent one. Per-window sampling is rejected on that ground.

**Uniform over 1 to 50, not over NB08's four budgets.** Drawing from {5, 10, 25, 50} was
considered and rejected: it would leave 46 of the 50 lengths the halting rule can select
untrained, so the rule could stop at a length the model had never been trained at.

**What uniform costs, stated rather than corrected.** A five-record prefix gets the same
share of the training as a fifty-record one although it carries a fraction of the
information. That is a property of the design. No length weighting is applied, because
choosing a weighting would be a second design choice inside a run whose one change is the
training input, and the one-change-per-run rule fixes NB08b as one run.

**What this does not change:** No class set, no threshold, no comparator and no feature set.
The architecture, the split, the seed, the batch size and the ten epochs are the parent's.
The tau grid, the halting rule and the earliness definition are Amendment 15's and nothing
here touches them.

---

## 2026-08-11 — NB07b withdrawn

**Decision:** NB07b is withdrawn. It will not be executed and nothing from it is
reported.

**The reason, which is a property of the design and not of any result.**
`PREREGISTRATION.md` Amendment 16 records that 11 of the 45 training groups are
single-capture classes, where the group and the class are the same set of windows, and
that all five classes fixed in Amendment 6 are among them. Amendment 17 records that the
weights start uniform, so that coincidence is operative from the first update rather
than only in the limit. Taken together, on the class set the first dependent variable is
evaluated over, the intervention is class weighting. NB07 already tested class weighting
through five interventions.

What survives is the capture-invariance question on the 8 classes recorded more than
once. On that scope the notebook was judged not to carry a contribution proportionate to
its cost, and it is withdrawn rather than run and reported.

**What is not recorded.** No figure from the aborted run is recorded anywhere. The run
was stopped during the DRO training, after the batch_share check had completed. Nothing
is written to `RESULTS_LEDGER.md`, because no run completed and the ledger records runs.

**The amendments stand as written.** Amendments 14, 16 and 17 are not withdrawn. They
are the record of an extension that was designed, specified and costed, and Amendment 16
in particular is where the counts that led to this decision were established. A
pre-registration that only held the things that were carried out would not be a
pre-registration.

---

## 2026-08-11 — the batch_share check interval was defective

**Decision:** The interval recorded under the 2026-08-10 entry, [0.690480, 0.737104], is
recorded as defective. No replacement is specified.

**The arithmetic.** The interval was centred on 0.713792, the NB06 parent's own macro-F1,
with a half-width of 0.023312 taken from the five NB08 cross-seed values at k = 50. Those
five values are 0.713792, 0.755196, 0.765181, 0.737731 and 0.714422. The centre is the
smallest of them. Running the five through the interval that their own spread set: two
pass and three fail. 0.755196 is above the upper bound by 0.018092, 0.765181 by 0.028077
and 0.737731 by 0.000627.

The criterion therefore rejects three runs of the configuration it was built to accept.

**How it was missed.** The interval was set jointly, before the run, from the right
quantities: the parent as the thing the loop had to reproduce, and the measured
cross-seed spread as the width. What was not done was to run the five values that set the
width back through the interval they produced. Centring on the minimum of a sample and
allowing one standard deviation either side covers the downside and truncates the upside
at less than half the observed span, which the five values would have shown immediately.

**Why no replacement is given.** The defect was found only after the check returned
0.744304 and was rejected on it. Any interval chosen now would be chosen with that figure
in view, which is the thing a criterion fixed before a run exists to prevent. A criterion
for this check, if one is wanted again, is fixed before whatever run it is to judge.

---

## 2026-08-12 — NB09 split into 09a and 09b

**Decision:** NB09 is two notebooks. 09a trains the timing-excluded models and computes
the attributions. 09b applies the mapping, counts agreement, computes Kendall's tau and
queries openFDA.

**Reason:** the combined notebook was a four-to-five hour session dominated by five
sequence training runs, and an error in the mapping would have cost the whole run. 09b
reads 09a's artefacts, runs on a CPU and is re-runnable without retraining anything, so a
mapping mistake costs minutes.

**The forest arm stays in 09a.** Moving it to 09b was considered and rejected: 09b would
then need the record arrays, 1.1 GB for training and 228 MB for test, and would stop being
analysis-only. It is kept in its own cell in 09a, marked as needing no GPU, and the resume
checks let a CPU session run that arm alone by skipping the sequence fits already written.

---

## 2026-08-12 — shap nsamples, measured; the first reading was wrong

**What was measured:** wall time per explained window and top-10 stability at nsamples 10,
25, 50, 100 and 200, on the dry-run fixture on CPU, one explainer call over the same fixed
windows at every value.

**The first reading, at 20 explained windows, was wrong.** The timings came out
non-monotonic — 10 at 1.17s per window, 25 at 1.32, 50 at 1.53, 100 at 1.11, 200 at 3.19 —
and were read as showing that nsamples was not the cost driver. Twenty windows is too few
to see through the fixed per-call overhead.

**The second reading, at 100 windows, supersedes it.** The timings are monotonic and
nsamples is the cost driver: 0.47s per window at 10, 0.58 at 25, 0.78 at 50, 2.19 at 100
and 4.84 at 200, which is 10.3 times the cost at 10.

**Extrapolated to the real explained set**, 862 windows across five models: about 1.2
hours at nsamples 50 against 5.8 hours at the library default of 200.

**Consequence:** `PREREGISTRATION.md` Amendment 19 fixes nsamples at 50 on this cost
curve. The stability figures from the same measurement are recorded there as fixture-only
evidence, having been measured on Gaussian noise where there is no signal for attributions
to find.

---

## 2026-08-12 — the SHAP cell called the explainer nineteen times per model

**What was wrong:** `sequence_attributions` called `shap_values` once per class, nineteen
times per model. Each call met a new batch shape and retraced. On the dry-run fixture, 228
explained windows across five models did not finish in half an hour.

**The fix:** one `shap_values` call over every explained window, sliced per class
afterwards. The aggregation is unchanged.

**Where it was found:** the dry run, `tools/dry_run`, on CPU on the fixture. It was not
found in Colab, and it would have cost a session there. The same run also established that
`nsamples` was being taken from a library default and had never been fixed.

---

## 2026-08-12 — the 50 percent and the 70 percent measure different quantities

**Decision:** nothing changes. H3's threshold stays at 70 percent, and this entry records
why the two figures were never in competition.

**The 50 percent is a capture-identification accuracy.** `PREREGISTRATION.md` Amendment 3
stated it as the first clause of H3: timing features will identify the source capture at
above 50 percent accuracy with the attack class held fixed. Its fails-if reads
"capture-identification accuracy with class fixed falls below 0.50". Amendment 7 dropped
it as a hypothesis clause and retained it as a reported result. It appears in
`PROJECT_RECORD.md` Section 3 under "Reported results — not hypothesis tests" as capture
identifiability, served by notebook 03, and in Section 5 at 0.8280 with the attack class
held fixed against a mean chance rate of 0.1750.

**The 70 percent is a proportion of classes whose mapped category matches the reference
standard.** It is the only threshold H3 has ever carried for STRIDE consistency: it
appears in Amendment 7, in Amendment 9 and in Section 3, and no 50 percent figure is
attached to STRIDE consistency anywhere in the record.

**What Amendment 7 records about it.** The 70 percent criterion appears in no earlier
amendment and is not a narrowing of any Amendment 3 clause, measuring agreement between
the mapping and the attack semantics documented in the benchmark paper, which no earlier
clause measured. Amendment 2 carried a different STRIDE clause, a permutation test on SHAP
profile separation, and Amendment 3 withdrew it.

**The margin.** `config/stride_ground_truth.yaml` assigns 12 of the 18 attack classes to
Denial of Service, a majority-class baseline of 0.667. Seventy percent of 18 is 12.6, so
the pass mark is 13 and clears that baseline by one class. A 50 percent bar on the same
denominator would be 10 of 18, two classes below the baseline count.

**What this does not do:** no amendment is made and no file changes. H3 stands as
Amendment 9 states it.

---

## 2026-08-13 — the TreeExplainer cost estimate was wrong by an order of magnitude

**What was estimated:** minutes. The NB09 design report put TreeSHAP on the forest at
"minutes" and treated the forest arm as negligible beside the sequence training.

**What happened:** on 2026-08-12 the pass ran for over an hour against 33,653 explained
records and was interrupted without completing. The forest it explains is 100 trees at
`min_samples_leaf` 20, fitted over 999,998 records, so the trees are deep and TreeSHAP's
cost scales with depth and leaf count rather than with the number of trees alone. The
estimate did not account for that.

**What did complete:** the forest fit itself. `forest_timing_excluded` wrote all five
files, cross-validated over five folds, and scored macro-F1 0.5910 on 1,229,711 records in
107.8 seconds. Only the attribution pass is outstanding.

**Where the arm sits:** in a notebook holding an A100, while needing no GPU. TreeSHAP is
CPU work and the sequence training is not, so the hour was spent on an accelerator that
the outstanding work cannot use.

**What the resume run has to complete, on a free CPU runtime:** the TreeExplainer pass,
and `attributions.json`. The second is not optional. It is written once in the cell after
the forest, so the interruption cost it, and NB09b reads it separately from its glob over
the per-seed files. NB09b cannot run until it exists. The resume skips already in NB09a
will pass over the five sequence fits, the five attribution files and the forest fit, so a
CPU run reaches the outstanding work directly.
