# Documentation index

[فارسی](../fa/INDEX.md) · [Home](../../README.md) · [Start here](START_HERE.md)

**Updated: 2026-09-20. Status: proposed design and documentation, not proof of a working deployment.** The active master prompt is English; the original Persian specification remains in the preserved v2 archive.

> **Current new-server profile:** three NextOps VMs plus `zabbix-server` (4 vCPU / 16 GiB / 200 GiB) = **4 VMs / 40 vCPU / 184 GiB RAM / 980 GiB virtual disks**. Do not add the earlier small lab VM as well. [START_HERE](START_HERE.md) defines the order and Stage 1A–1E; [ZABBIX_SERVER](ZABBIX_SERVER.md) defines the monitoring VM, LVM and read-only integration.

> **Mandatory constraint:** local CPU answers, fresh local login and cold restart must work without Internet. Read [OFFLINE_RUNTIME](OFFLINE_RUNTIME.md) before choosing dependencies. GitHub is not a runtime service.

> **First outcome:** a real, evidence-linked local answer about authorized Zabbix status with WAN blocked. Linux enrichment follows in Phase 2. Prepare the dedicated Zabbix server before Stage 1C live reads, or reuse an existing suitable authorized local instance.

## Reading paths

Begin with [START_HERE](START_HERE.md), [ZABBIX_SERVER](ZABBIX_SERVER.md) and the [deployment amendment](../requirements/DEPLOYMENT_UPDATE.md). Then review the [roadmap](ROADMAP.md), [offline contract](OFFLINE_RUNTIME.md), [storage controls](../STORAGE_PLAN.md), [server plan](SERVER_PLAN.md), [ESXi baseline](ESXI_BASELINE.md), architecture and security. Earlier three/four/five-VM tables count NextOps only; the current inclusive profile is in the Zabbix guide.

| Guide | Contents |
|---|---|
| [Phase 0 report](PHASE_0_REPORT.md) | Repository findings, architecture, gaps, threat summary, resource plan and the approval checkpoint |
| [Start here](START_HERE.md) | Creation order, four-VM profile, Phase 1A–1E, boundaries and restart dependencies |
| [Dedicated Zabbix server](ZABBIX_SERVER.md) | 4 vCPU / 16 GiB / 200 GiB, detailed LVM, software, retention, read-only API, self-monitoring and combined budgets |
| [Offline operating contract](OFFLINE_RUNTIME.md) | New local answers, cold start/login, hidden dependencies, LAN boundaries and OFF-01–OFF-10 |
| [G10 server plan](SERVER_PLAN.md) | NextOps-only phase counts, trust placement and ZBX-01–ZBX-08; current dedicated Zabbix supersedes old lab examples |
| [ESXi baseline](ESXI_BASELINE.md) | Supplied build/CPU sample, reference mappings, guest ISA, topology and patch-review gates |
| [Diagram atlas](DIAGRAMS.md) | Context, deployment, investigation, approvals, data, CPU scheduling and releases |
| [Suggested stack](TECH_STACK.md) | Core/optional technologies, UI, CPU models and tradeoffs |
| [Architecture](ARCHITECTURE.md) | Module boundaries, responsibilities and repository layout |
| [CPU-only AI](CPU_AI.md) | Models, evaluation, thread/concurrency and resource limits |
| [Security](SECURITY.md) | Identity, credentials, policy, approvals and threat model |
| [Installation](INSTALL.md) | Current repository setup and future guest deployment gates |
| [Configuration](CONFIGURATION.md) | Settings, inventory, models and credential references |
| [MCP](MCP.md) | Protocol, gateway and execution contracts |
| [Integrations](INTEGRATIONS.md) | Eleven families, scope, limitations and compatibility status |
| [Data and API](DATA_API.md) | Durable work, evidence, memory, topology, RCA and endpoints |
| [UI](UI.md) | Bilingual console, design system, approvals and accessibility |
| [Development](DEVELOPMENT.md) | Module ownership, GitHub, CI and delivery discipline |
| [Testing](TESTING.md) | Security, integration, offline, language and model evaluations |
| [Operations](OPERATIONS.md) | Local monitoring, backup/restore, failures and release rollback |
| [Troubleshooting](TROUBLESHOOTING.md) | Safe diagnostics and unknown outcomes |
| [Roadmap](ROADMAP.md) | Phases 0–8 and five work packages ending in the offline Zabbix answer |
| [Glossary](GLOSSARY.md) | Consistent Persian and English terminology |

## Sources and project control

Read [SOURCES](../requirements/SOURCES.md), the [active prompt](../requirements/NEXTOPS_MASTER_PROMPT.md), the [preserved v2 source](../requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md), [TRACEABILITY](../requirements/TRACEABILITY.md), [ADRs](../adr/README.md), [PROJECT_STATE](../PROJECT_STATE.md) and [NEXT_TASK](../NEXT_TASK.md). The [Zabbix allocation record](../requirements/ZABBIX_SERVER_PLAN.json) and [deployment amendment](../requirements/DEPLOYMENT_UPDATE.md) distinguish proposed allocations from hardware observations. The [visual review](../VISUAL_REVIEW.md) is not an offline-runtime test.

Every English guide has a same-named Persian counterpart. Update them together. Do not translate executable identifiers, protocol fields or the master prompt. Keep credentials and real infrastructure identifiers out of this public repository. Documentation and calculated budgets are not evidence of installed services or passed tests.
