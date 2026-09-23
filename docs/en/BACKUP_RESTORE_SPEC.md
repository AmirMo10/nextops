# Backup and isolated-restore specification

[فارسی](../fa/BACKUP_RESTORE_SPEC.md) · [Specification workflow](SPECIFICATION_WORKFLOW.md) · [Operations](OPERATIONS.md)

**Status: logical restore mechanics exercised and the repository qualification contract is
implemented; independent recovery is blocked.** On
2026-09-23, checksummed custom-format dumps of both PostgreSQL 16 databases restored successfully
into separate socket-only temporary clusters and were verified and removed. This does not satisfy
the independent-backup gate: no destination independent of the serving guests, DS-C/G10 and its
host has been verified; pgBackRest/WAL, PITR, restic artifact recovery, retention and key recovery
remain unimplemented. The [public recovery contract](../../deploy/recovery/README.md) now prevents
an unsupported production claim. See the [Stage 1 report](STAGE_1_COMPLETION_REPORT.md).

## Evaluated design and claim boundary

[ADR 0008](../adr/0008-independent-recovery-repositories.md) proposes separate pgBackRest
repositories for the application and Zabbix PostgreSQL 16 clusters and a third restic repository
only for approved non-database files. The current controlled-bundle candidates are pgBackRest
2.59.1 and restic 0.19.1. They are not installed production dependencies: artifact hashes, exact
offline bundles, dependency/license approval and same-version pgBackRest endpoint verification are
still required.

`deploy/recovery/recovery-profile.yaml` records only public policy and sanitized readiness state.
Its schema plus `scripts/check_recovery_profile.py` reject duplicate YAML keys, shared database
repository IDs, secret-like fields or URL user information, database/WAL inclusion in restic, and
qualified claims without an approved independent destination, RPO/RTO, retention, verified offline
bundles, key recovery and every restore/negative/offline gate. Normal CI accepts the honest blocked
state. Production review must additionally run the validator with `--require-qualified`.

## Problem statement

The controlled deployment has two independent PostgreSQL 16 clusters—NextOps application state and
Zabbix state—plus release artifacts, configuration, manifests, and permitted evidence files. It has
no independently stored, restoration-tested recovery set. A command that reports a successful
backup is insufficient; the release gate is a verified isolated restore.

## Requirements

- Keep the application and Zabbix database repositories, credentials, retention policies, restore
  procedures, and restore evidence separate.
- Evaluate `pgBackRest` as the preferred PostgreSQL-aware candidate for full backups, an explicitly
  justified differential/incremental schedule, WAL archiving, retention, integrity checks, and
  point-in-time recovery. Pin the selected version and prepare its packages offline.
- Evaluate `restic` only for non-database artifacts: protected configuration, release bundles,
  manifests, documentation, and evidence files whose retention policy permits backup. Filesystem
  backup must not replace PostgreSQL-aware backup.
- Store recovery material independently enough to survive the declared guest, datastore, and G10
  failure scenarios. A second directory or VM on the same G10 is staging, not disaster recovery.
- Keep repository credentials, encryption keys, and recovery secrets outside Git and outside
  general backup configuration. Document key-loss recovery and operator separation.
- Perform backup and restore without Internet access after provisioning. No restore step may fetch a
  package, image, release, model, or signing key from the Internet.
- Define proposed RPO/RTO, storage growth, bandwidth, retention, and restore-test cadence before
  implementation; record measured results rather than promises.

## Non-goals

This feature does not provide high availability, database replication, automatic failover, model
artifact redownload, production authorization, or backup of unrestricted secrets. It does not merge
the NextOps and Zabbix databases or turn a same-host copy into disaster recovery.

## Threat considerations

Protect against stolen backup credentials, destructive deletion, ransomware or host compromise,
silent corruption, incomplete WAL chains, restoration into production routes, secret disclosure,
unbounded evidence retention, and untrusted restored configuration. A restored lab must have no
route or credential that can mutate production targets. Logs and reports must redact repository
locations, credentials, keys, private addresses, and sensitive evidence.

## Implementation plan and tasks

1. Inventory database sizes, WAL rates, file classes, retention duties, current mounts, failure
   scenarios, and an approved independent destination using sanitized outputs.
2. Write an ADR comparing pgBackRest/native PostgreSQL alternatives and restic/file-copy
   alternatives, including licensing, offline packaging, encryption, operations, and rollback.
3. Build authenticated, checksummed, pinned offline bundles in a disposable environment. Verify
   install and uninstall behavior without touching the serving guests.
4. Configure least-privilege backup identities and separate repositories for application and Zabbix
   in an isolated lab that mirrors PostgreSQL 16.
5. Exercise full plus chosen differential/incremental backups, WAL archiving, retention expiry,
   repository verification, and interrupted/corrupt/missing-segment failures.
6. Restore each database and permitted file set into isolated hosts with production routes and
   credentials absent. Apply the matching application/Zabbix release and schema compatibility.
7. Verify authentication, authorization, session revocation behavior, audit continuity, evidence
   hashes/references, Zabbix history/configuration, and service restart after restore.
8. Record measured RPO/RTO, CPU, memory, storage, I/O, errors, and operator steps; then update the
   release-status gate and bilingual runbooks.

## Acceptance criteria

- Both PostgreSQL clusters restore independently from the approved destination with a complete,
  verified WAL chain and the intended recovery point.
- The file repository restores only approved classes and matches recorded hashes/manifests.
- The isolated environment starts with Internet unavailable and cannot reach or mutate production
  targets.
- Restored identity, authorization, audit, evidence provenance, application/model compatibility,
  and Zabbix operation pass defined checks.
- Corrupt, incomplete, expired, wrong-key, and wrong-release recovery sets fail safely with useful
  operator errors; no silent fallback or online download occurs.
- The report records exact versions, commands, duration, measured RPO/RTO, resources, failures,
  skipped/not-run cases, cleanup, and residual risks.

## Rollback and documentation

Initial implementation is additive: do not remove an existing recovery copy until the new path has
passed isolated restore and its retention overlap has completed. A failed rollout disables the new
jobs, preserves prior recovery material, removes only verified new configuration, and leaves serving
databases unchanged. Required deliverables are paired English/Persian backup, restore, key-recovery,
failure, and cleanup runbooks plus the ADR, release manifest update, and dated sanitized evidence.
