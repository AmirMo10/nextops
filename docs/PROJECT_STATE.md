# Project state / وضعیت پروژه

Baseline, visual documentation, offline clarification, Zabbix-first plan and owner-supplied ESXi hardware/build updates: 2026-09-20.

## English

### Observed requirements and repository state

The connected GitHub identity is `AmirMo10`. `AmirMo10/nextops` existed as an empty public repository before the documentation baseline. Its visibility has not been changed. The owner authorized English and native-Persian documentation except a new translation of the prompt, then diagrams and suggested technologies, mandatory offline CPU answers, and a per-phase G10 server plan.

The first implementation milestone must end with **an actual Zabbix status answer**. The [revised roadmap](en/ROADMAP.md) places Zabbix-only answers in Phase 1 and direct Linux enrichment in Phase 2. Security foundations precede real target access. The archived prompt remains unchanged. No software phase is complete.

### Hardware evidence supplied by the owner

The owner supplied results from `esxcli hardware cpu global get` and `esxcli hardware memory get`: 4 CPU packages, 112 physical cores, 224 logical threads, active/enabled/supported hyperthreading, 4 NUMA nodes and 1,442,743,631,872 bytes physical RAM. Calculated memory is 1,343.6597 GiB / 1.3121677 TiB / 1.4427436 decimal TB. The sanitized [hardware record](requirements/HARDWARE_BASELINE.json) distinguishes reported values, calculations, unknowns and proposals.

The subsequent `esxcli system version get` reports **ESXi 8.0.3, build 24414501, Update 3, Patch 55**. The first 35 lines of the CPU list supply CPU 0 completely and CPU 1 partially. Sampled identifiers are family/model/stepping 6/85/7, `GenuineIntel`, package/node 0/0, reported core speed 2,693,671,674 Hz, CPU 0 L2/L3 cache 1 MiB/38.5 MiB and microcode `0x5003707`. Rated base/turbo speed and an all-package inventory are not established.

The [English](en/ESXI_BASELINE.md) and [Persian](fa/ESXI_BASELINE.md) supplements cite the independent official mappings: build 24414501 is ESXi 8.0 Update 3c, released 2024-12-12; tuple `06-55-07` matches Intel's CLX-SP B1 / Xeon Scalable Gen2 entry. These reference mappings are separate from owner-supplied facts. The exact CPU marketing SKU remains unknown. The ESXi build is no longer unknown; older discovery wording is superseded, and neither this build nor the host totals should be requested again.

These observations replace the old 90-CPU / 1-TB estimate. Preserve ESXi and treat Ubuntu as the proposed VM guest OS. The output was supplied by the owner, not collected through direct assistant host access. The 28-core and 335.9149-GiB per-node values remain arithmetic averages, not verified distributions or free capacity. No GPU inventory, memory-health result or measured inference performance is inferred.

### Delivered documentation

English/Persian READMEs and **21 paired guides** cover architecture, CPU inference, security, configuration, MCP, all eleven integration families, data/API/UI, development, testing, operations, troubleshooting, roadmap, glossary, diagrams, technology choices, offline operation, [G10 server planning](en/SERVER_PLAN.md) and the [ESXi/CPU baseline supplement](en/ESXI_BASELINE.md). The repository retains 51-section traceability, proposed ADRs, agent/contributor/security rules, review templates and a local documentation checker.

The visual baseline contains seven Mermaid architecture views per language and one overview per README. Its [visual review](VISUAL_REVIEW.md) records structural versus unperformed rendering/runtime checks. Suggested packages remain proposals, not installed dependencies or compatibility locks. Existing diagrams and the master prompt are preserved by this update.

The [offline contract](en/OFFLINE_RUNTIME.md) requires new local answers, cold start/reboot and fresh local login without Internet. It distinguishes model knowledge, local documents and fresh LAN evidence; inventories hidden runtime dependencies; and defines OFF-01–OFF-10, all NOT RUN.

The server plan still proposes three initial NextOps VMs, four after recommended database separation and five with an isolated change executor. Existing Zabbix, optional lab/observability/test VMs and independent backup destinations are separate. The AI VM proposal stays **24 vCPU / 128 GiB RAM**. Total proposals remain **36 vCPU / 168 GiB RAM**, **44 / 232**, and **48 / 248** for the three-, four- and five-VM profiles; disk totals remain 780, 1,080 and 1,160 GiB. None is a measured capacity guarantee, configured reservation or proven NUMA placement.

