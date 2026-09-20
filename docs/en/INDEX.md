# Documentation index

[فارسی](../fa/INDEX.md) · [Home](../../README.md)

**Baseline date: 2026-09-20. Status: proposed design and documentation.** The guides describe what must be built; they are not evidence of a working deployment. The supplied master prompt retains its original preparation date and is not translated again.

> **Mandatory constraint:** after provisioning, Internet loss must not stop local CPU answers, new local login or offline restart. Read the [offline operating contract and acceptance suite](OFFLINE_RUNTIME.md) before selecting any runtime dependency.

> **First implementation outcome:** Phase 1 must end with a real, evidence-linked local AI answer about Zabbix status while Internet is blocked. The [G10 server plan](SERVER_PLAN.md) proposes three initial NextOps VMs and defines the later four/five-VM layout; the [revised roadmap](ROADMAP.md) supersedes older first-answer timing.

## Reading paths

Start with the [offline operating contract](OFFLINE_RUNTIME.md), [G10 server plan](SERVER_PLAN.md), [diagram atlas](DIAGRAMS.md), [suggested technology stack](TECH_STACK.md), [architecture](ARCHITECTURE.md), [CPU-only AI](CPU_AI.md), and [security](SECURITY.md). Then read [installation](INSTALL.md), [configuration](CONFIGURATION.md), and [development](DEVELOPMENT.md) before any implementation or host change.

| Guide | Contents |
|---|---|
| [Offline operating contract](OFFLINE_RUNTIME.md) | Mandatory local answers, offline cold start/login, dependency inventory, LAN boundaries and OFF-01–OFF-10 acceptance tests |
| [G10 servers and Zabbix milestone](SERVER_PLAN.md) | Per-phase VM counts, proposed resource budgets, existing versus lab Zabbix, trust placement and ZBX-01–ZBX-08 acceptance gates |
| [Diagram atlas](DIAGRAMS.md) | Seven Mermaid views: context, deployment, investigation, approvals, data, CPU scheduling and releases |
| [Suggested technology stack](TECH_STACK.md) | Core choices, UI system, CPU AI profile, optional additions, alternatives and official references |
| [Architecture](ARCHITECTURE.md) | Boundaries, service responsibilities, stack, repository layout |
| [CPU-only AI](CPU_AI.md) | Models, runtime, benchmark stages, resource limits |
| [Security](SECURITY.md) | Identity, credentials, policy, approvals, threat model |
| [Installation](INSTALL.md) | Current repository setup; future Compose/systemd deployment gates |
| [Configuration](CONFIGURATION.md) | Settings contracts, inventories, models, secret references |
| [MCP](MCP.md) | Protocol, gateway, tool and execution contracts |
| [Integrations](INTEGRATIONS.md) | All eleven families, capabilities, safety and compatibility status |
| [Data and API](DATA_API.md) | Persistence, jobs, evidence, memory, topology, RCA, endpoints |
| [UI](UI.md) | Operations console, bilingual layouts, design system, approval screens |
| [Development](DEVELOPMENT.md) | Module ownership, GitHub workflow, CI/release, coding discipline |
| [Testing](TESTING.md) | Adversarial, integration, offline, language, and model evaluation |
| [Operations](OPERATIONS.md) | Observability, backup/restore, outage modes, release rollback |
| [Troubleshooting](TROUBLESHOOTING.md) | Safe diagnostic decision paths and unknown outcomes |
| [Roadmap](ROADMAP.md) | Phases 0–8, Zabbix answers in Phase 1 and measurable acceptance gates |
| [Glossary](GLOSSARY.md) | Consistent English/Persian product terminology |

## Sources and project control

[Source notes](../requirements/SOURCES.md) identify the supplied documents. [Master prompt](../requirements/NEXTOPS_MASTER_PROMPT.md) contains the enhanced specification and the original Persian appendix. [Traceability](../requirements/TRACEABILITY.md) maps all 51 original sections. [ADRs](../adr/README.md) record proposed architectural choices. [Project state](../PROJECT_STATE.md) and [next task](../NEXT_TASK.md) distinguish delivered documentation from unimplemented software. The [visual documentation review](../VISUAL_REVIEW.md) records the scope and limits of the diagram/technology update's checks, not offline runtime validation.

Every English guide has a Persian counterpart with the same filename. Update both in the same change. Machine identifiers, protocol fields, executable commands, and the master prompt are not translated. Source examples are not live inventory or measured results.
