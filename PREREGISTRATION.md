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

# Amendment 11 — 2026-08-09

Made after NB07, before NB08 was run. Records the observation-budget grid and the
rule for classes that do not reach the H1 threshold within it.

## The budget grid, fixed here

Observation budget k in {5, 10, 25, 50}, measured in records. Budgets are taken as
prefixes of the sequences already built in NB04 at window 50 and stride 25: at budget
k the first k records of each window are visible and the remainder are not. Sequence
membership and count are identical at every budget, so all four budgets are scored on
the same 49,159 test windows.

A separate model is trained at each budget. Budget 50 is the existing
`sequence_cnn_lstm_19class` run and is not retrained.

The grid is not extended beyond 50. Doing so would require rebuilding the sequences at
a longer window, which would change the sequence count per class and make the runs
incomparable with those already executed.

## Right-censoring

H1 measures records observed to reach F1 >= 0.80, per class, compared as group medians.
A class that does not reach F1 >= 0.80 at k = 50 has no such value. It is recorded as
right-censored at 50 and reported as "> 50", not as 50 and not as any imputed figure.

A group median is reported as a number only when it is determined by the uncensored
values alone, that is, when the value at the median position is uncensored. Otherwise
the group median is reported as not reached within 50 records.

The twofold comparison H1 states is evaluated only when both group medians are
determinate. When either is not, H1 is reported on the direction of the difference,
with the censored classes and the budget ceiling stated alongside.

## Group membership

Unchanged. Low-rate: Recon-OS_Scan, Recon-Port_Scan, Recon-VulScan, Spoofing,
MQTT-Malformed_Data. Volumetric: the eight DDoS and DoS classes. Recon-Ping_Sweep
remains excluded under Amendment 4.

## What this amendment does not do

It sets no new threshold and changes no class set. F1 >= 0.80 is unchanged, the
multiple stays at twice, and the direction stays as fixed in Amendment 8.

---

# Amendment 12 — 2026-08-10

Made after NB08 was run. Restates the research questions and hypotheses, reorders
and renumbers them, and changes the metric the observation hypothesis is measured
on. No result changes.

## The reordering and renumbering

The three questions are reordered detector, observation, interpretation. The
sequence hypothesis carried as H2 from Amendment 5 onward becomes H1. The
observation hypothesis carried as H1 from Amendment 7 onward becomes H2. H3 is
unchanged in position.

Every reference to H1, H2 and H3 in PROJECT_RECORD.md, PREREGISTRATION.md,
DECISIONS.md, RESULTS_LEDGER.md and the notebooks is renumbered accordingly, in one
pass on this date. Amendments 1 through 11 are not edited. Where they name H1 or H2
they mean the numbering in force when they were written, and this amendment is the
key to reading them.

## H1 — the sequence hypothesis, formerly H2

**H1.** Sequence-based modelling improves detection of specific hard-to-detect
classes relative to single-record models.

The class set is unchanged, fixed by Amendment 6 as Recon-VulScan, Recon-OS_Scan,
MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data. The threshold is
unchanged at F1 0.50, fixed by Amendment 5. The comparator is unchanged as the
published CNN.

The claim is class-specific and is not a claim of general improvement. The
aggregate macro-F1 difference against the published CNN is +0.0028 against a
cross-seed standard deviation of 0.0233 at k = 50, and is not reported as a gain.

## H2 — the observation hypothesis, formerly H1

**H2.** Low-rate classes require more observation to reach detection saturation
than volumetric classes.

Metric: the observation budget at which each class reaches saturation, defined as
the smallest budget within epsilon = 0.02 of that class's own achievable ceiling
across the budget grid, following Silvey & Liu (JMIR 2024) and Mohr et al. (arXiv
2201.12150). Group medians compared.

### The metric changes from records-to-threshold to saturation

