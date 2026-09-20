# Next task / کار بعدی

## English — complete the remaining preflight, then start 1A

Read [START_HERE](en/START_HERE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [ESXI_BASELINE](en/ESXI_BASELINE.md), the [offline contract](en/OFFLINE_RUNTIME.md), [hardware record](requirements/HARDWARE_BASELINE.json), the archived master prompt and relevant security/contracts guides. Preserve existing repository work. This update changes planning documents, not the approval or implementation status.

Already supplied: ESXi 8.0.3 build 24414501; four packages, 112 physical cores, 224 logical threads, four NUMA nodes and 1,442,743,631,872 bytes RAM. Do not ask for these again or treat them as free capacity. Exact CPU SKU and actual node mapping remain unknown; do not infer them from the partial CPU sample.

The immediate Phase 0 task is to close the actionable gaps: available host CPU/memory and existing VM load, datastore headroom/latency, chosen VM compatibility, permitted internal network and recovery access, reachable authorized Zabbix or an approved lab alternative, scoped credentials/host groups, offline artifact availability and agreed quality/latency targets. Map each dependency to local, approved LAN or provisioning-only. Resolve ordinary design questions from evidence; do not turn nonessential inventory questions into an indefinite planning loop.

Produce the architecture/gap/threat report required by the master prompt: repository findings, known versus missing host facts, traceability, service/trust/network/storage boundaries, typed data/workflow/API/MCP contracts, resource/benchmark plan, secret and approval controls, UI/language requirements, connector roadmap and CI/offline/release/restore gates. Use only authorized read-only discovery. Do not install, stress-test, reboot, change ESXi networking or contact production targets just to prepare the report. Provisioning and access require explicit authorization.

After that approval, create the NextOps VMs in this order:

| Order | VM | vCPU | RAM GiB | Disk GiB |
|---|---|---:|---:|---:|
| 1 | `nextops-app` | 8 | 32 | 200 |
| 2 | `nextops-ai` | 24 | 128 | 500 |
| 3 | `nextops-connectors-ro` | 4 | 8 | 80 |
| Total | 3 VMs | 36 | 168 | 780 |

Ubuntu Server 24.04 LTS is the proposed guest, not an ESXi replacement. The old 44-vCPU initial total in this file was stale; 36 is consistent with the hardware record's 24-vCPU AI proposal. No allocation has been applied. Reuse existing LAN Zabbix; an optional small approved `zabbix-lab` is separate and adds 4 vCPU / 8 GiB RAM / 100 GiB disk. Do not create `nextops-db`, `nextops-executor-rw`, a separate monitoring VM or one VM per connector for the first delivery.

Start **1A** on the app VM with typed policy/contracts, PostgreSQL/durable state, local identity, sanitized audit and denial tests using fixtures; no target credentials yet. Continue through **1B** local CPU model, **1C** protected read-only Zabbix evidence, **1D** evidence-linked answer and **1E** offline acceptance. Gates and restart order are in START_HERE. Keep unsupported components explicit rather than success-returning stubs.

**Phase 1 ends only when a new Persian and English question about real authorized Zabbix status receives a locally generated answer with Internet blocked, sources/timestamps and audit.** ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 require actual results, including fresh login and offline restart. A model hello-world, cached response, raw JSON or simulator-only result is not completion. Distinguish API reachability, monitored-host status and monitoring-engine health; never invent missing evidence. Linux enrichment follows in Phase 2.

After each stage update PROJECT_STATE with what was really done, tests run/failed/skipped, blockers and the next single stage. No new VM, runtime, Zabbix connection or offline test has been performed by this documentation update.

## فارسی — پیش‌نیازهای باقی‌مانده، سپس شروع 1A

[راهنمای شروع](fa/START_HERE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [برنامهٔ سرورها](fa/SERVER_PLAN.md)، [یادداشت ESXi](fa/ESXI_BASELINE.md)، [الزام آفلاین](fa/OFFLINE_RUNTIME.md)، [رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json)، پرامپت بایگانی‌شده و راهنماهای امنیت و قراردادها خوانده شوند. کار موجود مخزن حفظ شود. این تغییر، برنامه را به‌روز می‌کند؛ نه وضعیت تأیید یا پیاده‌سازی را.

مشخصات موجود: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هستهٔ فیزیکی، ۲۲۴ رشتهٔ منطقی، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت. این موارد دوباره درخواست و منابع آزاد تلقی نشوند. مدل تجاری دقیق CPU و نگاشت واقعی گره‌ها هنوز نامعلوم‌اند؛ از نمونهٔ ناقص CPU حدس زده نشوند.

کار فوری مرحلهٔ صفر، روشن کردن کمبودهای مؤثر بر شروع است: CPU و حافظهٔ آزاد و بار VMهای موجود، حاشیه و تأخیر دیسک، سازگاری انتخاب‌شدهٔ ماشین، شبکهٔ داخلی و مسیر بازیابی مجاز، Zabbix قابل‌دسترسی یا جایگزین آزمایشگاهی مصوب، اطلاعات ورود و گروه‌های محدود، فایل‌های آفلاین و هدف کیفیت و تأخیر. هر وابستگی محلی، شبکهٔ داخلیِ مجاز یا صرفاً زمان آماده‌سازی باشد. تصمیم‌های عادی از شواهد حل شوند و پرسش غیرضروری دربارهٔ موجودی، برنامه‌ریزی را بی‌پایان نکند.

گزارش معماری، فاصله با نیازها و تهدید مطابق پرامپت تهیه شود: یافته‌های مخزن، مشخصات معلوم و نامعلوم میزبان، ردیابی، مرز سرویس و اعتماد و شبکه و ذخیره، قرارداد داده و گردش‌کار و API و MCP، منابع و سنجش، حفاظت اطلاعات ورود و تأیید، رابط و زبان، مسیر اتصال‌ها و معیارهای CI و آفلاین و انتشار و بازیابی. فقط شناسایی فقط‌خواندنیِ مجاز انجام شود. صرف تهیهٔ گزارش، اجازهٔ نصب، آزمون فشار، راه‌اندازی دوباره، تغییر شبکهٔ ESXi یا تماس با تجهیزات عملیاتی نیست. ساخت ماشین و دسترسی، تأیید صریح می‌خواهند.

پس از تأیید، ابتدا `nextops-app` با **۸ vCPU، حافظهٔ ۳۲ GiB و دیسک ۲۰۰ GiB**، سپس `nextops-ai` با **۲۴ vCPU، حافظهٔ ۱۲۸ GiB و دیسک ۵۰۰ GiB** و در پایان `nextops-connectors-ro` با **۴ vCPU، حافظهٔ ۸ GiB و دیسک ۸۰ GiB** ساخته شوند. مجموع **۳ ماشین، ۳۶ vCPU، حافظهٔ ۱۶۸ GiB و دیسک ۷۸۰ GiB** است.

Ubuntu Server 24.04 LTS مهمان پیشنهادی است، نه جایگزین ESXi. عدد قبلی ۴۴ vCPU در این فایل قدیمی بود؛ ۳۶ با پیشنهاد AI دارای ۲۴ vCPU در رکورد سخت‌افزار هماهنگ است. هیچ تخصیصی اعمال نشده است. Zabbix موجود دوباره ساخته نشود؛ نمونهٔ کوچک و مجاز `zabbix-lab` فقط در صورت نیاز، جداگانه ۴ vCPU، حافظهٔ ۸ GiB و دیسک ۱۰۰ GiB اضافه می‌کند. برای تحویل اول، ماشین مستقل پایگاه، اجرای تغییر، پایش یا ماشین جدا برای هر اتصال نسازید.

گام **1A** روی ماشین برنامه با قرارداد دامنه و سیاست، PostgreSQL و وضعیت ماندگار، ورود محلی، ممیزی پالایش‌شده و آزمون رد عملیات با دادهٔ ساختگی شروع شود؛ هنوز اطلاعات ورود مقصد لازم نیست. سپس **1B** مدل CPU محلی، **1C** شواهد فقط‌خواندنی Zabbix، **1D** پاسخ دارای منبع و **1E** پذیرش آفلاین تکمیل شوند. معیارها و ترتیب شروع مجدد در راهنمای شروع آمده‌اند. جزء پشتیبانی‌نشده صریح باشد، نه تابع نمایشی که موفقیت برمی‌گرداند.

**پایان مرحلهٔ یک فقط زمانی است که سؤال تازهٔ فارسی و انگلیسی دربارهٔ وضعیت واقعی و مجاز Zabbix، با اینترنت قطع، پاسخ تولیدشدهٔ محلی همراه منبع، زمان و ممیزی بگیرد.** ZBX-01 تا ZBX-08 و موارد قابل‌اعمال OFF-01 تا OFF-10، از جمله ورود تازه و شروع آفلاین، نتیجهٔ واقعی می‌خواهند. پاسخ آزمایشی مدل، کش، JSON خام یا شبیه‌ساز پایان کار نیست. دسترسی API، وضعیت میزبان و سلامت موتور پایش جدا باشند و دادهٔ غایب ساخته نشود. گسترش Linux در مرحلهٔ دو است.

پس از هر گام، کار واقعی، آزمون اجراشده یا ناموفق یا اجرا‌نشده، مانع و همان یک گام بعد در PROJECT_STATE ثبت شوند. این به‌روزرسانی مستندات هیچ VM، محیط اجرایی، اتصال Zabbix یا آزمون آفلاینی ایجاد یا اجرا نکرده است.
