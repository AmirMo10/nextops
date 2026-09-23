# Data, durable workflows, evidence and API

[فارسی](../fa/DATA_API.md) · [Index](INDEX.md)

**Status: Stage 1A durable foundation plus the deployed Stage 1D live-investigation linkage and a
source-tested, not-yet-deployed Phase 2A incident-context read.**
Source: master specification sections 11, 16–17 and 20. The implemented subset is deliberately
local, single-organization and read-only. General model-only answers remain separate; live Zabbix
investigations now use the existing durable run and append-only audit model.

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
| `GET /api/v1/assistant/ready` | bearer | Returns bounded local inference readiness without exposing its service credential |
| `POST /api/v1/assistant/generate` | bearer | Returns a model-only general answer with no monitoring evidence |
| `GET /api/v1/monitoring/summary` | bearer plus server-derived `zabbix.read` scope | Retrieves the current bounded read-only Zabbix summary |
| `GET /api/v1/monitoring/incident-context` | bearer plus server-derived `zabbix.read` scope | Retrieves the configured host's bounded current summary, recent numeric history and trigger events; source-tested, not yet deployed |
| `POST /api/v1/investigate` | bearer | Creates a durable scoped run, retrieves bounded evidence, generates locally, then atomically stores the result/evidence hash and completion audit |
| `POST /api/v1/runs` | bearer plus `Idempotency-Key` | Authorizes and persists one read-only fixture run, leases it, and returns its explicit fixture result |
| `GET /api/v1/runs/{run_id}` | bearer | Reads only within the actor's server-derived organization/environment scope |

Passwords use Argon2id. Session and lease tokens are opaque, returned once, and stored as
hashes. A reused idempotency key returns the same run only for identical canonical intent;
changed intent returns a conflict. Expired worker leases can be reclaimed after restart.
Required state and audit writes share transactions, so audit/database failure cannot
produce reported success. Errors have stable codes, message keys, retryability, details,
and a correlation ID.

The original fixture result remains explicit, stale and non-live. A live investigation creates its
run before contacting the connector or model. Successful completion stores the bounded
`MonitoringSummary`, its canonical SHA-256 and `run-evidence:<run_id>` reference, the typed local
model result, scope identifiers and the matching completion-audit ID in the run result. The state
change and append-only audit insert share one transaction. Safe failure code, message key and
retryability are stored and audited without raw dependency responses. The API and panel expose the
run/evidence/audit identifiers, and scoped run retrieval returns the same durable result.

`MonitoringSummary` now carries `is_partial` plus bounded, machine-readable `partial_reasons`.
Current reasons distinguish a truncated metric selection, a problem page that reached its result
limit, and absence of usable measurements. The marker and reasons are included in the canonical
evidence hash, durable result and completion audit. Every source-controlled string remains
untrusted content: authentication establishes where the observation came from, not permission for
instructions embedded in a host, metric, value, unit or problem name. Staleness remains a separate
per-measurement flag because a freshly fetched summary can contain old source values.

`MonitoringIncidentContext` is the additive Phase 2A transport contract. It fixes the target to the
connector's configured host, bounds the lookback and list sizes, preserves source timestamps, and
uses explicit partial reasons. This first increment intentionally does not create a new durable run,
send the context to the model or expose it in the browser workflow; those gates require controlled
deployment and acceptance evidence.

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

The implemented routes above use `/api/v1`. Agents, connector/device administration, incidents,
separate evidence and audit browsing, approvals, user/role administration, settings, streaming,
pagination, cancellation, and alert ingress remain planned rather than implemented.
Preserve old paths through an explicit compatibility decision if existing code is later
imported. Liveness/readiness endpoints disclose no sensitive public diagnostics.

A long request creates a durable run and returns its ID. Authenticated progress streaming supports reconnection; cancellation is a request, not proof of halted remote work. Define pagination, bounded payloads, idempotent command submission and structured errors. Browser timeouts never erase jobs.

Alert ingress validates payloads, authenticates scoped senders, applies replay/deduplication and rate limits, and routes malformed input for manual review. Anonymous input must not trigger arbitrary operations. No direct browser route to inference or connectors is permitted.