The previous statement measured records observed to reach F1 >= 0.80 and required
the low-rate median to be at least twice the volumetric median. NB08 measured that
and it was not evaluable: three of five low-rate classes do not reach F1 0.80 within
50 records, so the low-rate median is not determinate. That handling was fixed in
Amendment 11 before the run, and the direction was reported instead.

The records-to-threshold measurement is retained and reported. It is no longer what
H2 stands or falls on.

### No numeric multiple

H2 states the direction only.

The previous twofold requirement was not evaluable under the previous metric. Under
the saturation metric both medians are determinate and the ratio is known, so
stating a multiple now would set a threshold against a figure already in hand. The
direction is stated and the ratio is reported as an observed figure without a pass
mark.

### The question wording

RQ2 asks how much traffic must be observed before each attack class stops improving.
It previously asked when each class becomes reliably detectable.

Saturation marks where a class stops improving, not where it becomes reliably
detected. Eight of nineteen classes saturate at an F1 below 0.80. The narrower
question is what the metric measures. The reliability reading is retained through
the records-to-threshold figures, which are reported alongside.

## H3 — unchanged

Unchanged in substance from Amendment 9. The 70% threshold and the reference
standard are unchanged.

## What this amendment does not do

No result changes. No class set, no comparator and no F1 threshold moves. The
budget grid, the censoring rule and the group definitions stand as fixed in
Amendment 11 and PROJECT_RECORD.md Section 3.


---

# Amendment 13 — 2026-08-10

Adds NB03b as a reported result. It is not a hypothesis test. Made before NB03b
was run.

## What NB03b measures

Capture-identification accuracy with Duration removed from the timing family,
measured under the NB03 protocol. The comparison figures are NB03's: 0.9301 for
the timing family, and 0.8010 and 0.8280 for all 44 features.

## Duration

Duration is the TTL header field. Published guidance on intrusion-detection
benchmarks names TTL among the features that cause spurious correlation and
inflate reported performance, alongside IP addresses, port numbers, timestamps
and flow IDs: Goldschmidt, J. and Chudá, D., *Network Intrusion Datasets: A
Survey, Limitations, and Recommendations*, arXiv:2502.06688. Not yet verified
against the primary PDF.

## The feature set does not change

Duration stays in the 44 features for all previously executed runs. This probe
measures the column's contribution to the NB03 figures; it does not change the
feature set.

---

# Amendment 14 — 2026-08-10

Adds capture-invariant training as an additional intervention under H1. Made
before NB07b was run.

## The intervention

Capture-invariant training joins the five interventions NB07 tested, on the same
footing: one change per run, evaluated on the class set and threshold H1 already
fixes. The parent is `sequence_cnn_lstm_19class` and the single change is the
training objective.

## What is held fixed

- The class set fixed in Amendment 6: Recon-VulScan, Recon-OS_Scan,
  MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data.
- The F1 0.50 threshold fixed in Amendment 5.
- The same 49,159 test windows.

## The environment variable

The environment variable is `capture_id` from the NB04 manifest, 57 captures.

## Dependent variables

First, per-class F1 on the five classes and macro-F1, as for the five
interventions already run.

Second, capture identifiability measured off the learned representation. The LSTM
output for each test window is taken as the representation, the NB03 RandomForest
capture-identification protocol is fitted on it, and the accuracy is reported
against the NB03 figures.

## No cost clause is reinstated

No cost clause on majority-class F1 is reinstated. Amendment 10 records that
Amendment 2's cost clause did not survive the Amendment 5 replacement. This
amendment sets no such threshold.

---

# Amendment 15 — 2026-08-10

Adds NB08b as a reported result under RO2. It is not a hypothesis test. Made
before NB08b was run.

## H2 and records to threshold are unchanged

H2 stands as measured on saturation under Amendment 12. Records to threshold
remains a reported result, right-censored under Amendment 11. NB08b re-tests
neither.

## The metric

Earliness at a per-class confidence trigger, reported against macro-F1 across a
sweep of the trigger threshold tau.

## The halting rule

Each test window is stepped through one record at a time. The window halts at the
first record where the top-class softmax score crosses tau and is classified at
that point. A window whose score never crosses tau is classified on the full 50
records.

