# God Brain DriftGuard R11 Source-Admission Delta V0.1

Status: **RESEARCH SOURCE-ADMISSION DELTA / NO RUNTIME COUPLING / NO CANONICAL EFFECT**

Parent God Brain research assessment:
`research/god-brain-driftguard-source-admission-v0-1-20260920@68e7ba2320e7aa17fe291f7325f22ca96fc84fcc`

Observed DriftGuard canonical main:
`9894692ff6b549e4378bcc2b8ca46813ff18bf37`

Exact new source subject:
- repository: `thebrazenbeard/driftguard`
- Draft PR: #34
- base: `9df4800d81ab2e937ffa97263b8095305a845661`
- exact head: `351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f`
- source path: `docs/R11_GOVERNED_BENCHMARK_HOLDOUT_V1.md`
- source blob: `11e7a18ff01669656fd0b471b9b5d9fa2c37304a`

## Why this delta exists

The prior God Brain DriftGuard admission package already covers:
- R10 frozen-candidate comparison and no same-holdout promotion;
- PR #31 atomic currentness snapshot as a bounded source mechanism;
- PR #32 effect-fence / reconcile-before-retry design.

R11 adds a different governance layer: the **history and single-use semantics of the experiment itself**.

The useful transfer is not “use DriftGuard’s benchmark.” It is the protocol pattern for preventing hidden retries, discarded attempts, repeated reveal/run, and untracked predecessor holdouts from being mistaken for clean confirmatory evidence.

`DRIFTGUARD_SOURCE != GOD_BRAIN_RUNTIME_DEPENDENCY`

`BENCHMARK_PROTOCOL_PASS != SCIENTIFIC_VALIDATION`

`DETECTOR_ALARM != CONTACT`

`SEPARATE_CHAT != INDEPENDENT_CORROBORATION`

## Fresh review state

At exact head `351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f` the DriftGuard PR reports 279/279 tests passing on Ubuntu and Windows plus compile/diff/smoke checks.

Fresh review readback still shows BT2 self-hostile `PASS_WITH_CLAIM_CEILING` on this head.

That is **not independent corroboration**.

A Vera hostile exact-head rereview later examined this same head. Vera explicitly states that the review is **not independent corroboration** because that lane has prior exposure to the R11 design/review history. Its corrected final disposition on exact head `351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f` is `CHANGES_REQUIRED` (review `PRR_kwDOUh0Fi88AAAABOiir_A`), superseding an earlier same-head PASS.

The blocker is specific: after `begin_execution()`, the governed run path catches every `Exception` and routes it through semantic-failure invalidation. Unexpected runtime/infrastructure failures such as SQLite/OSError/unexpected RuntimeError can therefore terminalize `EXECUTING -> INVALIDATED` and reopen successor eligibility even though execution outcome is ambiguous.

Therefore the source disposition here is:

`RESEARCH_ONLY_BLOCKED_BY_HOSTILE_EXACT_HEAD_REVIEW`

The independent-review state remains `NOT_OBSERVED`; the hostile Vera review does not become independent merely because it is exact-head. A repaired DriftGuard source must move to a new exact head, and God Brain must re-bind both source identity and review evidence before any admission upgrade.

## Candidate transferable mechanisms

### 1. Durable attempt ancestry

R11 keeps terminal attempts in durable history and requires a successor to reference prior terminal attempt receipt digests.

God Brain candidate rule:

`FAILED_OR_ABORTED_ATTEMPT != DISAPPEARED_ATTEMPT`

For confirmatory research, a failed or abandoned attempt is part of the study ancestry, not optional narrative.

### 2. Prior-holdout disclosure

A successor attempt must disclose prior attempt HOLDOUT digests, and the new HOLDOUT must differ from disclosed predecessor holdouts.

God Brain candidate rule:

`DECLARED_HOLDOUT_NONREUSE != COMPLETE_HISTORICAL_NONACCESS_PROOF`

This is useful only with its ceiling intact: the mechanism cannot discover hidden prior holdouts or prove that nobody accessed the holdout before commitment.

### 3. Single-use reveal

R11 binds reveal to durable SEALED state, exact corpus/manifests/artifact bytes, and consumes:

`SEALED -> REVEALED`

God Brain candidate rule:

`REVEAL_IS_A_CONSUMING_TRANSITION`

A reveal receipt is evidence of exact committed-data equality under the protocol, not evidence of trusted time or prior non-access.

### 4. Single-use execution claim

Immediately before governed comparison, R11 consumes:

`REVEALED -> EXECUTING`

Replay/concurrent execution cannot legitimately reuse the already-consumed execution claim.

God Brain candidate rule:

`EXECUTION_CLAIM_IS_SINGLE_USE_BEFORE_ANALYSIS`

This is stronger than “log that a test ran.” The authority to perform the governed confirmatory analysis is consumed before the analysis path.

### 5. Ambiguity does not restore retry authority

The most important repaired R11 rule is that an ambiguous post-claim completion/storage state stays `EXECUTING` rather than becoming operator-abortable or retryable.

God Brain candidate rule:

`AMBIGUOUS_CONFIRMATORY_EXECUTION != SAFE_TO_RETRY`

An operator reason string must not erase uncertainty after the single-use execution claim has already been consumed.

A later recovery path, if needed, must be separately typed and evidence-bound.

### 6. Execution-closure binding

R11 binds the DriftGuard-local source closure used by the governed benchmark:
- `benchmark.py`
- `calibration.py`
- `comparison.py`
- `sequential.py`
- `model.py`

and rechecks those hashes at seal, reveal, and run.

God Brain candidate rule:

`PARAMETER_PRECOMMIT != EXECUTION_IMPLEMENTATION_PRECOMMIT`

A confirmatory protocol should bind the actual execution subject needed for the claim, not merely parameters or a top-level script.

R11 itself correctly limits this: declared Git provenance is not independently authenticated; interpreter/stdlib identity and hostile in-memory mutation are outside the claim.

### 7. Receipt rebinding

R11 does not treat a factory-originated receipt as universally valid. Reveal/run transitions re-bind receipts to exact study, attempt, precommit, execution binding, holdout subject, and downstream plan identities.

God Brain candidate rule:

`VALID_RECEIPT != VALID_FOR_THIS_SUBJECT`

Receipts should be admitted only after exact-subject rebinding at the transition that consumes them.

## God Brain disposition

Candidate admission class:

`RESEARCH_ONLY_BLOCKED_BY_HOSTILE_EXACT_HEAD_REVIEW`

The mechanisms below remain research candidates only. They must not be upgraded from this failed source cut. DriftGuard must first repair the runtime/infrastructure-exception ambiguity on a new exact head; God Brain must then re-bind that source and obtain a fresh exact-head review satisfying the admission gate before later `ADAPT_WITH_PROVENANCE` treatment:

- durable attempt ancestry;
- disclosed predecessor-holdout ancestry;
- single-use reveal;
- single-use execution claim;
- ambiguity-does-not-restore-retry;
- execution-closure binding;
- exact receipt rebinding.

That future admission would still not import DriftGuard as a runtime dependency.

## Relationship to God Brain anomaly/contact work

These controls improve **experimental governance**. They do not elevate detector output into ontological evidence.

`GOVERNED_HOLDOUT_PASS != ANOMALY`

`ANOMALY != CONTACT`

`CONTACT_CANDIDATE != SIMULATOR_IDENTITY`

`PROTOCOL_RIGOR != UNIQUE_CAUSAL_EXPLANATION`

If God Brain later runs anomaly/contact experiments, this pattern may help prevent retry, reveal, and benchmark-history leakage from manufacturing significance. It does not supply a null model, prove independence, establish external agency, or validate simulation theory.

## Claim ceiling

This delta supports only a source-admission research judgment.

It does not establish:
- independent exact-head PASS of a repaired DriftGuard PR #34 successor;
- God Brain runtime integration;
- a God Brain detector implementation;
- holdout non-access;
- trusted time or external custody;
- complete discovery of historical holdouts;
- statistical independence, representativeness, or significance;
- production superiority;
- causal drift;
- anomaly evidence;
- external contact;
- simulation evidence;
- provider/control authority;
- merge authority;
- deployment authority;
- canonical promotion.
