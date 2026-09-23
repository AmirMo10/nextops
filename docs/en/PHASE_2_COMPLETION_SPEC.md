# Phase 2 completion specification

[فارسی](../fa/PHASE_2_COMPLETION_SPEC.md) · [Architecture decision](../adr/0007-forced-command-linux-connector.md) · [Current state](../PROJECT_STATE.md)

**Status: implementation in progress.** Phase 2A's bounded connector route is deployed; the durable
incident workflow, Linux diagnostic boundary and complete acceptance program remain to converge.

## Problem and outcome

The current user flow explains a point-in-time Zabbix summary. Phase 2 must let an authenticated
operator choose one approved guest and receive a durable bilingual incident explanation grounded in
bounded Zabbix history/events plus a direct read-only Linux snapshot. The result must identify
observations, limitations, plausible hypotheses and safe next diagnostics without claiming an
unproven root cause.

## Requirements

- Preserve CPU-only local inference, offline operation, existing general and Stage 1 monitoring
  modes, and all accepted security boundaries.
- Resolve target IDs only from deployment-owned configuration. No caller-supplied address, user,
  command, Zabbix method, path, unit, time range or output field is permitted.
- Require an authenticated application session plus server-derived `zabbix.read`, `linux.read` and
  `runs.read` scopes where applicable.
- Use the exact five-method Zabbix reader allowlist and the existing bounded history/event contract.
- Collect Linux evidence through ADR 0007's forced-command identity with strict host-key checking
  and distinct per-target keys.
- Bound CPU/load, memory/swap, filesystems, processes, service states, critical journal entries,
  user/package counts, listening sockets, routes and resolver observations.
- Preserve UTC source times, target identity, collector version, truncation and failure reasons.
- Treat every remote name and message as untrusted data; redact likely credential material before
  persistence, model input and display.
- Persist the run before dependency calls. Store the canonical combined evidence hash, model
  result, safe failures and append-only audit linkage atomically.
- Keep each dependency failure explicit. Never replace unavailable Linux or Zabbix evidence with a
  model guess or a broader credential.
- Provide natural Persian RTL and English LTR views with isolated technical identifiers and
  accessible target/evidence controls.

## Non-goals

Phase 2 does not provide arbitrary SSH, shell, SQL, file reads, package changes, service restarts,
acknowledgements, remediation, topology/RAG, multi-organization operation or production acceptance.
It does not make correlation a verified cause. Independent backup, WAL/PITR and disaster recovery
remain separate production gates.

## Threat considerations

The principal risks are target substitution, SSH option injection, host-key bypass, misuse of the
deployment account, forced-command escape, oversized output, secret-bearing log text, prompt
injection, stale cross-source evidence and audit omission. Fixed typed configuration, per-target
keys, forced commands, constant subprocess arguments, timeouts, byte/row limits, redaction,
provenance validation, deterministic scopes and transactional persistence mitigate these risks.

## Implementation tasks

1. Add typed Linux and combined incident-evidence contracts.
2. Add the bounded local collector, strict SSH transport, immutable target registry and protected
   connector routes.
3. Add `linux.read`, durable incident run/result/audit behavior and composite model prompt.
4. Add target selection, history/events and Linux evidence to the bilingual panel.
5. Add migration, systemd credential/configuration examples and rollback-compatible deployment.
6. Add unit, API, PostgreSQL, collector, prompt-injection, failure and browser tests.
7. Promote immutable releases and qualify authenticated browser, rollback, WAN denial, service
   restart and serial VM reboot on the controlled guests.

## Acceptance criteria

- Formatting, lint, strict typing, documentation/deployment validators and all non-integration and
  PostgreSQL integration tests pass.
- Unauthorized sessions/scopes, unknown targets, altered SSH commands, malformed/oversized output
  and mismatched provenance fail closed with safe errors and audit where required.
- A new English and Persian incident question each returns fresh Zabbix and Linux evidence, a local
  CPU answer, run/evidence/audit IDs and no unsupported cause claim.
- WAN-denied fresh-browser use, process restarts, serial VM reboot, dependency loss/recovery and
  app/connector rollback pass without runtime Internet downloads.
- All temporary policies and test resources are removed; services end healthy with prior releases
  retained. Any unexecuted item remains `not_run`.

## Rollback

Atomically restore the prior app and connector release links, run the existing database downgrade
only if the new scope migration prevents the previous release from operating, and verify Stage 1
summary/investigation behavior. Disable the new target keys/accounts after the previous release is
healthy. Never remove audit history or reuse the administrative deployment key for runtime access.
