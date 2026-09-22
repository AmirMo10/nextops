---
name: nextops-change-planner
description: Plan a bounded NextOps feature or repair from the current repository state without rebuilding completed work or treating agent output as authorization.
---

# NextOps change planner

Load `nextops-project-context` first. Use this workflow before a substantial feature, deployment
change, migration, new dependency, connector, recovery mechanism, or architectural refactor.

## Establish the baseline

1. Inspect the current Git state and the files changed by the proposed work.
2. Read `docs/status/current-release.yaml`, `docs/PROJECT_STATE.md`, `docs/NEXT_TASK.md`, the relevant
   accepted ADRs, and the task route in `docs/MARKDOWN_CONTEXT_INDEX.md`.
3. Inspect neighboring source, tests, deployment artifacts, dependency locks, and CI. Classify each
   relevant capability as implemented, partially implemented, planned, contradicted, or unknown.
4. Treat historical reports as dated evidence, not current instructions. Flag contradictions
   instead of silently selecting the most convenient claim.

## Produce a bounded plan

Define the problem, requirements, non-goals, dependencies, threat considerations, operational and
documentation impact, acceptance tests, rollback/recovery path, and explicit out-of-scope work.
Split the plan into reviewable increments with observable exit criteria. Reuse working boundaries;
require an ADR only for a durable architectural decision.

The plan must preserve CPU-only local inference, offline restart, bilingual behavior, Zabbix-first
evidence, default denial, credential isolation, auditability, provenance, bounded resources, and
least privilege. A plan is not infrastructure authorization and must not contain operational
credentials or private inventory.

Before implementation, identify which results can be proven locally, which need an isolated lab,
and which remain not run. Never label a fixture, schema check, simulated fault, or agent review as
deployment acceptance.
