# NextOps project status brief

[فارسی](../fa/PROJECT_STATUS_BRIEF.md) · [Documentation index](INDEX.md) · [Project state](../PROJECT_STATE.md) · [Next task](../NEXT_TASK.md)

Updated: 2026-09-21

This brief is the presentation-ready summary of verified progress and remaining delivery work. The
four Ubuntu 24.04 servers are qualified and prepared at the operating-system package layer, and the
local CPU inference runtime and model have passed a bounded authenticated smoke test. Product
services are intentionally stopped while production configuration, integration, recovery, and
offline acceptance remain open.

## Executive position

NextOps has moved beyond architecture-only planning. The repository contains tested application
and inference foundations, all four role servers have passed a sanitized qualification, the required
native packages are installed, and the pinned local model has generated fresh Persian and English
responses on the AI server. The project is not yet a working production deployment: no production
database or Zabbix instance has been initialized, the application and connector are not deployed,
and the required Internet-blocked end-to-end acceptance has not run.

## Status at a glance

| Workstream | Current status | Verified result | Remaining acceptance |
|---|---|---|---|
| Architecture and governance | Accepted baseline | Phase 0 and ADRs 0001–0006 accepted; four-server, CPU-only, read-only-first architecture recorded | Continue operation-specific approvals and keep private deployment evidence outside Git |
| Application foundation | Implemented and tested in source | Identity, sessions, policy, PostgreSQL migrations, durable runs and leases, append-restricted audit, authenticated API, and bilingual fixture flow | Package and deploy the release; initialize the production database; add TLS, browser UI, backup, restore, and deployment acceptance |
| Four Ubuntu servers | Qualified and package-prepared | Ubuntu 24.04.5 LTS, healthy systemd, UFW active, SSH-only wildcard listener, expected resources and role packages | Install reviewed service configuration, initialize stateful services, and perform service-level acceptance |
| Local CPU inference | Artifact-prepared with smoke evidence | Pinned llama.cpp build and Qwen model verified by hash; authenticated loopback smoke test cold-started in 7 seconds and returned English and Persian readiness results | Deploy the reviewed systemd unit; run quality, load, cancellation, failure, restart, rollback, and Internet-blocked tests |
| Zabbix and connector | Package layer only | Zabbix 7.0.30 stack is installed but inactive; connector host has its Python environment and protected service identity | Initialize Zabbix and its PostgreSQL database; create a restricted API reader; deploy and test the read-only connector |
| End-to-end offline milestone | Not yet demonstrated | Contracts, safety boundaries, and test cases are documented | Prove a fresh Persian and English question can use current Zabbix evidence and local CPU generation with WAN access blocked and a complete audit record |

## Work completed

### Architecture requirements and safety boundaries

- The owner accepted Phase 0, the Stage 1A–1E delivery path, and ADRs 0001–0006.
- The initial deployment is four virtual machines: application, local AI, read-only connectors, and
  dedicated Zabbix. The approved starting budget is 40 vCPU, 184 GiB RAM, and 980 GiB virtual disk.
- Local CPU generation is mandatory. The system has no GPU dependency and no cloud inference
  fallback. The model never receives infrastructure credentials or authority to approve actions.
- Phase 1 remains read-only. Later changes require deterministic policy, exact-operation approval,
  isolated execution, and audit.

### Repository and application foundation

- The Python project is locked and provides typed domain and application boundaries.
- Stage 1A implements Argon2id bootstrap, login and recovery; opaque hashed sessions; server-derived
  organization, environment, role and scope; PostgreSQL and Alembic migrations; idempotent durable
  runs; expiring worker leases; append-restricted audit; and an authenticated FastAPI surface.
- Stage 1B implements a runtime-neutral `LLMProvider`, authenticated inference boundaries, a
  loopback llama.cpp adapter, one-active/two-queued scheduling, bounded input and output, timeout and
  cancellation handling, safe readiness, and explicit overload or dependency failures.
- Four schema-validated deployment dossiers and guarded role installers define the public handoff
  without storing private addresses, credentials, fingerprints, or raw operational logs in Git.

### Server qualification and package preparation

- All four clean replacement guests passed SSH host-key verification, key-only authentication,
  direct-root denial, resource and mount checks, time synchronization, VMware Tools checks, and
  system health review.
- Each guest reports Ubuntu 24.04.5 LTS, no failed unit, no pending update or reboot, active UFW, and
  no wildcard TCP listener other than SSH.
- Packages were installed through the existing strict proxy chain without a broad operating-system
  upgrade. Automatic service startup and automatic PostgreSQL cluster creation were blocked.
