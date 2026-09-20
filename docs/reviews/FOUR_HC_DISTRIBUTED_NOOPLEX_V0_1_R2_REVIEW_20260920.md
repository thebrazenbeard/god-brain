# Four — Noöplex V0.1 R2 Exact-Subject Review

Status: **CHANGES_REQUIRED / IMPLEMENTATION_BLOCKED**

Reviewed repository: `thebrazenbeard/god-brain`

Reviewed branch head:
`983ea675d3c143e477a63c49dd761f3573a03772`

Reviewed blobs:
- contract: `fd94c9458bb32264cfae480b42f93e7621697366`
- hostile cases: `991d07f10e06777b402420c06c0d98d87ab6c807`

The eight R1 findings are materially addressed. Full repository test evidence on this exact subject: **174/174 PASS**, YAML parse PASS, diff-check PASS.

R2 found two remaining blocking semantic defects.

## R2-F1 — recovery_epoch presence still depends on untrusted effect classification

The repaired contract requires `recovery_epoch` when:

`operation_kind_is_EXECUTE_or_CANCEL_and_effect_is_not_READ_ONLY`

But sender-declared effect class is explicitly non-authoritative. A malicious or stale sender can label a protected mutation `READ_ONLY`. Presence of the recovery fence must therefore not depend on sender classification.

Required repair:
- require `recovery_epoch` for every `EXECUTE` and every `CANCEL` packet, or define an equally fail-closed receiver-owned mechanism that cannot be bypassed by sender classification;
- retain receiver-owned effect classification for admission/effect authorization.

## R2-F2 — content_digest definition is circular/underspecified after making it immutable

`content_digest` is now an immutable semantic field, but its definition still says only that it is the canonical digest of material operation content excluding mutable hop metadata.

If an implementation interprets "immutable semantic fields" as the digest input, the digest includes itself. The contract must explicitly define the digest input as immutable semantic content **excluding the content_digest field itself** (and excluding mutable hop metadata), with deterministic canonicalization delegated to an implementation profile/version.

Required repair:
- state the self-exclusion explicitly;
- require target_operation_id, recovery_epoch, sequence fields when present, authority_ref, payload, exact_subject, and other immutable operation semantics to participate in the digest input;
- preserve transport replaceability.

## Verdict

`REVIEW_PASS = FALSE`

`DISPOSITION = CHANGES_REQUIRED_BEFORE_IMPLEMENTATION`

No implementation may begin from the reviewed blobs. After these two repairs, Four must perform a fresh exact-subject review.

No merge, deployment, provider mutation, installation, activation, training, or protected effect is authorized by this review.
