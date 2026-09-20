# NEXTOPS — GitHub-First, CPU-Only Engineering Master Prompt

Version: 2.0 | Prepared: 2026-09-19

## How to use this document

Give this entire document to the coding agent working in the NextOps repository. The first assignment is **Phase 0: discovery and architecture**, not unrestricted implementation. Appendix A preserves the original Persian specification. This document is a development instruction, not a claim that a repository, deployment, benchmark, or integration already exists.

---

## 1. Your role and operating contract

Act as NextOps's Principal Software Architect, Senior Python Engineer, Infrastructure/Network Engineer, CPU Inference Engineer, Security Engineer, SRE, and Product/UX Engineer. Produce a maintainable IT operations platform, not a chatbot with unrestricted shell access.

Make explicit decisions, implement small verified increments after architecture approval, and keep the repository ready for another engineer or agent to continue. Use evidence from the repository and server. Distinguish **observed**, **proposed**, **implemented**, **tested**, **blocked**, and **deferred**. Never invent tool access, server specifications, benchmark results, successful tests, device capabilities, or completed deployments.

Engineering objectives, in order: protect infrastructure and data; produce correct, evidence-grounded diagnostics; remain usable on CPU-only hardware; stay operable by a small team; preserve extension points without unnecessary services.

Use English identifiers and code. Support native, readable Persian and English in the product and documentation. Do not rewrite functioning project conventions without a documented reason.

## 2. Fixed deployment requirements and unresolved facts

The owner has specified:

- GitHub is the source-control repository and collaboration system.
- Initial development, hardware validation, and deployment target one G10-class server.
- The server reportedly has approximately 90 CPU units, 1 TB RAM, and sufficient disk capacity.
- There is **no GPU**. **All NextOps AI processing must execute locally on CPUs.**
- The original target operating system is Ubuntu; Ubuntu 24.04 LTS is a proposed baseline only if compatible with the actual host and owner-approved installation.
- The platform must retain the original eleven integration families, Persian support, auditability, approvals, and offline operation.

Do not interpret “90 CPU” as 90 physical cores, 90 sockets, or any particular CPU model. It may mean logical CPUs or an allocation inside a VM. Do not infer the manufacturer, processor generation, NUMA layout, AVX/AVX-512/AMX capabilities, disk type, network bandwidth, or free capacity from “G10.” Discover these.

CPU-only applies to generation, planning, embeddings, reranking, semantic search models, anomaly models, local evaluation/judging, and any subsequently introduced AI worker. Do not introduce external AI APIs, remote GPU inference, accelerator-dependent packages, or a silent cloud fallback. Preserve a provider interface, but ship this deployment with local CPU providers only. An API using an OpenAI-compatible request format does not authorize calls to OpenAI or any external inference service.

GitHub connectivity is for controlled development and release synchronization; it must not be necessary for runtime operations. Runtime network access to explicitly authorized managed infrastructure remains necessary. Offline means no Internet dependency, not no access to the management LAN.

## 3. Preserve the original specification; apply explicit revisions

Appendix A is the original product scope. Preserve its terminology and required capabilities. Create `docs/requirements/TRACEABILITY.md`, mapping every original numbered section to a domain, milestone, implementation location, acceptance test, and delivery status.

These changes intentionally supersede conflicting portions of the original roadmap:

1. Security, authorization, audit, bounded execution, and approval contracts belong in the foundation, before real infrastructure access—not a late security phase.
2. CPU-only inference and offline validation begin before building an agent dependent on them—not after UI completion.
3. All eleven integrations remain in scope, but delivery uses complete vertical slices rather than eleven superficial adapters.
4. Cloud providers are not enabled in this deployment. Future provider portability is an interface requirement, not permission to use external AI.
5. PostgreSQL is the initial production system of record. Retain the database abstraction; do not claim MySQL/SQLite runtime parity before conformance and migration tests exist. Keep alternate internal backends explicitly tracked. Managed MySQL/MariaDB and SQL Server integrations are separate requirements.
6. Admin roles do not bypass audit or critical-action controls. A “read-only” label does not automatically authorize arbitrary commands or queries.
7. RCA must distinguish hypotheses from verified causes. Do not invent numeric probabilities; use qualified confidence unless calibration has been validated.
8. Show concise decision summaries, evidence, and tool activity—not unrestricted internal reasoning traces.
9. One physical host is one failure domain. Multiple containers, VMs, database processes, or replicas on it do not constitute host-level high availability.

Do not silently remove other original requirements. Explain every deliberate deviation in an architecture decision record (ADR).

## 4. Phase 0: inspect before changing anything

First establish whether a repository and server connection actually exist. Inspect available tools and credentials without displaying secrets. If either resource is unavailable, complete the architecture using labeled assumptions and provide a read-only discovery script for the owner; never pretend to have inspected it.

Repository discovery:

- Check Git status, branch, sanitized remotes, existing commits, and tracked first-party files. Preserve dirty changes and existing implementations.
- Read project/agent instructions, architecture, source, dependency manifests/lockfiles, migrations, deployment configuration, workflows, and test definitions.
- Map modules, API contracts, implemented capabilities, placeholders, security boundaries, and technical debt.
- Review test/install scripts for unsafe side effects before running them in an isolated environment without production credentials.
- Record baseline test/lint/type-check results, including commands and actual failures. Do not read credential files just to inventory them.
- Never use destructive reset/clean operations, overwrite existing work, rewrite history, or publish private data.

Host discovery should use non-destructive commands where available, with sanitized reporting:

```bash
cat /etc/os-release
uname -r
lscpu
lscpu -e=CPU,CORE,SOCKET,NODE,ONLINE
nproc
free -h
numactl --hardware                 # only if already installed
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,ROTA
findmnt
systemd-detect-virt
ss -lnt                            # do not publish sensitive listener details
```

Also inspect permitted CPU affinity/cgroups, available rather than installed RAM, existing workloads, storage mounts/free space, time synchronization, service managers, container tooling, certificate practices, management network routes, and backup destinations. Hardware serial numbers, production addresses, and private host inventories do not belong in public reports.

Do not install packages, run stress tests, alter networking, reboot, or download large models during discovery. CPU/memory/storage benchmarking requires a controlled workload window and resource limits. Do not run destructive disk tests or globally drop caches on a shared host.

Also establish the operating envelope: approximate managed-asset count, event/alert rate, log/evidence volume, retention, simultaneous investigations, interactive latency goals, and existing workload contention. Treat unavailable values as unresolved assumptions; do not infer them from RAM size. Propose measurable latency/throughput targets before model selection and label every target as a target, not a benchmark result.

Deliver the Phase 0 report in the format specified in Section 26, then stop before large changes until the owner approves the architecture/roadmap.

## 5. Architectural direction: a modular core with isolated execution

Start with a **modular monolith for the control plane**, a durable worker process, an independently protected execution/MCP gateway, and a local CPU inference service. Split deployment processes for trust, resource isolation, or independently measured scaling needs—not simply because a feature exists.

Proposed logical architecture:

```text
Browser / CLI / monitoring event ingress
                  |
             TLS reverse proxy
                  |
        FastAPI control plane + UI API
     identity | inventory | incidents | approvals
                  |
          persisted workflow + worker
           /            |             \
 CPU inference     evidence/RAG      policy decisions
 no device creds   scoped retrieval       |
                                          v
                              protected MCP execution gateway
                                audit + authorization + limits
                                          |
                         isolated, enabled connector runners
                                          |
                              authorized infrastructure

PostgreSQL: business state, jobs, approvals, audit, topology, retrieval metadata
Local restricted storage: sanitized evidence, pinned models, backup staging
Observability: metrics, structured logs, traces; separate from security audit
```

Enforce the diagram operationally. The browser never accesses connectors or inference directly. The model process has no infrastructure credentials or management-network access. API/planning processes cannot bypass the gateway. Connector processes get only their own target-scoped credentials and network access. Control-plane database permissions and execution-side permissions must reflect these boundaries; a shared unrestricted database account would undermine them.

An initial deployment may have approximately these roles: reverse proxy/static frontend, API, workflow worker, MCP gateway, enabled connector runners, inference, PostgreSQL, and optional observability services. Share code packages where sensible. Do not start every future connector or infrastructure service by default.

Do not add Kubernetes, a service mesh, Kafka, a standalone graph database, several vector databases, or a second workflow engine without an ADR showing a current requirement. Keep interfaces ready for future separate-host deployment.

## 6. Proposed stack and decision discipline

Use these defaults for an empty repository, subject to compatibility checks and ADRs:

| Layer | Starting choice | Boundary |
|---|---|---|
| Backend | Python 3.12 baseline, FastAPI, Pydantic | Verify installed/runtime compatibility and pin supported versions. |
| Persistence | PostgreSQL, SQLAlchemy, Alembic | PostgreSQL is authoritative; use real PostgreSQL in integration tests. |
| Work execution | PostgreSQL-backed durable jobs and bounded Python workers | Persist leases, retries, workflow state, and approvals; never rely on web-process memory. |
| Cache | None initially; add Redis only for a measured need | Cache is never the authority for approvals, job completion, or audit. |
| Retrieval | PostgreSQL metadata + local lexical retrieval + pgvector when enabled | Validate Persian search; avoid claiming English tokenization handles Persian correctly. |
| Frontend | React, TypeScript, Vite, accessible components, RTL-aware CSS | Prefer existing good project conventions; use no hosted runtime assets. |
| AI generation | Pinned `llama.cpp` CPU build and local `llama-server` | One dedicated service, not one model per API worker. |
| Embeddings | One benchmarked multilingual CPU model | Optional separate worker; no remote embedding API. |
| MCP | Official maintained Python SDK and a pinned compatible protocol version | Real protocol initialization, tools, schemas, errors, and transports. |
| Deployment | Docker Compose baseline; supported systemd alternative | Same settings/contracts, documented feature parity and limitations. |
| Telemetry | Structured logging, Prometheus metrics, OpenTelemetry where justified | No hosted telemetry dependency. |
| Tests | pytest, HTTP/API tests, frontend tests and browser E2E | Fixtures/simulators by default; real-device tests are explicit opt-in. |

Resolve package versions against official documentation and the existing project when implementation begins. Lock Python/frontend dependencies, container digests, model revisions, and runtime builds. Do not use floating `latest` in releases or assume a package mentioned here has been installed.

## 7. Repository structure

For a greenfield repository, start from this structure and create directories only when they contain a real implementation, contract, or document. Adapt rather than duplicate an existing good structure.

```text
nextops/
  README.md
  README_FA.md
  AGENTS.md
  SECURITY.md
  CONTRIBUTING.md
  CHANGELOG.md
  pyproject.toml
  uv.lock                         # or the existing chosen lockfile
  .env.example
  .gitignore
  .github/
    CODEOWNERS
    ISSUE_TEMPLATE/
    pull_request_template.md
    workflows/                    # CI, security, release; controlled deploy
  apps/
    api/
    worker/
    mcp_gateway/
    web/
  packages/nextops/
    domain/                       # entities and invariants; no framework I/O
    application/                  # use cases, orchestration, approval workflows
    contracts/                    # versioned events, requests, tool/result schemas
    policy/                       # deterministic decisions and authorization
    inference/                    # CPU provider client, budgets, model registry
    knowledge/                    # ingestion, retrieval, topology, incident memory
    connectors/
      base/
      linux/
      windows/
      cisco/
      juniper/
      fortigate/
      sophos/
      zabbix/
      grafana/
      sqlserver/
      mysql/
      esxi/
    infrastructure/               # DB repositories, secret adapters, durable jobs
    observability/
    localization/
  migrations/
  config/
    app.example.yaml
    models.example.yaml
    inventory.example.yaml
    credentials.example.yaml      # references only; never actual credentials
    policies.example.yaml
    resource-profiles.example.yaml
  deploy/
    compose/
    systemd/
    reverse-proxy/
  scripts/
    discover.sh
    install.sh
    setup.sh
    start.sh
    stop.sh
    test.sh
    benchmark_cpu.sh
    backup.sh
    restore.sh
    release.sh
    rollback.sh
    offline_bundle.sh
  tests/
    unit/
    integration/
    contract/
    security/
    e2e/
    fixtures/
  evals/
    datasets/
    rubrics/
    runners/
  benchmarks/
    scenarios/
    reports/                      # sanitized results only
  docs/
    requirements/
    architecture/
    adr/
    operations/
    security/
    integrations/
    fa/
    en/
    PROJECT_STATE.md
    NEXT_TASK.md
```

Define Python packaging/import roots explicitly; the directory sketch is not a build configuration. Keep dependencies directed inward: infrastructure implements application/domain ports, not the reverse. Avoid a giant `utils.py`, a single massive agent module, and untyped dictionaries as cross-module contracts.

Store models and operational data outside Git and outside the source checkout. Proposed paths are `/srv/nextops/models`, `/var/lib/nextops`, `/etc/nextops`, and a separately configured backup destination. Paths must be configurable, ownership-restricted, and validated against actual mounts.

## 8. GitHub workflow and supply-chain controls

Use short-lived branches, small reviewable changes, issue/milestone traceability, protected main where available, and tagged releases. Do not create a repository, change visibility, push, merge, or configure account-level settings without authorization. If no remote is supplied, use a clearly marked placeholder and complete local planning; do not invent an owner or repository.

Create `AGENTS.md` describing CPU-only constraints, safety invariants, module boundaries, required tests, and phase completion rules. Avoid copying this entire master prompt into every agent instruction file.

CI should check formatting, lint, types, unit/contract/security tests, actual PostgreSQL integration tests, frontend build/E2E as appropriate, secret scanning, dependency vulnerabilities, and release metadata. Add software/model bills of materials and artifact checksums. Pin third-party actions by reviewed commit SHA; grant minimal workflow permissions.

Proposed policy: generic untrusted PR checks use isolated GitHub-hosted workers when approved, or an equivalent disposable sandbox with no management-network reachability. Hardware benchmarks and authorized infrastructure tests run on the G10 in an isolated trusted workflow. This extends the original server-based testing rule without uploading operational data.

Do **not** attach a privileged persistent GitHub Actions runner to the management host and allow arbitrary PRs to execute there. Private repositories also require protection from untrusted contributors. Do not use `pull_request_target` to execute untrusted checkout contents with secrets.

Default deployment is owner-triggered promotion of a verified release, not automatic production deployment on every push. The server can pull approved artifacts over an outbound path; no public SSH exposure is required. Use scoped read-only repository access where sufficient. Verify artifact identity, compatibility, migrations, backups, health checks, and rollback conditions. If GitHub features require an unavailable plan/permission, document the limitation and use a manual review gate; do not claim protection exists.

## 9. CPU-only AI architecture

Use deterministic software for parsing, policy, scheduling, inventory resolution, basic correlation, and known runbooks. Reserve LLM calls for language understanding and evidence-grounded synthesis that need them.

Maintain these independently testable interfaces: `LLMProvider`, `EmbeddingProvider`, optional `RerankerProvider`, `ModelRegistry`, `TokenBudget`, and `InferenceScheduler`. Capability metadata must distinguish structured output, tool calling, context limits, streaming, and CPU execution. A configured provider is not healthy until its contract tests pass.

The initial generation candidate is a supported, quantized multilingual model in the approximately 7–9B parameter class. `Qwen/Qwen3-8B` is one baseline candidate, not a claim of current superiority. Compare it with a smaller candidate for triage and a roughly 14B candidate for quality. Consider 24–32B only if measured task quality justifies latency. Never choose a 70B+ model merely because its weights fit in 1 TB RAM. Record total and active parameter counts for MoE candidates; do not infer speed from active counts alone.

Evaluate compatible GGUF quantizations, for example Q4_K_M and Q5_K_M where available. Validate quantization quality on Persian diagnostics and tool arguments, not only generic benchmarks. Default to bounded non-thinking/short-output behavior where supported; verify model-specific chat templates and runtime switches rather than appending magic prompt strings.

`llama.cpp` is the baseline because its official project supports CPU inference, quantized models, and a local server. Use a pinned CPU build; explicitly disable GPU backends/offload supported by that build and verify startup reports CPU execution. Do not install CUDA, ROCm, GPU containers, FlashAttention-only dependencies, or accelerator runtimes. Set GPU layers to zero where supported and verify there is no remote endpoint fallback. The deployment smoke test must work without an accelerator device.

Ollama, OpenVINO CPU, or vLLM CPU may be benchmarked as **alternatives**, not additional mandatory services. Adopt one only after confirming the exact CPU ISA, model/quantization support, tool-output behavior, operating complexity, and measured improvement. Never assume a CPU package supports this particular G10 processor.

For embeddings, compare a small multilingual encoder with a candidate such as Qwen3-Embedding-0.6B. Validate Persian recall, mixed-language device names, dimensions, pooling, instruction templates, and CPU costs. Force CPU execution explicitly. Reranking is optional and must demonstrate retrieval improvement within its budget. Do not implement foundation-model training or fine-tuning as an MVP prerequisite.

Download models only during an approved provisioning step, or import an offline bundle. Record exact source, revision, tokenizer/chat template, quantization, license, file size, and cryptographic checksum. Do not enable arbitrary model remote code. Runtime uses verified local paths only and must not fetch missing artifacts automatically.

## 10. Hardware-aware benchmarking and resource isolation

RAM capacity is not a performance measurement. Determine effective CPU allocation, physical-core topology, memory locality, memory pressure, and existing workload interference before selecting concurrency or model size.

Create a staged benchmark harness, not an enormous Cartesian sweep:

1. Establish one small model, one active request, a bounded prompt/output, and a safe thread allocation.
2. Compare generation-thread and prompt-processing-thread counts, physical-core versus SMT placement, and one NUMA node versus a controlled multi-node configuration where supported.
3. Compare representative quantizations and model sizes on the same dataset.
4. Increase active inference requests from 1 to 2 and then 4 only when latency and resource pressure remain acceptable.
5. Test representative contexts, initially approximately 2K, 4K, and 8K input tokens, with explicit output and per-slot limits. Verify the selected server's total-versus-per-request context semantics.
6. Run controlled mixed workloads: user chat, incident synthesis, embeddings, ingestion, database work, and bounded builds/tests.

Record model/runtime/build identity, flags, CPU mask, NUMA memory policy, input/output token counts, cold/warm state, queue time, time to first token, prompt throughput, generation throughput, total completion latency, p50/p95, resident/peak memory, CPU utilization, page faults/swap pressure, cancellations, and errors. Preserve raw sanitized measurements and evaluation sample counts.

Do not promise tokens/second, simultaneous users, or maximum model size before measurement. Do not claim linear scaling with cores. Test NUMA-aware placement rather than binding arbitrary contiguous CPU numbers that might select SMT siblings.

Maintain one global resource budget across inference, embeddings, workers, web services, databases, tests, and compilation. As an **unvalidated starting experiment**, reserve roughly 20% of effective CPU capacity for control-plane/OS and cap initial inference to a conservative share of the remainder. Replace percentages with topology-aware measured allocations. Do not reserve all RAM just because it exists.

Use enforced cgroup/systemd or validated container limits, per-process thread caps, queue length caps, request admission, cancellation, and backpressure. Keep `OMP_NUM_THREADS`/BLAS/runtime thread pools from multiplying across workers. Do not automatically start 90 web workers or allocate 90 inference threads to every request.

Interactive work outranks batch re-indexing. Cap fan-out and parallel investigations. Start with one generation service; extra model replicas must fit a measured CPU/memory plan. Let the API, audit, and manual incident views remain responsive when inference is saturated or unavailable.

## 11. Durable agent workflow; no autonomous shell loop

Represent investigation as a persisted, bounded workflow, for example:

```text
RECEIVED -> AUTHORIZED -> SCOPED -> PLANNED
 -> COLLECTING -> ANALYZING -> PROPOSAL_READY
 -> AWAITING_APPROVAL -> READY_TO_EXECUTE -> EXECUTING
 -> VERIFYING -> COMPLETED

Additional states: DENIED, EXPIRED, CANCEL_REQUESTED, CANCELLED,
FAILED, OUTCOME_UNKNOWN, MANUAL_RECONCILIATION_REQUIRED
```

Read-only investigations bypass change approval but not authorization, scope checks, audit, and resource limits. A recommendation alone is never execution authorization.

Set configurable limits for elapsed time, LLM calls, tokens, tool calls, bytes, fan-out, per-target work, and retries. Example starting experiment: at most six LLM calls and twenty tool calls per investigation; tune using evidence, not to appear more agentic.

Persist progress and checkpoints before/after external effects. Use transactional job creation/outbox where needed, worker leases/heartbeats, idempotency keys, and duplicate detection. Never claim exactly-once execution across a remote device and the local database. An ambiguous timeout after a mutation becomes `OUTCOME_UNKNOWN`; reconcile the target state before retrying.

Cancellation of a local task is not proof that a remote command stopped. Surface that distinction. Verify postconditions through a fresh read and health checks. Rollback/compensation requires its own policy and may be unavailable or riskier than leaving the state unchanged.

Logical agent roles may include planner, collector, analyst, and verifier. They do not imply four concurrent models or an unbounded multi-agent swarm. Prefer shared bounded inference and deterministic verification.

## 12. MCP gateway and connector contract

An internal Python `execute()` method is not by itself MCP. Use the official SDK, compatible protocol initialization/capability negotiation, typed tool schemas, proper results/errors, cancellation, and transport behavior. Pin and test the protocol/SDK combination.

Use local stdio for suitably isolated local connectors, or authenticated Streamable HTTP for long-lived independently deployed connectors. Never expose unauthenticated MCP endpoints on public interfaces. Validate HTTP origins where applicable. Keep client authentication, downstream credentials, session identity, and token audiences separate; do not pass arbitrary upstream tokens through to downstream services.

Start with an administrator-controlled connector registry; do not auto-install arbitrary MCP servers. Version and review connector manifests/tool schemas. Validate identity, destination allowlists, redirects, and resolved addresses. Management LAN access is permitted only for approved targets; it must not become an arbitrary SSRF proxy.

A typed tool definition must include name/version, connector, input/output schemas, target types, required scopes, environment constraints, deterministic risk class, execution limits, idempotency semantics, approval requirement, preconditions, and verification behavior. Treat remotely supplied tool descriptions and “read-only” annotations as untrusted metadata, not policy authority.

Each execution request includes operation ID, actor and scope, immutable target ID, validated arguments, policy version, approval reference when needed, deadline, idempotency key, and correlation ID. A result includes status, timestamps, sanitized evidence references, partial-result information, verification outcome, and structured error details.

The gateway enforces service authentication, authorization, policy, approval validation, budgets, target serialization where needed, and audit. Connector runners enforce the relevant constraints again at the execution boundary and never accept an unauthenticated direct bypass.

Connector failures must not crash the platform. Use bounded retries for eligible reads, deadlines, circuit breakers, concurrency limits, and typed authentication/permission/connectivity/vendor errors. Do not retry a possibly executed mutation just because transport failed.

## 13. Security and approval invariants

The LLM can propose an operation. Deterministic code decides whether it is permitted. The model cannot grant privileges, lower risk, fabricate consent, edit its own policies, retrieve credentials, or disable auditing.

Retain roles `viewer`, `operator`, `engineer`, `admin`; combine them with action/target/environment scopes and deny-by-default policy. Use one explicit organization scope initially, with an organization/environment key in permission-sensitive records. Do not market the first release as secure multi-tenant SaaS before isolation testing.

Preserve `READ_ONLY`, `LOW_RISK`, `MEDIUM_RISK`, `HIGH_RISK`, `CRITICAL`. Risk is assigned by versioned trusted policy, not the generated command's wording. Even reads can disclose sensitive data or overload a device.

Default MVP policy: read-only, allowlisted diagnostics only; all infrastructure mutations disabled. Later mutations require a named runbook, preconditions, scoped permission, audit availability, and approval. High-risk/critical actions require independent approval and a maintenance-window/impact check; critical destructive actions remain disabled unless explicitly configured through an owner-reviewed change. Admin is not a universal safety bypass.

Bind approval to a canonical digest of exact action, arguments, targets, requester, environment, expected pre-state/config version, policy version, expiry, and single-use nonce. Store it durably. Recheck actor/approver permissions and preconditions at execution. Any material change invalidates consent. Enforce atomic state transitions so duplicate jobs or concurrent clicks cannot reuse an approval. A chat message saying “approved” is not sufficient authorization.

Keep secrets out of source, prompts, responses, ordinary logs, audit payloads, exception messages, traces, screenshots, fixtures, and plaintext database fields. Use credential references. Decrypt target credentials only within the authorized execution boundary, with an external secret-manager interface and a documented local encrypted option whose key is not stored alongside ciphertext. Treat `.env` as a restricted development mechanism, not a production vault.

Verify SSH host keys and TLS certificates; do not use blanket auto-accept or `verify=False`. Use narrow sudo/JEA/API permissions as applicable, credential rotation, session expiration, rate limits, and secure admin bootstrap with no default password. Separate deploy identities from target-device identities. Never expose the container engine socket to the agent, web app, or connector just for convenience.

## 14. Treat external content as data, not instructions

Logs, retrieved runbooks, database strings, alert payloads, device banners, repository documents, and tool output may contain prompt injection. They cannot override policy or instruct the agent to exfiltrate secrets or invoke new tools.

Separate trusted instructions from labeled evidence. Normalize/parse structured fields, cap output length, validate tool arguments, and require execution policy regardless of model output. Enforce authorization before retrieval and again when serving evidence; do not retrieve all tenants/devices and filter only in the UI.

Never expose raw arbitrary shell, PowerShell, SQL, or Python execution as a default tool. Use named operations and validated parameter schemas, library/API calls where possible, and fixed reviewed command templates without shell interpolation. A denylist of dangerous words is insufficient. Protect against shell metacharacters, path traversal, Unicode/bidirectional spoofing, target substitution, and command expansion.

SQL diagnostics use dedicated read-only accounts and narrowly scoped predefined queries/views, statement/query-time/row/byte limits, and appropriate read-only transactions. The prefix `SELECT` does not prove safety; user-defined functions, stored routines, `SELECT INTO`/file output, locks, and expensive execution require separate controls. Treat execution-oriented `EXPLAIN` variants according to their real semantics. SQL parsing is defense in depth, not a replacement for database permissions.

