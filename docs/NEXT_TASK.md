# Next task / کار بعدی

Updated: 2026-09-20 — aligned with active master prompt v3.0.

## English — finish the remaining preflight, then resume the next authorized stage

Read the [active master prompt v3.0](requirements/NEXTOPS_MASTER_PROMPT.md) first, then [prompt history](requirements/PROMPT_CHANGELOG.md), [PROJECT_STATE](PROJECT_STATE.md), [START_HERE](en/START_HERE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [ESXI_BASELINE](en/ESXI_BASELINE.md), [OFFLINE_RUNTIME](en/OFFLINE_RUNTIME.md), [STORAGE_PLAN](STORAGE_PLAN.md) and [HARDWARE_BASELINE](requirements/HARDWARE_BASELINE.json). Read the complete [preserved v2 source](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) for original feature detail, applying v3's explicit revisions. The archive is immutable; the active prompt was updated at the owner's request. Preserve current repository work and inspect actual checkpoint/approval evidence before deciding where to resume.

### Already supplied; do not request again as missing

The owner supplied ESXi 8.0.3 build 24414501, four CPU packages, 112 physical cores, 224 logical threads, four NUMA nodes and 1,442,743,631,872 bytes RAM; a partial Intel CPU sample; and a point-in-time listing of three mounted VMFS-6 datastores. These are supplied observations, not directly inspected current free CPU/RAM, reservations or benchmarks. Exact CPU SKU, guest ISA and actual per-node distribution remain unresolved.

Public DS-C, the largest datastore, reports 3576.75 GiB total and 3166.8701 GiB free at that observation. It is the proposed initial placement. Keep real names, UUIDs, paths and credentials private. Leave DS-A/DS-B outside the initial allocation and do not use VMFSOS/boot volumes. Retain the owner's 3 TB project ceiling despite the larger measured filesystem total. Refresh free space at execution time rather than treating the previous listing as missing.

### Remaining Phase 0 gate

Check available host CPU/RAM, existing VM load/reservations, outstanding storage commitments, backing-device health/latency, chosen VM compatibility/guest features, authorized internal network and administrative recovery access, scoped Zabbix access or an approved lab alternative, offline artifact availability and agreed response-quality/latency goals. Map each dependency to local, approved LAN or provisioning-only. Resolve ordinary design questions from evidence; do not postpone independent safe work indefinitely over nonessential inventory details.

Produce the report in active-prompt section 26: repository findings and actual tests; supplied/verified/unknown host facts; original-requirement traceability; service/identity/network/storage boundaries; typed data/workflow/API/MCP contracts; model/resource benchmark plan; secrets/policy/approval threat model; bilingual UI; connector roadmap; CI/release/offline/restore gates; explicit blockers; and the next small implementation checkpoint.

Use only authorized read-only discovery for that report. No installation, model download, stress test, ESXi networking change, patch, reboot or production-device access is implied. Required architecture, provisioning and target-access approvals must be evidenced. If Phase 0 is already genuinely complete and approved, resume the next unfinished authorized Stage 1A–1E instead of repeating planning.

### VM creation after authorization

| Order | VM | vCPU | RAM GiB | Total disk GiB | Proposed datastore |
|---|---|---:|---:|---:|---|
| 1 | nextops-app | 8 | 32 | 200 | DS-C |
| 2 | nextops-ai | 24 | 128 | 500 | DS-C |
| 3 | nextops-connectors-ro | 4 | 8 | 80 | DS-C |
| Total | 3 NextOps VMs | 36 | 168 | 780 | DS-C |

Ubuntu Server 24.04 LTS is the proposed guest, not an ESXi replacement. These are budget experiments and a capacity-based placement, not allocations already applied or performance certification. Reuse an authorized LAN Zabbix. If none is available, separately account for one approved small lab VM: 4 vCPU, 8 GiB RAM, 100 GiB disk and an 8-GiB provisional ESXi swap allowance. This does not size production Zabbix. Do not create the later standalone database, change executor, monitoring VM or one VM per connector merely to start.

### Storage preflight

The three VMDKs total 780 GiB; plus 168 GiB provisional ESXi swap, the initial subtotal is 948 GiB before other overhead. Including the optional lab gives 1056 GiB. The exact 25% free-space target on DS-C is 894.1875 GiB, conservatively about 900, not the old hypothetical 700-GiB example. With unchanged existing usage, the initial subtotal leaves 2218.87 GiB free before extra growth/overhead, or 1324.68 GiB above the exact target. That difference is not approved spare capacity.

Account separately for outstanding thin-disk growth, powered-off VM swap, VMX/other files, snapshots/consolidation, migration/restore peaks and offline artifacts outside guest disks. Verify swap placement and reconcile any already-created VM to prevent double counting. Check both the retained project ceiling and per-datastore headroom. The normal-operation free-space fraction is a proposed project policy, not a vendor guarantee. No automatic disk shrink/deletion/migration/repartition or memory-reservation change is authorized. Preserve verified model/rollback files, mandatory audit retention, bounded logs and local low-space alerts.

### Phase 1 must finish with the Zabbix answer

**1A:** application guest, typed contracts/policy, PostgreSQL/migrations/durable state, local identity/scopes, sanitized audit, minimal UI/API and denial tests using fixtures. No real target credentials before these controls pass.

**1B:** local CPU inference guest, reviewed artifacts, authenticated internal model service, bounded resource tests, actual new Persian/English generation and offline cold loading. This alone is not the Zabbix milestone.

**1C:** protected gateway and separate read-only Zabbix runner on the connector guest; approved scoped credentials, real bounded reads, deterministic counts, timestamped evidence and denied writes.

**1D:** connect question, collection, aggregation, local synthesis and evidence display. Answer a new Zabbix status question with scope, freshness, missing data, sources and audit. Distinguish API reachability, monitored-host state and engine health.

**1E:** complete-profile offline acceptance with server/browser WAN blocked and authorized Zabbix LAN reachability retained; fresh login, cold start, permitted restart/reboot, failure/low-space behavior and bounded-load measurements. ZBX-01–ZBX-08 and all applicable OFF-01–OFF-10 require real results. Never substitute cached answers, JSON, screenshots or simulator-only success. Direct Linux enrichment follows in Phase 2.

Creation order is not service readiness order. Use START_HERE's dependency-aware startup/shutdown: local storage/key/time prerequisites and database first; model/gateway can start independently; API reports truthful degraded state; worker admits investigations only when required dependencies are healthy. Zabbix failure must not block general local Q&A when its own dependencies are healthy.

After each stage, update PROJECT_STATE with actual work, created roles, versions, exact test commands/results, failed/skipped/not-run checks, blockers and the next single checkpoint. This prompt revision does not create VMs or execute host, model, Zabbix, storage or offline tests.

## فارسی — تکمیل پیش‌نیازها و ادامه از نخستین گام ناتمامِ دارای مجوز

ابتدا [پرامپت فعال نسخهٔ ۳.۰](requirements/NEXTOPS_MASTER_PROMPT.md) و سپس [تاریخچهٔ آن](requirements/PROMPT_CHANGELOG.md)، [وضعیت پروژه](PROJECT_STATE.md)، [راهنمای شروع](fa/START_HERE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [برنامهٔ سرورها](fa/SERVER_PLAN.md)، [یادداشت ESXi](fa/ESXI_BASELINE.md)، [الزام آفلاین](fa/OFFLINE_RUNTIME.md)، [ذخیره‌سازی](STORAGE_PLAN.md) و [رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خوانده شوند. [نسخهٔ محفوظ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) برای جزئیات کامل اولیه، با اعمال اصلاحات صریح نسخهٔ ۳، بررسی شود. بایگانی ثابت است؛ پرامپت فعال به درخواست مالک به‌روز شده است. پیش از ادامه، کار فعلی مخزن و شواهد تکمیل و تأیید هر گام بررسی شوند.

### اطلاعات موجود؛ دوباره به‌عنوان دادهٔ غایب درخواست نشوند

ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هستهٔ فیزیکی، ۲۲۴ رشته، چهار گرهٔ NUMA، حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، نمونهٔ ناقص CPU و فهرست لحظه‌ای سه datastore متصل VMFS-6 قبلاً ارسال شده‌اند. این‌ها شاهد ارسالی‌اند، نه اتصال مستقیم، منابع آزاد فعلی، رزرو یا سنجش کارایی. مدل تجاری دقیق CPU، قابلیت‌های مهمان و توزیع واقعی گره‌ها هنوز روشن نیستند.

DS-C نام عمومی بزرگ‌ترین datastore است: ظرفیت ارسالی ۳۵۷۶٫۷۵ GiB و فضای آزاد ۳۱۶۶٫۸۷۰۱ GiB در همان مشاهده. محل اولیهٔ پیشنهادی همین است. نام واقعی، UUID، مسیر و اطلاعات ورود خصوصی بمانند. DS-A و DS-B در تخصیص اولیه نیستند و حجم‌های VMFSOS و راه‌اندازی استفاده نشوند. سقف سه‌ترابایتی پروژه با وجود ظرفیت بیشتر حفظ شود. فضای آزاد هنگام تغییر واقعی تازه‌سازی شود؛ فهرست قبلی اطلاعات ارسال‌نشده نیست.

### شرط باقی‌ماندهٔ مرحلهٔ صفر

CPU و RAM آزاد، بار و رزرو ماشین‌های موجود، تعهدهای ذخیره‌سازی، سلامت و تأخیر دیسک، سازگاری VM و ویژگی‌های مهمان، شبکهٔ داخلی و بازیابی دسترسی مجاز، دسترسی محدود Zabbix یا آزمایشگاه مصوب، فایل‌های آفلاین و هدف کیفیت و تأخیر بررسی شوند. هر وابستگی محلی، داخلیِ مجاز یا صرفاً زمان آماده‌سازی باشد. تصمیم‌های عادی از شواهد حل شوند و پرسش کم‌اهمیت دربارهٔ موجودی، کار مستقل ایمن را بی‌پایان عقب نیندازد.

گزارش بخش ۲۶ پرامپت فعال تهیه شود: یافته و آزمون واقعی مخزن، مشخصات ارسالی و تأییدشده و نامعلوم، ردیابی نیازها، مرز سرویس و هویت و شبکه و دیسک، قراردادهای دارای نوع، برنامهٔ مدل و منابع، حفاظت اطلاعات ورود و سیاست و تأیید، رابط دوزبانه، مسیر اتصال‌ها، معیارهای انتشار و آفلاین و بازیابی، مانع‌ها و گام کوچک بعدی.

فقط شناسایی فقط‌خواندنیِ دارای مجوز برای گزارش انجام شود. تهیهٔ گزارش اجازهٔ نصب، دانلود مدل، آزمون فشار، تغییر شبکه، وصله، راه‌اندازی دوباره یا تماس عملیاتی نیست. تأیید معماری، ساخت ماشین و دسترسی مقصد باید مستند باشد. اگر مرحلهٔ صفر واقعاً تکمیل و تأیید شده است، از گام ناتمام 1A تا 1E ادامه دهید؛ برنامه‌ریزی را از ابتدا تکرار نکنید.

### ساخت ماشین‌ها پس از مجوز

ابتدا nextops-app با **۸ vCPU، حافظهٔ ۳۲ GiB و دیسک ۲۰۰ GiB**، سپس nextops-ai با **۲۴، ۱۲۸ و ۵۰۰** و در پایان nextops-connectors-ro با **۴، ۸ و ۸۰** ساخته شوند. محل پیشنهادی هر سه DS-C است. مجموع **۳ ماشین، ۳۶ vCPU، حافظهٔ ۱۶۸ GiB و دیسک ۷۸۰ GiB** است. Ubuntu Server 24.04 LTS مهمان پیشنهادی است، نه جایگزین ESXi. منابع و محل پیشنهادی، رزرو اعمال‌شده یا تأیید کارایی نیستند.

Zabbix موجود و مجاز دوباره ساخته نشود. نبود نمونهٔ مناسب می‌تواند یک آزمایشگاه کوچکِ جدا با ۴ vCPU، حافظهٔ ۸ GiB، دیسک ۱۰۰ GiB و سهم موقت swap برابر ۸ GiB نیاز داشته باشد؛ این ظرفیت‌سنجی Zabbix عملیاتی نیست. برای شروع، ماشین مستقل پایگاه، اجرای تغییر، پایش یا یک ماشین برای هر اتصال نسازید.

### بررسی ظرفیت دیسک

۷۸۰ GiB دیسک به‌علاوهٔ ۱۶۸ GiB سهم موقت swap در ESXi، پیش از سایر سربارها ۹۴۸ GiB می‌شود؛ با آزمایشگاه اختیاری ۱۰۵۶ GiB. حاشیهٔ دقیق ۲۵ درصد DS-C برابر ۸۹۴٫۱۸۷۵ GiB و محافظه‌کارانه حدود ۹۰۰ است، نه مثال قدیمیِ ۷۰۰. با ثابت ماندن مصرف موجود، پس از جمع اولیه و پیش از سایر رشد و سربار، ۲۲۱۸٫۸۷ GiB آزاد و ۱۳۲۴٫۶۸ GiB بالاتر از حاشیهٔ دقیق باقی می‌ماند. این اختلاف فضای اضافهٔ تأییدشده نیست.

رشد تعهدشدهٔ thin، swap ماشین خاموش، فایل‌های VMX، snapshot و ادغام، فضای اوج انتقال و بازیابی و فایل‌های بیرون از دیسک مهمان جدا حساب شوند. محل swap و ماشین احتمالیِ ازقبل‌ساخته‌شده تطبیق داده شوند تا دوباره‌شماری رخ ندهد. سقف پروژه و حاشیهٔ هر datastore هم‌زمان کنترل شوند. حاشیه، سیاست پیشنهادی پروژه است و تضمین سازنده نیست. کوچک کردن، حذف، انتقال یا پارتیشن‌بندی خودکار و تغییر رزرو حافظه مجاز نیست. فایل سالم مدل و بازگشت، نگهداری ممیزی، لاگ محدود و هشدار محلی کمبود فضا حفظ شوند.

### پایان مرحلهٔ یک باید پاسخ واقعی باشد

**1A:** ماشین برنامه، قرارداد و سیاست دارای نوع، PostgreSQL و مهاجرت و وضعیت ماندگار، ورود و دامنهٔ محلی، ممیزی پالایش‌شده، رابط حداقلی و آزمون رد عملیات با دادهٔ ساختگی. اطلاعات ورود مقصد فقط پس از قبولی کنترل‌ها وارد شوند.

**1B:** ماشین CPU محلی، فایل‌های بازبینی‌شده، سرویس داخلی احرازهویت‌شده، سقف منابع، پاسخ تازهٔ فارسی و انگلیسی و شروع آفلاین مدل. این به‌تنهایی خروجی Zabbix نیست.

**1C:** درگاه و اتصال‌دهندهٔ فقط‌خواندنی با هویت مستقل، اطلاعات ورود محدود، فراخوانی واقعیِ محدود، شمارش قطعی، شاهد زمان‌دار و رد نوشتن.

**1D:** اتصال سؤال، جمع‌آوری، محاسبه، تولید محلی و نمایش شاهد. پاسخ تازهٔ Zabbix باید دامنه، تازگی، دادهٔ ناقص، منبع و ممیزی داشته باشد. دسترسی API، وضعیت میزبان و سلامت موتور پایش جدا باشند.

**1E:** آزمون کل چیدمان و مرورگر تازه با اینترنت قطع و مسیر داخلی مجاز Zabbix؛ ورود تازه، شروع از حالت متوقف، راه‌اندازی دوبارهٔ مجاز، خطا و کمبود فضا و بار محدود. معیارهای ZBX و همهٔ موارد قابل‌اعمال OFF نتیجهٔ واقعی می‌خواهند؛ کش، JSON، تصویر یا موفقیت صرفاً شبیه‌سازی‌شده کافی نیست. بررسی مستقیم Linux در مرحلهٔ دو اضافه می‌شود.

ترتیب ساخت با آمادگی سرویس یکسان نیست. ترتیب وابستگی‌محور راهنمای شروع رعایت شود: ذخیره و کلید و ساعت و پایگاه ابتدا؛ مدل و درگاه مستقل؛ API با نمایش صادقانهٔ وضعیت محدود؛ پذیرش بررسی توسط پردازشگر فقط با آماده بودن وابستگی‌های الزامی. قطع Zabbix نباید پرسش‌وپاسخ عمومی محلی را با وجود سلامت وابستگی‌های خودش متوقف کند.

پس از هر گام، کار واقعی، نقش‌های ساخته‌شده، نسخه‌ها، دستور و نتیجهٔ دقیق آزمون، شکست و اجرا‌نشدن، مانع و همان یک گام بعد در PROJECT_STATE ثبت شوند. این بازنگری پرامپت هیچ ماشین، مدل اجرایی، تماس با Zabbix یا آزمون میزبان و ذخیره‌سازی و آفلاین ایجاد یا اجرا نکرده است.
