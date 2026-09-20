# Start here: first VMs and the offline Zabbix milestone

[فارسی](../fa/START_HERE.md) · [Index](INDEX.md) · [Roadmap](ROADMAP.md) · [Server plan](SERVER_PLAN.md)

**Updated: 2026-09-20. Status: implementation plan; no VMs or application services have been created by this documentation change.** This guide orders the existing plan; it does not increase the server count or change the archived master prompt. All acceptance cases remain NOT RUN.

## 1. First decision

Keep the existing ESXi host. After the limited Phase 0 preflight and provisioning approval, create these three NextOps VMs in this order:

| Order | VM | vCPU | RAM GiB | Total disk GiB | Initial responsibility |
|---|---|---:|---:|---:|---|
| 1 | `nextops-app` | 8 | 32 | 200 | API, local login, minimal interface, workflow worker, and PostgreSQL as a separate restricted service. |
| 2 | `nextops-ai` | 24 | 128 | 500 | One local CPU inference service and verified model artifacts. No device credentials. |
| 3 | `nextops-connectors-ro` | 4 | 8 | 80 | Protected MCP gateway and isolated read-only Zabbix runner. |
| **Total** | **3 NextOps VMs** | **36** | **168** | **780** | **One serving environment; not measured minimum requirements.** |

Ubuntu Server 24.04 LTS remains the proposed guest baseline, subject to the compatibility review in [ESXi baseline](ESXI_BASELINE.md). Do not replace ESXi with Ubuntu or install NextOps in the ESXi management shell. VM creation order is an operational convenience, not a technical requirement to finish every application feature before creating the AI VM. All three may be provisioned in the same approved work session.

These allocations are initial experiments, not reservations already applied or guarantees of free host capacity. The 24-vCPU AI setting is not 24 simultaneous questions or an instruction to set every thread pool to 24. Begin with one active generation request; compare bounded CPU configurations before resizing. The generous 128 GiB/500 GiB allocation is not the minimum footprint of the first quantized model.

**Zabbix is a separate dependency.** Reuse an existing authorized LAN installation. If none exists, provision one separate approved `zabbix-lab` VM before Stage 1C: provisional 4 vCPU, 8 GiB RAM and 100 GiB disk for a small lab only. Total with this optional lab is 4 VMs, 40 vCPU, 176 GiB RAM and 880 GiB disk. Production Zabbix sizing requires its own workload and retention data. Never assume an instance exists, or rebuild an existing one unnecessarily.

## 2. Phase 0: close only the remaining prerequisites

Do not repeat discovery already supplied by the owner: ESXi 8.0.3 build 24414501; 4 packages, 112 physical cores, 224 logical threads, 4 NUMA nodes and 1,442,743,631,872 bytes RAM. See [hardware evidence](../requirements/HARDWARE_BASELINE.json). These are host totals, not currently available capacity.

Before allocating resources, verify available CPU/memory, existing VM reservations and load, usable datastore capacity/latency, the selected VM compatibility level, and approved network/administrative access. Record actual per-node distribution when available; the 28-core per-node average does not prove placement. Exact CPU SKU is still useful for tuning, but is not a reason to repeat the supplied build/totals or indefinitely postpone safe planning. Runtime compatibility must be verified from guest-visible features before selecting its build.

Record the Zabbix endpoint/version, permitted host groups, protected credential delivery, and a small agreed question set. Define response-time/quality goals and the authorized offline test window. Keep actual addresses, tokens and private inventories outside this public repository. Preserve ESXi recovery access. Obtain approval for provisioning, installation and network rules; this documentation request alone does not authorize them. Missing Zabbix access can block live testing without blocking independent foundation work.

Review the [ESXi supplement](ESXI_BASELINE.md) before configuring topology. Automatic vTopology requires virtual hardware version 20 or later and the appropriate automatic Cores per Socket setting [1]. Verify the saved result: the standalone Host Client has a documented case of replacing automatic assignment with one core per socket [2]. Do not create vCenter merely for this project, guess a NUMA node to pin, change BIOS settings, or upgrade existing VMs without a reviewed plan. Review host patches/firmware before a production pilot; do not turn that review into an unapproved host upgrade.

## 3. Phase 1: five steps, one completion gate

Stages 1A–1E are work packages inside Phase 1, not new top-level phases. Phase 1 remains incomplete until 1E passes for the deployed profile.

| Stage | Work and VM placement | Required checkpoint |
|---|---|---|
| **1A — Application and safety foundation** | Create `nextops-app` first. Establish guest administration, locally stored configuration, typed contracts, PostgreSQL/migrations, local authentication/scopes, durable requests and audit. Prepare the minimal UI/API and deny-by-default policy with synthetic fixtures. | Local login and durable state work; forbidden operations fail; permissions/audit tests pass. No target credentials or production-device access in this stage. |
| **1B — Local CPU answer service** | Create `nextops-ai` second. Import one reviewed quantized multilingual model and compatible pinned CPU runtime. Authenticate the internal service, enforce resource limits and verify local artifact loading. | A fresh Persian question and English question receive actual locally generated answers; cold-load without Internet works. Record latency and resource measurements. General model answers do not count as Zabbix evidence. |
| **1C — Read-only Zabbix evidence** | Create `nextops-connectors-ro` third. Implement the MCP gateway and separate Zabbix runner identities. Provision a restricted Zabbix identity through an approved secret path only after Stage 1A controls pass. | Real authorized API reads yield scoped, timestamped evidence and deterministic counts. Writes and unsupported methods are denied. Token/error/output handling is sanitized. Fixtures remain labeled as fixtures. |
| **1D — The first useful answer** | Connect the application request, read-only collection, deterministic aggregation, local CPU synthesis and source display. Use the same three VMs. | A new Zabbix question produces a readable Persian/English explanation matching captured evidence, with scope, freshness, missing data and audit. A raw JSON response or cached demo is insufficient. |
| **1E — Offline acceptance** | Test all three VMs and a fresh browser with WAN blocked and the authorized Zabbix LAN route available. Test service restart, permitted reboot, failure cases and bounded load. | ZBX-01–ZBX-08 and all applicable OFF-01–OFF-10 cases have recorded outcomes; no skipped applicable case is presented as passing. Phase 1 finishes only after live-data, security and offline gates pass. |

