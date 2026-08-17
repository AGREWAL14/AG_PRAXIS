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

---

## Prose conventions — all chapters

### The governance apparatus is scaffolding and does not appear in the chapters

**Claim:** Chapter 3 describes the method as executed, as a coherent design, not the
amendment history that produced it. Chapter 4 reports results. Chapter 5 interprets. None
of these appears in any chapter: amendment numbers, notebook numbers, commit hashes,
config filenames, dry-run findings, run configs, artifact paths, hyperparameter names, or
the reasoning behind superseded decisions.

One exception. Chapter 3 may state in a sentence or two that design decisions were
recorded before execution, with a pointer to the repository. Not an enumeration.

Limitations reach the prose only where they change how a result should be read. The
entries already in this file are that set.

**Rests on:** Nothing measured. It is a scope rule, fixed here.

**Serves:** All chapters.

**Added:** 2026-08-13

---

## Chapter 4 — reporting

### The two models lose very differently when the timing columns are removed

**Claim:** removing the same four columns costs the two models very differently. The
random forest falls from macro-F1 0.8418 at 44 features to 0.5910 at 40, a fall of 0.2508.
The sequence model falls from 0.7138 to a five-seed mean of 0.6901, a fall of 0.0237. The
comparison is worth reporting in its own right.

It also bears on how the forest's role should be described. The forest is the exactness
check on the sequence model's approximate attributions, and at 40 features it is a
materially weaker model than at 44 — weaker, on its own numbers, than the model it is
checking. That does not disqualify it: TreeSHAP is exact whatever the model scores, and
the check is about the attribution method rather than about accuracy. But a reader told
only that the forest is the exact comparator should also be told what it scores.

**Rests on:** `RESULTS_LEDGER.md` under NB09a, and `PROJECT_RECORD.md` Section 5 under
timing-excluded models. The two figures are on different units, 1,229,711 records against
49,159 windows.

**Serves:** Chapter 4, reporting the timing-excluded models and H3.

**Added:** 2026-08-13

---

## Chapter 4 — reporting

### 18 of 18 is a result that could have failed

**Claim:** the mapping refuses twenty of the forty features. A class whose top-10
attributions landed entirely on refused features would have resolved to no CAPEC pattern
and no STRIDE category, and would have counted against H3. That every one of the eighteen
attack classes resolved is therefore a measurement and not an artifact of a table built to
cover everything. The write-up should state the refusal count alongside the result, because
without it the reader cannot tell the two apart.

**Rests on:** `config/shap_capec_map.yaml`, which lists twenty features under `no_entry`
with the reason for each, and `RESULTS_LEDGER.md` under NB09b.

**Serves:** Chapter 4, reporting H3.

**Added:** 2026-08-13

### Semantic agreement is the finding beyond prior work

**Claim:** resolving explanations to a CAPEC pattern is what the prior chain does.
Measuring whether the category it resolves to matches the attack semantics documented for
that class is not, and that is where the result is: 9 of 18, 0.500, against a
majority-class baseline of 0.667. A pipeline can complete for every class and still be
right about half of them.

The forest rules out the obvious explanation. Its TreeSHAP attributions are exact rather
than approximate, and it agrees less often, 6 of 18 against 9 of 18. So the disagreement is
not approximation error in the sequence model's attributions.

**Rests on:** `RESULTS_LEDGER.md` under NB09b, from
`data/processed/NB09b/threat_mapping.json`.

**Serves:** Chapter 4, reporting the semantic-agreement result, and Chapter 5, where the
contribution is positioned.

**Added:** 2026-08-13

### Correction: the 70% threshold entry above is superseded

**Claim:** the entry "The 70% threshold has no derivation" describes a hypothesis H3 no
longer states. `PREREGISTRATION.md` Amendment 20 restated H3 after NB09b ran: it now tests
CAPEC resolution at 80%, pass mark 15 of 18. The 0.667 majority-class baseline still
applies, but to semantic agreement, which is now a reported result rather than the
hypothesis test. What survives from that entry is the observation that a threshold should
be reported with its baseline and its assignment count, which holds for the new statement
as well.

**Rests on:** `PREREGISTRATION.md` Amendment 20 and `DECISIONS.md` under 2026-08-13.

**Serves:** Chapter 4, and reading the earlier entry in this file.

**Added:** 2026-08-13

---

