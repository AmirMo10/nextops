# Storage limit and capacity guardrails / محدودیت ذخیره‌سازی و بودجهٔ دیسک

Updated: 2026-09-20. Status: owner requirement plus proposed planning controls; no datastore inspection or configuration change performed.

[English startup](en/START_HERE.md) · [شروع فارسی](fa/START_HERE.md) · [Next task / کار بعدی](NEXT_TASK.md) · [Hardware record / رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json)

## English

### 1. Binding storage constraint

The owner has stated: **only 3 TB of disk space is available for this project/host planning context**. Do not continue treating disk capacity as unlimited or merely "sufficient." This statement does not establish whether the figure is raw disk capacity, RAID-usable capacity, total datastore size or current free space. The unit convention, storage layout and existing consumption remain unverified.

For conservative arithmetic, 3 decimal TB is 3,000,000,000,000 bytes, approximately **2,793.97 GiB / 2.7285 TiB**. This is a conditional unit conversion, not measured datastore capacity. Use the actual usable capacity and free bytes reported by ESXi before approving provisioning. Several datastores must be checked separately, not treated as one interchangeable pool of free space.

This constraint applies to every phase. The existing VM count, CPU/RAM proposals and first offline Zabbix-answer milestone remain unchanged. The archived master prompt is unchanged; this clarification supersedes any earlier assumption of abundant disk space. It is not authorization to shrink, delete, move or reformat existing disks.

### 2. Keep the existing VM budgets, but account for more than VMDKs

| VM | First phase | Planned total virtual disk GiB |
|---|---|---:|
| `nextops-app` | 1 | 200 |
| `nextops-ai` | 1 | 500 |
| `nextops-connectors-ro` | 1 | 80 |
| `nextops-db` | Recommended from 3 | 300 |
| `nextops-executor-rw` | 7, only when enabled | 80 |

These totals include each guest's OS and application/data allowance. The AI disk is a capacity budget, not a required 500-GiB model download. Do not add another full model copy, log budget or guest swap allocation on top if it is already inside these virtual disks.

Broadcom's VM file-layout documentation distinguishes virtual disks from swap, suspend, memory, log and other files [1]. Until actual swap placement, reservation settings and powered-on files are inspected, carry an additional **provisional swap-space allowance equal to the configured guest RAM**. This is a conservative accounting assumption, not measured disk use or a complete overhead ceiling. VMX overhead, snapshots and maintenance workspace must still be accounted for separately. Do not change memory reservations merely to make a disk spreadsheet fit.

| Serving profile | NextOps VMs | VMDK budget GiB | Provisional swap allowance GiB | Subtotal before other overhead GiB |
|---|---:|---:|---:|---:|
| Phases 1–2 | 3 | 780 | 168 | 948 |
| Phases 3–6, separate database | 4 | 1,080 | 232 | 1,312 |
| Phases 7–8, remediation enabled | 5 | 1,160 | 248 | 1,408 |

A Phase 8 read-only deployment can retain the four-VM profile. Existing Zabbix and other VMs are outside these NextOps counts, but consume the same storage budget if they use these datastores. The optional small Zabbix lab adds **100 GiB VMDK plus an 8-GiB provisional swap allowance**, taking the first-stage subtotal to **1,056 GiB**, before other overhead. Full test clones, restore copies, optional observability and imported artifacts outside the VM disks also count. They are not implicitly approved by these totals.

### 3. Headroom and provisioning gate

**Proposed project policy: preserve at least 25% of each relevant datastore's verified usable capacity as free headroom during normal operation.** This is our planning target, not a universal VMware requirement or a guarantee that a particular snapshot/restore will fit. On a hypothetical datastore of exactly 3 decimal TB, the target would be approximately **698.49 GiB**, rounded to **700 GiB** for discussion. Recalculate from actual datastore bytes; do not subtract RAID or filesystem overhead twice.

Approve an operation only when this peak-capacity budget fits:

```text
existing workloads at planned peak
+ NextOps full virtual-disk commitments
+ host/VM file overhead, including swap at its actual location
+ operation-specific snapshot, consolidation, migration or restore workspace
+ offline artifacts outside those virtual disks
+ protected free-space headroom
<= verified usable capacity of the relevant datastore
```

Avoid double-counting files already included in a VM disk or an existing-workload total. Conversely, do not mistake a small current thin-disk footprint for permission to promise all remaining space again: include growth to approved disk sizes. If current free space cannot satisfy the gate, pause the new allocation and review smaller NEW guest disks, retention or an independent storage destination. Do not automatically shrink an existing VMDK or delete evidence.

### 4. Storage controls without breaking offline operation

