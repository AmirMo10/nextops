# Phased roadmap and acceptance gates

[فارسی](../fa/ROADMAP.md) · [Index](INDEX.md) · [G10 server plan](SERVER_PLAN.md)

**Status: proposed sequencing; no software phase is complete. Updated 2026-09-20.** Source: master specification sections 3 and 22–26, mandatory offline contract, and the owner's clarification that the first implementation milestone must end with an AI answer about Zabbix status. Publishing documentation does not approve the architecture or authorize server changes.

**First delivery is now Phase 1: a new question -> authorized read-only Zabbix data -> local CPU-generated answer -> source/time references and audit, with Internet blocked.** Linux enrichment follows in Phase 2. This explicitly supersedes older text that placed the first useful answer in Phase 2; the archived prompt is unchanged.

| Phase | Deliverable | NextOps runtime VMs on one G10 | Exit evidence |
|---|---|---:|---|
| 0 — Discover and design | Repository/host report, threat model, architecture, ADRs, 51-section traceability, workload assumptions and CPU benchmark plan | 0 new | Owner approves architecture/roadmap; unavailable facts remain explicit blockers |
| 1 — Safe foundation and Zabbix status MVP | Conventions/CI, API, PostgreSQL/migrations, local identity/scopes, audit, durable jobs, policy/approval contracts, simulator, CPU harness, real read-only Zabbix adapter and minimal question/answer interface | 3 | A new Persian and English status question produces a local evidence-linked answer with WAN blocked; ZBX-01–ZBX-08, offline startup and denial tests pass in an authorized environment |
| 2 — Linux/Zabbix incident explanation | Add bounded history/events and direct Linux diagnostics to the working status flow | 3 | Fixtures and authorized lab investigations, restart and offline tests; no mutations enabled |
| 3 — Network and observability | Windows, Cisco, Juniper, Grafana, evidence-linked inventory/topology; recommended database separation | 4 recommended | Versioned contracts and simulators; scoped lab tests; isolated connector failures; tested data migration/recovery |
| 4 — Firewalls | FortiGate and Sophos VPN/routing/policy diagnostics | 4 | Version/API limitations verified; cross-device evidence; no unapproved changes |
| 5 — Databases and virtualization | SQL Server, MySQL/MariaDB and ESXi | 4 | Read-only account/query controls and documented version/license limits |
| 6 — Knowledge and RCA | Incident memory, local retrieval, topology-based correlation and stronger bilingual evaluation | 4 | Held-out quality results, freshness and scope controls, measured CPU budgets |
| 7 — Controlled remediation | Small reviewed runbook set, exact-action approval, verification, reconciliation and rollback; isolated write executor | 5 if enabled | Replay/TOCTOU/unknown-outcome tests; lab sign-off before any production mutation |
| 8 — Production qualification | Hardened deployment, complete UI/docs, offline bundle, release/rollback and independent backup/restore drill | 5 with remediation; 4 read-only | Reviewed readiness checklist, measured operating envelope and RPO/RTO, accepted single-host risks |

Counts refer to one serving environment, not physical servers or connector count. They exclude existing Zabbix/managed systems, temporary test VMs and backup destinations. A missing Zabbix instance adds one optional lab VM. The [server plan](SERVER_PLAN.md) defines allocations, optional additions, headroom and the exception under which a small read-only pilot can remain on three VMs. The Phase 3 fourth VM is for data lifecycle/access separation, not proven throughput need.

## Phase 1 increments: the phase must end with an answer

1. Establish typed contracts, local identity, deny-by-default policy, durable state and audit before real target access.
2. Provision one verified CPU model under the approved process, benchmark bounded generation, and test offline loading.
3. Implement the allowlisted Zabbix reads, scoped credentials, deterministic status aggregation and evidence provenance.
4. Connect a minimal web view or authenticated CLI to new Persian/English questions, local generation and source display.
5. Run ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 cases, including fresh login and cold start with WAN blocked. Record actual test outcomes and unresolved deployment gates.

These are increments inside Phase 1, not permission to call the phase complete after scaffolding or a model 'hello world'. Advanced RAG, direct Linux SSH and the other ten integrations do not block the first Zabbix status answer. Distinguish API reachability, monitored-host state and monitoring-engine health.

## Explicit changes to the original fourteen-phase order

Security and local CPU inference move to the foundation, not late phases. Integrations remain in scope but arrive as tested complete flows. PostgreSQL is the initial authoritative backend; alternative internal backends stay tracked. External AI providers are disabled. Admin does not bypass safeguards. Root-cause claims require evidence. Single-host deployments are not high availability. See [ADRs](../adr/README.md) and [traceability](../requirements/TRACEABILITY.md).

The latest owner clarification additionally brings Zabbix-only answers forward to Phase 1. Original requirement 17 is first exercised there and extended by Phase 2; other requirements remain in scope. New VM placements are proposals pending host verification, not claims of provisioned infrastructure.

## Cross-cutting done criteria

Every increment includes typed working code, tests at the real boundary, recorded results, security review, Persian/English documentation, traceability and a commit. All phases retain bounded execution, credential isolation and CPU-only operation. Do not call a phase production-ready merely because its feature exists.

Read-only production pilots and mutation enablement require separate approvals even after lab tests. Dependencies, hardware access, license limits, backups and missing operational targets are explicit blockers rather than guessed facts. The [offline contract](OFFLINE_RUNTIME.md) applies to every enabled component; documented tests are not passing results.

## Immediate next action

Complete [Phase 0 discovery and architecture review](../NEXT_TASK.md) using the new Phase 1 outcome as the first implementation target. The smallest implementation can still start with one testable foundation contract, but the phase must end with the Zabbix answer. Approval to document the repository is not approval to deploy or mutate infrastructure.
