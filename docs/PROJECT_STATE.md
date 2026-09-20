# Project state / وضعیت پروژه

Updated: 2026-09-20 — startup order and Phase 1 work packages. This is a documentation baseline, not a deployment report.

## English

### Requirements and repository history

The connected owner is `AmirMo10`. The previously empty public `AmirMo10/nextops` repository was populated with English/native-Persian documentation. Visibility remains unchanged. Subsequent owner clarifications require local CPU-only AI, new answers and startup without Internet, Zabbix status as the first useful delivery, per-phase VM planning, and now an explicit starting order. The archived master prompt remains unchanged; original scope is retained through 51-section traceability and proposed ADRs.

The first accepted deliverable remains **a real authorized Zabbix status answer generated locally with Internet blocked**, with source times, scope and audit. Linux enrichment is Phase 2. No software phase has been completed or approved as production-ready through these documentation changes.

### Supplied hardware versus unknown capacity

[HARDWARE_BASELINE.json](requirements/HARDWARE_BASELINE.json) retains the owner's ESXCLI evidence: 4 CPU packages, 112 physical cores, 224 logical threads, hyperthreading active/enabled/supported, 4 NUMA nodes and 1,442,743,631,872 bytes RAM. Calculated memory is 1,343.6597 GiB / 1.3121677 TiB / 1.4427436 decimal TB. ESXi is 8.0.3, build 24414501, Update 3, raw Patch 55. The partial CPU sample covers CPU 0 completely and CPU 1 partly: family/model/stepping 6/85/7, GenuineIntel, package/node 0/0, reported 2,693,671,674 Hz, CPU 0 L2/L3 1 MiB/38.5 MiB and microcode 0x5003707.

The [ESXi supplement](en/ESXI_BASELINE.md) separately records the official build mapping to Update 3c (2024-12-12) and CPU tuple mapping to CLX-SP B1 / Xeon Scalable Gen2. These do not confirm an exact marketing SKU, rated base/turbo frequency or all-package identity. The 28-core and 335.9149-GiB per-node figures are arithmetic averages, not measured distribution or free capacity. Preserve ESXi; Ubuntu is the proposed guest. Do not repeat requests for supplied totals/build. No direct assistant host inspection, GPU inventory or memory-health test occurred.

Still unresolved: free CPU/memory, existing workload/reservations, per-node mapping, exact CPU SKU/all-package consistency, guest ISA, VM hardware level, license/VM limits, vCenter availability, storage capacity/latency, workload scale, Zabbix endpoint/version/permissions and self-monitoring items. These are tracked prerequisites, not invented facts.

### Delivered documentation and current plan

The repository contains bilingual READMEs and paired guides for architecture, security, CPU inference, configuration, MCP and all eleven integrations, data/API/UI, development, testing, operations, troubleshooting, roadmap, glossary, diagrams, technology choices, offline operation, server planning, ESXi baseline and now [START_HERE](en/START_HERE.md). Existing diagrams, source records, master prompt, review templates, agent/contributor/security rules and documentation tooling are preserved. Technology choices are proposals, not installed/locked dependencies. Prior [visual review](VISUAL_REVIEW.md) limitations still apply.

The current VM proposal is unchanged:

| Role | First phase | vCPU | RAM GiB | Disk GiB |
|---|---|---:|---:|---:|
| nextops-app | 1 | 8 | 32 | 200 |
| nextops-ai | 1 | 24 | 128 | 500 |
| nextops-connectors-ro | 1 | 4 | 8 | 80 |
| nextops-db | 3, recommended | 8 | 64 | 300 |
| nextops-executor-rw | 7, only if enabled | 4 | 16 | 80 |

Totals for 3/4/5 VMs remain 36/44/48 vCPU, 168/232/248 GiB RAM and 780/1,080/1,160 GiB disk. These are not reservations, proven NUMA placement or capacity guarantees. Existing Zabbix, an optional lab VM, temporary tests, optional dedicated observability and independent backups are separate. The startup update corrects NEXT_TASK's stale initial 44-vCPU figure to 36.

Create the initial VMs in the order **app → AI → read-only connectors**, after preflight and provisioning approval. PostgreSQL is initially an isolated service in the app VM, not a fourth VM. The [roadmap](en/ROADMAP.md) now defines:

