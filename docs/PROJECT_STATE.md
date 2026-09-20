# Project state / وضعیت پروژه

Baseline, visual documentation, offline clarification, Zabbix-first plan and owner-supplied ESXi hardware update: 2026-09-20.

## English

### Observed requirements and repository state

The connected GitHub identity is `AmirMo10`. `AmirMo10/nextops` existed as an empty public repository before the documentation baseline. Its visibility has not been changed. The owner authorized English and native-Persian documentation except a new translation of the prompt, then diagrams and suggested technologies, mandatory offline CPU answers, and a per-phase G10 server plan.

The first implementation milestone must end with **an actual Zabbix status answer**. The [revised roadmap](en/ROADMAP.md) places Zabbix-only answers in Phase 1 and direct Linux enrichment in Phase 2. Security foundations precede real target access. The archived prompt remains unchanged. No software phase is complete.

### Hardware evidence supplied by the owner

The owner supplied results from `esxcli hardware cpu global get` and `esxcli hardware memory get`: 4 CPU packages, 112 physical cores, 224 logical threads, active/enabled/supported hyperthreading, 4 NUMA nodes and 1,442,743,631,872 bytes physical RAM. Calculated memory is 1,343.6597 GiB / 1.3121677 TiB / 1.4427436 decimal TB. The sanitized [hardware record](requirements/HARDWARE_BASELINE.json) distinguishes reported values, calculations, unknowns and proposals.

This replaces the earlier ambiguous 90-CPU / 1-TB estimate. ESXi is now the reported host platform; retain it and treat Ubuntu as the proposed VM guest OS. The output was supplied by the owner, not collected through a direct assistant host connection. The 28-core and 335.9149-GiB per-node figures are arithmetic averages, not verified distributions or free capacity. No CPU model, ESXi build, GPU inventory, memory health or measured inference result is inferred from these totals.

### Delivered documentation

English/Persian READMEs and 20 paired guides cover architecture, CPU inference, security, configuration, MCP, all eleven integration families, data/API/UI, development, testing, operations, troubleshooting, roadmap, glossary, diagrams, technology choices, offline operation and [G10 server planning](en/SERVER_PLAN.md). The repository retains 51-section traceability, proposed ADRs, agent/contributor/security rules, review templates and a local documentation checker.

The visual baseline contains seven Mermaid architecture views per language and one overview per README. Its [visual review](VISUAL_REVIEW.md) records structural versus unperformed rendering/runtime checks. Suggested packages remain proposals, not installed dependencies or compatibility locks. The diagrams are preserved by this hardware update.

The [offline contract](en/OFFLINE_RUNTIME.md) requires new local answers, cold start/reboot and fresh local login without Internet. It distinguishes model knowledge, local documents and fresh LAN evidence; inventories hidden runtime dependencies; and defines OFF-01–OFF-10, all NOT RUN.

The server plan still proposes three initial NextOps VMs, four after recommended database separation and five with an isolated change executor. Existing Zabbix, optional lab/observability/test VMs and independent backup destinations are counted separately. The AI VM's proposed baseline is now **24 vCPU / 128 GiB RAM**, replacing 32 vCPU for an initial topology-aware trial. Total proposals are **36 vCPU / 168 GiB RAM**, **44 / 232**, and **48 / 248** for the three-, four- and five-VM profiles. Disk totals remain 780, 1,080 and 1,160 GiB. None is a measured capacity guarantee or configured reservation.

ZBX-01–ZBX-08 define the first answer, count correctness, offline startup, failures, read-only enforcement, CPU measurements and audit; all remain NOT RUN. ZBX-07 now explicitly includes guest/host NUMA and contention evidence. The server guides, READMEs and AGENTS.md identify the latest hardware source and preserve the first milestone.

### Not implemented or verified

No API, frontend, database schema, MCP server, connector, simulator, production model, benchmark harness, installer, Compose deployment or systemd service is implemented by these documentation changes. No G10 VM was provisioned; no Zabbix endpoint, local model or host was accessed directly. Host totals are now evidenced by the supplied output, but available CPU/memory, existing VM load/reservations, per-node distribution, CPU model/ISA, ESXi build/license/VM limits and storage capacity/latency remain unresolved.

The operating envelope, Zabbix existence/version/access and monitoring-engine self-monitoring availability also remain unresolved. Application, model, browser-offline, network-blocked, restart and restore tests are unrun. Documentation and Git checks do not prove platform readiness. GitHub Actions, protected main, required reviews and private vulnerability reporting are not asserted to be configured. No software license has been selected.

### Next decisions and blockers

