# God Brain Intake and Evidence Admission Contract V0.1

Status: **RESEARCH SPECIFICATION / NO RUNTIME IMPLEMENTATION**

Parent portfolio subject: Source Universe V3 exact head `f56f52b3606839147a12e68375612336fb9bbfdd`.

## Purpose

God Brain needs a hard boundary between acquiring information and believing, remembering, currentizing, or acting on it.

The contract therefore separates:

```text
ACQUIRED != TRUSTED
RAW != NORMALIZED
NORMALIZED != INTERPRETED
INTERPRETED != VERIFIED
RETRIEVED != ADMITTED
STORED != CURRENT
CURRENT != TRUE
SIMILAR != SAME_PROVENANCE
TOOL_OUTPUT != AUTHORITY
```

The central design rule is:

> Intake may preserve and structure evidence. It may not manufacture truth, currentness, independence, memory authority, or effect authority.

## Donor evidence

Fresh exact donor heads bound for this research subject:

- `ingest@27764c9fb97c84d178a3f66e0da2d669df645ed6`
- `semiotics@37117a2097f7f2aa35968fc9db24eacf7240826e`
- `semanticatlas@895677a64af5d29b580306ca52ecc0e0607a9ccc`
- God Brain target main `495c2b42932153cba0926744d04a69bc34557f81`

Ingest contributes exact acquisition, raw preservation, deterministic derivation, hashing, and receipt discipline. Semiotics contributes source/context-bound interpretations that remain interpretations. Semantic Atlas contributes provenance/lifecycle separation and the rule that semantic similarity does not merge provenance, authority, identity, or historical state.

God Brain's existing current-memory, deep-memory, adaptable-I/O, semantic, cognitive, and evidence-boundary contracts remain target constraints.

## Four object families

### AcquisitionRecord

Captures what was actually acquired and from where. It binds source locator/kind, observation time, exact raw digest/size, media type, privacy scope, revision binding, and transport evidence.

An acquisition record does not say the content is true.

### NormalizationRecord

Binds one derivative to one raw parent, normalizer/version, exact derivative digest, transformations, and fidelity class.

Normalization is never allowed to erase the raw artifact's identity or masquerade as raw evidence.

### InterpretationCandidate

Binds a proposed proposition/meaning to an artifact, source context, provenance class, uncertainty, and lifecycle.

Interpretation can be proposed, active, superseded, retracted, or unresolved without rewriting the source artifact.

### EvidenceAdmissionDecision

Decides whether a candidate may enter a bounded evidence plane, with explicit evidence class, claim ceiling, independence family, currentness scope, privacy scope, disposition, and rationale.

Admission does not decide global truth and does not authorize effects.

## Pipeline

```text
acquire raw
  -> verify raw identity
  -> optional normalization
  -> build interpretation candidates
  -> classify provenance + independence
  -> apply privacy + scope
  -> admit / quarantine / reject / defer
  -> hand off to currentness resolution
```

Currentness remains downstream because God Brain already requires explicit supersession/conflict handling rather than newest-wins selection.

## Mutable sources

A mutable branch name, webpage, database row, tool response, or provider object may be useful evidence, but an exact-artifact claim requires an exact revision/object identity when the provider supports one. Otherwise the admission ceiling must say that the material was observed at a time, not that a mutable locator permanently identifies those bytes.

## Independence

Two summaries, features, embeddings, model opinions, or repository copies derived from one source family are one evidence lineage unless independent acquisition/provenance establishes otherwise.

```text
MULTIPLE_DERIVATIVES != INDEPENDENT_EVIDENCE
COPIED_LINEAGE != INDEPENDENT_CORROBORATION
```

## Privacy

Privacy may stay the same or become narrower during admission; it may not silently broaden.

Private source access does not make private content generic training material, public research evidence, or portable architecture payload.

## Authority firewall

No acquisition, normalization, interpretation, admission, retrieval, model output, tool result, source label, or currentness projection can create permission for a protected effect.

```text
EVIDENCE != AUTHORITY
CAPABILITY != PERMISSION
CURRENTNESS != AUTHORIZATION
```

## Hostile fixtures

`specs/research/fixtures/GOD_BRAIN_INTAKE_EVIDENCE_HOSTILE_CASES_V0_1.json` binds cases for mutable refs, raw/normalized confusion, model self-verification, false independence, private-scope widening, newest-wins currentness, tool-result authority escalation, provenance collapse, destructive supersession, retrieval-frequency truth promotion, and user-statement overpromotion.

## Claim ceiling

This research subject does not install an intake runtime, migrate memory, couple God Brain to Ingest/Semantic Atlas/Semiotics at runtime, promote current state, grant effect authority, or establish scientific validation.