| Stage | Planned outcome | Actual status |
|---|---|---|
| 0 | Close remaining prerequisites and approve the plan | Documentation prepared; host/access/capacity checks and approval not established |
| 1A | App/local identity/database/audit/policy foundation | Not started; tests not run |
| 1B | Local CPU model with offline loading and new bilingual answers | Not started; tests not run |
| 1C | Real scoped read-only Zabbix evidence | Not started; tests not run |
| 1D | Evidence-linked local Zabbix answer | Not started; tests not run |
| 1E | Offline, restart, security and failure acceptance | Not started; tests not run |

The [offline contract](en/OFFLINE_RUNTIME.md) still governs local model knowledge, local documents and live LAN evidence. OFF-01–OFF-10 and ZBX-01–ZBX-08 are all NOT RUN; applicable cases may not be silently skipped. Startup order, readiness checks and local Q&A during connector failure are documented in START_HERE. A running VM/model or a cached demonstration does not complete Phase 1.

### Limits, validation and next step

No API, frontend, database schema, connector, simulator, production model, benchmark harness, installer, Compose deployment or systemd service was implemented here. No VM was provisioned, host setting changed, patch installed, Zabbix queried, model run, or offline/restart/restore/load test executed. No vulnerability audit or compatibility certification was performed. GitHub Actions, branch protection, required reviews and private vulnerability reporting are not asserted to be configured; no software license has been selected.

This change is limited to documentation. The editing environment could not clone GitHub because its direct GitHub hostname resolution failed; repository reads/writes use the connected GitHub API instead. Do not claim a local clone-based documentation test, application test or browser-rendering test passed. Review the commit diff and published file content separately from runtime readiness.

Next: follow [NEXT_TASK](NEXT_TASK.md) and [START_HERE](en/START_HERE.md), resolve only remaining actionable preflight gaps, and obtain the required authorizations. Define latency/quality goals, verify offline artifacts and local key/certificate recovery, review VM topology and a supported host patch/firmware baseline, and identify an independent backup destination. Host/network changes, production access, installs, stress tests and reboots require separate approval. Record one actual next stage after each increment; do not promise background continuation.

## فارسی

### نیازها و پیشینهٔ مخزن

مالک متصل `AmirMo10` است. مخزن عمومی و قبلاً خالی `AmirMo10/nextops` با مستندات انگلیسی و فارسی تکمیل شد؛ وضعیت عمومی تغییر نکرده است. توضیحات بعدی مالک، اجرای صرفاً محلی روی CPU، پاسخ تازه و شروع بدون اینترنت، پاسخ وضعیت Zabbix در اولین تحویل، برنامهٔ ماشین‌های هر مرحله و اکنون ترتیب روشن آغاز کار را الزامی کرده‌اند. پرامپت بایگانی‌شده تغییر نکرده و دامنهٔ اولیه با ردیابی ۵۱ بخش و سوابق تصمیم پیشنهادی حفظ شده است.

اولین خروجی پذیرفته‌شده همچنان **پاسخ واقعی دربارهٔ Zabbix مجاز، تولیدشده روی CPU محلی و با اینترنت قطع** است؛ همراه زمان، دامنه و ممیزی. بررسی تکمیلی Linux در مرحلهٔ دو است. هیچ مرحلهٔ نرم‌افزاری از طریق این تغییر مستندات تکمیل یا آمادهٔ بهره‌برداری اعلام نشده است.

### سخت‌افزار ارسالی و ظرفیت نامشخص

[رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) شواهد ESXCLI مالک را نگه می‌دارد: چهار بستهٔ CPU، تعداد ۱۱۲ هستهٔ فیزیکی و ۲۲۴ رشتهٔ منطقی، Hyperthreading فعال و روشن و پشتیبانی‌شده، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت. تبدیل حافظه برابر ۱٬۳۴۳٫۶۵۹۷ GiB، یا ۱٫۳۱۲۱۶۷۷ TiB، یا ۱٫۴۴۲۷۴۳۶ TB ده‌دهی است. ESXi برابر 8.0.3، ساخت 24414501، Update 3 و مقدار خام Patch 55 است. نمونهٔ ناقص CPU، رکورد صفر را کامل و رکورد یک را ناقص پوشش می‌دهد: خانواده و مدل و بازنگری 6/85/7، سازندهٔ GenuineIntel، بسته و گرهٔ صفر، سرعت گزارش‌شدهٔ ۲٬۶۹۳٬۶۷۱٬۶۷۴ هرتز، L2 و L3 برابر ۱ و ۳۸٫۵ MiB و میکروکد 0x5003707 در CPU 0.

