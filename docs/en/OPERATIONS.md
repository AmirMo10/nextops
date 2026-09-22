# Operations, observability and disaster recovery

[فارسی](../fa/OPERATIONS.md) · [Index](INDEX.md)

**Status: the controlled services are installed and logical isolated restore has passed; no independent backup job or disaster-recovery procedure exists.** Restart, rollback, failure recovery, bounded load and socket-only restores of both PostgreSQL 16 databases passed. Independent storage, WAL/PITR, artifact recovery and disaster recovery remain open. See the [backup specification](BACKUP_RESTORE_SPEC.md) and [Stage 1 report](STAGE_1_COMPLETION_REPORT.md).

## Environments and service boundaries

Use separate development, staging and production identities, databases, volumes, ports and inventories. On one G10 these remain one physical failure domain. Only intended UI ingress is exposed; inference, database, MCP and telemetry administration remain internal. Verify container and host rules together rather than assuming every published port is protected.

Use restricted users/capabilities, bounded resources and reviewed restart policies. Lifecycle scripts must be idempotent, preflight changes, protect existing services and avoid secret output. Do not change SSH/firewalls, reboot or reformat without explicit authorization and recovery access. Serialize migrations.

## Observe the platform itself

Track API/worker/connector health, durable queue age, collection failures, inference queue/TTFT/tokens, CPU/RAM/swap pressure, database state, audit failures, storage growth, backup age and restore-test status. Use structured logs, metrics and justified traces without hosted telemetry dependence. Avoid sensitive prompts and unbounded asset/user identifiers in metric labels.

Distinguish host health, application readiness, model readiness and each connector's actual capability. Ordinary logs support diagnosis; security audit provides a separate record of authorized decisions and effects.

## Degraded operation

| Failure | Required behavior |
|---|---|
| Model absent/saturated | Keep API, audit and manual evidence views usable; queue/reject work within limits |
| Connector fails | Return typed partial results; isolate the failure; bounded eligible-read retries |
| Database unavailable | Do not pretend jobs or approvals are durable; expose degraded readiness |
| Audit unavailable | Block mutations and alert; never silently drop the record |
| Mutation timeout | Mark unknown outcome; reconcile target state before retry |
| Host loss | Recover from independent backups and external recovery instructions |

Alert-storm handling deduplicates and groups evidence before expensive synthesis. Required outage notifications need a path outside the failed host.

## Backup and restore

Back up PostgreSQL consistently, permitted sanitized evidence, non-secret configuration and model manifests. Keep encryption recovery material in a separate protected process. Models can be re-imported only when documented in the recovery plan. Encrypt backup artifacts, define retention and access, and test restoration in an isolated environment.

An independent off-host destination is a production decision. A second partition, local directory or container on the G10 is staging, not disaster recovery. Define proposed recovery point/time objectives, then measure them in a restore drill. Validate restored identity, authorization, evidence references, audit continuity and keys; protect against accidentally connecting the restored test instance to production assets.

## Release and rollback

Promote verified artifacts explicitly. Record release identity and configuration/model/schema compatibility, take required backups, run serialized migrations and verify health. Rolling back an image is not a schema rollback. Prefer compatible expand/contract changes or a tested restore path when needed. Compensation on remote equipment requires separate authorization and may not be possible.

The operational handover must include offline bundle contents/checksums, clean-start procedure, monitoring ownership, recovery access, backup destination, retention, measured limits, known single-host risks and a dated readiness decision.