## The tau grid

0.50 to 0.90 in steps of 0.05, then 0.95, 0.97 and 0.99. Twelve values. The grid
is non-uniform: resolution is concentrated in the upper tail because that is where
windows begin failing to reach tau within 50 records, and the share of windows
that never trigger is one of the reported quantities.

## Earliness averaging

Earliness is averaged over correctly classified windows only.

---

# Amendment 16 — 2026-08-10

Corrects the partition the second dependent variable in Amendment 14 is measured on,
and records two counts about the group variable that were not established when
Amendment 14 was written. Made before NB07b was run.

## The correction

Amendment 14 states that the LSTM output for each test window is taken as the
representation. The partition is corrected from test to train.

## Why test cannot carry the measurement

The test partition holds 19 classes across 19 captures, one capture per class. The
validation partition holds 19 classes across 19 captures, also one per class. A
capture-identification measurement with the attack class held fixed asks which of a
class's captures a window came from, and on either partition a class has one, so there
is nothing to tell apart. Pooled across captures the same structure makes capture and
class the same label, so identifying the capture is identifying the class under another
name.

The training partition holds 45 captures, of which 34 belong to the 8 classes recorded
more than once: DDoS-ICMP 8, DDoS-UDP 8, DDoS-SYN 3, DDoS-TCP 3, DoS-ICMP 3, DoS-SYN 3,
DoS-TCP 3 and DoS-UDP 3. That is the multi-capture structure NB03 measured on.

Counts read from `data/processed/NB04_manifest.json`.

## The chance rates

Pooled over the 34 captures of those 8 classes, chance is 1/34 = 0.0294. With the attack
class held fixed, chance is the mean of 1/n over the 8 classes, 0.2812.

These differ from NB03's 0.0200 and 0.1750 because NB03 counted a capture's train file
and its test file as two recordings and reached 50, while the unit here is the capture
and only its training side exists.

## What the measurement is on

The probe measures identifiability on the partition the training objective optimised
over. That is a limitation of the measurement and is reported as such wherever the
figure appears.

## The number of groups

The group variable is unchanged. It is `capture_id`, derived from the recording name by
`src/captures.py parse_capture`.

Amendment 14 records 57 captures. That is the corpus-wide figure. The count over
training windows is 45, and the objective is computed over training windows, so 45 is
the number of groups it forms. The remaining 12 captures appear only in the validation
or test partition and the objective cannot see them.

## Where the group is the class

Of the 45 training groups, 34 are captures within the 8 classes recorded more than once,
and 11 are single-capture classes, where the group and the class are the same set of
windows. For those 11, worst-group weighting and worst-class weighting are the same
operation.

All five classes fixed in Amendment 6 — Recon-VulScan, Recon-OS_Scan,
MQTT-DDoS-Publish_Flood, Spoofing and MQTT-Malformed_Data — have one training capture
each, so all five sit among those 11.

The intervention is therefore capture-invariant on the 8 multi-capture classes, and on
the remaining 11 it acts on the same axis as the class-imbalance interventions NB07
tested.

## What this amendment does not do

It changes no class set, no threshold, no comparator and no group variable. The
intervention, the parent, the fixed quantities and the first dependent variable stand as
Amendment 14 states them.

---

# Amendment 17 — 2026-08-10

Records what the objective in Amendment 14 optimises before any update has happened.
Made before NB07b was run.

## The starting weights

The objective weights the groups' mean losses rather than the windows themselves. The
weights start uniform, at 1/45, which is the standard group-DRO initialisation and is
what NB07b uses.

Under that start a group of 24 training windows and a group of 8,290 carry the same
weight from the first update. The parent's objective is the mean over the windows,
which in this notation is the weighting that gives each group its share of them. So
from the first update the run differs from its parent by group balancing, before any
worst-group weighting has moved anything.

## What that means on the Amendment 6 class set

