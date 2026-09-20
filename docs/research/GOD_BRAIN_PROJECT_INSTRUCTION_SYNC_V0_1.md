# God Brain Project Instruction Source / Installation Sync V0.1

Status: **RESEARCH PROPOSAL / NO PROJECT-SETTING MUTATION**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Base inspected:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

Related candidate deliberately not modified:
- Draft PR #11 — ChatGPT Project interface V1
- exact reviewed-request head currently bound externally: `d80dcec08137d5fd1a8b5cafa62fb60d956e7ce2`

## Problem

A repository file can be the intended source for ChatGPT Project instructions without proving that the ChatGPT Project is actually using that text.

Therefore:

`SOURCE_INSTRUCTIONS != INSTALLED_PROJECT_INSTRUCTIONS`

`INSTALLED_PROJECT_INSTRUCTIONS != CURRENT_CHAT_CONSUMPTION_PROOF`

`REPO_COMMIT != PROJECT_SETTING_EFFECT`

A clean Git source plus a stale Project configuration produces a split-brain operator surface: future chats may reconstruct from one contract while the Project injects another.

## Proposed ownership

### Canonical source text

Future canonical source path:

`architecture/chatgpt/PROJECT_INSTRUCTIONS.md`

Its job is to hold the reviewed human-facing Project instruction payload.

Git owns:
- exact source bytes;
- history;
- reviewable changes;
- current canonical source after promotion.

Git does not prove:
- installation into the ChatGPT Project;
- when installation occurred;
- whether a particular chat consumed that installed version.

### External Project setting

The ChatGPT Project configuration is an external effect surface.

Changing it should be treated separately from merging the source file.

`SOURCE_PROMOTION != PROJECT_INSTALLATION`

The repository may prepare source text without changing the Project setting.

Installing/replacing the Project instructions should require Patrick's explicit authorization for that exact external configuration effect.

## Proposed synchronization state model

Use these states:

- `SOURCE_DRAFT` — source exists only on a noncanonical branch/PR.
- `SOURCE_CANONICAL_NOT_VERIFIED_INSTALLED` — canonical Git source exists but installation has not been verified.
- `INSTALLATION_REPORTED_UNVERIFIED` — an installation action was reported but no adequate comparison evidence exists.
- `INSTALLED_EXACT_SOURCE_VERIFIED` — installed text was compared against the exact canonical source bytes or normalized digest.
- `INSTALLATION_DRIFT` — installed text differs from the intended source.
- `INSTALLATION_UNKNOWN` — current installed content cannot be read or verified.

Do not collapse `UNKNOWN` into `MATCH`.

## Proposed installation receipt

After an authorized installation, record an external-state receipt outside the instruction source subject.

Candidate namespace:

`state/project-interface/instruction-installation/`

A receipt should include:

- receipt schema/version;
- repository;
- source status: `CANONICAL` or `CANDIDATE_NONCANONICAL`;
- canonical source commit when the source status is `CANONICAL`;
- candidate source head and source PR when the source status is `CANDIDATE_NONCANONICAL`;
- source path;
- source Git blob;
- normalized source SHA-256;
- target Project identifier or stable non-secret label;
- action type: install / replace / verify-only;
- installer/operator identity;
- installation timestamp;
- verification method;
- observed installed SHA-256 when readable;
- comparison result;
- limitations;
- explicit claim ceiling.

Example claim ceiling:

`INSTALLATION_RECEIPT != PROOF_CURRENT_CHAT_CONSUMED_TEXT`

A candidate-source receipt must not masquerade as canonical: `canonical_source_commit` remains null while an exact candidate head and positive source PR identify the noncanonical source. A canonical receipt must carry an exact canonical commit and no candidate identity.

The receipt must not contain credentials, tokens, private connector secrets, or unrelated Project content.

## Normalization rule

If a text digest is used, define one deterministic normalization:

1. UTF-8 decode;
2. normalize line endings to LF;
3. preserve all other characters exactly;
4. ensure exactly one final LF;
5. SHA-256 the resulting UTF-8 bytes.

This allows copy/paste installation verification without treating insignificant CRLF differences as semantic drift.

Git blob SHA remains useful source provenance, but it is not interchangeable with the normalized text SHA-256.

`GIT_BLOB_SHA != NORMALIZED_TEXT_SHA256`

## Bootstrap behavior

A fresh chat should not infer installed Project instructions merely because the canonical source file exists.

When installation state matters:

1. read canonical source;
2. read the latest valid installation receipt if one exists;
3. fresh-check any available Project-setting evidence;
4. compare exact source identity to receipt/evidence;
5. classify as MATCH, DRIFT, or UNKNOWN;
6. never invent successful installation.

If the platform does not expose installed instruction bytes for verification, report:

`INSTALLATION_UNKNOWN`

rather than treating the source file as proof.

## Current-chat limitation

Even an exact installation receipt proves only that the setting matched at the observed time.

It does not independently prove that a specific later chat received or followed that version.

`SETTING_MATCH_AT_T1 != CHAT_CONSUMPTION_AT_T2`

A chat may use its available project/context state, but it should not manufacture a cryptographic consumption claim unless the platform exposes evidence that supports one.

## Update workflow

Proposed future workflow:

`EDIT_SOURCE -> REVIEW_SOURCE -> PROMOTE_SOURCE -> AUTHORIZE_INSTALL -> INSTALL -> VERIFY -> RECORD_RECEIPT -> FRESH_CHAT_RECONSTRUCTION_TEST`

Each arrow is a separate stage.

A source edit must not silently imply installation.

An installation must not silently imply successful fresh-chat reconstruction.

A successful reconstruction test must not expand the Project's protected-effect authority.

## Drift handling

If source and installed instructions differ:

1. preserve the old source/install receipt;
2. determine whether Git or the Project setting is intended current authority;
3. do not silently overwrite either side;
4. prepare the bounded correction;
5. require exact authorization before changing the Project setting;
6. verify again after the effect.

For unreviewed source branches:

`DRAFT_SOURCE != INSTALLATION_TARGET`

Do not install an unreviewed branch merely because it is newer.

## Interaction with PR #11

PR #11 proposes the durable source/interface layout.

This proposal does not modify that exact subject while it is delegated for review.

After PR #11 review returns, the result should be reconciled with this synchronization model before any Project-setting installation is treated as verified.

## Recommended eventual machine contract

A future machine-readable contract should define:

- allowed sync states;
- normalization algorithm;
- required receipt fields;
- forbidden receipt fields;
- claim ceilings;
- authorized effect boundary.

The contract should remain research-only until reviewed and deliberately integrated.

## Explicit non-actions

This proposal does not:
- change current ChatGPT Project instructions;
- assert what exact Project instruction bytes are currently installed;
- merge PR #11;
- modify `main`;
- grant permission to change Project settings;
- claim any chat consumed a particular source version.
