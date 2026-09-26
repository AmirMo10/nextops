"""Deterministic truthfulness controls around locally generated assistant text."""

# Ruff's confusable-character rule is not suitable for intentional Persian user-facing text.
# ruff: noqa: RUF001

from __future__ import annotations

import re
from datetime import datetime

from nextops.api.incident_focus import incident_focus
from nextops.contracts.assistant import AssistantRequest, AssistantResponse
from nextops.contracts.incidents import IncidentEvidence, IncidentInvestigationRequest
from nextops.contracts.monitoring import MonitoringSummary
from nextops.inference.contracts import FinishReason

_LIVE_QUESTION_MARKERS = re.compile(
    r"(?:\b(?:current|currently|now|today|live|status|state|health|running|available|"
    r"restarted|rebooted|deployed|installed|changed)\b|"
    r"(?:وضعیت|همین\s*الان|اکنون|فعلی|زنده|سلامت|در\s*حال\s*اجرا|راه[‌ ]اندازی\s*مجدد|"
    r"ری[‌ ]استارت|نصب|اعمال))",
    re.IGNORECASE,
)
_OPERATIONAL_SUBJECT_MARKERS = re.compile(
    r"(?:\b(?:server|service|system|database|zabbix|linux|host|vm|deployment|application|"
    r"connector|infrastructure)\b|"
    r"(?:سرور|سرویس|سامانه|سیستم|پایگاه\s*داده|زبیکس|لینوکس|میزبان|ماشین\s*مجازی|"
    r"استقرار|برنامه|کانکتور|زیرساخت))",
    re.IGNORECASE,
)
_UNSAFE_EXECUTION_CLAIMS = (
    re.compile(
        r"\b(?:i|we)\s+(?:have\s+)?(?:successfully\s+)?(?:restarted|rebooted|deployed|"
        r"installed|changed|deleted|fixed|executed|ran|rotated)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:من|ما).{0,32}(?:راه[‌ ]اندازی\s*مجدد|ری[‌ ]استارت|استقرار|نصب|تغییر|حذف|"
        r"اصلاح|اجرا|تعویض).{0,24}(?:کردم|کردیم|انجام\s*دادم|انجام\s*دادیم|شد|شده\s*است)",
        re.IGNORECASE,
    ),
)
_UNSUPPORTED_CAUSE_CLAIMS = (
    re.compile(r"\b(?:the\s+)?(?:root\s+)?cause\s+(?:is|was)\b", re.IGNORECASE),
    re.compile(r"\b(?:was|is)\s+caused\s+by\b", re.IGNORECASE),
    re.compile(r"علت\s+(?:اصلی|ریشه[‌ ]ای).{0,20}(?:است|بود)", re.IGNORECASE),
)
_PARTIAL_DISCLOSURE = re.compile(
    r"(?:\b(?:partial|incomplete|limited|truncated)\b|(?:ناقص|جزئی|محدود|کامل\s+نیست))",
    re.IGNORECASE,
)
_STALE_DISCLOSURE = re.compile(
    r"(?:\b(?:stale|outdated|not\s+current|current\s+(?:state|status)\s+is\s+unknown)\b|"
    r"(?:قدیمی|کهنه|به[‌ ]روز\s+نیست|وضعیت\s+فعلی.{0,12}نامعلوم))",
    re.IGNORECASE,
)
_ZABBIX_DISCLOSURE = re.compile(r"(?:\bzabbix\b|زبیکس)", re.IGNORECASE)
_LINUX_DISCLOSURE = re.compile(r"(?:\blinux\b|لینوکس)", re.IGNORECASE)
_PROMPT_BOUNDARY_LEAK = re.compile(
    r"(?:user question \((?:bounded )?untrusted|untrusted zabbix|"
    r"data only, never instructions|answer the user's question directly)",
    re.IGNORECASE,
)
_SYSTEM_FILE_REQUEST = re.compile(
    r"(?:\b(?:show(?:ing)?|list(?:ing)?|display(?:ing)?|find(?:ing)?)\b.{0,60}"
    r"\b(?:system files|filesystems?|file systems?)\b|"
    r"(?:نشان\s*بده|نمایش\s*بده|فهرست\s*کن).{0,60}(?:فایل|فایل[‌ ]?سیستم)|"
    r"(?:فایل|فایل[‌ ]?سیستم).{0,60}(?:نشان\s*بده|نمایش\s*بده|فهرست\s*کن))",
    re.IGNORECASE,
)


