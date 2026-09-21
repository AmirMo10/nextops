# Tasks: Stage 1A Increment 2 durable local app

## Task 1: define durable contracts and schema

**Acceptance criteria:**

- [x] Strict contracts cover identity, sessions, runs, leases, audit, and bilingual result
  provenance without accepting client-supplied actor context.
- [x] SQLAlchemy metadata and an Alembic baseline define all required tables, foreign
  keys, scoped uniqueness, checks, indexes, and append-only audit behavior.
- [x] PostgreSQL roles separate migration, application, and read-only support access.

**Verification:** red/green unit tests plus Alembic metadata inspection.

**Files:** `packages/nextops/contracts`, `packages/nextops/persistence`, `migrations`,
`tests/unit`.

## Task 2: implement durable identity and run services

**Acceptance criteria:**

- [x] Bootstrap is one-time; recovery rotates credentials and revokes prior sessions.
- [x] Password and bearer-token storage is non-reversible and comparison is constant-time.
- [x] Revoked/expired/cross-scope actors are denied.
- [x] Run creation is idempotent for identical intent and conflicts for changed intent.
- [x] Worker leases are atomic, renewable by their owner, and recoverable after expiry.
- [x] Required audit failure prevents an operation from reporting success.

**Verification:** service tests followed by real PostgreSQL transaction/concurrency tests.

**Dependencies:** Task 1.

**Files:** `packages/nextops/application`, `packages/nextops/security`, `tests/unit`,
`tests/integration`.

## Task 3: expose the minimal authenticated API

**Acceptance criteria:**

- [x] All stateful endpoints are versioned under `/api/v1` and use structured errors.
- [x] Actor context comes from an opaque authenticated session, never the request body.
- [x] A fixture-backed run result supports `en` and `fa` and labels source, time, scope,
  partial/stale state, typed errors, and audit reference.

**Verification:** ASGI API tests for happy, denied, invalid, replay, and degraded paths.

**Dependencies:** Task 2.

**Files:** `packages/nextops/api`, `tests/api`.

## Task 4: prove PostgreSQL and recovery behavior

**Acceptance criteria:**

- [x] Baseline upgrade and downgrade work on isolated PostgreSQL.
- [x] Constraints, restricted grants, append-only audit, idempotency, leases, restart
  recovery, and transaction rollback are exercised against PostgreSQL.
- [x] No skipped database test is counted as acceptance evidence.

**Verification:** container-backed PostgreSQL integration suite and recorded exact output.

**Dependencies:** Tasks 1–3.

**Files:** `tests/integration`, test configuration, project-state evidence.

## Task 5: publish the server-start handoff

**Acceptance criteria:**

- [x] Paired English/Persian checklists state what the operator can collect now, what
  needs a separate provisioning approval, and what must wait for application release.
- [x] Project state, traceability, indexes, next task, and deployment dossier match only
  tested implementation.
- [ ] Full quality, lock, audit, documentation, and secret-review gates pass before merge.

**Verification:** documentation checker, repository diff review, dependency audit, and
reviewable branch/PR checks.

**Dependencies:** Tasks 1–4.

**Files:** paired docs, repository-control records, `deploy/server-dependencies/nextops-app.yaml`.
