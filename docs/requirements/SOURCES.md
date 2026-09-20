# Source and documentation provenance / مبنای مستندات

Updated: 2026-09-20 — active prompt v3.0.

## English

### Active and preserved specifications

The owner explicitly requested updating the development prompt after supplying additional requirements and host evidence. [NEXTOPS_MASTER_PROMPT.md](NEXTOPS_MASTER_PROMPT.md), version **3.0**, is now the active engineering prompt. It consolidates those decisions and retains the original 26-section engineering organization.

The complete supplied v2.0 prompt, prepared 2026-09-19, is preserved byte-for-byte at [archive/NEXTOPS_MASTER_PROMPT_v2.0.md](archive/NEXTOPS_MASTER_PROMPT_v2.0.md). Its existing Appendix A preserves the original Persian `nextops.txt`, all 51 numbered sections and all eleven integration families. No new translation of either prompt is produced. The original source is not overwritten or reworded inside the archive.

Archive identity: Git blob `d6420b4436907c8a9daa5599dc8e7398b540b280`; SHA-256 `35d7f8be94145bacc53ca4447695abbcab6115b1a3812a087251ddc2850c54c4`. The archive is created using the existing Git blob, not by reconstructing its text.

Read the archive for complete original feature detail, together with the active prompt and [traceability matrix](TRACEABILITY.md). Non-conflicting requirements remain in scope. The active prompt explicitly revises obsolete hardware estimates, Ubuntu-host interpretation, first-answer timing and cloud examples. It does not remove security, audit, integration, testing or recovery requirements. The [prompt changelog](PROMPT_CHANGELOG.md) records the changes and precedence.

### Sources for the revision

The revision uses the owner's instructions and the repository's existing records: [hardware evidence](HARDWARE_BASELINE.json), [storage plan](../STORAGE_PLAN.md), [startup order](../en/START_HERE.md), [server plan](../en/SERVER_PLAN.md), [offline operating contract](../en/OFFLINE_RUNTIME.md), [ESXi supplement](../en/ESXI_BASELINE.md) and [roadmap](../en/ROADMAP.md). Human-facing guides remain paired in English and Persian.

Supplied host evidence establishes reported CPU/RAM totals, ESXi build and point-in-time datastore bytes; it is not a direct agent inspection, current capacity reservation or performance benchmark. The partial CPU sample does not establish a precise marketing SKU or complete per-node distribution. The earlier roughly 90 CPU / 1 TB / sufficient-disk assumptions are historical, not the current planning basis.

VM counts/resources, 24-vCPU AI sizing, DS-C placement, the conservative interpretation of the 3 TB ceiling, the 25% headroom proposal and phased acceptance gates remain documented planning decisions. They are not vendor minimums, measurements, approval to create machines or proof of deployment. No new model selection, dependency upgrade or host change is introduced by v3.

Official references already recorded in the guides support the specifically attributed vendor/library details. This revision is consolidation of supplied sources, not a new external compatibility, security, patch or performance audit. Recheck applicable official versioned documentation when implementation begins, or use verified local reference material during offline work.

Older guide sentences saying the master prompt is unchanged describe their earlier publication state. From this revision onward, that immutability applies to the archived v2 source. The canonical master-prompt path now serves v3.0; source/history claims must not prevent the owner-authorized update. Future prompt changes require explicit versioning and preservation of provenance.

## فارسی

### پرامپت فعال و نسخهٔ محفوظ

مالک پس از ارائهٔ نیازهای تکمیلی و مشخصات میزبان، به‌روزرسانی پرامپت توسعه را صریحاً درخواست کرده است. اکنون [NEXTOPS_MASTER_PROMPT.md](NEXTOPS_MASTER_PROMPT.md) با نسخهٔ **۳.۰** پرامپت فعال پروژه است. این نسخه تصمیم‌های جدید را یکپارچه می‌کند و ساختار ۲۶بخشی سند مهندسی را نگه می‌دارد.

نسخهٔ کامل ۲.۰ با تاریخ آماده‌سازی ۱۹ سپتامبر ۲۰۲۶، بدون تغییر حتی یک بایت در [بایگانی](archive/NEXTOPS_MASTER_PROMPT_v2.0.md) نگهداری می‌شود. پیوست A آن همان متن فارسی اولیهٔ `nextops.txt` با ۵۱ بخش و یازده خانوادهٔ اتصال است. ترجمهٔ تازه‌ای از پرامپت‌ها تهیه نشده و متن منبع داخل بایگانی بازنویسی نشده است.

