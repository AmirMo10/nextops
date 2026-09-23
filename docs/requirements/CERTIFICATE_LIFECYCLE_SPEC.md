# Local certificate lifecycle / چرخهٔ محلی گواهی

Status: **source implemented; controlled deployment pending.** Date: 2026-09-23.

## English

### Problem

The controlled application and Zabbix frontends validate TLS, but a valid certificate today does
not prove that expiry will be detected, renewed offline, or safely rolled back. An expired
certificate would block fresh login and monitoring access even while every backend service remained
healthy. Production qualification therefore needs an explicit local lifecycle control.

### Requirements

- Check each deployed frontend certificate at least daily with a configurable 1–3,650-day warning
  window; the controlled profile uses 90 days.
- Use only the local certificate, pinned `/usr/bin/openssl`, the system clock and Python 3.12. No
  DNS, WAN, CDN, public CA or hosted telemetry call is permitted.
- Read public certificate metadata only. The checker must never accept, open or report a private-key
  path.
- Emit one bounded JSON record containing the deployment-owned label, validity interval, remaining
  seconds, warning window and SHA-256 certificate fingerprint. Never emit subject/SAN data, key
  material, credentials or an endpoint address.
- Return success only for a currently valid certificate outside the warning window. Expiring,
  expired and not-yet-valid certificates fail the service; malformed input and tool failures use a
  distinct error exit.
- Run as the dedicated non-login `nextops-certcheck` identity with no network address family,
  capabilities, writable system path or private-key permission. A persistent systemd timer catches
  checks missed during a shutdown.
- Renewal remains a reviewed operator change: stage offline, verify the certificate/key pair and
  local CA chain, preserve the prior pair, validate Nginx, atomically promote, reload, test with
  ordinary certificate validation, and roll back on failure.
- The failed/expiring service state must be connected to a locally owned alert before production
  sign-off. A journal entry alone is not sufficient notification.

### Non-goals

This increment does not automatically issue or renew certificates, contact an Internet CA, rotate
private keys, disable expiry/hostname validation, disclose internal names, or claim production
acceptance. It does not replace independent backup, trusted local time, revocation planning or a
human-reviewed rotation record.

### Threat considerations

- A substituted certificate path or binary could create false health; deployment pins absolute
  root-owned paths and the unit cannot write them.
- A malformed or oversized certificate must fail closed without logging raw parser output.
- Running the checker as root would unnecessarily expose the private directory; deployment grants a
  dedicated identity traversal and read access to the public certificate only while the key remains
  root-only.
- A disabled timer or missing alert could hide expiry. Acceptance checks enabled/active timer state,
  a recent successful invocation and a controlled failing fixture.
- Clock drift can make a certificate appear valid or invalid. The lifecycle check depends on the
  separately monitored local time source and never extends validity to compensate.

### Implementation and tasks

1. `scripts/check_certificate_expiry.py` parses bounded OpenSSL metadata into deterministic states.
2. `nextops-certificate-check.service` and `.timer` run the checker locally under a hardened,
   dedicated identity.
3. Deploy the same reviewed artifacts to the application and Zabbix TLS frontends with per-host,
   non-secret configuration.
4. Prove healthy, expiring and malformed states; inspect unit hardening and verify the key remains
   root-only.
5. Connect the failed/expiring state to Zabbix or another approved local notification path, then
   perform a staged rotation and rollback exercise.

### Acceptance criteria and tests

- Formatting, lint, strict typing, focused state/parser tests and static systemd tests pass.
- Both live frontend certificates decode successfully and are outside the 90-day warning window.
- Both timers are enabled and active; an immediate service run exits successfully after reboot-safe
  installation.
- A temporary short-lived certificate returns `expiring` and a non-zero status without touching the
  live pair; malformed input returns the distinct error status.
- The checker identity can read the public certificate but cannot read the private key.
- Nginx validation, reload, normal browser TLS, offline login and Zabbix HTTPS/API access pass after
  an authorized rotation; the previous pair remains usable for rollback.
