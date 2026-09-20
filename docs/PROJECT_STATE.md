# Project state / وضعیت پروژه

Baseline: 2026-09-20. Visual documentation update: 2026-09-20.

## English

### Observed

The connected GitHub identity is `AmirMo10`. `AmirMo10/nextops` existed as an empty public repository with default branch `main` before this documentation work. Its visibility has not been changed. The owner authorized documenting the project in English and native Persian, except a new translation of the master prompt, and subsequently requested diagrams and suggested technology stacks.

### Delivered scope

English/Persian READMEs and 18 paired guides; architecture, CPU-only inference, security, configuration, MCP, eleven integration families, data/API/UI, development, testing, operations, troubleshooting and roadmap; glossary; original-requirement traceability; proposed ADRs; agent/contributor/security rules; review templates; and a local documentation checker. The source prompt is preserved as a single document with its existing Persian appendix, not a newly translated duplicate.

The visual update adds seven Mermaid architecture views in each language, a compact overview in each README, and paired technology-stack guides with core/optional choices, an RTL-aware frontend proposal, CPU-only model evaluation, alternatives and official references. Documentation indexes link the new guides. The [visual review record](VISUAL_REVIEW.md) distinguishes local structural checks from unperformed Mermaid rendering and runtime tests. These are proposals, not installed dependencies or approved architecture changes.

### Not delivered or verified

No API, frontend, database schema, MCP server, connector, simulator, production model, benchmark harness, installer, Compose deployment or systemd service is implemented. No authenticated G10 access or real-device test was available for this task. Reported 90 CPU units / 1 TB RAM / sufficient storage remain owner-provided, not measured. CPU topology, OS, ISA, free resources and workload envelope are unresolved.

Application tests and benchmarks are unrun. Documentation-structure checks are separate and do not prove technical correctness or platform readiness. GitHub Actions, protected main, required reviews and private vulnerability reporting are not asserted to be configured. No software license has been selected.

### Pending decisions and blockers

Architecture/roadmap approval; authorized host discovery; actual operating envelope and latency goals; approved lab targets and permission scopes; pinned runtime/dependency/model versions; off-host backup destination and measured recovery objectives; release access and review configuration. No production writes or host changes are authorized by the documentation request.

Next: [Phase 0](NEXT_TASK.md). Update this record only with observed evidence, and never promote planned/simulated features to production status without the relevant tests.

## فارسی

### مشاهده‌شده

هویت متصل GitHub برابر `AmirMo10` است. مخزن `AmirMo10/nextops` پیش از این کار وجود داشت، عمومی و خالی بود و شاخهٔ پیش‌فرض آن `main` بود. وضعیت عمومی تغییر نکرده است. مالک مستندسازی انگلیسی و فارسی طبیعی را خواسته و پرامپت را از ترجمهٔ تازه مستثنا کرده است. سپس افزودن نمودار و پیشنهاد فناوری‌ها را درخواست کرده است.

### دامنهٔ تحویل

README دوزبانه و ۱۸ راهنمای متناظر؛ معماری، اجرای CPU-only، امنیت، تنظیمات، MCP، یازده خانوادهٔ اتصال، داده و API و رابط، توسعه، آزمون، عملیات، عیب‌یابی و نقشهٔ راه؛ واژه‌نامه؛ ردیابی نیازهای اولیه؛ تصمیم‌های معماری پیشنهادی؛ قواعد عامل و مشارکت و امنیت؛ قالب بازبینی و ابزار بررسی مستندات. پرامپت منبع در یک فایل و با پیوست فارسی موجود حفظ می‌شود و نسخهٔ ترجمه‌شدهٔ جدیدی ندارد.

در به‌روزرسانی تصویری، هفت نمای معماری Mermaid در هر زبان، نمودار خلاصه در هر README و راهنمای متناظر فناوری‌ها اضافه شده‌اند. ابزارهای اصلی و اختیاری، پیشنهاد رابط سازگار با RTL، ارزیابی مدل CPU، گزینه‌های جایگزین و منابع رسمی مشخص شده‌اند. فهرست‌ها به راهنماهای جدید پیوند دارند. [گزارش بازبینی](VISUAL_REVIEW.md) کنترل ساختاری محلی را از نمایش Mermaid و آزمون اجراییِ انجام‌نشده جدا می‌کند. این موارد پیشنهادند، نه وابستگی نصب‌شده یا تغییر معماریِ تأییدشده.

### تحویل‌نشده یا بررسی‌نشده

API، رابط، schema پایگاه، سرور MCP، اتصال‌دهنده، شبیه‌ساز، مدل عملیاتی، ابزار سنجش کارایی، نصب‌کننده، استقرار Compose و سرویس systemd ساخته نشده‌اند. برای این کار دسترسی معتبر G10 یا آزمون تجهیز واقعی وجود نداشت. حدود ۹۰ واحد CPU، یک ترابایت RAM و فضای کافی، اطلاعات اعلام‌شدهٔ مالک‌اند و اندازه‌گیری نشده‌اند. توپولوژی پردازنده، سیستم‌عامل، ISA، منابع آزاد و بار هدف نامشخص‌اند.

آزمون برنامه و کارایی اجرا نشده است. بررسی ساختار مستندات، صحت فنی یا آمادگی محصول را ثابت نمی‌کند. تنظیم بودن Actions، حفاظت main، بازبینی الزامی و گزارش خصوصی آسیب‌پذیری ادعا نمی‌شود. مجوز نرم‌افزاری انتخاب نشده است.

### تصمیم‌ها و موانع بعدی

تأیید معماری و نقشهٔ راه، شناسایی مجاز میزبان، بار و هدف تأخیر، تجهیزات آزمایشگاهی و دامنهٔ مجوز، نسخهٔ ثابت وابستگی و مدل، مقصد پشتیبان بیرونی و هدف بازیابیِ سنجیده و تنظیم بازبینی و دسترسی انتشار لازم‌اند. درخواست مستندسازی اجازهٔ تغییر عملیاتی یا میزبان نمی‌دهد.

گام بعد: [مرحلهٔ صفر](NEXT_TASK.md). این سند فقط با شاهد واقعی به‌روز شود. ویژگی برنامه‌ریزی‌شده یا شبیه‌سازی‌شده بدون آزمون لازم، عملیاتی معرفی نشود.
