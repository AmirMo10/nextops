# Specification-driven development

[فارسی](../fa/SPECIFICATION_WORKFLOW.md) · [Index](INDEX.md) · [Current status](../status/current-release.yaml)

**Status: adopted for bounded brownfield changes; no project regeneration or Spec Kit runtime has
been installed.** Existing requirements, accepted ADRs, current project state, and working source
remain authoritative.

NextOps adopts the useful brownfield pattern from [GitHub Spec Kit](https://github.com/github/spec-kit):
specify → plan → tasks → implement → converge. It does not import the complete template repository,
replace the existing documentation tree, or allow generated text to override accepted security and
offline constraints. Spec Kit is MIT-licensed; a later tool installation still requires a pinned,
reviewed dependency decision.

## When a feature needs a specification

Create a bounded feature packet for a new dependency, connector, recovery mechanism, persistent
schema, public contract, deployment profile, security boundary, or acceptance program. Small defect
repairs may use an issue and test when they do not alter those boundaries.

Each feature packet must contain:

1. problem statement and user/operational outcome;
2. requirements and measurable invariants;
3. non-goals and compatibility boundaries;
4. threat and privacy considerations;
5. implementation plan and dependencies;
6. reviewable task breakdown;
7. acceptance criteria with pass/fail evidence;
8. rollback, recovery, and migration strategy;
9. required English/Persian and operator documentation.

Specifications describe intent. `docs/status/current-release.yaml` records the current sanitized
release and gate state; `PROJECT_STATE.md` records the evidence narrative; `NEXT_TASK.md` selects the
next unfinished checkpoint. Historical reports remain unchanged.

## Convergence rule

A feature converges only when implementation, tests, manifests, current documentation, and rollback
evidence agree with its requirements. Record unavailable lab or production evidence as `not_run`.
The agent workflows under `.agents/skills` help plan and review work but are not security boundaries,
approvers, or holders of infrastructure credentials.

The first packet governed by this process is the [backup and isolated-restore specification](BACKUP_RESTORE_SPEC.md).
