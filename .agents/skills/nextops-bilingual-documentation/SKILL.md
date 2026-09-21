---
name: nextops-bilingual-documentation
description: Create or update NextOps Markdown, requirements, README, operator guidance, traceability, ADRs, or paired English and Persian documentation without losing project history.
---

# NextOps bilingual documentation

Load `nextops-project-context` first and identify whether the document is current guidance,
historical evidence, an accepted decision, or an immutable archive.

## Documentation rules

- Keep files under `docs/en` and `docs/fa` paired by filename and meaning. Write natural Persian,
  preserve the RTL wrapper, and keep code identifiers and commands unchanged.
- Do not translate, reword, or overwrite
  `docs/requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md`.
- Preserve dated historical reports. Correct active indexes, state, next task, traceability, and
  operator guidance instead of retroactively changing what an older report observed.
- Distinguish implemented source, passing tests, package-layer tooling, server evidence, and full
  deployment acceptance. Never promote one evidence class into another.
- Update `docs/MARKDOWN_CONTEXT_INDEX.md` in the same change when any project Markdown file is
  added, renamed, or removed.

## Validation

Run `uv run python scripts/check_docs.py`. When the change touches deployment dossiers, inference
artifacts, or installers, also run their matching validator under `scripts/`. Report application or
hardware tests only when they actually ran.
