# ADR 0002 — Local CPU-only AI from the foundation

Status: accepted on 2026-09-21. Source: master sections 2–3, 9–10, 19.

## English

All AI workloads run locally on CPUs. Keep provider interfaces but disable external inference, embeddings, reranking and cloud fallback. Offline means no Internet dependency after provisioning, not denial of authorized management-LAN access.

Start evaluation with one pinned llama.cpp CPU service and a modest quantized multilingual candidate. Compare measured quality/latency before selecting model size, NUMA placement, thread counts or concurrency. Preserve the reported hardware uncertainty. Consequence: no cloud escape from poor performance; deterministic work, smaller models, budgets and benchmarking become foundational rather than late optimizations.

## فارسی

وضعیت: پذیرفته‌شده در ۲۱ سپتامبر ۲۰۲۶. همهٔ بارهای هوش مصنوعی روی CPU محلی اجرا می‌شوند. رابط ارائه‌دهنده حفظ می‌شود، اما تولید، بردارسازی، بازرتبه‌بندی و جایگزین ابری خارجی غیرفعال‌اند. آفلاین یعنی نبود وابستگی اینترنت پس از آماده‌سازی، نه قطع شبکهٔ مدیریت مجاز.

ارزیابی با یک سرویس CPU ثابت llama.cpp و مدل چندزبانهٔ کوانتیزهٔ متعادل شروع می‌شود. اندازهٔ مدل، NUMA، رشته و هم‌زمانی پس از سنجش کیفیت و تأخیر انتخاب می‌شوند. ابهام سخت‌افزار اعلام‌شده حفظ شود. پیامد: فرار از کندی به ابر وجود ندارد؛ کد قطعی، مدل کوچک‌تر، بودجه و سنجش از پایهٔ معماری‌اند، نه بهینه‌سازی آخر کار.