def assure_general_answer(
    request: AssistantRequest,
    assistant: AssistantResponse,
) -> AssistantResponse:
    """Label model-only output and replace unverifiable operational claims."""

    requires_live_evidence = bool(
        _LIVE_QUESTION_MARKERS.search(request.question)
        and _OPERATIONAL_SUBJECT_MARKERS.search(request.question)
    )
    file_request = bool(_SYSTEM_FILE_REQUEST.search(request.question))
    unsafe_claim = _contains_unsafe_execution_claim(assistant.answer)
    prompt_echo = _is_long_prompt_echo(request.question, assistant.answer)
    incomplete = assistant.finish_reason != FinishReason.STOP
    if (
        not requires_live_evidence
        and not file_request
        and not unsafe_claim
        and not prompt_echo
        and not incomplete
    ):
        return assistant.model_copy(
            update={
                "evidence_mode": "model_only",
                "live_monitoring_data": False,
                "integrity_status": "model_unverified",
                "limitations": ("no_live_evidence", "model_output_may_be_incorrect"),
            }
        )

    limitations: tuple[str, ...]
    if file_request:
        answer = (
            "دستیار عمومی به فایل‌های سیستم دسترسی ندارد. «بررسی رخداد» تنها می‌تواند ظرفیت "
            "نقاط اتصالِ مجاز را نشان دهد، نه نام یا محتوای فایل‌ها."
            if request.locale == "fa"
            else "General assistant cannot inspect system files. Incident investigation can show "
            "only approved filesystem mount capacity, not file names or contents."
        )
        integrity_status = "scope_redirect"
        limitations = (
            "no_live_evidence",
            "read_only_no_action_performed",
            "file_listing_unavailable",
        )
    elif prompt_echo or incomplete:
        answer = (
            "مدل محلی پاسخ قابل اتکایی تولید نکرد. پرسش را با عبارت‌بندی دقیق‌تر دوباره مطرح کنید؛ "
            "برای وضعیت زیرساخت نیز یکی از حالت‌های دارای شاهد زنده را به کار ببرید."
            if request.locale == "fa"
            else "The local model did not produce a reliable answer. Rephrase the question more "
            "precisely, or use a live evidence mode for infrastructure state."
        )
        integrity_status = "deterministic_fallback"
        limitations = ("no_live_evidence", "model_output_may_be_incorrect")
    else:
        answer = (
            "حالت «دستیار عمومی» به شواهد زنده دسترسی ندارد؛ بنابراین نمی‌توانم وضعیت فعلی "
            "زیرساخت یا انجام‌شدن یک عملیات را تأیید کنم. برای دریافت دادهٔ تازه و قابل انتساب، "
            "حالت «پایش زنده» یا «بررسی رخداد» را انتخاب کنید."
            if request.locale == "fa"
            else "General assistant mode has no live evidence, so I cannot verify the current "
            "infrastructure state or claim that an operation occurred. Select Live monitoring or "
            "Incident investigation for fresh, attributable evidence."
        )
        integrity_status = "scope_redirect"
        limitations = ("no_live_evidence", "read_only_no_action_performed")
    return assistant.model_copy(
        update={
            "answer": answer,
            "evidence_mode": "model_only",
            "live_monitoring_data": False,
            "integrity_status": integrity_status,
            "limitations": limitations,
        }
    )


