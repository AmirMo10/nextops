"""Deterministic question focus for bounded, read-only incident explanations."""

# Intentional Persian patterns contain characters flagged as confusable by Ruff.
# ruff: noqa: RUF001

from __future__ import annotations

import re
from typing import Literal

IncidentFocus = Literal["overview", "filesystems", "file_listing"]

_FILESYSTEM = re.compile(
    r"(?:\b(?:filesystems?|file\s+systems?|disk\s+(?:space|usage)|mounts?|"
    r"storage\s+(?:space|usage))\b|فایل[‌ ]?سیستم|سامانه[‌ ]?فایل|فضای\s*دیسک|"
    r"پارتیشن|نقطه[‌ ]?اتصال)",
    re.IGNORECASE,
)
_FILES = re.compile(
    r"(?:\b(?:files?|directories|directory|folders?)\b|/(?:etc|var|usr)(?:/|\b)|"
    r"فایل[‌ ]?ها|پرونده[‌ ]?ها|پوشه[‌ ]?ها|فایل[‌ ]?های\s*سیستم)",
    re.IGNORECASE,
)
_OTHER = re.compile(
    r"(?:\b(?:services?|cpu|memory|ram|events?|journal|processes?|network|"
    r"problems?|everything|all\s+data)\b|سرویس|پردازنده|حافظه|رویداد|فرایند|"
    r"شبکه|همه[ٔ‌ ]?\s*داده)",
    re.IGNORECASE,
)
_FILE_ACTION = re.compile(
    r"(?:\b(?:show(?:ing)?|list(?:ing)?|display(?:ing)?|find(?:ing)?|"
    r"read(?:ing)?|open(?:ing)?)\b|نشان|نمایش|فهرست|بخوان|باز\s*کن)",
    re.IGNORECASE,
)
_EXCLUDED_OTHER = re.compile(
    r"(?:\b(?:no|not|without|exclude|excluding)\s+(?:any\s+|the\s+)?"
    r"(?:services?|cpu|memory|ram|events?|journal|processes?|network|problems?)\b|"
    r"بدون\s*(?:سرویس|پردازنده|حافظه|رویداد|فرایند|شبکه))",
    re.IGNORECASE,
)


def incident_focus(question: str) -> IncidentFocus:
    """Narrow only an unambiguous single-topic request; never grant new access."""

    filesystem_requested = bool(_FILESYSTEM.search(question))
    file_requested = bool(_FILES.search(question))
    if file_requested and not filesystem_requested and _FILE_ACTION.search(question):
        return "file_listing"
    if _OTHER.search(_EXCLUDED_OTHER.sub("", question)):
        return "overview"
    if filesystem_requested:
        return "filesystems"
    if file_requested:
        return "file_listing"
    return "overview"