[یادداشت ESXi](fa/ESXI_BASELINE.md) نگاشت مستقل و رسمیِ build به Update 3c با تاریخ ۱۲ دسامبر ۲۰۲۴ و شناسهٔ CPU به CLX-SP B1 / Xeon Scalable Gen2 را ثبت می‌کند. این‌ها مدل تجاری دقیق، فرکانس اسمی پایه و توربو یا هویت همهٔ بسته‌ها را ثابت نمی‌کنند. اعداد ۲۸ هسته و ۳۳۵٫۹۱۴۹ GiB در هر گره، میانگین‌اند؛ نه توزیع یا ظرفیت آزاد سنجیده. ESXi حفظ و Ubuntu مهمان پیشنهادی باشد. مجموع‌ها و build دوباره درخواست نشوند. اتصال مستقیم دستیار، فهرست GPU یا آزمون سلامت حافظه انجام نشده است.

CPU و حافظهٔ آزاد، بار و رزرو موجود، نگاشت گره‌ها، مدل دقیق و یکسان بودن بسته‌ها، ISA مهمان، سطح سخت‌افزار VM، مجوز و محدودیت‌ها، وجود vCenter، ظرفیت و تأخیر دیسک، بار هدف، نشانی و نسخه و مجوز Zabbix و شاخص‌های خودپایشی همچنان باید روشن شوند. این موارد پیش‌نیاز پیگیری‌شده‌اند، نه واقعیت فرضی.

### مستندات تحویل‌شده و برنامهٔ فعلی

READMEهای دوزبانه و راهنماهای متناظر معماری، امنیت، CPU، تنظیمات، MCP و یازده اتصال، داده و API و رابط، توسعه، آزمون، عملیات، عیب‌یابی، نقشهٔ راه، واژه‌نامه، نمودار، فناوری، آفلاین، سرورها، ESXi و اکنون [شروع کار](fa/START_HERE.md) موجودند. نمودارها، منابع، پرامپت، قالب بازبینی، قواعد عامل و مشارکت و امنیت و ابزار مستندات حفظ شده‌اند. فناوری‌ها پیشنهادند، نه وابستگی نصب‌شده یا تثبیت‌شده. محدودیت‌های [بازبینی تصویری](VISUAL_REVIEW.md) همچنان برقرارند.

منابع پیشنهادی تغییر نکرده‌اند: ماشین برنامه ۸ vCPU، حافظهٔ ۳۲ GiB و دیسک ۲۰۰ GiB؛ ماشین AI برابر ۲۴، ۱۲۸ و ۵۰۰؛ اتصال فقط‌خواندنی برابر ۴، ۸ و ۸۰. پایگاه مستقل از مرحلهٔ سه، در صورت پذیرش پیشنهاد، ۸، ۶۴ و ۳۰۰؛ ماشین اجرای تغییر فقط در مرحلهٔ هفت و هنگام فعال شدن آن، ۴، ۱۶ و ۸۰ است.

برای سه، چهار و پنج ماشین، مجموع vCPU به‌ترتیب ۳۶، ۴۴ و ۴۸؛ حافظه ۱۶۸، ۲۳۲ و ۲۴۸ GiB؛ و دیسک ۷۸۰، ۱٬۰۸۰ و ۱٬۱۶۰ GiB است. این‌ها رزرو اعمال‌شده، جای‌گذاری اثبات‌شده یا تضمین ظرفیت نیستند. Zabbix موجود، نمونهٔ اختیاری آزمایشگاهی، آزمون موقت، پایش اختصاصی اختیاری و پشتیبان مستقل جدا حساب می‌شوند. این تغییر عدد قدیمیِ مجموع اولیهٔ ۴۴ vCPU در NEXT_TASK را به ۳۶ اصلاح می‌کند.

