# Stage 1B native systemd service profile

[فارسی](../fa/AI_SYSTEMD.md) · [Index](INDEX.md) · [CPU-only AI](CPU_AI.md) · [Offline runtime](OFFLINE_RUNTIME.md)

**Status: installed and running on the authorized AI server; controlled Stage 1B qualification
passed on 2026-09-22, while production and full offline acceptance remain open.**

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

The promoted llama.cpp build keeps its shared libraries beside the executable. The installed unit
sets `LD_LIBRARY_PATH` to the stable protected runtime `bin` directory; this corrects the first live
relocation failure without referencing a developer checkout. Controlled startup waits for the
authenticated model health response, not merely an open socket.

The Python configuration loader accepts systemd `LoadCredential` files, rejects symlinks, multiline
values, oversized files, ambiguous environment-plus-file sources, and world-accessible credential
files on POSIX. Ordinary environment values remain available only for isolated development/tests;
the deployment profile does not use them.

The protected application release `nextops-0.1.0-62de8d6` is active. It contains the prompt fix that
preserves the supplied event, failure mode, timestamp, scope, and current-state uncertainty in the
requested language. `nextops-0.1.0-417d888` remains available and has passed an application-link
rollback/readiness test; it is not the accepted quality release. The earlier `5de76ac` build remains
historical staging/rollback evidence, not the current application.

## Verified live result

The private evidence record for 2026-09-22 verifies:

1. the runtime and 5,027,783,488-byte model match their pinned SHA-256 values and are reached through
   stable links to immutable protected release directories;
2. two distinct root-owned `0400` credentials are installed without entering Git or logs;
3. both units are enabled and active only on `127.0.0.1:8080` and `127.0.0.1:8090`, and each receives
   `2.7 OK` from `systemd-analyze security`;
4. unauthenticated generation returns `401`, readiness returns `200`, bounded load admits one active
   request and rejects/times out excess work as designed, and two independent Persian/English
   four-case runs passed both automated checks and human review;
5. a cold process restart restored the authenticated services in 109 seconds; the unit network policy
   denied non-loopback IP traffic throughout;
6. application rollback to `417d888` and forward restoration to `62de8d6` both passed authentication
   denial/readiness checks, leaving `62de8d6` active.

This is a controlled Stage 1B qualification, not production acceptance. Still required are an
authorized VM reboot, an explicit external WAN-disconnection observation, live cancellation and
dependency-failure cases, runtime/model rollback, corrupt or missing artifact behavior, sustained
performance and NUMA thresholds, dependency-license approval, an independent artifact/backup copy,
and an isolated restore. Full Phase 1 also requires the application, PostgreSQL, Zabbix, connector,
browser, audit, and end-to-end offline gates.
