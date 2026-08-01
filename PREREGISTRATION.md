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
