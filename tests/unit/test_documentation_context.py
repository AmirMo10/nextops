import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "check_docs.py"
SPEC = importlib.util.spec_from_file_location("nextops_check_docs", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECK_DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_DOCS)

markdown_catalog_entries = CHECK_DOCS.markdown_catalog_entries
markdown_catalog_errors = CHECK_DOCS.markdown_catalog_errors
project_markdown_files = CHECK_DOCS.project_markdown_files


def test_project_markdown_files_excludes_generated_and_dependency_trees(tmp_path: Path) -> None:
    tracked_paths = (
        ".agents/skills/context/SKILL.md",
        ".github/pull_request_template.md",
        "docs/dist/guide.md",
        "docs/guide.md",
    )
    ignored_paths = (
        ".git/README.md",
        ".mypy_cache/README.md",
        ".pytest_cache/README.md",
        ".ruff_cache/README.md",
        ".venv/lib/site-packages/dependency/README.md",
        "dist/README.md",
    )
    for relative_path in tracked_paths + ignored_paths:
        path = tmp_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Test\n", encoding="utf-8")

    discovered = {
        path.relative_to(tmp_path).as_posix() for path in project_markdown_files(tmp_path)
    }

    assert discovered == set(tracked_paths)


def test_markdown_catalog_reports_missing_and_stale_entries(tmp_path: Path) -> None:
    project_paths = (tmp_path / "README.md", tmp_path / "docs/guide.md")
    catalog = """
- `README.md` — Repository entry point.
- `docs/removed.md` — Stale entry.
"""

    assert markdown_catalog_entries(catalog) == {"README.md", "docs/removed.md"}
    assert markdown_catalog_errors(tmp_path, project_paths, catalog) == [
        "Markdown context index is missing: docs/guide.md",
        "Markdown context index has stale entry: docs/removed.md",
    ]

    duplicate_catalog = """
- `README.md` — First entry.
- `README.md` — Duplicate entry.
- `docs/guide.md` — Guide.
"""
    assert markdown_catalog_errors(tmp_path, project_paths, duplicate_catalog) == [
        "Markdown context index has duplicate entry: README.md"
    ]


def test_repository_markdown_context_index_is_complete() -> None:
    root = Path(__file__).resolve().parents[2]
    project_paths = project_markdown_files(root)
    catalog = (root / "docs/MARKDOWN_CONTEXT_INDEX.md").read_text(encoding="utf-8")

    assert markdown_catalog_errors(root, project_paths, catalog) == []
