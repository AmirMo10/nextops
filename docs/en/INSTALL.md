# Installation and G10 preparation

[فارسی](../fa/INSTALL.md) · [Index](INDEX.md)

**Current capability: source development plus a separately qualified controlled deployment.** The repository contains the guarded OS-package layer, locked Python application, bilingual browser UI, connector and hardened AI source units. The four live guests have passed the controlled gates recorded in the [release status](../status/current-release.yaml), but the repository still has no complete reproducible production installer, approved independent backup/WAL/PITR bundle or production authorization. The host steps below remain an implementation checklist; they do not recreate or authorize the existing deployment by themselves.

## Available now

```bash
git clone https://github.com/Omid-NextAI/nextops.git
cd nextops
git status --short
uv sync --extra dev --frozen
uv run ruff format --check packages migrations tests scripts deploy/installers
uv run ruff check packages migrations tests scripts deploy/installers
uv run mypy packages tests deploy/installers
uv run pytest -m "not integration"
```

Read the master specification, architecture, security, CPU plan and next task before changing the host. Use an authenticated administrative connection approved by the owner; do not post SSH keys or passwords in GitHub issues.

## Per-server package scripts

The scripts under [`deploy/installers`](../../deploy/installers) cover only the exact Ubuntu package layer
for `nextops-app`, `nextops-ai`, `nextops-connectors-ro`, and `zabbix-server`. Read the
[installer handoff](../../deploy/installers/README.md) before use. Each script consumes a complete signed
local APT repository, an exact lock including transitive packages, and a separately approved SHA-256 for
the bundle manifest.

Start with non-mutating validation on the matching guest:

```bash
./deploy/installers/install-nextops-app.sh \
  --check \
  --bundle-dir /srv/nextops/import/nextops-app \
  --bundle-manifest-sha256 "$APP_BUNDLE_MANIFEST_SHA256"
```

Apply is a separate approved change. It requires root ownership/non-writable permissions on the bundle,
Ubuntu 24.04 on VMware, `NEXTOPS_PROVISIONING_AUTHORIZED=YES`, and `--change-id`. It installs only the
authenticated exact package lock, blocks automatic service start, and prevents automatic PostgreSQL
cluster creation. It does not configure or start the product. No real bundle or production package lock
is committed yet, so package installation remains blocked until those artifacts are built and approved.

## Read-only host inventory

Run only commands already present and only on the authorized server. Inspect outputs locally; redact hostnames, production addresses, mount names and other sensitive details before publishing.

```bash
cat /etc/os-release
uname -r
lscpu
lscpu -e=CPU,CORE,SOCKET,NODE,ONLINE
nproc
free -h
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,ROTA
findmnt
systemd-detect-virt
# Optional, only when installed:
numactl --hardware
# Listener information can be sensitive; keep this local:
ss -lnt
```

Also establish effective CPU affinity/cgroups, available RAM, existing workloads, free disk on intended mounts, clock synchronization, management routes and backup destination. Absence of `numactl` is not permission to install it during discovery. Do not run stress tests, drop caches, change firewall/SSH, repartition, reboot or download large models in Phase 0.

Ubuntu is the source requirement; Ubuntu 24.04 LTS and Python 3.12 are proposed baselines subject to compatibility and owner approval. No OS reinstall is implied. Resolve asset count, incident volume, retention, concurrent investigations and latency goals before capacity planning.

## Future Compose path

After a deployable release is approved: verify its artifacts; preflight host resources and ports; provision restricted service identities/storage; supply credential references outside Git; import verified CPU model files; initialize the selected PostgreSQL patch; run serialized migrations; bootstrap local authentication without a default password; start internal services; validate the reverse proxy, health checks and denied operations. Enable only simulators or explicitly authorized lab connectors.

Require non-root/restricted containers, tested resource limits and network separation. Do not expose the database, inference or MCP ports publicly or mount the container engine socket. Publish exact runnable commands only when the corresponding files have passed clean-install tests.

## Future native/systemd path

Use compatible pinned packages and a dedicated virtual environment, dedicated service users, restricted data/configuration paths, and separate API, worker, gateway and CPU inference units. Record unit dependencies, restart behavior, resource caps, writable paths and hardening limitations. Native and Compose paths must share configuration semantics and acceptance tests.

## Offline path

Prepare a verified bundle in an approved connected environment: application packages/images, transitive dependencies, local frontend assets, model/tokenizer files, migrations, documentation and checksums. Exclude production credentials. Import and verify offline; missing artifacts must fail preflight rather than download themselves. Prove authentication, local inference, retrieval, permitted LAN diagnostics and audit with Internet access blocked.

## Deployment acceptance

Record release/host identity, actual test output, CPU execution evidence, permissions, port exposure, audit durability, restart recovery and restore results. Define off-host backup, proposed then measured RPO/RTO, and an administrative access-recovery path. A local backup directory is only staging. Do not call the host production-ready until Phase 8 evidence is reviewed.
