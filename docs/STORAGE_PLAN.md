# Storage evidence and capacity guardrails / شواهد ذخیره‌سازی و بودجهٔ دیسک

Updated: 2026-09-20. Source: owner-supplied `esxcli storage filesystem list` output. Capture time is unknown; no direct host access or configuration change was performed.

[English startup](en/START_HERE.md) · [شروع فارسی](fa/START_HERE.md) · [Next task / کار بعدی](NEXT_TASK.md) · [Hardware record / رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json)

## English

### 1. What the supplied listing establishes

The owner has now supplied the requested filesystem listing. Capacity and free-space values are no longer entirely unknown: they have point-in-time, owner-supplied evidence. They are not a live reservation, independent host inspection, or a measurement of future growth or performance. Public documentation uses aliases ordered by increasing capacity; actual volume names, UUIDs and mount paths are intentionally omitted. Keep that mapping in private deployment inventory.

All three rows below were reported mounted and of type `VMFS-6`. Calculations use 1 GiB = 1,073,741,824 bytes; used space is Size minus Free. Use numeric fields, not capacity-like volume names.

| Public alias | Reported size, bytes | Reported free, bytes | Total GiB | Used GiB | Free GiB |
|---|---:|---:|---:|---:|---:|
| DS-A — smallest VMFS datastore | 160792838144 | 159276597248 | 149.75 | 1.41 | 148.34 |
| DS-B — middle VMFS datastore | 1199906488320 | 1191717109760 | 1117.50 | 7.63 | 1109.87 |
| DS-C — largest VMFS datastore | 3840506068992 | 3400400896000 | 3576.75 | 409.88 | 3166.87 |

The VMFS rows sum to 4,844.00 GiB total and 4,425.08 GiB free at the reported observation. This is an inventory sum, NOT one pooled datastore or permission to allocate all of it. The listing also contains a `VMFSOS` system volume and two `vfat` boot volumes. Exclude those system/boot rows from the NextOps budget and leave them untouched. A filesystem listing includes more than application datastores [1].

**The owner's earlier 3 TB limit remains the project planning ceiling.** The new evidence shows that DS-C alone reports about 3.8405 decimal TB total and 3.4004 decimal TB free; it does not automatically expand the project budget or allocate DS-A/DS-B. The meaning of the earlier rounded statement has not been retroactively reinterpreted. Continue using 3 decimal TB (2,793.97 GiB) as the conservative project ceiling until the owner changes it; this is a planning convention, not the measured datastore size.

### 2. Proposed initial placement: all three NextOps VMs on DS-C

This is a capacity-based starting proposal, not a claim that DS-C is the fastest or most resilient storage. Confirm operational ownership, existing growth commitments and storage health before provisioning. Keep other datastores out of the baseline; no migration or repartitioning is needed merely to make this plan fit.

| Creation order | VM | vCPU | RAM GiB | Total virtual disk GiB | Proposed datastore |
|---|---|---:|---:|---:|---|
| 1 | `nextops-app` | 8 | 32 | 200 | DS-C |
| 2 | `nextops-ai` | 24 | 128 | 500 | DS-C |
| 3 | `nextops-connectors-ro` | 4 | 8 | 80 | DS-C |
| Total | 3 NextOps VMs | 36 | 168 | 780 | DS-C |

These disk budgets include each guest's OS, application and data allowance. The AI disk is not a required 500-GiB model download. Files inside a guest disk, including guest swap, must not be counted again as separate datastore consumption. Separate OS/data virtual disks are possible within the same total, not in addition to it.

VM files outside VMDKs include swap and other overhead [2]. Until actual memory reservations, swap placement and powered-on file sizes are reviewed, carry a provisional ESXi swap allowance equal to configured guest RAM. This is an accounting assumption, not measured usage or a complete overhead ceiling. Do not change memory reservations simply to reduce a displayed disk total. The baseline assumes these files are on DS-C; if actual placement differs, charge each datastore separately.

Reuse existing authorized LAN Zabbix. If no suitable instance exists, one approved small `zabbix-lab` adds 100 GiB virtual disk and 8 GiB provisional swap allowance on its selected datastore. It is optional, not a duplicate of an existing monitoring deployment. Existing Zabbix and other VMs must still be counted in shared datastore consumption.