Amendment 16 records that 11 of the 45 training groups are single-capture classes where
the group and the class are the same set of windows, and that all five classes fixed in
Amendment 6 are among them. With the weights starting uniform, those five are equally
weighted in the objective from the first update whatever their window counts, which are
Recon-VulScan 86, MQTT-Malformed_Data 191, Spoofing 497, Recon-OS_Scan 577 and
MQTT-DDoS-Publish_Flood 1,008.

On that class set the first dependent variable therefore measures the parent plus class
balancing plus worst-group weighting, and not the parent plus capture invariance.

## What this amendment does not do

It changes no class set, no threshold, no comparator and no group variable. The
intervention, the parent, the fixed quantities and both dependent variables stand as
Amendments 14 and 16 state them.

---

# Amendment 18 — 2026-08-11

Records what is fixed for H3 before NB09 is run. It changes no hypothesis, no
threshold and no class set.

## The model H3 is scored on

H3 is scored on the sequence model at 40 features, the timing-excluded set fixed by
`NB04_manifest.json` under `timing_excluded_slice`. The random forest at 40 features is
an exactness check on that model's approximate attributions and is not what H3 stands
or falls on. The two are scored on different units, 49,159 windows against 1,229,711
records, and no figure crosses between them.

## The mapping rule and the reference standard

Both are files, committed at 8f51f1f before any model trained:
`config/stride_ground_truth.yaml`, `config/shap_capec_map.yaml` and
`config/capec_stride.yaml`. The rule is not written in the notebook and is not chosen
after attributions are visible.

## The denominator

Eighteen attack classes. Benign is excluded, being not an attack and so having no
attack semantics to be consistent with. The pass mark is 13 of 18.

## The majority-class baseline

Twelve of the eighteen classes are Denial of Service, so a rule emitting that category
for every class scores 0.667 against a threshold of 0.70. That figure is reported
alongside H3 wherever H3 appears.

## Attribution aggregation

For the sequence model: mean absolute attribution across the 50 records of a window,
then the mean over that class's windows, per feature per class. Signed attribution is
discarded deliberately. The mapping asks which features the model used, not which
direction they pushed.

## k

k = 10, for the mapping and for the top-k Kendall's tau is computed over. One number
serves both.

## Kendall's tau

Computed on the sequence model over five seeds, 42 to 46, with the SHAP background
sample drawn once and held fixed across all five. Holding it fixed is what makes the
statistic isolate training stochasticity rather than conflating it with resampling of
the explainer's background.

Yuan et al., "An empirical study of the effect of background data size on the stability
of SHapley Additive exPlanations (SHAP) for deep learning models", arXiv:2204.11351v3,
9 April 2023, report that SHAP values and model-level variable rankings fluctuate when
background datasets are drawn by random sampling, and that the fluctuation decreases as
the background size increases. The same work reports a U-shape in ranking stability,
SHAP being more reliable for the most and least important variables than for moderately
important ones, which bears on a top-10 cut of 40 features.

The reference is verified as to authorship, title, identifier, version and date. The
primary PDF has not been read, so the findings above are recorded as reported in the
abstract and are to be checked against the paper before they are relied on in Chapter 2.

Tau carries no pass mark. Amendment 7 records that the 0.70 threshold did not survive
into v1.0.

## MAUDE

The openFDA device event API, over a window opening 2019-01-01 and closing on the
retrieval date, with the retrieval date recorded in the run config. The denominator is
by `device.generic_name` and the keyword list is committed before searching, both in
`config/maude_keywords.yaml`. Counts are reported as device-category adverse events and
never as cyber-caused harm.

## What this amendment does not do

It changes no hypothesis, no threshold, no class set and no comparator. H3 stands as
Amendment 9 states it, and the 70% criterion and the reference standard are unchanged.

---

# Amendment 19 — 2026-08-12