ZBX-01–ZBX-08 define the first answer, correct counts, offline startup, failures, read-only enforcement, CPU measurements and audit; all remain NOT RUN. ZBX-07 includes host/guest NUMA and contention evidence. The new ESXi supplement records HW20+ Automatic vTopology conditions, the standalone Host Client caveat, guest ISA verification and patch/firmware review without authorizing host changes. AGENTS.md and the documentation indexes link the new evidence.

### Not implemented or verified

No API, frontend, database schema, MCP server, connector, simulator, production model, benchmark harness, installer, Compose deployment or systemd service is implemented by these documentation changes. No G10 VM was provisioned; no Zabbix endpoint, local model or host was accessed directly. CPU/RAM totals and ESXi build now have owner-supplied evidence, but free capacity, existing VM load/reservations, per-node distribution, exact CPU SKU, all-package identity, guest ISA, VM hardware version, license/VM limits, vCenter presence and storage capacity/latency remain unresolved.

The operating envelope, Zabbix existence/version/access and self-monitoring availability remain unresolved. Application, model, browser-offline, network-blocked, restart and restore tests are unrun. No host patch, microcode update, compatibility certification or vulnerability audit was performed. Documentation and Git checks do not prove readiness. GitHub Actions, protected main, required reviews and private vulnerability reporting are not asserted to be configured. No software license has been selected.

### Next decisions and blockers

Complete [Phase 0](NEXT_TASK.md) using the supplied totals and build rather than asking again: approve architecture; obtain only missing authorized read-only CPU-description/guest/topology/free-capacity facts; define asset/event volume and latency/quality goals; establish scoped Zabbix lab access; verify compatible offline artifacts; measure VM sizing/NUMA; map dependencies to local, approved LAN or provisioning-only; identify key/certificate recovery and independent backups. Review a supported patch/firmware baseline before production. G10 network changes, patch installation, production writes, stress tests and deployment require separate authorization.

A small Phase 1 increment may begin with domain/policy contracts, but Phase 1 must end with a real read-only Zabbix-to-local-AI answer. Do not substitute scaffolding, cached answers, JSON or simulator-only results. Keep supplied, calculated, reference-mapped, proposed, tested and blocked statuses distinct.

## فارسی

### نیازها و وضعیت مشاهده‌شدهٔ مخزن

هویت متصل GitHub برابر `AmirMo10` است. مخزن `AmirMo10/nextops` پیش از پایهٔ مستندات وجود داشت و عمومی و خالی بود. وضعیت عمومی آن تغییر نکرده است. مالک مستندسازی انگلیسی و فارسی بدون ترجمهٔ تازهٔ پرامپت، سپس نمودار و فناوری پیشنهادی، پاسخ CPU آفلاین و برنامهٔ سرورهای هر مرحله را خواسته است.

پایان نخستین مرحلهٔ پیاده‌سازی باید **پاسخ واقعی دربارهٔ وضعیت Zabbix** باشد. [نقشهٔ راه](fa/ROADMAP.md) این پاسخ را در مرحلهٔ یک و بررسی مستقیم Linux را در مرحلهٔ دو قرار می‌دهد. پایهٔ امنیت پیش از دسترسی واقعی به مقصد است. پرامپت بایگانی‌شده تغییر نمی‌کند و هیچ مرحلهٔ نرم‌افزاری تکمیل نشده است.

### شواهد سخت‌افزاری ارسالی مالک

مالک خروجی `esxcli hardware cpu global get` و `esxcli hardware memory get` را فرستاده است: ۴ بستهٔ پردازنده، ۱۱۲ هستهٔ فیزیکی، ۲۲۴ رشتهٔ منطقی، Hyperthreading فعال و روشن و پشتیبانی‌شده، ۴ گرهٔ NUMA و ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت حافظهٔ فیزیکی. تبدیل محاسبه‌شده برابر ۱٬۳۴۳٫۶۵۹۷ GiB، یا ۱٫۳۱۲۱۶۷۷ TiB، یا ۱٫۴۴۲۷۴۳۶ TB ده‌دهی است. [رکورد پالایش‌شده](requirements/HARDWARE_BASELINE.json) مقدار ارسالی، محاسبه، مجهول و پیشنهاد را جدا می‌کند.

