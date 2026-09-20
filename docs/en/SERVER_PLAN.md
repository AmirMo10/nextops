# G10 server plan and the first Zabbix deliverable

[فارسی](../fa/SERVER_PLAN.md) · [Roadmap](ROADMAP.md) · [Offline contract](OFFLINE_RUNTIME.md) · [CPU plan](CPU_AI.md)

**Planning revision: 2026-09-20, updated with owner-supplied ESXi output.** Hardware totals below come from the supplied command output; VM allocations remain proposals, not measured performance or deployed infrastructure. The first implementation milestone must end with local AI answering questions about Zabbix status. Security and offline operation are not deferred.

## Hardware evidence update

Source: the owner supplied output from `esxcli hardware cpu global get` and `esxcli hardware memory get`. No direct host connection or independent measurement was performed. The sanitized machine-readable record is [HARDWARE_BASELINE.json](../requirements/HARDWARE_BASELINE.json); it contains no hostname, address, serial number or credential.

| Field | Reported value / calculation | Evidence status |
|---|---|---|
| Host platform | VMware ESXi | Identified from the supplied command session; version/build unknown |
| CPU packages | 4 | Reported |
| Physical CPU cores | 112 | Reported; replaces the ambiguous earlier 90-CPU estimate |
| Logical CPU threads | 224 | Reported; not 224 physical cores |
| Hyperthreading | Active, supported and enabled | Reported |
| Physical memory | 1,442,743,631,872 bytes | Reported total, not free memory |
| Converted physical memory | 1,343.6597 GiB = 1.3121677 TiB = 1.4427436 decimal TB | Calculated from the byte count |
| NUMA nodes | 4 | Reported; per-node CPU/memory mapping not supplied |
| Average cores per package / NUMA node | 28 / 28 | Arithmetic averages, not proof of equal distribution |
| Average memory per NUMA node | 335.9149 GiB | Arithmetic average, not measured per-node or available memory |

The raw output also reports `HV Support: 3` and `Reliable Memory: 0 Bytes`. These values are retained without inferring CPU model, ECC condition, a hardware fault or a completed memory-health test. Do not change BIOS settings on their basis. The no-GPU constraint remains the owner's requirement; these two commands alone are not a GPU inventory.

This evidence replaces the old approximately 90 CPU / 1 TB assumption wherever it appears in current planning. The archived master prompt keeps the original wording. Installed totals do not establish free resources, a performance target, a VM-count limit, storage capacity or the exact server model.

## 1. What is being counted

Plan for **one existing physical G10, initially three NextOps virtual machines (VMs)**. Grow to four for a separate database boundary and five when a separately isolated change executor is enabled. These are recommended service placements, not vendor minimum requirements. One connector family does not require one VM. The larger reported host does not require more VMs.

The table counts one serving NextOps environment only. It excludes the existing Zabbix installation, managed devices, the hypervisor, developer workstations, temporary test environments and off-host backup storage. Reuse a reachable authorized LAN Zabbix instance. If no instance is available, add one separate small lab Zabbix VM; do not label it a production monitoring deployment.

**Preserve the existing ESXi host.** Ubuntu 24.04 LTS remains a proposed guest OS for the NextOps VMs, subject to compatibility checks. Compose/systemd and the application run inside those guests, not in the ESXi management shell. Do not replace ESXi with Ubuntu, install an application runtime on the hypervisor, or introduce nested virtualization for this plan. Check ESXi build, license/per-VM limits and guest compatibility before provisioning. Earlier generic Ubuntu-host proposals do not authorize a host reinstall.

## 2. Recommended runtime VM count by phase

