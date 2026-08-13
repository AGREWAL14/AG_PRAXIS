# AG_PRAXIS — Notes for Writing

Append only. Corrections are appended as new entries, never edited in.

Material needed when the chapters are drafted that has no home in the existing governance
files. This is not a draft and holds no prose. Each entry states a claim, what the claim
rests on, and which chapter it serves.

`PROJECT_RECORD.md` remains the single source of truth for results. Nothing here is a
result, and no figure originates here. This file holds positioning and interpretation
only, and where an entry quotes a figure it names the artifact the figure comes from.

---

## Chapter 2 — citation gaps to close

### CICIoMT2024 design critique, Internet of Things (2025)

**Claim:** A 2025 paper in *Internet of Things* critiques CICIoMT2024's design choices and
argues for unweighted rather than weighted metrics on an imbalanced dataset. It partly
pre-empts this project's macro-averaging argument and its split-protocol argument, so it
has to be cited and positioned against rather than left out.

**Rests on:** Nothing in this repository. The DOI and full reference are not yet located.
To be located and verified against the primary source before use.

**Serves:** Chapter 2, related work, and the Chapter 3 justification for macro-averaging.

**Added:** 2026-08-10

### Device-disjoint splitting on CICIoMT2024, IJIES (2026)

**Claim:** A 2026 IJIES paper evaluates CICIoMT2024 under device-disjoint splitting,
framed around device-level data leakage inflating performance estimates.

**Rests on:** Nothing in this repository. The full reference is not yet located. To be
located and verified against the primary source before use.

**Serves:** Chapter 2, related work, and the Chapter 5 positioning of the split protocol.

**Added:** 2026-08-10

### Split governance and leakage auditing, Future Internet (2026)

**Claim:** A 2026 *Future Internet* paper makes split governance and leakage auditing the
research object rather than a methodological precaution. It works on CICIoT-DIAD, not
CICIoMT2024.

**Rests on:** Nothing in this repository. The full reference is not yet located. To be
located and verified against the primary source before use.

**Serves:** Chapter 2, related work, and the Chapter 5 positioning of the split protocol.

**Added:** 2026-08-10

### The early detection line, for NB08b's earliness framing

**Claim:** Three strands carry the earliness framing NB08b measures against. Djaidja et
al., IEEE TIFS 19:7783 (2024). A-THENA, arXiv:2604.21623 (2026). The early classification
of time series benchmark literature. A-THENA evaluates on CICIoT23-WEB, MQTT-IoT-IDS2020
and IoTID20 rather than CICIoMT2024, and argues that feature-based pipelines cannot detect
early.

**Rests on:** The two identifiers above, neither checked against its primary source. The
benchmark literature is not yet enumerated. All to be verified before use.

**Serves:** Chapter 2, related work, and the Chapter 4 reporting of NB08b under
`PREREGISTRATION.md` Amendment 15.

**Added:** 2026-08-10

### Goldschmidt and Chudá, arXiv:2502.06688, as the warrant for NB03b and NB07b

**Claim:** The survey names TTL among the features that cause spurious correlation and
inflate reported performance, which is the published warrant NB03b and NB07b are built on.
Its coverage is datasets published to 2023 inclusive and does not include CICIoMT2024, so
it supports the general claim about contaminating features and says nothing about this
dataset in particular. Any sentence that reads it as evidence about CICIoMT2024 overstates
it.

**Rests on:** The primary PDF, fetched and checked. Patrik Goldschmidt (Brno University of
Technology and the Kempelen Institute of Intelligent Technologies) and Daniela Chudá (the
Kempelen Institute of Intelligent Technologies and the Slovak University of Technology),
arXiv:2502.06688v3 [cs.CR], 22 May 2025, submitted to *Computers & Security* in April
2025. Cite as a preprint unless later publication is confirmed. It is a systematic review
of 89 public NIDS datasets across 13 properties, covering datasets published to 2023
inclusive.

The TTL sentence itself is not verified. It sits in Section 6, which the fetch did not
reach, so the state is: reference verified, specific claim not yet located to a section or
page. `PREREGISTRATION.md` Amendment 13 cites the work and `DECISIONS.md` under 2026-08-10
records the citation as unverified; this entry narrows that to the one outstanding
sentence.

**Serves:** Chapter 2, related work, and the Chapter 3 justification for NB03b and NB07b.

**Added:** 2026-08-10

---

## Chapter 4 — reporting

### Duration alone is above chance, not at chance

**Claim:** Duration alone identifies the source recording at 0.0299 against a chance rate
of 0.0200. That is above chance, not at chance. The defensible reading is that the column
carries a small amount of recording information on its own, well below anything usable,
and not that it carries none. Any sentence describing it as at chance overstates the
measurement.

