# Data, durable workflows, evidence and API

[فارسی](../fa/DATA_API.md) · [Index](INDEX.md)

**Status: Stage 1A durable foundation implemented; later workflow/evidence domains remain
conceptual.** Source: master specification sections 11, 16–17 and 20. The implemented
subset is deliberately local, single-organization, read-only, and fixture-backed; it has
no target credential or model path.

## Implemented Stage 1A subset

Alembic revision `0001_durable_app` creates PostgreSQL tables for organizations,
environments, targets, identities, opaque sessions, runs, worker leases, and audit events.
Database constraints enforce the single-organization starting boundary, scoped foreign
keys, run idempotency, bounded run/locale states, and lease validity. The migration creates
`nextops_migrator`, `nextops_app`, and `nextops_support_ro` group roles; the application
role can append but cannot update/delete audit records, and a trigger also rejects audit
mutation by a table owner. Deployment login roles and secret delivery remain external
deployment work.

The implemented HTTP surface is:

| Method and path | Authentication | Behavior |
|---|---|---|
| `GET /healthz` | none | Process liveness only; it does not claim dependency readiness |
| `POST /api/v1/bootstrap` | one-time deployment header | Atomically creates the organization, environment, admin, fixture target, audit event, and first session |
| `POST /api/v1/login` | local username/password | Returns an opaque expiring bearer token; only its SHA-256 digest is stored |
| `POST /api/v1/recovery` | protected recovery header | Rotates the admin password/version and revokes every prior session |
| `GET /api/v1/me` | bearer | Returns actor roles/scopes derived from the database session |
| `POST /api/v1/runs` | bearer plus `Idempotency-Key` | Authorizes and persists one read-only fixture run, leases it, and returns its explicit fixture result |
| `GET /api/v1/runs/{run_id}` | bearer | Reads only within the actor's server-derived organization/environment scope |

Passwords use Argon2id. Session and lease tokens are opaque, returned once, and stored as
hashes. A reused idempotency key returns the same run only for identical canonical intent;
changed intent returns a conflict. Expired worker leases can be reclaimed after restart.
Required state and audit writes share transactions, so audit/database failure cannot
produce reported success. Errors have stable codes, message keys, retryability, details,
and a correlation ID.

The first result supports Persian or English and includes organization/environment/target
scope, source method, collection/measurement time, partial/stale flags, typed errors, and
an audit reference. It is marked as stale fixture data and explicitly says no live
connection was made.

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

## Implemented and planned API behavior

The implemented routes above use `/api/v1`. Chat, agents, connectors, devices, incidents,
evidence, approvals, audit browsing, user/role administration, settings, models, streaming,
pagination, cancellation, and alert ingress remain planned rather than implemented.
Preserve old paths through an explicit compatibility decision if existing code is later
imported. Liveness/readiness endpoints disclose no sensitive public diagnostics.

A long request creates a durable run and returns its ID. Authenticated progress streaming supports reconnection; cancellation is a request, not proof of halted remote work. Define pagination, bounded payloads, idempotent command submission and structured errors. Browser timeouts never erase jobs.

Alert ingress validates payloads, authenticates scoped senders, applies replay/deduplication and rate limits, and routes malformed input for manual review. Anonymous input must not trigger arbitrary operations. No direct browser route to inference or connectors is permitted.
