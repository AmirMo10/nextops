# Next task / کار بعدی

Updated: 2026-09-21 — Phase 0 accepted; Stage 1A Increment 1 is implemented and the durable app slice is next.

## English — continue Stage 1A with the durable local app slice

Read the [active master prompt](requirements/NEXTOPS_MASTER_PROMPT.md) with the new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md), [Zabbix guide](en/ZABBIX_SERVER.md), [per-server deployer guide](en/DEPLOYMENT_DOSSIERS.md), [allocation record](requirements/ZABBIX_SERVER_PLAN.json), [START_HERE](en/START_HERE.md), [PROJECT_STATE](PROJECT_STATE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [STORAGE_PLAN](STORAGE_PLAN.md), [OFFLINE_RUNTIME](en/OFFLINE_RUNTIME.md), [ESXI_BASELINE](en/ESXI_BASELINE.md) and [hardware evidence](requirements/HARDWARE_BASELINE.json). Original detail remains in the [unchanged v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md); all 51 sections and eleven integrations remain in scope.

The new amendment supersedes the old small `zabbix-lab` fallback and combined totals in active-prompt v3.0 section 18 and older guide examples. It does not change the three initial NextOps core VMs or authorize provisioning. Inspect actual Git state, work already done and approval/test evidence before resuming; do not overwrite work or restart completed discovery indefinitely.

### Current checkpoint: Stage 1A Increment 2

The owner accepted the paired [Phase 0 report](en/PHASE_0_REPORT.md), [Persian report](fa/PHASE_0_REPORT.md), ADRs 0001–0006, trust boundaries, and Stage 1A–1E roadmap on 2026-09-21. Stage 1A Increment 1 now provides the locked Python project, typed boundary contracts, and deterministic denial policy with 18 passing unit cases. It has no live service, database, connector, credential, or AI path.

The next bounded change is Increment 2: define the local identity bootstrap/recovery flow, add PostgreSQL migrations and least-privilege roles for organization/environment/target/run/audit state, persist idempotent run creation and worker leases, expose the minimal authenticated versioned API, and return one bilingual fixture-backed result. Build and test this locally before any target credential or model integration.

The four schema-validated files under `deploy/server-dependencies` are now the public deployer handoff for the selected servers. They do not make Increment 2 or any VM deployable. Increment 2 should replace the app dossier's currently blocked installer/readiness entries only after actual migrations, roles, runtime dependencies, service definitions, clean offline install, backup, and rollback procedures exist and are tested. Environment-specific values belong in an approved private deployment record keyed by `required_inputs`, never in these public files.

Acceptance evidence for Increment 2:

- authenticated actor context is derived server-side and revoked or cross-scope access is denied;
- migrations, database constraints, restricted roles, audit append behavior, idempotency, leases, restart recovery, and rollback/recovery are tested against real isolated PostgreSQL;
- audit/database failure returns an explicit failed or degraded state rather than unlogged success;
- a minimal Persian/English fixture result shows source, time, scope, partial/stale state, typed errors, and audit reference;
- Ruff, strict mypy, pytest, documentation checks, frozen install, dependency audit, and secret review pass with exact results recorded.

### Already supplied

ESXi 8.0.3 build 24414501; four packages, 112 physical cores, 224 threads, four NUMA nodes and 1,442,743,631,872 memory bytes; a partial Intel CPU sample; and point-in-time VMFS values. DS-C reports 3576.75 GiB total and 3166.8701171875 GiB free. These are owner-supplied observations, not a live capacity reservation or directly performed inspection. Do not ask for them again as missing. Exact CPU SKU, guest ISA, actual node distribution, current available CPU/RAM and competing workload still need evidence.

Keep real datastore names, UUIDs, addresses and credentials private. DS-C is the capacity-based initial placement; DS-A/DS-B and system/boot volumes remain outside this allocation. Retain the 3 TB project ceiling and refresh changing capacity at the execution window.

### Remaining private preflight and provisioning gate

Check available CPU/RAM, VM load/reservations, outstanding thin-disk commitments, actual ESXi swap placement, backing storage health/latency, VM compatibility and guest features, approved local network/admin recovery paths, offline package/model artifacts and agreed quality/latency targets. Map each dependency to local, approved LAN or provisioning-only.

For the new Zabbix path, prepare a separate monitoring VM; when an appropriate authorized installation already exists, inspect and reuse it instead of duplicating it. Confirm frontend base path/version, read-only host-group scope, protected token delivery, self-monitoring items, required monitored guests and sample questions. Do not put private details or tokens into the repository.

The active-prompt section 26 report is accepted and the first local contract increment is complete. Before any infrastructure operation, use only authorized read-only discovery to close the facts that affect that operation. Stage 1A code approval does not imply VM creation, host installation, model download, target access, patch, stress test, network change or reboot.

### Selected starting profile after authorization

| Order / deadline | VM | vCPU | RAM GiB | Disk GiB | Datastore |
|---|---|---:|---:|---:|---|
| 1 | nextops-app | 8 | 32 | 200 | DS-C |
| 2 | nextops-ai | 24 | 128 | 500 | DS-C |
| 3 | nextops-connectors-ro | 4 | 8 | 80 | DS-C |
| Ready before 1C; preparation may run alongside 1A/1B | zabbix-server | 4 | 16 | 200 | DS-C |
| Total | 3 NextOps + 1 Zabbix = 4 VMs | 40 | 184 | 980 | DS-C |

Keep ESXi; Ubuntu Server 24.04 LTS is the proposed guest. Zabbix uses its own local PostgreSQL, Nginx/PHP frontend/API and Agent 2; the NextOps database is still an independent restricted service in `nextops-app`. Do not create a separate NextOps DB, write executor, additional lab/monitoring VM, second model server or per-connector VMs for this milestone.

The Zabbix LVM proposal is `vg_zabbix`: 1-GiB EFI and 2-GiB /boot outside LVM; root 32, /var 16, /var/log 8, /var/lib/postgresql 112 and guest swap 4 GiB, leaving approximately 25 GiB free in the VG. Fresh disks only; verify mounts before database initialization. See the guide for metadata/alignment, encryption/recovery and ownership caveats. Proposed history/trend retention is 7/90 days, subject to effective item settings and actual growth; not a preconfigured guarantee.

### Storage and offline gate

The combined virtual disks total 980 GiB. Provisional ESXi swap of 184 GiB gives **1164 GiB before other overhead**. From the supplied free-space snapshot, unchanged existing usage would leave **2002.87 GiB free**, approximately **1108.68 GiB above the exact 894.1875-GiB headroom target**. Round the target conservatively to about 900 GiB. Do not add the old 100-GiB lab or guest swap already inside VMDKs a second time.

Future combined profiles are 5 VMs / 48 vCPU / 248 GiB RAM / 1280 GiB disks after the NextOps DB split, and 6 VMs / 52 vCPU / 264 GiB RAM / 1360 GiB disks with remediation. Their provisional disk-plus-ESXi-swap subtotals are 1528 and 1624 GiB. These profiles are alternatives, not cumulative additions or resource reservations. Pure NextOps counts remain 3/4/5.

Apply the retained project ceiling and every per-datastore capacity check: existing growth, powered-off VM swap, VMX files, snapshots/consolidation, maintenance/restore copies and offline artifacts outside guest disks. Reconcile any already-created VM to avoid double subtraction. No disk shrink, deletion, migration, repartition or memory-reservation change is authorized. Keep verified model/rollback files, required audit retention and local low-space alerts. Independent backups remain a production gate.

### First useful answer, not just installation

**1A:** local identity/scopes, typed contracts/policy, PostgreSQL/migrations, durable requests, audit and minimal fixture-backed UI/API on the app VM; denied operations tested before real target credentials.

**1B:** approved local CPU runtime/model on the AI VM, authenticated internal inference, bounded resources, real Persian/English answers and offline cold loading.

**Zabbix prerequisite before 1C:** actual database mount, services, frontend/API and current monitoring evidence on the dedicated VM, with local administration and restricted reader identity. Monitor itself and the initial guests through approved narrowly scoped agent paths; do not grant the model broad network access or command execution.

**1C:** MCP gateway and isolated Zabbix runner, scoped token, bounded version-compatible API reads, deterministic counts/timestamps, deny all writes and unlisted methods. Only this runner receives the Zabbix token; model and browser never do.

**1D:** new question -> evidence collection -> deterministic aggregation -> CPU explanation -> actual source/time/scope and audit. Distinguish API reachability, monitored-estate state and engine health; fresh API retrieval does not make old measurements current. Prompt injection in event names remains untrusted data.

**1E:** all four VMs and a fresh browser tested with Internet blocked and approved local reachability retained. Include Zabbix/database/model cold start, fresh login, revoked token/unreachable/stale-data cases, failure/low-space behavior and measured latency/resource limits. Satisfy ZBX-01–ZBX-08 and applicable OFF-01–OFF-10; fixtures, cached replies, JSON or a dashboard alone do not pass. Linux enrichment is Phase 2.

Use dependency-aware service readiness, not fixed sleeps or an Internet test. The databases precede their dependants; model/gateway can start independently. Zabbix failure must not prevent general local Q&A when its own dependencies are healthy. A host failure affects both systems; independent host-outage detection and backups are separate requirements.

After each increment, update PROJECT_STATE with actual work, created roles, exact versions/test commands/results, failed/skipped/not-run cases, remaining blockers and the next checkpoint. Increment 1 changed local repository code only; no host, VM, LVM, model, Zabbix, network, restart or recovery work was performed.

## فارسی — ادامهٔ 1A با برش ماندگار app محلی

[پرامپت فعال](requirements/NEXTOPS_MASTER_PROMPT.md)، [اصلاحیهٔ تازهٔ چیدمان](requirements/DEPLOYMENT_UPDATE.md)، [راهنمای Zabbix](fa/ZABBIX_SERVER.md)، [راهنمای پرونده‌های استقرار](fa/DEPLOYMENT_DOSSIERS.md)، [رکورد تخصیص](requirements/ZABBIX_SERVER_PLAN.json)، [شروع کار](fa/START_HERE.md)، [وضعیت پروژه](PROJECT_STATE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [سرورها](fa/SERVER_PLAN.md)، [ذخیره‌سازی](STORAGE_PLAN.md)، [آفلاین](fa/OFFLINE_RUNTIME.md)، [ESXi](fa/ESXI_BASELINE.md) و [شاهد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خوانده شوند. جزئیات اولیه در [بایگانی ثابت نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) باقی است؛ ۵۱ بخش و یازده اتصال حذف نمی‌شوند.

اصلاحیه فقط نمونهٔ آزمایشگاهی کوچک و مجموع منابع وابسته به آن را در بخش ۱۸ پرامپت ۳.۰ و مثال‌های قدیمی جایگزین می‌کند؛ تعداد سه ماشین اولیهٔ خود NextOps و شروط مجوز تغییر نمی‌کنند. پیش از ادامه، Git، کار موجود، تأییدها و نتیجهٔ آزمون بررسی شوند؛ کار بازنویسی یا شناسایی تکمیل‌شده بی‌دلیل تکرار نشود.

### نقطهٔ فعلی: Increment 2 از 1A

مالک در ۲۱ سپتامبر ۲۰۲۶ [گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md)، ADRهای 0001 تا 0006، مرزهای اعتماد و نقشهٔ 1A تا 1E را پذیرفت. Increment 1 از 1A اکنون پروژهٔ Python قفل‌شده، قراردادهای مرزی دارای نوع و سیاست قطعی رد پیش‌فرض را با ۱۸ آزمون قبول‌شده دارد. هنوز سرویس زنده، پایگاه، connector، credential یا مسیر AI وجود ندارد.

تغییر محدود بعدی Increment 2 است: طراحی bootstrap و recovery هویت محلی، migration و role محدود PostgreSQL برای سازمان، محیط، هدف، run و audit، ساخت idempotent run و lease ماندگار، API نسخه‌دار و احرازهویت‌شدهٔ حداقلی و یک نتیجهٔ دوزبانه با fixture. این مسیر ابتدا محلی و بدون credential مقصد یا مدل ساخته و آزموده شود.

چهار فایل معتبرشده با schema در `deploy/server-dependencies` اکنون قرارداد عمومی تحویل به مسئول استقرارند؛ اما Increment 2 یا هیچ VM را آمادهٔ نصب نمی‌کنند. ورودی مسدود app فقط پس از وجود و آزمون migration، role، dependency، service definition، نصب پاک آفلاین، backup و rollback واقعی جایگزین شود. مقدار محیط واقعی در رکورد خصوصی و بر اساس شناسهٔ `required_inputs` قرار می‌گیرد، نه در فایل عمومی.

شاهد پذیرش Increment 2:

- Actor احرازشده در سرور ساخته و دسترسی لغوشده یا خارج از دامنه رد شود؛
- migration، قید، role محدود، append ممیزی، idempotency، lease، بازیابی پس از restart و rollback/recovery با PostgreSQL جدا و واقعی آزموده شوند؛
- خرابی ممیزی یا پایگاه به وضعیت شکست یا کاهش‌یافتهٔ صریح برسد، نه موفقیت ثبت‌نشده؛
- نتیجهٔ fixture فارسی و انگلیسی منبع، زمان، دامنه، partial/stale، خطای دارای نوع و ارجاع audit را نشان دهد؛
- Ruff، mypy سخت‌گیرانه، pytest، بررسی مستندات، نصب قفل‌شده، audit وابستگی و بررسی رمز با نتیجهٔ دقیق قبول شوند.

### اطلاعات موجود

ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ CPU، تعداد ۱۱۲ هسته و ۲۲۴ رشته، چهار گرهٔ NUMA، حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، نمونهٔ ناقص CPU و ظرفیت لحظه‌ای VMFSها قبلاً ارسال شده‌اند. DS-C ظرفیت 3576.75 GiB و فضای آزاد 3166.8701171875 GiB گزارش کرده است. این‌ها شاهد ارسالی‌اند، نه رزرو یا اتصال مستقیم. دوباره به‌عنوان دادهٔ غایب خواسته نشوند. مدل دقیق CPU، ISA مهمان، توزیع گره‌ها، منابع آزاد و بار رقابتی هنوز بررسی می‌خواهند.

نام واقعی datastore، UUID، نشانی و اطلاعات ورود خصوصی بمانند. DS-C محل پیشنهادی بر اساس ظرفیت است؛ DS-A و DS-B و حجم‌های سیستم و راه‌اندازی خارج از تخصیص‌اند. سقف سه‌ترابایتی حفظ و فضای آزاد هنگام اجرای تغییر تازه‌سازی شود.

### شرط خصوصیِ باقی‌مانده برای ساخت

CPU/RAM آزاد، بار و رزرو ماشین‌ها، رشد تعهدشدهٔ thin، محل swap، سلامت و تأخیر دیسک، سازگاری VM و ویژگی مهمان، شبکه و بازیابی مجاز، فایل آفلاین و هدف کیفیت و زمان پاسخ بررسی شوند. هر وابستگی محلی، شبکهٔ داخلیِ مجاز یا صرفاً زمان آماده‌سازی باشد.

برای مسیر جدید، ماشین پایش مستقل آماده شود؛ اگر Zabbix مناسب و مجاز موجود است، ابتدا بررسی و همان استفاده شود. مسیر پایه و نسخهٔ API، گروه‌های میزبان، روش امن توکن، خودپایشی، مهمان‌های هدف و سؤال نمونه معلوم شوند. جزئیات خصوصی در مخزن نباشند.

گزارش بخش ۲۶ پذیرفته و نخستین برش قرارداد محلی کامل شده است. پیش از هر عملیات زیرساخت، فقط با شناسایی مجاز و فقط‌خواندنی واقعیت مؤثر همان عملیات روشن شود. مجوز کد 1A به معنی ساخت VM، نصب روی میزبان، دانلود مدل، دسترسی مقصد، وصله، فشار، شبکه یا reboot نیست.

### چیدمان منتخب پس از مجوز

سه ماشین NextOps به‌ترتیب برنامه با ۸ vCPU و ۳۲ GiB و ۲۰۰ GiB، AI با ۲۴ و ۱۲۸ و ۵۰۰، و اتصال فقط‌خواندنی با ۴ و ۸ و ۸۰ آماده شوند. `zabbix-server` با **۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB** پیش از 1C آماده باشد و می‌تواند کنار 1A و 1B ساخته شود. محل پیشنهادی همه DS-C و مجموع **۴ ماشین، ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** است.

ESXi حفظ شود و Ubuntu Server 24.04 LTS مهمان پیشنهادی بماند. Zabbix پایگاه PostgreSQL، رابط Nginx/PHP و Agent 2 خودش را دارد؛ پایگاه NextOps همچنان سرویس مستقلِ محدود در ماشین برنامه است. برای این خروجی، پایگاه NextOps مستقل، اجرای تغییر، آزمایشگاه یا پایش اضافی، مدل دوم یا ماشین به‌ازای اتصال نسازید.

LVM پیشنهادی `vg_zabbix`: بیرون LVM یک GiB برای EFI و دو GiB برای `/boot`؛ داخل آن ریشه ۳۲، `/var` برابر ۱۶، `/var/log` برابر ۸، `/var/lib/postgresql` برابر ۱۱۲ و swap برابر ۴ GiB، با حدود ۲۵ GiB آزاد در VG. فقط دیسک تازه و خالی؛ پیش از ایجاد پایگاه mount بررسی شود. جزئیات هم‌ترازی، مالکیت و رمزگذاری در راهنماست. پیشنهاد history و trends به‌ترتیب ۷ و ۹۰ روز است و باید با تنظیم مؤثر و رشد سنجیده تطبیق داده شود؛ تضمین آماده نیست.

### دیسک و آفلاین

۹۸۰ GiB دیسک به‌علاوهٔ ۱۸۴ GiB سهم موقت swap در ESXi، پیش از سربارهای دیگر **۱۱۶۴ GiB** است. بر اساس فضای آزاد ارسالی و مصرف ثابت، **۲۰۰۲٫۸۷ GiB آزاد** و **۱۱۰۸٫۶۸ GiB بالاتر از حاشیهٔ دقیق 894.1875 GiB** باقی می‌ماند. حاشیه را حدود ۹۰۰ GiB در نظر بگیرید. آزمایشگاه قبلیِ ۱۰۰ GiB یا swap مهمانِ داخل دیسک دوباره شمرده نشود.

پس از جداسازی پایگاه NextOps، مجموع با زبیکس ۵ ماشین، ۴۸ vCPU، حافظهٔ ۲۴۸ GiB و دیسک ۱۲۸۰ GiB است؛ با اصلاح کنترل‌شده، ۶ ماشین، ۵۲ vCPU، حافظهٔ ۲۶۴ GiB و دیسک ۱۳۶۰ GiB. جمع با سهم موقت ESXi swap به‌ترتیب ۱۵۲۸ و ۱۶۲۴ GiB است. ردیف‌ها جایگزین‌اند و تعداد ماشین‌های خود NextOps همچنان ۳، ۴ و ۵ است.

سقف پروژه و همهٔ کنترل‌های هر datastore برقرارند: رشد موجود، swap ماشین خاموش، VMX، snapshot و ادغام، فضای نگهداری و بازیابی و فایل آفلاین خارج از دیسک مهمان. VM ازقبل‌ساخته‌شده دوباره کم نشود. کوچک کردن، حذف، انتقال، پارتیشن‌بندی یا تغییر رزرو حافظه مجاز نشده است. مدل سالم و بازگشت، ممیزی الزامی، هشدار محلی فضا و پشتیبان مستقل حفظ شوند.

### پایان با پاسخ واقعی

**1A:** هویت و دامنه، قرارداد و سیاست، PostgreSQL و مهاجرت، وضعیت ماندگار، ممیزی و رابط/API حداقلی با fixture؛ رد عملیات پیش از توکن واقعی آزموده شود.

**1B:** مدل و محیط CPU محلیِ مجاز، سرویس داخلیِ احرازهویت‌شده، منابع محدود، پاسخ تازهٔ فارسی و انگلیسی و بارگذاری سرد آفلاین.

**وابستگی Zabbix پیش از 1C:** mount و پایگاه، سرویس، رابط/API و شواهد تازه، ورود محلی و reader محدود. خود سرور و مهمان‌های اولیه از مسیر عامل پایشِ مجاز و محدود بررسی شوند؛ به مدل دسترسی گسترده یا اجرای فرمان ندهید.

**1C:** درگاه و فرایند جداشدهٔ اتصال، توکن محدود، خواندن سازگار و محدود، شمارش و زمان قطعی و رد نوشتن و روش نامجاز. فقط runner توکن می‌گیرد؛ نه مدل و مرورگر.

**1D:** سؤال تازه، جمع‌آوری، محاسبه، توضیح CPU، منبع و زمان و دامنه و ممیزی. API، تجهیزات و موتور پایش جدا باشند. خواندن تازه، اندازه‌گیری قدیمی را تازه نمی‌کند؛ متن مخرب رخداد دادهٔ غیرقابل‌اعتماد است.

**1E:** هر چهار ماشین و مرورگر تازه بدون اینترنت و با شبکهٔ داخلی مجاز آزموده شوند. شروع سرد Zabbix و پایگاه و مدل، ورود تازه، لغو توکن، قطع مقصد، دادهٔ قدیمی، کمبود فضا و حدود واقعی سنجیده شوند. ZBX-01 تا ZBX-08 و OFFهای لازم با شاهد قبول شوند؛ fixture، کش، JSON یا داشبورد کافی نیست. بررسی مستقیم Linux مرحلهٔ دو است.

شروع سرویس تابع وابستگی باشد، نه تأخیر ثابت یا تست اینترنت. پایگاه پیش از وابسته بالا بیاید و مدل و درگاه بتوانند مستقل شروع شوند. قطع Zabbix مانع سؤال عمومی محلی با وابستگی سالم نشود. خرابی میزبان هر دو سامانه را قطع می‌کند؛ پشتیبان و بررسی قطعی مستقل نیاز جدا هستند.

پس از هر گام، کار واقعی، نقش ساخته‌شده، نسخه و فرمان و نتیجهٔ آزمون، شکست و اجرا‌نشده و مانع و یک گام بعد در وضعیت پروژه ثبت شوند. Increment 1 فقط کد مخزن محلی را تغییر داد؛ هیچ میزبان، VM، LVM، مدل، Zabbix، شبکه، شروع مجدد یا بازیابی انجام نشد.
