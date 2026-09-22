# Changelog / تاریخچهٔ تغییرات

## 2026-09-21 — Bilingual project status brief / گزارش دوزبانهٔ وضعیت پروژه

### English

Added paired presentation-ready English and native-Persian status briefs plus an editable bilingual
Word document. The brief distinguishes verified repository work, four-server qualification,
role-package preparation, and bounded local CPU model smoke evidence from the production service,
Zabbix, connector, recovery, and Internet-blocked acceptance gates that remain open.

Updated the README, documentation indexes, development and testing summaries, project state, and
next-task record to remove older statements that predated the authorized server preparation and AI
smoke test. No server, package, service, database, network, credential, model, or runtime state was
changed by this documentation update.

Revised the Persian brief and the Persian half of the Word document as native executive prose.
Translation-heavy wording and unnecessary English operational terms were replaced with consistent
formal Persian while product names, code identifiers, measured results, and acceptance boundaries
were preserved.

### فارسی

گزارش‌های متناظر و آمادهٔ ارائه به فارسی طبیعی و انگلیسی، همراه یک فایل Word دوزبانه و قابل‌ویرایش
افزوده شدند. گزارش، کار تأییدشدهٔ مخزن، صلاحیت‌سنجی چهار سرور، آماده‌سازی packageهای هر نقش و
smoke test محدود مدل محلی روی CPU را از سرویس تولید، Zabbix، connector، بازیابی و پذیرش با اینترنت
قطع‌شده که هنوز باقی مانده‌اند، جدا می‌کند.

README، فهرست‌های مستندات، خلاصه‌های توسعه و آزمون، وضعیت پروژه و رکورد کار بعدی نیز اصلاح شدند تا
عبارت‌های قدیمیِ پیش از آماده‌سازی مجاز سرورها و smoke test مدل حذف شوند. این تغییر مستندات هیچ
سرور، package، سرویس، پایگاه، شبکه، credential، مدل یا وضعیت runtime را تغییر نداد.

متن گزارش فارسی و بخش فارسی فایل Word نیز از نو و با نثر رسمیِ مناسب ارائهٔ مدیریتی ویرایش شد.
عبارت‌های ترجمه‌وار و واژه‌های انگلیسیِ غیرضروری با معادل‌های یکدست فارسی جایگزین شدند؛ در عین حال،
نام محصولات، شناسه‌های فنی، نتایج اندازه‌گیری‌شده و مرز میان آزمون مقدماتی و پذیرش عملیاتی بدون
تغییر باقی ماندند.

## 2026-09-21 — Durable repository context / حافظهٔ ماندگار مخزن

### English

Added three repository-scoped Codex skills for general NextOps context, authorized server operations,
and bilingual documentation. Added a task-routing index that catalogs every project-owned Markdown
file without loading all documents into every task. Updated `AGENTS.md` and contributing guidance to
use Git and maintained artifacts as durable memory.

The documentation validator now excludes dependency/build trees and requires complete catalog
coverage. Three focused tests verify project Markdown discovery plus missing and stale entries. No
application behavior, package, VM, network, model, database, or service was changed.

### فارسی

سه skill مخصوص مخزن برای context عمومی NextOps، عملیات مجاز سرور و مستندات دوزبانه افزوده شد.
فهرست مسیردهی تازه، همهٔ فایل‌های Markdown متعلق به پروژه را ثبت می‌کند، بدون اینکه هر بار همهٔ
سندها وارد context شوند. `AGENTS.md` و راهنمای مشارکت نیز Git و artifact نگه‌داری‌شده را حافظهٔ
ماندگار پروژه می‌دانند.

اعتبارسنج مستندات اکنون پوشه‌های وابستگی و build را حذف و پوشش کامل catalog را الزامی می‌کند. سه
آزمون متمرکز discovery و ورودی غایب یا قدیمی را می‌سنجند. رفتار برنامه، package، VM، شبکه، مدل،
پایگاه یا سرویس تغییر نکرد.

## 2026-09-20 — Phase 0 report and threat model / گزارش مرحلهٔ صفر و مدل تهدید

### English

Added paired English/Persian Phase 0 architecture, gap and readiness reports plus a repository-grounded threat model. Recorded the verified local repository state, owner-confirmed single-organization/small-start/dedicated-Zabbix context, four-VM proposal, trust and data boundaries, CPU benchmark plan, resource/storage gates, all-connector roadmap, offline/recovery tests, blockers and the smallest denial-first Stage 1A slice. Updated project state, next task, indexes and traceability without marking architecture accepted or implementation complete.

Aligned stale offline wording so the first read-only Zabbix answer is a Phase 1 outcome and Linux enrichment follows in Phase 2. Updated current clone commands to `Omid-NextAI/nextops`; preserved historical provenance that names the earlier repository. No infrastructure, model, package, network, Zabbix, ESXi or storage change was performed.

### فارسی

گزارش متناظر فارسی و انگلیسی مرحلهٔ صفر دربارهٔ معماری، فاصله‌ها و آمادگی و نیز مدل تهدید مبتنی بر مخزن افزوده شد. وضعیت واقعی مخزن، فرض‌های تأییدشدهٔ تک‌سازمانی و شروع کوچک و Zabbix مستقل، چیدمان چهارماشینی، مرز اعتماد و داده، برنامهٔ سنجش CPU، کنترل منابع و دیسک، نقشهٔ همهٔ اتصال‌ها، آزمون آفلاین و بازیابی، موانع و کوچک‌ترین برش 1A با رد پیش‌فرض ثبت شدند. وضعیت پروژه، کار بعدی، فهرست‌ها و ردیابی بدون ادعای پذیرش معماری یا تکمیل پیاده‌سازی به‌روز شدند.

عبارت قدیمی راهنمای آفلاین اصلاح شد تا پاسخ فقط‌خواندنی نخست Zabbix خروجی مرحلهٔ یک و بررسی مستقیم Linux در مرحلهٔ دو باشد. فرمان‌های clone جاری به `Omid-NextAI/nextops` تغییر کردند و سابقهٔ تاریخی نام پیشین حفظ شد. هیچ زیرساخت، مدل، بسته، شبکه، Zabbix، ESXi یا دیسکی تغییر نکرد.

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
