# God Brain Typed Semantic Mediation V0.1

Status: **RESEARCH SPECIFICATION / NO RUNTIME**

Transfer candidate: **T37 — SEMANTIC_MEDIATION_WITH_EXPLICIT_FIDELITY**

Parent coordination head: `c40d98a98a4627ec3b1a83ffaad514ad345f9612`

Fresh donor cuts:

- `sql-connectome@b609fcec50fe5a135ca1d8139f5563f5631582b2`
- `spm@d9ea72798ac892ac75f858177b6ed0c5a6b4c37c`
- `semiotics@37117a2097f7f2aa35968fc9db24eacf7240826e`

## Purpose

God Brain needs to translate meaning across representations, tools, models, protocols, and research artifacts without pretending that linguistic or structural similarity proves semantic identity.

```text
SYNTAX SIMILARITY != SEMANTIC EQUIVALENCE
SEMANTIC SIMILARITY != SAME PROVENANCE
TRANSLATION PASS != BEHAVIORAL EQUIVALENCE
INTERPRETATION != TRUTH
SPECIFICITY != CONFIDENCE
MEANING != AUTHORIZATION
TARGET ACCEPTANCE != SOURCE/TARGET EQUIVALENCE
AMBIGUITY != PERMISSION TO COLLAPSE
```

## Meaning frame

A source frame binds context, referents, propositions, modality/force, polarity, scope, speech acts, unresolved interpretations, and provenance. A mediation target does not inherit any of those merely because its surface form is similar.

The anti-Righter rule is structural: `PROBABLE(X)` cannot silently become `ASSERTED(X)`.

## Typed mediation

A mediation mapping records what was preserved, changed, dropped, added, narrowed, broadened, or left unresolved. The system does not replace this with a single similarity score.

Fidelity is one of:

- `EXACT`
- `QUALIFIED`
- `LOSSY`
- `UNRESOLVED`
- `INCOMPATIBLE`

Component fidelity is recorded separately before an overall ceiling is assigned.

## Validation

Target validation can establish that the target representation parses, plans, type-checks, or otherwise satisfies a target-specific validator. It cannot prove equal behavior for all possible inputs.

```text
TRANSLATE != VALIDATE != EXECUTE != BEHAVIORAL EQUIVALENCE
```

## Interpretation lineage

Semiotic interpretations remain source-bound. Specificity is deterministic ordering, not confidence or truth. Corrections supersede rather than erase history. Explicit relations remain metadata and do not acquire inverse, transitive, or truth-propagating force unless separately evidenced.

## Authority

Understanding what a command means is not permission to carry it out.

```text
UNDERSTAND COMMAND != AUTHORITY TO EXECUTE
SEMANTIC RECEIPT != AUTHORIZATION RECEIPT
```

Effect authorization remains external to semantic mediation.

## Semantic loss

Loss and uncertainty are monotonic across the mediation receipt chain: later validation cannot erase earlier loss markers merely because a target accepts the result.

## Pipeline

```text
bind source context
  -> construct source meaning frame
  -> declare target representation
  -> map with typed transformations
  -> assess component fidelity
  -> preserve unresolved ambiguity
  -> validate target representation where available
  -> emit provenance-bound mediation receipt
  -> hand off without authority promotion
```

## Claim ceiling

This contract defines a bounded semantic mediation architecture. It does not establish universal semantic equivalence, behavioral equivalence, truth/currentness, execution authority, model consciousness, AGI, simulation evidence, or external contact.