## Chapter 2 — citation gaps to close

### The 80% threshold has no publication behind it

**Claim:** H3's 80% follows a precedent from the author's own earlier work, a feature-level
enrichment notebook on a different IoMT dataset that used a top-10 feature cut and a 0.80
chain-completion threshold. Chapter 2 has two honest options: state the threshold plainly
as a criterion chosen for this work, or describe it as following a chain-completion
criterion used in prior work on the same pipeline. It must not be cited as though a
published source exists, because none does, and no citation should be attached to it.

**Rests on:** `PREREGISTRATION.md` Amendment 20 and `DECISIONS.md` under 2026-08-13.

**Serves:** Chapter 2, and Chapter 3 where the criterion is stated.

**Added:** 2026-08-13

---

## Chapter 5 — interpretation and positioning

### Adaptive earliness, as specified future work

**Claim:** measuring earliness under a per-class confidence trigger is the indicated next
step for the observation work, and it is specified rather than speculative.
`PREREGISTRATION.md` Amendment 15 fixes the halting rule, the twelve-value tau grid with
its resolution concentrated in the upper tail, the metric of earliness against macro-F1,
and the averaging over correctly classified windows only. The notebook is written,
committed and passes its dry run. The write-up can say what the next experiment is in terms
precise enough to run.

**Rests on:** `PREREGISTRATION.md` Amendment 15, and `DECISIONS.md` under 2026-08-13, which
records why it was parked.

**Serves:** Chapter 5, future work.

**Added:** 2026-08-13

---

## Chapter 2 — citation gaps to close

### Graph-based work on this dataset builds similarity graphs, not topology

**Claim:** a published application of Graph Attention Networks and a hybrid GCN to
CICIoMT2024 exists, and it constructs edges from a 0.6 feature-similarity threshold, the
other stated criteria being unavailable in the released columns. The exclusion of graph
modelling is therefore a choice not to impose a similarity structure, not a claim that
graph methods cannot be applied to this dataset. Any sentence saying no graph can be
built on this dataset overstates the position and is refuted by a citable paper.

**Rests on:** the Chethan et al. PDF, Section II.C and equation (1), read and verified.
Chethan, G. S., Patil, N. S., Prakash, G. L., and Muneshwara, M. S. (2026). Adaptive
graph-based intrusion detection for Internet of Medical Things (IoMT) networks.
*Engineering, Technology & Applied Science Research*, 16(3), 36934-36941. DOI
10.48084/etasr.17590.

**Serves:** Chapter 2, related work, and the Chapter 3 scope exclusion.

**Added:** 2026-08-14

### arXiv 2201.11628 as the named prior work for earliness

**Claim:** per-class earliness and minimum-number-of-packets is an established
measurement on CICIDS-2017, reported in arXiv 2201.11628, "Early Detection of Network
Attacks Using Deep Learning". This project adapts it to CICIoMT2024, where no per-class
earliness study exists. The contribution wording is "first per-class observation-budget
analysis on this dataset", not "first observation budgets".

**Rests on:** arXiv 2201.11628, not yet verified against the primary source.

**Serves:** Chapter 2, related work, and the Chapter 4 positioning of the
observation-budget result.

**Added:** 2026-08-14

---

## Chapter 5 — interpretation and positioning

### Saturation is not a detection ceiling

**Claim:** saturation marks where a class stops improving with more observation, not
where it becomes reliably detectable. Eight of nineteen classes saturate at an F1 below
0.80. The phrase "detection ceiling" appears in the thesis statement in
`PROJECT_RECORD.md` Section 1 and in the RO2 row of Section 3, and it does not describe
the quantity that was measured. The wording is to be resolved when the title and thesis
statement are settled, and is recorded here rather than changed, since both are deferred
to that pass. The low-rate median of 25 against a volumetric 15 is also a property of the
{5, 10, 25, 50} grid as much as of the classes, since a median can take only one of those
four values or a midpoint between two, so report the direction and not the ratio.

**Rests on:** `PROJECT_RECORD.md` Section 3 and Section 5.

**Serves:** Chapter 4, reporting the observation budgets, and Chapter 5, where the result
is interpreted.

**Added:** 2026-08-14

---

## Chapter 5 — interpretation and positioning

### The provenance finding has an external counterpart

