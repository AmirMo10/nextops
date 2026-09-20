# Dedicated Zabbix server and on-demand local AI answers

[فارسی](../fa/ZABBIX_SERVER.md) · [Start here](START_HERE.md) · [Index](INDEX.md) · [Allocation record](../requirements/ZABBIX_SERVER_PLAN.json)

**Updated: 2026-09-20. Status: recommended deployment profile; not provisioned or tested by this documentation change.** The owner requested publication of the dedicated Zabbix VM recommendation. This guide replaces the earlier small `zabbix-lab` default for the new-monitoring-server path. It does not authorize reinstalling an existing working Zabbix server or modifying ESXi.

## 1. One monitoring VM, separate from the three NextOps VMs

Create one `zabbix-server` VM on the existing G10. It collects monitoring data continuously. When an authorized user asks a question, the NextOps connector retrieves relevant evidence through its API and the local CPU model explains that evidence. Installing Zabbix alone does not implement the NextOps connector or the answering workflow.

| Setting | Starting recommendation |
|---|---|
| VM | `zabbix-server` |
| Guest OS | Ubuntu Server 24.04 LTS, after compatibility review |
| CPU | 4 vCPU |
| CPU topology | Prefer supported automatic topology; manual alternative: 4 cores per socket, 1 virtual socket |
| CPU Hot Add | Disabled for the initial fixed-size profile |
| RAM | 16 GiB |
| Total virtual disk | 200 GiB, including OS, database and guest swap |
| Datastore | DS-C, the largest datastore in the sanitized hardware record |
| New-install firmware | UEFI |
| Network | Approved internal route, stable private address, locally usable name resolution and trusted HTTPS |
| GPU | None |

These are proposed starting allocations, not host reservations, measured requirements or a guarantee for a particular device count. Zabbix publishes a 4-CPU/16-GiB medium configuration example but explicitly requires workload-specific evaluation [1]. Our 200-GiB disk allowance is an engineering proposal. Item count, sampling frequency, value types, database growth and retention determine actual demand.

For automatic CPU topology, check the VM compatibility level and saved settings described in [ESXI_BASELINE](ESXI_BASELINE.md). A manual 4-core virtual socket does not reserve a physical socket or prove NUMA placement.

There are now **three NextOps VMs plus one Zabbix VM: four total** for this profile. Do not also create the old 4-vCPU/8-GiB/100-GiB lab VM. Reuse an existing authorized, suitable local Zabbix instance instead when one is already present; first inspect it rather than duplicating or reformatting it. This guide covers the selected new-server path.

## 2. Proposed software inside zabbix-server

| Component | Recommendation |
|---|---|
| Monitoring | Zabbix 7.0 LTS, with a reviewed maintained 7.0 patch release [2] |
| Database | PostgreSQL 16, with reviewed maintenance updates [1] |
| Frontend/API | Zabbix frontend, Nginx and compatible PHP-FPM [1] |
| Guest monitoring | Zabbix Agent 2 |
| Service management | Native packages and systemd |

Pin the actual versions, package sources, checksums and compatible templates at provisioning time. This is not a package lockfile or an installation already performed. No major-version upgrade, TimescaleDB deployment, separate Zabbix database VM, proxy fleet or extra AI runtime is required for the first milestone.

Zabbix's PostgreSQL instance belongs only to Zabbix and remains inside this VM initially. NextOps's independent PostgreSQL instance starts inside `nextops-app` and later moves to `nextops-db` according to the roadmap. Do not share database credentials, schemas or an unrestricted PostgreSQL service account between the two products. The AI and connector do not receive either database's credentials.

## 3. LVM: one 200-GiB disk, vg_zabbix

**Fresh, empty Ubuntu guest disks only.** Do not run formatting commands in the ESXi shell or reformat an installed VM. The sizes below divide the same 200-GiB virtual disk; they are not additional disk allocations.

| Partition or LV | Size GiB | Type | Mount point | Purpose |
|---|---:|---|---|---|
| EFI System Partition | 1 | FAT32 / ESP, outside LVM | `/boot/efi` | UEFI boot files |
| Boot partition | 2 | ext4, outside LVM | `/boot` | Kernel and boot files |
| `vg_zabbix/lv_root` | 32 | ext4 | `/` | OS and installed software |
| `vg_zabbix/lv_var` | 16 | ext4 | `/var` | Variable system data and package caches |
| `vg_zabbix/lv_log` | 8 | ext4 | `/var/log` | System and service logs |
| `vg_zabbix/lv_pg` | 112 | ext4 | `/var/lib/postgresql` | Database data, indexes and WAL |
| `vg_zabbix/lv_swap` | 4 | Linux swap | No directory mount | Guest swap |
| Unallocated VG extents | Approximately 25 | Not a filesystem | None | Future LV growth |
| **Total virtual disk** | **200** | | | |

Create the LVM physical volume from the remaining partition after EFI and `/boot`, then create `vg_zabbix` and its ordinary linear LVs. Do not create a logical volume named `free`; leave free extents. Alignment and metadata make the final free value slightly smaller than 25 GiB. Use the installer's actual available size rather than forcing an exact sum.

