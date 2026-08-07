# AG_PRAXIS — Pre-Registration

Written before any experiment. Hypotheses and failure thresholds are fixed here.
A result that contradicts an expectation is reported, not reframed.

---

## Objective 1 — Establish an honest performance baseline

Quantify the effect of capture-file leakage on reported detection performance for
CICIoMT2024, and develop a sequence-based detector evaluated under capture-disjoint
splits using macro-averaged metrics.

**RQ1.** To what extent does capture-file leakage inflate reported detection
performance on CICIoMT2024, and does sequence-based modelling improve detection once
that leakage is removed?

**H1.** Under capture-disjoint evaluation, macro-F1 will fall below the value obtained
under the shipped within-capture split by more than 0.05.

- Test: identical model and configuration, only the split protocol changes.
- Fails if: the difference is 0.05 or less.
- If it fails: RQ1 reframes to reporting honest performance on a sound benchmark.
  Objectives 2 and 3 are unaffected.

**H1b.** Under capture-disjoint evaluation, the sequence model will achieve higher
macro-F1 than the single-record baseline, by more than the across-seed standard
deviation.

- Test: five seeds each, macro-F1 mean and standard deviation, McNemar on paired
  predictions.
- Fails if: the gain is within one standard deviation, or McNemar is not significant
  at alpha = 0.05.
- If it fails: reported as a finding that these attacks are identifiable from single
  records and temporal context adds nothing.

---

## Objective 2 — Recover the underrepresented attack classes

Diagnose why minority classes fail, evaluate class-imbalance interventions
independently, and document the resulting gains alongside their cost to
majority-class performance.

**RQ2.** Can class-imbalance interventions recover the attack classes that
macro-averaged evaluation reveals as failing, and what is the cost to majority-class
performance?

**H2.** At least one intervention will raise macro-F1 above baseline by more than the
across-seed standard deviation, with a proportionally smaller decrease in
majority-class F1.

- Interventions tested independently: logit adjustment, class-weighted loss, focal
  loss, window-level resampling, per-class threshold tuning.
- Test: one change per run, five seeds, McNemar with Holm-Bonferroni correction.
- Fails if: no intervention exceeds one standard deviation, or gains on minority
  classes are matched by equal or larger majority-class losses.
- If it fails: reported as evidence that the failure is not caused by imbalance,
  directing attention to feature separability instead.

---

## Objective 3 — Translate detection into actionable threat intelligence

Map model explanations to established attack patterns and threat categories, validate
the mappings computationally, and assess whether postmarket surveillance can capture
the threats identified.

**RQ3.** Can model explanations be systematically linked to established attack
patterns and threat categories, and does postmarket surveillance capture the threats
so identified?

**H3a.** SHAP profiles will differ significantly between attack classes mapped to
different STRIDE categories.

- Test: within-category versus between-category distance, permutation test,
  alpha = 0.05.
- Fails if: p >= 0.05, indicating the mapping carries no structure.

**H3b.** Feature attributions will be stable across seeds.

- Test: Kendall's tau on top-10 features across five seeds.
- Fails if: tau < 0.7.
- If it fails: reported as a finding about explanation instability, which is itself
  relevant to the explainable-IDS literature.

**H3c.** The proportion of MAUDE records attributable to cyberattack will be
negligible relative to documented incident rates.

- Test: keyword and category search of MAUDE bulk records.
- Fails if: cyber-attributable records are found at a rate comparable to documented
  incidence, indicating surveillance is adequate.

---

## Fixed parameters

| Parameter | Value |
|---|---|
| Seed | 42 |
| Split | 70 / 15 / 15, capture-disjoint |
| Window | 50 records |
| Stride | 25 records |
| Batch size | 32 |
| Epochs | 10 |
| Primary metric | macro-F1 |
| Significance test | McNemar, Holm-Bonferroni correction |
| Seeds for stability | 5 |

---

## Standing commitments

- One change per experimental run.
- Hyperparameters tuned on validation only. Test evaluated once per configuration.
- Every run logged, including runs that made results worse.
- The ledger is append-only. Corrections are appended, never overwritten.
- Negative results are reported as findings.

---

# Amendment 1 — 2026-08-02

Made before any model was trained. Prompted by the capture inventory in NB01, which
established that eleven of nineteen classes are represented by a single capture and
cannot be evaluated under a fully capture-disjoint split.

