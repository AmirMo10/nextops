# Project state / وضعیت پروژه

Baseline, visual documentation, offline clarification and G10/Zabbix-first planning revision: 2026-09-20.

## English

### Observed requirements and repository state

The connected GitHub identity is `AmirMo10`. `AmirMo10/nextops` existed as an empty public repository before the documentation baseline. Its visibility has not been changed. The owner authorized English and native-Persian documentation except a new translation of the prompt, then diagrams and suggested technologies, mandatory offline CPU answers, and a per-phase G10 server plan.

The latest clarification requires **an actual Zabbix status answer by the end of the first implementation milestone**. The [revised roadmap](en/ROADMAP.md) moves Zabbix-only answers into Phase 1 and leaves direct Linux enrichment in Phase 2. This supersedes earlier first-answer timing without editing the archived master prompt. Security foundations still precede real target access. No software phase is complete.

### Delivered documentation

English/Persian READMEs and 20 paired guides cover architecture, CPU inference, security, configuration, MCP, all eleven integration families, data/API/UI, development, testing, operations, troubleshooting, roadmap, glossary, diagrams, technology choices, offline operation and now [G10 server planning](en/SERVER_PLAN.md). The repository also retains 51-section traceability, proposed ADRs, agent/contributor/security rules, review templates and a local documentation checker.

The visual baseline contains seven Mermaid architecture views per language and one overview per README. Its [visual review](VISUAL_REVIEW.md) records structural versus unperformed rendering/runtime checks. Suggested packages remain proposals, not installed dependencies or compatibility locks.

The [offline contract](en/OFFLINE_RUNTIME.md) requires new local answers, cold start/reboot and fresh local login without Internet. It distinguishes model knowledge, local documents and fresh LAN evidence; inventories hidden runtime dependencies; and defines OFF-01–OFF-10, all NOT RUN.

The server plan proposes one physical G10 with three initial NextOps VMs, four after recommended database separation and five when a separate change executor is enabled. Existing Zabbix, optional lab/observability/test VMs and off-host backups are counted separately. Proposed baseline totals are 44 vCPU/168 GiB RAM, 52/232 and 56/248; none is a measured capacity result. ZBX-01–ZBX-08 define the first answer, count correctness, offline startup, failure behavior, read-only enforcement, CPU measurements and audit evidence; all are NOT RUN. Updated READMEs, indexes, AGENTS.md and NEXT_TASK.md direct development toward this outcome.

### Not implemented or verified

No API, frontend, database schema, MCP server, connector, simulator, production model, benchmark harness, installer, Compose deployment or systemd service is implemented by these documentation changes. No G10 VM was provisioned and no real Zabbix endpoint was queried. No authenticated G10 access or real-device test was available. Approximately 90 CPU units, 1 TB RAM and sufficient disk remain owner-provided, not measured.

CPU topology/ISA, available resources, hypervisor/bare-metal context, workload envelope, Zabbix existence/version/access and engine self-monitoring availability remain unresolved. Application, model, browser-offline, network-blocked, restart and restore tests have not been executed. Documentation and Git checks are not proof of platform readiness. GitHub Actions, protected main, required reviews and private vulnerability reporting are not asserted to be configured. No software license has been selected.

### Next decisions and blockers

Complete [Phase 0](NEXT_TASK.md): approve architecture; obtain authorized non-destructive host discovery; define asset/event volume and latency/quality targets; establish scoped Zabbix lab access; verify versions and offline artifacts; review VM allocation and NUMA placement; map dependencies to local, approved LAN or provisioning-only; and identify key/certificate recovery and independent backup destinations. G10 network changes, production writes, installs, stress tests and deployment need separate authorization.

The smallest Phase 1 increment may begin with domain/policy contracts, but Phase 1 must end with a real read-only Zabbix-to-local-AI answer. Do not substitute scaffolding, cached answers, a JSON dump or simulator-only results. Update this record with observed evidence and retain honest planned/simulated/lab/production labels.

## فارسی

### نیازها و وضعیت مشاهده‌شدهٔ مخزن

هویت متصل GitHub برابر `AmirMo10` است. مخزن `AmirMo10/nextops` پیش از پایهٔ مستندات وجود داشت و عمومی و خالی بود. وضعیت عمومی آن تغییر نکرده است. مالک مستندسازی انگلیسی و فارسی، بدون ترجمهٔ تازهٔ پرامپت، سپس نمودار و فناوری پیشنهادی، پاسخ CPU آفلاین و برنامهٔ سرورهای هر مرحله را خواسته است.

تأکید تازه، **پاسخ واقعی دربارهٔ وضعیت Zabbix در پایان اولین مرحلهٔ پیاده‌سازی** است. [نقشهٔ راه بازنگری‌شده](fa/ROADMAP.md) پاسخ مبتنی بر Zabbix را به مرحلهٔ یک می‌آورد و بررسی مستقیم Linux را در مرحلهٔ دو نگه می‌دارد. این زمان‌بندی بر متن قدیمی مقدم است و پرامپت بایگانی‌شده تغییر نمی‌کند. پایهٔ امنیت همچنان پیش از دسترسی واقعی به مقصد قرار دارد. هیچ مرحلهٔ نرم‌افزاری تکمیل نشده است.

### مستندات تحویل‌شده