**Claim:** two 2026 papers publish random forest feature importance on this dataset and
rank the same timing features highest. Gencturk et al. place IAT first by a wide margin
with Rate and Srate next; Alkhodaidi et al. give IAT 0.21 and Rate 0.05 and advise
security teams to monitor IAT and packet rate. Both interpret the ranking as attack
signal. This project measures those same columns identifying the source recording.

The correspondence is exact on three features. IAT, Rate and Srate identify the source
recording at 0.8935 on the fifty-way task against a chance rate of 0.0200, and those same
three are the top three of Gencturk et al.'s random forest importance ranking. The same
three features, read as attack signal there and measured as recording provenance here. On
first rank the two also agree, by a different measurement: IAT is Gencturk et al.'s
highest-ranked feature by a wide margin, and it is this project's top feature by mutual
information on the 19-class task at 2.1500 nats of 2.1940 available. The 0.8935 figure
itself treats the three as a set and does not rank them, so what corresponds there is
membership rather than order.

Two further figures place that. The timing family, those three plus Duration, reaches
0.9301 on the same fifty-way task, and capture identification with the attack class held
fixed reaches 0.8280 across all 44 features against a mean chance rate of 0.1750.

The gap is not that the literature is wrong about their predictive value. It is that no
published work distinguishes the two contributions, so a feature can be top-ranked for
detection and carrying recording provenance at the same time and nothing in the published
record separates them. This is the strongest available positioning for the provenance
finding, and it replaces any framing that argues the point in the abstract: the argument
is now against two named rankings rather than against a hypothetical practitioner.

**Rests on:** the Gencturk et al. and Alkhodaidi et al. PDFs, read and verified, and
`PROJECT_RECORD.md` Section 5, under feature provenance for the three identification
figures and under feature separability for the mutual information figure.

**Serves:** Chapter 5, where the provenance finding is positioned, and Chapter 2, related
work.

**Added:** 2026-08-14

### The balancing negative result is consistent with independent work

**Claim:** Gencturk et al. conclude across ECU-IoHT, WUSTL and CICIoMT2024 that
balancing's benefit is not universal and in several multi-class settings is limited or
inferior to the unbalanced baseline. Alkhodaidi et al. report a deep model falling from
98.61% to 73.25% accuracy on the 19-class task under ADASYN. This project's finding is
therefore consistent with published work rather than an artifact of the intervention set
chosen here: two of five interventions lowered macro-F1 against the parent, and no
intervention raised the count of classes detected at F1 0.50.

**Rests on:** both PDFs, read and verified, and `PROJECT_RECORD.md` Section 5 under class
balancing.

**Serves:** Chapter 5, interpreting the balancing result, and Chapter 4 where it is
reported.

**Added:** 2026-08-14

### Aggregate and class-sensitive metrics diverge, published on this dataset

**Claim:** Gencturk et al.'s Table 19 reports a model with aggregate F1 0.4676 and zero
recall on the smallest class, and two deep models recovering that class better than a
random forest while scoring far worse overall. They state that aggregate and
class-sensitive metrics can tell different stories for the same model. That is this
project's weighted-minus-macro argument reached independently on the same dataset, so it
can be cited rather than argued from first principles.

**Rests on:** the Gencturk et al. PDF, read and verified.

**Serves:** Chapter 4, reporting the macro against weighted gap, and Chapter 3 where
macro-averaging is justified.

**Added:** 2026-08-14

### The hard-class diagnostic is measured on a different unit

**Claim:** Gencturk et al. use Recon-Ping_Sweep as their headline minority-class
diagnostic and interpret its recall. This project reports the class without interpreting
it, because at window 50 and stride 25 its 926 records yield 4 test sequences. Their unit
is records and this project's is windows, so the exclusion does not transfer and they are
not in error on their own terms. Any citation of their figures must state the difference
in unit, or a reader will ask why the same class is interpreted there and not here.

**Rests on:** the Gencturk et al. PDF, and `PREREGISTRATION.md` Amendment 4.

**Serves:** Chapter 2, related work, and Chapter 4 where the class is reported without
being interpreted.

**Added:** 2026-08-14

---

## Chapter 2 — citation gaps to close

### No published work on this benchmark states its averaging method

