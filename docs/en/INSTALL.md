# Installation and G10 preparation

[فارسی](../fa/INSTALL.md) · [Index](INDEX.md)

**Current capability: clone, review documentation, and run the local Stage 1A contract/policy checks.** The repository now has `pyproject.toml` and generated `uv.lock`, but no runnable application installer, migration runner, Compose stack, connector, AI service, or systemd unit. Host preparation steps below remain an implementation checklist, not authorization or commands for a deployed product.

## Available now

```bash
git clone https://github.com/Omid-NextAI/nextops.git
cd nextops
git status --short
uv sync --extra dev --frozen
uv run --extra dev pytest
```

Read the master specification, architecture, security, CPU plan and next task before changing the host. Use an authenticated administrative connection approved by the owner; do not post SSH keys or passwords in GitHub issues.

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

After architecture approval and implementation: verify a pinned release and its artifacts; preflight host resources and ports; provision restricted service identities/storage; supply credential references outside Git; import verified CPU model files; initialize PostgreSQL; run serialized migrations; bootstrap local authentication without a default password; start internal services; validate the reverse proxy, health checks and denied operations. Enable only simulators or explicitly authorized lab connectors.

Require non-root/restricted containers, tested resource limits and network separation. Do not expose the database, inference or MCP ports publicly or mount the container engine socket. Publish exact runnable commands only when the corresponding files have passed clean-install tests.

## Future native/systemd path

Use compatible pinned packages and a dedicated virtual environment, dedicated service users, restricted data/configuration paths, and separate API, worker, gateway and CPU inference units. Record unit dependencies, restart behavior, resource caps, writable paths and hardening limitations. Native and Compose paths must share configuration semantics and acceptance tests.

## Offline path

Prepare a verified bundle in an approved connected environment: application packages/images, transitive dependencies, local frontend assets, model/tokenizer files, migrations, documentation and checksums. Exclude production credentials. Import and verify offline; missing artifacts must fail preflight rather than download themselves. Prove authentication, local inference, retrieval, permitted LAN diagnostics and audit with Internet access blocked.

## Deployment acceptance

Record release/host identity, actual test output, CPU execution evidence, permissions, port exposure, audit durability, restart recovery and restore results. Define off-host backup, proposed then measured RPO/RTO, and an administrative access-recovery path. A local backup directory is only staging. Do not call the host production-ready until Phase 8 evidence is reviewed.