## H1 — replaces the original statement

**H1.** Macro-F1 under the strictest disjoint split each class permits will fall
below the value obtained under the shipped within-capture split by more than 0.05.

- Test: identical model and configuration, only the split protocol changes.
- Fails if: the difference is 0.05 or less.

## H1c — new

**H1c.** Within a single evaluation under the two-tier protocol, Tier B classes
(single capture, contiguous block split) will show higher F1 relative to their class
support than Tier A classes (multiple captures, whole chunks held out).

- Rationale: Tier B retains within-capture continuity between training and test
  partitions that Tier A does not. If capture provenance carries signal, that
  advantage should be visible.
- Test: per-class F1 regressed on log class support, separately by tier. Compare
  residuals between tiers.
- Fails if: Tier B shows no advantage once support is accounted for, indicating
  within-capture continuity confers no benefit.
- If it fails: reported as evidence that residual within-capture splitting does not
  materially inflate performance, which narrows but does not eliminate the leakage
  argument.

## Tier definitions, fixed here

**Tier A** — eight classes, whole capture chunks held out:
DDoS-ICMP, DDoS-SYN, DDoS-TCP, DDoS-UDP, DoS-ICMP, DoS-SYN, DoS-TCP, DoS-UDP.

**Tier B** — eleven classes, contiguous block split 70/15/15 within the single
capture:
Benign, Spoofing, MQTT-DDoS-Connect_Flood, MQTT-DDoS-Publish_Flood,
MQTT-DoS-Connect_Flood, MQTT-DoS-Publish_Flood, MQTT-Malformed_Data,
Recon-OS_Scan, Recon-Ping_Sweep, Recon-Port_Scan, Recon-VulScan.

Macro-F1 is reported overall and separately by tier in all experiments.


---

# Amendment 2 — 2026-08-02

Made before any model was trained. All three hypotheses restated with explicit numeric thresholds.

## H1

Under a capture-disjoint split, a sequence-based detector will achieve macro-F1 at least 0.03 above a single-record baseline, while the same protocol reduces macro-F1 by more than 0.05 relative to the shipped within-capture split.

- Fails if: the sequence gain is below 0.03 or within one standard deviation, or the protocol difference is 0.05 or less.

## H2

At least one class-imbalance intervention will raise macro-F1 by at least 0.05 over baseline and lift at least three of the four lowest-scoring classes to F1 of 0.40 or above, while reducing mean majority-class F1 by no more than 0.02.

The four target classes are fixed here as Recon-VulScan, Recon-OS_Scan, MQTT-DDoS-Publish_Flood, and Spoofing. The majority set is the eight classes with highest support.

- Independent: intervention type, one per run — logit adjustment, class-weighted loss, focal loss, window-level resampling, per-class threshold tuning.
- Dependent: macro-F1; per-class F1 for the four target classes; mean F1 across the eight majority classes.
- Testable: five seeds per intervention; gain must exceed the across-seed standard deviation; McNemar with Holm-Bonferroni correction.
- Fails if: no intervention meets all three conditions.

## H3

Feature attributions will show Kendall's tau of 0.70 or above across five seeds, SHAP profiles will separate by STRIDE category at p below 0.05, and fewer than one percent of matched MAUDE records will be attributable to cyberattack.

- Fails if: tau falls below 0.70, or the permutation test returns p of 0.05 or greater.

The denominator for the MAUDE proportion is defined before searching as records matching the device categories represented in CICIoMT2024.

---

# Amendment 3 — 2026-08-02

Made after NB04, before any detector was trained.

## Test result: H1 second clause not supported

Amendment 2 stated that a capture-disjoint split would reduce macro-F1 by more than 0.05 relative to the shipped within-capture split.

NB04 measured this on the eight Tier A classes, the only classes where the comparison is possible, using the full dataset. Macro-F1 with a whole capture held out was 0.9993; with rows pooled across captures it was 0.9995. The difference is 0.0002. The result is stable: the same comparison at one percent sampling gave 0.0004.

The clause is not supported and cannot be tested elsewhere. The eleven Tier B classes have a single capture each, so no capture can be held out.

Interpretation: capture identity is recoverable, but on multi-capture classes the detector does not depend on it. Both figures sit at ceiling. This null is retained and reported as a finding, since the leakage literature assumes identifiability implies score inflation.