### 3. Recalculate the free-space target from actual datastore size

**Project proposal: keep at least 25% of each relevant datastore's usable capacity free in normal operation.** This is not a universal VMware requirement, a configured reservation or a guarantee that any snapshot/restore fits.

For DS-C, use the supplied Size value, not the old rounded 3 TB assumption:

- Total: 3,576.75 GiB.
- Current reported free space: 3,166.8701171875 GiB.
- Exact 25% target: **894.1875 GiB**, approximately **900 GiB** for a conservative operational target.
- Free space above the exact target: **2,272.6826171875 GiB**, BEFORE unaccounted commitments or operational workspace.

The previous approximately 700-GiB example was for a hypothetical 3-decimal-TB datastore; it is not the correct 25% target for DS-C. Both the project ceiling and the per-datastore free-space target must be respected; neither authorizes consuming all residual space.

### 4. Phase budgets against DS-C

The following are separate alternative serving profiles, not amounts to add together. Calculations assume each profile is newly allocated, all its virtual disks and provisional swap are on DS-C, and existing usage stays unchanged. If any NextOps VM already exists, reconcile its allocation first instead of subtracting it twice. Capacity is not reserved by this table.

| Profile | VMs | VMDK GiB | Provisional swap GiB | Subtotal GiB | DS-C free after subtotal, GiB | Remaining above exact 25% target, GiB |
|---|---:|---:|---:|---:|---:|---:|
| Phases 1–2 | 3 | 780 | 168 | 948 | 2218.87 | 1324.68 |
| Phase 1 plus optional lab Zabbix | 4 | 880 | 176 | 1056 | 2110.87 | 1216.68 |
| Phases 3–6, separate database | 4 | 1080 | 232 | 1312 | 1854.87 | 960.68 |
| Phases 7–8, remediation enabled | 5 | 1160 | 248 | 1408 | 1758.87 | 864.68 |

A read-only Phase 8 may retain four VMs. The later 300-GiB database and 80-GiB write-executor disks are unchanged; CPU/RAM remain as in SERVER_PLAN. No additional application VM is justified just by discovering another datastore.

**The remaining column is not approved spare capacity.** Subtract existing thin-disk growth, missing swap for powered-off VMs, VMX/other file overhead, snapshots and consolidation workspace, migration/restore peaks, templates/test clones, and offline artifacts outside guest disks before approving an operation. Do not assume thin disks create physical capacity or that present low usage covers their full commitments.

Use this incremental gate for each datastore:

```text
new allocations at their approved peak
+ existing commitments not already included in current used bytes
+ additional VM/host overhead at its actual location
+ operation-specific maintenance and restore workspace
+ externally staged artifacts not already counted inside guest disks
<= current reported free bytes - protected free-space target
```

Separately check total NextOps-attributed commitments against the retained 3 TB project ceiling. Current Free already subtracts existing used files; do not subtract those again. Recheck free capacity at the actual change window, not because the earlier evidence was missing. If the gate fails, review smaller NEW disks, retention or an independently approved storage destination. Do not automatically shrink, delete, move or reformat existing disks.

### 5. What remains unknown and what must stay local

DS-A and DS-B remain unallocated by this plan. Their apparent spare space does not establish SSD/HDD type, independent RAID groups, controller separation, IOPS, health or failure isolation. DS-C selection is based on reported capacity only. A second datastore on the same G10 is not an off-host backup. An independent approved LAN backup destination or controlled offline-media process remains necessary for host-loss recovery.

Keep a small verified local model set: active model, required rollback artifacts, and only the embedding model actually enabled. Preserve tokenizer/configuration/runtime files needed for offline cold start. Obsolete copies may be removed only after inventory and retention review; never delete the only working model and rely on a download during an outage.

Set log/cache/build-artifact limits and approved evidence/audit retention. Keep bulk monitoring history in Zabbix. Use local free-space alarms and pause optional ingestion/model imports before required state or audit writes fail. Do not silently discard mandatory audit records. Test low-space handling in an isolated environment; do not deliberately fill the production datastore.

