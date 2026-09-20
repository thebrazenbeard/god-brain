# God Brain Recovery and Continuation Contract V1

Status: CANDIDATE PROJECT INTERFACE

A continuation artifact exists to reduce reconstruction cost. It is never currentness authority.

## Continuation role

A continuation may record:

- last observed `main` head;
- open PRs/branches relevant at save time;
- reviewed exact heads and evidence pointers;
- delegated subjects and Bus thread pointers;
- known blockers;
- work completed in the retiring execution surface;
- next candidate frontiers;
- unresolved questions;
- exact files/commits produced by that execution surface.

It must label those facts as observations at save time.

## Required warning

Every continuation should state, in substance:

> Treat this checkpoint as a starting snapshot, not current truth. Fresh-check mutable GitHub and Bus state before resuming work. Preserve head movement and newer durable evidence.

## What a continuation must not do

A continuation must not:

- declare a remembered head current without fresh verification;
- resurrect an expired delegation;
- extend a review verdict to a changed head;
- claim a deployment/provider state is still current without readback;
- create protected-effect authority;
- redefine worker identity solely by prose;
- overwrite newer GitHub/Bus evidence;
- turn chat history into canonical project state.

## Recommended storage

Use:

`state/continuation/<DESCRIPTIVE_ID>.md`

A save should live on an isolated state branch unless an already-authorized canonical contract says otherwise.

The filename should carry enough project/role/time identity to distinguish it from unrelated saves.

## Minimal continuation format

```text
checkpoint_id:
created_at:
role:
repository:
save_branch:
save_commit:
observed_main_head:

completed:
- ...

reviewed_exact_heads:
- subject:
  head:
  verdict:
  evidence_pointer:

delegated_subjects:
- subject:
  owner:
  exact_head:
  bus_thread:
  status_at_save:

known_blockers:
- ...

next_candidate_frontiers:
- ...

required_fresh_checks:
- main
- open PRs
- relevant branch heads
- Bus coordination
- reviews/verdicts
- delegated subjects

protected_effects_not_authorized_by_checkpoint:
- merge
- deploy
- ...
```

## Recovery algorithm

When a fresh chat receives a continuation:

1. read `CHATGPT_REPO_INTERFACE.yaml`;
2. read this contract and the bootstrap procedure;
3. read the continuation;
4. fresh-read all mutable state named by the continuation;
5. compare observed current state to the snapshot;
6. preserve newer state and classify stale snapshot facts as historical;
7. reconstruct collision ownership;
8. continue the highest-value valid frontier.

If the checkpoint conflicts with newer durable evidence, newer durable evidence wins within its actual scope.

## Chat retirement

Before intentionally retiring a substantial God Brain execution chat, create a continuation only when meaningful state would otherwise be expensive to reconstruct.

Do not create checkpoints merely to preserve conversational flavor. Important architectural decisions belong in ordinary repository artifacts; work-bearing coordination belongs in the Bus; review evidence belongs on exact bound review surfaces.

`CHAT_CONTINUATION != PROJECT_MEMORY`

`CHECKPOINT != CANON`

`RECOVERY_SPEED != AUTHORITY`