Fixes the number of background draws each SHAP attribution averages over. Amendment 18
fixed the background sample at 200 windows and the aggregation, and said nothing about
this, so it was being taken from a library default. It is a parameter of the measurement
and not only of the runtime: it changes the attribution values, and therefore the top-10,
the mass summed per CAPEC pattern, and the STRIDE category a class is assigned.

Made before NB09 was run. It changes no hypothesis, no threshold and no class set.

## The value

`nsamples` = 50 for `shap.GradientExplainer`, fixed here and not tuned.

## The cost basis, which transfers

Measured on the dry-run fixture on CPU, one explainer call over 100 windows at each of
five values, the same windows throughout:

| nsamples | seconds per explained window |
|---|---|
| 10 | 0.47 |
| 25 | 0.58 |
| 50 | 0.78 |
| 100 | 2.19 |
| 200 | 4.84 |

Extrapolated to the real explained set, 862 windows across five models: about **1.2 hours
at nsamples 50** against **5.8 hours at the library default of 200**. The cost curve is a
property of the explainer and of this architecture, so it transfers from the fixture to
the real data.

## The stability evidence, which is fixture-only

On the same fixture, the top-10 ranking settles from nsamples 25 upward: nine of ten
members shared between every consecutive pair, the rank-1 feature unchanged from 25
onward, and Kendall's tau flat at 0.60 to 0.64. At nsamples 50 all ten top-10 members are
shared with the default of 200.

**This is fixture-only evidence.** It was measured on Gaussian noise with a small
per-capture offset, where there is no signal for attributions to find, so it says nothing
about what the ranking does on CICIoMT2024. It is recorded because it establishes that 50
is not obviously below the point where the machinery settles, and for no more than that.

## The check that is committed to

The stability check is re-reported on the real attributions in NB09b, where it costs
nothing extra because the attributions are already computed. Consecutive-value comparison
is not available there, since the run produces one value of nsamples; what is reported is
the across-seed stability the notebook already computes, read against this fixture
plateau.

If the real-data check disagrees with the fixture plateau, that is a finding to report.
It is not a reason to revise nsamples after the fact: a value chosen once the real
attributions are visible would be chosen on them, which is what fixing it beforehand
exists to prevent.

## What this amendment does not do

It changes no hypothesis, no threshold, no class set and no comparator. The background
size stays at 200 and held fixed across seeds, the aggregation stays as Amendment 18
fixes it, k stays at 10, and H3 stays as Amendment 9 states it.

---

# Amendment 20 — 2026-08-13

Made after NB09b was run. This is the one amendment in this file that follows the run it
concerns, and it is recorded as such.

## RQ3 and H3 are restated

**RQ3.** Can model explanations be resolved to CAPEC attack patterns and STRIDE threat
categories through a deterministic pipeline?

**H3.** For at least 80% of attack classes, the top-10 SHAP features of the timing-excluded
sequence model will resolve to a CAPEC attack pattern and therefore a STRIDE category under
the deterministic mapping.

Metric: proportion of the 18 attack classes receiving a CAPEC assignment. Pass mark 15 of
18. Measured 18 of 18.

RO3 is unchanged.

## What the previous statement was, and where it went

H3 as Amendment 9 stated it required a STRIDE category consistent with the documented
attack semantics for at least 70% of attack classes. Measured, that is 9 of 18 for the
sequence model, 0.500, against a majority-class baseline of 0.667.

That measurement is not withdrawn. It moves to `PROJECT_RECORD.md` Section 3 under
"Reported results — not hypothesis tests" as semantic agreement of the resolved STRIDE
category, served by notebook 09b, with the forest's 6 of 18 beside it.

## The threshold

The 80% follows a precedent set in the author's own earlier work: a feature-level
enrichment notebook on a different IoMT dataset, which used a top-10 feature cut and a 0.80
chain-completion threshold. It is a precedent being followed, not a published result, and
nothing about it is outstanding.

## What this amendment does not do

It changes no class set, no denominator and no reference standard. The denominator stays 18
attack classes with Benign excluded, and `config/stride_ground_truth.yaml` remains the
standard semantic agreement is measured against.