**Rests on:** `RESULTS_LEDGER.md` under NB03b and
`data/processed/NB03b/duration_ablation.json`, run `duration_only`. Single run at seed 42,
no seed replicates.

**Serves:** Chapter 4, reporting of NB03b, and Chapter 5 where the provenance finding is
defended.

**Added:** 2026-08-10

---

## Chapter 5 — interpretation and positioning

### Conformal prediction and capture-disjoint evaluation are in tension by construction

**Claim:** Split-conformal coverage rests on exchangeability between the calibration
points and the test points. A capture-disjoint split breaks that exchangeability
deliberately, so the two are in tension by construction rather than by any property of the
implementation.

**Rests on:** `DECISIONS.md` under 2026-08-09, "Conformal prediction feasibility-tested
and dropped", and under 2026-08-10, "Conformal prediction and the capture-disjoint
split".

**Serves:** Chapter 5, and the scope exclusion in `PROJECT_RECORD.md` Section 3.

**Added:** 2026-08-10

### The split protocol is not the differentiator

**Claim:** The split-protocol contribution is being overtaken by the 2025 and 2026 work
recorded under Chapter 2 above. What remains this project's own is the measured mechanism
recorded in NB03 and NB03b: not that a capture-disjoint split should be used, but what the
features are doing that makes it necessary. Position the contribution accordingly.

**Rests on:** `PROJECT_RECORD.md` Section 5, feature provenance, and the three references
above, none of them yet verified.

**Serves:** Chapter 5, contribution and positioning.

**Added:** 2026-08-10

### NB03b strengthens rather than weakens the provenance finding

**Claim:** Capture identification with the attack class held fixed does not depend on the
TTL header field, and rises when it is removed: 0.8504 against 0.8280. So the provenance
finding cannot be dismissed as an artifact of one badly chosen column.

**Rests on:** `PROJECT_RECORD.md` Section 5 and `RESULTS_LEDGER.md` under NB03b, from
`data/processed/NB03b/duration_ablation.json`. Single runs at seed 42, no seed replicates.

**Serves:** Chapter 5, and the defence of the provenance finding in Chapter 4.

**Added:** 2026-08-10

### NB07b's warrant follows from that

**Claim:** The provenance signal sits in measured timing behaviour that also carries the
attack signal, so it cannot be removed by feature selection without losing what the model
is meant to detect. That is why the intervention in NB07b is at the level of the
representation rather than the feature set.

**Rests on:** `PROJECT_RECORD.md` Section 5, feature provenance, and `PREREGISTRATION.md`
Amendment 14.

**Serves:** Chapter 5, and the Chapter 3 justification for capture-invariant training.

**Added:** 2026-08-10

### Capture-invariant training, as future work rather than as a gap

**Claim:** Capture-invariant training is the indicated direction for the provenance
finding, and it is specified rather than speculative. `PREREGISTRATION.md` Amendments 14,
16 and 17 fix the intervention, the group variable, the counts of groups the objective
forms over training windows against the corpus, the derived chance rates for measuring
identifiability off a learned representation, and the fact that on 11 of the 45 groups
the group and the class are the same set of windows. The write-up can therefore say what
the next experiment is, in terms precise enough to run, rather than gesturing at one.

This entry supersedes "NB07b's warrant follows from that" above, which was written while
the notebook was still to be run and reads as though it will be.

**Rests on:** `PREREGISTRATION.md` Amendments 14, 16 and 17, and `DECISIONS.md` under
2026-08-11, which records why the notebook built on them was withdrawn.

**Serves:** Chapter 5, future work.

**Added:** 2026-08-11

---

## Chapter 4 — reporting

### The provenance finding, stated at its strongest

**Claim:** The shortcut cannot be removed by feature selection without removing the
signal. NB03 identifies the recording at 0.8280 with the attack class held fixed, so the
identification is not the model telling attacks apart. NB03b shows this does not depend
on the TTL header field: removing Duration raises it to 0.8504, and the timing family
without Duration still reaches 0.8935 against a chance rate of 0.0200. So the provenance
signal sits in measured timing behaviour that also carries the attack signal, and there
is no column whose removal separates the two.

**Rests on:** `PROJECT_RECORD.md` Section 5, feature provenance, which carries all four
figures and their sources.

**Serves:** Chapter 4, where the finding is reported, and Chapter 5, where it is defended.

**Added:** 2026-08-11

---

## Prose conventions — all chapters

### The chapters do not name notebooks