**Claim:** four papers now checked against their PDFs report F1 on the 19-class task
without stating whether it is macro, micro or weighted — the benchmark paper itself,
Dadkhah et al. (2024), and three applications of it, Chethan et al. (2026), Gencturk et
al. (2026) and Alkhodaidi et al. (2026). This is a property of how the benchmark is
reported in the literature rather than four separate omissions, and it makes stating the
averaging method a methodological position rather than housekeeping. Alkhodaidi et al.
report a random forest at 99.53% accuracy and 0.9951 F1 on the task where this project's
macro figure is 0.8418. A difference of that size is consistent with weighted averaging on
a corpus imbalanced at 2,157.7 : 1, but it cannot be established without their code and
must not be asserted.

**Rests on:** the four PDFs, and `DECISIONS.md` under 2026-08-07, which records that
"macro", "micro" and "weighted" appear nowhere in Dadkhah et al.'s 22 pages.

**Serves:** Chapter 2, related work, and Chapter 3 where the metric is fixed.

**Added:** 2026-08-14

### Correction: the 2025 Internet of Things design critique is Doménech et al.

**Claim:** the entry "CICIoMT2024 design critique, *Internet of Things* (2025)" above
records that the DOI and full reference are not yet located. The reference is Doménech,
J., León, O., Siddiqui, M. S., and Pegueroles, J. (2025). Evaluating and enhancing
intrusion detection systems in IoMT: The importance of domain-specific datasets.
*Internet of Things*, 32, Article 101631. DOI 10.1016/j.iot.2025.101631. The rest of that
entry stands as written. The PDF has not been read, so the work remains on the pending
list in `PROJECT_RECORD.md` Section 11 and none of its claims may enter a chapter.

Two claims are attributed to it by secondary sources and are recorded here as unverified
rather than as findings: that it recommends shuffling to address temporal correlation, and
that it reports F1 drops of up to 66.87% on transfer between CICIoT2023 and CICIoMT2024.
Both need the primary source before use. The second bears on the cross-dataset scope
exclusion in `PROJECT_RECORD.md` Section 3, which rests on this project's own transfer
measurement and does not depend on it.

**Rests on:** the located reference above. Nothing read.

**Serves:** Chapter 2, related work, and reading the earlier entry in this file.

**Added:** 2026-08-14

---

## Chapter 2 — citation gaps to close

### All seven pending citations are read; the gaps close

**Claim:** every reference this section recorded as unlocated or unread was read against
its primary source on 2026-08-15, so nothing in this section now blocks a chapter. The
entries above stand as the claim each reference supports, narrowed or corrected by the
entries below where the reading changed something. Two references change form and the
earlier citations are superseded: the early-detection work is Ahmad, T., Truscan, D.,
Vain, J., and Porres, I. (2022), "Early detection of network attacks using deep learning",
2022 IEEE ICSTW, 30-39, DOI 10.1109/icstw55395.2022.00020, cited in place of arXiv
2201.11628; and Goldschmidt and Chudá is published as *Computers & Security* 156:104510,
DOI 10.1016/j.cose.2025.104510, so the instruction to cite it as a preprint is discharged.
The IJIES device-disjoint paper, unlocated until now, is Abo-Haat, M., and Zuhair, H.
(2026), "Advanced multi-protocols framework for cyber attacks detection in IoMT",
*International Journal of Intelligent Engineering and Systems* 19(3), 338-359, DOI
10.22266/ijies2026.0331.21. The split-governance paper is Chikezie, C. I., Usman, A. U.,
David, M., Zubair, S., Ohize, H. O., and Ojeniyi, J. (2026), *Future Internet* 18(6), 287,
DOI 10.3390/fi18060287, and its recorded claim holds as written: preprocessing is the
research object rather than a precaution, the authors disclaim any downstream classifier
superiority, and the corpus is CICIoT-DIAD 2024 at 35,672,407 flows across 180 files,
not CICIoMT2024.

**Rests on:** the seven PDFs, and `DECISIONS.md` under 2026-08-15.

**Serves:** Chapter 2, and every chapter citing any of the seven.

**Added:** 2026-08-15

### Shuffling is a published position against this project's split protocol

**Claim:** Doménech et al. (2025) recommend, in their Section 5.1.3, that shuffling be
explicitly documented and performed for all models to reduce bias from temporal
correlation, and note it is unclear whether CICIoMT2024's authors did so, though the
published scripts suggest it was applied to neural network training. That is a conflict
with this project and not support for it. Shuffling dissolves capture structure, and
holding capture structure intact is exactly what the split protocol here is built to do.
Both positions treat temporal correlation as the problem and draw opposite conclusions
about what to do with it: shuffle so that no partition is defined by when it was recorded,
or partition by recording so that nothing learned about a session can be scored on that
same session. The disagreement is stated plainly and the paper is cited as a contrasting
published position, not paraphrased into agreement.

