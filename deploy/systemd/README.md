# Native systemd profiles for controlled user testing

The directory now covers the protected AI, authenticated application, read-only connector and two
restricted SSH-forward boundaries used by the controlled user-testing deployment. The source units
contain no private address or credential. Environment-specific destinations, host-key pins and
secrets are delivered outside Git.

Application-side units:

- `nextops-app.service` runs the authenticated panel/API on loopback and reads database, bootstrap,
  recovery, AI-service and connector-service credentials through `LoadCredential`.
- `nextops-ai-tunnel.service` forwards one app-local port to the AI loopback API using a dedicated
  key, pinned host key and server-side `PermitOpen` restriction.
- `nextops-connector-tunnel.service` does the same for the connector summary API on a different
  loopback port. Neither tunnel grants an interactive shell, remote forwarding, agent forwarding or
  access to an arbitrary destination.

Connector-side units:

- `nextops-connector.service` runs as the non-login `nextops-connector` identity on loopback. It
  reads the Zabbix token and internal service secret through `LoadCredential`, validates Zabbix TLS
  against the deployment CA, bypasses inherited proxies and exposes only the named read-only
  summary operation.

The 2026-09-22 controlled deployment verified all three application-side services and the connector
service active, with the app, AI and connector listeners confined to loopback. The external browser
entry is private TLS through Nginx. This is user-testing evidence, not proof for another host or a
production-acceptance claim.

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
/etc/nextops/credentials/connector-service-secret
/etc/nextops/credentials/connector-tunnel-key
/etc/nextops/ssh/connector_known_hosts
/etc/nextops/nextops-app.env
/etc/nextops/nextops-connector-tunnel.env
/etc/nextops/nextops-connector.env
/etc/nextops/tls/zabbix-ca.crt
/etc/nextops/credentials/zabbix-api-token
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
