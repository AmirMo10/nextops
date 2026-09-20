# Changelog / تاریخچهٔ تغییرات

## 2026-09-20 — Startup order and Phase 1A–1E / ترتیب شروع و گام‌های مرحلهٔ یک

### English

Added English/native-Persian START_HERE guides and linked them from both documentation indexes. Revised both roadmaps and NEXT_TASK to specify the first VM order: nextops-app, nextops-ai, nextops-connectors-ro. Phase 1 is now decomposed into 1A application/safety foundation, 1B local CPU model, 1C read-only Zabbix evidence, 1D evidence-linked answer and 1E offline acceptance. VM budgets remain 8/32/200, 24/128/500 and 4/8/80 (vCPU/RAM GiB/disk GiB); corrected the stale initial 44-vCPU NEXT_TASK total to 36. Optional lab Zabbix and later database/write-executor VMs are counted separately.

Clarified remaining preflight, creation versus restart order, local service readiness, credential/network boundaries, separate disposable untrusted test environments and actual completion evidence. Updated PROJECT_STATE without marking any software phase complete. Preserved the master prompt, hardware evidence, existing diagrams, repository settings and G10 configuration. This is a documentation-only change; no VM, model, Zabbix or offline acceptance test was run. Direct clone was unavailable because GitHub hostname resolution failed in the editing environment; connected API reads/writes remained available.

### فارسی

راهنمای متناظر START_HERE و پیوند آن در هر دو فهرست اضافه شد. نقشه‌های راه و NEXT_TASK ترتیب ساخت را روشن می‌کنند: ابتدا برنامه، سپس AI و بعد اتصال فقط‌خواندنی. مرحلهٔ یک به 1A پایهٔ برنامه و ایمنی، 1B مدل CPU محلی، 1C شواهد فقط‌خواندنی Zabbix، 1D پاسخ دارای منبع و 1E پذیرش آفلاین تقسیم شد. منابع ماشین‌ها همان ۸/۳۲/۲۰۰، ۲۴/۱۲۸/۵۰۰ و ۴/۸/۸۰ با واحد vCPU، حافظهٔ GiB و دیسک GiB هستند؛ مجموع قدیمی ۴۴ vCPU در NEXT_TASK به ۳۶ اصلاح شد. نمونهٔ آزمایشگاهی Zabbix و ماشین‌های پایگاه و اجرای تغییرِ مراحل بعد جدا حساب می‌شوند.

پیش‌نیازهای باقی‌مانده، تفاوت ترتیب ساخت و شروع سرویس، آمادگی محلی، مرز اطلاعات ورود و شبکه، محیط موقت جدا برای آزمون غیرقابل‌اعتماد و شواهد پایان مشخص شدند. PROJECT_STATE بدون کامل اعلام کردن مرحلهٔ نرم‌افزاری به‌روز شد. پرامپت، شاهد سخت‌افزار، نمودارها، تنظیمات مخزن و G10 حفظ شدند. تغییر فقط مستندات است؛ هیچ آزمون VM، مدل، Zabbix یا پذیرش آفلاین اجرا نشد. clone مستقیم به‌دلیل نام‌یابی GitHub در محیط ویرایش ممکن نبود؛ اتصال API برای خواندن و نوشتن موجود بود.

## 2026-09-20 — Diagrams and technology choices / نمودارها و انتخاب فناوری

### English

Added paired `DIAGRAMS.md` and `TECH_STACK.md` guides. Seven Mermaid views per language cover system context, single-host deployment zones, read-only investigation, future exact-action approvals, conceptual data relationships, CPU scheduling and release delivery. Both READMEs now include an overview diagram, a stack summary and direct navigation. Both documentation indexes and project state are updated.

The stack guide separates the existing specification from supplemental recommendations, core choices from feature-gated tools, and local CPU candidates from unmeasured performance claims. It includes official references and RTL-aware frontend guidance. The master prompt, original requirement scope, repository visibility, host configuration and application implementation remain unchanged. Local guide-structure checks and rendering limitations are recorded in `docs/VISUAL_REVIEW.md`.

### فارسی

راهنماهای متناظر `DIAGRAMS.md` و `TECH_STACK.md` اضافه شدند. هفت نمودار در هر زبان نمای سامانه، ناحیه‌های استقرار روی یک میزبان، بررسی فقط‌خواندنی، تأیید دقیق اصلاحات آینده، ارتباط مفهومی داده‌ها، زمان‌بندی CPU و مسیر انتشار را پوشش می‌دهند. هر دو README اکنون نمودار خلاصه، جدول فناوری و پیوند مستقیم دارند. فهرست‌های مستندات و وضعیت پروژه نیز به‌روز شدند.

راهنمای فناوری‌ها مبنای موجود را از پیشنهاد تکمیلی، ابزار اصلی را از گزینهٔ وابسته به نیاز و نامزد مدل CPU را از ادعای کاراییِ سنجیده‌نشده جدا می‌کند. منابع رسمی و راهنمای رابط سازگار با RTL اضافه شده‌اند. پرامپت، دامنهٔ نیازهای اولیه، وضعیت عمومی مخزن، تنظیمات میزبان و پیاده‌سازی برنامه تغییر نکرده‌اند. کنترل ساختار راهنماها و محدودیت بررسی نمایش در `docs/VISUAL_REVIEW.md` ثبت شده است.

## 2026-09-20 — Documentation baseline / پایهٔ مستندات

### English

Initialized the existing empty `AmirMo10/nextops` repository without changing its public visibility. Added English and native-Persian documentation, architecture and execution boundaries, CPU-only evaluation plan, all eleven integration contracts, data/API/UI design, phases 0–8, security/testing/recovery requirements, traceability for all 51 original sections, agent/contributor rules and review templates. Retained the supplied master prompt without a new translation. Added a local documentation-structure checker.

No application, model deployment, G10 inspection, benchmark, real-device integration or production service is delivered by this baseline. Repository settings such as branch protection, Actions and private vulnerability reporting are not asserted to be configured.

### فارسی

مخزن خالیِ موجود `AmirMo10/nextops` بدون تغییر وضعیت عمومی آن مقداردهی شد. راهنماهای انگلیسی و فارسی، معماری و مرز اجرا، برنامهٔ ارزیابی CPU-only، قرارداد یازده اتصال، طراحی داده و API و رابط، مراحل صفر تا هشت، نیازهای امنیت و آزمون و بازیابی، ردیابی ۵۱ بخش اولیه، قواعد عامل و مشارکت و قالب بازبینی اضافه شدند. پرامپت دریافت‌شده بدون ترجمهٔ جدید حفظ شد و ابزار بررسی ساختار مستندات افزوده شد.

این نسخه برنامه، مدل مستقر، بررسی سرور G10، آزمون کارایی، اتصال واقعی یا سرویس عملیاتی تحویل نمی‌دهد. تنظیم بودن حفاظت شاخه، Actions یا گزارش خصوصی آسیب‌پذیری نیز ادعا نمی‌شود.