Complete [Phase 0](NEXT_TASK.md) using the supplied totals rather than asking for them again: approve architecture; obtain only the missing authorized read-only hardware/build/available-capacity observations; define asset/event volume and latency/quality goals; establish scoped Zabbix lab access; verify versions and offline artifacts; benchmark VM sizing/NUMA; map dependencies to local, approved LAN or provisioning-only; and identify key/certificate recovery and independent backups. G10 networking changes, production writes, installs, stress tests and deployment require separate authorization.

A small Phase 1 increment may begin with domain/policy contracts, but Phase 1 must end with a real read-only Zabbix-to-local-AI answer. Do not substitute scaffolding, cached answers, JSON or simulator-only results. Keep observed, supplied, calculated, proposed, tested and blocked statuses distinct.

## فارسی

### نیازها و وضعیت مشاهده‌شدهٔ مخزن

هویت متصل GitHub برابر `AmirMo10` است. مخزن `AmirMo10/nextops` پیش از پایهٔ مستندات وجود داشت و عمومی و خالی بود. وضعیت عمومی آن تغییر نکرده است. مالک مستندسازی انگلیسی و فارسی بدون ترجمهٔ تازهٔ پرامپت، سپس نمودار و فناوری پیشنهادی، پاسخ CPU آفلاین و برنامهٔ سرورهای هر مرحله را خواسته است.

پایان نخستین مرحلهٔ پیاده‌سازی باید **پاسخ واقعی دربارهٔ وضعیت Zabbix** باشد. [نقشهٔ راه](fa/ROADMAP.md) این پاسخ را در مرحلهٔ یک و بررسی مستقیم Linux را در مرحلهٔ دو قرار می‌دهد. پایهٔ امنیت پیش از دسترسی واقعی به مقصد است. پرامپت بایگانی‌شده تغییر نمی‌کند و هیچ مرحلهٔ نرم‌افزاری تکمیل نشده است.

### شواهد سخت‌افزاری ارسالی مالک

مالک خروجی `esxcli hardware cpu global get` و `esxcli hardware memory get` را فرستاده است: ۴ بستهٔ پردازنده، ۱۱۲ هستهٔ فیزیکی، ۲۲۴ رشتهٔ منطقی، Hyperthreading فعال و روشن و پشتیبانی‌شده، ۴ گرهٔ NUMA و ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت حافظهٔ فیزیکی. تبدیل محاسبه‌شده برابر ۱٬۳۴۳٫۶۵۹۷ GiB، یا ۱٫۳۱۲۱۶۷۷ TiB، یا ۱٫۴۴۲۷۴۳۶ TB ده‌دهی است. [رکورد پالایش‌شده](requirements/HARDWARE_BASELINE.json) مقدار گزارش‌شده، محاسبه، مجهول و پیشنهاد را جدا می‌کند.

این شاهد جایگزین برآورد مبهمِ ۹۰ واحد CPU و یک ترابایت است. بستر گزارش‌شده ESXi است؛ حفظ شود و Ubuntu مهمان پیشنهادی ماشین‌ها باشد. خروجی را مالک فرستاده و از اتصال مستقیم دستیار به میزبان به دست نیامده است. ۲۸ هسته و ۳۳۵٫۹۱۴۹ GiB در هر گره فقط میانگین محاسبه‌شده‌اند، نه توزیع تأییدشده یا منابع آزاد. مدل پردازنده، build، فهرست GPU، سلامت حافظه یا نتیجهٔ سنجش AI از این اعداد استنتاج نمی‌شود.

### مستندات تحویل‌شده

README فارسی و انگلیسی و ۲۰ راهنمای متناظر، معماری، CPU، امنیت، تنظیمات، MCP، یازده خانوادهٔ اتصال، داده و API و رابط، توسعه، آزمون، عملیات، عیب‌یابی، نقشهٔ راه، واژه‌نامه، نمودار، فناوری، آفلاین و [چیدمان سرورهای G10](fa/SERVER_PLAN.md) را پوشش می‌دهند. ردیابی ۵۱ بخش، تصمیم‌های پیشنهادی، قواعد عامل و مشارکت و امنیت، قالب بازبینی و ابزار محلی بررسی مستندات حفظ شده‌اند.

پایهٔ تصویری شامل هفت نمای Mermaid در هر زبان و یک نمای خلاصه در هر README است. [گزارش بازبینی](VISUAL_REVIEW.md) بررسی ساختاری را از نمایش و اجرای آزموده‌نشده جدا می‌کند. بسته‌های پیشنهادی نصب نشده‌اند و سازگاری نسخه‌های آن‌ها تثبیت نشده است. نمودارها در این به‌روزرسانی حفظ شده‌اند.

