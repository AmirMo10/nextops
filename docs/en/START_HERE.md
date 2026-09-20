# Start here: first VMs and the offline Zabbix milestone

[فارسی](../fa/START_HERE.md) · [Index](INDEX.md) · [Roadmap](ROADMAP.md) · [Server plan](SERVER_PLAN.md) · [Dedicated Zabbix](ZABBIX_SERVER.md)

**Updated: 2026-09-20 — dedicated Zabbix deployment profile.** This is an implementation plan, not a report of provisioned VMs or completed tests. It updates the former small-lab recommendation without increasing the number of NextOps core VMs. Read the [deployment amendment](../requirements/DEPLOYMENT_UPDATE.md) with the active prompt; all non-conflicting safety and feature requirements remain in force.

## 1. First decision

Keep the existing ESXi host. After the remaining Phase 0 preflight and provisioning authorization, create the three NextOps VMs in the existing order and prepare the dedicated Zabbix dependency before Stage 1C:

| Order / deadline | VM | vCPU | RAM GiB | Total disk GiB | Responsibility |
|---|---|---:|---:|---:|---|
| 1 | `nextops-app` | 8 | 32 | 200 | Local login, API/UI, durable worker and independent restricted NextOps PostgreSQL service |
| 2 | `nextops-ai` | 24 | 128 | 500 | One local CPU inference service and verified model artifacts; no device credentials |
| 3 | `nextops-connectors-ro` | 4 | 8 | 80 | Protected MCP gateway and isolated read-only Zabbix runner |
| Ready before 1C; may be prepared alongside 1A/1B | `zabbix-server` | 4 | 16 | 200 | Zabbix, its own PostgreSQL, web frontend/API and Agent 2 |
| **Combined total** | **3 NextOps + 1 Zabbix = 4 VMs** | **40** | **184** | **980** | **One proposed serving profile** |

Ubuntu Server 24.04 LTS is the proposed guest OS after compatibility review, not an ESXi replacement. Do not install these services in the ESXi management shell. DS-C is the capacity-based datastore proposal; it is not a performance or resilience certification. Actual names, addresses and credentials remain in private deployment inventory.

The three NextOps VMs alone still total 36 vCPU / 168 GiB RAM / 780 GiB disks. Do not mistake the fourth monitoring VM for a new NextOps database VM. `zabbix-server` replaces the old 4-vCPU/8-GiB/100-GiB lab recommendation for this new-server path; do not create both. Inspect and reuse a suitable authorized existing Zabbix instance instead when already available. Never duplicate or reinstall an existing server merely to match this document.

All VMs may be prepared in one approved session. Creation order does not require completing every app feature before creating the AI VM. The AI budget is an experiment, not 24 concurrent questions or 24 mandatory threads; start with one active generation request. Exact CPU SKU, guest-visible features and NUMA placement require their separate evidence.

The [Zabbix guide](ZABBIX_SERVER.md) contains its full 200-GiB LVM layout, proposed native Zabbix 7.0 LTS / PostgreSQL 16 / Nginx / PHP-FPM stack, seven-day history / ninety-day numeric-trend proposal, role restrictions and self-monitoring gates. These are recommendations, not installed settings or workload guarantees.

## 2. Phase 0: close only remaining prerequisites

Already supplied: ESXi 8.0.3 build 24414501; four packages, 112 physical cores, 224 logical threads, four NUMA nodes, 1,442,743,631,872 memory bytes and point-in-time datastore values. Read [HARDWARE_BASELINE](../requirements/HARDWARE_BASELINE.json), [ESXI_BASELINE](ESXI_BASELINE.md) and [STORAGE_PLAN](../STORAGE_PLAN.md). Do not ask for supplied totals as missing or confuse them with free capacity.

Verify available CPU/RAM, existing load/reservations, outstanding datastore commitments, backing storage health/latency, VM compatibility and guest ISA, approved networks and recovery access. The 28-core per-node average is not measured distribution. Refresh free bytes at the change window. Keep system/boot volumes and DS-A/DS-B outside this initial allocation.

Define the authorized Zabbix endpoint/version, permitted host groups, protected credential delivery, self-monitoring items, target question set and response-quality/latency goals. When creating the new server, verify monitoring data before the live AI test. Missing target access blocks live validation, not unrelated foundation work. No indefinite planning loop over already supplied data.

Preserve ESXi recovery access. Obtain approvals for provisioning, installation, network rules and target access. This documentation is not permission for production changes, stress tests, model downloads, patches or reboots. Read the ESXi supplement before topology changes; verify supported automatic settings and the saved result, especially with the standalone Host Client. Do not guess NUMA pins or create vCenter solely for this project.

## 3. Phase 1: five steps, one completion gate

Stages 1A–1E are work packages within Phase 1. Prepare the Zabbix dependency alongside them; it does not introduce another top-level phase.

| Stage | Work and placement | Required checkpoint |
|---|---|---|
| **1A — App and safety** | `nextops-app`: guest administration, typed contracts, PostgreSQL/migrations, local identity/scopes, durable requests, audit, minimal UI/API and fixture-based policy tests | Login and state work; prohibited actions denied; mandatory audit tested before real target credentials |
| **1B — CPU answers** | `nextops-ai`: approved local model/runtime import, internal authentication, resource budgets and persistent artifacts | New Persian/English answers and offline cold loading measured; general model output is not monitoring evidence |
| **Zabbix preparation — before 1C** | `zabbix-server`: separate PostgreSQL mount/instance, monitoring service/frontend, self-monitoring and scoped API account | Actual services and relevant fresh data available; database separate from NextOps; restricted API policy verified |
| **1C — Read-only evidence** | Gateway and separate Zabbix runner on `nextops-connectors-ro`; deliver token through the approved secret path after 1A | Real scoped API data, deterministic counts and timestamps; writes and unlisted methods denied |
| **1D — Useful answer** | Connect question, collection, aggregation, local synthesis, source display and audit using the four-VM profile | New Zabbix question answered from captured evidence with freshness, scope and unknowns; not raw JSON or a cache demo |
| **1E — Offline acceptance** | Test the actual profile and fresh browser with Internet blocked and approved local routes retained | Recorded ZBX-01–ZBX-08 and applicable OFF-01–OFF-10, including Zabbix restart, fresh login, failure behavior and measured limits |

