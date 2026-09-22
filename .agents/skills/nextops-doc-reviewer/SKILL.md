---
name: nextops-doc-reviewer
description: Review current NextOps documentation for English/Persian parity, status drift, broken links, architecture drift, and inconsistent release terminology while preserving historical evidence.
---

# NextOps documentation reviewer

Load `nextops-project-context` and `nextops-bilingual-documentation`. Compare current guidance with
`docs/status/current-release.yaml`, `docs/PROJECT_STATE.md`, `docs/NEXT_TASK.md`, implemented source,
tests, deployment artifacts, and accepted ADRs.

## Review

Check English/Persian pairs for equivalent meaning, natural Persian, RTL wrappers, stable technical
identifiers, and matching links. Find stale deployment claims, contradictory next actions,
aspirational diagrams presented as actual architecture, obsolete release names, inconsistent
component names, undocumented acronyms, ambiguous production-readiness wording, and version drift.

Preserve immutable archives, accepted ADR history, changelog entries, and dated reports. Correct
active indexes, guides, state, and manifests instead of rewriting what a historical record observed.
Markdown remains authoritative human documentation; generated portals are renderers, not a second
source of truth.

Run `uv run python scripts/check_docs.py` and the release-status validator. Treat those checks as
structural validation only; Persian quality and truthfulness require human review. Report external
link maintenance separately from the fully offline local-link gate.