## Test result: capture identifiability supported

NB04 also measured whether the features identify the source recording. Across fifty captures against a chance baseline of 0.02, a RandomForest reached 0.9340 using all 43 features and 0.9427 with the attack class held fixed. Four timing features — Duration, Rate, Srate, IAT — reached 0.9364 alone. The five features named as most important by prior work reached 0.9444. Protocol features reached 0.2471 and statistical features 0.1280.

## H1c withdrawn

Amendment 1 stated H1c, comparing Tier B and Tier A performance adjusted for class support. It is withdrawn as a hypothesis and retained as a reported analysis. With eight and eleven classes, a support-adjusted residual comparison has too little power to carry a formal claim. Recorded before the analysis was run.

## Restructure

The three objectives are restated as the conditions a threat model built from observation must satisfy: timeliness, coverage, and trustworthy translation. The research questions and hypotheses are restated accordingly. Objective 2 is unchanged in substance.

### H1 — Timeliness

Sequence-based detection will identify at least twelve of nineteen threat classes at F1 of 0.80 or above within fifty observed records, and will exceed single-record classification by at least 0.03 macro-F1, with median minimum-observation requirements differing at least threefold between volumetric and low-rate classes.

- Independent: observation budget k in {5, 10, 25, 50}; model input structure.
- Dependent: per-class F1 at each budget; macro-F1; median minimum number of records per class.
- Testable: budget sweep under capture-disjoint evaluation; five seeds, mean and standard deviation; McNemar on paired predictions at alpha = 0.05.
- Fails if: fewer than twelve classes reach F1 of 0.80 at k = 50, or the sequence gain falls below 0.03, or minimum-observation requirements show no systematic difference between attack families.

### H2 — Coverage

Unchanged from Amendment 2.

### H3 — Trustworthy translation

Timing features will identify the source capture at above 50 percent accuracy with attack class held fixed and will rank in the top five by SHAP importance; attributions will show Kendall's tau of 0.70 or above across five seeds; and fewer than one percent of matched MAUDE records will be attributable to cyberattack.

- Independent: feature family; STRIDE category assignment under a deterministic rule fixed in advance; random seed.
- Dependent: capture-identification accuracy with class fixed; SHAP rank of timing features; Kendall's tau on top-10 features; percentage of cyber-attributable MAUDE records.
- Testable: RandomForest capture-identity classifier per family, equal row draws per capture, chance baseline 0.02 across fifty captures; tau across five seeds; keyword and category search of MAUDE bulk records.
- Fails if: capture-identification accuracy with class fixed falls below 0.50, or timing features do not rank in the top five by SHAP importance, or tau falls below 0.70.

First clause already supported by NB04 at 0.9427. Remaining clauses open.

The permutation test on STRIDE separation, stated in Amendment 2, is withdrawn as a hypothesis clause and retained as a reported analysis. Eight Tier A and eleven Tier B classes give too few groups for the test to carry weight. Recorded before the test was run.

---

# Amendment 4 — 2026-08-04

Made after NB04, before any model was trained.

## Sequence counts and one class too small to evaluate

NB04 built the sequences at window 50 and stride 25. Recon-Ping_Sweep yields 24
training, 2 validation and 4 test sequences from its 926 records. An F1 computed on two
samples can only take the values 0, 0.5 or 1, so no per-class metric on that partition
is interpretable.

H1 compares the median records-to-threshold of low-rate classes against volumetric
classes. Recon-Ping_Sweep is excluded from that median. The low-rate group is therefore
Recon-OS_Scan, Recon-Port_Scan, Recon-VulScan, Spoofing and MQTT-Malformed_Data. The
volumetric group is unchanged: the eight DDoS and DoS classes.

Recon-Ping_Sweep's per-class figures are still reported, marked as resting on too few
sequences to interpret.

Recon-VulScan at 18 validation sequences and MQTT-Malformed_Data at 38 are also thin.
Both are retained in the low-rate group, and their per-class figures carry the same
caveat wherever they are reported.

## The window is not adjusted for small classes

Window 50 and stride 25 are unchanged. Shortening the stride for the smaller classes
would produce near-duplicate windows and would make those classes incomparable with the
rest. This is recorded before NB06 runs so that the parameters cannot be read as having
been chosen once results were known.

## Tier B partition boundaries

