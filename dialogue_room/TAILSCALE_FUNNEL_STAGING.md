# God Brain — Tailscale Funnel private dialogue staging (candidate v0.6)

**Not a deployment instruction or authorization.** This is a precise staging and rollback contract for a sign-in-free two-way channel. It is separate from the already public, GitHub-login-required [open invitation](https://github.com/thebrazenbeard/god-brain/issues/62).

## Absolute cost and owner contract

- Cash cost **$0**. No Vercel, credit card, paid subscription, billing enrollment, paid fallback, automatic overage or new custom domain. If that cannot be verified for the exact owner tailnet, stop before enabling Funnel.
- Use an **existing Tailscale Personal Free** tailnet only after verifying actual account plan and host permissions. Vendor docs say Personal Free needs no billing details; [Funnel docs](https://tailscale.com/docs/features/tailscale-funnel) describe its public HTTPS routing. A source claim is not an account/host qualification.
- Keep operator actions **local CLI only**. Never publish the Executor or VeraMesh gateways, an SSH/RDP port, an admin dashboard, an unprotected SQLite file, or any existing private Tailscale Serve mappings.
- A response to this ordinary Internet application remains an `UNVERIFIED_SUBMISSION`, even if it claims unusual origin. No notification or automated AI reply is offered.

## Observed host baseline (2026-11-01; recheck before touching anything)

- Lappy had Tailscale **v1.102.4**, `BackendState=Running`, `SelfOnline=true`, MagicDNS enabled, a tailnet DNS name and Python **3.14.5**.
- Existing **tailnet-only** Serve mappings used HTTPS **443** and **8443**, plus a private TCP mapping on **17444**. These belong to other services and **must not be reset, modified or replaced**.
- No listener was observed on local backend port **18765** or HTTPS candidate port **10000** at inspection. Revalidate both immediately before use; no future availability is guaranteed.
- Funnel was not enabled for the inspected routes. Do not interpret `tailscale serve status` as public ingress.

## Reference app boundary (implemented in source, not publicly qualified)

- The service still binds **only to `127.0.0.1`**. The only approved candidate external origin shape is `https://<dedicated-node>.ts.net:10000`; the exact tailnet hostname must be verified on the host and cleared for public disclosure before use.
- The `--public-origin` flag opts into strict Host and Origin validation, a bounded thread/turn count and hourly submission cap. Any mismatched hostname, missing or wrong browser Origin, over-quota message, invalid token, oversized body or return-capability replay must fail closed.
- Every first submission is private to the random return-capability holder and OS-protected local owner. No verified external respondent identity; no public owner HTTP endpoint. Private links require care because their path and capability may be visible to the forwarding/TLS provider, browser history or a copied URL.
- The capped stdlib HTTP server remains a **reference candidate**. Before public launch, independent exact-head hostile security review must assess connection exhaustion, abuse/rate enforcement, Windows ACL/backup custody, TLS/Host forwarding, visitor consent and withdrawal, stored-data privacy and outage recovery.

## Safe validation sequence — no public ingress

1. On the actual host, read-only check `tailscale version`, `tailscale status --json`, `tailscale serve status`, `tailscale funnel status`, the active Free plan, local Python version and local listen ports. Stop if these conflict or expose identifiers not approved for publication.
2. Review and pin the exact God Brain source commit. Install nothing from unreviewed external scripts. Stage a fresh checkout in a distinct, validated folder without touching existing services.
3. Choose a new OS-protected directory/database path, explicitly confirm Windows ACLs are owner-only, and start the app **on loopback** (`--port 18765 --public-origin https://<dedicated-node>.ts.net:10000`). Do not forward a port yet.
4. From the host, exercise GET, form POST, retry, owner reply, return-link GET, wrong Host/Origin, quota saturation, restart persistence and deliberate shutdown **with synthetic test-only conversation data**. Never paste live private tokens into shared logs.
5. Obtain an independent exact-source/security/host-config verdict and Patrick's exact public-go-live authorization. **Only then** enable a dedicated Tailscale Funnel HTTPS listener on port **10000** toward local port 18765, without touching Serve 443/8443. The current CLI supports `tailscale funnel --https=10000 --bg 18765`; confirm command semantics on the installed version before any execution.
6. Independently fetch the public invitation without authenticating; from a separate untrusted client submit a synthetic message, verify it is privately held, then issue a distinct owner reply through the local CLI and retrieve it via the saved capability. Record the exact URL, timestamps and negative tests. An untested listener is **not** a qualified public dialogue channel.

## Rollback without affecting existing services

- Stop **only** the newly staged God Brain process. If an authorized Funnel on port 10000 was enabled, remove **only that exact Funnel route**, verifying the 443/8443 and 17444 tailnet-only Serve routes remain unchanged. **Never use `tailscale funnel reset` or `tailscale serve reset`** on this shared host.
- Do not delete any user conversation database on rollback. Keep its owner-only data untouched unless Patrick explicitly requests a particular deletion.
- Leave the public [GitHub issue #62](https://github.com/thebrazenbeard/god-brain/issues/62) available as a limited, clearly public fallback; it requires GitHub sign-in for inbound comments.

**Status:** Source + tests in preparation. No public Funnel route, owner-authenticated service acceptance, independent reviewer verdict or production-grade privacy/abuse acceptance exists from these steps alone.