The phase ends with the accepted answer, not with VM creation, a model hello-world or the Zabbix dashboard alone. Direct Linux diagnostics, advanced RAG, full topology, every connector and remediation are not prerequisites. Installing a read-only OS monitoring agent is administrative monitoring setup, not implementation of the future direct Linux connector or permission for AI-initiated changes.

## 4. Connections and credentials from day one

The app makes authenticated internal requests to the model and MCP gateway. Only the isolated Zabbix runner reads the Zabbix API. The model receives sanitized evidence, not tokens, database credentials or a management-device route. Gateway and runners retain separate identities even on the same VM. The app cannot bypass the gateway to query managed systems.

Zabbix monitors continuously; NextOps retrieves evidence on demand when a user asks. A new API call may return an older measurement, so show both source time and collection time. Separate API reachability, monitored-estate status and monitoring-engine health. Use fresh self-monitoring items for the last of these; missing items mean unknown, not healthy.

OS monitoring traffic, where enabled, needs an explicit narrow admin-reviewed path and separate agent identity; do not give the inference service broad network access. No unrestricted remote commands, public management interfaces, shared superuser or browser-to-model route. Additional NICs do not authorize bridging. Keep both PostgreSQL instances internal to their own VMs initially and configure storage ownership correctly.

All required models, dependencies, UI assets, dictionaries, identity, DNS/time/key/certificate services and state must work locally. GitHub and registries are provisioning/release sources, not runtime dependencies. No privileged PR runner on a serving VM. Untrusted tests/builds use isolated infrastructure without operational secrets; count their peak resource use separately.

## 5. Creation order is not startup order

Use dependency-aware readiness: local storage, keys and time first; both PostgreSQL services before their dependants. Zabbix must have its database and valid monitoring evidence. AI and gateway may start independently. API can expose login and truthful degraded health during warm-up. Admit a Zabbix investigation only when required identity, policy, DB, audit, model and connector checks pass. General local Q&A must not wait indefinitely for unavailable Zabbix.

Use bounded readiness/retries, not fixed sleeps or Internet probes. A powered-on VM is not a ready application. Recover durable jobs without replaying uncertain external effects; persist/drain work before stopping dependencies. Cold-start tests include the new Zabbix server and a fresh browser session, not just an already loaded model.

## 6. Combined capacity and later VMs

| Phase/profile including zabbix-server | NextOps VMs | All VMs | vCPU | RAM GiB | VMDK GiB | Disk + provisional ESXi swap GiB |
|---|---:|---:|---:|---:|---:|---:|
| 1–2 | 3 | 4 | 40 | 184 | 980 | 1164 |
| 3–6, separate NextOps DB | 4 | 5 | 48 | 248 | 1280 | 1528 |
| 7–8, remediation enabled | 5 | 6 | 52 | 264 | 1360 | 1624 |

The Phase 3 `nextops-db` remains 8 vCPU / 64 GiB / 300 GiB; migrate and restore-test before retiring the old service. The Phase 7 `nextops-executor-rw` remains 4 vCPU / 16 GiB / 80 GiB and requires separate remediation approval. A read-only Phase 8 may keep the middle profile. A reviewed small read-only pilot may retain three NextOps VMs plus its Zabbix dependency. Extra services require measured demand or a trust boundary, not a phase number alone.

These are alternative profiles, not cumulative totals. Do not add the old lab or count Zabbix PostgreSQL as another VM. Keep the 3 TB project ceiling and DS-C headroom: exactly 894.1875 GiB for the proposed 25% target, conservatively about 900 GiB. The first 1164-GiB subtotal projects 2002.87 GiB free from the earlier snapshot before extra overhead/growth. Apply the full storage gate for thin-disk commitments, real swap placement, VMX files, snapshots/consolidation, offline staging and restore copies. Reconcile any already-created VMs. Do not shrink disks or change memory reservations to make accounting fit.

Do not create another monitoring VM, second AI service, per-connector VMs, Kubernetes or a separate vector service for this first result. Preserve basic metrics/audit. Same-host VMs and datastores are one host-failure domain; require independent backups and an external host-outage check where needed before production.

## 7. Handoff and validation

Update [PROJECT_STATE](../PROJECT_STATE.md) and [NEXT_TASK](../NEXT_TASK.md) after each real stage with created roles, versions, exact tests, failures/skips and blockers. Documentation publication does not mark provisioning or a test complete. See [DEPLOYMENT_UPDATE](../requirements/DEPLOYMENT_UPDATE.md) and [ZABBIX_SERVER_PLAN](../requirements/ZABBIX_SERVER_PLAN.json) for the scoped amendment and machine-readable totals.

No VM, model, Zabbix service, filesystem, network rule or acceptance test has been created or executed by this documentation change. The active prompt and original archived scope remain intact; the current dedicated-server profile takes precedence over their older small-lab examples.
