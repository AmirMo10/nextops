# NextOps Markdown context index

Updated: 2026-09-21

This is the durable inventory and routing map for project-owned Markdown. It lets an agent remember
that every document exists without flooding each task with every file. The documentation validator
requires every project Markdown file to appear exactly once in the complete inventory below.

این فایل فهرست ماندگار همهٔ مستندات Markdown پروژه است. عامل باید ابتدا بر اساس نوع کار،
فقط سندهای مرتبط را از مسیرهای زیر بخواند؛ فهرست کامل به معنی بارگذاری هم‌زمان همهٔ فایل‌ها
نیست.

## Core context for every task

Read `AGENTS.md`, `docs/PROJECT_STATE.md`, and `docs/NEXT_TASK.md`. Use this index to choose the
remaining task-specific sources. The repository skill
`.agents/skills/nextops-project-context/SKILL.md` defines precedence and conflict handling.

## Task routing

| Task | Read before acting |
|---|---|
| Requirements, scope, or acceptance | `docs/requirements/NEXTOPS_MASTER_PROMPT.md`, `PROMPT_CHANGELOG.md`, `TRACEABILITY.md`, relevant amendment, and the archive only for original non-conflicting detail |
| Architecture or public interfaces | relevant ADRs, `docs/en/ARCHITECTURE.md`, `DATA_API.md`, `MCP.md`, `SECURITY.md`, and their Persian pairs |
| Application or database code | `docs/en/DEVELOPMENT.md`, `DATA_API.md`, `TESTING.md`, current state/next task, source contracts, migrations, and neighboring tests |
| Authentication or session lifecycle | `docs/requirements/SESSION_TERMINATION_SPEC.md`, `docs/en/SECURITY.md`, `DATA_API.md`, `TESTING.md`, current release manifest, source service/API, and identity integration tests |
| Certificate lifecycle | `docs/requirements/CERTIFICATE_LIFECYCLE_SPEC.md`, `docs/en/OPERATIONS.md`, Persian operations pair, systemd checker/timer, Nginx profiles, current release manifest, and private rotation/alert evidence |
| Local CPU inference | `docs/en/CPU_AI.md`, `OFFLINE_RUNTIME.md`, `TESTING.md`, inference manifest, current state/next task, and Persian pairs when human-facing text changes |
| Server, storage, or deployment | use `nextops-server-operations`; read the start checklist, matching dossier, installer guide, storage/offline/server guide, and current private change record |
| Zabbix or connector work | Zabbix guide, integration guide, MCP/security/data contracts, matching dossiers, ZBX/OFF acceptance cases, and target-specific private evidence |
| Documentation | use `nextops-bilingual-documentation`; read the source requirement plus both language versions and update state/traceability when capability changes |
| Substantial feature or architecture change | use `nextops-change-planner`; read `docs/en/SPECIFICATION_WORKFLOW.md`, the current release manifest, applicable ADRs, and the feature specification |
| Phase 2 Linux/Zabbix investigation | `docs/en/PHASE_2_COMPLETION_SPEC.md`, `docs/en/PHASE_2_OPERATIONS.md`, Persian pairs, ADR 0007, current release manifest, and the connector/systemd deployment profiles |
| Backup, restore, or disaster recovery | `docs/en/BACKUP_RESTORE_SPEC.md`, Persian pair, ADR 0008, `deploy/recovery/README.md`, recovery profile, current release manifest, operations guide, and private destination/restore evidence |
| Acceptance or release review | use `nextops-acceptance-reviewer`; read the feature specification, current release manifest, test evidence, offline contract, and security guide |
| Documentation consistency review | use `nextops-doc-reviewer` plus `nextops-bilingual-documentation`; compare current guidance with the release manifest, source, tests, and paired language files |
| Release or GitHub workflow | `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `docs/en/DEVELOPMENT.md`, test guide, and GitHub templates |

## Complete inventory

Each bullet uses a repository-relative path followed by its role. Keep the paths synchronized when a
Markdown file is added, renamed, or removed.

- `.agents/skills/nextops-bilingual-documentation/SKILL.md` — Bilingual documentation workflow and archive rules.
- `.agents/skills/nextops-change-planner/SKILL.md` — Bounded brownfield change-planning workflow.
- `.agents/skills/nextops-acceptance-reviewer/SKILL.md` — Evidence-based offline, security, reliability, and release review.
- `.agents/skills/nextops-doc-reviewer/SKILL.md` — Documentation drift, parity, terminology, and release-consistency review.
- `.agents/skills/nextops-project-context/SKILL.md` — Core project-memory, source-precedence, and context-routing workflow.
- `.agents/skills/nextops-server-operations/SKILL.md` — Authorized server, package, storage, and deployment workflow.
- `.github/ISSUE_TEMPLATE/bug_report.md` — GitHub defect-report template.
- `.github/ISSUE_TEMPLATE/design_request.md` — GitHub architecture and design-request template.
- `.github/pull_request_template.md` — Pull-request evidence and review checklist.
- `AGENTS.md` — Repository-wide agent instructions and safety boundaries.
- `CHANGELOG.md` — Versioned repository change history.
- `CONTRIBUTING.md` — Contribution, review, and verification requirements.
- `deploy/installers/README.md` — Offline OS-package bundle and installer operator guide.
- `deploy/systemd/README.md` — Native Stage 1B systemd source profile, installed layout, and deployment gates.
- `deploy/linux/README.md` — Forced-command Phase 2 Linux collector assets and operational boundary.
- `deploy/recovery/README.md` — Bilingual guarded promotion sequence for independent recovery.
- `docs/adr/0001-modular-single-host.md` — ADR for the modular core and initial single-host topology.
- `docs/adr/0002-local-cpu-only.md` — ADR for mandatory local CPU-only AI.
- `docs/adr/0003-security-before-execution.md` — ADR for policy and safety before execution.
- `docs/adr/0004-postgresql-first.md` — ADR for PostgreSQL authoritative state.
- `docs/adr/0005-incremental-delivery.md` — ADR for incremental complete-flow delivery.
- `docs/adr/0006-evidence-and-bilingual-ui.md` — ADR for evidence-qualified answers and bilingual UI.
- `docs/adr/0007-forced-command-linux-connector.md` — ADR for forced-command, read-only Linux diagnostics.
- `docs/adr/0008-independent-recovery-repositories.md` — Proposed ADR for separate PostgreSQL and file recovery repositories.
- `docs/adr/README.md` — ADR status and navigation.
- `docs/en/ARCHITECTURE.md` — English architecture and repository boundaries.
- `docs/en/BACKUP_RESTORE_SPEC.md` — English bounded specification for independent backup and isolated restore.
- `docs/en/CONFIGURATION.md` — English configuration contracts and current implemented subset.
- `docs/en/CPU_AI.md` — English local CPU inference and capacity plan.
- `docs/en/AI_SYSTEMD.md` — English Stage 1B native systemd service profile and installation hold.
- `docs/en/DATA_API.md` — English durable data, workflow, evidence, and API contracts.
- `docs/en/DEPLOYMENT_DOSSIERS.md` — English per-server dossier workflow.
- `docs/en/DEVELOPMENT.md` — English development, CI, GitHub, and release workflow.
- `docs/en/DIAGRAMS.md` — English architecture diagram atlas.
- `docs/en/ENGINEERING_UPGRADE_PLAN.md` — English phased candidate-adoption and modernization plan.
- `docs/en/ESXI_BASELINE.md` — English ESXi and guest CPU evidence boundaries.
- `docs/en/GLOSSARY.md` — English product terminology.
- `docs/en/INDEX.md` — English documentation navigation.
- `docs/en/INSTALL.md` — English repository setup and future installation gates.
- `docs/en/INTEGRATIONS.md` — English integration scope and capability status.
- `docs/en/MCP.md` — English MCP gateway and connector contracts.
- `docs/en/OFFLINE_RUNTIME.md` — English mandatory offline-runtime contract.
- `docs/en/OPERATIONS.md` — English observability, backup, recovery, and rollback design.
- `docs/en/PHASE_0_REPORT.md` — Dated English Phase 0 evidence and decision report.
- `docs/en/PHASE_2_COMPLETION_SPEC.md` — English bounded specification for completing the Linux/Zabbix incident phase.
- `docs/en/PHASE_2_OPERATIONS.md` — English deployment, acceptance, and rollback guide for the Phase 2 forced-command connector.
- `docs/en/PROJECT_STATUS_BRIEF.md` — Presentation-ready English summary of verified progress and remaining delivery gates.
- `docs/en/ROADMAP.md` — English phased roadmap and acceptance gates.
- `docs/en/SECURITY.md` — English identity, policy, approval, and threat controls.
- `docs/en/SPECIFICATION_WORKFLOW.md` — English brownfield specification workflow and source-of-truth boundaries.
- `docs/en/STAGE_1_COMPLETION_REPORT.md` — Dated English controlled Stage 1 qualification and recovery evidence.
- `docs/en/SERVER_PLAN.md` — English G10 VM plan and Zabbix milestone.
- `docs/en/SERVER_START_CHECKLIST.md` — English first-server and package-bundle checklist.
- `docs/en/START_HERE.md` — English onboarding and first milestone.
- `docs/en/TECH_STACK.md` — English technology choices and constraints.
- `docs/en/TESTING.md` — English test, evaluation, and release-evidence plan.
- `docs/en/TROUBLESHOOTING.md` — English fail-closed diagnostic playbook.
- `docs/en/UI.md` — English bilingual console and design-system requirements.
- `docs/en/ZABBIX_SERVER.md` — English dedicated Zabbix server design.
- `docs/fa/ARCHITECTURE.md` — Persian architecture and repository boundaries.
- `docs/fa/BACKUP_RESTORE_SPEC.md` — Persian bounded specification for independent backup and isolated restore.
- `docs/fa/CONFIGURATION.md` — Persian configuration contracts and current implemented subset.
- `docs/fa/CPU_AI.md` — Persian local CPU inference and capacity plan.
- `docs/fa/AI_SYSTEMD.md` — Persian Stage 1B native systemd service profile and installation hold.
- `docs/fa/DATA_API.md` — Persian durable data, workflow, evidence, and API contracts.
- `docs/fa/DEPLOYMENT_DOSSIERS.md` — Persian per-server dossier workflow.
- `docs/fa/DEVELOPMENT.md` — Persian development, CI, GitHub, and release workflow.
- `docs/fa/DIAGRAMS.md` — Persian architecture diagram atlas.
- `docs/fa/ENGINEERING_UPGRADE_PLAN.md` — Persian phased candidate-adoption and modernization plan.
- `docs/fa/ESXI_BASELINE.md` — Persian ESXi and guest CPU evidence boundaries.
- `docs/fa/GLOSSARY.md` — Persian product terminology.
- `docs/fa/INDEX.md` — Persian documentation navigation.
- `docs/fa/INSTALL.md` — Persian repository setup and future installation gates.
- `docs/fa/INTEGRATIONS.md` — Persian integration scope and capability status.
- `docs/fa/MCP.md` — Persian MCP gateway and connector contracts.
- `docs/fa/OFFLINE_RUNTIME.md` — Persian mandatory offline-runtime contract.
- `docs/fa/OPERATIONS.md` — Persian observability, backup, recovery, and rollback design.
- `docs/fa/PHASE_0_REPORT.md` — Dated Persian Phase 0 evidence and decision report.
- `docs/fa/PHASE_2_COMPLETION_SPEC.md` — Persian bounded specification for completing the Linux/Zabbix incident phase.
- `docs/fa/PHASE_2_OPERATIONS.md` — Persian deployment, acceptance, and rollback guide for the Phase 2 forced-command connector.
- `docs/fa/PROJECT_STATUS_BRIEF.md` — Presentation-ready native-Persian summary of verified progress and remaining delivery gates.
- `docs/fa/ROADMAP.md` — Persian phased roadmap and acceptance gates.
- `docs/fa/SECURITY.md` — Persian identity, policy, approval, and threat controls.
- `docs/fa/SPECIFICATION_WORKFLOW.md` — Persian brownfield specification workflow and source-of-truth boundaries.
- `docs/fa/STAGE_1_COMPLETION_REPORT.md` — Dated Persian controlled Stage 1 qualification and recovery evidence.
- `docs/fa/SERVER_PLAN.md` — Persian G10 VM plan and Zabbix milestone.
- `docs/fa/SERVER_START_CHECKLIST.md` — Persian first-server and package-bundle checklist.
- `docs/fa/START_HERE.md` — Persian onboarding and first milestone.
- `docs/fa/TECH_STACK.md` — Persian technology choices and constraints.
- `docs/fa/TESTING.md` — Persian test, evaluation, and release-evidence plan.
- `docs/fa/TROUBLESHOOTING.md` — Persian fail-closed diagnostic playbook.
- `docs/fa/UI.md` — Persian bilingual console and design-system requirements.
- `docs/fa/ZABBIX_SERVER.md` — Persian dedicated Zabbix server design.
- `docs/MARKDOWN_CONTEXT_INDEX.md` — This complete Markdown inventory and task router.
- `docs/NEXT_TASK.md` — Current unfinished checkpoint and acceptance evidence.
- `docs/PROJECT_STATE.md` — Current implemented, tested, proposed, and blocked state.
- `docs/requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md` — Immutable original requirements and Persian appendix.
- `docs/requirements/CERTIFICATE_LIFECYCLE_SPEC.md` — Bilingual local expiry, alert, rotation, and rollback contract.
- `docs/requirements/DEPLOYMENT_UPDATE.md` — Active four-server deployment amendment.
- `docs/requirements/NEXTOPS_MASTER_PROMPT.md` — Active engineering requirements and precedence.
- `docs/requirements/nextops-threat-model.md` — Repository-grounded threat model and mitigations.
- `docs/requirements/PHASE_2_INCIDENT_CONTEXT_SPEC.md` — Bounded Phase 2 Zabbix history/event feature packet.
- `docs/requirements/PROMPT_CHANGELOG.md` — Prompt version and precedence history.
- `docs/requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md` — Per-server dossier and package-layer specification.
- `docs/requirements/SESSION_TERMINATION_SPEC.md` — Bilingual bounded specification for audited server-side logout.
- `docs/requirements/SOURCES.md` — Source provenance and archive identities.
- `docs/requirements/TRACEABILITY.md` — Mapping of all original requirements to phases and evidence.
- `docs/STORAGE_PLAN.md` — Bilingual storage evidence, arithmetic, and capacity guardrails.
- `docs/VALIDATION.md` — Dated publication and source-identity validation record.
- `docs/VISUAL_REVIEW.md` — Dated visual-documentation review record.
- `README_FA.md` — Persian project overview and navigation.
- `README.md` — English project overview and navigation.
- `SECURITY.md` — Repository security policy and reporting process.
- `tasks/plan.md` — Implementation plan record for Stage 1B Increment 3.
- `tasks/todo.md` — Completed task record for guarded per-server package installers.