**Claim:** Chapter prose never refers to a notebook by number or by name. No "NB09", no
"notebook 9", no "the sequence model notebook". The writing describes what was tested and
what was found: a model trained on sequences of records rather than single ones, the
timing feature ablation, capture identification with the attack class held fixed.
Notebook numbering belongs to the governance files and the repository, not to the praxis.

**Rests on:** Nothing measured. It is a register rule, fixed here, and it holds for every
chapter rather than for one.

**Serves:** All chapters.

**Added:** 2026-08-11

---

## Chapter 4 — reporting

### The 70% threshold has no derivation

**Claim:** H3's 70% criterion is not derived from anything. `PREREGISTRATION.md` Amendment
7 records that it appears in no earlier amendment and is not a narrowing of any Amendment
3 clause; Amendment 2 carried a different STRIDE clause, a permutation test, which
Amendment 3 withdrew. What can be said about the number is that it clears the
majority-class baseline of 0.667 by one class out of eighteen. The write-up should report
the proportion, the baseline and the count of classes assigned together, so a reader can
see the margin rather than take the threshold as given.

**Rests on:** `PREREGISTRATION.md` Amendments 2, 3 and 7, and
`config/stride_ground_truth.yaml`, whose header carries the baseline and its arithmetic.

**Serves:** Chapter 4, reporting H3.

**Added:** 2026-08-12

### Reaching nothing and reaching the wrong category are different failures

**Claim:** `config/shap_capec_map.yaml` maps twenty of the forty features and refuses
twenty, so a class whose top-ranked features fall entirely among the refused ones reaches
no attack pattern and receives no category. That is a statement about how far the mapping
reaches, not about the detector being wrong, and the two must be counted separately. It is
also the outcome most likely to hold H3 below the pass mark, so a low proportion has to be
read against the assignment count before it is read as a failure of the explanations.

**Rests on:** `config/shap_capec_map.yaml`, which lists every refusal with its reason, and
the reporting in the threat-mapping notebook, which counts assignment and agreement
separately.

**Serves:** Chapter 4, reporting H3.

**Added:** 2026-08-12

### The CAPEC-to-STRIDE correspondence is a community artifact

**Claim:** the correspondence is Brett Crawley's, published on a personal blog in March
2022 and revised since. It is not a MITRE output and not a standards-body document, and no
official CAPEC-to-STRIDE mapping exists: CAPEC's own taxonomy mappings go to ATT&CK, WASC
and OWASP, not STRIDE. The provenance is stated wherever the mapping is described, not
only in the bibliography.

**Rests on:** `config/capec_stride.yaml`, whose header carries the provenance, the source
URL and the retrieval date.

**Serves:** Chapter 3, where the method is described, and Chapter 4, where its output is
reported.

**Added:** 2026-08-12

### Spoofing reaches its category through one weak link

**Claim:** Spoofing is the only class assigned to the Spoofing category, and the only
route to it runs through the ARP feature mapping to CAPEC-151 Identity Spoofing.
`config/shap_capec_map.yaml` records that entry as the weakest in the file, resting on a
functional link — ARP is the protocol by which a host asserts its link-layer identity —
rather than on a pattern named for the protocol. If that class is assigned correctly, the
result rests on that one link and the write-up should say so.

**Rests on:** `config/shap_capec_map.yaml` and `config/stride_ground_truth.yaml`.

**Serves:** Chapter 4, reporting H3.

**Added:** 2026-08-12

### MQTT-Malformed_Data is thin and is the only route to Tampering

**Claim:** MQTT-Malformed_Data rests on 40 test windows, which carries the caveat
`PREREGISTRATION.md` Amendment 4 fixes, and it is the only class the ground truth assigns
to Tampering. So the Tampering category stands or falls on a single thin class, and a
reader should not take a correct or incorrect assignment there as evidence about the
category.

**Rests on:** `config/stride_ground_truth.yaml` and `PREREGISTRATION.md` Amendment 4.

**Serves:** Chapter 4, reporting H3.

**Added:** 2026-08-12

---

## Chapter 5 — interpretation and positioning

### The MAUDE measurement cannot separate two explanations

**Claim:** a low count of adverse-event reports mentioning attack-related terms is equally
consistent with such events being rare and with MAUDE having no category in which to
record them. The second is the reading Section 2 of `PROJECT_RECORD.md` already advances,
citing Section 524B and the absence of a cybersecurity category in postmarket
surveillance. The measurement cannot distinguish them, and the write-up must not present a
low count as evidence for either.

**Rests on:** `config/maude_keywords.yaml`, which records this under
`absence_is_not_evidence_of_safety`, and `PROJECT_RECORD.md` Section 2.

**Serves:** Chapter 5, and Chapter 4 where the count is reported.

**Added:** 2026-08-12
