# ADR 0008 — Independent recovery repositories / مخزن‌های مستقل بازیابی

Status: **proposed; repository policy implemented; infrastructure decision blocked on an approved
independent destination, recovery objectives, and key custody.** Date: 2026-09-23.

## English

### Context

NextOps has two separate PostgreSQL 16 clusters, immutable application/model releases, protected
configuration, documentation, manifests, and permitted evidence. Logical dumps of both databases
have restored successfully into isolated socket-only clusters, but all serving workloads remain in
one G10 failure domain and no independently stored WAL-aware recovery set exists. Filesystem copies
cannot prove database consistency or point-in-time recovery, and a second directory, VM, or
datastore-visible copy on the same serving host does not survive the declared disaster.

### Decision

Use pgBackRest as the PostgreSQL-aware candidate for both databases, with distinct repository IDs,
access identities, policies, evidence, and restore procedures for the application and Zabbix. Use
full plus justified differential backups, continuous WAL archiving, retention, repository checks,
and isolated point-in-time restore tests. The repository host or service must be independent of the
serving guest, datastore, and hypervisor.

Use restic only for explicitly approved non-database classes: release artifacts, manifests,
documentation, approved configuration, and permitted evidence. PostgreSQL data directories, live
database snapshots, and WAL are forbidden restic inputs. Recovery keys and access material remain
outside Git and use custody separate from ordinary backup operation.

The current evaluation candidates are pgBackRest 2.59.1 (MIT) and restic 0.19.1 (BSD-2-Clause).
They are selections for controlled offline-bundle qualification, not installed production
dependencies. Exact artifacts, SHA-256 values, dependency/license approval, and offline
installation remain gates. The public profile under `deploy/recovery` is the machine-enforced
claim boundary; `--require-qualified` must fail until all recovery evidence exists.

### Alternatives

- `pg_dump` alone: retained for logical portability, but rejected as the disaster-recovery path
  because it does not provide a continuous WAL chain or bounded PITR.
- PostgreSQL base backup plus hand-written WAL scripts: technically possible, but rejected for the
  initial design because retention, validation, expiry, parallelism, and recovery orchestration
  would become bespoke security-critical code.
- Restic for database directories: rejected because file-level capture is not a replacement for a
  PostgreSQL-aware consistent backup.
- Same-G10 storage or another local VM: useful only for staging and rejected as independent
  recovery because it shares the declared host failure domain.
- Mandatory cloud storage: rejected because runtime backup and restore must not require Internet;
  an approved LAN or physically transferred independent destination remains possible.

### Consequences

Two database repositories and a third file repository increase storage, monitoring, credential,
version, retention, and operator work. Exact pgBackRest versions must match across cooperating
endpoints. Backup success is not a release gate by itself: isolated restoration, compatibility,
negative tests, offline operation, and measured RPO/RTO are required. This cost creates a clear
failure-domain boundary and avoids presenting a local copy as disaster recovery.

### Security and operational impact

Repository deletion, ransomware, stolen keys, silent corruption, missing WAL, wrong-key restore,
and accidental production reconnection are explicit test cases. Restore labs have no production
route or credential. Public records contain only sanitized identifiers and hashes. Rollout is
additive; no existing recovery material is deleted until the new path restores successfully and
its overlap period ends. Rollback disables new jobs and removes only verified new configuration,
leaving the serving clusters unchanged.

## فارسی

<div dir="rtl">

### زمینه

NextOps دو خوشهٔ جداگانهٔ PostgreSQL 16، انتشارهای تغییرناپذیر برنامه و مدل، پیکربندی محافظت‌شده،
مستندات، مانیفست‌ها و شواهد مجاز دارد. dump منطقی هر دو پایگاه با موفقیت در خوشه‌های جدا و
فقط‌سوکتی بازیابی شده است؛ بااین‌حال همهٔ سرویس‌ها هنوز در دامنهٔ خرابی یک G10 قرار دارند و
مجموعهٔ بازیابی مستقل و آگاه از WAL وجود ندارد. کپی فایل، سازگاری پایگاه یا PITR را ثابت نمی‌کند و
پوشه، VM یا نسخهٔ دیگری که به همان میزبان سرویس‌دهنده وابسته باشد، بحران تعریف‌شده را تاب نمی‌آورد.

### تصمیم