Mount `/var/lib/postgresql` before PostgreSQL initialization, and verify it is the intended filesystem. Its 112 GiB is separate from the 16 GiB at `/var`, despite the nested path. Require the mount before database startup; never silently write database files into the underlying root directory when that mount is missing. Set restricted ownership, backups and log rotation before loading monitoring data. The Ubuntu installer documents custom partitioning, volume groups and logical volumes [3].

An existing EFI partition need not be duplicated. For an installed legacy-BIOS guest, retain its reviewed boot arrangement rather than changing firmware blindly. Encryption requires an offline-capable unlock/recovery procedure; do not promise unattended restart until tested. Guest swap is already inside the 200-GiB disk; ESXi VM swap is accounted for separately.

## 4. Retention and disk growth

**Initial policy proposal:** seven days of detailed item history and ninety days of numeric trends, with explicitly approved exceptions for important incident metrics. Configure and inspect effective item/template/housekeeping settings; these values are not automatically applied by installing Zabbix.

History stores collected values; trends summarize numeric values by hour [4]. Older trend data cannot reproduce every individual reading or a detailed incident timeline after history expires. Answers must disclose the actual time resolution and retention boundary. Keep bulk monitoring history in Zabbix, not duplicated wholesale into NextOps.

Measure database, index and WAL growth, write latency, queue backlog, unsupported items and free disk before widening scope. Review sampling intervals and log ingestion rather than assuming 112 GiB of database space covers an unknown estate. Free extents allow reviewed growth; they are not a backup or a promise of reclaimed datastore space. Keep local low-space alerts and required audit/evidence retention. Never delete the only model copy or required database data as automatic cleanup.

## 5. Read-only question-to-answer contract

```text
User -> nextops-app: authenticate, authorize scope, persist question
nextops-app -> nextops-connectors-ro: named bounded diagnostic request
Zabbix runner -> zabbix-server: approved HTTPS API read
nextops-app: validate evidence, compute counts, retain source timestamps
nextops-app -> nextops-ai: sanitized evidence, no credentials
nextops-ai -> nextops-app -> user: explanation, sources, freshness, unknowns
nextops-app: durable audit and final result
```

Use the JSON-RPC API at the deployed frontend's `api_jsonrpc.php` path, over certificate-verified HTTPS [5]. Discover the configured frontend base path; do not assume every installation uses `/zabbix`. Do not scrape dashboard HTML, issue arbitrary SQL or SSH into Zabbix for every question.

Provision a dedicated identity such as `nextops-reader`, limited to approved host groups and read-only resource permissions. Configure a custom role with an explicit non-empty API method allowlist [6]. A token inherits its user's permissions [7]; having a token does not itself enforce read-only access. Test actual method and host-scope restrictions and enforce the allowlist independently in the gateway.

Begin with version-compatible `host.get`, `hostinterface.get`, `problem.get`, `trigger.get` and `item.get`. Treat `apiinfo.version` as a version probe, not successful authenticated evidence. Permit bounded `history.get` and `event.get` only where needed. Deny acknowledgement, problem closure, remote script execution, configuration changes and all unlisted operations. Validate input schemas, destination, fields, time ranges, row/byte limits and deadlines; do not let the model choose arbitrary API methods.

Only the isolated Zabbix runner receives the API token through the approved secret mechanism. Never put it in the browser, AI prompt, Git, screenshots, normal logs or an unrestricted environment shared by services. Protect token expiry/rotation and local recovery; unavailable credentials produce an explicit error, not a fallback identity.

Compute counts deterministically under the authorized scope. Show active versus resolved problems, maintenance/suppression filters and complete versus partial result sets. Do not exclude older unresolved problems from an all-current-problems count. A freshly fetched API response may contain older collected values: retain both API collection time and measurement time. Never invent live state from model memory.

## 6. Zabbix self-monitoring and network boundaries

Configure the version-matched Zabbix server-health template and appropriate guest monitoring. Official integration material documents internal process, cache, queue and uptime measurements [8]. Missing or stale self-monitoring data means unknown engine health, not healthy. Keep these separate:

| Status dimension | Evidence |
|---|---|
| API connectivity | Actual authenticated request outcome |
| Monitored estate | Scoped hosts, active problems and relevant measurements |
| Monitoring engine | Fresh self-monitoring items, queue/cache/process health and gaps |

Initially monitor `zabbix-server` and the three NextOps Ubuntu guests through an explicitly reviewed monitoring path. This is an infrastructure-admin setup, not permission for the NextOps AI to make changes. Keep OS monitoring agents separate from the model service identity; allow only the required monitoring traffic and checks. Do not grant the model a managed-device route or credentials to make self-monitoring convenient. Disallow unrestricted remote commands. No public management ports or direct browser-to-inference access.

The model remains isolated from Zabbix. Only the connector initiates its approved Zabbix API requests; the API and database interfaces have distinct permissions. PostgreSQL is local to the Zabbix VM and is not a general network endpoint for NextOps.