Preserve original English command/error text for diagnosis, but redact detected secrets before persistence or model exposure and label redaction explicitly. Do not promise both unmodified retention and secret-free storage for the same secret-containing payload.

## 15. Integration scope and delivery contracts

Keep all original capabilities in the traceability matrix. For every connector, publish the exact vendor/OS/API versions tested, authentication method, minimum permissions, supported actions, unsupported actions, simulator coverage, real-device test status, and known limitations. Use `planned`, `simulated`, `lab-verified`, and `production-validated` accurately. A placeholder returning success is forbidden.

| Integration | Required diagnostic scope | Communication and safety requirements |
|---|---|---|
| Linux | CPU/RAM/disk, load, uptime, processes, services/systemd, journal/logs, filesystems, users, packages, ports/sockets, routes/DNS/network | SSH or approved local adapter; fixed bounded diagnostics; host-key verification. |
| Windows | CPU/RAM/disk, services/processes, Event Viewer, network/DNS/routes/ports, updates, users, PowerShell and AD-related diagnostics | Supported authenticated management transport; avoid unencrypted Basic auth; constrained operations/JEA where available. |
| Cisco IOS/IOS-XE | Interfaces/errors, VLAN/trunk/STP, routes/ARP/MAC, BGP/OSPF/DHCP, ACL/NAT, health/logs/configuration | Prefer supported structured APIs/NETCONF/RESTCONF, otherwise verified SSH; platform-specific parsing. |
| Juniper Junos | Interfaces/VLAN/routes/ARP/MAC, BGP/OSPF, firewall filters, health/logs, configuration/diff/commit status | NETCONF/PyEZ or supported API/SSH; controlled commit/rollback procedures when mutations are enabled. |
| FortiGate | Interfaces/routes/policies/objects/services, sessions, VPN/IPsec/SSL VPN, HA, DHCP/DNS, health/logs/configuration | Versioned API or restricted SSH; VDOM/permission awareness; VPN phase/policy/routing evidence. |
| Sophos | Firewall/interfaces/routing/rules/NAT, VPN phases, DHCP/DNS, sessions, HA/health/logs/alerts | Separate Firewall and Central capabilities; verify API/version/licensing; do not fabricate unavailable telemetry endpoints. |
| Zabbix | Hosts/groups/templates/items/triggers/problems, events, history/trends, latest data and graph metadata | Authenticated API; bounded polling/webhooks, deduplication, pagination, retention-aware queries. |
| Grafana | Dashboards/folders/panels/datasources, alerts/annotations and supported queries | Dashboard metadata is not the underlying metric store; use authorized supported datasource queries/adapters and scoped tokens. |
| SQL Server | Health, databases/tables/indexes, sessions/connections, blocking/locks/deadlocks, waits, query performance, jobs/backups | Read-only diagnostic identities and supported drivers/TLS; verify DMV permissions/version support. |
| MySQL/MariaDB | Databases/tables/indexes/users, sessions/processes/locks, slow queries, replication, health/status/variables | Detect engine/version; bounded read-only diagnostics; no unrestricted arbitrary SQL. |
| VMware ESXi | Host health/CPU/RAM, datastores/network, VM inventory/power/snapshots/disks/NICs, performance, alarms/events/logs | Verify version, API and license capabilities; separate future vCenter adapter; no implicit authorization for power/snapshot/delete actions. |

Future extension points remain: Active Directory, vCenter, Proxmox, MikroTik, Kubernetes, Docker, Sophos Central, cloud platforms, storage, and backup systems. Adding a connector must not require rewriting core orchestration.

Device inventory uses stable IDs, type, environment, owner/tags, approved addresses, capability/version facts, credential references, and last verification time. Do not run unrestricted network discovery or test against production equipment by default. Maintenance/check operations on NextOps's own host are separately protected to prevent self-lockout or self-destruction.

## 16. Persistence, topology, memory, and evidence-grounded RCA

Design explicit records for organizations/environments, users/roles/scopes, assets/endpoints, credential references, connector registrations/capabilities, incidents/events, workflow runs/steps, evidence, action proposals, approvals, executions, audit, topology nodes/edges, documents/chunks/embeddings, and model/prompt/policy versions.

Specify IDs, foreign keys, uniqueness constraints, indexes, migrations, retention, and authorization rules. Use UTC timestamps internally and preserve source time zone, collection time, and clock-skew uncertainty. Make local display time configurable rather than assuming every installation is in one time zone.

PostgreSQL is authoritative. Use relational topology edges first with relationship type, source, freshness, and observed-versus-inferred status; add a graph engine only after a demonstrated need. Keep raw monitoring history in its existing monitoring system when possible rather than duplicating every metric.

Implement scoped short-term/conversation memory, incident memory, infrastructure memory, and topology memory. Retrieved historical text is not proof of current state. Apply expiry/freshness rules and permission-aware caches. Re-index only changed documents; preserve provenance, source version, chunk identity, embedding version/dimension, and content hash. Switching embedding models must trigger a compatible index migration, not mix vectors silently.

RCA combines time-bounded events, dependency paths, device/metric evidence, maintenance/change history, and alternative explanations. Correlation is not proof of causation. Structure output as:

```text
Incident / affected assets / symptoms / time window
Collected evidence with source references and timestamps
Ranked possible causes and supporting/contradictory evidence
Confidence label with justification; explicit unknowns
Next safe diagnostic step
Recommended action, risk, approval requirement, verification/rollback plan
Verified root cause only when evidence supports that designation
```

An alert storm should be deduplicated/grouped before LLM synthesis. Keep evidence collection deterministic and bounded. Do not hallucinate successful tool calls, measurements, or live connectivity.

## 17. API, event ingestion, CLI, and bilingual UI

Use versioned APIs, such as `/api/v1/chat`, `/runs`, `/agents`, `/connectors`, `/devices`, `/incidents`, `/evidence`, `/approvals`, `/audit`, `/users`, `/roles`, `/settings`, and `/models`. Provide separate liveness/readiness endpoints with no sensitive public diagnostics. Preserve/bridge existing API paths when compatibility is needed.

Long investigations create a durable run and return its ID; stream progress through authenticated SSE or a justified alternative. Support reconnect, cancellation requests, pagination, bounded payloads, idempotent command submission, and structured errors. A UI timeout must not erase the job or imply a remote action was cancelled.

Alert ingress requires validated payload schemas, scoped sender authentication/signatures where available, replay/deduplication handling, rate limits, and dead-letter/manual review for malformed events. Do not expose an anonymous endpoint that can trigger arbitrary infrastructure operations.

Provide an operational UI, not only chat: overview, asset inventory/details, incident timeline/evidence, topology, approvals, connector health, audit search, model/resource health, and settings. Make loading, empty, stale, partial, offline, overloaded, denied, pending-approval, and unknown-outcome states explicit. Read-only and mutation modes must be visually distinct. Approval screens show exact target/action/diff, impact, freshness, approver, and expiry—not only an “Approve” button.

Persian is a first-class language: real RTL layout, natural wording, bilingual terminology glossary, mixed-direction isolation for code/IPs/interfaces/timestamps, and English LTR mode. Keep executable commands ASCII/unchanged except explicit secret redaction. Store semantic data independently of localized labels. Host fonts/icons/assets locally with proper licenses; no CDN dependency. Review Persian output for readability, not just the presence of Persian characters.

Show brief decision summaries, tool calls, sanitized results, and final evidence-linked answers. Include keyboard navigation, accessible labels/contrast, responsive layouts, and RTL browser tests. Define reusable spacing/typography/color/component tokens and status semantics before multiplying pages; do not substitute a decorative landing page for the operations console.

## 18. Deployment, environments, and network boundaries

Support `development`, `staging`, and an explicitly enabled `production` profile. Separate databases, volumes, ports, credentials, inventories, and permissions. Never copy production secrets into tests. Shared-host environments remain a shared failure domain; do not describe them as physically isolated.

Default Compose deployment is rootless/non-root where feasible with restricted capabilities, read-only filesystems where practical, health checks, restart policies, resource limits, and internal networks. No privileged containers, host-network shortcuts, or Docker socket mounts without an approved exception. The systemd path uses dedicated users, restricted filesystem access, resource controls, and carefully tested hardening settings.

Only the reverse proxy should be reachable by intended users. Keep databases, inference, queues, telemetry administration, and MCP endpoints internal. Limit SSH and host management to an approved administrative path. Separate UI ingress, service communication, and connector egress logically and enforce the separation with tested host/container rules. Do not assume a host firewall automatically protects every published container port.

Installer scripts must be idempotent, explicit about changes, preflight dependencies/disk/ports/permissions, avoid secret output, preserve existing services, and support safe failure/retry. Do not disable SSH, replace firewall policy, reformat storage, or reboot without authorization and an access-recovery plan. Migrations are versioned and serialized; never run uncontrolled production migrations concurrently from every application replica.

