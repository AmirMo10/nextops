# Phased roadmap and acceptance gates

[فارسی](../fa/ROADMAP.md) · [Start here](START_HERE.md) · [Index](INDEX.md) · [G10 server plan](SERVER_PLAN.md)

**Status: the sequence is accepted and the controlled Phase 2 implementation is deployed and qualified across four guests.** Four fixed targets now combine bounded Zabbix history/events with direct read-only Linux snapshots in a durable bilingual local-CPU investigation. Live API, restart, rollback, server/API WAN denial, authenticated browser, serial reboot and dependency-recovery checks pass. This is not production acceptance; independent backup, WAL/PITR and disaster recovery remain open. The [release manifest](../status/current-release.yaml) and [project state](../PROJECT_STATE.md) are authoritative.

**Phase 1 delivered the first Zabbix answer; Phase 2 now adds bounded direct Linux evidence.** The archived prompt is unchanged; older Phase-2-first-answer wording is superseded.

**Phase 2 implementation and qualification are complete for controlled user testing.** Application
release `nextops-0.1.0-54c8bb4` and connector release `nextops-0.1.0-e2dad3a` combine the bounded authenticated Zabbix incident context with fixed-target,
forced-command Linux snapshots, durable audit/evidence linkage and bilingual model output. Source
CI, live English/Persian API requests, service restart, rollback, guarded WAN isolation,
authenticated browser, serial reboot and dependency recovery pass.

## Create these VMs first

After separate provisioning authorization, create **`nextops-app` → `nextops-ai` → `nextops-connectors-ro`**. Their proposed allocations are respectively **8/32/200**, **24/128/500** and **4/8/80**, expressed as vCPU / RAM GiB / disk GiB. Total: **3 VMs, 36 vCPU, 168 GiB RAM and 780 GiB disk**. PostgreSQL initially runs as a separate restricted service inside the app VM. Do not create the dedicated database or write-execution VM yet.

The [startup guide](START_HERE.md) separates VM creation, software implementation and service restart order. Reuse a suitable authorized LAN Zabbix when available. For the selected new-server path, prepare the dedicated 4-vCPU / 16-GiB / 200-GiB `zabbix-server` before 1C. The combined initial profile is 4 VMs / 40 vCPU / 184 GiB RAM / 980 GiB disk; do not add the older small lab as well. These are planning budgets, not free-capacity measurements or a measured monitoring capacity claim.

## Overall phases

| Phase | Deliverable | NextOps VMs on one G10 | Exit evidence |
|---|---|---:|---|
| 0 — Remaining preflight and design | Preserve repository work; reuse supplied hardware/build; check free capacity, storage, network/recovery access, VM compatibility, Zabbix access, workload goals, threat model and offline artifact plan | 0 new | Owner approves architecture and provisioning plan; unavailable facts stay explicit. Do not request the already supplied CPU/RAM totals or ESXi build again. |
| 1 — Safe foundation and Zabbix status MVP | Complete 1A–1E below, including local identity, database, audit, durable work, CPU model, read-only Zabbix and a minimal answer interface | 3 | New Persian/English status questions produce evidence-linked local answers with WAN blocked; ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 cases pass. |
| 2 — Linux/Zabbix incident explanation | Bounded history/events and direct Linux diagnostics enrich the existing status flow | 3 | Simulator and authorized lab investigations; restart/offline checks; mutations disabled. |
| 3 — Network and observability | Windows, Cisco, Juniper, Grafana and evidence-linked inventory/topology; recommended database separation | 4 recommended | Versioned contracts, scoped lab tests and isolated connector failures; database migration and recovery tested. |
| 4 — Firewalls | FortiGate and Sophos VPN/routing/policy diagnostics | 4 | Verified API/version limits, cross-device evidence and no unapproved changes. |
| 5 — Databases and virtualization | SQL Server, MySQL/MariaDB and ESXi | 4 | Read-only identity/query controls and documented version/license limits. |
| 6 — Knowledge and RCA | Incident memory, local retrieval, topology correlation and stronger bilingual evaluation | 4 | Held-out quality results, freshness/scope controls and measured CPU budgets. |
| 7 — Controlled remediation | Reviewed runbooks, exact-action approval, verification, reconciliation and rollback; separate write executor | 5 if enabled | Replay, time-of-check/time-of-use and unknown-outcome tests; authorized lab sign-off before production mutations. |
| 8 — Production qualification | Hardened deployment, complete UI/docs, offline bundle, release/rollback and independent backup/restore drill | 5 with remediation; 4 read-only | Reviewed readiness checklist, measured operating envelope and RPO/RTO, accepted single-host risks. |