README فارسی و انگلیسی و ۲۰ راهنمای متناظر، معماری، CPU، امنیت، تنظیمات، MCP، یازده خانوادهٔ اتصال، داده و API و رابط، توسعه، آزمون، عملیات، عیب‌یابی، نقشهٔ راه، واژه‌نامه، نمودار، فناوری، آفلاین و اکنون [چیدمان سرورهای G10](fa/SERVER_PLAN.md) را پوشش می‌دهند. ردیابی ۵۱ بخش اولیه، تصمیم‌های پیشنهادی، قواعد عامل و مشارکت و امنیت، قالب بازبینی و ابزار محلی بررسی مستندات نیز حفظ شده‌اند.

پایهٔ تصویری شامل هفت نمای Mermaid در هر زبان و یک نمای خلاصه در هر README است. [گزارش بازبینی](VISUAL_REVIEW.md) بررسی ساختاری را از نمایش و اجرای آزموده‌نشده جدا می‌کند. بسته‌های پیشنهادی نصب نشده‌اند و سازگاری نسخه‌های آن‌ها تثبیت نشده است.

[الزام آفلاین](fa/OFFLINE_RUNTIME.md) پاسخ تازهٔ محلی، شروع پس از توقف یا روشن شدن دوباره و ورود تازه بدون اینترنت را می‌خواهد. دانش مدل، سند محلی و شاهد تازهٔ داخلی را جدا، وابستگی‌های پنهان را فهرست و OFF-01 تا OFF-10 را تعریف می‌کند؛ همه اجرا نشده‌اند.

برنامهٔ سرورها یک G10 فیزیکی با سه ماشین اولیهٔ NextOps، چهار ماشین پس از جداسازی پیشنهادی پایگاه و پنج ماشین در صورت فعال شدن اجرای تغییرِ جدا پیشنهاد می‌کند. Zabbix موجود، ماشین آزمایشگاهی و پایش و آزمون اختیاری و پشتیبان بیرونی جدا شمرده می‌شوند. مجموع‌های پیشنهادی به‌ترتیب ۴۴ vCPU و ۱۶۸ GiB حافظه، ۵۲ و ۲۳۲، و ۵۶ و ۲۴۸ هستند؛ هیچ‌کدام نتیجهٔ اندازه‌گیری نیست. ZBX-01 تا ZBX-08 پاسخ اولیه، صحت شمارش، شروع آفلاین، خطا، فقط‌خواندنی بودن، اندازه‌گیری CPU و ممیزی را تعریف می‌کنند؛ همه اجرا نشده‌اند. READMEها، فهرست‌ها، AGENTS.md و NEXT_TASK.md به این خروجی ارجاع می‌دهند.

### ساخته‌نشده یا بررسی‌نشده

این تغییرات مستندات، API، رابط، طرح پایگاه، سرور MCP، اتصال‌دهنده، شبیه‌ساز، مدل عملیاتی، ابزار سنجش، نصب‌کننده، Compose یا سرویس systemd پیاده‌سازی نمی‌کنند. ماشینی روی G10 ساخته نشده و Zabbix واقعی فراخوانی نشده است. دسترسی معتبر G10 و آزمون تجهیز واقعی در دسترس نبود. حدود ۹۰ واحد CPU، یک ترابایت RAM و دیسک کافی، اطلاعات مالک‌اند و سنجیده نشده‌اند.

توپولوژی و ISA پردازنده، منابع آزاد، بستر مجازی‌سازی یا نصب مستقیم، بار هدف، وجود و نسخه و دسترسی Zabbix و شاخص‌های خودپایشی آن نامشخص‌اند. آزمون برنامه، مدل، مرورگر آفلاین، قطع شبکه، راه‌اندازی دوباره و بازیابی اجرا نشده است. مستندات و بررسی Git، آمادگی محصول را ثابت نمی‌کنند. تنظیم بودن Actions، حفاظت main، بازبینی الزامی و گزارش خصوصی آسیب‌پذیری ادعا نمی‌شود. مجوز نرم‌افزاری انتخاب نشده است.

### تصمیم‌ها و موانع بعدی

[مرحلهٔ صفر](NEXT_TASK.md) تکمیل شود: تأیید معماری، شناسایی غیرمخرب و مجاز میزبان، تعیین حجم تجهیز و رویداد و هدف تأخیر و کیفیت، دسترسی محدود آزمایشگاهی Zabbix، بررسی نسخه و فایل‌های آفلاین، بازبینی منابع و NUMA، دسته‌بندی وابستگی به محلی و داخلیِ مجاز و زمان آماده‌سازی، و تعیین بازیابی کلید و گواهی و مقصد پشتیبان مستقل. تغییر شبکهٔ G10، نوشتن عملیاتی، نصب، آزمون فشار و استقرار مجوز جدا می‌خواهند.

کوچک‌ترین گام مرحلهٔ یک می‌تواند قرارداد دامنه و سیاست باشد؛ ولی پایان همان مرحله باید پاسخ واقعی مبتنی بر Zabbix فقط‌خواندنی و مدل محلی باشد. اسکلت پروژه، پاسخ کش‌شده، خروجی JSON یا شبیه‌ساز به‌تنهایی جای این خروجی را نمی‌گیرند. این سند با شواهد واقعی به‌روز و برچسب برنامه‌ریزی‌شده، شبیه‌سازی‌شده، آزمایشگاهی و عملیاتی صادقانه حفظ شود.