Classes with a single recording concatenate their train and test files and cut at 70
and 85 percent of the whole, so a partition can span the file boundary. The two files
are halves of one recording, so this is the correct treatment, but it is a design
choice and is stated as such. Benign trains on Benign_train rows 0 to 161,237,
validates on Benign_train rows 161,237 to 192,732 plus Benign_test rows 0 to 3,056, and
tests on the remainder of Benign_test.


---

# Amendment 5 — 2026-08-05

Made after the NB05 baseline runs, before NB06 was written.

## Numbering

Under the numbering fixed by PROJECT_RECORD.md v1.0, H2 is the sequence hypothesis.
The class-imbalance intervention claim carried under the H2 label in Amendments 2 and
3 is no longer a hypothesis. It is a reported result of NB07, listed in
PROJECT_RECORD.md Section 3 under "Reported results — not hypothesis tests".
Amendments 2 and 3 stand as written and are not edited.

## H2 — replaces the previous statement

**H2.** Sequence-based detection improves macro-averaged F1 on the attack classes
the published CNN model fails to detect.

## What is superseded

PROJECT_RECORD.md Section 3 row 2 previously required a mean pairwise F1 gain of at
least 0.05 on within-family pairs. That threshold is superseded and is no longer the
test H2 stands or falls on. Mean pairwise F1 is still computed and reported in
Chapter 4 as a secondary result.

## The class set, fixed here

The class set is fixed by the published_cnn_19class run in NB05, which ran before
NB06 was written. The classes scoring F1 below 0.50 in that run are Recon-VulScan,
Recon-OS_Scan, MQTT-DDoS-Publish_Flood and Spoofing.

## The threshold

A class counts as detected at F1 of 0.50 or above. The same threshold defines
membership of the set above and defines improvement on it.

## The comparator

The comparator named in H2 is the published CNN. The single-record random forest is
reported as a third comparison in Chapter 4 but is not the hypothesis comparator.


---

# Amendment 6 — 2026-08-05

## Correction to the H2 class set

Amendment 5 named four classes as scoring F1 below 0.50 in the published_cnn_19class
run. Reading metrics.json for that run directly shows six. The four named came from a
separate reproduction reported in PROJECT_RECORD.md Section 5, which scores macro-F1
0.75 against 0.7110 for published_cnn_19class and reports Spoofing at 0.40 against
0.3438. The two are not the same run.

The six classes below F1 0.50 in published_cnn_19class are Recon-VulScan 0.0000,
Recon-Ping_Sweep 0.0107, Recon-OS_Scan 0.0343, MQTT-DDoS-Publish_Flood 0.1858,
Spoofing 0.3438 and MQTT-Malformed_Data 0.4883.

## The set used for H2

Recon-Ping_Sweep is excluded, on the rule already fixed in Amendment 4: it yields 2
validation and 4 test sequences at window 50 and stride 25, so no per-class metric on
that partition is interpretable. Its per-class figures are still reported, marked as
resting on too few sequences to interpret.

The H2 class set is therefore Recon-VulScan, Recon-OS_Scan, MQTT-DDoS-Publish_Flood,
Spoofing and MQTT-Malformed_Data.

MQTT-Malformed_Data is retained despite sitting close to the threshold. No rule
excludes it, and dropping a borderline class after seeing its value would be a
post-hoc choice.

## The threshold

Unchanged. A class counts as detected at F1 of 0.50 or above.


---

# Amendment 7 — 2026-08-05

H1 and H3 were restated when PROJECT_RECORD.md v1.0 was written on 3 August 2026. No
amendment recorded either change at the time. This amendment records them.

## H1 — replaces the statement in Amendment 3

**H1.** Reconnaissance and low-rate attack classes will require at least twice as many
observed records to reach F1 >= 0.80 as volumetric flooding classes.

Metric: records observed to reach F1 >= 0.80, per class. Notebooks 04, 06 and 08.

## What changed in H1, and when

Restated on 3 August 2026, when PROJECT_RECORD.md v1.0 was written, before NB06 was
run. Amendment 3 stated H1 as three conjuncts. Two were dropped and one was altered.

**Clause 1, dropped.** "at least twelve of nineteen threat classes at F1 of 0.80 or
above within fifty observed records". Nothing in v1.0 sets a number of classes that
must reach F1 0.80, and the ceiling of fifty observed records is not carried.

