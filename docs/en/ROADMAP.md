# Phased roadmap and acceptance gates

[فارسی](../fa/ROADMAP.md) · [Index](INDEX.md)

**Status: proposed sequencing; no software phase is complete.** Source: master specification sections 3 and 22–26. Publishing documentation does not approve the architecture or authorize server changes.

| Phase | Deliverable | Exit evidence |
|---|---|---|
| 0 — Discover and design | Repository/host report, threat model, architecture, ADRs, 51-section traceability, workload assumptions and CPU benchmark plan | Owner approves architecture/roadmap; unavailable facts remain explicit blockers |
| 1 — Safe foundation | Conventions/CI, API, PostgreSQL/migrations, local identity/scopes, audit, durable jobs, policy/approval contracts, simulator and CPU harness | Clean setup/test path; prohibited actions denied; a CPU candidate measured when authorized hardware is available |
| 2 — First complete flow | Persian request, read-only Zabbix history/events and Linux diagnostics, evidence-linked answer, audit and minimal UI | Fixtures and authorized lab flow, restart and offline tests; no mutations enabled |
| 3 — Network and observability | Windows, Cisco, Juniper, Grafana, evidence-linked inventory/topology | Versioned contracts and simulators; scoped lab tests; isolated connector failures |
| 4 — Firewalls | FortiGate and Sophos VPN/routing/policy diagnostics | Version/API limitations verified; cross-device evidence; no unapproved changes |
| 5 — Databases and virtualization | SQL Server, MySQL/MariaDB and ESXi | Read-only account/query controls and documented version/license limits |
| 6 — Knowledge and RCA | Incident memory, retrieval, topology-based correlation and stronger bilingual evaluation | Held-out quality results, freshness and scope controls, measured CPU budgets |
| 7 — Controlled remediation | Small reviewed runbook set, exact-action approval, verification, reconciliation and rollback paths | Replay/TOCTOU/unknown-outcome tests; lab sign-off before any production mutation |
| 8 — Production qualification | Hardened deployment, complete UI/docs, offline bundle, release/rollback and off-host backup/restore drill | Reviewed readiness checklist, measured operating envelope and RPO/RTO, accepted single-host risks |

## Explicit changes to the original fourteen-phase order

Security and local CPU inference move to the foundation, not late phases. Integrations remain in scope but arrive as tested complete flows. PostgreSQL is the initial authoritative backend; alternative internal backends stay tracked. External AI providers are disabled. Admin does not bypass safeguards. Root-cause claims require evidence. Single-host deployments are not high availability. See [ADRs](../adr/README.md) and [traceability](../requirements/TRACEABILITY.md).

## Cross-cutting done criteria

Every increment includes typed working code, tests at the real boundary, recorded results, security review, Persian/English documentation, traceability and a commit. All phases retain bounded execution, credential isolation and CPU-only operation. Do not call a phase production-ready merely because its feature exists.

The first useful operational milestone is Phase 2, not eleven adapters at once. Read-only production pilots and mutation enablement require separate approvals even after lab tests. Dependencies, hardware access, license limits, backups and missing operational targets are explicit blockers rather than guessed facts.

## Immediate next action

Complete [Phase 0 discovery and architecture review](../NEXT_TASK.md). The smallest later implementation should establish one testable foundation contract rather than build the whole platform. Approval to document the repository is not approval to deploy or mutate infrastructure.