شناسهٔ Git و SHA-256 بالا هویت نسخهٔ محفوظ را مشخص می‌کنند. برای ساخت بایگانی از همان شیء موجود در Git استفاده شده است، نه از بازسازی دستی متن.

برای جزئیات کامل قابلیت‌های اولیه، بایگانی را در کنار پرامپت فعال و [ماتریس ردیابی](TRACEABILITY.md) بخوانید. نیازهای بدون تعارض همچنان برقرارند. پرامپت فعال فقط برآورد قدیمی سخت‌افزار، برداشت نصب Ubuntu روی میزبان، زمان اولین پاسخ و مثال‌های ابری را صریحاً اصلاح می‌کند؛ الزام امنیت، ممیزی، اتصال‌ها، آزمون و بازیابی حذف نشده است. [تاریخچهٔ پرامپت](PROMPT_CHANGELOG.md) تغییرات و تقدم اسناد را ثبت می‌کند.

### مبنای بازنگری

این بازنگری بر دستورهای مالک و اسناد موجود مخزن استوار است: [رکورد سخت‌افزار](HARDWARE_BASELINE.json)، [برنامهٔ ذخیره‌سازی](../STORAGE_PLAN.md)، [ترتیب شروع](../fa/START_HERE.md)، [برنامهٔ سرورها](../fa/SERVER_PLAN.md)، [الزام آفلاین](../fa/OFFLINE_RUNTIME.md)، [یادداشت ESXi](../fa/ESXI_BASELINE.md) و [نقشهٔ راه](../fa/ROADMAP.md). راهنماهای کاربری و مهندسی همچنان در دو زبان نگهداری می‌شوند.

خروجی ارسالی، مجموع گزارش‌شدهٔ CPU و RAM، نسخهٔ ESXi و ظرفیت لحظه‌ای datastore را نشان می‌دهد؛ نه اتصال مستقیم دستیار، رزرو منابع آزاد یا آزمون کارایی. نمونهٔ ناقص CPU نام تجاری دقیق یا توزیع کامل گره‌ها را مشخص نمی‌کند. عبارت‌های قدیمیِ حدود ۹۰ واحد CPU، یک ترابایت RAM و فضای کافی، سابقهٔ طرح‌اند و مبنای فعلی نیستند.

تعداد و منابع ماشین‌ها، پیشنهاد ۲۴ vCPU برای AI، محل DS-C، تعبیر محافظه‌کارانهٔ سقف سه‌ترابایتی، حاشیهٔ پیشنهادی ۲۵ درصد و معیارهای مرحله‌ای، تصمیم‌های برنامه‌ریزی‌اند؛ نه حداقل تجویزی سازنده، اندازه‌گیری، اجازهٔ ساخت ماشین یا اثبات استقرار. نسخهٔ ۳ مدل تازه‌ای انتخاب نمی‌کند، وابستگی‌ها را ارتقا نمی‌دهد و میزبان را تغییر نمی‌دهد.

ارجاع‌های رسمیِ موجود در راهنماها فقط جزئیات فنیِ منتسب به همان منابع را پشتیبانی می‌کنند. این کار یکپارچه‌سازی منابع ارسالی است، نه ممیزی تازهٔ سازگاری، امنیت، وصله یا کارایی. هنگام پیاده‌سازی، مرجع رسمیِ متناسب با نسخه یا نسخهٔ محلیِ تأییدشدهٔ آن بررسی شود.

عبارت «پرامپت تغییر نکرده است» در راهنماهای قدیمی، وضعیت انتشار همان زمان را توصیف می‌کند. از این بازنگری به بعد، نسخهٔ ثابت همان بایگانی ۲.۰ است و مسیر اصلی، نسخهٔ فعال ۳.۰ را ارائه می‌دهد. این عبارت‌های تاریخی نباید جلوی تغییرِ درخواست‌شدهٔ مالک را بگیرند. تغییر بعدی نیز باید نسخه و مبنای روشن داشته باشد.
