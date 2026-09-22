# Stage 1 controlled completion report

[فارسی](../fa/STAGE_1_COMPLETION_REPORT.md) · [Testing](TESTING.md) · [Project state](../PROJECT_STATE.md)

**Change ID:** `stage1-completion-20260922-01`

**Completed:** 2026-09-23 (Asia/Tehran)

**Decision:** the executable Stage 1 controlled-qualification gates passed. Production promotion is
still withheld because an independently verified off-datastore backup destination, WAL/PITR
recovery and disaster-recovery sign-off do not yet exist.

This report records observed results, not an architectural rebuild or a claim of production
acceptance. Private credentials, addresses, host keys and raw responses remain outside Git. The
sanitized release status is authoritative; detailed raw evidence is retained in the restricted
operator record under change ID `stage1-completion-20260922-01`.

## Results

| Gate | Result | Observed evidence |
|---|---|---|
| Fresh browser with WAN denied | Passed | A new Microsoft Edge context loaded all assets, authenticated, used English/LTR and Persian/RTL, produced a direct general answer and a Persian evidence-grounded answer, displayed provenance/audit identifiers, cleared the tab session on sign-out and required login in a new tab. Page traffic addressed only the private application origin. The deny proxy blocked 21 Edge background Internet attempts. |
| Application rollback | Passed | The application link moved from `13a3369` to verified prior release `fde27bd`; health and authenticated login passed. The link returned to `13a3369`, and health/login passed again. |
| Runtime/model rollback | Passed | Protected rollback copies matched the approved runtime and model SHA-256 values. Both stable links moved to the copies, the production inference API generated successfully, and the original links were restored with another successful generation. This proves artifact-location rollback of identical bits, not a model-version downgrade. |
| Cancellation and recovery | Passed | A client connection was terminated during a live 128-token request. The active slot was observed, then returned to zero with no queued work; a follow-up generation succeeded. |
| Dependency loss and recovery | Passed | Stopping the required llama service stopped the inference boundary and removed both listeners. The application returned a sanitized retryable `503 dependency_unavailable`; restart restored application readiness. |
| Missing/corrupt artifact | Passed | Temporary missing and 4 KiB corrupt model targets failed closed as `503 unavailable`; restoring the verified model link returned successful generation after each case. The approved model was not modified. |
| Low-space behavior | Passed, isolated staging case | Copying the model into a 64 MiB isolated filesystem failed with `ENOSPC`. The active link and model hash were unchanged and generation remained healthy. No serving filesystem was filled. |
| Sustained load | Passed | The five-minute, two-client, 16-token workload completed 99 requests: 98 HTTP 200 and one bounded HTTP 504 (1.01% error rate). Total-latency p50/p95/max were 6.095/6.114/8.520 seconds; queue p50/p95/max were 3042/3050/3424 ms. Scheduler maxima were one active and one queued request. |
| Resource bounds | Passed for the load profile | Average cgroup CPU use was 1585.37% of one core, peak measured service memory was 4,885,475,328 bytes, minimum system-available memory was 128,265,498,624 bytes and maximum one-minute load was 15.93. The guest exposed one NUMA node. The final state was ready with zero active/queued requests. TTFT is not observable through the current non-streaming API. |
| NextOps PostgreSQL restore | Passed, logical isolated restore | The verified custom-format dump restored into a temporary PostgreSQL 16.15 cluster reachable only by a private Unix socket. Nine public tables, Alembic revision `0001_durable_app`, one identity, 9 runs, 65 audit events and the append-only audit trigger were verified. |
| Zabbix PostgreSQL restore | Passed, logical isolated restore | The verified custom-format dump restored into a separate socket-only PostgreSQL 16.15 cluster. The drill verified 203 public tables, one `dbversion` row, 411 hosts, 18,806 items, 3 users, 12 events and 59,022 `history_uint` rows. |
| Temporary restore cleanup | Passed | Both temporary clusters, PostgreSQL-owned dump copies, sockets and test data directories were removed after validation. The restricted source dumps remain available in the operator staging record. |
| Final fleet health | Passed | All four guests reported system state `running`, zero failed units and no reboot requirement after the campaign. |
| Independent disaster backup | **Not passed** | Two checksummed logical dumps exist and restored successfully, but the desktop staging disk and the four guests have no verified independent physical failure domain. A second copy on the same G10/datastore is not disaster recovery. |

## Integrity and recovery identities

- llama.cpp binary SHA-256:
  `dbe5a5cdd4842fe2d498270c1e1df58344e9052e97214e2ba9c9845443a1b0dc`
- Qwen model SHA-256:
  `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`
- NextOps logical dump SHA-256:
  `f621cebfac5f3dfa7df3a7e27762f99c4225bdc7db0d733189dbf8a6c7f5f7b2`
- Zabbix logical dump SHA-256:
  `7951788e7dd32fb4ec7bf1daf9b64379ebd6f8fed120a3042f90a7b623e0e402`

The recovery API rotated the controlled administrator credential to version 2 and revoked 45 prior
sessions. The new credential remains only in the restricted operator record. No secret value was
printed or committed.

## Remaining production gate

Provide and verify an approved destination that survives loss of the serving guest, DS-C/G10 and
its host. Then implement the accepted PostgreSQL-aware design with separate NextOps/Zabbix
repositories, full plus justified differential/incremental backups, continuous WAL archiving,
retention and repository verification. Use `restic` only for approved non-database artifacts.
Repeat the restore on an independent host, exercise PITR and missing/corrupt-WAL failure cases,
record RPO/RTO and key recovery, and obtain operational sign-off. Until then, the deployment remains
**controlled user testing, not production accepted**.
