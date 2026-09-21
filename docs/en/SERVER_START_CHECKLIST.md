# Server start checklist

**Status: operator handoff, not permission to provision.** Phase 0 and Stage 1A code
work are approved. VM creation, guest installation, network/firewall changes, package
installation, target access, reboots, and destructive storage work still require a
separate recorded change authorization.

## What to do first

Start with the **private deployment preflight for `nextops-app`**. Do not install NextOps
on a server yet: the repository has an application foundation, but no approved offline
release bundle, production service units, reverse-proxy configuration, backup/restore
procedure, or completed production database-version lock.

In the same approved planning window, prepare the information for all four machines.
After a separate provisioning approval, use this creation order:

| Order | Server | vCPU | RAM | Disk | Initial purpose |
|---:|---|---:|---:|---:|---|
| 1 | `nextops-app` | 8 | 32 GiB | 200 GiB | API, durable worker, audit, initial NextOps PostgreSQL |
| 2 | `nextops-ai` | 24 | 128 GiB | 500 GiB | Local CPU inference only |
| 3 | `nextops-connectors-ro` | 4 | 8 GiB | 80 GiB | Isolated read-only gateway/runners |
| Parallel prerequisite before 1C | `zabbix-server` | 4 | 16 GiB | 200 GiB | Dedicated monitoring database, server, frontend/API, Agent 2 |

All four are proposed for DS-C. This is 40 vCPU, 184 GiB RAM, and 980 GiB of VMDKs.
It is a budget, not a reservation. Reconcile any VM that already exists before
subtracting capacity.

## 1. Open the private change record

Create one record outside Git and give it a change identifier. Resolve the
`required_inputs` keys in each file under `deploy/server-dependencies/`. At minimum,
record privately:

- approver, operator, authorized actions, maintenance window, stop conditions, and
  rollback owner;
- actual VM names, datastore mapping, addresses, DNS names, VLAN/firewall sources,
  administrator route, recovery-console route, and SSH host keys;
- exact Ubuntu image/checksum, VM hardware compatibility, firmware, Secure Boot decision,
  virtual NIC/storage controllers, thin/thick policy, and guest disk layout;
- current available CPU/RAM, reservations, contention, current DS-C free space, thin-disk
  commitments, snapshot/consolidation needs, ESXi swap placement, and storage health;
- local DNS/time/PKI dependencies, certificate renewal/revocation, package source,
  backup destination, restore staging, RPO/RTO, and monitoring route;
- reference identifiers for secrets. Never copy a password, token, private key, recovery
  secret, real address, datastore UUID, or route into this repository or a model prompt.

Keep approximately 900 GiB free on DS-C after the approved initial allocation and all
other overhead. Count VMX files, snapshots, staging/restore copies, existing growth, and
powered-off VM swap separately. Do not shrink, delete, migrate, repartition, or change a
memory reservation as part of this checklist.

## 2. Pass the host-side gate before VM creation

Using only the authorized read-only ESXi/management interface, confirm:

1. The intended VM does not already exist under another name or inventory record.
2. Current CPU, memory, datastore, storage-health, and outstanding-commitment evidence is
   fresh for the change window.
3. The selected VM compatibility level and guest CPU exposure are supported by the
   existing ESXi 8.0.3 build; ESXi itself remains unchanged.
4. Management access, console recovery, local DNS/time, and independent backup paths work
   without public Internet.
5. The approved network rules provide only the flows in each server dossier. The app and
   model server have no direct target-management access; only the connector boundary may
   later receive narrowly approved routes and credentials.

Stop if evidence is stale, an existing VM cannot be reconciled, storage health is
unknown, the remaining DS-C margin would be breached, or rollback/recovery access is not
available.

## 3. After separately authorized provisioning

On each new Ubuntu guest, capture these read-only checks into the private change record:

```bash
cat /etc/os-release
uname -r
systemd-detect-virt
lscpu
free -h
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,ROTA
findmnt
df -hT
timedatectl status
sudo ss -lntup
```

Expected starting evidence is the approved Ubuntu image, VMware virtualization, the
correct vCPU/RAM/disk values, only the reviewed disks and mounts, trusted local time, and
no unexplained listener or port conflict. Keep the full output private because it may
contain infrastructure identifiers.

Then apply these server-specific holds:

- **`nextops-app`:** reserve the guest and complete OS/network/storage evidence only. Do
  not initialize the NextOps database or run migrations until the application release,
  database version, login roles, service units, backup, and downgrade/recovery procedure
  are promoted together. CI currently tests PostgreSQL 17.6; the dossier's PostgreSQL 16
  proposal is not a production lock and must be reconciled before installation.
- **`nextops-ai`:** record actual guest-visible CPU flags and NUMA view before selecting a
  CPU build. Do not download a model or install CUDA, ROCm, GPU containers, or a remote
  fallback. The model/runtime checksum, license, memory budget, and measured quality and
  latency remain gates.
- **`nextops-connectors-ro`:** keep target routes and credentials absent. Confirm the VM
  cannot reach management targets by default. Later access must be by immutable target
  IDs, method allowlists, protected per-runner credentials, and explicit read-only tests.
- **`zabbix-server`:** it may be prepared in parallel so it is ready before Stage 1C, but
  first inspect and reuse a suitable authorized local Zabbix deployment if one exists.
  For a new empty disk, follow the dedicated Zabbix guide and verify the proposed LVM
  mounts before database initialization. Never apply its disk commands to an identified
  or non-empty disk.

## 4. Do not call a powered-on VM “ready”

A server moves from *prepared* to *ready* only when its dossier acceptance gates have
evidence. For `nextops-app`, that eventually includes a verified offline artifact,
restricted database roles, successful upgrade/downgrade and isolated restore, identity
bootstrap/recovery, authenticated API, audit failure behavior, service restart recovery,
TLS, backup, and Internet-blocked operation. The current application code and CI do not
authorize those server actions by themselves.

Return a sanitized summary containing the change identifier, timestamps, actual resource
values, guest OS/kernel, mount verification, local dependency reachability, backup/restore
status, each acceptance result, deviations, and rollback outcome. Store raw infrastructure
output and all secrets only in the approved private system.

The source of truth for each machine is its YAML dossier and the paired
[deployment-dossier guide](DEPLOYMENT_DOSSIERS.md). The detailed Zabbix disk and service
plan is in [ZABBIX_SERVER](ZABBIX_SERVER.md).
