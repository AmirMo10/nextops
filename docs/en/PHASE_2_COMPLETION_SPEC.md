# Phase 2 completion specification

[فارسی](../fa/PHASE_2_COMPLETION_SPEC.md) · [Architecture decision](../adr/0007-forced-command-linux-connector.md) · [Current state](../PROJECT_STATE.md)

**Status: implementation complete; controlled qualification partial.** Application and connector
release `nextops-0.1.0-e2dad3a` implements the durable incident workflow and bounded Linux/Zabbix
evidence boundary. It is live for controlled user testing, not production-accepted.

## Qualification record — 2026-09-23

| Gate | Status | Evidence |
|---|---|---|
| Source quality and security CI | `passed` | Formatting, lint, strict typing, 128 non-integration tests, PostgreSQL 16/17 jobs, real-browser fixture and secret scan passed |
| Authorization and target boundary | `passed` | Unauthenticated requests returned `401`; unknown/unapproved target returned `403`; the browser and model received no target credentials |
| Four direct Linux collectors | `passed` | Each fixed target returned a schema-valid, bounded, redacted snapshot through its distinct forced-command key; generic shell execution was denied |
| Four composite connector paths | `passed` | Each target returned bounded Zabbix history/events plus direct Linux evidence with explicit partial/truncation metadata |
| Live bilingual local-model flow | `passed` | Fresh English and Persian API investigations returned local CPU answers and durable run/evidence/audit identifiers |
| App/connector restart | `passed` | Both services returned healthy on the promoted release after restart |
| Immutable rollback/forward | `passed` | App and connector each ran the prior release, then returned to `e2dad3a`; the additive migration remained compatible |
| Server/API WAN-denied path | `passed` | Direct public-network access was denied on all four guests while local connector evidence and model generation remained available |
| Fresh live browser on this release | `not_run` | The automation browser did not trust the private CA; no TLS bypass was used. The fixture-backed real-browser test passed but does not substitute for live acceptance |
| Phase 2 serial VM reboot | `not_run` | Stage 1 reboot evidence is preserved but is not counted as a Phase 2 rerun |
| Phase 2 dependency loss/recovery | `not_run` | Stage 1 recovery evidence is preserved but is not counted as a Phase 2 rerun |

All four guests ended `running`, with zero failed units and no reboot requirement. A local
pre-migration PostgreSQL dump passed checksum/list validation, but it is not an independent backup
or restore proof. Independent backup, WAL/PITR, certificate lifecycle and disaster recovery remain
production blockers.

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