**Clause 2, dropped.** "will exceed single-record classification by at least 0.03
macro-F1". A sequence-versus-single-record claim now sits in H2, but Amendment 5
restates H2 against the published CNN with no numeric macro-F1 threshold, so the 0.03
figure is no longer stated anywhere in the project.

**Clause 3, retained and altered in three ways.** Amendment 3 read "median
minimum-observation requirements differing at least threefold between volumetric and
low-rate classes".

- The multiple is twice, not threefold.
- The aggregation is no longer stated. Amendment 3 compared medians. v1.0 states the
  metric as records observed to reach F1 >= 0.80, per class, and names no summary
  statistic. Amendment 4's exclusion of Recon-Ping_Sweep was written against a median
  and still presumes one.
- The direction is now fixed. Amendment 3 required the requirements to differ, which a
  difference in either direction satisfies. v1.0 requires low-rate classes to need more
  records than volumetric ones.

**Scaffold, dropped.** The observation budget k in {5, 10, 25, 50} is no longer fixed,
so the grid on which records observed is measured is open. The failure condition is
dropped; v1.0 states no fails-if for any hypothesis. Five seeds and McNemar at alpha
0.05 survive in Section 8's fixed parameters rather than attached to H1.

**Group membership, unresolved.** v1.0 Section 3 lists Recon-Ping_Sweep in the low-rate
group. Amendment 4 excludes it from the H1 median, because two validation and four test
sequences cannot support a per-class metric. The two statements disagree. The exclusion
in Amendment 4 governs, and PROJECT_RECORD.md Section 3's low-rate group listing is to
be corrected to match. That correction is logged as an open item in Section 11 rather
than made here.

## H3 — replaces the statement in Amendment 3

**H3.** For at least 70% of attack classes, the deterministic mapping will assign a
STRIDE category consistent with that class's documented attack semantics in the
CICIoMT2024 benchmark paper.

Metric: proportion of classes with a consistent STRIDE assignment. Notebook 09.

## What changed in H3, and when

Restated on 3 August 2026, when PROJECT_RECORD.md v1.0 was written, before NB09 was
run. H3 as stated in v1.0 shares no clause with H3 as stated in Amendment 3. All four
of Amendment 3's clauses left the hypothesis, and the clause that replaced them is new.

**Clause 1, dropped as a hypothesis clause, retained as a reported result.** "Timing
features will identify the source capture at above 50 percent accuracy with attack
class held fixed." Amendment 3 recorded it as already supported at 0.9427. It now
appears in v1.0 Section 3 under "Reported results — not hypothesis tests" as capture
identifiability, served by notebook 03, and in Section 5 at 0.8280 with the attack
class held fixed.

**Clause 2, dropped, and no longer testable.** "and will rank in the top five by SHAP
importance." v1.0 Section 5 fixes SHAP to run on a timing-excluded model in NB09,
dropping Duration, Rate, Srate and IAT and leaving 40 features. Timing features cannot
hold a SHAP rank under that design, so the clause is not merely unstated but foreclosed.

**Clause 3, moved to a reported result.** "attributions will show Kendall's tau of 0.70
or above across five seeds." It appears in v1.0 Section 3 as attribution stability,
Kendall's tau, served by notebook 09, reported with the mapping. The 0.70 threshold is
not carried, so tau is reported without a pass mark.

**Clause 4, moved to a reported result.** "fewer than one percent of matched MAUDE
records will be attributable to cyberattack." It appears as the MAUDE cyber-attributable
share, served by notebook 09, as corroboration and surveillance coverage. The one
percent threshold is not carried.

**New clause, first stated in v1.0.** The 70 percent STRIDE consistency criterion
appears in no amendment. It is not a narrowing of any Amendment 3 clause: it measures
agreement between the deterministic mapping and the attack semantics documented in the
benchmark paper, which no earlier clause measured. Amendment 2 carried a different
STRIDE clause, a permutation test on SHAP profile separation at p below 0.05, and
Amendment 3 withdrew it. The 70 percent criterion is not that test.

**Scaffold, dropped.** Amendment 3's independent, dependent, testable and fails-if
entries for H3 are not carried into v1.0.

## Notebook renumbering