خروجی بعدیِ `esxcli system version get`، **ESXi 8.0.3، ساخت 24414501، Update 3 و Patch 55** را گزارش می‌کند. در ۳۵ خط نخست فهرست CPU، رکورد CPU 0 کامل و CPU 1 ناقص است. شناسه‌های نمونه، خانواده و مدل و بازنگری 6/85/7، سازندهٔ `GenuineIntel`، بسته و گرهٔ صفر، سرعت گزارش‌شدهٔ ۲٬۶۹۳٬۶۷۱٬۶۷۴ هرتز، حافظهٔ نهان L2 و L3 در CPU 0 برابر ۱ و ۳۸٫۵ MiB و میکروکد `0x5003707` هستند. فرکانس اسمی پایه و توربو و مشخصات همهٔ بسته‌ها از این نمونه مشخص نمی‌شوند.

یادداشت‌های [فارسی](fa/ESXI_BASELINE.md) و [انگلیسی](en/ESXI_BASELINE.md) منابع رسمیِ مستقل را معرفی می‌کنند: ساخت 24414501 متعلق به ESXi 8.0 Update 3c با تاریخ انتشار ۱۲ دسامبر ۲۰۲۴ است؛ شناسهٔ `06-55-07` با ردیف CLX-SP B1 / Xeon Scalable Gen2 در مرجع Intel مطابقت دارد. این نگاشت‌ها با دادهٔ ارسالی مالک جدا ثبت شده‌اند. نام تجاری دقیق CPU هنوز معلوم نیست. نسخهٔ ESXi دیگر مجهول نیست؛ متن قدیمی شناسایی در این مورد به‌روز شده و درخواست دوبارهٔ build یا مجموع منابع لازم نیست.

این شواهد جایگزین برآورد قدیمیِ ۹۰ واحد CPU و یک ترابایت‌اند. ESXi حفظ شود و Ubuntu مهمان پیشنهادی ماشین‌ها باشد. خروجی را مالک فرستاده و از اتصال مستقیم دستیار به میزبان به دست نیامده است. ۲۸ هسته و ۳۳۵٫۹۱۴۹ GiB در هر گره فقط میانگین‌اند، نه توزیع تأییدشده یا منابع آزاد. فهرست GPU، سلامت حافظه یا کارایی سنجیدهٔ مدل از این اطلاعات استنتاج نمی‌شود.

### مستندات تحویل‌شده

README فارسی و انگلیسی و **۲۱ راهنمای متناظر**، معماری، CPU، امنیت، تنظیمات، MCP، یازده خانوادهٔ اتصال، داده و API و رابط، توسعه، آزمون، عملیات، عیب‌یابی، نقشهٔ راه، واژه‌نامه، نمودار، فناوری، آفلاین، [چیدمان سرورهای G10](fa/SERVER_PLAN.md) و [یادداشت نسخه و پردازنده](fa/ESXI_BASELINE.md) را پوشش می‌دهند. ردیابی ۵۱ بخش، تصمیم‌های پیشنهادی، قواعد عامل و مشارکت و امنیت، قالب بازبینی و ابزار محلی بررسی مستندات حفظ شده‌اند.

پایهٔ تصویری شامل هفت نمای Mermaid در هر زبان و یک نمای خلاصه در هر README است. [گزارش بازبینی](VISUAL_REVIEW.md) بررسی ساختاری را از نمایش و اجرای آزموده‌نشده جدا می‌کند. بسته‌های پیشنهادی نصب نشده‌اند و سازگاری نسخه‌های آن‌ها تثبیت نشده است. نمودارهای موجود و پرامپت اصلی در این به‌روزرسانی حفظ شده‌اند.

[الزام آفلاین](fa/OFFLINE_RUNTIME.md) پاسخ تازه، شروع پس از توقف یا روشن شدن دوباره و ورود تازه بدون اینترنت را می‌خواهد. دانش مدل، سند محلی و شاهد تازهٔ داخلی را جدا، وابستگی‌های پنهان را فهرست و OFF-01 تا OFF-10 را تعریف می‌کند؛ همه اجرا نشده‌اند.