| Phase | Required user-facing result | NextOps VMs | Change in placement |
|---|---|---:|---|
| 0 — Discovery and design | Verified inventory, workload assumptions and approved plan | 0 new runtime VMs | Use the supplied totals; inspect the remaining unknowns without provisioning. |
| 1 — Offline Zabbix status MVP | A new Persian/English question receives a locally generated, evidence-linked Zabbix status answer with Internet blocked | 3 | `nextops-app`, `nextops-ai`, `nextops-connectors-ro`; database initially inside app VM as a separate restricted service. |
| 2 — Linux/Zabbix investigation | Add bounded history and direct Linux diagnostics to explain incidents | 3 | Add isolated runner processes, not another server by default. |
| 3 — Network and observability integrations | Windows, Cisco, Juniper and Grafana diagnostics | 4 recommended | Move PostgreSQL to `nextops-db` for separate data access, maintenance and recovery controls. |
| 4 — Firewall diagnostics | FortiGate/Sophos investigations | 4 | Add read-only runners within the approved connector boundary. |
| 5 — Databases and virtualization | SQL Server, MySQL/MariaDB and ESXi diagnostics | 4 | Existing managed databases/ESXi hosts are targets, not new NextOps servers. |
| 6 — Knowledge and RCA | Local documents, incident memory and better evidence correlation | 4 | Use the AI VM for bounded CPU embeddings when enabled; use existing data/evidence storage. |
| 7 — Controlled remediation | Approved runbooks with exact-action approval, verification and reconciliation | 5 when enabled | Add `nextops-executor-rw` with narrowly scoped change credentials; retain the read-only boundary. |
| 8 — Production qualification | Offline restart/restore, measured limits and recovery evidence | 5 with remediation; 4 read-only | No automatic extra VM. An independent backup destination is a separate production requirement. |

The Phase 3 database split is a design recommendation for lifecycle and access isolation, not an assertion that a fourth VM is needed for throughput. A small read-only pilot may remain on three with a documented exception and successful isolation/recovery tests. Do not add services merely because a phase number changes. Extra connector groups or inference replicas need measured contention or a new trust boundary.

Optional local observability can use a **sixth VM** once the five-VM layout exists. It is not a prerequisite for the first Zabbix answer. Temporary fixture CI can use one disposable test VM, but a one-VM test setup does not validate the isolation of a three/five-VM production topology. Schedule complete-topology tests separately and account for every concurrently running VM.

## 3. Revised initial allocations

Assumptions: one NextOps environment, one Zabbix API instance, bounded on-demand status queries, one active generation request initially, and no foundation-model training. Asset count, event volume, simultaneous users and response-time goals are not yet known. The following numbers are **starting budget proposals**, not minimums or performance guarantees. RAM and disk are GiB; each disk figure includes OS and application/data allowance.

| VM | First used | vCPU | RAM GiB | Disk GiB | Responsibilities |
|---|---|---:|---:|---:|---|
| `nextops-app` | Phase 1 | 8 | 32 | 200 | TLS/static UI, API, local authentication, durable worker; separate PostgreSQL service initially. |
| `nextops-ai` | Phase 1 | 24 | 128 | 500 | One local CPU generation service; verified model artifacts; optional later CPU embedding worker within the same budget. |
| `nextops-connectors-ro` | Phase 1 | 4 | 8 | 80 | Protected MCP gateway and separately restricted read-only runners; initially Zabbix only. |
| `nextops-db` | Recommended Phase 3 | 8 | 64 | 300 | PostgreSQL state/jobs/audit and approved evidence storage; separate roles and evidence service/filesystem permissions. |
| `nextops-executor-rw` | Phase 7 only | 4 | 16 | 80 | Authenticated executor, scoped change credentials and reviewed runbooks; disabled until its safety gates pass. |

| Profile | Count | Sum vCPU | Sum RAM GiB | Sum provisioned disk GiB |
|---|---:|---:|---:|---:|
| First Zabbix milestone | 3 | 36 | 168 | 780 |
| Separated database | 4 | 44 | 232 | 1,080 |
| Controlled-remediation layout | 5 | 48 | 248 | 1,160 |
| Optional observability VM, additional only | +1 | +4 | +16 | +200 |
| Optional small Zabbix lab VM, additional only | +1 | +4 | +8 | +100 |

