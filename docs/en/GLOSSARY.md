# Product terminology

[فارسی](../fa/GLOSSARY.md) · [Index](INDEX.md)

Use consistent language without changing machine identifiers. This glossary is editorial guidance derived from the supplied specification, not a new protocol standard.

| English | Preferred Persian | Meaning in NextOps |
|---|---|---|
| Incident | رخداد | An operational problem being investigated |
| Event | رویداد | An observed occurrence from a source system |
| Alert | هشدار | A monitoring notification |
| Evidence | شواهد | Attributed observations supporting analysis |
| Audit log | سابقهٔ ممیزی | Security record of decisions, access and effects |
| Connector | اتصال‌دهنده | Adapter for an authorized infrastructure family |
| Execution gateway | درگاه اجرا | Protected routing and enforcement boundary |
| Durable workflow | گردش‌کار ماندگار | Progress survives process restart |
| Policy | سیاست اجرایی | Trusted deterministic authorization rules |
| Approval | تأیید عملیات | Consent bound to an exact action and state |
| Read-only | فقط‌خواندنی | No intended mutation; still scoped and bounded |
| Root cause analysis | تحلیل علت ریشه‌ای | Evidence-based investigation, not certainty by default |
| Hypothesis | فرضیه | Possible explanation not yet verified |
| Topology | توپولوژی؛ ساختار ارتباطات | Asset/service dependency relationships |
| Inference | اجرای مدل | Producing model output from input |
| Embedding | بردارسازی | Representing content as model-generated vectors |
| Reranking | بازرتبه‌بندی | Reordering retrieved candidates |
| Backpressure | کنترل پذیرش متناسب با ظرفیت | Limit incoming work when resources are saturated |
| Runbook | دستورالعمل عملیاتی | Reviewed named diagnostic or remediation procedure |
| Unknown outcome | نتیجهٔ نامشخص | Remote action may have executed; reconciliation required |
| Rollback | بازگردانی | Authorized restoration to a prior compatible state |
| RPO | هدف نقطهٔ بازیابی | Target tolerance for data loss in recovery |
| RTO | هدف زمان بازیابی | Target restoration time, measured in a drill |

Status labels: `planned` = برنامه‌ریزی‌شده; `simulated` = شبیه‌سازی‌شده; `lab-verified` = تأییدشده در آزمایشگاه; `production-validated` = اعتبارسنجی‌شده در بهره‌برداری. Do not collapse them into “supported.”

Keep code, API fields, CLI commands, IPs, interface names and IDs in their original form. Explain an English error naturally in Persian alongside the sanitized original, rather than rewriting its technical content.