pgBackRest گزینهٔ تخصصی هر دو پایگاه است؛ اما شناسهٔ مخزن، هویت دسترسی، سیاست، شاهد و روش بازیابی
برنامه و Zabbix باید کاملاً جدا باشند. پشتیبان کامل به‌همراه پشتیبان تفاضلی موجه، بایگانی پیوستهٔ
WAL، نگه‌داری، کنترل مخزن و آزمون PITR در محیط جدا الزامی است. میزبان یا سرویس مخزن باید از مهمان،
datastore و hypervisor سرویس‌دهنده مستقل باشد.

restic فقط برای رده‌های غیرپایگاهیِ صریحاً مصوب به‌کار می‌رود: artifact انتشار، مانیفست، مستندات،
پیکربندی مصوب و شواهد مجاز. پوشهٔ دادهٔ PostgreSQL، snapshot زندهٔ پایگاه و WAL ورودی مجاز restic
نیستند. کلید و اطلاعات دسترسی بیرون Git می‌مانند و حضانت آن‌ها از اجرای عادی پشتیبان جداست.

گزینه‌های فعلی ارزیابی، pgBackRest 2.59.1 با مجوز MIT و restic 0.19.1 با مجوز BSD-2-Clause هستند.
این انتخاب برای صلاحیت‌سنجی بستهٔ آفلاین است و به معنی نصب وابستگی تولیدی نیست. artifact دقیق،
SHA-256، تأیید وابستگی و مجوز و نصب آفلاین هنوز دروازه‌اند. پروفایل عمومی `deploy/recovery` مرز
ماشین‌خوان ادعاست و گزینهٔ `--require-qualified` تا پیش از وجود همهٔ شواهد باید شکست بخورد.

### گزینه‌های دیگر

- `pg_dump` برای جابه‌جایی منطقی حفظ می‌شود، اما چون زنجیرهٔ پیوستهٔ WAL و PITR محدودشده فراهم
  نمی‌کند، مسیر بازیابی بحران نیست.
- base backup بومی PostgreSQL با اسکریپت‌های دستی WAL شدنی است، اما نگه‌داری، اعتبارسنجی، انقضا،
  هم‌روندی و هماهنگی بازیابی را به کد سفارشی و امنیت‌حساس تبدیل می‌کند؛ بنابراین انتخاب نخست نیست.
- استفاده از restic برای پوشهٔ پایگاه رد می‌شود؛ پشتیبان فایل جایگزین پشتیبان سازگار با PostgreSQL
  نیست.
- فضای همان G10 یا VM محلی دیگر فقط برای staging مفید است و بازیابی مستقل محسوب نمی‌شود.
- وابستگی اجباری به cloud رد می‌شود، زیرا پشتیبان و بازیابی زمان اجرا نباید به اینترنت نیاز داشته
  باشند؛ مقصد مستقل LAN یا رسانهٔ فیزیکی مصوب همچنان ممکن است.

### پیامدها

دو مخزن پایگاه و یک مخزن فایل، هزینهٔ فضا، پایش، هویت، تطبیق نسخه، نگه‌داری و عملیات را افزایش
می‌دهند. نسخهٔ pgBackRest در دو سوی همکاری باید دقیقاً یکسان باشد. موفقیت job پشتیبان به‌تنهایی
دروازهٔ انتشار نیست؛ بازیابی جدا، سازگاری، آزمون منفی، کارکرد آفلاین و RPO/RTO اندازه‌گیری‌شده لازم
است. در برابر این هزینه، مرز دامنهٔ خرابی روشن می‌شود و نسخهٔ محلی به‌اشتباه بازیابی بحران نامیده
نمی‌شود.

### اثر امنیتی و عملیاتی

حذف مخزن، باج‌افزار، سرقت کلید، خرابی خاموش، WAL مفقود، کلید نادرست و اتصال تصادفی محیط بازیابی
به تولید، آزمون‌های صریح‌اند. آزمایشگاه بازیابی مسیر یا اعتبارنامهٔ تولید ندارد. سند عمومی فقط
شناسه و hash پالایش‌شده نگه می‌دارد. استقرار افزایشی است؛ مواد بازیابی موجود تا بازیابی موفق مسیر
جدید و پایان دورهٔ هم‌پوشانی حذف نمی‌شوند. بازگشت، jobهای تازه را غیرفعال و فقط پیکربندی تازه و
راستی‌آزمایی‌شده را حذف می‌کند و خوشه‌های سرویس‌دهنده را دست‌نخورده نگه می‌دارد.

</div>