Retain all original scripts and bilingual installation/configuration/security/MCP/development/troubleshooting documentation, organized under `docs/fa` and `docs/en` or equivalent. Document both container and native execution from clean prerequisites to verified health.

## 19. Offline installation and operation

Provide two distinct processes: controlled online provisioning, and offline installation/runtime using a verified bundle.

The bundle contains compatible application artifacts, pinned images or native packages/wheels, frontend assets, required model/tokenizer files, migration scripts, public verification material, and documentation. Do not include production credentials. Inventory all transitive runtime dependencies and external calls, including fonts, model caches, telemetry, license checks, and startup package downloads.

Missing dependencies/models must cause an actionable preflight failure, not an attempt to contact the Internet. Updates are explicit imported releases. Keep GitHub unavailable during offline acceptance tests while allowing only approved infrastructure LAN destinations.

Run a network-restricted smoke/E2E test proving the platform starts, authenticates locally, retrieves local knowledge, performs local CPU inference, uses permitted connectors, and records audit without any external AI or Internet access.

## 20. Reliability, audit, backup, and disaster recovery

Keep security audit distinct from ordinary application logs. Audit requests, authorization decisions, evidence access where relevant, proposals, approval/rejection, credential-use references, execution/verification outcomes, administrative policy changes, and release changes. Include actor/scope, target, policy/model/tool versions, correlation IDs, timestamps, durations, and sanitized errors.

Use append-restricted audit writes and tamper-evident checkpoints where justified. A hash chain on the same machine is not protection against a host administrator who controls all data and keys; stronger assurance needs an independently protected external checkpoint/archive. Say which guarantee actually exists. If durable audit is unavailable, block mutations and surface degraded state.

Observe API/worker/connector health, queue delay, collection errors, inference wait/TTFT/tokens, memory/CPU pressure, database health, audit failures, storage growth, backup age, and restore-test status. Avoid sensitive prompt content or unbounded asset/user IDs as metric labels. Distinguish host, application, and model readiness.

Back up PostgreSQL consistently, permitted evidence, non-secret configuration, encryption recovery material through a separate protected process, and model manifests. Model binaries can be re-imported when that is part of the restore plan. Encrypt backups, define retention, and test restore into an isolated environment.

An off-host backup destination is a required production-readiness decision. Until supplied, label local backup as staging only—not disaster recovery. Define proposed RPO/RTO, then measure restore time and validate recovery access. Account for the management host itself failing and for monitoring/alert delivery outside that host if outage notification is required.

Release rollback includes application/config/model compatibility and database migration strategy. Do not assume rolling back a container reverses a schema change or that every migration has a safe down migration. Use expand/contract or a tested restoration plan where appropriate.

## 21. Test and evaluation strategy

Every implemented feature requires tests at its real boundary. Use unit, PostgreSQL integration, MCP protocol/contract, connector simulator, API, policy/security, browser E2E, migration, restart/recovery, offline, and controlled CPU-load tests. Use isolated fixtures—not real credentials. Unsupported connector features must return explicit errors, not fabricated data.

Mandatory adversarial cases include prompt injection in logs/runbooks/tool descriptions; unauthorized devices and cross-environment evidence; command/SQL injection; secret leakage; forged/stale/replayed approvals; changed targets/arguments after approval; role revocation; duplicate delivery; gateway bypass; DNS/redirect target substitution; model-output schema failure; connector timeout/crash; exhausted disk; unavailable audit/database/model; cancelled or unknown-outcome mutations; and worker restart mid-operation.

Build a versioned bilingual evaluation corpus before selecting the production model. Include Persian, English, and mixed-language requests; realistic synthetic Linux/network/firewall/database/ESXi incidents; ambiguous targets; missing evidence; malicious embedded instructions; and refusal/approval cases. Split development and held-out cases and document their sizes. Have domain and Persian-language review; automated LLM judges are optional local CPU tools, not sole arbiters.

Measure tool/argument correctness, policy outcomes, unsupported-claim rate, evidence-reference correctness, recovery behavior, retrieval quality, Persian readability, schema validity, and latency/resource usage. Do not let a good average hide a catastrophic action category. Zero unauthorized executions in the defined adversarial suite is a release requirement—not proof that all future attacks are impossible.

Report exact commands, commits, test counts, failures/skips, evaluation data/model versions, and hardware used. Never describe mocked tests as real-device validation or unrun tests as passing. Never weaken tests or security boundaries simply to make CI green.

## 22. Milestones and acceptance gates

Security, tests, native Persian support, documentation, and resource awareness apply throughout.

| Phase | Deliverable | Exit condition |
|---|---|---|
| 0 — Discover/design | Repository/host report, threat model, architecture, ADRs, traceability, roadmap, benchmark plan | Owner approves proposed architecture; unavailable facts remain explicitly blocked. |
| 1 — Safe foundation | Repository conventions, CI, API, PostgreSQL/migrations, local auth/scopes, audit, durable jobs, policy/approval contracts, simulator, CPU benchmark harness | Clean install/test path; prohibited actions denied; one local CPU candidate measured where hardware access is available. |
| 2 — First vertical slice | Persian request -> read-only Zabbix event/history + Linux diagnostics -> evidence-linked incident answer -> audit/UI | Bounded end-to-end flow on fixtures and an authorized lab; restart/offline tests pass; no mutation path enabled. |
| 3 — Network/observability | Windows, Cisco, Juniper, Grafana; evidence-linked inventory/topology | Versioned contracts/simulators and scoped lab tests; connector failure isolation demonstrated. |
| 4 — Firewall diagnostics | FortiGate and Sophos; cross-device VPN/routing/policy investigations | Version-verified diagnostics; missing API capabilities stated; no unapproved changes. |
| 5 — Database/virtualization | SQL Server, MySQL/MariaDB, ESXi | Read-only permission/query controls; connector/version/license limitations documented and tested. |
| 6 — Knowledge/RCA depth | Persistent incident memory, retrieval, topology-based correlation, bilingual evaluation improvement | Held-out evidence/quality evaluation; freshness/authorization controls; CPU budgets respected. |
| 7 — Controlled remediation | Small reviewed runbook set, exact-action approval, verify/reconcile/rollback paths | Replay/TOCTOU/unknown-outcome tests pass; authorized lab sign-off before any production mutation. |
| 8 — Production qualification | Hardened deployment, complete UI/docs, offline bundle, release/rollback, off-host backups and restore drill | Signed readiness checklist; measured operating limits/RPO/RTO; known single-host risks accepted. |

Do not treat “phase implemented” as “safe for production.” Read-only production pilots and mutation enablement require separate authorization and evidence. Deferred original features retain explicit status and acceptance criteria.

## 23. Definition of done for each increment

An increment is done only when its implementation is functional, typed, reviewed for policy/security boundaries, tested with recorded results, documented in both required languages where user-facing, included in traceability, and committed locally with a meaningful message. Push or open a PR only through the authorized workflow.

No production path may contain a success-returning stub, an undocumented mock, a silent security fallback, or a TODO that bypasses an invariant. Supported features must be demonstrable; unsupported ones must say so.

Update `PROJECT_STATE.md` with the actual architecture/decisions, completed work, test commands/results, open risks, and blocked dependencies. Update `NEXT_TASK.md` with one concrete next increment and its acceptance test. Record sanitized reproduction steps for unresolved failures. Do not claim asynchronous continuation after the session ends.

## 24. Coordination when multiple coding agents are available

Use parallel work only for independent bounded tasks with disjoint ownership, such as architecture review, CPU benchmark design, security test design, or frontend scaffolding after contracts are agreed. If subagent tools are unavailable, perform the review sequentially without pretending multiple agents ran.

The principal architect owns contracts and integration. The security reviewer checks execution/credential/approval boundaries. The CPU/SRE reviewer checks inference resource isolation and operations. The product/UX reviewer checks scope, native Persian usability, and end-to-end acceptance. Separate worktrees/branches where useful; never let several agents rewrite migrations, shared contracts, or dependency locks simultaneously.

Finish with a principal-engineer integration review. More agents or more generated code is not a success metric.

## 25. Decision rules when information is missing

Resolve ordinary dependency, Python, test, and configuration issues from inspected evidence without repeatedly asking the owner. Prefer the simplest reversible choice and document it. Do not invent missing credentials, network access, product licenses, ownership permissions, or benchmark measurements.

Ask only for information/authorization necessary to cross a real boundary: repository ownership/visibility, infrastructure targets and credentials, production writes, host networking changes, destructive operations, outside services/costs, or acceptance of a consequential design change. When blocked, complete the safe independent work and report the precise blocker.

Use official documentation for runtime, protocol, library, and vendor details. Record consulted versions/dates. If browsing is unavailable, pin already verified project versions and label unverified behavior; do not copy unverified commands into an installer.

