# Architecture and repository structure

[فارسی](../fa/ARCHITECTURE.md) · [Index](INDEX.md)

**Status: proposed.** Source: [master specification](../requirements/NEXTOPS_MASTER_PROMPT.md), sections 2–8, 16–20. The repository currently contains documentation, not the services below.

## Decision

Use a modular control plane, a durable workflow worker, a protected execution gateway, isolated enabled connectors, and one dedicated local CPU inference service. A module is a code boundary; it need not be a microservice. Separate processes where credentials, network reachability, or resource isolation demand it.

```text
User / CLI / alert sender
          |
   TLS reverse proxy
          |
   FastAPI + web console
          |
   Persisted workflow worker
     |            |              |
 CPU model   Scoped retrieval   Trusted policy
                                  |
                           MCP execution gateway
                                  |
                         Target-scoped connectors
                                  |
                         Authorized infrastructure

PostgreSQL <-> durable jobs / incidents / approvals / audit / topology
Restricted storage <-> sanitized evidence / verified model files
```

## Responsibilities and enforceable boundaries

| Component | Owns | Must not receive/do |
|---|---|---|
| Web/API | Sessions, input validation, inventory views, run submission | Raw target credentials or direct connector access |
| Workflow worker | Bounded planning, evidence collection, checkpoints | Self-granted permissions or gateway bypass |
| CPU inference | Language understanding and evidence synthesis | Target credentials, arbitrary Internet calls, management-network access |
| Policy | Versioned deterministic permissions, risk and approval rules | Model-controlled privilege changes |
| Gateway | Authentication, policy recheck, audit, limits, execution routing | Unauthenticated direct execution |
| Connector | One integration's authorized operations and credentials | Unrestricted discovery or unrelated targets |
| PostgreSQL | Authoritative business/workflow state | A shared superuser account for all components |

Use service identities, scoped database roles, network controls, filesystem permissions, and execution-boundary checks to make these restrictions real. A diagram alone does not enforce isolation.

## Starting stack, not locked dependencies

Python 3.12 is a proposed baseline with FastAPI and Pydantic. PostgreSQL, SQLAlchemy and Alembic handle state and migrations. A PostgreSQL-backed job system is preferred initially; Redis is optional only after a measured need. React, TypeScript and Vite are the proposed frontend. Local lexical retrieval and optionally pgvector support evidence search. Generation uses a pinned CPU build of llama.cpp; embeddings use a separately evaluated local CPU model.

Implementation must verify compatible versions and commit dependency locks, image digests, model revisions and checksums. No package in this document is implied to be installed. PostgreSQL is the initial production backend; alternate internal MySQL/SQLite backends remain tracked rather than falsely presented as equivalent.

## Planned source layout

```text
apps/
  api/                  # HTTP composition root
  worker/               # durable workflow process
  mcp_gateway/          # separately protected execution entrypoint
  web/                  # bilingual operations console
packages/nextops/
  domain/               # entities/invariants; no framework I/O
  application/          # use cases and ports
  contracts/            # typed requests/events/tool schemas
  policy/               # authorization and approval rules
  inference/            # local CPU providers and budgets
  knowledge/            # evidence, retrieval, memory, topology
  connectors/           # base + eleven integration families
  infrastructure/       # repositories, jobs, secret adapters
  observability/
  localization/
migrations/
config/                 # sanitized examples, never credentials
deploy/                 # compose, systemd, reverse-proxy
scripts/                # reviewed lifecycle/benchmark/recovery tools
tests/                  # unit, integration, contract, security, e2e
evals/                  # versioned bilingual cases and rubrics
benchmarks/             # scenarios and sanitized measurements
docs/                   # requirements, ADRs, English/Persian guides
```

Only create implementation directories when they contain real code or contracts. Define packaging/import roots explicitly. Infrastructure implements domain/application ports, never the reverse. Avoid one giant agent module, broad utility modules and untyped cross-module dictionaries.

## Single-host deployment

Separate development, staging and production credentials, inventories, databases, volumes and ports. All environments still share one host failure domain. Expose only the reverse proxy to intended users; keep inference, database, MCP and telemetry administration internal. Proposed configurable data paths are `/srv/nextops/models`, `/var/lib/nextops`, and `/etc/nextops`; verify actual mounts and ownership first.

Compose and systemd must follow the same contracts with documented limitations. Do not introduce Kubernetes, Kafka, a service mesh, another workflow engine or a graph database without an ADR demonstrating a current requirement. Off-host backups and an access-recovery plan are production gates, not optional decorations.