**Change from the previous budget:** reduce the AI VM's initial proposal from 32 to 24 vCPU and recompute the profile totals. This is a topology-aware experiment, not a finding that 24 is faster or that 32 cannot work. The arithmetic average is 28 physical cores per NUMA node; a 24-vCPU candidate is intended to test a one-node placement with headroom, conditional on the actual mapping and contention. No node is reserved or pinned by this document. A VM allocation is not the inference thread count or concurrent-question count.

The AI VM's 128 GiB is a generous experiment/artifact-growth budget, not a requirement for a 7–9B quantized model. Reduce it if measurements justify that. Even though 128 GiB is below the arithmetic per-node average, a single-node fit is not proved until actual local memory and other workloads are checked.

Do not subtract 48 vCPU from 112 cores or 224 threads and call the difference free physical CPUs. vCPU configuration, physical capacity, reservations and observed utilization are different quantities. Keep measured headroom for ESXi, existing VMs, storage services, builds and tests. Avoid sustained CPU overcommit and model swap dependence.

Disk totals are virtual capacity reservations, not IOPS, actual used space, RAID usable capacity, snapshot space or backups. Keep the operator-approved datastore margin; account separately for model versions, WAL, retention, backup staging and restore tests. Do not duplicate all Zabbix history into NextOps. Production Zabbix sizing requires its own item rates, intervals, retention and storage measurements; the lab row does not size production Zabbix.

### NUMA-aware CPU evaluation

Broadcom's ESXi 8.0 guidance recommends sizing for workload demand and keeping a VM's CPU and memory within a physical NUMA node when feasible. Larger VMs require attention to vNUMA; additional vCPUs do not automatically improve performance [7]. Apply version-specific details only after identifying this host's build.

Proposed experiments: start with the 24-vCPU VM and one active request; compare bounded generation/prompt thread settings within that allocation. If useful and authorized, compare 16-, 24- and 28-vCPU configurations after verifying node sizes. Treat 32-vCPU or larger trials as separate topology experiments rather than automatic upgrades. Keep model, quantization, prompt/output limits and evaluation cases constant.

Record host CPU ready/co-stop, local versus remote memory, ballooning/swap, guest-visible CPU/NUMA/ISA, queue time, first-token and full-answer latency, errors and bilingual correctness. A guest NUMA view alone does not prove physical placement. Do not invent a CPU model, AVX/AVX-512/AMX support, local memory bandwidth, tokens/second or supported user count.

For confirmed ESXi 8.x with virtual hardware 20+, evaluate the supported automatic topology setting; do not impose it on an unidentified version. Avoid manual CPU/NUMA affinity and advanced tuning as defaults. Cores-per-socket and CPU-hot-add behavior are version-dependent [7]. No BIOS, host power-policy or hyperthreading changes are authorized by this plan.

### Remaining read-only discovery

The CPU count, memory total and NUMA count have already been supplied; do not repeatedly request them. Useful next commands are `esxcli system version get` and `esxcli hardware cpu list` [8][9]. Gather full CPU topology privately; a shortened excerpt can identify a model but cannot establish the complete map. Obtain available memory, existing workload utilization/reservations, per-node memory and datastore capacity/latency through authorized host monitoring. Share only sanitized summaries; no credentials, IPs, serials or private inventory in this public repository.

## 4. First-milestone service and trust placement

```text
User browser on an authorized local route
  -> app VM: local login, API and durable request
  -> connector VM: policy checks and read-only Zabbix API request
  -> existing Zabbix over the LAN
  -> app VM: scoped, sanitized evidence and deterministic counts
  -> AI VM: local CPU explanation using only supplied evidence
  -> app VM: evidence-linked answer, source time and audit
```

