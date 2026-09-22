# Native systemd profile for Stage 1B

This directory contains the reviewed source profile used for the first controlled `nextops-ai`
qualification. On 2026-09-22 the profile was installed on the authorized AI guest and the bounded
deployment, bilingual quality, cold-process restart, and application rollback checks passed. Raw
host evidence and credentials remain outside Git; the repository profile alone is not proof of a
different host's state or production acceptance.

The profile deliberately uses two processes under the existing unprivileged `nextops-ai` identity:

- `nextops-llama.service` loads the pinned llama.cpp runtime and Qwen model on CPU only. It binds
  only to `127.0.0.1:8080`, authenticates requests from a systemd credential, exposes no Web UI or
  slot endpoint, and admits one llama.cpp slot.
- `nextops-ai.service` runs the authenticated NextOps boundary on `127.0.0.1:8090`. It reads the
  provider key and the distinct client-facing bearer secret from systemd credentials, then applies
  the source-level one-active/two-queued scheduler.

Both units deny non-loopback IP traffic at the service cgroup, clear proxy variables, use read-only
artifact and release trees, restrict writable paths, remove Linux capabilities, and set explicit
CPU, memory, task, file, restart, and core-dump limits. The initial llama.cpp profile uses 16
generation and prompt-processing threads on the 24-vCPU guest. This is a bounded qualification
starting point, not a final performance claim or NUMA decision.

The llama.cpp build stores its required shared libraries beside `llama-server`. The unit therefore
sets `LD_LIBRARY_PATH` to the protected stable runtime `bin` directory. Do not replace it with a
developer-build path: the first relocated start demonstrated that a socket check alone cannot prove
the executable has loaded its immutable dependencies or finished loading the model.

## Required installed layout

```text
/srv/nextops/runtime/llama.cpp/current/bin/llama-server
/srv/nextops/models/current/Qwen3-8B-Q4_K_M.gguf
/srv/nextops/releases/current/venv/bin/uvicorn
/etc/nextops/nextops-ai.env
/etc/nextops/credentials/llama-api-key
/etc/nextops/credentials/inference-service-secret
```

`current` must be an atomic symlink to one immutable, checksummed release. Retain one compatible
last-known-good runtime/model/application set for rollback. Credential files contain one secret per
file, are root-owned, are not world-accessible, and are never committed or printed. The two values
must be different and at least 32 characters.

## Review, installation, and remaining acceptance gates

Before installation on any new or rebuilt host:

1. Re-run the read-only guest, mount, listener, CPU/NUMA, memory, free-space, update, and service
   preflight. Stop on a changed baseline, pending reboot, unexpected listener, unavailable recovery
   route, or missing rollback artifact.
2. Verify the complete runtime library tree, model, Python release, licenses, and manifests against
   independently supplied SHA-256 trust anchors.
3. Build the Python virtual environment from the approved locked local wheel bundle. A production
   service must not execute from a developer checkout or fetch packages at startup.
4. Deliver credentials through the approved private change record. Do not pass a secret as a unit
   argument, shell command, repository value, or ordinary environment value.
5. Validate the units with `systemd-analyze verify`, inspect their effective sandbox with
   `systemd-analyze security`, and review every deviation on the target Ubuntu 24.04 guest.

Install the non-secret environment file and units as root, preserving the modes below:

```bash
install -o root -g nextops-ai -m 0640 deploy/systemd/nextops-ai.env /etc/nextops/nextops-ai.env
install -o root -g root -m 0644 deploy/systemd/nextops-llama.service /etc/systemd/system/nextops-llama.service
install -o root -g root -m 0644 deploy/systemd/nextops-ai.service /etc/systemd/system/nextops-ai.service
systemctl daemon-reload
systemctl enable nextops-llama.service nextops-ai.service
```

Enabling does not prove readiness. Start only inside the approved change window, wait for the
authenticated llama.cpp health endpoint rather than only the listener, verify both loopback
listeners and the API authentication boundary, capture CPU-only startup without secrets, and run
the versioned bilingual/load/failure/offline evaluation. The 2026-09-22 qualification covers the
current controlled deployment, bounded load, cold process restart, and application-link rollback.
VM reboot, explicit WAN-disconnection testing, runtime/model rollback, corrupt-artifact isolation,
cancellation under live load, independent restore, license approval, and agreed production
performance thresholds remain separate evidence gates.