- A local alert reaches its approved operator path. Until the rotation and alert gates pass, the
  production certificate-lifecycle gate remains partial.

### Rollback and documentation

Disable the timer, stop the checker, restore the prior unit/configuration and certificate-directory
ownership, then remove the dedicated identity only after it owns no files. This monitoring rollback
must not alter the active certificate/key pair or weaken Nginx validation. Record dates,
fingerprints, result, alert evidence, change identifier and rollback outcome outside public Git;
keep only sanitized capability status in the repository.

## فارسی

<div dir="rtl">

### مسئله

رابط‌های برنامه و Zabbix در محیط کنترل‌شده گواهی TLS را اعتبارسنجی می‌کنند؛ اما معتبر بودن گواهی
در امروز ثابت نمی‌کند که انقضا به‌موقع تشخیص داده، تمدید در حالت آفلاین انجام یا بازگشت با ایمنی
اجرا می‌شود. گواهی منقضی می‌تواند ورود تازه و دسترسی پایشی را متوقف کند، حتی اگر همهٔ سرویس‌های
پشتی سالم باشند. بنابراین صلاحیت تولید به کنترل صریح و محلی چرخهٔ عمر نیاز دارد.

### الزامات

- هر گواهی رابط دست‌کم روزی یک‌بار با بازهٔ هشدار قابل‌تنظیم از ۱ تا ۳۶۵۰ روز بررسی شود؛ پروفایل
  کنترل‌شده ۹۰ روز است.
- بررسی فقط از گواهی محلی، `/usr/bin/openssl` ثابت، ساعت سامانه و Python 3.12 استفاده کند. هیچ
  فراخوانی DNS، WAN، CDN، مرجع صدور عمومی یا پایش میزبانی‌شده مجاز نیست.
- فقط فرادادهٔ عمومی گواهی خوانده شود. ابزار نباید مسیر کلید خصوصی را بپذیرد، باز کند یا گزارش دهد.
- یک رکورد JSON محدود شامل برچسب متعلق به استقرار، بازهٔ اعتبار، ثانیهٔ باقی‌مانده، بازهٔ هشدار و
  اثرانگشت SHA-256 گواهی نوشته شود. نام موضوع/SAN، مادهٔ کلید، اعتبارنامه و نشانی endpoint نباید
  ثبت شود.
- موفقیت فقط برای گواهی معتبر و بیرون از بازهٔ هشدار است. گواهی نزدیک انقضا، منقضی یا هنوز
  نامعتبر سرویس را ناموفق می‌کند؛ ورودی خراب و خرابی ابزار کد خروج جدا دارد.
- اجرا با هویت مستقل و بدون ورود `nextops-certcheck`، بدون خانوادهٔ نشانی شبکه، قابلیت Linux، مسیر
  سیستمی قابل‌نوشتن یا مجوز کلید خصوصی باشد. timer ماندگار بررسی ازدست‌رفته هنگام خاموشی را جبران
  کند.
- تمدید همچنان تغییر بازبینی‌شدهٔ بهره‌بردار است: آماده‌سازی آفلاین، تطبیق گواهی و کلید و زنجیرهٔ
  CA محلی، حفظ جفت پیشین، اعتبارسنجی Nginx، ترویج اتمی، reload، آزمون با اعتبارسنجی عادی و بازگشت
  در صورت شکست.
- پیش از تأیید تولید، وضعیت ناموفق یا نزدیک انقضا باید به هشدار محلی با مالک مشخص متصل شود؛ ثبت در
  journal به‌تنهایی اعلان کافی نیست.

### خارج از دامنه

این increment گواهی را خودکار صادر یا تمدید نمی‌کند، با CA اینترنتی تماس نمی‌گیرد، کلید خصوصی را
نمی‌چرخاند، اعتبارسنجی انقضا یا نام میزبان را کنار نمی‌گذارد، نام داخلی را افشا نمی‌کند و ادعای
آمادگی تولید ندارد. همچنین جای پشتیبان مستقل، ساعت محلی قابل‌اعتماد، برنامهٔ ابطال یا رکورد تغییر
بازبینی‌شده را نمی‌گیرد.

