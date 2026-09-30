# OpenAI / VeraMesh Execution-Surface Routing V1

Status: **ARCHITECTURE CANDIDATE / NO RUNTIME EFFECT**

Observed against current OpenAI documentation on 2026-09-24.

## Problem this contract prevents

A healthy private MCP transport does not imply that every OpenAI product surface can discover or invoke that MCP server in the same way.

The following are distinct:

- a VeraMesh Secure MCP Tunnel being healthy;
- a ChatGPT workspace being allowed to register/select that tunnel as a custom app;
- Codex/plugin packaging being able to declare an MCP server;
- the OpenAI Responses API being able to address the tunnel directly.

Do not treat failure of one product-registration surface as failure of VeraMesh transport.

## Canonical programmatic workstation route

For God Brain / VeraMesh machine-control work, the preferred programmatic route is:

```text
authorized operator
    -> OpenAI Responses API
        -> MCP tool with tunnel_id
            -> OpenAI Secure MCP Tunnel
                -> tunnel-client on workstation
                    -> veraport-mcp-stdio
                        -> VeraPort ControllerRuntime
                            -> VeraPortAgent
                                -> workstation
```

OpenAI currently documents `tunnel_id` as the Responses API field for a private MCP server reached through Secure MCP Tunnel. The OpenAI-hosted tunnel endpoint must not be substituted into `server_url`.

Primary evidence:
- https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp

## Surface classification

### Responses API

Role: **canonical programmatic control surface** for private VeraMesh workstation operations.

Properties:

- addresses an existing Secure MCP Tunnel directly by `tunnel_id`;
- does not require a public workstation ingress;
- does not require ChatGPT custom-app discovery to be available;
- supports MCP tool allowlisting;
- supports explicit MCP call approval;
- supports stateless operation when the client uses `store:false` and replays required response output items.

This route still requires an OpenAI Platform API credential and incurs normal API usage charges. Credential creation/use and billable live acceptance are protected effects and remain separately authorized.

### ChatGPT custom MCP app

Role: **optional product UI surface**, not canonical transport or workstation authority.

ChatGPT developer-mode app availability and tunnel discovery are separate workspace/product permissions from the tunnel itself. A tunnel that works through the Responses API may therefore fail to appear in a particular ChatGPT app-registration UI without implying a VeraMesh defect.

Do not make God Brain workstation control depend on this UI.

### Codex/plugin MCP declaration

Role: **Codex/plugin execution surface**.

An MCP declaration bundled with a plugin can be useful where that product surface supports it. Do not infer from successful Codex/plugin loading that normal ChatGPT web has registered the same MCP server as a ChatGPT app.

### Public HTTPS MCP forwarding

Role: **diagnostic/bootstrap fallback only**.

Do not expose Lappy/VeraPort publicly merely to work around ChatGPT app-registration limitations when a healthy Secure MCP Tunnel already exists.

Any temporary public bridge must be:
- explicitly authorized;
- capability/auth protected;
- short lived;
- torn down after the diagnostic;
- excluded from the canonical architecture.

## Authority is layered

Product/tool discovery never grants workstation authority.

The effective permission for an operation is the intersection of:

1. operator-request scope;
2. model-visible `allowed_tools`;
3. Responses API MCP approval state;
4. tunnel association/authorization;
5. VeraPort controller requested capability ceiling;
6. fenced lane claims;
7. workstation local policy and allowed roots;
8. operation-specific process/filesystem policy.

A broader upstream surface cannot expand a narrower downstream authority.

## Credential boundary

- Never put `OPENAI_API_KEY`, tunnel runtime credentials, private keys, or full private tunnel identifiers into repository content, Bus messages, prompts intended for durable publication, or user-visible diagnostic output.
- Prefer environment-only or protected local credential material.
- A tunnel runtime API key used by `tunnel-client` is not the same credential as an OpenAI Platform key used by a Responses API client.
- An operator that reads local VeraMesh tunnel configuration may read `tunnel_id` only; it must not read or propagate the runtime API-key file unless a separate operation explicitly requires it.
- Credential creation, rotation, revocation, provider/permission changes, and billable API execution remain protected effects.

## First live acceptance

The first live Responses API acceptance is intentionally narrow:

1. verify the existing VeraMesh tunnel runtime remains healthy;
2. use the operator `read` profile;
3. keep MCP approval explicit;
4. set `store:false`;
5. expose only the read-profile tool allowlist;
6. request exactly one `machine_info` operation;
7. approve only that exact call;
8. require returned MCP evidence from the expected VeraMesh server;
9. record exact operator/tunnel/runtime provenance without recording secrets.

A successful first acceptance establishes:

`RESPONSES_API -> SECURE_MCP_TUNNEL -> VERAMESH -> LAPPY_READ_PATH`

It does **not** establish filesystem-write qualification, managed-process qualification, unrestricted shell authority, deployment authority, or permission to retire another control channel.

## Process-control gate

Process execution/control is a later independent gate.

Before any build/process profile is used:

- VeraPort process authority must be separately enabled and qualified;
- the exact managed-process implementation must satisfy its current security/review contract;
- process mutation must remain fenced to VeraPort-owned handles/lanes;
- a successful filesystem/read acceptance must not be treated as process qualification.

## Failure routing

When a workstation call fails, classify the layer before changing architecture:

- tunnel runtime unhealthy -> diagnose VeraMesh/tunnel-client;
- Responses API cannot address tunnel -> diagnose Platform org/tunnel authorization;
- MCP tool missing -> inspect `allowed_tools`, controller operations, and downstream authority;
- approval request rejected -> no tool effect occurred;
- ChatGPT custom app cannot list tunnel -> treat as ChatGPT product/workspace registration issue, not VeraMesh transport failure;
- Codex plugin works but ChatGPT web does not -> treat as surface distinction, not transport contradiction;
- public-forwarding workaround fails -> do not replace the private architecture unless the underlying private route is independently shown defective.

## Current implementation binding

Current candidate operator:

- repository: `thebrazenbeard/vera-mesh`
- Draft PR: `#40`
- exact head when this document was authored:
  `fe57945f4886641a48b22e83d94a0f40d211e93e`
- base:
  VeraMesh PR #37 exact head
  `8e886e7859bfc77d6b95a6752aadeea727b489ad`

That candidate is an implementation binding, not canonical God Brain state. Exact-head review semantics still apply.

## Claim ceiling

`SUPPORTED_EXECUTION_SURFACE_ROUTING_CONTRACT_ONLY`

This contract identifies the correct supported route and effect boundaries. It does not create an API credential, incur API cost, enable workstation process authority, perform a live Lappy call, merge a repository branch, or establish deployment qualification.