[الزام آفلاین](fa/OFFLINE_RUNTIME.md) پاسخ تازه، شروع پس از توقف یا روشن شدن دوباره و ورود تازه بدون اینترنت را می‌خواهد. دانش مدل، سند محلی و شاهد تازهٔ داخلی را جدا، وابستگی‌های پنهان را فهرست و OFF-01 تا OFF-10 را تعریف می‌کند؛ همه اجرا نشده‌اند.

تعداد ماشین‌های پیشنهادی همچنان سه در ابتدا، چهار پس از جداسازی پایگاه و پنج با اجرای تغییرِ مستقل است. Zabbix موجود، ماشین‌های اختیاری آزمایشگاه و پایش و آزمون و مقصد پشتیبان مستقل جدا شمرده می‌شوند. مبنای پیشنهادی AI اکنون **۲۴ vCPU و ۱۲۸ GiB حافظه** است؛ ۳۲ vCPU قبلی با هدف آزمایش اولیهٔ متناسب با NUMA بازنگری شده است. مجموع‌ها برای سه، چهار و پنج ماشین به‌ترتیب **۳۶ vCPU و ۱۶۸ GiB حافظه**، **۴۴ و ۲۳۲** و **۴۸ و ۲۴۸** هستند. دیسک همچنان ۷۸۰، ۱٬۰۸۰ و ۱٬۱۶۰ GiB است. هیچ‌کدام تضمین ظرفیت سنجیده یا رزرو اعمال‌شده نیستند.

ZBX-01 تا ZBX-08 پاسخ اولیه، صحت شمارش، شروع آفلاین، خطا، فقط‌خواندنی بودن، سنجش CPU و ممیزی را تعریف می‌کنند؛ همه اجرا نشده‌اند. در ZBX-07 شواهد NUMA میزبان و مهمان و رقابت بر سر منابع نیز صریح شده‌اند. راهنمای سرورها، READMEها و AGENTS.md به مبنای تازهٔ سخت‌افزار ارجاع می‌دهند و خروجی مرحلهٔ یک را حفظ می‌کنند.

### ساخته‌نشده یا بررسی‌نشده

این تغییرات مستندات، API، رابط، طرح پایگاه، سرور MCP، اتصال‌دهنده، شبیه‌ساز، مدل عملیاتی، ابزار سنجش، نصب‌کننده، Compose یا سرویس systemd پیاده‌سازی نمی‌کنند. هیچ VM ساخته نشده و اتصال مستقیم به G10، Zabbix یا مدل برقرار نشده است. مجموع‌های میزبان اکنون شاهد ارسالی دارند؛ اما CPU و حافظهٔ آزاد، بار و رزرو ماشین‌های موجود، توزیع گره‌ها، مدل و ISA، نسخه و مجوز ESXi و محدودیت هر VM و ظرفیت و تأخیر ذخیره‌سازی نامعلوم‌اند.

بار هدف، وجود و نسخه و دسترسی Zabbix و شاخص‌های خودپایشی آن نیز روشن نیستند. آزمون برنامه، مدل، مرورگر آفلاین، قطع شبکه، راه‌اندازی دوباره و بازیابی اجرا نشده است. مستندات و بررسی Git آمادگی محصول را ثابت نمی‌کنند. تنظیم بودن Actions، حفاظت main، بازبینی الزامی و گزارش خصوصی آسیب‌پذیری ادعا نمی‌شود. مجوز نرم‌افزاری انتخاب نشده است.

### تصمیم‌ها و موانع بعدی

[مرحلهٔ صفر](NEXT_TASK.md) بر اساس مشخصات ارسالی تکمیل شود و مجموع‌های موجود دوباره خواسته نشوند: تأیید معماری، دریافت فقط مشاهدات مجاز و فقط‌خواندنیِ باقی‌مانده دربارهٔ سخت‌افزار و نسخه و منابع آزاد، حجم تجهیز و رویداد و هدف تأخیر و کیفیت، دسترسی محدود Zabbix آزمایشگاهی، نسخه و فایل آفلاین، سنجش اندازهٔ VM و NUMA، دسته‌بندی وابستگی‌ها و بازیابی کلید و گواهی و پشتیبان مستقل. تغییر شبکه، نوشتن عملیاتی، نصب، آزمون فشار و استقرار مجوز جدا می‌خواهند.

گام کوچک مرحلهٔ یک می‌تواند قرارداد دامنه و سیاست باشد؛ پایان همان مرحله باید پاسخ واقعی مبتنی بر Zabbix فقط‌خواندنی و مدل محلی باشد. اسکلت، پاسخ کش‌شده، JSON و شبیه‌ساز به‌تنهایی کافی نیستند. وضعیت مشاهده‌شده، ارسالی، محاسبه‌شده، پیشنهادی، آزموده‌شده و مسدود از هم جدا بماند.
