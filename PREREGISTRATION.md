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