def assure_monitoring_answer(
    request: AssistantRequest,
    assistant: AssistantResponse,
    evidence: MonitoringSummary,
) -> AssistantResponse:
    """Accept bounded synthesis only when mandatory monitoring qualifiers survive."""

    is_stale = any(metric.stale for metric in evidence.metrics)
    limitations = _evidence_limitations(is_partial=evidence.is_partial, is_stale=is_stale)
    if _SYSTEM_FILE_REQUEST.search(request.question):
        if request.locale == "fa":
            qualification = (
                f" شاهد Zabbix ناقص است ({', '.join(evidence.partial_reasons)})."
                if evidence.is_partial
                else ""
            ) + (" برخی سنجه‌های Zabbix قدیمی‌اند." if is_stale else "")
        else:
            qualification = (
                f" Zabbix evidence is partial ({', '.join(evidence.partial_reasons)})."
                if evidence.is_partial
                else ""
            ) + (" Some Zabbix metrics are stale." if is_stale else "")
        answer = (
            "پایش Zabbix نام یا محتوای فایل‌های سیستم را نمی‌بیند. برای ظرفیت نقاط اتصالِ "
            "مجاز، حالت «بررسی رخداد» را انتخاب کنید؛ آن حالت نیز فایل‌ها را فهرست "
            f"نمی‌کند.{qualification}"
            if request.locale == "fa"
            else "Zabbix monitoring cannot see system file names or contents. Choose Incident "
            "investigation for approved filesystem mount capacity; it cannot list files "
            f"either.{qualification}"
        )
        return assistant.model_copy(
            update={
                "answer": answer,
                "evidence_mode": "live_zabbix",
                "live_monitoring_data": True,
                "integrity_status": "deterministic_focus",
                "limitations": (*limitations, "file_listing_unavailable"),
            }
        )
    safe = (
        _is_safe_evidence_answer(
            assistant.answer,
            require_linux=False,
            is_partial=evidence.is_partial,
            is_stale="stale_evidence" in limitations,
        )
        and assistant.finish_reason == FinishReason.STOP
        and not _is_long_prompt_echo(request.question, assistant.answer)
    )
    return assistant.model_copy(
        update={
            "answer": assistant.answer if safe else _monitoring_fallback(request.locale, evidence),
            "evidence_mode": "live_zabbix",
            "live_monitoring_data": True,
            "integrity_status": "evidence_bounded" if safe else "deterministic_fallback",
            "limitations": limitations,
        }
    )


def assure_incident_answer(
    request: IncidentInvestigationRequest,
    assistant: AssistantResponse,
    evidence: IncidentEvidence,
) -> AssistantResponse:
    """Accept bounded synthesis only when both evidence sources remain explicit."""

    is_stale = any(metric.stale for metric in evidence.zabbix.summary.metrics)
    limitations = _evidence_limitations(is_partial=evidence.is_partial, is_stale=is_stale)
    focus = incident_focus(request.question)
    if focus != "overview":
        # A lexical source check cannot verify whether a generated file name or capacity is real.
        # Render the bounded collector data directly until semantic validation is qualified.
        return assistant.model_copy(
            update={
                "answer": _focused_incident_summary(request.locale, evidence, focus),
                "evidence_mode": "live_zabbix_linux",
                "live_monitoring_data": True,
                "integrity_status": "deterministic_focus",
                "limitations": (
                    (*limitations, "file_listing_unavailable")
                    if focus == "file_listing"
                    else limitations
                ),
            }
        )
    safe = (
        assistant.finish_reason == FinishReason.STOP
        and not _is_long_prompt_echo(request.question, assistant.answer)
        and _is_safe_evidence_answer(
            assistant.answer,
            require_linux=True,
            is_partial=evidence.is_partial,
            is_stale=is_stale,
        )
        and evidence.target_id.casefold() in assistant.answer.casefold()
    )
    return assistant.model_copy(
        update={
            "answer": assistant.answer if safe else _incident_fallback(request.locale, evidence),
            "evidence_mode": "live_zabbix_linux",
            "live_monitoring_data": True,
            "integrity_status": "evidence_bounded" if safe else "deterministic_fallback",
            "limitations": limitations,
        }
    )