Counts cover one serving environment, not physical hosts or connector families. Existing Zabbix/managed systems, temporary tests and independent backup destinations are separate. The fourth VM is recommended for database lifecycle/access isolation, not a measured throughput need; a small reviewed read-only pilot may remain on three under the exception in [SERVER_PLAN](SERVER_PLAN.md). Adding a connector does not automatically add a VM.

## Phase 1 work packages

| Stage | Primary VM and work | Exit checkpoint |
|---|---|---|
| **1A — Application and safety foundation** | Create app VM first; implement typed contracts, local identity/scopes, PostgreSQL/migrations, durable requests, audit, minimal UI/API and deny-by-default policy using fixtures | Local login/state work; policy/audit/denial tests pass before real target credentials are used. |
| **1B — Local CPU service** | Create AI VM second; import one reviewed model/runtime, enforce service authentication and budgets, verify CPU execution and offline loading | Fresh Persian/English local answers and recorded latency/resource measurements; not yet a Zabbix completion result. |
| **1C — Zabbix evidence** | Create read-only connector VM third; gateway plus isolated runner, restricted token, named allowlisted reads, deterministic aggregation and evidence provenance | Real scoped API evidence; correct counts and freshness; denied writes/unsupported methods; sanitized audit. |
| **1D — End-to-end answer** | Join the app, connector and model flow using the same three VMs | A new question returns a readable answer matching captured Zabbix facts with scope, timestamps and references. |
| **1E — Offline acceptance** | Block Internet for the test workloads and fresh browser while preserving approved LAN routes; exercise startup, failure and bounded-load cases | Recorded ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 outcomes, including fresh local login and authorized cold-start/reboot checks. |

Phase 0, the controlled Stage 1A–1E path and the Phase 2 implementation have evidence recorded in
[PROJECT_STATE](../PROJECT_STATE.md). Three Phase 2 acceptance exercises remain explicit there. The
next development phase requires an approved independent destination, PostgreSQL-aware backup/WAL,
file-artifact recovery and independent-host PITR. Later phases remain unaccepted unless an
evidence-backed entry says otherwise. Contracts, scaffolding, raw JSON, cached answers or simulators
alone never complete an acceptance gate.

Advanced RAG, direct Linux SSH, a full dashboard and the other ten connector families must not delay the first Zabbix status answer. Separate API connectivity, monitored-host state and monitoring-engine health. The model must not invent counts, live observations or missing self-monitoring data.

## Explicit revisions and unchanged safeguards

Security and local CPU inference belong in the foundation, not late phases. All eleven integrations remain in scope as tested complete flows. PostgreSQL is authoritative initially; alternative internal backends remain tracked. External AI is disabled. Admin does not bypass safeguards. Root-cause claims require evidence. One G10 is one failure domain. See [ADRs](../adr/README.md) and [traceability](../requirements/TRACEABILITY.md).

The owner's Zabbix-first clarification moves original requirement 17 into Phase 1 and extends it in Phase 2. This startup revision adds 1A–1E and fixes the stale 44-vCPU initial total in NEXT_TASK to **36**; it does not enlarge the VM allocations or modify the archived prompt. The [hardware record](../requirements/HARDWARE_BASELINE.json) and [ESXi supplement](ESXI_BASELINE.md) supersede old 90-CPU/1-TB and unknown-build assumptions.

## Done and next action

Every increment needs working typed code, boundary tests with actual outcomes, security review, Persian/English documentation, traceability and a commit. Keep CPU-only execution, credential isolation, bounded work and audit throughout. The [offline contract](OFFLINE_RUNTIME.md) applies to every enabled dependency. Documentation is not proof of implementation or deployment.

Read [START_HERE](START_HERE.md), then continue from the first unfinished checkpoint in [NEXT_TASK](../NEXT_TASK.md). New infrastructure operations still require their applicable authorization. Read-only production pilots and later mutations each require separate approval; missing credentials, workload targets, compatible artifacts, or recovery access are explicit blockers, not invented facts.
