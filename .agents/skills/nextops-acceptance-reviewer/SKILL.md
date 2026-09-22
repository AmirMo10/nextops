---
name: nextops-acceptance-reviewer
description: Review a NextOps change or release candidate against offline, security, reliability, bilingual, and recovery acceptance requirements without operating live infrastructure.
---

# NextOps acceptance reviewer

Load `nextops-project-context`, then read the governing specification, changed files, tests, current
release manifest, and relevant acceptance cases. This is an evidence review; it grants no
infrastructure access or approval.

## Review dimensions

Check the change for:

- local CPU-only execution and absence of cloud or silent runtime downloads;
- authentication, deterministic authorization, least privilege, target scope, and credential
  isolation from the model and browser;
- durable audit, correlation, evidence provenance, freshness, partial/stale labeling, and safe
  handling of untrusted monitoring text;
- bounded input, output, queues, retries, timeouts, CPU, memory, storage, and failure recovery;
- explicit unavailable, denied, partial, stale, overload, expiry, and unknown-outcome behavior;
- rollback, backup, isolated restore, schema compatibility, and disaster-recovery implications;
- English/Persian behavior, RTL/LTR, accessibility, and technical-identifier isolation;
- accurate dependency locks, artifact identity, licensing, and offline provisioning requirements.

## Evidence rules

Report each applicable gate as `passed`, `failed`, `partial`, or `not_run`, with the exact command,
test, artifact, or dated record supporting it. A missing test is `not_run`, not an inferred pass.
Simulated dependency faults do not prove WAN isolation, and a successful backup command does not
prove restoration.

Lead with blocking findings and regressions. Do not approve production readiness while any required
gate is failed, partial, or not run. Do not reveal secrets or copy private operational evidence into
the repository.
