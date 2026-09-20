# Next task / کار بعدی

## English — complete the remaining preflight, then start 1A

Read [START_HERE](en/START_HERE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [ESXI_BASELINE](en/ESXI_BASELINE.md), the [offline contract](en/OFFLINE_RUNTIME.md), the bilingual [storage plan](STORAGE_PLAN.md), [hardware record](requirements/HARDWARE_BASELINE.json), the archived master prompt and relevant security/contracts guides. Preserve existing repository work. This update changes planning documents, not approval or implementation status.

**Latest storage evidence is now supplied.** The owner's filesystem listing reports three mounted VMFS-6 datastores. Public aliases DS-A/DS-B/DS-C omit real names, UUIDs and paths. DS-C, the largest, reports 3,576.75 GiB total and 3,166.8701 GiB free; propose it for the three initial NextOps VMs. Leave DS-A/DS-B unallocated and exclude VMFSOS/boot volumes. Retain the earlier 3 TB project ceiling despite the larger observed total. Do not ask for the filesystem listing as though it were still missing; refresh it only for capacity freshness at the actual change window.

**Storage gate:** the unchanged 200/500/80-GiB VM disks total 780 GiB; plus 168 GiB provisional ESXi swap, the first profile is 948 GiB before other overhead. With existing usage unchanged, DS-C would retain 2,218.87 GiB free before additional growth/overhead. The exact 25% free-space target is now 894.1875 GiB (round conservatively to about 900), not the former hypothetical 700-GiB example. The 1,324.68-GiB difference above that exact target must still cover existing thin-disk growth, powered-off VM swap, VMX/other files, maintenance/restore workspace and artifacts outside guest disks. It is not approved spare capacity. Check both project ceiling and per-datastore headroom. Review actual swap placement and reconcile any already-created VM to avoid double counting. No disk shrink, deletion, migration, repartition or memory-reservation change is authorized by this plan.

Already supplied: ESXi 8.0.3 build 24414501; four packages, 112 physical cores, 224 logical threads, four NUMA nodes and 1,442,743,631,872 bytes RAM, plus the point-in-time datastore listing. Do not ask for these again or treat host totals as free CPU/RAM. Exact CPU SKU and actual node mapping remain unknown; do not infer them from the partial CPU sample. Filesystem capacity does not establish RAID layout, disk health or performance.

The immediate Phase 0 task is to close actionable gaps: available host CPU/memory and existing VM load, outstanding storage commitments and backing-device health/latency, chosen VM compatibility, permitted internal network and recovery access, reachable authorized Zabbix or an approved lab alternative, scoped credentials/host groups, offline artifacts and agreed quality/latency targets. Map each dependency to local, approved LAN or provisioning-only. Resolve ordinary design questions from evidence; do not turn nonessential inventory questions into an indefinite planning loop.

Produce the architecture/gap/threat report required by the master prompt: repository findings, known versus missing host facts, traceability, service/trust/network/storage boundaries, typed data/workflow/API/MCP contracts, resource/benchmark plan, secret and approval controls, UI/language requirements, connector roadmap and CI/offline/release/restore gates. Use only authorized read-only discovery. Do not install, stress-test, reboot, change ESXi networking or contact production targets just to prepare the report. Provisioning and access require authorization.

After approval and the preflight gate, create the NextOps VMs in this order. Placement is a capacity-based proposal, not a performance certification:

| Order | VM | vCPU | RAM GiB | Disk GiB | Datastore alias |
|---|---|---:|---:|---:|---|
| 1 | `nextops-app` | 8 | 32 | 200 | DS-C |
| 2 | `nextops-ai` | 24 | 128 | 500 | DS-C |
| 3 | `nextops-connectors-ro` | 4 | 8 | 80 | DS-C |
| Total | 3 VMs | 36 | 168 | 780 | DS-C |

Ubuntu Server 24.04 LTS is the proposed guest, not an ESXi replacement. The 36-vCPU total matches the 24-vCPU AI proposal; no allocation has been applied. Reuse existing LAN Zabbix. An optional small approved `zabbix-lab` adds 4 vCPU / 8 GiB RAM / 100 GiB disk and an 8-GiB provisional swap allowance; the initial subtotal including that lab is 1,056 GiB. Production Zabbix sizing is separate. Do not create `nextops-db`, `nextops-executor-rw`, a separate monitoring VM or one VM per connector for the first delivery.

Start **1A** on the app VM with typed policy/contracts, PostgreSQL/durable state, local identity, sanitized audit and denial tests using fixtures; no target credentials yet. Continue through **1B** local CPU model, **1C** protected read-only Zabbix evidence, **1D** evidence-linked answer and **1E** offline acceptance. Gates and restart order are in START_HERE. Keep unsupported components explicit rather than success-returning stubs.

**Phase 1 ends only when new Persian and English questions about real authorized Zabbix status receive locally generated answers with Internet blocked, sources/timestamps and audit.** ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 require actual results, including fresh login and offline restart. A model hello-world, cached response, raw JSON or simulator-only result is not completion. Distinguish API reachability, monitored-host status and monitoring-engine health; never invent missing evidence. Linux enrichment follows in Phase 2. Preserve verified model/rollback files, bounded logs and local low-space alerts; do not trade away offline readiness to save disk.

After each stage update PROJECT_STATE with actual work, tests run/failed/skipped, blockers and the next single stage. The supplied storage snapshot supersedes older statements that no capacity figures have been provided. No new VM, runtime, Zabbix connection, storage test or offline test has been performed by this documentation update.

## فارسی — پیش‌نیازهای باقی‌مانده، سپس شروع 1A

[راهنمای شروع](fa/START_HERE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [برنامهٔ سرورها](fa/SERVER_PLAN.md)، [یادداشت ESXi](fa/ESXI_BASELINE.md)، [الزام آفلاین](fa/OFFLINE_RUNTIME.md)، [برنامهٔ دوزبانهٔ ذخیره‌سازی](STORAGE_PLAN.md)، [رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json)، پرامپت بایگانی‌شده و راهنماهای امنیت و قراردادها خوانده شوند. کار موجود مخزن حفظ شود. این تغییر، برنامه را به‌روز می‌کند؛ نه وضعیت تأیید یا پیاده‌سازی را.

**شاهد تازهٔ ذخیره‌سازی دریافت شده است.** خروجی ارسالی مالک سه datastore متصل از نوع VMFS-6 دارد. در مخزن عمومی، DS-A و DS-B و DS-C نام مستعارند و نام واقعی، UUID و مسیر منتشر نمی‌شود. DS-C، بزرگ‌ترین مورد، ظرفیت ۳٬۵۷۶٫۷۵ GiB و فضای آزاد ۳٬۱۶۶٫۸۷۰۱ GiB گزارش می‌کند و محل پیشنهادی هر سه ماشین اولیه است. DS-A و DS-B تخصیص نگیرند و حجم‌های VMFSOS و راه‌اندازی کنار گذاشته شوند. سقف قبلی سه‌ترابایتی پروژه با وجود ظرفیت بیشتر حفظ شود. فهرست فایل‌سیستم دوباره به‌عنوان اطلاعات ارسال‌نشده خواسته نشود؛ فقط هنگام تغییر واقعی، تازگی فضا کنترل شود.

**شرط دیسک:** دیسک‌های ۲۰۰، ۵۰۰ و ۸۰ GiB همچنان مجموعاً ۷۸۰ GiB هستند. با سهم موقت ۱۶۸ GiB برای swap در ESXi، جمع اولیه پیش از سایر سربارها ۹۴۸ GiB می‌شود. با ثابت ماندن مصرف موجود، پیش از رشد و سربار اضافی، ۲٬۲۱۸٫۸۷ GiB آزاد باقی می‌ماند. حاشیهٔ دقیق ۲۵ درصد اکنون ۸۹۴٫۱۸۷۵ GiB است که محافظه‌کارانه حدود ۹۰۰ GiB در نظر گرفته می‌شود؛ مثال فرضیِ ۷۰۰ GiB دیگر مبنا نیست. اختلاف ۱٬۳۲۴٫۶۸ GiB بالاتر از حاشیهٔ دقیق، باید رشد تعهدشدهٔ thin، swap ماشین‌های خاموش، سربار VMX و سایر فایل‌ها، فضای موقت نگهداری و بازیابی و فایل‌های بیرون از دیسک مهمان را پوشش دهد؛ فضای اضافهٔ تأییدشده نیست. سقف پروژه و حاشیهٔ هر datastore هم‌زمان بررسی شوند. محل واقعی swap و ماشین احتمالیِ ازقبل‌ساخته‌شده تطبیق داده شوند تا دوباره‌شماری رخ ندهد. این طرح مجوز کوچک کردن، حذف، انتقال، پارتیشن‌بندی یا تغییر رزرو حافظه نیست.

مشخصات موجود: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هستهٔ فیزیکی، ۲۲۴ رشتهٔ منطقی، چهار گرهٔ NUMA، حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت و فهرست لحظه‌ای datastore. این موارد دوباره درخواست و منابع کل CPU/RAM، منابع آزاد تلقی نشوند. مدل دقیق CPU و نگاشت گره‌ها هنوز معلوم نیست و از نمونهٔ ناقص حدس زده نمی‌شود. ظرفیت فایل‌سیستم، RAID، سلامت و کارایی دیسک را ثابت نمی‌کند.

کار فوری مرحلهٔ صفر، روشن کردن کمبودهای مؤثر بر شروع است: CPU و حافظهٔ آزاد و بار VMهای موجود، تعهدهای ذخیره‌سازی و سلامت و تأخیر دیسک، سازگاری ماشین، شبکهٔ داخلی و مسیر بازیابی مجاز، Zabbix قابل‌دسترسی یا آزمایشگاه مصوب، اطلاعات ورود و گروه‌های محدود، فایل‌های آفلاین و هدف کیفیت و تأخیر. هر وابستگی محلی، داخلیِ مجاز یا صرفاً زمان آماده‌سازی باشد. تصمیم‌های عادی از شواهد حل شوند و پرسش غیرضروری برنامه‌ریزی را بی‌پایان نکند.

گزارش معماری، فاصله با نیازها و تهدید مطابق پرامپت تهیه شود: یافته‌های مخزن، واقعیت‌های معلوم و نامعلوم، ردیابی، مرز سرویس و اعتماد و شبکه و ذخیره، قرارداد داده و گردش‌کار و API و MCP، منابع و سنجش، حفاظت اطلاعات ورود و تأیید، رابط و زبان، مسیر اتصال‌ها و معیارهای CI و آفلاین و انتشار و بازیابی. فقط شناسایی فقط‌خواندنیِ مجاز انجام شود. تهیهٔ گزارش اجازهٔ نصب، آزمون فشار، راه‌اندازی دوباره، تغییر شبکهٔ ESXi یا تماس با تجهیز عملیاتی نیست. ساخت ماشین و دسترسی تأیید می‌خواهند.

پس از تأیید و عبور از بررسی پیش‌نیازها، ابتدا `nextops-app` با **۸ vCPU، حافظهٔ ۳۲ GiB و دیسک ۲۰۰ GiB**، سپس `nextops-ai` با **۲۴ vCPU، حافظهٔ ۱۲۸ GiB و دیسک ۵۰۰ GiB** و در پایان `nextops-connectors-ro` با **۴ vCPU، حافظهٔ ۸ GiB و دیسک ۸۰ GiB** ساخته شوند. محل پیشنهادی هر سه **DS-C** است. مجموع **۳ ماشین، ۳۶ vCPU، حافظهٔ ۱۶۸ GiB و دیسک ۷۸۰ GiB** است. این پیشنهاد بر ظرفیت متکی است، نه تأیید کارایی.

Ubuntu Server 24.04 LTS مهمان پیشنهادی است، نه جایگزین ESXi. عدد ۳۶ vCPU با پیشنهاد AI دارای ۲۴ vCPU هماهنگ است و هیچ تخصیصی اعمال نشده است. Zabbix موجود دوباره ساخته نشود؛ `zabbix-lab` کوچکِ مجاز فقط در صورت نیاز ۴ vCPU، حافظهٔ ۸ GiB، دیسک ۱۰۰ GiB و سهم موقت swap برابر ۸ GiB اضافه می‌کند؛ جمع اولیه با این آزمایشگاه ۱٬۰۵۶ GiB است. ظرفیت‌سنجی Zabbix عملیاتی جداست. برای تحویل اول ماشین مستقل پایگاه، اجرای تغییر، پایش یا یک ماشین برای هر اتصال نسازید.

گام **1A** با قرارداد دامنه و سیاست، PostgreSQL و وضعیت ماندگار، ورود محلی، ممیزی پالایش‌شده و آزمون رد عملیات روی دادهٔ ساختگی شروع شود؛ اطلاعات ورود مقصد هنوز لازم نیست. سپس **1B** مدل CPU محلی، **1C** شواهد فقط‌خواندنی Zabbix، **1D** پاسخ دارای منبع و **1E** پذیرش آفلاین تکمیل شوند. معیار و ترتیب شروع مجدد در راهنمای شروع آمده‌اند. جزء پشتیبانی‌نشده صریح باشد، نه تابع نمایشیِ موفق.

**پایان مرحلهٔ یک فقط زمانی است که سؤال‌های تازهٔ فارسی و انگلیسی دربارهٔ وضعیت واقعی و مجاز Zabbix با اینترنت قطع، پاسخ تولیدشدهٔ محلی همراه منبع، زمان و ممیزی بگیرند.** ZBX-01 تا ZBX-08 و موارد قابل‌اعمال OFF-01 تا OFF-10، از جمله ورود تازه و شروع آفلاین، نتیجهٔ واقعی می‌خواهند. پاسخ آزمایشی مدل، کش، JSON خام یا شبیه‌ساز کافی نیست. دسترسی API، وضعیت میزبان و سلامت موتور پایش جدا و دادهٔ غایب ساخته نشود. گسترش Linux در مرحلهٔ دو است. فایل سالم مدل و بازگشت، لاگ محدود و هشدار محلی کمبود فضا حفظ شوند؛ صرفه‌جویی دیسک نباید کارکرد آفلاین را از بین ببرد.

پس از هر گام، کار واقعی، آزمون اجراشده یا ناموفق یا اجرا‌نشده، مانع و همان یک گام بعد در PROJECT_STATE ثبت شوند. شاهد تازه بر عبارت‌های قدیمیِ نبود اطلاعات ظرفیت مقدم است. این به‌روزرسانی هیچ VM، محیط اجرایی، اتصال Zabbix، آزمون ذخیره‌سازی یا آزمون آفلاینی ایجاد یا اجرا نکرده است.
