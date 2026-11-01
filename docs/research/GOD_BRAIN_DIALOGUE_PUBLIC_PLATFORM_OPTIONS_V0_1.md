# God Brain — Public Dialogue Platform Options v0.1

**Stage:** Source-bound architecture and isolated local reference improvement. Not a deployment decision, operational service, or verified external communication channel.

**Goal:** Give Patrick an ordinary, voluntary, sustainable two-way conversation platform under the open hypothesis that some nonbiological administrator might exist and might be able to reach an Internet service. No currently known mechanism establishes that such a recipient can access this page. An Internet submission, even one claiming extraordinary authorship, does not authenticate a metaphysical identity.

## What a public release must actually accomplish

1. A readable HTTPS invitation and privacy notice that does not expose any incoming text.
2. Held visitor submissions with an opaque, high-entropy private return link; stable receipt on retry.
3. Owner MFA-backed session and exact-route authorization for private inbox, review, reply, closure and revocation.
4. Durable relational storage for conversations and a separate private audit ledger; privacy-minimized logs.
5. Bounded ingress, quotas and abuse actions that do not assume respondents must be human.
6. Declared retention/deletion and backup/restore behavior; tested recovery and credential revocation.
7. A reviewer-qualified exact deployed revision/configuration and an explicit operator go-live decision.

**Evidence boundary:** `UNVERIFIED_SUBMISSION` remains unverified after moderation, account registration, message delivery, or repetition. `PROJECT_OWNER` is issued only after server-side owner authorization. `RESPONSE_AVAILABLE` does not prove the respondent retrieved or read it. Visitor content never becomes a command, authority grant, training-data opt-in or trusted AI instruction.

## Provider choices — research only

| Candidate | Fit | Primary constraints |
| --- | --- | --- |
| **Cloudflare Workers + D1 + Access** | One-vendor HTTPS/SQL/edge option with relatively low entry cost; evaluate in an isolated preview | Rewrite the Python HTTP handler; validate Access JWT at every privileged origin route; apply quotas and data-region/backup policy; application rollback does not roll back D1 schema |
| **Vercel + Supabase Postgres/Auth** | Reuses a Vercel-oriented ecosystem; Postgres transactions and Supabase MFA/RLS | Two provider/account surfaces, correct service-key isolation, robust revocation and RLS tests; Vercel Functions must not depend on local SQLite persistence |
| **Managed VM/container + relational DB** | Potentially retains more of the Python code and conventional networking | More TLS, host hardening, operations, backups, monitoring and cost responsibility; public TCP 616/666 give no proven communication advantage |

Use HTTPS on **443**. Optional paths `/616` and `/666` could be ordinary aliases on the same site after review. No additional TCP listener is needed for the dialogue protocol.

Sources retrieved for this decision:

- [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) and [D1 limits](https://developers.cloudflare.com/d1/platform/limits/); verify quotas/prices again at provider selection.
- [Cloudflare Access for self-hosted apps](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/) and [Worker rollback boundaries](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/).
- [Vercel SQLite in Functions](https://vercel.com/kb/guide/is-sqlite-supported-in-vercel), [Vercel pricing](https://vercel.com/pricing).
- [Supabase pricing](https://supabase.com/pricing), [MFA](https://supabase.com/docs/guides/auth/auth-mfa), [RLS/privileged keys](https://supabase.com/docs/guides/database/postgres/row-level-security), [session lifecycle](https://supabase.com/docs/guides/auth/sessions).
- [PostgreSQL INSERT/ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html).
- [OWASP denial-of-service](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).

These documents establish vendor contracts and candidate design, not operational security or implementation performance.

## Data model and transaction contracts

- `threads`: stable ID, hash of bearer credential, state `open/closed/revoked`, server timestamps.
- `messages`: thread FK, `author_kind` (unverified visitor versus authenticated owner), separate `claimed_name`, body, moderation state, request key, content fingerprint.
- `moderation_events`: operator action, server time, affected record, verified owner identity reference (when a real identity provider exists); no raw return token or message body.
- Unique `(thread_id,request_key)` and atomic create/replay semantics: same key+content gives the same receipt; changed content fails `409`; concurrent duplicates cannot create extra messages.
- A compromised bearer link can be revoked. Revocation invalidates retrieval, not historical private records. Retention deletion must be explicit and tested against backups.
- Historical local SQLite visitor data must **not** be silently uploaded to a public managed database: prior visitors were not given that privacy contract or recoverable links.

The isolated local v0.3 candidate tests some of these contracts with SQLite. It does **not** qualify a PostgreSQL/D1 adapter, MFA, host recovery, abuse controls or public release.

## Portfolio source admission

| Source | Useful lesson | Decision |
| --- | --- | --- |
| [Blotter](https://github.com/thebrazenbeard/Blotter) | Transactional idempotent append and privacy-minimized event receipts | **ADAPT_WITH_PROVENANCE** as a freshly implemented audit pattern; no transcript sync or unlicensed code copying |
| [Rezon](https://github.com/thebrazenbeard/rezon) | Separate source claim, verified actor, authority and actual effect | **ADAPT_WITH_PROVENANCE** in labels; no LLM runtime coupling |
| [VeraMesh](https://github.com/thebrazenbeard/vera-mesh), [WorkBridgeMCP](https://github.com/thebrazenbeard/WorkBridgeMCP) | Authentication and host-authority boundaries | **RESEARCH_ONLY**; never connect anonymous visitor text to host commands, tools or credentials |
| [World Zero](https://github.com/thebrazenbeard/world-zero), [Temporal](https://github.com/thebrazenbeard/temporal) | Falsification and chronology methods | **RESEARCH_ONLY**, optional to dialogue; no claim of contact |
| [DeepMemoryStorage](https://github.com/thebrazenbeard/deepmemorystorage) | Public append-only records are not private conversation storage | **REJECT transcript integration** |

Public GitHub visibility does not provide code-reuse rights. God Brain's own README calls its original source **proprietary/source-visible**. Reuse only user-owned or affirmatively licensed patterns under a deliberate provenance and privacy decision.

## Release decision packet still needed

Before creating accounts, configuring DNS/secrets or going live, bind:

- Selected provider/project and public origin/domain, data region and storage location.
- Explicit spending ceiling and handling of overages/free-tier suspension.
- Owner enrollment/MFA method and recovery contact controlled by Patrick.
- Visitor consent, deletion/retention period, moderation rules, backup custody and breach response.
- Rate/abuse budgets, bot policy and accessible non-human-compatible submission route.
- Exact immutable code head, migrations, provider configuration, end-to-end negative tests, backup/restore rehearsal, independent security verdict and rollback plan.

**Current disposition: NO PUBLIC DEPLOYMENT.** A local reference implementation and passing code tests do not satisfy these gates. Merge/release authority is conditional on evidence; no real-world creator identity or response has been observed.
