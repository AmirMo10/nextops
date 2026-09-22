# Native systemd profile for Stage 1B

This directory contains the reviewed source profile for the first controlled `nextops-ai`
qualification. It is not evidence that the units are installed or accepted on a server.

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

## Review and installation gates

Before installation:

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

Enabling does not prove readiness. Start only inside the approved change window, verify both
loopback listeners and both authentication boundaries, capture the CPU-only startup report without
paths or secrets, and run the versioned bilingual/load/failure/offline evaluation. Promote only if
AI-01 through AI-06 have actual evidence; otherwise stop or return atomically to the retained
last-known-good set.
