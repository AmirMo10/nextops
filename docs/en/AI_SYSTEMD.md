# Stage 1B native systemd service profile

[فارسی](../fa/AI_SYSTEMD.md) · [Index](INDEX.md) · [CPU-only AI](CPU_AI.md) · [Offline runtime](OFFLINE_RUNTIME.md)

**Status: implemented and tested in repository source; not installed or accepted on the AI server.**

Stage 1B uses the native systemd profile under [`deploy/systemd`](../../deploy/systemd). Docker is
not required and no service receives a container socket. The profile separates the pinned llama.cpp
process from the authenticated NextOps inference boundary:

- `nextops-llama.service` loads only the verified local model, uses CPU with zero GPU layers, binds
  to `127.0.0.1:8080`, accepts one runtime slot, disables the Web UI and slot endpoint, and requires
  a provider API key supplied by systemd credentials.
- `nextops-ai.service` binds to `127.0.0.1:8090`, uses a different bearer secret, and exposes the
  tested one-active/two-queued NextOps API. It does not accept client-selected provider URLs, model
  paths, system prompts, tools, agents, or target credentials.

The units clear proxy variables, deny non-loopback IP traffic at the service cgroup, run as the
unprivileged `nextops-ai` identity, make artifact/configuration trees read-only, restrict writable
state and log paths, disable core dumps and Linux capabilities, and set explicit CPU, memory, task,
file, and restart limits. The initial 16-thread llama.cpp setting is a qualification starting point,
not an accepted performance result or a topology claim.

The Python configuration loader accepts systemd `LoadCredential` files, rejects symlinks, multiline
values, oversized files, ambiguous environment-plus-file sources, and world-accessible credential
files on POSIX. Ordinary environment values remain available only for isolated development/tests;
the deployment profile does not use them.

## Installation hold

Do not install or start the units until the current private change record resolves all of the
following:

1. the target account has narrow approved privilege for the exact unit, credential, immutable
   release-link, daemon-reload, enable/start/stop, and evidence commands;
2. the latest guest preflight has no unresolved update/reboot, listener, mount, resource, recovery,
   or rollback issue;
3. the complete llama.cpp shared-library tree, model, Python release/wheel bundle, licenses, and
   independent SHA-256 trust anchors verify;
4. two distinct credentials are delivered without printing or committing them;
5. `systemd-analyze verify` and the effective sandbox/resource settings pass on the target guest;
6. an immutable previous compatible runtime/model/application set and an independent artifact copy
   exist for rollback and offline restore.

After installation, capture actual results for authentication, readiness, CPU-only startup,
bilingual generation, queue saturation, cancellation/timeouts, dependency failure, restart, resource
use, Internet-blocked cold start, rollback, and isolated restore. Until those results exist, AI-01
through AI-06 remain `not_run` and the service is not production-ready.
