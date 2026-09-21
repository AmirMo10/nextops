---
name: nextops-project-context
description: Load current NextOps repository state, requirements precedence, and task-specific Markdown context before planning, implementing, reviewing, or reporting work in this repository.
---

# NextOps project context

Use repository artifacts as durable memory. Do not rely on an earlier chat summary when the
current Git state or maintained documents can answer the question.

## Start every NextOps task

1. Inspect `git status`, the current branch, and recent relevant commits.
2. Read `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/NEXT_TASK.md`, and
   `docs/MARKDOWN_CONTEXT_INDEX.md`.
3. Use the routing table in the context index to select the requirements, architecture, safety,
   implementation, and operations documents needed for the task.
4. Read the files that govern the task before editing. Do not load every Markdown file into the
   context window merely because it is cataloged.
5. Inspect the source, tests, manifests, or deployment records that provide current evidence.

## Source precedence

Apply the latest explicit owner instruction first, followed by current project state and next-task
records, the active master prompt and later amendments, current paired guides, accepted ADRs, and
finally the preserved v2 archive for non-conflicting original detail. Historical reports record what
was true at their date; they do not override newer evidence.

Surface a real conflict instead of silently choosing one source. Never reinterpret a proposal,
fixture, test, or documentation statement as server acceptance.

## Keep memory durable

When work changes capability, decisions, deployment status, tests, or the next checkpoint, update
the corresponding maintained Markdown in the same change. Add, rename, or remove the matching entry
in `docs/MARKDOWN_CONTEXT_INDEX.md` whenever a project Markdown file changes identity. Run
`uv run python scripts/check_docs.py` before delivery.

Keep private infrastructure identifiers, credentials, and raw operational evidence outside Git.
Repository instructions do not authorize provisioning or server mutation.
