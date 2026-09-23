# Recovery deployment contract / قرارداد استقرار بازیابی

This directory contains only public, non-secret recovery policy. It does not contain a repository
location, access identity, encryption material, or proof of a successful restore. The canonical
input is [`recovery-profile.yaml`](recovery-profile.yaml), validated against
[`recovery-profile.schema.json`](recovery-profile.schema.json) and by
`scripts/check_recovery_profile.py`.

The checked-in profile is intentionally **blocked**. It selects pgBackRest for the two PostgreSQL
16 clusters and restic only for approved non-database files, while refusing to claim production
recovery until the external destination and every restore gate are verified.

## Promotion sequence

1. Approve a destination independent of each serving guest, its datastore, and the serving
   hypervisor. Record only a non-sensitive destination identifier in the public profile.
2. Approve RPO, RTO, retention, restore-test cadence, ownership, and separate key custody.
3. Acquire the selected tool versions in a connected disposable build environment. Verify source,
   license, artifact signature/checksum, dependencies, exact pgBackRest client/repository version
   compatibility, and offline install/remove behavior. Record only SHA-256 values publicly.
4. Create distinct pgBackRest repositories and access identities for the application and Zabbix
   clusters. Do not send PostgreSQL data directories, live database snapshots, or WAL to restic.
5. Test stanza checks, full and differential backups, WAL archiving, retention, repository
   verification, interrupted jobs, corruption, missing WAL, wrong key, and incompatible release.
6. Restore each database and the approved restic file classes into an isolated environment with no
   production route or production credential. Test point-in-time recovery with Internet denied.
7. Verify identity, authorization, session handling, audit continuity, evidence provenance,
   application/Zabbix compatibility, service restart, and cleanup. Record measured RPO/RTO and
   resource use in private evidence, then publish only sanitized results.
8. Set `qualification.qualified: true` only after every public gate is true. CI and release review
   must run `python scripts/check_recovery_profile.py --require-qualified` for production approval.

Normal CI runs the validator without `--require-qualified`; this proves the public contract is
consistent and honest, not that recovery is complete. No serving VM should receive packages or
configuration from this directory before steps 1–3 are approved and a rollback record exists.

## فارسی

<div dir="rtl">

این پوشه فقط سیاست عمومی و بدون راز بازیابی را نگه می‌دارد. نشانی مخزن، هویت دسترسی، مادهٔ
رمزنگاری یا ادعای بازیابی موفق در آن قرار نمی‌گیرد. ورودی مرجع
[`recovery-profile.yaml`](recovery-profile.yaml) است که با
[`recovery-profile.schema.json`](recovery-profile.schema.json) و
`scripts/check_recovery_profile.py` راستی‌آزمایی می‌شود.

پروفایل ثبت‌شده عمداً در وضعیت **مسدود** است. برای دو خوشهٔ PostgreSQL 16، pgBackRest و فقط برای
فایل‌های غیرپایگاهیِ مصوب، restic انتخاب شده است؛ تا مقصد بیرونی و همهٔ آزمون‌های بازیابی تأیید
نشوند، این قرارداد اجازهٔ ادعای آمادگی تولید نمی‌دهد.

### ترتیب ارتقا

1. مقصدی مستقل از مهمان سرویس‌دهنده، datastore آن و hypervisor سرویس‌دهنده تصویب شود. در پروفایل
   عمومی فقط یک شناسهٔ غیرحساس ثبت شود.
2. RPO، RTO، نگه‌داری، تناوب آزمون بازیابی، مالکیت و حضانت جداگانهٔ کلید تصویب شود.
3. نسخه‌های منتخب ابزار در محیط ساخت موقت و متصل دریافت شوند. مبدأ، مجوز، امضا یا checksum،
   وابستگی‌ها، برابری دقیق نسخهٔ pgBackRest در سمت کارخواه و مخزن، و نصب و حذف آفلاین آزموده شود.
   فقط SHA-256 در سند عمومی ثبت شود.
4. برای پایگاه برنامه و Zabbix دو مخزن و هویت دسترسی جدا ساخته شود. پوشهٔ دادهٔ PostgreSQL، snapshot
   زندهٔ پایگاه و WAL نباید به restic سپرده شود.
5. کنترل stanza، پشتیبان کامل و تفاضلی، بایگانی WAL، نگه‌داری، راستی‌آزمایی مخزن و حالت‌های قطع،
   خرابی، WAL مفقود، کلید نادرست و انتشار ناسازگار آزموده شود.
6. هر پایگاه و رده‌های فایل مجاز restic در محیطی جدا، بدون مسیر و اعتبارنامهٔ تولید بازیابی شوند؛
   PITR نیز با اینترنت قطع آزموده شود.
7. هویت، مجوز، نشست، پیوستگی ممیزی، منشأ شاهد، سازگاری برنامه و Zabbix، شروع دوبارهٔ سرویس و
   پاک‌سازی بررسی شود. RPO/RTO و مصرف منابع در شاهد خصوصی ثبت و فقط نتیجهٔ پالایش‌شده منتشر شود.
8. فقط پس از موفقیت همهٔ دروازه‌ها مقدار `qualification.qualified` برابر `true` شود. بازبینی تولید
   باید فرمان `python scripts/check_recovery_profile.py --require-qualified` را اجرا کند.

اجرای عادی CI بدون گزینهٔ `--require-qualified` فقط سازگاری و صداقت قرارداد عمومی را ثابت می‌کند،
نه تکمیل بازیابی را. پیش از تصویب گام‌های ۱ تا ۳ و ثبت مسیر بازگشت، هیچ بسته یا پیکربندی این پوشه
نباید روی VM سرویس‌دهنده اعمال شود.

</div>
