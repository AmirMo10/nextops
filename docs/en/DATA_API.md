# Data, durable workflows, evidence and API

[فارسی](../fa/DATA_API.md) · [Index](INDEX.md)

**Status: conceptual contracts; no migrations, schemas or endpoints are implemented.** Source: master specification sections 11, 16–17 and 20. Field groupings below organize the proposed requirements; exact schema and routes require implementation review.

## Persistence model

PostgreSQL is authoritative. Separate business data from the databases NextOps manages. Define stable IDs, foreign keys, unique constraints, indexes, retention and permission rules for each record group.

| Group | Records and relationships |
|---|---|
| Identity/scope | Organizations, environments, users, roles and scoped grants |
| Inventory | Assets, approved endpoints, capability/version facts and credential references |
| Integration | Connector registrations, versions and tool capabilities |
| Workflow | Incidents/events, runs, steps, durable jobs, leases and checkpoints |
| Evidence | Source references, asset/scope, observed/collected times, sanitized content reference and freshness |
| Actions | Proposals, approvals, execution attempts and verification outcomes |
| Knowledge | Documents/chunks/embeddings, conversations, incident memory, topology nodes/edges |
| Governance | Audit and model/prompt/policy/release versions |

Conceptual relationships: an organization contains environments and scoped users; an environment contains assets; an incident relates to affected assets and workflow runs; runs contain steps and evidence; a proposal relates to an exact target/action and possibly an approval; each execution attempt points to its proposal and verification evidence. Audit records reference the relevant actor, target and operation. This is not an executable ER schema.

Use UTC internally, preserving source timezone, collection time and clock-skew uncertainty. Permission-sensitive data must carry scope. Restrict database roles so API/planning code cannot forge execution approvals through unrestricted database writes.

## Durable workflow

```text
RECEIVED -> AUTHORIZED -> SCOPED -> PLANNED
  -> COLLECTING -> ANALYZING -> PROPOSAL_READY
  -> AWAITING_APPROVAL -> READY_TO_EXECUTE -> EXECUTING
  -> VERIFYING -> COMPLETED

Other outcomes: DENIED, EXPIRED, CANCEL_REQUESTED, CANCELLED,
FAILED, OUTCOME_UNKNOWN, MANUAL_RECONCILIATION_REQUIRED
```

Read-only investigations skip change approval, not authorization or audit. Persist progress around external effects. Use transactional job creation/outbox where necessary, leases/heartbeats and duplicate detection. Do not claim exactly-once execution across a device and PostgreSQL. Reconcile a possibly executed mutation before retry. Local cancellation does not guarantee remote cancellation.

Bound elapsed time, LLM calls/tokens, tool calls/bytes, fan-out and retries. The specification's six LLM calls and twenty tool calls are starting experiments, not measured optimal limits.

## Evidence, retrieval and topology

Store provenance, source version, source and collection timestamps, content hash, authorization scope and redaction/partial-result markers. Filter by permission before retrieval and when serving evidence. A historical incident is not proof of current state. Keep raw monitoring history in its source system where practical.

Start topology with relational edges carrying relationship type, origin, freshness and observed/inferred status. Re-index changed documents only. Track chunk and embedding model versions/dimensions; an embedding switch requires index compatibility work. Cached retrieval remains scope- and freshness-aware.

RCA output separates symptoms, collected evidence, possible causes, supporting and contradictory evidence, confidence with justification, unknowns, next safe diagnostic step and proposed action/risk/approval/verification. Only call a cause verified when supported. Do not generate unsupported numeric probabilities.

## Proposed API behavior

Use the `/api/v1` namespace for chat, runs, agents, connectors, devices, incidents, evidence, approvals, audit, users, roles, settings and models. Preserve old paths through an explicit compatibility decision if existing code is later imported. Liveness/readiness endpoints disclose no sensitive public diagnostics.

A long request creates a durable run and returns its ID. Authenticated progress streaming supports reconnection; cancellation is a request, not proof of halted remote work. Define pagination, bounded payloads, idempotent command submission and structured errors. Browser timeouts never erase jobs.

Alert ingress validates payloads, authenticates scoped senders, applies replay/deduplication and rate limits, and routes malformed input for manual review. Anonymous input must not trigger arbitrary operations. No direct browser route to inference or connectors is permitted.
