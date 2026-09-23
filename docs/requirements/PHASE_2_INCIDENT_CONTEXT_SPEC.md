# Phase 2 incident-context specification

**Status:** Increment 2A is implemented and deployed as immutable app/connector release
`nextops-0.1.0-1ab6586`. Exact Zabbix role expansion, live bounded retrieval, release/role rollback
and guarded WAN isolation pass. Authenticated browser/session acceptance, durable model/audit use,
VM reboot and direct Linux diagnostics are not yet run.

## Problem and outcome

The accepted Phase 1 flow provides a current Zabbix snapshot, but an operator cannot yet inspect a
bounded timeline when diagnosing an incident. Phase 2 begins by adding recent numeric history and
trigger events to the existing protected connector without widening it into an arbitrary Zabbix
proxy. The operator outcome for Increment 2A is an authenticated, source-qualified incident-context
response for the one preconfigured host.

## Requirements and invariants

- Preserve the existing fixed connector target, TLS verification, protected token, service bearer,
  proxy bypass and one-megabyte per-call response ceiling.
- Expose only the named `incident-context` operation. A caller cannot select a Zabbix method, host,
  item, event source, output field, sort, limit or arbitrary time range.
- Require both a valid application session and its server-derived `zabbix.read` scope before the
  application calls the credential-isolated connector.
- Use the configured lookback, defaulting to 60 minutes and bounded to 15–1,440 minutes.
- Query only numeric history types `0` and `3`, at most four selected items and eight values per
  item. Return at most 32 history points in total.
- Query only trigger events (`source=0`, `object=0`) for the configured host and return at most 25.
- Ask upstream for one row beyond each public limit so truncation is explicit rather than inferred
  from a full page.
- Preserve collection and source timestamps, event state, acknowledgement and suppression state.
- Treat every item name, key, value, unit and event name as untrusted evidence. Authentication and
  source identity do not make their text an instruction.
- Propagate current-snapshot partial reasons and add bounded reasons for truncated history metrics,
  history points and events.
- Keep Phase 1 summary and investigation contracts compatible. No mutation, acknowledgement,
  configuration method, remote command, shell or SQL surface is introduced.

## Non-goals and compatibility

Increment 2A does not select among the four monitored hosts, perform direct Linux diagnostics,
produce an RCA claim, change the browser workflow, persist a new incident schema, or declare live
deployment acceptance. It does not copy Zabbix history into PostgreSQL wholesale. Phase 1 routes
remain unchanged, and the new route is additive.

## Threat and privacy considerations

The principal threats are target substitution, unbounded history extraction, prompt injection in
monitoring text, inference from deleted entities retained by Zabbix housekeeping, oversized
responses and expansion of the reader role into write capability. Fixed server-side parameters,
host scoping, exact fields, bounded calls, strict contracts, output limits and explicit partial
markers mitigate these threats. The browser and model still receive no Zabbix credential.

## Implementation plan and tasks

1. Add strict incident, event and history contracts with source/time consistency validation.
2. Refactor the existing client to reuse one current snapshot, then perform fixed bounded
   `history.get` and `event.get` reads.
3. Add the authenticated connector route and the authenticated application gateway route.
4. Add a bounded deployment setting for the incident lookback.
5. Test allowlisted methods and parameters, authentication, source/time provenance, partial markers,
   malformed data, and unchanged Phase 1 behavior.
6. After review, deploy immutable connector/application releases, expand the existing Zabbix reader
   role by exactly `history.get` and `event.get`, and perform live rollback/offline qualification.
7. Follow with Increment 2B: immutable target selection and named direct Linux diagnostics under a
   separately scoped credential boundary.

## Acceptance criteria

- Repository formatting, lint, strict typing, unit/API tests and documentation validation pass.
- Unauthenticated calls and authenticated actors without `zabbix.read` fail; allowed calls expose
  no credential or arbitrary proxy.
- Recorded calls contain only `apiinfo.version`, `host.get`, `item.get`, `problem.get`,
  `history.get` and `event.get`, with fixed host, source/object, fields, windows and limits.
- More than eight points, 25 events or four numeric items is truncated and visibly marked partial.
- Malformed or over-limit upstream responses fail with the existing safe dependency error boundary.
- A live Zabbix 7.0.30 call and guarded WAN-denied server-path check passed under change
  `phase2a-incident-context-20260923-01`. Authenticated browser use and VM reboot were `not_run` at
  that historical checkpoint; the current release manifest records their later qualification.

## Rollback, recovery and documentation

Source rollback removes the additive routes and contracts while leaving Phase 1 summary behavior
unchanged. Live rollback must atomically return both application and connector release links to
their previously qualified versions and remove only the two newly authorized read methods from the
reader role. No database migration is required. Update English/Persian configuration, data/API,
integration, testing, roadmap and current-state guidance together; never present source tests as a
live deployment result.

## Primary protocol references

- [Zabbix 7.0 `history.get`](https://www.zabbix.com/documentation/7.0/en/manual/api/reference/history/get)
- [Zabbix 7.0 `event.get`](https://www.zabbix.com/documentation/7.0/en/manual/api/reference/event/get)