پس از بررسی و مجوز، ماشین‌ها به‌ترتیب **برنامه، AI و اتصال فقط‌خواندنی** ساخته شوند. PostgreSQL در ابتدا سرویس جدا و محدودشدهٔ ماشین برنامه است، نه VM چهارم. [نقشهٔ راه](fa/ROADMAP.md) اکنون گام‌های زیر را مشخص می‌کند:

| گام | خروجی برنامه‌ریزی‌شده | وضعیت واقعی |
|---|---|---|
| صفر | پیش‌نیازهای باقی‌مانده و تأیید برنامه | مستندات آماده است؛ بررسی میزبان و دسترسی و ظرفیت و تأیید احراز نشده‌اند. |
| 1A | برنامه، هویت محلی، پایگاه، ممیزی و سیاست | شروع و آزمون نشده است. |
| 1B | مدل CPU با بارگذاری آفلاین و پاسخ تازهٔ دوزبانه | شروع و آزمون نشده است. |
| 1C | شواهد واقعی، محدود و فقط‌خواندنی Zabbix | شروع و آزمون نشده است. |
| 1D | پاسخ محلی مستند دربارهٔ Zabbix | شروع و آزمون نشده است. |
| 1E | پذیرش آفلاین، شروع مجدد، امنیت و خطا | شروع و آزمون نشده است. |

[الزام آفلاین](fa/OFFLINE_RUNTIME.md) همچنان دانش مدل، سند محلی و شاهد تازهٔ داخلی را از هم جدا می‌کند. OFF-01 تا OFF-10 و ZBX-01 تا ZBX-08 همگی اجرا نشده‌اند؛ مورد لازم بی‌سروصدا کنار گذاشته نشود. ترتیب شروع، آمادگی سرویس و باقی ماندن سؤال‌وجواب محلی هنگام خرابی اتصال در راهنمای شروع آمده است. بالا بودن VM یا مدل یا نمایش کش‌شده پایان مرحلهٔ یک نیست.

### محدودیت، اعتبارسنجی و گام بعد

در این کار API، رابط، schema پایگاه، اتصال‌دهنده، شبیه‌ساز، مدل عملیاتی، ابزار سنجش، نصب‌کننده، Compose یا systemd پیاده نشده‌اند. VM ساخته نشده؛ میزبان تغییر نکرده؛ وصله نصب نشده؛ Zabbix فراخوانی و مدل اجرا نشده؛ آزمون آفلاین، شروع مجدد، بازیابی یا بار انجام نشده است. ممیزی آسیب‌پذیری و تأیید سازگاری نیز انجام نشده‌اند. تنظیم بودن Actions، حفاظت شاخه، بازبینی الزامی و گزارش خصوصی آسیب‌پذیری ادعا نمی‌شود؛ مجوز نرم‌افزاری انتخاب نشده است.

دامنهٔ تغییر فقط مستندات است. محیط ویرایش به‌دلیل شکست نام‌یابی مستقیم GitHub نتوانست clone بگیرد؛ خواندن و نوشتن از اتصال API گیت‌هاب انجام می‌شود. قبولی آزمون مستندات مبتنی بر clone محلی، آزمون برنامه یا نمایش مرورگر ادعا نشود. تفاوت commit و محتوای منتشرشده جدا از آمادگی اجرایی بررسی شوند.

گام بعد مطابق [کار بعدی](NEXT_TASK.md) و [راهنمای شروع](fa/START_HERE.md) است: فقط پیش‌نیاز مؤثر و باقی‌مانده روشن و مجوز لازم گرفته شود. هدف کیفیت و تأخیر، فایل آفلاین، بازیابی کلید و گواهی، توپولوژی VM، مبنای پشتیبانی‌شدهٔ وصله و میان‌افزار و مقصد پشتیبان مستقل مشخص شوند. تغییر میزبان و شبکه، دسترسی عملیاتی، نصب، آزمون فشار و راه‌اندازی دوباره مجوز جدا می‌خواهند. پس از هر تحویل فقط یک گام بعدِ واقعی ثبت و ادامهٔ پس‌زمینه وعده داده نشود.
