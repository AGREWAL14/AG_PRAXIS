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