**Rests on:** the Doménech et al. PDF, Section 5.1.3, read and verified.

**Serves:** Chapter 2, related work, and Chapter 5 where the split protocol is
positioned.

**Added:** 2026-08-15

### The 66.87% figure has to be stated exactly

**Claim:** the transfer figure attributed to Doménech et al. is a relative reduction in
macro F1, not a percentage-point drop and not an F1 value. Their random forest falls from
0.9429 to 0.2742 in the five-class generalisation setting of their Experiments 2 and 3,
training on CICIoT2023 and testing on CICIoMT2024, which is the 66.87%. Their comparable
reductions are 58.03% for the decision tree, 65.14% for XGBoost and 44.73% for the
feedforward network. Written as "an F1 drop of 66.87%" it will be read as points and is
wrong. It also does not bear on this project's cross-dataset scope exclusion, which rests
on this project's own transfer measurement.

**Rests on:** the Doménech et al. PDF, Experiments 2 and 3, read and verified, and
`PROJECT_RECORD.md` Section 3 for the exclusion.

**Serves:** Chapter 2, related work.

**Added:** 2026-08-15

### The published baseline is not one number

**Claim:** at least two mutually inconsistent figures for Dadkhah et al.'s nineteen-class
baseline now circulate in the literature. F1 0.551, read from their own Table 7 and
reproduced by Chethan et al., against Doménech et al.'s Table 8, which attributes to them
accuracy 0.7350, precision 0.7130, recall 0.7350 and F1 0.6760. Both are presented as the
same baseline. This strengthens the position already taken, that the published figure
reflects how the evaluation was carried out rather than what the model can do: a quantity
that is not stable across the papers reporting it is not a fixed anchor to be beaten.
Doménech et al.'s own system reaches 0.9985 accuracy and 0.9700 F1 under random splits
with shuffling and balancing, and that number must not be set against anything from this
project, which holds recording sessions apart.

**Rests on:** the Doménech et al. PDF Table 8, `DECISIONS.md` under 2026-08-07 and
2026-08-14, and `PROJECT_RECORD.md` Section 6.

**Serves:** Chapter 2, related work, and Chapter 4 where the baseline is reported.

**Added:** 2026-08-15

### Independent published support for macro-averaging

**Claim:** Doménech et al.'s Section 2.2 criticises the foundation model this project
reproduces, which they cite as Mohamadi et al. with one m, for using weighted averaging on
an imbalanced dataset, and argues for an unweighted mean. The macro-averaging choice here
was made on this project's own reasoning about the class distribution, so this is not what
the decision rests on; it is a published source arguing the same thing about the same
paper, which is worth citing where the choice is justified rather than leaving the
justification entirely internal.

**Rests on:** the Doménech et al. PDF, Section 2.2, and `DECISIONS.md` under 2026-08-01.

**Serves:** Chapter 2, and Chapter 3 where macro-averaging is justified.

**Added:** 2026-08-15

### The device-disjoint paper is citable for its design position only

**Claim:** Abo-Haat and Zuhair (2026) raise device-level leakage on this dataset, which is
worth citing, but their device labels are predicted rather than observed. Their Section
3.3.2 records that the dataset carries device identity only for Wi-Fi benign profiling
traffic, seven devices; they train an XGBoost device classifier on that and predict device
labels for all attack traffic, and their two MQTT "devices" are confidence buckets of that
classifier, High at 35 to 70% and Low below 35%, arranged so that one could go to train
and one to test. Zero device overlap is therefore disjointness of a predicted label. Cite
them as prior work raising the question, never as an established device-disjoint result.
No figure from the paper may be quoted: its sample totals read 2,767,675, 2,767,650 and
2,899,704 in different places against Table 1's 1,189,828, its combined accuracy reads
98.61% in Table 5 and 99.51% in Appendix C, and its feature count moves between 45, 45+1,
45+17 and 46.

