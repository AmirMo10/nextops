#!/usr/bin/env python3
"""Check repository documentation structure; never contact infrastructure.

بررسی ساختار مستندات؛ بدون تماس با شبکه یا تجهیزات.
This is not an application, security, model-quality, or language-quality test.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
CATALOG_ENTRY = re.compile(r"^- `([^`\n]+\.md)`(?: — .*)?$", re.MULTILINE)
EXCLUDED_MARKDOWN_ROOTS = frozenset(
    {
        ".git",
        ".local",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "dist",
    }
)
REQUIRED = (
    "README.md",
    "README_FA.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/PROJECT_STATE.md",
    "docs/NEXT_TASK.md",
    "docs/MARKDOWN_CONTEXT_INDEX.md",
    "docs/requirements/NEXTOPS_MASTER_PROMPT.md",
    "docs/requirements/TRACEABILITY.md",
    "docs/requirements/SOURCES.md",
)


def project_markdown_files(root: Path) -> list[Path]:
    """Return project-owned Markdown while excluding generated and dependency trees."""

    return sorted(
        path
        for path in root.rglob("*.md")
        if path.relative_to(root).parts[0] not in EXCLUDED_MARKDOWN_ROOTS
    )


def markdown_catalog_entries(text: str) -> set[str]:
    """Read normalized repository-relative Markdown paths from the context index."""

    return {match.replace("\\", "/") for match in CATALOG_ENTRY.findall(text)}


def markdown_catalog_errors(
    root: Path, markdown: tuple[Path, ...] | list[Path], catalog_text: str
) -> list[str]:
    """Report project Markdown missing from the index and stale index entries."""

    actual = {path.relative_to(root).as_posix() for path in markdown}
    normalized_entries = [match.replace("\\", "/") for match in CATALOG_ENTRY.findall(catalog_text)]
    cataloged = set(normalized_entries)
    errors = [f"Markdown context index is missing: {path}" for path in sorted(actual - cataloged)]
    errors.extend(
        f"Markdown context index has stale entry: {path}" for path in sorted(cataloged - actual)
    )
    counts = Counter(normalized_entries)
    errors.extend(
        f"Markdown context index has duplicate entry: {path}"
        for path in sorted(path for path, count in counts.items() if count > 1)
    )
    return errors


def without_fenced_code(text: str) -> str:
    """Remove fenced examples so sample paths are not treated as links."""
    output: list[str] = []
    fence_char = ""
    fence_size = 0
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            mark = match.group(1)
            if not fence_char:
                fence_char, fence_size = mark[0], len(mark)
            elif mark[0] == fence_char and len(mark) >= fence_size:
                fence_char, fence_size = "", 0
            continue
        if not fence_char:
            output.append(line)
    return "\n".join(output)


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")

    en = {p.name for p in (ROOT / "docs/en").glob("*.md")}
    fa = {p.name for p in (ROOT / "docs/fa").glob("*.md")}
    if en != fa:
        errors.append(
            f"Language pairs differ: EN-only={sorted(en - fa)}, FA-only={sorted(fa - en)}"
        )
    if not en:
        errors.append("No paired guides found")

    markdown = project_markdown_files(ROOT)
    checked = 0
    catalog_text: str | None = None
    for path in markdown:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            errors.append(f"Invalid UTF-8: {path.relative_to(ROOT)}: {exc}")
            continue
        checked += 1
        if path == ROOT / "docs/MARKDOWN_CONTEXT_INDEX.md":
            catalog_text = text
        if path.parent == ROOT / "docs/fa" or path.name == "README_FA.md":
            if '<div dir="rtl">' not in text or "</div>" not in text:
                errors.append(f"Missing RTL wrapper: {path.relative_to(ROOT)}")
            if not re.search(r"[\u0600-\u06ff]", text):
                errors.append(f"Missing Persian text: {path.relative_to(ROOT)}")
        for match in LINK.finditer(without_fenced_code(text)):
            destination = match.group(1).strip().split(' "', 1)[0].strip("<>")
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"Link escapes repository: {path.relative_to(ROOT)} -> {destination}")
            elif not target.exists():
                errors.append(f"Broken local link: {path.relative_to(ROOT)} -> {destination}")
    if catalog_text is not None:
        errors.extend(markdown_catalog_errors(ROOT, markdown, catalog_text))
    if errors:
        print("Documentation checks failed / بررسی مستندات ناموفق بود")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"PASS: {checked} Markdown files; {len(en)} EN/FA guide pairs; "
        "context catalog, local links, and RTL wrappers checked."
    )
    print("This is documentation validation only; application and hardware tests were not run.")
    print("این نتیجه فقط مربوط به مستندات است؛ برنامه و سخت‌افزار آزموده نشده‌اند.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
