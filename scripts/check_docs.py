#!/usr/bin/env python3
"""Check repository documentation structure; never contact infrastructure.

بررسی ساختار مستندات؛ بدون تماس با شبکه یا تجهیزات.
This is not an application, security, model-quality, or language-quality test.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
REQUIRED = (
    "README.md", "README_FA.md", "AGENTS.md", "CONTRIBUTING.md",
    "SECURITY.md", "docs/PROJECT_STATE.md", "docs/NEXT_TASK.md",
    "docs/requirements/NEXTOPS_MASTER_PROMPT.md",
    "docs/requirements/TRACEABILITY.md", "docs/requirements/SOURCES.md",
)


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
        errors.append(f"Language pairs differ: EN-only={sorted(en-fa)}, FA-only={sorted(fa-en)}")
    if not en:
        errors.append("No paired guides found")

    markdown = sorted(ROOT.rglob("*.md"))
    checked = 0
    for path in markdown:
        if ".git" in path.relative_to(ROOT).parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            errors.append(f"Invalid UTF-8: {path.relative_to(ROOT)}: {exc}")
            continue
        checked += 1
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
    if errors:
        print("Documentation checks failed / بررسی مستندات ناموفق بود")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {checked} Markdown files; {len(en)} EN/FA guide pairs; local links and RTL wrappers checked.")
    print("This is documentation validation only; application and hardware tests were not run.")
    print("این نتیجه فقط مربوط به مستندات است؛ برنامه و سخت‌افزار آزموده نشده‌اند.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