What is usable is their independent list, in the same section, of what the released CSVs
lack: timestamps, source and destination IP addresses, ports, MAC addresses or device
identifiers, and flow identifiers. That supports the split rationale from a second source,
with Doménech et al.'s Table A.9 as a third.

**Rests on:** the Abo-Haat and Zuhair PDF, read and verified.

**Serves:** Chapter 2, related work, and Chapter 3 where the split is justified.

**Added:** 2026-08-15

### The earliness prior work, narrowed

**Claim:** Ahmad et al. (2022) report earliness and a minimum number of packets per class
in their Table VI, so per-class earliness as established prior work stands and the
contribution wording "first per-class observation-budget analysis on this dataset"
survives. Two narrowings must travel with the citation. Their study covers four classes
from one day's web-attack subset of CICIDS2017 — Normal, Brute Force, XSS and SQL
Injection — and not the whole corpus. And their minimum number of packets counts packets
within a flow and is computed only over correctly classified flows, so measuring records
to a threshold over fixed windows is an adaptation of the idea rather than the same
measurement. Describe it as adapted, not as applied.

Djaidja et al. (2024) report initial packets required for correct classification per
attack class on CIC-IDS2017 and 5G-NIDD, built from raw pcap through their own flow
segmentation. They claim to be first to address early detection in this setting; Ahmad et
al. predates them and defines the metric. The field carries at least two independent
priority claims, so repeat neither.

**Rests on:** both PDFs, read and verified.

**Serves:** Chapter 2, related work, and Chapter 4 where the observation budgets are
reported.

**Added:** 2026-08-15

### TTL as shortcut feature, and the paper that uses it

**Claim:** the outstanding sentence in Goldschmidt and Chudá is located, in Section 6.3
under the shortcut-learning heading. TTL is named alongside IP addresses, port numbers,
timestamps and flow identifiers as features that can contaminate data-driven learning: if
used for training, a learner may spuriously correlate the artifact with an activity,
producing shortcut learning and overestimated performance. Their supporting evidence is
D'Hooge et al., reaching 70 to 100% accuracy on popular network intrusion datasets from
destination port alone. The caveat already recorded stands: their coverage is datasets
published to 2023 inclusive, so it does not cover CICIoMT2024 and says nothing about this
dataset in particular.

Djaidja et al.'s per-packet feature vector includes TTL, min-max normalised. A published
warrant naming TTL as a contaminating feature and a published early-detection model
feeding TTL to a network are two positions in the same literature. Where both appear in
one passage the tension is shown rather than smoothed over, and it is the reason this
project measures what its own TTL column contributes instead of arguing the point from
either citation.

**Rests on:** the Goldschmidt and Chudá PDF, Section 6.3, and the Djaidja et al. PDF, both
read and verified. `PROJECT_RECORD.md` Section 5 carries the measurement.

**Serves:** Chapter 2, related work, and Chapter 3 where the timing ablation is
justified.

**Added:** 2026-08-15

---

## Chapter 5 — interpretation and positioning

### Statistical-aggregate features are a live limitation, not only a citation

**Claim:** A-THENA's Table 8 shows nearly all feature-based baselines requiring the full
30-packet flow, because session-level statistics cannot be computed from a prefix. The
target of that argument is CICFlowMeter-style statistical aggregates, and CICIoMT2024's
released columns are exactly that kind of feature. So the limitation applies to the
sequence work here rather than sitting safely in related work: every record this project
reads is already a summary over a window of packets, and an observation budget is a budget
of summaries, not of packets. The earlier recording of their claim as "feature-based
pipelines cannot detect early" is too absolute in two ways. It concerns statistical
aggregates rather than feature-based pipelines generally, and their own table has Naive
Bayes at an earliness of 1. Their corpora are CICIoT23-WEB, MQTT-IoT-IDS2020 and IoTID20,
not CICIoMT2024.

**Rests on:** the A-THENA PDF, Table 8, read and verified.

**Serves:** Chapter 5, where the observation-budget result is interpreted, and Chapter 2,
related work.

**Added:** 2026-08-15

### The extraction window differs between the two groups being compared