## 7. When to create it and how to accept the result

Preserve the NextOps creation order: `nextops-app`, `nextops-ai`, then `nextops-connectors-ro`. Prepare `zabbix-server` during the same approved work period or alongside Stages 1A/1B, but **finish its monitoring and restricted API setup before Stage 1C live integration**. VM creation is not approval to access production targets.

The checkpoint order remains 1A local identity/policy/durable state/audit; 1B actual local CPU answers; 1C real read-only Zabbix evidence; 1D complete evidence-linked answer; 1E offline acceptance. General model output or a working Zabbix dashboard alone is not Phase 1 completion.

| Check | Acceptance evidence; all currently NOT RUN |
|---|---|
| Server readiness | Correct dedicated DB mount, services, local login, monitoring items and scoped authenticated API reads |
| Evidence correctness | Counts match captured API results; engine health, estate state and API availability remain distinct |
| Access controls | Out-of-scope reads and all mutations denied; token and injected event-name tests pass |
| Offline answer | New Persian and English questions answered locally with server and browser WAN blocked and approved LAN retained |
| Offline restart | Fresh login and cold start of Zabbix, database, connector, application and model from durable local artifacts |
| Failure behavior | Zabbix outage, expired token and stale/missing items reported truthfully; unrelated local Q&A remains available |
| Recovery and capacity | Approved offline restore/low-space tests and measured resource/latency limits; no live datastore filled deliberately |

These supplement, not replace, ZBX-01–ZBX-08 and applicable OFF-01–OFF-10. Use the natural questions "Is Zabbix collecting data correctly? What active problems and stale measurements do we have?" and their Persian equivalents. Zabbix's sampling continues independently of chat requests; the assistant reads evidence on demand.

## 8. Combined capacity: do not double-count the old lab

| Profile including this Zabbix server | NextOps VMs | All VMs | vCPU | RAM GiB | VMDK GiB | Provisional ESXi swap GiB | Subtotal GiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| Phases 1–2 | 3 | 4 | 40 | 184 | 980 | 184 | 1164 |
| Phases 3–6, DB separated | 4 | 5 | 48 | 248 | 1280 | 248 | 1528 |
| Phases 7–8 with remediation | 5 | 6 | 52 | 264 | 1360 | 264 | 1624 |

These are alternative profiles, not additive amounts or full overhead ceilings. A read-only Phase 8 can retain the middle profile. Do not add the old lab VM to any row. Confirm any existing VM allocation before subtracting again. The Zabbix PostgreSQL service is not an extra VM.

Using the previously supplied DS-C free value of 3166.8701171875 GiB and unchanged existing usage, the first profile projects **2002.87 GiB free** before other overhead/growth. That is **1108.68 GiB above the exact 894.1875-GiB free-space target**. Later projections are 1638.87 and 1542.87 GiB free. These calculations do not reserve capacity or prove disk performance.

Retain the 3 TB project ceiling and approximately 900-GiB operational free-space target on DS-C. Account for existing thin-disk growth, VMX files, real ESXi swap placement, snapshots/consolidation, artifact staging and restore copies. The Linux swap LV is already in its VMDK. Do not shrink existing disks or change memory reservations to make totals fit. Apply the full [storage gate](../STORAGE_PLAN.md); this guide supplies the updated Zabbix-inclusive profile, not a replacement for those controls.

All four starting VMs share one host failure domain. A Zabbix outage must not be reported as a healthy estate; a G10 outage can take both Zabbix and NextOps offline. Before production, require an independent LAN/offline-media backup and an independent host-outage check where needed. Another VM or datastore on the same G10 is not host-loss recovery.

## 9. Scope and source precedence

This profile is a planning update, not observed infrastructure. It supersedes only the earlier new-Zabbix lab recommendation and its combined totals in older START_HERE, SERVER_PLAN, storage examples and master-prompt v3.0 section 18. Existing three/four/five **NextOps-only** counts remain valid. All eleven original integrations, security gates, CPU-only operation and archived source requirements remain in scope. See [deployment amendment](../requirements/DEPLOYMENT_UPDATE.md).

The allocation, LVM and retention figures are engineering proposals derived from the preceding recommendation. Official sources support the named software behavior only, not capacity on this G10. References checked 2026-09-20; exact installation versions still require a reviewed lock and offline bundle. No host, model, Zabbix API, disk-formatting or offline test was executed for this documentation update.

## Official references

[1]: https://www.zabbix.com/documentation/7.0/en/manual/installation/requirements
[2]: https://www.zabbix.com/life_cycle_and_release_policy
[3]: https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/configure-storage.html
[4]: https://www.zabbix.com/documentation/7.0/en/manual/config/items/history_and_trends
[5]: https://www.zabbix.com/documentation/7.0/en/manual/api
[6]: https://www.zabbix.com/documentation/7.0/en/manual/web_interface/frontend_sections/users/user_roles
[7]: https://www.zabbix.com/documentation/7.0/en/manual/web_interface/frontend_sections/users/api_tokens
[8]: https://www.zabbix.com/integrations/zabbix