Keep a small, reviewed local model set: the active model and a verified rollback copy, plus only the embedding model actually needed. Preserve all tokenizer/configuration/runtime dependencies needed for offline cold start. Remove obsolete duplicates only after inventory, validation and explicit retention review; do not remove the only working model to save space. Downloads remain provisioning-only, never an automatic repair step during an outage.

Set bounded retention and size limits for application logs, temporary evidence, caches and build artifacts. Define audit/evidence retention with the operator; required audit records must not be silently discarded when full. Keep Zabbix monitoring history in Zabbix and collect only the scoped evidence needed for an investigation. Maintain local free-space alerts and stop optional ingestion/model imports before they threaten required state or audit writes.

Snapshots are not backups and can continue growing [2]. Do not keep permanent baseline snapshots or assume a percentage of free space makes any snapshot safe. Review the write rate, expected duration and consolidation requirements before creating one. Prefer avoiding memory-inclusive snapshots of the 128-GiB AI guest unless specifically justified and budgeted. Do not cancel consolidation or manually remove snapshot files as an automatic cleanup action.

Keep an independent backup destination reachable through an approved local route or a reviewed offline-media process. A backup directory, backup VM or snapshot on the same G10 does not protect against losing that host. Do not rely on Internet/cloud backup as the only recovery path. Offline restore drills need their own capacity check.

### 5. Next read-only check and acceptance

The next missing evidence is datastore capacity/free space, not another CPU/RAM report. Broadcom documents this read-only listing [3]:

```bash
esxcli storage filesystem list
```

Inspect the VMFS/NFS datastore rows rather than counting boot filesystems as application storage. Review the actual output locally; sanitize datastore names, UUIDs and paths before sharing or committing. A filesystem listing does not prove RAID resilience, IOPS or workload latency.

Before approving Phase 1 provisioning, record verified usable/free bytes, existing commitments, swap placement, the protected margin and peak maintenance needs. Before calling the first release ready, test offline cold start and Zabbix answers with this footprint, log rotation, low-space alerts and controlled low-space failure handling in an isolated test environment. No capacity, restart, model, Zabbix or low-space test has been run by this documentation change.

---

<div dir="rtl">

## فارسی

### ۱. محدودیت قطعی ذخیره‌سازی

مالک اعلام کرده است که **برای برنامه‌ریزی این پروژه و میزبان فقط ۳ ترابایت فضای دیسک در اختیار داریم**. از این پس نباید دیسک را نامحدود یا صرفاً «کافی» فرض کرد. هنوز مشخص نیست این عدد ظرفیت خام دیسک‌ها، ظرفیت قابل‌استفاده پس از RAID، کل datastore یا فضای آزاد فعلی است. شیوهٔ نمایش واحد، چیدمان ذخیره‌سازی و مصرف موجود نیز تأیید نشده‌اند.

اگر منظور ۳ TB ده‌دهی باشد، برابر با ۳٬۰۰۰٬۰۰۰٬۰۰۰٬۰۰۰ بایت، حدود **۲٬۷۹۳٫۹۷ GiB یا ۲٫۷۲۸۵ TiB** است. این فقط تبدیل مشروط واحد است، نه اندازه‌گیری datastore. پیش از تأیید ساخت ماشین‌ها، ظرفیت قابل‌استفاده و فضای آزاد واقعی در ESXi بررسی شوند. چند datastore را نباید یک فضای یکپارچه و قابل‌جایگزینی فرض کرد؛ ظرفیت هرکدام جدا کنترل شود.

این محدودیت دربارهٔ همهٔ مراحل برقرار است. تعداد ماشین‌ها، پیشنهاد CPU و RAM و هدف اولین پاسخ آفلاین دربارهٔ Zabbix تغییر نمی‌کنند. پرامپت بایگانی‌شده دست‌نخورده می‌ماند؛ این توضیح بر فرض قدیمیِ فراوان بودن دیسک مقدم است. این سند مجوز کوچک کردن، حذف، انتقال یا قالب‌بندی دیسک موجود نیست.

### ۲. بودجهٔ ماشین‌ها ثابت می‌ماند؛ مصرف فقط VMDK نیست

| ماشین | زمان نیاز | کل دیسک مجازی پیشنهادی، GiB |
|---|---|---:|
| `nextops-app` | مرحلهٔ یک | ۲۰۰ |
| `nextops-ai` | مرحلهٔ یک | ۵۰۰ |
| `nextops-connectors-ro` | مرحلهٔ یک | ۸۰ |
| `nextops-db` | ترجیحاً از مرحلهٔ سه | ۳۰۰ |
| `nextops-executor-rw` | مرحلهٔ هفت، فقط در صورت فعال شدن | ۸۰ |

