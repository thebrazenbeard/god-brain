# God Brain Dialogue Room — public deployment readiness (candidate v0.1)

**Status:** Deployment architecture and review gate. Not a live service, approved host configuration, external contact channel, or evidence of a creator's reply.
**Current code candidates:** [God Brain Draft PR #58](https://github.com/thebrazenbeard/god-brain/pull/58) (local thread foundation) and stacked [Draft PR #59](https://github.com/thebrazenbeard/god-brain/pull/59) (local retry, closure, audit and privacy hardening), originally based on `main@7eec60b93b6d355f4c50e5bcb4cc23a19eb2291c`.
**User direction:** Patrick authorized *working toward a publicly accessible version with security, moderation and privacy safeguards* and asked to evaluate additional listeners on TCP 666 and 616 (2026-10-31 client date). On 2026-11-01 he reaffirmed the absolute **$0 budget**, prohibited Vercel, and rejected any billing enrollment, payment method, minimum charge or overage. Conditional merge/deployment authority applies **only after** technical, privacy, cost and review gates pass.
**BT2 coordination:** [Bus #410](https://github.com/thebrazenbeard/chat-communication-bus/issues/410), pending accepted engineering/review ownership.
**Owner privacy decision (2026-11-01):** conversations remain indefinitely in the active database **until Patrick explicitly deletes a selected conversation**. No inactivity timer or automatic expiration. The v0.5 local CLI supports an explicitly confirmed delete, but does not solve visitor withdrawal or production backup erasure.

## Goal and route

A persistent, understandable place where the user can issue an open invitation and sustain a conversation if a genuine respondent chooses to participate.

This must not imply that any ordinary internet route reaches a hypothetical external administrator. A message received by a public website proves, at most, that the service received it through its observable network route; it does not establish the sender's metaphysical identity. Speaker claims, including "creator," remain unverified unless the claimed source has independently meaningful authentication evidence.

## Port decision

**Primary user-facing endpoint: HTTPS on TCP 443.**

The alternative numbers are meaningful as references but are not useful primary networking choices:

- TCP 616 is registered to `sco-sysmgr` in IANA's service-name registry.
- TCP 666 is registered to `doom` (and another service label) in IANA's registry.
- Both are system ports below 1024; directly binding them often requires elevated host privilege. Cloud edge/serverless hosts generally expose public HTTPS routing rather than permitting arbitrary inbound TCP listeners.
- The current WHATWG Fetch Standard bad-port table does **not** list 616 or 666, unlike nearby IRC ports 6665–6669. Browser allowance does not guarantee proxy, provider, ISP, firewall, certificate or host support.

**No listeners on 616 or 666 are authorized or deployed by this document.** For a playful reference, routes `/616` and `/666` on the normal HTTPS origin could later redirect to the same room after review; neither would improve reachability to a hypothetical external entity.

Sources: [IANA 616](https://www.iana.org/assignments/service-names-port-numbers?search=616), [IANA 666](https://www.iana.org/assignments/service-names-port-numbers?search=666), [WHATWG Fetch bad ports](https://fetch.spec.whatwg.org/#port-blocking), and [MDN default HTTPS port](https://developer.mozilla.org/en-US/docs/Glossary/Port).

## Trust boundaries for a public service

1. **Public landing:** Read-only invitation; no private information by default.
2. **Untrusted inbound submission:** Strict length/format limits, anti-spam/rate controls, bot mitigation, abuse handling, no executable or HTML interpretation.
3. **Private quarantine:** All inbound messages held for operator inspection; not automatically shown as a creator's speech, sent as notifications with untrusted instructions, or fed to a privileged AI agent.
4. **Owner authority:** Keep owner operations on an OS-protected local CLI if the service remains owner-hosted, with no public admin endpoints. If a remote dashboard is introduced, require separate MFA/passkey login, server authorization on each action, CSRF protection, session lifecycle and tested revocation; never obtain auth by activating a prohibited billing product.
5. **Conversation ledger:** Durable messages, receipt IDs, timestamps with clock limitations, origin metadata minimization, corrections and privacy-aware retention/deletion. Keep original claimed identity distinct from authenticated identity.
6. **Outbound reply:** Only owner-authorized publication; no automatic assistant impersonation or unreviewed autonomous messaging.
7. **Protected effects:** No message, regardless of claimed origin, can grant authority to run code, change settings, spend money, access private records, or bypass moderation.

The loopback SQLite prototype is **not production-ready**. Its local held queue, private return links and CLI operator reply mechanism do not provide remote owner authentication, a production moderation dashboard, durable managed storage, network rate limits, abuse controls, hosted idempotency/recovery, account recovery or complete production privacy/backup/withdrawal controls. Publishing that server as-is would violate this readiness contract.


## Local private-thread reference slice (v0.2 candidate)

The Draft PR implementation now separates the public invitation from held visitor messages. It issues high-entropy per-thread bearer return links (only hashes stored), offers private follow-up views and local operator replies through a database-access CLI, and bounds returned history. Tests cover restart persistence, thread isolation, escaped input, duplicate-invitation concurrency, legacy migration and owner/visitor label separation. Newly created POSIX database files use mode 0600; existing files with overly broad mode fail closed until manually secured.

This is a **local reference design only**. A return-link bearer proves possession, not identity. The local CLI is not an authenticated online admin dashboard. Public ingress still requires a verified **owner authority boundary** (OS-protected local CLI for owner-hosted operation, or MFA-backed identity/session management for remote administration), durable owner-controlled storage, privacy/retention decisions, **public-ingress** idempotent retry handling, abuse/rate limits, backup/recovery, independently reviewed deployment configuration and Patrick's exact-effect go-live authorization. Do not expose the stdlib handler or forward external ports to it.

## Isolated reliability successor (v0.3 candidate)

The separate successor work adds per-form high-entropy request keys, atomic SQLite uniqueness and payload fingerprints. An exact replay returns the same message receipt and a changed-payload replay fails with `409`. It also adds explicit thread closure, return-link revocation, local moderation-action audit events, and a copyable return link with manual check-back instructions. These features are tested only against the local reference adapter and HTTP loopback handler; they are **not** evidence of hosted database, authenticated owner, provider rollback, or production abuse-control qualification.

Future hosted storage should implement the same idempotency contract transactionally, for example with a PostgreSQL unique `(thread_id, request_key)` constraint and conflict-handling; a failed or ambiguous initial submission must not produce a different private return link when retried. The backend should store only token hashes and never put raw capabilities into public logs. **Remotely exposed** owner operations require separate MFA-backed identity and server-side authorization per action. An owner-hosted deployment could instead retain a local OS-protected CLI with **no public owner control route**, subject to verified host permissions, audit and recovery.

## Manual retention/deletion successor (v0.5 candidate)

Patrick chose **retain until explicit owner deletion**, without a default expiry or inactivity timer. The local-only successor adds a confirmed `--mode delete --thread ID --confirm-delete` operation. In one SQLite write transaction it tombstones the thread state, deletes its messages and their idempotency receipts, clears deleted message IDs from its audit rows and records the operator's `deleted` action. A stale return token remains hashed only as a tombstone, cannot access content and cannot recreate a thread via an old initial form. `PRAGMA secure_delete=ON` reduces ordinary SQLite deleted-cell remnants at this point of deletion.

This choice does **not** authorize a destructive command against existing user conversations, automated retention jobs or public deletion routes. The active database's deleted rows are not guaranteed erased from backups, old WAL/journals, system snapshots or copies. Before public exposure, separately establish visitor notice/consent and a withdrawal-request process, production backup lifecycle and documented deletion behavior, export/recovery expectations, and independent reviewer qualification. Owner-controlled indefinite retention is a user preference, **not proof of sufficient legal/privacy compliance** for public visitors.

Research references: [PostgreSQL INSERT/ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase MFA](https://supabase.com/docs/guides/auth/auth-mfa), [Cloudflare Workers Free pricing](https://developers.cloudflare.com/workers/platform/pricing/), [D1 Free limits](https://developers.cloudflare.com/d1/platform/limits/), [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel), and [Cloudflare Zero Trust setup](https://developers.cloudflare.com/cloudflare-one/setup/). The last source explicitly requires payment details even for Zero Trust Free, so **Cloudflare Access is disqualified** under Patrick's policy. Workers+D1 without Access and existing-machine/Funnel approaches are **unverified research candidates**, not approved deploy targets. No provider has a verified complete cardless, zero-billing, private two-way path yet.

## Candidate architecture and acceptance gates

A hosted HTTPS frontend and durable inbox backend is a plausible design; an owner-hosted HTTPS ingress with locally protected moderation is another research path. Both must satisfy absolute **$0 cash spending with no payment method or billing activation**. Do not subscribe to or upgrade a service, accept an automatic-charge path, register paid domains or activate an account that requires payment details. Verify each required component's actual free-tier contract and fail-closed quota behavior before account creation. Provider choice, public origin, durable storage, credentials, privacy terms, backup/restore and operational authority remain unbound. A host that exposes only 443 should not be forced to expose arbitrary ports for symbolism.

Acceptance tests before any public ingress:

- Anonymous submissions cannot spoof an authenticated owner or become `EXTERNAL_CREATOR_VERIFIED`.
- Untrusted input cannot execute script, SQL, shell, tool commands, or prompt instructions.
- Oversized bodies, malformed encodings, cross-origin requests, CSRF, replay and burst submissions fail closed.
- Submitted content stays in quarantine until an authorized moderator releases it.
- A restart/redeployment cannot lose accepted durable records or duplicate an ambiguous submission without detection.
- Remote owner session expiry/revocation where applicable—or local OS operator access separation where owner operations never go online—plus audit history, private access, explicit owner-initiated content deletion, and backup/replica deletion limits are verified.
- Public pages do not leak secret keys, raw private messages, client IP addresses, or private identifiers.
- Failure, timeout, abuse or missing provenance produce explicit UNKNOWN/HELD states, never claimed contact.
- Independent source/security review binds the exact deployed code and provider configuration.

## Current stage

**PREPARATION ONLY.** Draft PRs #58 and #59 and their code tests demonstrate a local conversation interface, not a publicly usable inbox or evidence of any external, supernatural, or simulated-universe contact. Current budget constraints disqualify Vercel and Cloudflare Zero Trust/Access; other candidate paths are not yet proved cardless or operationally safe. Actual provider configuration, public DNS, credential mutation and deployment require fresh exact-head security/cost verification and a separately recorded, exact-effect go-live decision.