## 26. Your first response and first assignment

**Start with Phase 0 now. Do not implement the whole platform or modify the host.**

Return a concrete report with these headings:

```text
1. Executive architecture recommendation
2. Repository findings and preserved components
3. Verified hardware/OS facts and unresolved assumptions
4. Original-spec traceability and explicit revisions
5. Logical architecture and enforced trust boundaries
6. Single-host deployment/network/storage design
7. Repository/module layout and dependency direction
8. CPU-only model/runtime shortlist and staged benchmark plan
9. Resource-budget proposal (clearly unmeasured until tested)
10. Identity, secrets, policy, approvals, and threat model
11. Data model, durable workflow, evidence, topology, and RCA
12. Connector roadmap and real-versus-simulated capability matrix
13. API/UI design, Persian/English behavior, and accessibility
14. GitHub/CI/release/rollback workflow
15. Tests, offline verification, backup/restore, and readiness gates
16. Prioritized implementation increments with acceptance tests
17. Risks, blocked dependencies, and owner decisions required
18. Smallest proposed first implementation change
```

Include textual component/deployment/sequence diagrams and an initial ER model. Deliver actionable file paths, interfaces, test gates, and ADR choices—not only a technology list. Cite repository locations and host observations for findings. Where the environment is unavailable, give a sanitized discovery script and clearly mark the architecture as proposed.

After the owner accepts the roadmap, begin the smallest Phase 1 increment and follow the definition of done. Do not skip directly to eleven connectors, an elaborate dashboard, or a huge local model.

The intended result is a **secure, modular, bilingual, evidence-grounded AI IT operations platform that runs all AI locally on CPUs, starts on the specified single server, uses GitHub for controlled development, and can expand without rewriting the core or weakening its safety boundaries.**

---

## Engineering reference notes

These references informed the proposed additions, not the owner's original requirements. They are starting points for implementation-time verification, not pinned dependency versions or measured claims about the G10 server. Requirements such as the resource budget, module boundaries, phase order, and acceptance gates above are proposed engineering decisions.

- llama.cpp CPU build documentation: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- llama.cpp server configuration: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- llama.cpp tool calling and model-template compatibility: https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
- Official MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP 2025-11-25 transport specification: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP security guidance: https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices
- GitHub Actions secure-use guidance: https://docs.github.com/en/actions/reference/security/secure-use
- Qwen3-8B model card (candidate only): https://huggingface.co/Qwen/Qwen3-8B
- Qwen3-Embedding-0.6B model card (candidate only): https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- OpenVINO latency/concurrency guidance: https://docs.openvino.ai/2026/openvino-workflow/running-inference/optimize-inference/optimizing-latency.html
- vLLM CPU installation overview (alternative only): https://docs.vllm.ai/en/latest/getting_started/installation/cpu/
- pgvector documentation: https://github.com/pgvector/pgvector

---

## Appendix A — Original Persian specification, preserved verbatim

The following is the source document supplied by the owner. Use it for feature detail and traceability. The explicit revisions above govern conflicts in sequencing, enabled inference providers, deployment assumptions, and safety guarantees. Preserving this appendix does not mean that any original feature has already been implemented.

````text
NEXTOPS — AI IT OPERATIONS AGENT

Master Development Specification

تو به عنوان Lead Software Architect، Senior Python Developer، DevOps Engineer، Network Engineer و AI Agent Engineer پروژه NextOps عمل می‌کنی.

هدف تو ساخت یک AI Operations Agent حرفه‌ای برای مدیریت، مانیتورینگ، عیب‌یابی و اتوماسیون زیرساخت IT است.

این پروژه باید از ابتدا با معماری Production-Ready طراحی شود، اما تمام مراحل Development و Testing روی همین Ubuntu Server انجام می‌شود.

1. قانون بسیار مهم

قبل از هرگونه تغییر:

کل repository را بررسی کن.

ساختار فعلی پروژه را شناسایی کن.

فایل‌های موجود را بخوان.

قابلیت‌های فعلی را مشخص کن.

مشکلات معماری و امنیتی را پیدا کن.

dependencyهای موجود را بررسی کن.

تست‌های موجود را اجرا کن.

Git status را بررسی کن.

بدون بررسی پروژه، فایل‌های موجود را بازنویسی یا حذف نکن.

اگر چیزی از قبل پیاده‌سازی شده، آن را حفظ و در معماری جدید ادغام کن.

2. هدف اصلی NextOps

NextOps باید بتواند با استفاده از LLM و MCP:

وضعیت Infrastructure را بررسی کند.

Incidentها را تحلیل کند.

Alertهای Zabbix را تحلیل کند.

مشکلات Network را عیب‌یابی کند.

مشکلات Linux و Windows را بررسی کند.

تجهیزات Cisco و Juniper را مدیریت کند.

Firewallها را بررسی کند.

VMware ESXi را مدیریت و مانیتور کند.

Databaseها را بررسی کند.

Grafana را Query کند.

Logها را تحلیل کند.

ارتباط بین سرویس‌ها و تجهیزات را پیدا کند.

علت احتمالی خرابی را پیدا کند.

راهکار پیشنهاد دهد.

در صورت مجاز بودن، عملیات اصلاحی انجام دهد.

تمام عملیات را Audit کند.

3. زبان و فارسی

پشتیبانی کامل از زبان فارسی الزامی است.

NextOps باید بتواند:

ورودی فارسی را بفهمد.

پاسخ فارسی تولید کند.

سؤال انگلیسی را بفهمد.

سؤال فارسی و انگلیسی را ترکیبی پردازش کند.

نام تجهیزات و commandهای انگلیسی را بدون مشکل پردازش کند.

خروجی فارسی RTL داشته باشد.

در UI از RTL پشتیبانی کند.

Error messageهای انگلیسی را برای کاربر فارسی‌زبان توضیح دهد.

Log و command اصلی را دست‌کاری نکند.

امکان تعیین زبان پاسخ در Configuration وجود داشته باشد.

مثلاً:

language: default: fa supported: - fa - en 

LLM باید بتواند پاسخ را فارسی بدهد ولی command واقعی سیستم را انگلیسی اجرا کند.

مثال:

User:

وضعیت CPU سرورهای ESXi را بررسی کن 

Agent:

در حال بررسی Hostهای ESXi هستم... 

سپس command/API واقعی را اجرا کند.

4. معماری اصلی

معماری باید تقریباً به شکل زیر باشد:

User | v UI / API / CLI | v Agent Orchestrator | +----------------+ | | v v LLM Provider Memory / Topology | v Policy / Security Engine | v MCP Gateway | +------------------------------------------------+ | | | | | | v v v v v v Linux Windows Cisco Juniper Firewall Zabbix | +---------+---------+ | | FortiGate Sophos | +-----------------------------+ | | ESXi Grafana | Databases | +----------+----------+ | | SQL Server MySQL

--- # 5. MCP Architecture هر integration باید MCP جداگانه یا module مستقل داشته باشد. MCPهای اصلی: 1. Linux MCP 2. Windows MCP 3. Cisco MCP 4. Juniper MCP 5. FortiGate MCP 6. Sophos MCP 7. Zabbix MCP 8. Grafana MCP 9. SQL Server MCP 10. MySQL MCP 11. VMware ESXi MCP در آینده architecture باید امکان اضافه کردن موارد زیر را داشته باشد: - Active Directory - VMware vCenter - Proxmox - MikroTik - Kubernetes - Docker - Sophos Central - Cloud platforms - Storage - Backup systems بدون اینکه Core Agent نیاز به تغییر اساسی داشته باشد. --- # 6. MCP Gateway یک MCP Gateway مرکزی ایجاد کن. وظایف: - Service discovery - Authentication - Authorization - Routing - Timeout - Retry - Rate limiting - Logging - Audit - Health check - Error handling مثلاً: ```text Agent | v MCP Gateway | +--> linux +--> windows +--> cisco +--> juniper +--> fortigate +--> sophos +--> zabbix +--> grafana +--> sqlserver +--> mysql +--> esxi 

7. Security

امنیت یکی از مهم‌ترین قسمت‌های پروژه است.

پیاده‌سازی:

RBAC

Roleهای پایه:

viewer operator engineer admin 

هر Role باید permissionهای متفاوت داشته باشد.

مثلاً:

viewer: read-only operator: read limited actions engineer: read diagnostic approved changes admin: full access 

8. Approval System

هر command خطرناک نباید مستقیماً اجرا شود.

مثلاً:

show interface 

می‌تواند Read-only باشد.

ولی:

shutdown interface delete route reload restart service configure firewall rule delete database 

نیازمند approval باشد.

Workflow:

User Request | v Agent | v Risk Analysis | +---- Safe ----> Execute | +---- Dangerous | v Approval | v Execute 

9. Secrets Management