- The application host has PostgreSQL 16.15 and Nginx 1.24. The AI host has GCC 13.3, CMake 3.28,
  Ninja 1.11, OpenBLAS 0.3.26, and uv 0.12.17. The connector host has Python 3.12 virtual-environment
  support. The monitoring host has Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24, PHP 8.3.6, the
  frontend, SQL scripts, and Agent 2.
- Protected non-login service identities and role directories exist. Product, database, and web
  services remain inactive and disabled by design.
- Docker was not installed because the current native systemd design does not require it and a
  container socket would expand the trust boundary.

### Local CPU model evidence

- The pinned llama.cpp revision was built in Release mode with native CPU settings, OpenMP, and
  OpenBLAS. It has no GPU linkage, and the promoted binary checksum is recorded in the inference
  manifest.
- The pinned `Qwen3-8B-Q4_K_M.gguf` artifact is 5,027,783,488 bytes. Its SHA-256 matched before and
  after promotion to the protected model volume.
- A temporary authenticated service bound only to loopback, used one slot, an 8K context, zero GPU
  layers, and no Web UI. It cold-started in 7 seconds, returned `READY` in 630 ms and `آماده` in
  1,431 ms, then stopped cleanly without a residual process or listener.
- This is bounded smoke evidence. It is not a quality benchmark, sustained-load test, production
  service acceptance, or proof of operation with Internet blocked.

### Verification completed

- Repository formatting, lint, strict typing, documentation, deployment-dossier, inference-artifact,
  and installer validation passed for the reviewed revision.
- The desktop suite passed 71 non-integration tests, with five database tests skipped because no
  local PostgreSQL URL was supplied.
- On the application server, the same revision passed formatting, lint, strict typing, all 71
  non-integration tests, and all five PostgreSQL integration tests against a temporary isolated
  PostgreSQL 16.15 cluster. The cluster was removed after the test.

## Work remaining

### Stage 1B production inference service

Create and review the root-owned configuration and secret references, install the `nextops-ai`
systemd unit, retain loopback-only binding, apply CPU and memory controls, and verify authenticated
health, restart, logging, overload, cancellation, timeout, and rollback behavior. Run a versioned
Persian and English evaluation with recorded quality, latency, token, memory, CPU, thread, and queue
measurements. Repeat cold-start testing with Internet blocked and approved LAN access retained.

### Stage 1A application deployment

Package an offline application release, initialize PostgreSQL 16 on the dedicated mount, create
least-privilege roles, run migrations, bootstrap local identity, deploy the API and worker services,
and configure Nginx and TLS. Complete the browser interface, secret delivery, backup, restore, and
rollback tests before calling the application deployable.

### Zabbix prerequisite

Initialize the Zabbix PostgreSQL database on its dedicated mount, import the schema, configure
Zabbix Server, Nginx, PHP-FPM, and Agent 2, and establish local administrator recovery. Configure
self-monitoring, validate the initial retention policy against real growth, and create a restricted
read-only API identity. No monitoring service should be exposed beyond its approved network scope.

### Read-only connector and first useful answer

Deploy the gateway and isolated Zabbix runner on the connector server. Give only that runner the
scoped Zabbix token, allow only listed read methods, bound result size and time, compute counts in
code, and treat collected text as untrusted evidence. Then demonstrate a fresh Persian and English
question flowing through current Zabbix evidence, deterministic aggregation, local CPU explanation,
source and observation time, scope, and append-restricted audit.

### Offline and recovery acceptance

Complete Stage 1E with WAN access blocked across all four servers and a fresh client. Prove cold
starts for PostgreSQL, Zabbix, the application, the connector, and the model; fresh local login;
revoked-token and unreachable-target handling; stale-data labeling; low-space behavior; resource
limits; independent backups; restore drills; and release rollback. The documented ZBX-01–ZBX-08
and applicable OFF-01–OFF-10 cases require actual recorded outcomes.

## Recommended delivery sequence

1. Productionize the AI service and complete the Stage 1B bilingual offline evaluation.
2. Package and deploy the application database, API, worker, reverse proxy, TLS, secrets, backup,
   and restore path.
3. Initialize Zabbix and establish the restricted read-only API identity.
4. Deploy the connector and complete live, bounded Stage 1C reads.
5. Demonstrate the evidence-linked Stage 1D answer and complete Stage 1E offline and recovery
   acceptance.

## Presentation conclusion

The infrastructure and software foundations are ready for controlled service deployment. The
project has verified hosts, installed role packages, tested repository foundations, and a working
local CPU model artifact. The remaining work is production configuration, stateful-service
initialization, read-only integration, recovery proof, and full offline acceptance. Until those
gates pass, NextOps must be described as prepared and partially validated, not production-ready.