The source specification already requires Zabbix host/problem/history analysis and auditing; this guide makes the owner's later Zabbix-first delivery order actionable. Direct Linux diagnostics, full topology, advanced RAG, every other connector and remediation are not prerequisites for the first answer.

## 4. Connections and credentials from day one

The application initiates authenticated internal requests to the AI service and MCP gateway; results return over those connections. The connector runner alone initiates approved Zabbix API calls. The AI cannot directly query Zabbix, read target credentials, reach the managed-device LAN or call external AI. The app has no direct managed-device access. Only intended clients and the approved administration path can reach the application ingress.

Keep PostgreSQL internal to the app VM initially, with separate service roles and restricted storage. Gateway and runner remain distinct processes/identities even on the same connector VM. An allowlisted API token is delivered only to its runner. Additional NICs or port groups are not permission to route or bridge networks; enforce destination/service rules and verify there is no bypass. Choose actual IPs, VLANs and ports from the operator's environment, not examples copied into public documentation.

Runtime has no Internet dependency. Provision dependencies through a controlled download/import step and keep the AI runtime isolated. Models, tokenizer files, UI assets, local login, key access, certificates and required data must survive restart. GitHub and package registries are release/provisioning sources only. Do not enable public SSH or attach a privileged GitHub Actions runner to these serving VMs. Untrusted builds/tests use a separate disposable environment without service credentials; count its concurrent resource use separately.

## 5. Do not confuse creation order with restart order

Creation order is **app → AI → read-only connectors**. After installation, the operational startup sequence is dependency-aware: local storage/key/time prerequisites and PostgreSQL first; AI and gateway/runner services may start independently; the API may provide login and truthful degraded status while dependencies warm; the worker admits a Zabbix investigation only when the required database, audit, authorization, model and connector checks pass. Use bounded readiness/retry behavior, not fixed sleeps or Internet connectivity tests. Zabbix unavailability must not block general local Q&A when its own dependencies are healthy.

After a restart, recover durable jobs without blindly replaying remote effects. Guest service readiness must be checked even if ESXi has already powered on the VM. Shutdown should drain or persist work before stopping its dependencies; do not confuse a stopped browser request with a cancelled remote operation.

## 6. Add later, not now

| When | VM decision |
|---|---|
| Phase 2 | Keep 3; add bounded Linux diagnostics and Zabbix history within the existing read-only boundary. |
| Phase 3 | Recommend adding `nextops-db` (8 vCPU, 64 GiB RAM, 300 GiB disk); migrate and test restore before removing the old database service. Total 4 VMs / 44 vCPU / 232 GiB RAM / 1,080 GiB disk. This is an isolation decision, not a measured throughput requirement. |
| Phases 4–6 | Keep 4 unless measured demand or an additional trust boundary justifies more. A reviewed small read-only pilot may remain on 3 as described in SERVER_PLAN. |
| Phase 7 | Add `nextops-executor-rw` (4 vCPU, 16 GiB RAM, 80 GiB disk) only for separately approved remediation. Total 5 VMs / 48 vCPU / 248 GiB RAM / 1,160 GiB disk. |
| Phase 8 | No automatic extra VM: qualify 5 with remediation or 4 read-only. Require an independent backup destination and an actual restore drill. Same-host replicas/backups do not protect against loss of the G10. |

Do not create a standalone database, write executor, dedicated monitoring VM, per-connector VMs, Kubernetes cluster, separate vector service or second AI VM just to begin Phase 1. Basic health/metrics/audit still belong in the first delivery; only the extra infrastructure is deferred.

## 7. Handoff and validation record

After each stage, record its status, VM roles actually created, versions, exact test commands/results, remaining blockers and the next checkpoint in [PROJECT_STATE](../PROJECT_STATE.md) and [NEXT_TASK](../NEXT_TASK.md). A check mark requires evidence; VM allocation, model startup and documentation publication are different from the first accepted Zabbix answer. Architecture approval, host access, model runs, VM provisioning, network isolation and acceptance tests are not claimed by this guide.

Sources: existing [server plan](SERVER_PLAN.md), [offline contract](OFFLINE_RUNTIME.md), [hardware record](../requirements/HARDWARE_BASELINE.json), [master specification](../requirements/NEXTOPS_MASTER_PROMPT.md), and the owner's subsequent clarifications. Resource budgets and ordering are engineering proposals. Official topology references checked 2026-09-20 support only the named ESXi behaviors, not NextOps performance.

[1]: https://knowledge.broadcom.com/external/article/438023
[2]: https://knowledge.broadcom.com/external/article/425838
