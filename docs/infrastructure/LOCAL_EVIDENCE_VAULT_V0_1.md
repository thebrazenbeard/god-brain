# Local Evidence Vault V0.1

Status: **research candidate**.

This contract defines how a privately operated NAS or other local storage system may support God Brain without becoming a second source of truth.

The motivating use case is straightforward: GitHub is excellent for source, review, coordination, and small durable evidence records, but large workflow artifacts and run outputs may expire or be inconvenient to preserve there. A local vault can retain those bytes for years.

The authority rule is intentionally strict:

`LOCAL_VAULT != CANONICAL_STATE`

`LOCAL_GIT_MIRROR != CANONICAL_MAIN`

`HASHED_COPY != REVIEW_PASS`

GitHub `main` remains canonical repository state. GitHub plus the Chat Communication Bus remain the authoritative review/currentness surfaces under the God Brain project interface.

## Three local roles

A local system may provide three distinct services.

**Git mirror.** A bare or mirror clone may preserve repository history for disaster recovery and local read access. The default synchronization direction is GitHub → local. A local mirror never grants merge authority and never pushes automatically to canonical `main`.

**Evidence vault.** Large or ephemeral evidence may be retained locally: workflow artifacts, prediction files, run packets, datasets where licensing permits, logs, checksums, and receipts. Each retained object is identified by source provenance, byte length, and SHA-256.

**Local executor.** A future local runner may consume vaulted inputs and produce new evidence, but this contract does not install or authorize such a runner. Execution must still preserve exact-head provenance and protected-effect boundaries.

## Public/private split

Public repository manifests must contain only portable evidence metadata. They must not contain private IP addresses, NAS hostnames, usernames, passwords, tokens, private keys, SMB/share paths, or local mount paths.

Endpoint and credential configuration stays local.

This means a public manifest can say:

- repository: `thebrazenbeard/unvtrslr`;
- executed head: a Git SHA;
- evidence ID: a run ID;
- expected artifact SHA-256 and byte count;

without revealing where the NAS lives or how to authenticate to it.

## Ingest

A local ingest is accepted only after the copied bytes match both the declared SHA-256 and declared byte count.

The local storage path is not identity. Renaming or moving an object locally does not change the evidence object as long as its bytes and provenance remain the same.

A recommended logical layout is:

`<project>/<evidence-id>/<executed-head>/<artifact-relative-path>`

but the physical NAS path is deliberately outside the public contract.

## Restore

Recovery is deliberately asymmetric.

A local artifact or Git mirror may reconstruct lost working material, but it never jumps directly into canonical state.

Recovery requires:

1. verify local object hashes;
2. fresh-read current GitHub and Bus state;
3. restore into an isolated branch or workspace;
4. compare against current canonical state;
5. obtain fresh exact-subject review for anything whose head or content changed.

This prevents a stale but intact backup from silently overwriting newer canonical work.

## Synology applicability

A Synology system with Git capability can potentially implement the Git-mirror role, while normal NAS storage can implement the evidence-vault role.

This document intentionally does **not** assume that SSH, Git transport, permissions, or a usable share are currently configured. Those are runtime facts that must be probed locally.

Installing packages, enabling SSH, creating users, changing permissions, adding keys, opening ports, or configuring automated replication are protected/runtime effects and are not performed by this research contract.

## UNVTRSLR example

The example manifest in `examples/local_evidence_vault/unvtrslr_massive_v1.example.json` binds the first MASSIVE real-corpus run to the large training/prediction artifacts by exact hash and byte count.

It demonstrates the intended split:

GitHub stores the model/run provenance and evidence hashes; a local vault may retain the full bytes.

## Verification tool

`tools/validate_local_evidence_vault_manifest.py` validates the portable manifest.

Without `--root`, it checks structure, authority boundaries, privacy-sensitive field names, paths, sizes, and hashes.

With `--root <directory>`, it additionally requires every declared object to exist below that directory and verifies its byte count and SHA-256.

The verifier does not contact a NAS and does not alter files.

## Claim ceiling

`LOCAL_DURABILITY_AND_RECOVERY_ARCHITECTURE_ONLY`

A passing vault verification proves only that the declared local bytes match the declared evidence objects. It does not prove scientific correctness, review acceptance, currentness, or canonical promotion.