Snapshots are not backups, can grow, and require their own change-rate/duration/consolidation budget [3]. Avoid permanent snapshots and unbudgeted memory-inclusive snapshots of the 128-GiB AI guest. Do not cancel consolidation or manually delete snapshot files as automatic cleanup. A full test clone or restore copy needs a fresh peak-capacity check; the table does not preapprove one.

The filesystem listing has been supplied; do not ask for the same missing observation again. Remaining preflight items are existing VM commitments and swap locations, backing-device/RAID health and workload latency, operational ownership and fresh capacity at execution time. No such checks, VM creation, storage moves, performance benchmarks or offline acceptance tests have been performed here.

Phase 1 still ends with a new authorized Zabbix-status question answered by local CPU AI with Internet blocked, source/time references and audit. Storage changes must not introduce a cloud dependency. The archived master prompt remains unchanged. Numeric conversions and profile sums were recalculated from the supplied byte values; those calculations are not a production readiness test.

---

<div dir="rtl">

## فارسی

### ۱. خروجی ارسالی چه چیزی را مشخص می‌کند؟

مالک اکنون خروجی درخواستیِ `esxcli storage filesystem list` را فرستاده است. ظرفیت و فضای آزاد دیگر کاملاً نامشخص نیستند؛ برای لحظهٔ ثبت خروجی، شاهد ارسالی داریم. این شاهد، رزرو زندهٔ فضا، بررسی مستقل میزبان یا سنجش رشد آینده و کارایی نیست. در مخزن عمومی، از نام‌های مستعار به‌ترتیب ظرفیت استفاده شده و نام واقعی حجم‌ها، UUID و مسیرها حذف شده‌اند. نگاشت نام‌ها در فهرست خصوصی استقرار بماند.

هر سه ردیف زیر در خروجی، متصل و از نوع `VMFS-6` هستند. هر GiB برابر ۱٬۰۷۳٬۷۴۱٬۸۲۴ بایت است. مصرف از تفاضل Size و Free محاسبه شده؛ نام حجم معیار ظرفیت نیست.

| نام مستعار | ظرفیت کل، GiB | مصرف‌شده، GiB | فضای آزاد، GiB |
|---|---:|---:|---:|
| DS-A؛ کوچک‌ترین datastore | ۱۴۹٫۷۵ | ۱٫۴۱ | ۱۴۸٫۳۴ |
| DS-B؛ datastore میانی | ۱٬۱۱۷٫۵۰ | ۷٫۶۳ | ۱٬۱۰۹٫۸۷ |
| DS-C؛ بزرگ‌ترین datastore | ۳٬۵۷۶٫۷۵ | ۴۰۹٫۸۸ | ۳٬۱۶۶٫۸۷ |

اعداد دقیق بایت در جدول انگلیسی و رکورد سخت‌افزار ثبت شده‌اند. جمع سه ردیف VMFS، ظرفیت ۴٬۸۴۴٫۰۰ GiB و فضای آزاد ۴٬۴۲۵٫۰۸ GiB است. این فقط جمع موجودی است؛ نه یک datastore یکپارچه و نه مجوز استفاده از همهٔ آن. ردیف `VMFSOS` و دو ردیف راه‌اندازی از نوع `vfat` در بودجهٔ NextOps حساب نمی‌شوند و دست‌نخورده می‌مانند. فرمان فهرست فایل‌سیستم، فقط datastoreهای برنامه را نشان نمی‌دهد [1].

**سقف قبلیِ ۳ ترابایت برای برنامه‌ریزی پروژه حفظ می‌شود.** خروجی تازه برای DS-C حدود ۳٫۸۴۰۵ TB ظرفیت و ۳٫۴۰۰۴ TB فضای آزاد ده‌دهی نشان می‌دهد؛ این اطلاعات خودبه‌خود بودجهٔ پروژه را افزایش نمی‌دهد و DS-A یا DS-B را به پروژه اختصاص نمی‌دهد. معنای جملهٔ گرد‌شدهٔ قبلی نیز بدون تأیید مالک بازتفسیر نمی‌شود. تا تغییر صریح بودجه، ۳ TB ده‌دهی، برابر حدود ۲٬۷۹۳٫۹۷ GiB، سقف محافظه‌کارانهٔ برنامه‌ریزی است؛ نه اندازهٔ واقعی datastore.