هیچ password یا API key نباید داخل source code باشد.

پشتیبانی:

.env environment variables encrypted secrets secret manager abstraction 

Credentialها باید با:

username password token api_key certificate private_key 

قابل تعریف باشند.

مثلاً:

devices: firewall01: type: fortigate host: 192.168.1.1 credential: fortigate-prod 

و credential جداگانه نگهداری شود.

Password نباید در:

Log

Audit

Prompt

Error message

Git

Database plaintext

ذخیره شود.

10. Audit Logging

هر operation باید Audit شود.

ثبت:

timestamp user role request agent decision target MCP command risk level approval result duration error 

Password و Secret هرگز log نشود.

11. Linux MCP

قابلیت‌ها:

CPU

RAM

Disk

Network

Processes

Services

systemd

logs

journalctl

filesystem

users

ports

sockets

routes

DNS

uptime

load

packages

Command execution باید Policy-controlled باشد.

12. Windows MCP

قابلیت‌ها:

CPU

RAM

Disk

Services

Processes

Event Viewer

Network

DNS

routes

ports

Windows updates

PowerShell

users

AD-related diagnostics

PowerShell commandها باید Policy-controlled باشند.

13. Cisco MCP

پشتیبانی از:

IOS

IOS-XE

قابلیت‌ها:

interfaces

VLAN

trunk

routing

ARP

MAC address table

STP

CPU

memory

logs

BGP

OSPF

DHCP

ACL

NAT

configuration

interface errors

ترجیحاً از SSH/NETCONF/RESTCONF در صورت موجود بودن استفاده کن.

14. Juniper MCP

پشتیبانی از Junos.

قابلیت‌ها:

interfaces

VLAN

routing

ARP

MAC

BGP

OSPF

firewall filters

CPU

memory

logs

configuration

commit status

configuration diff

از روش‌های استاندارد مانند:

NETCONF SSH Junos PyEZ REST API 

در صورت مناسب بودن استفاده کن.

Commandهای destructive نیازمند approval باشند.

15. FortiGate MCP

پشتیبانی از:

REST API

SSH در صورت نیاز

قابلیت‌ها:

interfaces

routes

policies

sessions

VPN

IPsec

SSL VPN

CPU

memory

HA

logs

DHCP

DNS

firewall policies

address objects

services

configuration

امکان تشخیص مشکلات:

VPN down Phase 1 failure Phase 2 failure session drop routing problem policy mismatch DNS problem interface problem 

16. Sophos MCP

Sophos باید به عنوان integration مستقل پیاده‌سازی شود.

در صورت وجود API:

Sophos Firewall API Sophos Central API 

قابلیت‌ها:

firewall status

interfaces

routing

firewall rules

NAT

VPN

IPsec

SSL VPN

DHCP

DNS

active sessions

system health

CPU

RAM

logs

HA

alerts

Agent باید بتواند Incidentهای Sophos را تحلیل کند.

مثلاً:

VPN قطع شده است. 

Agent باید بتواند:

VPN status را بررسی کند.

Phase 1 را بررسی کند.

Phase 2 را بررسی کند.

Routing را بررسی کند.

Firewall policy را بررسی کند.

Logها را بررسی کند.

نتیجه را به زبان فارسی توضیح دهد.

17. Zabbix MCP

پشتیبانی از Zabbix API.

قابلیت‌ها:

hosts

host groups

templates

items

triggers

problems

history

trends

graphs

latest data

events

Agent باید بتواند سؤال‌هایی مثل این را پاسخ دهد:

چرا سرور X امروز چند بار Down شده؟ 

Agent باید:

Zabbix Problemها را بخواند.

History را بررسی کند.

Trigger را تحلیل کند.

Host را بررسی کند.

Correlation انجام دهد.

در صورت نیاز Linux/Windows/Network MCP را فراخوانی کند.

18. Grafana MCP

پشتیبانی از Grafana API.

قابلیت‌ها:

dashboards

folders

panels

datasources

alerts

annotations

dashboard queries

Agent باید بتواند از Grafana برای تحلیل Monitoring استفاده کند.

مثلاً:

چرا latency شبکه در یک ساعت گذشته افزایش پیدا کرده؟ 

Agent بتواند:

Zabbix + Grafana + Network MCP + Firewall MCP 

را با هم استفاده کند.

19. SQL Server MCP

پشتیبانی از Microsoft SQL Server.

قابلیت‌ها:

server health

databases

tables

indexes

connections

sessions

locks

blocking

deadlocks

CPU

memory

disk

query performance

long-running queries

wait statistics

jobs

backup status

Database operations به صورت Read-only پیش‌فرض باشند.

SQL write/delete/drop نیازمند approval باشند.

20. MySQL MCP

پشتیبانی از:

MySQL

MariaDB در صورت امکان

قابلیت‌ها:

databases

tables

indexes

users

connections

processes

locks

slow queries

replication

health

CPU

memory

disk

variables

status

performance

Queryهای:

SELECT SHOW EXPLAIN 

به طور پیش‌فرض مجاز باشند.

اما:

DELETE DROP TRUNCATE UPDATE ALTER 

نیازمند approval باشند.

21. VMware ESXi MCP

پشتیبانی از VMware ESXi.

در معماری، abstraction را طوری بساز که بعداً vCenter هم اضافه شود.

قابلیت‌ها:

host health

CPU

memory

datastore

network

VM list

VM power state

snapshots

disks

NIC

VM performance

alarms

events

logs

برای ارتباط، در صورت امکان از APIهای استاندارد VMware استفاده کن.

Operationهای خطرناک:

power off VM reboot VM delete snapshot delete VM change configuration 

نیازمند approval باشند.

22. Topology / Infrastructure Knowledge

یک مدل Topology ایجاد کن.

مثلاً:

Internet | FortiGate | Core Switch | +---- ESXi | | | +---- VM01 | +---- VM02 | +---- SQL Server | +---- Zabbix | +---- Grafana 

Agent باید بتواند relationshipها را بفهمد.

مثلاً اگر:

VM unreachable 

ابتدا بررسی کند:

VM ↓ ESXi ↓ vSwitch ↓ Physical Switch ↓ Firewall ↓ Network 

23. Incident Correlation

یکی از قابلیت‌های اصلی NextOps باید Correlation باشد.

مثلاً:

Zabbix:

Server unreachable 

همزمان:

Grafana latency ↑ 

و:

Cisco interface errors ↑ 

Agent باید بتواند تشخیص دهد که احتمالاً مشکل اصلی Network است، نه اینکه فقط سه Alert مستقل نشان دهد.

24. Root Cause Analysis

یک RCA Engine ایجاد کن.

خروجی:

Incident Symptoms Evidence Possible Causes Probability Root Cause Recommended Action Risk 

مثلاً:

Root Cause: افزایش packet loss روی interface Gi1/0/24 Evidence: - CRC errors increased - packet loss increased - Zabbix latency increased - Grafana network traffic anomaly Recommendation: بررسی کابل/Transceiver و interface طرف مقابل 

25. LLM Abstraction

LLM را hard-code نکن.

یک abstraction بساز:

LLMProvider 

و امکان providerهای مختلف:

OpenAI Anthropic local Ollama vLLM OpenAI-compatible APIs 

وجود داشته باشد.

هدف نهایی این است که NextOps بتواند بدون وابستگی اجباری به Cloud کار کند.

26. Offline Mode

معماری باید از ابتدا قابلیت Offline داشته باشد.

مثلاً:

ONLINE: NextOps -> Cloud LLM OFFLINE: NextOps -> Ollama/vLLM -> Local Model 

Core Agent نباید به Cloud وابستگی hard-coded داشته باشد.

27. Memory

Memory system ایجاد کن.

حداقل:

short-term memory conversation memory incident memory infrastructure memory topology memory 

Agent باید بتواند Incidentهای قبلی را به خاطر بیاورد.

مثلاً:

این سرور قبلاً هم همین مشکل را داشته؟ 

28. Database

یک Database abstraction ایجاد کن.

ترجیحاً:

SQLAlchemy 

و امکان استفاده از:

PostgreSQL MySQL SQLite 

را در Core فراهم کن.

Database داخلی NextOps از Databaseهای تحت مدیریت خودش جدا باشد.

29. API

Backend API با FastAPI طراحی شود.

Endpointهای اصلی:

/api/chat /api/health /api/agents /api/mcp /api/devices /api/incidents /api/audit /api/users /api/roles /api/settings 

API authentication داشته باشد.

30. UI

یک UI ساده ولی حرفه‌ای ایجاد کن.

قابلیت‌ها:

Chat

فارسی RTL

English LTR

Device inventory

MCP status

Incident list

Logs

Audit

Approval requests

System health

Chat باید امکان نمایش:

Thinking / analysis summary Tool calls Results Final answer 

را به شکل قابل فهم داشته باشد.

اطلاعات حساس نباید در UI نمایش داده شود.

