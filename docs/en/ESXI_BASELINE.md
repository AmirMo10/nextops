# ESXi build, CPU identification and VM configuration baseline

[فارسی](../fa/ESXI_BASELINE.md) · [Server plan](SERVER_PLAN.md) · [CPU evaluation](CPU_AI.md) · [Offline contract](OFFLINE_RUNTIME.md) · [Hardware record](../requirements/HARDWARE_BASELINE.json)

**Updated 2026-09-20. Evidence: owner-supplied command output and separately identified official references.** No direct host inspection, VM modification or benchmark was performed. This supplement resolves the older “ESXi build unknown” wording without changing the archived prompt, phase order or proposed resource budgets.

## 1. What the new output establishes

The owner supplied `esxcli system version get` and the first 35 lines of `esxcli hardware cpu list`. The version output reports **VMware ESXi 8.0.3, build 24414501, Update 3, Patch 55**. Broadcom's build table maps build 24414501 to **ESXi 8.0 Update 3c**, released **2024-12-12** [1]. Preserve `Patch: 55` as the reported field; use the build table for the release name rather than treating 55 as a release label.

| Sampled CPU 0 field | Supplied value | Interpretation or calculation |
|---|---|---|
| Brand | `GenuineIntel` | Vendor identifier, not a Xeon marketing model |
| Family / Model / Stepping | `6 / 85 / 7` | Hexadecimal tuple `06-55-07` |
| Package / NUMA node | `0 / 0` | Placement of this sampled logical CPU only |
| Core speed | `2693671674` Hz | Approximately **2.694 GHz** as reported; not proof of rated base/turbo or sustained inference frequency |
| L2 cache | `1048576` bytes | **1 MiB** in the CPU 0 record; cache CPU count is 2 |
| L3 cache | `40370176` bytes | **38.5 MiB** in the CPU 0 record; cache CPU count is 56 |
| Microcode | `0x5003707` | Recorded value, not a claim of current firmware compliance |

CPU 0 is complete in the excerpt; CPU 1 is partial. Both shown records place those logical CPUs in package 0 / node 0. Do not generalize this into an inspection of the other packages, their firmware or their memory distribution. Do not multiply shared-cache sizes by the number of logical CPUs.

Intel's reference table associates `06-55-07` with **CLX-SP, B1, Xeon Scalable Gen2** [2]. This is a reference-based family identification, not proof of a specific part such as a particular Xeon Platinum SKU. The exact processor model remains unconfirmed. The earlier command is useful for identifiers but did not expose a marketing model name; there is no need to repeat the same truncated command.

The previously supplied **4 packages / 112 physical cores / 224 logical threads / 4 NUMA nodes / 1,343.6597 GiB RAM** remain unchanged. Those are host totals, not available resources. The 28-core-per-node and 335.9149-GiB-per-node values remain arithmetic averages until per-node inventory is obtained.

## 2. Proposed placement stays the same

| Phase 1 VM | vCPU | RAM GiB | Disk GiB | Purpose |
|---|---:|---:|---:|---|
| `nextops-app` | 8 | 32 | 200 | Local UI/auth/API/worker and initially a separately restricted PostgreSQL service |
| `nextops-ai` | 24 | 128 | 500 | One dedicated local CPU generation service |
| `nextops-connectors-ro` | 4 | 8 | 80 | Policy-controlled MCP gateway and scoped read-only Zabbix runner |
| **Total** | **36** | **168** | **780** | One serving environment; existing Zabbix and test/backup environments excluded |

These are proposals, not minimum requirements, reservations or proof of spare capacity. Keep three VMs in Phases 1–2, four recommended in Phases 3–6, and five when Phase 7 remediation is enabled; Phase 8 can remain four if read-only. See [SERVER_PLAN.md](SERVER_PLAN.md) for the unchanged four/five-VM and optional-lab totals.

The 24-vCPU AI VM is a starting experiment below the **average** 28 physical cores per node. It does not prove the VM fits any particular node or reserve 24 dedicated cores. Check actual per-node CPU/memory capacity, ESXi placement, existing load, and the guest's topology. Compare 16, 24 and 28 vCPUs under the same workload; select by measured latency/throughput and resource pressure, not by the largest number. Do not automatically create one AI instance for every NUMA node.

## 3. ESXi 8-specific configuration proposal

For **new** NextOps Ubuntu VMs, use a supported compatibility level and review virtual hardware version 20 or later. Check any vCenter, backup and recovery-host compatibility first; the ESXi version does not reveal an existing VM's hardware version. Do not automatically upgrade unrelated VMs.