**Claim:** the dataset's features were extracted over 100-packet windows for DDoS and DoS
traffic and 10-packet windows for everything else, recorded by Doménech et al. in their
Section 5.1.1, who argue it alters the feature distribution across classes and recommend a
uniform window. That boundary falls exactly on the boundary between the volumetric and
low-rate groups this project compares: the volumetric group is the eight DDoS and DoS
classes and the low-rate group is drawn from the remainder. A record on one side of the
comparison therefore summarises ten times the packets a record on the other side does, so
an observation budget counted in records or windows is counted in units of different size
between the groups. The direction the observation result reports is unaffected in
statement, but what a record means is not constant across it, and the write-up must say so
wherever the two medians are read against each other. This is a property of the dataset,
not of the measurement, and neither the groups nor any figure was changed on learning it —
the groups were fixed by the benchmark taxonomy before anything was measured.

**Rests on:** the Doménech et al. PDF, Section 5.1.1, and `PROJECT_RECORD.md` Section 4,
which now records the windows, and Section 3 for the group definitions.

**Serves:** Chapter 5, interpreting the observation result, Chapter 4 where the medians
are reported, and Chapter 3 where the dataset is described.

**Added:** 2026-08-15

### The TTL reading is documented, not only inferred

**Claim:** Doménech et al.'s Appendix Table A.9 maps the attributes of CICIoT2023 and
CICIoMT2024 and gives the description of the CICIoMT2024 Duration feature as TTL outright.
This project reached the same reading from the CICIoT2023 feature table and from the
values themselves, a full scan putting the global maximum at exactly 255 with 93.57% of
values at the default 64. The write-up can therefore state the identification as a
documented property of the feature and offer the distribution as confirmation, rather than
carrying the whole claim on inference.

**Rests on:** the Doménech et al. PDF, Appendix Table A.9, `PROJECT_RECORD.md` Section 5,
and `config/feature_families.yaml` under `table5_reconciliation`.

**Serves:** Chapter 3 and Chapter 4, where the timing ablation and the provenance finding
are reported.

**Added:** 2026-08-15

---

## Chapter 5 — interpretation and positioning

### The volumetric cost is a confusion within a family, not a failure to detect

**Claim:** the aggregate figure for the sequence model conceals what its losses on the
flooding classes actually are. They are not traffic the model failed to find. Of the
windows of one ICMP flooding class, three quarters are given the label of the other ICMP
flooding class and almost nothing goes anywhere else, and the confusion runs in both
directions, so both classes fall together. The same holds for the TCP and SYN pairs and
not for the UDP pair, whose two members are undamaged. A reader told only that a class
fell from F1 0.9960 to 0.3178 will take it as a detection failure, and it is not one:
every one of these classes is separated from the rest of the corpus and confused with its
own partner.

Two readings are ruled out by measurement rather than by argument. It is not a seed
artifact, since the fall reproduces across five seeds. And it is not aggregation
destroying the distinction: scoring every feature on how well it separates the two members
of a pair, first on single records and then on the average of the fifty records in a
window, the average separates these pairs better than a single record does, in all four
pairs. Whatever costs the model the distinction, it is not that averaging threw the
distinction away.

What is left is the part that connects to the rest of this work. In every one of the four
pairs the separation on the averaged window is carried by one feature, at a near-identical
figure across pairs, and it separates the two members by their level rather than by how
much the feature moves within a window. That is the same feature this project measures as
identifying which recording session a row came from. So the distinction that survives
aggregation is one that the provenance measurement says should not be trusted, and once
the provenance-carrying timing features are set aside there is very little left in these
columns that tells the two members of a pair apart. This is one line of the central
argument rather than a separate observation: the same measurement that makes the split
protocol necessary also explains why a within-family distinction is hard to make honestly
on this data.

The reading of that one feature as a session marker is consistent with what was measured
and is not a test of it. What was measured is that a single feature separates all four
pairs at nearly the same figure and does so on level rather than on variation, which is
what a per-session offset would look like. No experiment here distinguishes that from an
attack property that happens to behave the same way, and the write-up should say so.

**Rests on:** `PROJECT_RECORD.md` Section 5 under the sequence model and under feature
provenance, and Section 11 under the DoS-ICMP row, and `RESULTS_LEDGER.md` under NB06d.

**Serves:** Chapter 5, where the sequence result is interpreted and the provenance finding
is positioned, and Chapter 4, where the per-class figures are reported.

**Added:** 2026-08-15

---

## Chapter 1 — problem statement

### 1.3 Problem statement — approved wording, 2026-08-16