Amendment 3 is headed "Made after NB04" and cites capture-identification figures of
0.9340 and 0.9427. Under the numbering fixed by PROJECT_RECORD.md v1.0 Section 7, that
work is notebook 03, Feature Provenance Check. Section 5 records the same experiment
re-run under a constrained model at 0.8010 and 0.8280 and notes the earlier figures came
from 100 trees with no leaf constraint. References to NB04 in Amendments 1 through 3
mean the notebook now numbered 03.

The feature count differs between the two records of that same earlier run. Amendment 3
states 0.9340 was reached using all 43 features. v1.0 Section 5 reports 44 features
remaining after Drate is dropped from the 45 released columns. The discrepancy is
recorded here and not resolved.


---

# Amendment 8 — 2026-08-05

Made after Amendment 7, before NB06 was run.

## H1 — the median is named again

**H1.** The median number of observed records that low-rate attack classes require to
reach F1 >= 0.80 will be at least twice the median for volumetric flooding classes.

Amendment 7 recorded that v1.0 dropped the aggregation Amendment 3 had stated:
Amendment 3 compared medians, v1.0 stated the comparison with no summary statistic, and
Amendment 4's exclusion of Recon-Ping_Sweep continued to presume one. The median is
named again here.

Only the aggregation is restored. The multiple stays at twice, not the threefold of
Amendment 3, and the direction stays as v1.0 fixed it: low-rate classes require more
observed records than volumetric ones. The metric is unchanged — records observed to
reach F1 >= 0.80, measured per class and compared as group medians.

## The low-rate group listing is corrected

Amendment 4 fixed the low-rate group for the H1 median as Recon-OS_Scan,
Recon-Port_Scan, Recon-VulScan, Spoofing and MQTT-Malformed_Data, excluding
Recon-Ping_Sweep. PROJECT_RECORD.md v1.0 Section 3 listed Recon-Ping_Sweep among the
low-rate classes, which Amendment 7 recorded as an unresolved disagreement between the
two files. Section 3's listing is corrected to match Amendment 4. The volumetric group
is unchanged.

The exclusion rests on sequence count, not on measured performance. At window 50 and
stride 25 Recon-Ping_Sweep's 926 records yield 2 validation and 4 test sequences, and an
F1 computed on two samples can only take the values 0, 0.5 or 1. Its per-class figures
are still reported, marked as resting on too few sequences to interpret. The same
exclusion applies to the H2 class set under Amendment 6.

This closes the disagreement Amendment 7 left open.


---

# Amendment 9 — 2026-08-06

Made after Amendment 8. Section 3's objectives, questions and hypotheses were
reworded for consistency. One hypothesis is reworded. The rest carries no
hypothesis content.

## H3 — reworded to name SHAP as the subject

**H3.** For at least 70% of attack classes, SHAP explanations of the detection
model will map to a STRIDE category consistent with that class's documented
attack semantics.

The previous statement made the deterministic mapping the subject and left SHAP
implicit. The new statement makes SHAP explanations of the detection model the
subject. The 70% threshold is unchanged. The reference standard is unchanged: the
attack semantics documented in the CICIoMT2024 benchmark paper. The metric is
unchanged: the proportion of classes with a consistent STRIDE assignment. Made
before NB09 was run.

Section 3's H3 cell names the reference standard inline, ending "consistent with
that class's documented attack semantics in the CICIoMT2024 benchmark paper." The
boldface statement above stops at "documented attack semantics" and names the paper
in the prose that follows. The two say the same thing; only the placement differs.

## Wording changes carrying no hypothesis content

**H1, considered for shortening and left alone.** A shorter form was drafted:
"Low-rate attack classes will require at least twice the median observed records
of volumetric flooding classes to reach F1 >= 0.80." It names the median only on
the volumetric side, so the low-rate side reads as a per-class requirement rather
than a group median. That is the ambiguity Amendments 7 and 8 closed, so H1 stands
exactly as Amendment 8 states it and is unchanged by this amendment.

**RO1.** Previously named developing and validating a sequence-based neural
architecture that models the temporal structure of IoMT network traffic, and then
determining how much observation each class requires. It now states the
determination and names the sequence-based detector as the means.

**RQ1.** Previously asked both how accurately a model can identify threats from
partial observations and how many records must be observed. It now asks only the
records question. Per-class F1 at each observation budget is still what the
records figure is read from.