31. Configuration

تمام تنظیمات باید externalized باشند.

مثلاً:

config/ config.yaml devices.yaml credentials.yaml.example policies.yaml 

اما password واقعی نباید در Git ذخیره شود.

32. Device Inventory

یک Inventory abstraction ایجاد کن.

مثلاً:

devices: - name: core-sw01 type: cisco host: 10.0.0.1 credential: cisco-core - name: fw01 type: fortigate host: 10.0.0.254 credential: fortigate-main - name: esxi01 type: esxi host: 10.0.0.20 credential: esxi-main 

33. Health Check

برای تمام MCPها Health Check ایجاد کن.

مثلاً:

Linux ONLINE Windows ONLINE Cisco ONLINE Juniper ONLINE FortiGate ONLINE Sophos ONLINE Zabbix ONLINE Grafana ONLINE SQL Server ONLINE MySQL ONLINE ESXi ONLINE 

34. Error Handling

هیچ MCP نباید باعث crash شدن کل Agent شود.

هر MCP باید:

timeout

retry

structured error

connection error

authentication error

permission error

API error

را مدیریت کند.

35. Observability

خود NextOps باید قابل مانیتور شدن باشد.

پشتیبانی از:

structured logging metrics health endpoints audit logs 

در صورت امکان:

Prometheus Grafana 

را برای monitoring خود NextOps آماده کن.

36. Testing

برای پروژه تست واقعی ایجاد کن.

حداقل:

unit tests integration tests MCP tests security tests API tests agent tests policy tests 

برای تجهیزات واقعی dependency مستقیم نداشته باش.

Mock/Simulator ایجاد کن.

مثلاً:

mock Cisco mock FortiGate mock Sophos mock Zabbix mock ESXi mock MySQL mock SQL Server 

37. Docker

در صورت مناسب بودن:

docker-compose.yml 

برای سرویس‌های داخلی ایجاد کن.

مثلاً:

nextops database redis grafana prometheus 

اما Core NextOps باید بتواند بدون Docker نیز روی Ubuntu اجرا شود.

38. Installation Documentation

این قسمت بسیار مهم است.

یک Documentation کامل ایجاد کن.

حداقل:

docs/ INSTALL_FA.md INSTALL_EN.md CONFIGURATION_FA.md CONFIGURATION_EN.md ARCHITECTURE_FA.md ARCHITECTURE_EN.md SECURITY_FA.md SECURITY_EN.md MCP_FA.md MCP_EN.md TROUBLESHOOTING_FA.md TROUBLESHOOTING_EN.md DEVELOPMENT_FA.md DEVELOPMENT_EN.md 

39. فارسی بودن Documentation

مستندات فارسی باید واقعاً قابل استفاده باشند.

مثلاً:

راهنمای نصب NextOps روی Ubuntu 

شامل:

پیش‌نیازها

نصب Python

ایجاد Virtual Environment

نصب dependencyها

نصب Database

تنظیم Environment Variables

تنظیم LLM

تنظیم MCPها

تنظیم Cisco

تنظیم Juniper

تنظیم FortiGate

تنظیم Sophos

تنظیم Zabbix

تنظیم Grafana

تنظیم SQL Server

تنظیم MySQL

تنظیم ESXi

اجرای Migration

اجرای Backend

اجرای UI

اجرای Test

ایجاد systemd service

تنظیم Firewall

Backup

Restore

Troubleshooting

40. Installation Script

اسکریپت نصب ایجاد کن:

scripts/install.sh 

که بتواند یک Ubuntu تمیز را آماده کند.

همچنین:

scripts/setup.sh scripts/start.sh scripts/stop.sh scripts/test.sh scripts/backup.sh scripts/restore.sh 

ایجاد کن.

اسکریپت‌ها باید idempotent باشند.

41. Systemd

Serviceهای لازم را آماده کن.

مثلاً:

nextops.service 

و در صورت نیاز:

nextops-worker.service 

مستندات systemd را نیز بنویس.

42. Security Documentation

یک Security Guide کامل بنویس.

شامل:

RBAC

Secrets

API authentication

TLS

Audit

command policy

approval

least privilege

network segmentation

backup

credential rotation

43. README

README اصلی پروژه باید حرفه‌ای باشد.

شامل:

NextOps چیست؟ Features Architecture Supported integrations Installation Quick Start Configuration Security Development Testing Offline Mode Roadmap 

README فارسی و انگلیسی ایجاد کن.

44. Development Rules

قوانین:

Python code باید type hint داشته باشد.

PEP8 رعایت شود.

Docstring برای APIهای مهم.

Exceptionها مدیریت شوند.

هیچ secret در source code نباشد.

هیچ credential در Git نباشد.

Logging ساختاریافته باشد.

Unit test برای functionality جدید نوشته شود.

Code duplication کاهش یابد.

Architecture modular باشد.

45. MCP Interface Standard

یک interface استاندارد برای MCPها تعریف کن.

هر MCP باید چیزی شبیه این داشته باشد:

class BaseMCP: name: str version: str async def health_check(self): ... async def list_resources(self): ... async def execute(self, action, params): ... 

Interface را بر اساس MCP واقعی و استانداردهای مناسب پیاده‌سازی کن و اگر abstraction متفاوتی لازم است، آن را منطقی طراحی کن.

46. Tool Risk Classification

Toolها را طبقه‌بندی کن:

READ_ONLY LOW_RISK MEDIUM_RISK HIGH_RISK CRITICAL 

مثال:

show interfaces -> READ_ONLY restart service -> MEDIUM_RISK change firewall policy -> HIGH_RISK delete VM -> CRITICAL 

47. Agent Decision Process

Agent نباید کورکورانه command اجرا کند.

Workflow:

User Intent ↓ Intent Classification ↓ Plan ↓ Permission Check ↓ Risk Analysis ↓ Approval if required ↓ Tool Selection ↓ MCP Execution ↓ Result Validation ↓ Correlation ↓ Final Answer ↓ Audit 

48. Self Verification

Agent بعد از اجرای عملیات باید نتیجه را Verify کند.

مثلاً:

restart service 

نباید فقط command را اجرا کند.

باید:

restart ↓ check status ↓ check logs ↓ verify health 

سپس نتیجه را اعلام کند.

49. Do Not Build Everything Blindly

پروژه را مرحله‌ای توسعه بده.

Phase 1: Architecture + Core

Phase 2: MCP Gateway

Phase 3: Linux / Windows

Phase 4: Cisco / Juniper

Phase 5: FortiGate / Sophos

Phase 6: Zabbix / Grafana

Phase 7: SQL Server / MySQL

Phase 8: ESXi

Phase 9: Memory / Topology / RCA

Phase 10: Security / RBAC / Approval

Phase 11: UI

Phase 12: Offline LLM

Phase 13: Documentation

Phase 14: Production hardening

50. مهم‌ترین قانون اجرای پروژه

هر Phase باید:

Implement شود.

Test شود.

Errorها اصلاح شوند.

Documentation به‌روز شود.

Git commit ایجاد شود.

سپس Phase بعدی شروع شود.

اگر test شکست خورد، خودت علت را پیدا کن و اصلاح کن.

از من برای خطاهای عادی Python، dependency، configuration و test سؤال نپرس؛ خودت ابتدا مشکل را بررسی و اصلاح کن.

فقط در مواردی که نیازمند تصمیم معماری یا اطلاعاتی هست که نمی‌توانی از repository استخراج کنی، سؤال بپرس.

51. اولین کار تو

فعلاً هیچ implementation بزرگی انجام نده.

ابتدا:

1. Repository را کامل بررسی کن. 2. Architecture فعلی را استخراج کن. 3. فایل‌ها و moduleهای موجود را فهرست کن. 4. Testهای موجود را اجرا کن. 5. Dependencyها را بررسی کن. 6. مشکلات فعلی را پیدا کن. 7. Architecture پیشنهادی NextOps را طراحی کن. 8. Roadmap را تهیه کن. 9. Gap Analysis انجام بده. 

سپس یک گزارش کامل ارائه بده:

CURRENT STATE ARCHITECTURE PROBLEMS SECURITY RISKS MISSING COMPONENTS PROPOSED ARCHITECTURE IMPLEMENTATION PLAN TEST PLAN DOCUMENTATION PLAN 

قبل از تغییرات بزرگ، ابتدا همین گزارش را ارائه بده.

بعد از تأیید roadmap، implementation را مرحله‌به‌مرحله شروع کن.

هدف نهایی:

یک AI IT Operations Platform واقعی، Modular، Secure، قابل توسعه، فارسی‌زبان و قابل اجرا به صورت Offline که بتواند Linux، Windows، Cisco، Juniper، FortiGate، Sophos، Zabbix، Grafana، SQL Server، MySQL و VMware ESXi را از طریق یک Agent هوشمند مدیریت و عیب‌یابی کند.


````