Broadcom documents Automatic vTopology for ESXi 8 with **virtual hardware 20+ and Cores per Socket set to “Assigned at power on”** [3]. Use that as the default candidate rather than manually exposing 24 sockets or assuming “1 socket × 24 cores” pins a physical NUMA node. Verify the saved configuration and guest view after power-on.

**Host Client caveat:** Broadcom documents a case where saving VM settings through the standalone ESXi Host Client changes automatic topology into one core per socket [4]. Where an appropriately managed vCenter exists, use its vSphere Client as recommended by that article. vCenter is not an added NextOps runtime prerequisite; on a standalone host, inspect the actual saved topology through the available supported interface instead of assuming the setting survived. Do not blindly edit VMX files on running machines.

For the initial reproducible benchmark, propose fixed CPU/memory allocation and leave CPU Hot Add disabled unless required. This is a test-control choice, **not** a blanket claim that Hot Add always disables vNUMA: Broadcom explicitly documents vNUMA preservation with Automatic vTopology on HW20+ [3]. Any topology adjustment, affinity rule or reservation needs an approved change and before/after evidence.

Do not pin the AI VM to node 0 merely because the excerpt contains CPU 0. Start with the scheduler's normal placement. Collect CPU ready, co-stop, guest CPU usage, NUMA locality, memory pressure and host/guest swap alongside answer latency [3]. Free capacity and a complete per-node map are still missing.

## 4. CPU-only runtime and offline behavior

Keep the existing pinned `llama.cpp` CPU-runtime proposal. This CPU sample does not supply the guest's instruction flags. Verify the actual Ubuntu VM's CPU features and startup output before choosing an optimized build. Do not assume AVX-512, VNNI, AMX or any other extension is exposed merely from the family label; do not select a build requiring unsupported instructions.

Record guest-visible features, runtime commit/build options and model revision together. Compiler/build-machine capabilities must not be confused with those of the deployment guest. Preload all application/model/frontend artifacts through the approved provisioning process. No inference, embeddings, login, documentation assets or boot dependency may require Internet access.

**The Phase 1 outcome is unchanged:** with server and browser Internet access blocked and authorized LAN access to Zabbix available, a new Persian/English question receives a local CPU-generated answer grounded in actual read-only Zabbix evidence, source times and audit. A working VM, benchmark or model greeting alone is not completion. ZBX-01–ZBX-08 and OFF-01–OFF-10 remain acceptance requirements, not passing results.

## 5. Patch and firmware review before production

Build 24414501 is a **December 2024** release; Broadcom's table lists later ESXi 8.0 U3 releases [1]. The generic `8.0.3` label therefore does not establish current patch status. Review applicable advisories, supported OEM image/firmware/drivers, vCenter/backup compatibility, recovery access and an offline-import update procedure before choosing a production baseline. No target patch is approved by this document.

The sampled microcode revision is an inventory fact. Use the hardware vendor and ESXi-supported maintenance process; Intel's Linux microcode package is cited here for identification, **not** as installation instructions for the ESXi host. Do not patch, reboot, change BIOS policy, disable Hyperthreading or alter network access as part of this documentation task. Offline operation does not replace a patch/firmware maintenance process.

## 6. Remaining evidence and validation status

No need to resend host core/RAM totals or the ESXi build. Remaining useful inputs are the exact CPU marketing model, VM hardware level, guest-visible CPU flags, per-node memory map, available resources/competing VM load, datastore capacity/latency, and scoped LAN Zabbix access. The vSphere API documents `HostCpuPackage.description` as a human-readable CPU description [5]; an administrator can obtain the CPU model through the host hardware summary or that authenticated read-only property. Share only the relevant description, not full private inventory or credentials.

This update validates the arithmetic conversions and records official release/family mappings. It does **not** validate workload performance, guest ISA exposure, NUMA placement, compatibility, patch safety or offline operation on the G10. Those remain authorized lab/maintenance tasks.

## Official references

Consulted 2026-09-20. References support the named platform facts, not the proposed resource budget or a working NextOps deployment.

[1]: https://knowledge.broadcom.com/external/article/316595
[2]: https://raw.githubusercontent.com/intel/Intel-Linux-Processor-Microcode-Data-Files/main/releasenote.md
[3]: https://knowledge.broadcom.com/external/article/438023
[4]: https://knowledge.broadcom.com/external/article/425838
[5]: https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/vim.host.CpuPackage.html