### ملاحظات تهدید

- جایگزینی مسیر گواهی یا باینری می‌تواند سلامت دروغین بسازد؛ استقرار مسیرهای مطلق و متعلق به root
  را ثابت می‌کند و واحد اجازهٔ نوشتن آن‌ها را ندارد.
- گواهی خراب یا بیش‌ازحد بزرگ باید بدون ثبت خروجی خام parser به‌شکل امن رد شود.
- اجرای ابزار با root بی‌دلیل پوشهٔ خصوصی را در دسترس می‌گذارد؛ هویت مستقل فقط اجازهٔ عبور و خواندن
  گواهی عمومی را می‌گیرد و کلید فقط برای root باقی می‌ماند.
- timer غیرفعال یا نبود هشدار می‌تواند انقضا را پنهان کند. پذیرش، فعال بودن timer، اجرای موفق اخیر
  و fixture کنترل‌شدهٔ ناموفق را بررسی می‌کند.
- انحراف ساعت می‌تواند نتیجه را نادرست کند. ابزار به منبع زمان محلی که جداگانه پایش می‌شود متکی است
  و برای جبران، اعتبار گواهی را تمدید نمی‌کند.

### پیاده‌سازی و کارها

۱. `scripts/check_certificate_expiry.py` فرادادهٔ محدود OpenSSL را به وضعیت قطعی تبدیل می‌کند.
۲. واحد `nextops-certificate-check.service` و timer آن ابزار را با هویت مستقل و سخت‌سازی‌شده اجرا
می‌کنند.
۳. همان artifact بازبینی‌شده با تنظیم غیرمحرمانهٔ هر میزبان روی رابط برنامه و Zabbix مستقر شود.
۴. حالت سالم، نزدیک انقضا و خراب ثابت، سخت‌سازی واحد بررسی و دسترسی‌ناپذیری کلید تأیید شود.
۵. وضعیت ناموفق به Zabbix یا مسیر اعلان محلی مصوب متصل و سپس تمرین مرحله‌ای چرخش و بازگشت اجرا شود.

### معیار پذیرش و آزمون

- قالب، lint، نوع‌سنجی سخت‌گیرانه، آزمون متمرکز parser/وضعیت و بررسی ایستای systemd موفق باشد.
- هر دو گواهی زنده با موفقیت خوانده شوند و بیرون از بازهٔ هشدار ۹۰روزه باشند.
- هر دو timer فعال و enabled باشند و اجرای فوری سرویس پس از نصب سازگار با reboot موفق شود.
- گواهی موقت کوتاه‌عمر، بدون تماس با جفت زنده، وضعیت `expiring` و کد غیرصفر بدهد؛ ورودی خراب کد
  خطای جدا برگرداند.
- هویت checker بتواند گواهی عمومی را بخواند، اما نتواند کلید خصوصی را بخواند.
- پس از چرخش مجاز، اعتبارسنجی و reload در Nginx، TLS عادی مرورگر، ورود آفلاین و HTTPS/API زبیکس
  موفق باشند و جفت قبلی برای بازگشت حفظ شود.
- هشدار محلی به مسیر مصوب بهره‌بردار برسد. تا موفقیت چرخش و هشدار، دروازهٔ چرخهٔ گواهی برای تولید
  ناقص است.

### بازگشت و مستندسازی

timer غیرفعال و checker متوقف، واحد و تنظیم قبلی و مالکیت پوشهٔ گواهی برگردانده و هویت مستقل فقط
پس از اطمینان از نداشتن فایل حذف شود. این بازگشت پایش نباید جفت فعال گواهی/کلید را تغییر دهد یا
اعتبارسنجی Nginx را ضعیف کند. تاریخ، اثرانگشت، نتیجه، شاهد هشدار، شناسهٔ تغییر و نتیجهٔ بازگشت بیرون
از Git عمومی ثبت شوند؛ در مخزن فقط وضعیت پالایش‌شدهٔ قابلیت نگه داشته شود.

</div>
