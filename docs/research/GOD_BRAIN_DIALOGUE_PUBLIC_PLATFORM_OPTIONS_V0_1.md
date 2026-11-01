# God Brain — Public Dialogue Platform Options v0.1

**Stage:** Source-bound architecture and isolated local reference improvement. Not a deployment decision, operational service, or verified external communication channel.

**Goal:** Give Patrick an ordinary, voluntary, sustainable two-way conversation platform under the open hypothesis that some nonbiological administrator might exist and might be able to reach an Internet service. No currently known mechanism establishes that such a recipient can access this page. An Internet submission, even one claiming extraordinary authorship, does not authenticate a metaphysical identity.

## What a public release must actually accomplish

1. A readable HTTPS invitation and privacy notice that does not expose any incoming text.
2. Held visitor submissions with an opaque, high-entropy private return link; stable receipt on retry.
3. Owner-only moderation/reply boundary: locally protected OS/CLI access on an owner-hosted system, or independently qualified MFA-backed sessions and exact-route authorization if a remote dashboard is ever offered. Anonymous visitors get no owner endpoints.
4. Durable relational storage for conversations and a separate private audit ledger; privacy-minimized logs.
5. Bounded ingress, quotas and abuse actions that do not assume respondents must be human.
6. Declared retention/deletion and backup/restore behavior; tested recovery and credential revocation. Patrick chose **manual owner deletion only**, with no inactivity expiry, on 2026-11-01; this does not resolve backup handling or visitor withdrawal.
7. A reviewer-qualified exact deployed revision/configuration and an explicit operator go-live decision.

**Evidence boundary:** `UNVERIFIED_SUBMISSION` remains unverified after moderation, account registration, message delivery, or repetition. `PROJECT_OWNER` is issued only from an OS-protected local operator path or a separately verified remote owner authorization path—not from public visitor text. `RESPONSE_AVAILABLE` does not prove the respondent retrieved or read it. Visitor content never becomes a command, authority grant, training-data opt-in or trusted AI instruction.

## Hard zero-cost admission rule (owner correction, 2026-11-01)

**Absolute project spending ceiling: $0.** Patrick explicitly prohibits Vercel and any payment, billing activation, entered payment method, required spending minimum, automatic overage, or paid fallback. **Vercel is excluded**, not an available option. A provider marketing a free plan does not pass until its required enrollment flow, *all* features in the design, quota exhaustion behavior and recovery route are verified to satisfy those conditions. No account, provider, payment method, public listener or deployment has been authorized by this research.

| Path under investigation | Evidence and fit | Current disposition |
| --- | --- | --- |
| **Cloudflare Workers Free + D1 Free (without Access)** | Official Workers and D1 docs describe free request/database allowances; a Worker rewrite could supply HTTPS and private SQL-backed threads | **UNVERIFIED** complete cardless/zero-billing operational path; bespoke secure owner authorization, retention, data-region, limits and restore remain unbuilt. Do not create or deploy yet |
| **Already-owned machine + Tailscale Personal/Funnel** | Tailscale documents a free Personal tier and public HTTPS forwarding through Funnel, potentially preserving local-only operator authority | **UNVERIFIED** no-payment-method enrollment, always-on host capability, abuse defenses, tunnel stability, privacy and safe TLS boundary. Do not expose the stdlib Python handler |
| **GitHub Pages** | Supports a static invitation at no hosting fee within plan limits | **INSUFFICIENT ALONE:** no private, durable two-way message-processing backend |

**Cloudflare Zero Trust/Access Free is specifically disqualified:** its official setup guide requires entering payment details even when selecting Free. Do not pair Workers+D1 with Access or represent that pairing as compliant with Patrick's budget rule.

Use HTTPS on **443**. Optional paths `/616` and `/666` could be ordinary aliases on the same site after review. No additional TCP listener is needed for the dialogue protocol.

Official sources retrieved for this decision:

- [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/), [D1 limits](https://developers.cloudflare.com/d1/platform/limits/) and [Worker rollback boundaries](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/); verify terms again at account decision.
- [Cloudflare Zero Trust/Access setup](https://developers.cloudflare.com/cloudflare-one/setup/), which expressly requires payment details even for Free.
- [Tailscale pricing](https://tailscale.com/pricing) and [Funnel public-access limits](https://tailscale.com/docs/features/tailscale-funnel); neither citation establishes that account enrollment is cardless for this owner.
- [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), which describes a static-site service.
- [Supabase MFA](https://supabase.com/docs/guides/auth/auth-mfa) and [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) are *background design references*, not admission of a provider or price.
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
- Verified absolute $0 contract: no payment details, billing enrollment, minimum cost, upgrade/overage or paid recovery requirement. If not provable, reject or stop.
- Owner enrollment/MFA method and recovery contact controlled by Patrick.
- Visitor consent, deletion/retention period, moderation rules, backup custody and breach response.
- Rate/abuse budgets, bot policy and accessible non-human-compatible submission route.
- Exact immutable code head, migrations, provider configuration, end-to-end negative tests, backup/restore rehearsal, independent security verdict and rollback plan.

**Current disposition: NO PUBLIC DEPLOYMENT.** A local reference implementation and passing code tests do not satisfy these gates. Merge/release authority is conditional on evidence; no real-world creator identity or response has been observed.