Hospitals now run thousands of connected medical devices — infusion pumps, patient
monitors, imaging systems — on the same networks that carry clinical data. These
devices are hard to patch, run for years, and are attractive targets. Intrusion
detection systems are the practical defense, and machine learning models are
increasingly used to build them.

Two problems limit these systems today. First, detection models are usually trained
on single network records, one at a time. This works well for loud attacks such as
denial of service, which change traffic volume immediately, but it works poorly for
quiet attacks such as scanning and reconnaissance, which look like ordinary traffic
in any single record. On the CICIoMT2024 benchmark, the published detection model
scores below an F1 of 0.50 on five of the nineteen classes. Reconnaissance is the
stage where an attacker is still looking around, before any damage is done, so these
are the classes a defender most wants to catch. Reading records in sequence is the
obvious remedy, but whether it helps, which classes it helps, and what it costs on
the classes that were already detected are open questions.

Second, detection models report an attack class but not what the attack means. A
security team is told that traffic is "Recon-OS_Scan" and is left to decide on its
own what kind of threat that is and what to do about it. Threat modeling frameworks
such as CAPEC and STRIDE exist to answer that question, but they are normally built
by hand at design time, from assumptions about how a system might be attacked, rather
than from traffic that was actually observed, and no automated route runs from a
detector's output to a structured threat record.

**Wording notes.** "Scores below an F1 of 0.50 on five of nineteen" rather than "fails
to detect five of nineteen": three of the five are non-zero, and 0.50 is the threshold
fixed in Amendment 5. The five-class count is a measurement of this work, not a figure
Dadkhah et al. state — phrase it as a finding of this research, not as a cited claim.
The closing clause of paragraph two states a gap in method, which this work fills; an
earlier draft said "nothing converts an observed attack into a structured threat
record," which claims more than the semantic-agreement result of 9 of 18 supports. The
device framing over Wi-Fi, Bluetooth and home networks was removed: CICIoMT2024 as
modelled here is Wi-Fi and MQTT only, and that framing sets up a scope Chapter 1.8
then has to walk back.

---

## Chapter 4 — reporting

### Caveats that must travel with the H1 claim

**Claim:** three things travel with the four-of-five result wherever it appears.

Two of the four recovered classes rest on very few test sequences: Recon-VulScan on 18
and MQTT-Malformed_Data on 40. The caveat appears wherever the four-of-five result
appears.

The cost side is not one class. Nine classes gained F1 and ten lost. Gains sum to
+2.0566, losses to -2.0033, a net of +0.0533 over nineteen classes, which is the
+0.0028 macro-F1 difference. The five largest losses are all volumetric — DoS-ICMP,
DoS-TCP, DDoS-ICMP, DoS-SYN, DDoS-TCP — summing -1.7662, which is 88% of the total
negative movement. DoS-ICMP alone falls 0.9960 to 0.3178. The honest headline for RQ1
is that sequence context trades volumetric precision for reconnaissance coverage,
which is why the aggregate metric shows nothing.

Recon-VulScan reaches 0.5385 from 0.0000 and is one of the four classes that cross the
threshold. The class not recovered is MQTT-DDoS-Publish_Flood, 0.1858 to 0.0796. The
two are not interchangeable and no chapter text should pair them as jointly undetected.

**Rests on:** `PROJECT_RECORD.md` Section 5 under the sequence model, which carries the
per-class table, the gain and loss sums and the volumetric share, and
`PREREGISTRATION.md` Amendment 4 for the thin-class caveat.

**Serves:** Chapter 4, where H1 is reported, and Chapter 5, where the trade is
interpreted.

**Added:** 2026-08-16

### Caveat that must travel with the H3 claim

**Claim:** H3 passes on assignment: 18 of 18 classes resolve to a CAPEC pattern against
a pass mark of 15. Semantic agreement is a separate count and is reported alongside
every time: 9 of 18 for the sequence model, 0.500, against a majority-class baseline of
0.667; 6 of 18 for the forest. The threat records are produced reliably in form and are
no better than the majority guess in substance. Assignment and agreement are never
merged into one figure.

**Rests on:** `PROJECT_RECORD.md` Section 3, which carries both counts and the baseline,
and `data/processed/NB09b/threat_mapping.json`, from which both were read.
`PREREGISTRATION.md` Amendment 20 fixes H3 as chain resolution and the pass mark at 15
of 18.

**Serves:** Chapter 4, where H3 is reported.

**Added:** 2026-08-16
