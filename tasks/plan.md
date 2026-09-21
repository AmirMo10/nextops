# Implementation plan: Stage 1A Increment 2 durable local app

## Outcome

Deliver the smallest restart-safe local application slice: one-organization identity
bootstrap and recovery, PostgreSQL-authoritative state, authenticated versioned API,
idempotent run creation and worker leases, append-only audit, and one bilingual fixture
result. No target credential, connector, model, VM, network, or host mutation is in scope.

## Architecture decisions

- PostgreSQL is the only authoritative runtime database; SQLite is not a compatibility
  substitute.
- SQLAlchemy defines persistence mappings and Alembic owns schema changes.
- Authentication uses opaque, expiring bearer sessions stored only as hashes. Passwords
  use a memory-hard password hash; bootstrap/recovery secrets come from deployment
  configuration and never enter Git or application logs.
- The API derives actor organization, environment, roles, and scopes from the validated
  server-side session. Client payloads cannot supply actor context.
- Run idempotency is enforced by a database uniqueness constraint and request-payload
  hash. A reused key with different intent is a conflict.
- Worker lease acquisition is atomic and time-bounded. Expired leases can be recovered
  after restart; live leases cannot be stolen.
- Audit rows are append-only at the application role and every accepted or denied
  security-sensitive path records a stable event. Required audit failure fails the
  operation explicitly.
- The first result is deterministic fixture data in Persian and English. It is not
  presented as live infrastructure evidence.

## Delivery slices

### Slice 1: contracts and migration

- [ ] Add strict identity, session, run, lease, audit, and result contracts.
- [ ] Add SQLAlchemy mappings for organization, environment, target, identity, session,
  run, and audit state.
- [ ] Add an Alembic baseline with constraints, indexes, append-only audit protections,
  and least-privilege PostgreSQL role/grant definitions.
- [ ] Add failing contract/schema tests first, then make them pass.

### Slice 2: durable services

- [ ] Implement password hashing, opaque token hashing, one-time bootstrap, login,
  recovery rotation, revocation checks, and server-derived actor context.
- [ ] Implement atomic run creation with idempotency conflict detection.
- [ ] Implement lease claim/renew/release and expired-lease recovery.
- [ ] Make audit/database failure return a typed failure; never report unlogged success.
- [ ] Cover security boundaries and persistence behavior with focused tests.

### Slice 3: authenticated API and fixture result

- [ ] Add a `/api/v1` FastAPI application with health, bootstrap, recovery, login,
  current-actor, run-create, run-read, and worker-lease boundaries.
- [ ] Return consistent structured errors with correlation identifiers.
- [ ] Return one deterministic Persian/English fixture result with source, collection
  and measurement time, scope, partial/stale flags, typed errors, and audit reference.
- [ ] Verify unauthenticated, revoked, cross-scope, invalid, duplicate, and degraded cases.

### Slice 4: PostgreSQL and operational proof

- [ ] Run upgrade/downgrade, constraint, role, audit append, idempotency, lease,
  restart-recovery, and rollback/recovery tests against isolated real PostgreSQL.
- [ ] Run Ruff, strict mypy, pytest, documentation checks, frozen install, dependency
  audit, and a staged secret review.
- [ ] Record exact pass/fail/blocked evidence; do not count skipped PostgreSQL tests as
  acceptance.

### Slice 5: deployer handoff and project state

- [ ] Add paired English/Persian server-start checklists that distinguish safe preflight,
  separately authorized provisioning, and not-yet-deployable application steps.
- [ ] Update indexes, traceability, project state, next task, and the app deployment
  dossier only for capabilities that actually exist and were tested.
- [ ] Commit small verified slices, publish a review branch, and merge only after required
  checks pass.

## Checkpoints

- Contract checkpoint: boundary validation and migration metadata tests pass.
- Persistence checkpoint: the real PostgreSQL suite proves constraints, roles,
  idempotency, leases, audit, restart behavior, and migration rollback.
- API checkpoint: authentication and actor derivation are server-side and the fixture
  response is explicit about provenance and limitations.
- Handoff checkpoint: deployers have exact starting actions without any implied authority
  to provision or install.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Bootstrap endpoint remains usable after first setup | Critical | Database singleton guard, configured one-time secret, conflict after bootstrap |
| Stolen session token is reusable | High | Store only token hash, expire sessions, support revocation and recovery-wide rotation |
| Duplicate retry creates two runs | High | Transaction plus scoped unique constraint and canonical request hash |
| Worker restart strands work | High | Expiring database lease with atomic compare-and-set semantics |
| Audit write fails after state change | High | State mutation and required audit append share one transaction |
| Tests silently use SQLite semantics | High | PostgreSQL-only integration suite; blocked means blocked, never accepted |
| Server checklist is mistaken for approval | High | Explicit authority gates and non-executable placeholders for private inputs |

## Open gate

The workstation has Docker installed but the Docker engine is currently stopped. Real
PostgreSQL acceptance remains open until the engine is available or another isolated
PostgreSQL endpoint is explicitly supplied. This does not authorize starting services on
the target servers.