### ۲. پیشنهاد شروع: هر سه ماشین روی DS-C

این انتخاب بر پایهٔ ظرفیت است، نه ادعای سریع‌تر یا مقاوم‌تر بودن DS-C. پیش از ساخت، اختیار استفاده، تعهد رشد ماشین‌های موجود و سلامت ذخیره‌سازی بررسی شوند. دو datastore دیگر در طرح پایه استفاده نمی‌شوند. صرفاً برای جا شدن این چیدمان، انتقال داده یا پارتیشن‌بندی دوباره لازم نیست.

| ترتیب ساخت | ماشین | vCPU | حافظه، GiB | کل دیسک مجازی، GiB | محل پیشنهادی |
|---|---|---:|---:|---:|---|
| ۱ | `nextops-app` | ۸ | ۳۲ | ۲۰۰ | DS-C |
| ۲ | `nextops-ai` | ۲۴ | ۱۲۸ | ۵۰۰ | DS-C |
| ۳ | `nextops-connectors-ro` | ۴ | ۸ | ۸۰ | DS-C |
| مجموع | ۳ ماشین NextOps | ۳۶ | ۱۶۸ | ۷۸۰ | DS-C |

این دیسک‌ها سهم سیستم‌عامل، برنامه و دادهٔ مهمان را شامل می‌شوند. دیسک AI به معنای دانلود مدل ۵۰۰ GiB نیست. فایل‌های داخل دیسک مهمان، از جمله swap خود Linux، دوباره در مصرف datastore شمرده نشوند. تقسیم دیسک سیستم‌عامل و داده مجاز است، اما مجموع آن‌ها باید در همین بودجه بماند.

فایل‌های بیرون VMDK، از جمله swap و سایر سربارها، جدا هستند [2]. تا بررسی رزرو حافظه، محل swap و اندازهٔ فایل‌های ماشین روشن، به‌اندازهٔ RAM مهمان‌ها سهم موقت برای swap در ESXi در نظر بگیرید. این فرض حسابداری است، نه مصرف اندازه‌گیری‌شده یا سقف همهٔ سربارها. صرفاً برای کوچک شدن عدد دیسک، رزرو حافظه را تغییر ندهید. محاسبهٔ پایه، این فایل‌ها را روی DS-C فرض می‌کند؛ اگر جای دیگری باشند، مصرف همان datastore جدا حساب شود.

Zabbix موجود و مجاز شبکهٔ داخلی دوباره ساخته نشود. فقط در نبود نمونهٔ مناسب، یک `zabbix-lab` کوچک و مصوب، ۱۰۰ GiB دیسک و ۸ GiB سهم موقت swap به datastore انتخابی اضافه می‌کند. مصرف Zabbix و VMهای موجود نیز در بودجهٔ مشترک ذخیره‌سازی لحاظ شود.

### ۳. حاشیهٔ آزاد بر مبنای ظرفیت واقعی محاسبه می‌شود

**پیشنهاد پروژه: در کارکرد عادی دست‌کم ۲۵ درصد ظرفیت قابل‌استفادهٔ هر datastore مرتبط آزاد بماند.** این عدد الزام عمومی VMware، رزرو اعمال‌شده یا تضمین جا شدن هر snapshot و بازیابی نیست.

برای DS-C، ظرفیت ۳٬۵۷۶٫۷۵ GiB و فضای آزاد ۳٬۱۶۶٫۸۷۰۱ GiB گزارش شده است. حاشیهٔ دقیق ۲۵ درصد **۸۹۴٫۱۸۷۵ GiB** است؛ در کار عملی می‌توان آن را محافظه‌کارانه **حدود ۹۰۰ GiB** در نظر گرفت. پیش از کم کردن تعهدهای حساب‌نشده و فضای موقت عملیات، **۲٬۲۷۲٫۶۸۲۶ GiB** بالاتر از این حاشیه باقی می‌ماند.

