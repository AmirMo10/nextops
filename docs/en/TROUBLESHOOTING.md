# Troubleshooting without unsafe shortcuts

[فارسی](../fa/TROUBLESHOOTING.md) · [Index](INDEX.md)

**Status: diagnostic playbook requirements, not evidence of installed services.** Source: master specification sections 10–14 and 18–21. Collect timestamps, run/operation IDs and sanitized errors before changing anything.

| Symptom | Safe investigation | Do not do |
|---|---|---|
| No application starts after clone | Check project state and required development environment: a source ASGI factory and migration exist, but there is no production installer/service unit and configuration fails closed without required secrets/database URL | Invent a production installer, use placeholder secrets, or report an undeployed service as failed |
| Slow model responses | Separate queue delay, prompt time and generation time; inspect effective CPUs, NUMA placement, thread pools, context and contention | Increase every worker to 90 threads or choose a larger model because RAM is free |
| Model unavailable | Validate local artifact path/checksum, CPU build, model/template compatibility and resource cap | Fall back to an external AI API or download during offline runtime |
| Permission denied | Check actor, target/environment scope, named tool and current policy; use an authorized administrator for changes | Disable authorization or give the model admin credentials |
| Approval rejected | Check exact digest, expiry, nonce, pre-state and current requester/approver permissions | Reuse old consent after arguments or target changed |
| Connector timeout | Check approved route, verified TLS/SSH identity, scoped credentials, API/version limits and output deadline | Disable certificate checking, scan unrelated networks or blindly retry a mutation |
| SQL diagnostics fail | Check engine/version, diagnostic view permissions, bounded query support and read-only identity | Grant blanket database administrator privileges |
| Persian layout broken | Check RTL container, isolated LTR identifiers, local font/assets and both-language browser tests | Translate executable commands or modify device identifiers |
| Stale or misleading RCA | Check source freshness, time window, clock skew, scope, missing evidence and alternative causes | Present correlation or old incident memory as a verified current cause |
| Audit/database failure | Mark degraded readiness and prevent mutations; recover durable storage first | Continue changes with missing audit or pretend a job was persisted |
| Disk/memory pressure | Inspect resource budgets, retention and approved cleanup/backup procedures | Delete unknown data, run destructive disk tests or drop shared-host caches |
| Mutation outcome unknown | Record `OUTCOME_UNKNOWN`; gather fresh state; reconcile manually when necessary | Mark success from a timeout or blindly repeat the operation |

## Escalation record

Provide release/commit, component and model versions, relevant sanitized configuration references, run/operation/correlation IDs, time window, expected versus observed behavior, scope and reproducible steps. Preserve evidence securely. Do not post production addresses, secrets or raw discovery output in public issues.

## Recovery principle

A restarted process does not prove a remote action stopped. A passing health endpoint does not prove a connector can access a particular vendor/version. A recovered container does not prove database migrations or approvals are consistent. Verify the relevant postconditions and retain unresolved facts explicitly.

For host/network changes, obtain authorization and a tested access-recovery route. The documentation task itself authorizes no host changes.
