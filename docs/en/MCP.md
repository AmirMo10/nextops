# MCP gateway and connector contracts

[فارسی](../fa/MCP.md) · [Index](INDEX.md)

**Status: proposed contract; no MCP server is implemented.** Source: master specification sections 11–15 and 21.

## Protocol versus application abstraction

A Python method named `execute()` is not an MCP implementation. Use the official maintained SDK with a pinned, tested protocol version: initialization, capability negotiation, tool discovery, typed schemas, results/errors, cancellation and transport behavior. Resolve exact versions at implementation time.

Prefer local stdio for suitably isolated local connectors. Use authenticated Streamable HTTP for independently deployed long-running services when justified. Never expose unauthenticated endpoints; validate origins where applicable. Client identity, MCP sessions, downstream credentials and token audiences are different concerns. Do not blindly pass client tokens to downstream devices.

## Registry and boundaries

Begin with an administrator-controlled registry of reviewed connector manifests. Do not automatically install arbitrary remote MCP servers. Enable only required connectors. Each connector has a version, supported target/version matrix, health information, credential-reference requirements and bounded tool catalog.

The gateway authenticates callers, checks authorization and policy, validates approvals, enforces deadlines and quotas, records audit, routes calls and reports typed failures. Connector runners recheck relevant constraints and reject direct unauthenticated calls. Validate destinations, redirects and resolved addresses against authorized inventory; avoid unrestricted discovery and SSRF-style proxy behavior.

## Planned tool definition

| Field group | Required meaning |
|---|---|
| Identity | Name, version, connector and supported target types |
| Contract | Typed input/output schemas and structured error classes |
| Authorization | Required scope, environment and deterministic risk class |
| Execution | Timeout, byte/row/output limits, concurrency and cancellation behavior |
| Safety | Approval requirement, preconditions, idempotency semantics and verification |

Remote tool descriptions or read-only annotations are untrusted metadata. Policy authority remains in versioned application rules.

## Planned execution request and result

Request: operation ID, authenticated actor/scope, immutable target ID, validated arguments, policy version, optional approval reference, deadline, idempotency key and correlation ID.

Result: status, collection/execution timestamps, sanitized evidence references, partial-result marker, verification outcome and structured authentication/permission/connectivity/vendor errors. A connector without a capability returns an explicit unsupported result, never invented success.

## Bounded execution sequence

```text
Authorize actor and target
  -> validate named operation and arguments
  -> check policy / approval / preconditions / audit availability
  -> record durable intent
  -> execute through scoped connector
  -> persist result or unknown outcome
  -> verify fresh target state when applicable
  -> finish audit and user-visible summary
```

Eligible reads may use bounded retries and backoff. A mutation that timed out may already have executed; mark `OUTCOME_UNKNOWN` and reconcile before another attempt. Cancellation of a local request does not prove a remote command stopped. Connector failure must not crash the whole platform.

## Acceptance

Protocol conformance, invalid input, auth failures, target substitution, cancellation, bounded outputs, partial data, connector crash, replayed approval, duplicate delivery and unknown remote outcomes require tests. Simulators are the default; actual devices require explicit authorization and a documented lab/version record.