def _focused_incident_summary(locale: str, evidence: IncidentEvidence, focus: str) -> str:
    linux = evidence.linux
    when = _timestamp(linux.collected_at)
    partial_fa = (
        f" شواهد ناقص است ({', '.join(evidence.partial_reasons)})." if evidence.is_partial else ""
    )
    partial_en = (
        f" Evidence is partial ({', '.join(evidence.partial_reasons)})."
        if evidence.is_partial
        else ""
    )
    if focus == "file_listing":
        if locale == "fa":
            return (
                f"گردآورندهٔ فقط‌خواندنی Linux برای میزبان {evidence.target_id} در {when} "
                "فهرست نام یا محتوای فایل‌های سیستم را دریافت نکرده است؛ بنابراین نمی‌توانم "
                "آن فایل‌ها را نشان دهم. فقط ظرفیت نقاط اتصالِ مجاز قابل مشاهده است. "
                f"زمان Zabbix منبعی برای تأیید محتوای فایل نیست.{partial_fa}"
            )
        return (
            f"The read-only Linux collector for {evidence.target_id} at {when} did not retrieve "
            "system file names or contents, so I cannot list them. Only approved filesystem "
            f"mount capacity is available. Zabbix does not verify file contents.{partial_en}"
        )
    mounts = linux.filesystems
    if locale == "fa":
        details = (
            "؛ ".join(
                f"{item.path}: {item.used_percent:g}٪ مصرف، {item.available_bytes} بایت آزاد"
                for item in mounts[:3]
            )
            or "هیچ نقطهٔ اتصال مجازی ثبت نشد"
        )
        remainder = f"؛ {len(mounts) - 3} مورد دیگر در جزئیات شواهد" if len(mounts) > 3 else ""
        return (
            f"برای میزبان {evidence.target_id}، نمای فقط‌خواندنی Linux در {when} "
            f"این ظرفیت فایل‌سیستم‌های مجاز را ثبت کرد: {details}{remainder}.{partial_fa} "
            "این داده‌ها فهرست نام یا محتوای فایل‌های سیستم نیستند."
        )
    details = (
        "; ".join(
            f"{item.path}: {item.used_percent:g}% used, {item.available_bytes} bytes available"
            for item in mounts[:3]
        )
        or "no approved mounts were recorded"
    )
    remainder = f"; {len(mounts) - 3} more in evidence details" if len(mounts) > 3 else ""
    return (
        f"For {evidence.target_id}, the read-only Linux snapshot at {when} recorded only "
        f"approved filesystem capacity: {details}{remainder}.{partial_en} "
        "This does not list system file names or contents."
    )


def _contains_unsafe_execution_claim(answer: str) -> bool:
    return any(pattern.search(answer) for pattern in _UNSAFE_EXECUTION_CLAIMS)


def _is_long_prompt_echo(question: str, answer: str) -> bool:
    normalized_question = " ".join(question.casefold().split())
    normalized_answer = " ".join(answer.casefold().split())
    return len(normalized_question) >= 40 and normalized_answer == normalized_question


def _is_safe_evidence_answer(
    answer: str,
    *,
    require_linux: bool,
    is_partial: bool,
    is_stale: bool,
) -> bool:
    if _contains_unsafe_execution_claim(answer):
        return False
    if _PROMPT_BOUNDARY_LEAK.search(answer):
        return False
    if any(pattern.search(answer) for pattern in _UNSUPPORTED_CAUSE_CLAIMS):
        return False
    if not _ZABBIX_DISCLOSURE.search(answer):
        return False
    if require_linux and not _LINUX_DISCLOSURE.search(answer):
        return False
    if is_partial and not _PARTIAL_DISCLOSURE.search(answer):
        return False
    return not (is_stale and not _STALE_DISCLOSURE.search(answer))


def _evidence_limitations(*, is_partial: bool, is_stale: bool) -> tuple[str, ...]:
    values = ["read_only_no_action_performed"]
    if is_stale:
        values.append("stale_evidence")
    if is_partial:
        values.append("partial_evidence")
    return tuple(values)