تعداد ماشین‌های پیشنهادی همچنان سه در ابتدا، چهار پس از جداسازی پایگاه و پنج با اجرای تغییرِ مستقل است. Zabbix موجود، ماشین‌های اختیاری آزمایشگاه و پایش و آزمون و مقصد پشتیبان مستقل جدا شمرده می‌شوند. پیشنهاد AI همان **۲۴ vCPU و ۱۲۸ GiB حافظه** است. مجموع‌ها برای سه، چهار و پنج ماشین به‌ترتیب **۳۶ vCPU و ۱۶۸ GiB حافظه**، **۴۴ و ۲۳۲** و **۴۸ و ۲۴۸** هستند. دیسک نیز ۷۸۰، ۱٬۰۸۰ و ۱٬۱۶۰ GiB باقی می‌ماند. هیچ‌کدام تضمین ظرفیت سنجیده، رزرو اعمال‌شده یا جای‌گذاری اثبات‌شدهٔ NUMA نیستند.

ZBX-01 تا ZBX-08 پاسخ اولیه، صحت شمارش، شروع آفلاین، خطا، فقط‌خواندنی بودن، سنجش CPU و ممیزی را تعریف می‌کنند؛ همه اجرا نشده‌اند. ZBX-07 شامل شواهد NUMA میزبان و مهمان و رقابت بر سر منابع است. یادداشت جدید، شرط سخت‌افزار ۲۰ به بالا برای Automatic vTopology، نکتهٔ Host Client مستقل، بررسی ISA مهمان و بازبینی وصله و میان‌افزار را ثبت می‌کند؛ نه مجوز تغییر میزبان را. AGENTS.md و فهرست‌های مستندات به شواهد تازه پیوند دارند.

### ساخته‌نشده یا بررسی‌نشده

این تغییرات مستندات، API، رابط، طرح پایگاه، سرور MCP، اتصال‌دهنده، شبیه‌ساز، مدل عملیاتی، ابزار سنجش، نصب‌کننده، Compose یا سرویس systemd پیاده‌سازی نمی‌کنند. هیچ VM ساخته نشده و اتصال مستقیم به G10، Zabbix یا مدل برقرار نشده است. مجموع منابع و نسخهٔ ESXi شاهد ارسالی دارند؛ اما منابع آزاد، بار و رزرو موجود، توزیع گره‌ها، مدل تجاری CPU، هویت همهٔ بسته‌ها، ISA مهمان، نسخهٔ سخت‌افزار VM، مجوز و محدودیت‌ها، وجود vCenter و ظرفیت و تأخیر دیسک نامعلوم‌اند.

بار هدف، وجود و نسخه و دسترسی Zabbix و شاخص‌های خودپایشی آن نیز روشن نیستند. آزمون برنامه، مدل، مرورگر آفلاین، قطع شبکه، راه‌اندازی دوباره و بازیابی اجرا نشده است. نصب وصله، تغییر میکروکد، تأیید سازگاری یا ممیزی آسیب‌پذیری انجام نشده است. مستندات و بررسی Git آمادگی محصول را ثابت نمی‌کنند. تنظیم بودن Actions، حفاظت main، بازبینی الزامی و گزارش خصوصی آسیب‌پذیری ادعا نمی‌شود. مجوز نرم‌افزاری انتخاب نشده است.

### تصمیم‌ها و موانع بعدی

[مرحلهٔ صفر](NEXT_TASK.md) بر اساس مشخصات و build ارسالی تکمیل شود، نه با درخواست دوبارهٔ آن‌ها: تأیید معماری، دریافت فقط مشاهدات مجاز و فقط‌خواندنیِ باقی‌مانده دربارهٔ شرح CPU، مهمان، گره‌ها و منابع آزاد؛ تعیین حجم و هدف تأخیر و کیفیت؛ دسترسی محدود Zabbix؛ سازگاری فایل‌های آفلاین؛ سنجش VM و NUMA؛ دسته‌بندی وابستگی‌ها و تعیین بازیابی کلید و گواهی و پشتیبان مستقل. مبنای پشتیبانی‌شدهٔ وصله و میان‌افزار پیش از بهره‌برداری بازبینی شود. تغییر شبکه، نصب وصله، نوشتن عملیاتی، آزمون فشار و استقرار مجوز جدا می‌خواهند.

گام کوچک مرحلهٔ یک می‌تواند قرارداد دامنه و سیاست باشد؛ پایان همان مرحله باید پاسخ واقعی مبتنی بر Zabbix فقط‌خواندنی و مدل محلی باشد. اسکلت، پاسخ کش‌شده، JSON و شبیه‌ساز به‌تنهایی کافی نیستند. وضعیت ارسالی، محاسبه‌شده، نگاشت‌شده با مرجع، پیشنهادی، آزموده‌شده و مسدود از هم جدا بماند.