The AI VM has no device credentials and no route to the management LAN or Internet. The app has no direct device route or target credentials. The gateway runs policy checks; only its isolated Zabbix runner receives the read-only token. Gateway and runners remain distinct identities/processes even when sharing a VM. The initial database has independent service roles and restricted volumes, not a shared unrestricted app account. The optional write VM later rechecks authorization and approvals at its own boundary.

Serve UI, dictionaries, documentation assets and models locally. Use the provisioned local login/key/certificate path. All VMs must start without GitHub, package registries or Internet identity services. Internet loss must not change the inference provider. Zabbix must itself be reachable locally for fresh readings; an Internet-only monitoring endpoint cannot satisfy the live-offline requirement.

## 5. What Phase 1 must actually deliver

**Completion statement: with Internet blocked and Zabbix reachable over the LAN, a user asks for Zabbix status and receives a new local CPU-generated answer grounded in authorized API evidence.** A running model, an API token, a JSON dump, or a mocked screenshot alone does not complete this milestone.

Deliver the smallest complete loop: local login; question submission in a minimal web view or authenticated CLI; named allowlisted collection; typed evidence and deterministic aggregation; bounded local generation; response/source display; audit. Broad Linux SSH collection, every connector, advanced RAG, topology animation and autonomous remediation are not prerequisites for this first answer. Linux diagnostics remain Phase 2.

Distinguish these three meanings of status:

| Status dimension | Phase 1 response obligation |
|---|---|
| Zabbix API reachability | Report the actual authenticated call outcome and detected API version; do not infer that all monitoring processes are healthy. |
| State of the monitored estate | Report authorized enabled/disabled hosts, active problems by severity, affected assets, maintenance/suppression context and last observation times. |
| Health of the Zabbix monitoring engine | Report fresh configured self-monitoring items when accessible; otherwise explicitly mark this aspect unknown, not healthy. |

Zabbix documents its API as part of the web frontend [1]; successful API access is therefore not by itself a full engine-health test. Host `status` is enabled/disabled, not a proof of reachability [2]. Model explanations must respect those distinctions. Where configured, internal items such as `zabbix[uptime]` or `zabbix[queue]` provide additional engine evidence [6]; do not create missing items silently.

## 6. Read-only Zabbix adapter contract

Use a dedicated API identity with approved host-group visibility and a non-empty method allowlist. API tokens inherit their user's permissions [3]; token creation alone does not make an integration read-only. Test role restrictions [4] and independently deny unsupported methods in the gateway.

Start with the version-compatible subset of `apiinfo.version`, `host.get`, `hostinterface.get`, `problem.get`, `trigger.get` and `item.get`. Add bounded `history.get` and `event.get` only for questions that need historical evidence. Authenticate methods according to the detected version; `apiinfo.version` is a version probe, not proof that authenticated reads succeeded. No arbitrary method selection by the model. Use explicit field selections, target scopes, time ranges, row/byte caps and deadlines; redact before persistence/model use.

Use unresolved-problem semantics for current status; do not label recently resolved problems as active [5]. Do not apply a 'last hour' creation filter to an all-current-problems total: older unresolved incidents still matter. Display suppression/maintenance filters. Compute totals deterministically with the same authorized scope and filters as detail rows. Distinguish total counts from a bounded displayed sample; if queries are incomplete or collected at different times, disclose partial scope and the observation window. An empty result with uncertain permissions is not evidence of a healthy fleet.

The initial named tools can be `zabbix.status_overview`, `zabbix.host_status`, `zabbix.active_problems` and `zabbix.monitoring_health`. These are proposed NextOps tool names, not Zabbix API methods. Every answer records evidence IDs, source method/object IDs where appropriate, collection time, scope, filtering and missing data. Never ask the model to manufacture counts from memory.

## 7. Phase 1 acceptance evidence

All cases below are **NOT RUN**. Do not mark them passed until executed in an authorized environment.