def _monitoring_fallback(locale: str, evidence: MonitoringSummary) -> str:
    partial = ", ".join(evidence.partial_reasons)
    stale_count = sum(metric.stale for metric in evidence.metrics)
    if locale == "fa":
        qualification = (
            f"شاهد ناقص است ({partial}). "
            if evidence.is_partial
            else "شاهد با برچسب کامل دریافت شد. "
        )
        freshness = (
            f"{stale_count} سنجه قدیمی است و وضعیت فعلی آن نامعلوم است. "
            if stale_count
            else "سنجهٔ قدیمی علامت‌گذاری نشده است. "
        )
        return (
            "پاسخ کامل و قابل‌اتکایی به پرسش شما تولید نشد. "
            f"دادهٔ ثبت‌شدهٔ Zabbix در {_timestamp(evidence.collected_at)} "
            f"شامل {len(evidence.active_problems)} مشکل فعال و {len(evidence.metrics)} سنجه است. "
            f"{qualification}{freshness}از این نمای ثبت‌شده نمی‌توان علت ریشه‌ای، بازیابی یا انجام‌شدن "
            "هیچ تغییری را نتیجه گرفت. برای پاسخ به پرسش اصلی، جزئیات بخش شواهد را بررسی کنید."
        )
    qualification = (
        f"Evidence is partial ({partial}). "
        if evidence.is_partial
        else "Evidence is marked complete. "
    )
    freshness = (
        f"{stale_count} metric(s) are stale and their current state is unknown. "
        if stale_count
        else "No metric is marked stale. "
    )
    return (
        "A complete, reliable answer to your question was not produced. "
        f"The observed Zabbix snapshot collected at {_timestamp(evidence.collected_at)} contains "
        f"{len(evidence.active_problems)} active problem(s) and {len(evidence.metrics)} metric(s). "
        f"{qualification}{freshness}This snapshot does not establish a root cause, recovery, or "
        "any performed change. Review the attributable details in the evidence panel."
    )


def _incident_fallback(locale: str, evidence: IncidentEvidence) -> str:
    zabbix = evidence.zabbix
    linux = evidence.linux
    stale_count = sum(metric.stale for metric in zabbix.summary.metrics)
    partial = ", ".join(evidence.partial_reasons)
    service_states = "; ".join(
        f"{service.unit}={service.active_state}/{service.sub_state}" for service in linux.services
    ) or (
        "no bounded service records"
        if locale == "en"
        else "رکورد محدودشده‌ای برای سرویس‌ها دریافت نشد"
    )
    if locale == "fa":
        qualifier = (
            f"شاهد ناقص است ({partial}). "
            if evidence.is_partial
            else "شاهد با برچسب کامل دریافت شد. "
        )
        stale = (
            f"{stale_count} سنجهٔ Zabbix قدیمی است و وضعیت فعلی آن نامعلوم است. "
            if stale_count
            else "سنجهٔ قدیمی Zabbix علامت‌گذاری نشده است. "
        )
        return (
            "پاسخ کامل و قابل‌اتکایی به پرسش شما تولید نشد. "
            f"دادهٔ ثبت‌شده برای هدف {evidence.target_id}: نمای زبیکس در "
            f"{_timestamp(zabbix.collected_at)} شامل {len(zabbix.events)} رخداد و "
            f"{len(zabbix.summary.active_problems)} مشکل فعال است. نمای لینوکس در "
            f"{_timestamp(linux.collected_at)} بارهای {linux.load_1m:.2f}/{linux.load_5m:.2f}/"
            f"{linux.load_15m:.2f} و وضعیت سرویس‌های «{service_states}» را ثبت کرده است. "
            f"{qualifier}{stale}این داده‌ها علت ریشه‌ای، بازیابی یا اجرای تغییر را اثبات نمی‌کنند."
        )
    qualifier = (
        f"Evidence is partial ({partial}). "
        if evidence.is_partial
        else "Evidence is marked complete. "
    )
    stale = (
        f"{stale_count} Zabbix metric(s) are stale and their current state is unknown. "
        if stale_count
        else "No Zabbix metric is marked stale. "
    )
    return (
        "A complete, reliable answer to your question was not produced. "
        f"The observed snapshot for target {evidence.target_id}: Zabbix at "
        f"{_timestamp(zabbix.collected_at)} contains {len(zabbix.events)} event(s) and "
        f"{len(zabbix.summary.active_problems)} active problem(s). The Linux snapshot at "
        f"{_timestamp(linux.collected_at)} records load {linux.load_1m:.2f}/{linux.load_5m:.2f}/"
        f"{linux.load_15m:.2f} and service states {service_states}. "
        f"{qualifier}{stale}These observations do not prove a root cause, recovery, or "
        "executed change."
    )


def _timestamp(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")