مثال قبلیِ حدود ۷۰۰ GiB مربوط به datastore فرضیِ دقیقاً سه‌ترابایتی بود و دیگر عدد درستِ ۲۵ درصد برای DS-C نیست. سقف پروژه و حاشیهٔ آزاد هر datastore هم‌زمان رعایت شوند؛ هیچ‌کدام اجازهٔ مصرف همهٔ باقیمانده نیستند.

### ۴. بودجهٔ مراحل روی DS-C

هر ردیف یک چیدمان جایگزین است؛ ردیف‌ها با هم جمع نمی‌شوند. فرض محاسبه این است که همهٔ ماشین‌های آن چیدمان تازه ساخته شوند، دیسک و سهم موقت swap آن‌ها روی DS-C باشد و مصرف فعلی تغییر نکند. اگر ماشینی از NextOps قبلاً ساخته شده، ابتدا مصرف آن تطبیق داده شود تا دوبار کم نشود. این جدول فضا را رزرو نمی‌کند.

| چیدمان | ماشین | دیسک، GiB | سهم موقت swap، GiB | جمع، GiB | فضای آزاد پس از جمع، GiB | باقیمانده بالاتر از حاشیهٔ دقیق ۲۵ درصد، GiB |
|---|---:|---:|---:|---:|---:|---:|
| مراحل یک و دو | ۳ | ۷۸۰ | ۱۶۸ | ۹۴۸ | ۲٬۲۱۸٫۸۷ | ۱٬۳۲۴٫۶۸ |
| مرحلهٔ یک با Zabbix آزمایشگاهی اختیاری | ۴ | ۸۸۰ | ۱۷۶ | ۱٬۰۵۶ | ۲٬۱۱۰٫۸۷ | ۱٬۲۱۶٫۶۸ |
| مراحل سه تا شش؛ پایگاه جدا | ۴ | ۱٬۰۸۰ | ۲۳۲ | ۱٬۳۱۲ | ۱٬۸۵۴٫۸۷ | ۹۶۰٫۶۸ |
| مراحل هفت و هشت؛ اصلاح فعال | ۵ | ۱٬۱۶۰ | ۲۴۸ | ۱٬۴۰۸ | ۱٬۷۵۸٫۸۷ | ۸۶۴٫۶۸ |

مرحلهٔ هشت فقط‌خواندنی می‌تواند چهارماشینی بماند. دیسک ۳۰۰ GiB پایگاه آینده و ۸۰ GiB اجرای تغییر و منابع CPU/RAM طبق SERVER_PLAN ثابت‌اند. پیدا شدن datastore دیگر به‌تنهایی دلیل اضافه کردن ماشین برنامه نیست.

**ستون باقیمانده، فضای آزادِ مجاز برای خرج کردن نیست.** ابتدا رشد تعهدشدهٔ دیسک‌های thin موجود، swap ماشین‌های خاموش، سربار VMX و فایل‌ها، snapshot و ادغام، اوج انتقال و بازیابی، قالب‌ها و نسخه‌های آزمون و فایل‌های آفلاینِ بیرون از مهمان کم شوند. کم بودن مصرف فعلیِ thin به معنای ایجاد ظرفیت فیزیکی یا پوشش کامل تعهدها نیست.

برای هر datastore، مجموع تخصیص تازه در اوج، تعهد رشد موجود که در مصرف فعلی نیست، سربار اضافی در محل واقعی، فضای موقت عملیات و فایل‌های آماده‌سازیِ حساب‌نشده باید از «فضای آزاد فعلی منهای حاشیهٔ محافظت‌شده» کمتر باشد. جداگانه، کل تعهد منتسب به NextOps با سقف سه‌ترابایتی مقایسه شود. Free از قبل مصرف موجود را کم کرده است؛ آن مصرف را دوباره کم نکنید.

در زمان واقعی تغییر، تازگی فضای آزاد بررسی شود؛ نه با این فرض که خروجی قبلی هنوز ارسال نشده است. در صورت کافی نبودن بودجه، دیسک کوچک‌تر برای ماشین تازه، سیاست نگهداری یا مقصد مستقلِ دارای مجوز بررسی شود. دیسک موجود خودکار کوچک، حذف، منتقل یا فرمت نشود.