**RO2.** Previously named "the attack variants that flow-level features do not
separate" and now names "the attack classes the published CNN model fails to
detect". This aligns RO2 with the class set H2 tests. The two named different sets.

An intermediate wording, "the attack classes single-record classification fails to
detect", was considered and rejected. Amendment 5 fixes the H2 comparator as the
published CNN and excludes the single-record random forest, which resolves three of
the five classes in the set — Recon-OS_Scan, Spoofing and MQTT-Malformed_Data.
Naming single-record classification would therefore have named a smaller set than
H2 tests, reintroducing the mismatch this change closes.

**RQ2.** Drops "and which threat classes benefit most?". The question is still
answered: the class-imbalance interventions in notebook 07 are listed in Section 3
as a second route to it, and per-class F1 change is the row 2 metric.

**Row 2 metric.** "per-class F1" becomes "per-class F1 change", on the same class
set. The set is unchanged, fixed by Amendment 6 as Recon-VulScan, Recon-OS_Scan,
MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data.

**RO3.** Previously said the resulting threat records are corroborated against FDA
MAUDE adverse events. It now says the pipeline assesses whether postmarket
surveillance captures the threats identified. This matches the scoping recorded in
Amendment 7, where the MAUDE cyber-attributable share is a reported result rather
than a hypothesis clause, and it matches Objective 3 as stated at the head of this
file.

**RQ3.** Previously asked whether explanations can be mapped to STRIDE via a CAPEC
ontology pipeline linked to MAUDE signals, to produce actionable threat
intelligence. It now asks whether they can be mapped to STRIDE categories
consistent with documented attack semantics. The CAPEC pipeline and MAUDE remain
in RO3 and in notebook 09.

None of these changes a hypothesis, a threshold, a metric or a class set.

---

# Amendment 10 — 2026-08-07

Made after NB06 was run. This amendment records a gap between two statements of H2.
It changes no hypothesis, no threshold and no class set.

## What Amendment 2 carried

Amendment 2 stated H2 as three conditions held together: macro-F1 up by at least
0.05, at least three of the four lowest-scoring classes lifted to F1 0.40 or above,
and mean majority-class F1 reduced by no more than 0.02. The majority set was
defined there as the eight classes with highest support, which are the eight DDoS
and DoS classes.

The third condition is a cost clause. It said what a gain on the minority classes
was not allowed to cost the majority ones.

## What Amendment 5 carries

Amendment 5 replaced that statement with a single sentence: sequence-based
detection improves macro-averaged F1 on the attack classes the published CNN model
fails to detect. Amendment 6 fixed the class set at Recon-VulScan, Recon-OS_Scan,
MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data, and fixed the threshold
at F1 0.50.

No cost clause survives that replacement. H2 as stated in Amendment 5, and as
carried in PROJECT_RECORD.md from v1.0 onward, says nothing about what happens to
the classes outside the named set.

## The result the clause would have spoken to

NB06 trained the sequence model on the two-tier split at seed 42, window 50 and
stride 25. Against `published_cnn_19class`, across all nineteen classes, nine
classes gained F1 and ten lost. The gains sum to +2.0566 and the losses to -2.0033.
The five largest losses fall on volumetric classes and sum to -1.7662, which is 88%
of the total negative movement. DoS-ICMP crossed below the F1 0.50 line, 0.9960 to
0.3178, a loss larger in magnitude than any single class's gain among the five named
classes.

The quantity Amendment 2's cost clause named is the mean F1 across the eight
highest-support classes. That quantity moved 0.9972 to 0.7613, a difference of
-0.2358, against the 0.02 limit the withdrawn clause set. H2 as it now stands sets
no limit on this quantity. The figure states what the withdrawn clause's threshold
would have measured. It does not evaluate H2.

Figures from `data/processed/NB06/metrics.json` against
`results/NB05/published_cnn_19class/metrics.json`, at full precision. The two runs
are scored on different test partitions and different units, windows against
records, so these are two runs' own scores rather than a paired comparison.

## What this amendment does not do

It records the gap. It does not resolve it.

H2 is unchanged. It is evaluated on the five classes fixed in Amendment 6, at the
F1 0.50 threshold fixed in Amendment 5, and the movement described above sits
outside that set and does not bear on whether H2 is supported.

Whether a majority-class safeguard should be reinstated is left open. This
amendment sets no such threshold.