| ID | Acceptance gate |
|---|---|
| ZBX-01 | A new Persian question and a new English question about current status complete using a real authorized Zabbix instance and the local CPU model. Fixtures are separately labeled. |
| ZBX-02 | Displayed facts match captured scoped API results; counts are deterministic; enabled/available/unknown and active/resolved are correctly distinguished. |
| ZBX-03 | Remove server and browser Internet access while preserving approved LAN access; ask new questions; no external AI, CDN, login, model or package call occurs. |
| ZBX-04 | Cold-start model, API, database and connector services offline, then use a fresh local login. Include an authorized reboot check with recovery access before qualifying offline restart. |
| ZBX-05 | Revoke/expire the token, make Zabbix unreachable and simulate missing/stale items: disclose unavailable evidence without inventing status; local general Q&A remains available. |
| ZBX-06 | Requests to acknowledge/close a problem, execute a script or change configuration are denied. Prompt injection in an event name cannot bypass policy or expose secrets. |
| ZBX-07 | Capture the model/runtime version, VM allocation, guest/host NUMA placement, CPU ready/co-stop, memory pressure, queue delay, first-token time, full answer time and error rate. Agree latency/quality targets before evaluation; no performance promise is inferred from RAM. |
| ZBX-08 | Permission checks, durable request/evidence references and sanitized audit are demonstrated. Missing mandatory audit causes an explicit degraded/failed diagnostic path, not unlogged success. |

A representative request is: "Summarize the current Zabbix status, active problems and any missing or stale evidence." The Persian evaluation includes the equivalent natural wording, mixed technical identifiers and a host-specific follow-up. The answer must separate confirmed observations from possible explanations and safe suggestions.

## 8. Physical-host and backup limits

These layouts propose no additional physical application server for the pilot, subject to available-capacity verification. They provide no host-level high availability. If the G10 fails, all its VMs fail together. Before production, designate and test an independent backup destination such as an existing approved LAN backup server/NAS; it does not have to be a newly purchased compute server. A backup VM on the same G10 is staging, not protection from G10 loss.

An availability requirement that survives G10 loss needs a separate multi-host, storage, quorum/fencing, identity and recovery design. Do not promise that buying one extra box or adding VM replicas automatically achieves it. No VM provisioning, direct server access, Zabbix connection or load test was performed for this documentation change.

## Sources and precedence

Original section 17 requires Zabbix hosts/problems/history analysis. The owner's clarification moves the first Zabbix answer into Phase 1; Linux enrichment follows in Phase 2. The newly supplied ESXi totals replace the earlier approximate hardware assumptions. This revision proposes 24 rather than 32 vCPU for initial AI benchmarking and updates the arithmetic totals; VM counts and the first deliverable remain unchanged. The archived master prompt remains unchanged. Reported hardware, calculations, proposals and actual tests are distinct evidence categories.

Existing Zabbix references are retained; 7.4 is a reference, not an assumption about the installed version. Broadcom references [7]–[9] were consulted for this hardware-planning revision on 2026-09-20. Their capabilities do not establish this host's performance.

[1]: https://www.zabbix.com/documentation/7.4/en/manual/api
[2]: https://www.zabbix.com/documentation/7.4/en/manual/api/reference/host/object
[3]: https://www.zabbix.com/documentation/7.4/en/manual/web_interface/frontend_sections/users/api_tokens
[4]: https://www.zabbix.com/documentation/7.4/en/manual/web_interface/frontend_sections/users/user_roles
[5]: https://www.zabbix.com/documentation/7.4/en/manual/api/reference/problem/get
[6]: https://www.zabbix.com/documentation/7.4/en/manual/config/items/itemtypes/internal
[7]: https://knowledge.broadcom.com/external/article/438023
[8]: https://developer.broadcom.com/xapis/esxcli-command-reference/latest/namespace/esxcli_system.html
[9]: https://developer.broadcom.com/xapis/esxcli-command-reference/latest/namespace/esxcli_hardware.html