### ۵. مجهول‌های باقی‌مانده و الزامات آفلاین

DS-A و DS-B در این طرح تخصیص نمی‌گیرند. فضای آزاد آن‌ها نوع SSD/HDD، استقلال RAID یا کنترلر، IOPS، سلامت یا جدایی دامنهٔ خرابی را ثابت نمی‌کند. انتخاب DS-C فقط بر ظرفیت گزارش‌شده متکی است. datastore دوم روی همان G10، پشتیبان بیرون از میزبان نیست. برای بازیابی پس از خرابی میزبان، مقصد مستقل شبکهٔ داخلی یا فرایند رسانهٔ آفلاینِ بازبینی‌شده همچنان لازم است.

مجموعهٔ محلی مدل‌ها محدود و تأییدشده باشد: مدل فعال، فایل‌های لازم بازگشت و فقط مدل بردارسازیِ فعال. tokenizer، تنظیمات و محیط اجرای لازم برای شروع آفلاین حفظ شوند. نسخهٔ منسوخ فقط پس از بررسی موجودی و سیاست نگهداری حذف شود؛ تنها مدل سالم حذف نشود تا هنگام قطع اینترنت به دانلود وابسته بمانیم.

حجم لاگ، کش و خروجی ساخت محدود و نگهداری شواهد و ممیزی مصوب باشد. تاریخچهٔ حجیم پایش در Zabbix بماند. هشدار کمبود فضا محلی باشد و ورود اسناد یا مدل اختیاری پیش از اختلال در داده و ممیزی متوقف شود. سوابق الزامی بی‌سروصدا حذف نشوند. رفتار فضای کم در محیط جدا آزموده شود، نه با پر کردن عمدی datastore عملیاتی.

snapshot پشتیبان نیست، رشد می‌کند و بودجهٔ جدا برای نرخ تغییر، مدت و ادغام می‌خواهد [3]. snapshot دائمی و snapshot شامل حافظهٔ ۱۲۸ GiB ماشین AI بدون بودجه نگه ندارید. ادغام لغو و فایل snapshot به‌عنوان پاک‌سازی خودکار دستی حذف نشود. نسخهٔ کامل آزمون یا بازیابی آزمایشی بررسی اوج ظرفیت تازه می‌خواهد؛ جدول آن را از پیش تأیید نکرده است.

فهرست فایل‌سیستم دریافت شده و نباید دوباره به‌عنوان اطلاعات ارسال‌نشده خواسته شود. پیش‌نیازهای باقی‌مانده، تعهد VMها و محل swap، سلامت دیسک و RAID، تأخیر زیر بار، اختیار استفاده و تازگی ظرفیت هنگام اجرا هستند. اینجا هیچ‌کدام از این بررسی‌های زنده، ساخت یا انتقال VM، سنجش کارایی و آزمون پذیرش آفلاین انجام نشده‌اند.

پایان مرحلهٔ یک همچنان پاسخ محلی CPU به سؤال تازه دربارهٔ وضعیت مجاز Zabbix، با اینترنت قطع، منبع، زمان و ممیزی است. تصمیم ذخیره‌سازی نباید وابستگی ابری ایجاد کند. پرامپت بایگانی‌شده تغییر نکرده است. تبدیل واحد و جمع بودجه‌ها از بایت‌های ارسالی دوباره محاسبه شده‌اند؛ این محاسبه آزمون آمادگی بهره‌برداری نیست.

</div>

## References / منابع

Owner-supplied byte values are the source for capacity calculations. The following official references support only filesystem-listing scope, VM file categories and snapshot behavior; they do not verify host capacity, performance or readiness. Consulted 2026-09-20.

[1]: https://developer.broadcom.com/xapis/esxcli-command-reference/latest/namespace/esxcli_storage.html
[2]: https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/vim.vm.FileLayoutEx.FileType.html
[3]: https://knowledge.broadcom.com/external/article/318825