این اعداد فضای سیستم‌عامل مهمان و سهم برنامه یا داده را در بر می‌گیرند. دیسک ۵۰۰ GiB ماشین AI به معنای نیاز به دانلود مدل ۵۰۰ گیگابایتی نیست. اگر فایل مدل، لاگ یا swap مهمان داخل همین دیسک‌هاست، آن را دوباره به جمع datastore اضافه نکنید.

مستندات Broadcom، فایل‌های دیسک مجازی را از swap، فایل حالت تعلیق، حافظه، لاگ و سایر فایل‌ها جدا می‌کند [1]. تا زمانی که محل swap، تنظیمات رزرو حافظه و فایل‌های ماشین روشن بررسی نشده‌اند، **به‌اندازهٔ RAM تخصیص‌یافتهٔ مهمان‌ها یک سهم موقت برای swap** در نظر بگیرید. این فرض محافظه‌کارانهٔ حسابداری است؛ نه مصرف اندازه‌گیری‌شده و نه سقف همهٔ سربارها. سربار VMX، snapshot و فضای موقت عملیات همچنان جدا حساب شوند. صرفاً برای جا شدن اعداد در بودجهٔ دیسک، رزرو حافظه را تغییر ندهید.

| چیدمان سرویس‌دهی | تعداد ماشین NextOps | بودجهٔ VMDK، GiB | سهم موقت swap، GiB | جمع پیش از سایر سربارها، GiB |
|---|---:|---:|---:|---:|
| مراحل یک و دو | ۳ | ۷۸۰ | ۱۶۸ | ۹۴۸ |
| مراحل سه تا شش، با پایگاه جدا | ۴ | ۱٬۰۸۰ | ۲۳۲ | ۱٬۳۱۲ |
| مراحل هفت و هشت، با اصلاح فعال | ۵ | ۱٬۱۶۰ | ۲۴۸ | ۱٬۴۰۸ |

استقرار فقط‌خواندنی در مرحلهٔ هشت می‌تواند چهارماشینی بماند. Zabbix موجود و سایر ماشین‌ها در تعداد NextOps نیستند، اما اگر از همین datastore استفاده کنند، مصرف آن‌ها هم جزو همان محدودیت است. نمونهٔ کوچک و اختیاری Zabbix آزمایشگاهی، **۱۰۰ GiB دیسک و ۸ GiB سهم موقت swap** اضافه می‌کند؛ جمع مرحلهٔ اول با آن، پیش از سایر سربارها، **۱٬۰۵۶ GiB** می‌شود. نسخهٔ کامل آزمون، محل بازیابی آزمایشی، پایش اختیاری و فایل‌های واردشدهٔ بیرون از دیسک مهمان نیز باید حساب شوند. این جدول به معنای تأیید خودکار آن‌ها نیست.

### ۳. حاشیهٔ آزاد و شرط تخصیص

**سیاست پیشنهادی پروژه: در کارکرد عادی دست‌کم ۲۵ درصد ظرفیت قابل‌استفادهٔ هر datastore مرتبط آزاد بماند.** این هدف برنامه‌ریزی ماست، نه الزام همگانی VMware یا تضمین جا شدن هر عملیات snapshot و بازیابی. برای datastore فرضی با ظرفیت دقیقاً ۳ TB ده‌دهی، این حاشیه حدود **۶۹۸٫۴۹ GiB** است که برای توضیح آن را **۷۰۰ GiB** در نظر می‌گیریم. محاسبهٔ نهایی از بایت واقعی datastore انجام شود؛ سربار RAID یا فایل‌سیستم دوبار کم نشود.

پیش از تأیید هر عملیات، مجموع مصرف اوجِ بارهای موجود، کل ظرفیت تعهدشدهٔ دیسک‌های NextOps، فایل‌های سربار و swap در محل واقعی، فضای موقت snapshot و ادغام و انتقال و بازیابی، فایل‌های آفلاین خارج از دیسک مهمان و حاشیهٔ آزاد باید در ظرفیت قابل‌استفادهٔ همان datastore جا شود.

فایل داخل دیسک مهمان یا مصرفی که قبلاً در جمع بار موجود آمده است دوباره شمرده نشود. در مقابل، کم بودن مصرف فعلیِ دیسک thin نباید مجوز تعهد دوبارهٔ همان فضای آزاد باشد؛ رشد تا سقف مصوب نیز حساب شود. اگر فضای آزاد از این شرط کمتر است، تخصیص تازه متوقف و دیسک کوچک‌تر برای ماشین جدید، سیاست نگهداری یا مقصد ذخیره‌سازی مستقل بررسی شود. دیسک موجود خودکار کوچک و شواهد حذف نشوند.

