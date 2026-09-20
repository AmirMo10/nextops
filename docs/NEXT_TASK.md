# Next task / کار بعدی

## English — Phase 0: discovery and architecture review

Read the complete master prompt and all relevant guides, especially the [mandatory offline contract](en/OFFLINE_RUNTIME.md), [G10 server plan](en/SERVER_PLAN.md) and [revised roadmap](en/ROADMAP.md). Inspect the current repository and preserve changes. Establish actual server access before reporting hardware observations. Use only authorized non-destructive discovery; do not install packages, stress hardware, download models, change networking or contact production targets.

Produce an evidence-backed report covering repository findings, verified versus unresolved host facts, requirement traceability, component/trust/deployment boundaries, source layout, CPU model/runtime shortlist and staged benchmark, resource-budget proposal, identity/secrets/approval threat model, data/workflow/evidence/topology/API/UI contracts, connector capability roadmap, CI/release/rollback, tests/offline/backup gates and explicit blockers.

Define operating scale: asset count, event/evidence volume, retention, concurrent investigations and target response times. Do not infer scale or measured performance from RAM capacity. Record CPU cores versus logical allocation, NUMA/ISA, available resources and existing workloads only when actually inspected. Establish the current hypervisor/bare-metal context before choosing VM placement. Inventory every dependency as local, approved LAN or provisioning-only.

The owner's first implementation outcome is explicit: **by the end of Phase 1, local CPU AI must answer a new question about real authorized Zabbix status with Internet blocked.** Plan three NextOps VMs initially: app/database, CPU inference and protected read-only connectors. The 44 vCPU / 168 GiB RAM budget is unmeasured and must be reviewed against the real host. Reuse existing LAN Zabbix, or separately account for one authorized lab VM. Do not assume Zabbix already exists or that its version/access is known.

Resolve Zabbix version, endpoint reachability, scoped credential provisioning, allowed host groups, available self-monitoring items and expected question set through authorized discovery. Do not print credentials or private inventory. Test API reachability separately from monitored-host state and monitoring-engine health. The first answer does not wait for Linux SSH, advanced RAG or the full dashboard.

Acceptance: owner reviews and approves architecture/roadmap; unsupported facts remain labeled; the smallest Phase 1 increment has a concrete acceptance test. Stop before platform implementation or host changes. A candidate first increment is the typed domain/policy contract with deny-by-default tests and a durable-state design. Subsequent increments in that same phase must connect real Zabbix evidence to an offline local answer and satisfy ZBX-01–ZBX-08; foundation-only work does not complete Phase 1.

## فارسی — مرحلهٔ صفر: شناخت و بازبینی معماری

پرامپت کامل و راهنماهای مرتبط، به‌ویژه [الزام آفلاین](fa/OFFLINE_RUNTIME.md)، [چیدمان سرورها](fa/SERVER_PLAN.md) و [نقشهٔ راه بازنگری‌شده](fa/ROADMAP.md) خوانده شوند. مخزن فعلی بررسی و تغییرات حفظ شوند. پیش از گزارش سخت‌افزار، دسترسی واقعی سرور مشخص شود. فقط شناسایی غیرمخرب و مجاز انجام شود؛ نصب بسته، آزمون فشار، دانلود مدل، تغییر شبکه و تماس با تجهیز عملیاتی انجام نشود.

گزارش مستند باید یافتهٔ مخزن، مشخصات تأییدشده و نامشخص میزبان، ردیابی نیاز، مرز جزء و اعتماد و استقرار، ساختار کد، فهرست مدل و محیط اجرای CPU و برنامهٔ سنجش مرحله‌ای، پیشنهاد بودجهٔ منابع، مدل تهدید هویت و اطلاعات ورود و تأیید، قرارداد داده و کار و شواهد و توپولوژی و API و رابط، نقشهٔ قابلیت اتصال، CI و انتشار و بازگشت، معیار آزمون و آفلاین و پشتیبان و موانع صریح را پوشش دهد.

تعداد تجهیز، حجم رویداد و شاهد، نگهداری، بررسی هم‌زمان و هدف زمان پاسخ مشخص شوند. ظرفیت واقعی از RAM حدس زده نشود. هسته در برابر سهم منطقی، NUMA و ISA، منابع آزاد و بار موجود فقط پس از مشاهده ثبت شوند. پیش از چیدمان ماشین‌ها، وضعیت بستر مجازی‌سازی یا نصب مستقیم روشن شود. هر وابستگی در گروه محلی، شبکهٔ داخلیِ مجاز یا صرفاً زمان آماده‌سازی قرار بگیرد.

خروجی اولیهٔ خواسته‌شده روشن است: **تا پایان مرحلهٔ یک، هوش مصنوعی CPU محلی با اینترنت قطع به سؤال تازه دربارهٔ وضعیت واقعی و مجاز Zabbix پاسخ بدهد.** برای آغاز، سه ماشین NextOps در نظر بگیرید: برنامه و پایگاه، هوش مصنوعی و اتصال فقط‌خواندنیِ محافظت‌شده. بودجهٔ ۴۴ vCPU و ۱۶۸ GiB حافظه اندازه‌گیری نشده و باید با میزبان واقعی تطبیق داده شود. از Zabbix موجود در شبکهٔ داخلی استفاده یا یک ماشین آزمایشگاهی مجاز جدا حساب شود. وجود Zabbix، نسخه و دسترسی آن مفروض نیست.

نسخه، دسترسی به API، روش آماده‌سازی اطلاعات ورود محدود، گروه‌های میزبان مجاز، شاخص‌های خودپایشی موجود و سؤال‌های مورد انتظار از مسیر شناسایی مجاز مشخص شوند. اطلاعات ورود و موجودی خصوصی نمایش داده نشوند. دسترسی API از وضعیت میزبان‌ها و سلامت موتور پایش جدا آزموده شود. اولین پاسخ نباید منتظر SSH مستقیم Linux، RAG پیشرفته یا داشبورد کامل بماند.

معیار پذیرش: مالک معماری و نقشهٔ راه را بازبینی و تأیید کند؛ واقعیت بی‌شاهد برچسب داشته باشد؛ کوچک‌ترین گام مرحلهٔ یک آزمون پذیرش روشن داشته باشد. پیش از ساخت محصول یا تغییر میزبان توقف شود. قرارداد دارای نوع دامنه و سیاست با آزمون رد پیش‌فرض و طرح وضعیت ماندگار می‌تواند اولین گام باشد. گام‌های بعدی همان مرحله باید شواهد واقعی Zabbix را به پاسخ آفلاین محلی وصل کنند و ZBX-01 تا ZBX-08 را بگذرانند؛ آماده‌سازی پایه به‌تنهایی پایان مرحلهٔ یک نیست.