### ۴. کنترل مصرف بدون آسیب به کارکرد آفلاین

مجموعهٔ مدل محلی محدود و بازبینی‌شده باشد: مدل فعال و نسخهٔ تأییدشدهٔ بازگشت، همراه فقط مدل بردارسازیِ موردنیاز. tokenizer، تنظیمات و وابستگی‌های لازم برای شروع آفلاین حفظ شوند. نسخه‌های تکراری و منسوخ فقط پس از بررسی موجودی، اعتبارسنجی و سیاست نگهداری حذف شوند؛ تنها مدل سالم برای آزاد کردن فضا حذف نشود. دانلود فقط در آماده‌سازی مجاز است، نه به‌عنوان راه‌حل خودکار هنگام قطعی اینترنت.

برای لاگ برنامه، شواهد موقت، حافظهٔ نهان و خروجی ساخت، سقف حجم و دورهٔ نگهداری تعیین شود. نگهداری ممیزی و شواهد با مسئول سامانه مشخص شود؛ پر شدن دیسک نباید باعث حذف بی‌سروصدای سوابق الزامی شود. تاریخچهٔ پایش در خود Zabbix بماند و فقط شواهد محدودِ لازم برای هر بررسی جمع‌آوری شوند. هشدار فضای آزاد محلی باشد و ورود اسناد اختیاری یا مدل تازه پیش از تهدید داده و ممیزی متوقف شود.

snapshot نسخهٔ پشتیبان نیست و می‌تواند پیوسته رشد کند [2]. snapshot دائمی برای وضعیت اولیه نگه ندارید و فرض نکنید وجود درصدی فضای آزاد هر snapshot را ایمن می‌کند. پیش از ساخت آن، نرخ تغییر داده، مدت نگهداری و فضای لازم برای ادغام بررسی شود. snapshot شامل حافظه برای ماشین AI دارای ۱۲۸ GiB RAM، جز با نیاز مشخص و بودجهٔ جدا، انجام نشود. لغو ادغام یا حذف دستی فایل snapshot راه‌حل خودکار پاک‌سازی نیست.

مقصد پشتیبان مستقل، با مسیر محلی مجاز یا فرایند بازبینی‌شدهٔ رسانهٔ آفلاین، لازم است. پوشهٔ پشتیبان، VM پشتیبان یا snapshot روی همان G10 از خرابی خود میزبان محافظت نمی‌کند. تنها راه بازیابی نباید اینترنت یا فضای ابری باشد. تمرین بازیابی آفلاین نیز بررسی ظرفیت جدا می‌خواهد.

### ۵. بررسی بعدی و معیار پذیرش

اطلاعات باقی‌مانده، ظرفیت و فضای آزاد datastore است؛ نه تکرار گزارش CPU و RAM. فرمان فقط‌خواندنی زیر در مرجع Broadcom آمده است [3]:

</div>

```bash
esxcli storage filesystem list
```

<div dir="rtl">

ردیف‌های datastore از نوع VMFS یا NFS بررسی شوند؛ فایل‌سیستم راه‌اندازی، فضای برنامه تلقی نشود. خروجی ابتدا محلی بازبینی و پیش از اشتراک یا ثبت در مخزن، نام‌ها، UUIDها و مسیرهای خصوصی پالایش شوند. این فهرست، تاب‌آوری RAID، IOPS یا تأخیر زیر بار را ثابت نمی‌کند.

پیش از ساخت ماشین‌های مرحلهٔ یک، بایت قابل‌استفاده و آزاد، تعهدهای موجود، محل swap، حاشیهٔ محافظت‌شده و فضای اوج عملیات ثبت شوند. پیش از اعلام آمادگی نسخهٔ اول، شروع آفلاین و پاسخ Zabbix با همین چیدمان، چرخش لاگ، هشدار کمبود فضا و رفتار کنترل‌شده در فضای کم، در محیط آزمون جدا بررسی شوند. در این تغییر مستندات هیچ آزمون ظرفیت، شروع مجدد، مدل، Zabbix یا کمبود دیسک اجرا نشده است.

</div>

## References / منابع

The owner statement supplies the 3-TB constraint. Numbers and headroom targets are project calculations/proposals, not vendor minimums. The references support only the file categories, snapshot behavior and read-only command. Consulted 2026-09-20.

[1]: https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/vim.vm.FileLayoutEx.html
[2]: https://knowledge.broadcom.com/external/article/318825
[3]: https://developer.broadcom.com/xapis/esxcli-command-reference/latest/namespace/esxcli_storage.html
