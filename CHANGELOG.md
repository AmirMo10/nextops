# Changelog / تاریخچهٔ تغییرات

## Unreleased — controlled engineering foundation / بنیان مهندسی کنترل‌شده

### English

Added a schema-validated, non-secret release/status manifest and cross-checks against the pinned
llama.cpp/model artifact identity. Introduced a brownfield specification workflow, a bounded
backup/restore specification, a tool-adoption plan and three project workflows for change planning,
acceptance review and bilingual documentation review. These workflows are development aids, not
authorization or infrastructure security boundaries.

Aligned active English and Persian documentation with the verified four-host deployment, durable
investigation/audit, scoped failure qualification, WAN-isolated server/API path and serial reboot
evidence. Historical records remain intact. CI now tests PostgreSQL 16.15, matching deployment, and
17.6 in separate digest-pinned jobs; checkout credentials are not persisted, workflow permissions
remain minimal, and strict typing now includes operational scripts. The inference artifact records
the accepted offline cold-start result without promoting production readiness.

Local validation passes Ruff format/lint, strict mypy over 65 files, 103 non-integration tests,
documentation validation for 102 Markdown files and 31 bilingual guide pairs, release/deployment/
inference/installer validators, package build, locked-dependency audit, Gitleaks and pedantic
Zizmor 1.29.0 with no findings. The six
PostgreSQL integration tests retain prior isolated-database evidence but were not rerun in this
Windows session because no local server or working container runtime was available.

### فارسی

یک مانیفست پالایش‌شده و بدون اطلاعات محرمانه برای وضعیت انتشار، همراه schema و تطبیق هویت فایل
مدل و محیط اجرای تثبیت‌شدهٔ llama.cpp افزوده شد. گردش‌کار مشخصات برای سامانهٔ موجود، مشخصات محدود
پشتیبان و بازیابی، برنامهٔ ارزیابی ابزارها و سه راهنمای پروژه برای برنامه‌ریزی تغییر، بازبینی پذیرش
و بازبینی مستندات دوزبانه ایجاد شدند. این راهنماها ابزار توسعه‌اند و مرز مجوز یا امنیت زیرساخت نیستند.

مستندات فعال فارسی و انگلیسی با استقرار تأییدشدهٔ چهار میزبان، بررسی و ممیزی ماندگار، آزمون‌های
محدود خطا، قطع WAN در مسیر سرور/API و شواهد راه‌اندازی مجدد ترتیبی هم‌راستا شدند؛ سوابق تاریخی
دست‌نخورده ماندند. CI اکنون PostgreSQL 16.15، برابر با نسخهٔ مستقر، و 17.6 را در کارهای جدا و با
image تثبیت‌شده بر اساس digest می‌آزماید؛ اعتبارنامهٔ checkout حفظ نمی‌شود، مجوز گردش‌کار حداقلی
است و نوع‌سنجی سخت‌گیرانه scriptهای عملیاتی را نیز پوشش می‌دهد. فایل هویت هوش مصنوعی، نتیجهٔ پذیرفتهٔ
شروع سرد آفلاین را بدون ادعای آمادگی تولید ثبت می‌کند.

در محیط محلی، قالب و lint با Ruff، نوع‌سنجی سخت‌گیرانهٔ ۶۵ فایل، ۱۰۳ آزمون غیر‌یکپارچه، اعتبارسنجی
۱۰۲ فایل Markdown و ۳۱ جفت راهنمای دوزبانه، اعتبارسنج‌های انتشار، استقرار، هوش مصنوعی و نصب، ساخت
بسته، ممیزی وابستگی‌های قفل‌شده، Gitleaks و Zizmor 1.29.0 در حالت سخت‌گیرانه موفق‌اند. شش آزمون
PostgreSQL شواهد موفق پیشین روی پایگاه جدا
دارند، اما در این نشست Windows به‌دلیل نبود سرور محلی و محیط کانتینری سالم دوباره اجرا نشدند.

## 2026-09-22 — Stage 1F WAN and clean reboot qualification / صلاحیت‌سنجی قطع WAN و راه‌اندازی مجدد سالم در مرحلهٔ 1F

### English

Passed explicit WAN isolation across all four controlled Ubuntu 24.04 guests while preserving the
approved LAN, fresh authentication, bilingual model-only answers, local-AI readiness, eight fresh
Zabbix measurements, durable investigation storage and audit linkage. The temporary nftables policy
was guarded by automatic rollback, loaded before normal networking during the reboot checks and was
removed completely afterward.

The first Zabbix attempts exposed a 30-minute shutdown stall. The journal proved that the vendor
unit referenced PostgreSQL's inert meta-unit and allowed the real cluster to stop before Zabbix,
whose stop timeout was infinite. A versioned drop-in now requires and orders around
`postgresql@16-zabbix.service` and bounds shutdown at 90 seconds. A controlled stop completed in
under one second, and the accepted reboot stopped Zabbix before PostgreSQL and started it after the
database was active.

Connector and AI then passed serial clean reboots. The first application reboot exposed the same
meta-unit class of startup defect: the API started while `postgresql@16-nextops.service` remained
down. The application unit now requires the real cluster; the clean retry started PostgreSQL before
the API and passed login, bilingual Q&A, monitoring and a new durable investigation. Final read-only
preflight found every guest `running`, with zero failed units, no temporary policy residue and direct
HTTPS restored. Ruff, strict mypy, 102 non-integration tests, documentation validation and deployment
dossier validation pass. Independent browser isolation, rollback of the runtime/model artifacts,
backup, isolated restore, sustained load and production acceptance remain open.

### فارسی

قطع صریح WAN روی هر چهار مهمان کنترل‌شدهٔ Ubuntu 24.04 با موفقیت آزموده شد؛ شبکهٔ داخلی مصوب،
ورود تازه، پاسخ عمومی فارسی و انگلیسی، آمادگی هوش مصنوعی محلی، هشت سنجهٔ تازهٔ Zabbix، ذخیرهٔ
ماندگار بررسی و پیوند ممیزی برقرار ماند. سیاست موقت nftables زمان‌سنج بازگشت خودکار داشت، در آزمون
راه‌اندازی مجدد پیش از شبکهٔ عادی بار شد و در پایان بدون باقی‌ماندن فایل یا قاعده حذف شد.

تلاش‌های نخست Zabbix یک توقف ۳۰ دقیقه‌ای در خاموش‌شدن را آشکار کردند. گزارش‌ها ثابت کردند که واحد
شرکت سازنده به سرویس صوری PostgreSQL اشاره می‌کرد و خوشهٔ واقعی پیش از Zabbix خاموش می‌شد؛ مهلت
توقف Zabbix نیز نامحدود بود. drop-in نسخه‌دار جدید، `postgresql@16-zabbix.service` را الزام می‌کند،
ترتیب درست را می‌سازد و مهلت توقف را به ۹۰ ثانیه محدود می‌کند. توقف کنترل‌شده در کمتر از یک ثانیه
پایان یافت و در راه‌اندازی پذیرفته‌شده، Zabbix پیش از PostgreSQL خاموش و پس از آماده‌شدن پایگاه آغاز شد.

مهمان‌های اتصال و هوش مصنوعی سپس راه‌اندازی مجدد سالم و ترتیبی را گذراندند. نخستین بوت برنامه همان
ردهٔ نقص سرویس صوری را در آغاز آشکار کرد: API بالا آمد، اما `postgresql@16-nextops.service` خاموش
ماند. واحد برنامه اکنون خوشهٔ واقعی را الزام می‌کند؛ در تکرار سالم، PostgreSQL پیش از API فعال شد و
ورود، پاسخ عمومی دوزبانه، پایش و یک بررسی ماندگار تازه موفق بودند. پیش‌بررسی نهایی هر چهار مهمان را
با وضعیت `running`، صفر واحد خراب، بدون اثر سیاست موقت و با HTTPS مستقیمِ برقرار یافت. Ruff، mypy
سخت‌گیرانه، ۱۰۲ آزمون غیر‌یکپارچه، اعتبارسنجی مستندات و پرونده‌های استقرار موفق‌اند. جداسازی مستقل
مرورگر، بازگشت فایل‌های محیط اجرا و مدل، پشتیبان، بازیابی جدا، بار پایدار و پذیرش تولید هنوز بازند.

## 2026-09-22 — Stage 1E failure qualification / صلاحیت‌سنجی خطا در مرحلهٔ 1E

### English

Added explicit partial-evidence metadata to the bounded Zabbix summary: `is_partial` and typed
`partial_reasons`. The connector now marks bounded metric selection, a full problem-result page and
the absence of usable measurements. The durable investigation result and append-only audit retain
the marker, while the bilingual panel displays evidence coverage. Monitoring field content is now
identified as untrusted data in the model prompt even when it came through an authenticated source;
embedded instructions are never treated as authority. Malformed source text still becomes a safe,
typed dependency error.

Promoted connector release `nextops-0.1.0-3d7d725` and app release
`nextops-0.1.0-13a3369`. A temporary token owned by the existing reader identity inherited the
same four-host scope, then lost access immediately after revocation and was deleted; the live token
was unchanged. During a controlled Zabbix API outage, monitoring and investigation returned safe,
retryable `503` errors labeled `connector.summary_unavailable`, the failed investigation and its
audit event were persisted, and general model-only Q&A remained available. The frontend recovered,
fresh monitoring resumed, and a subsequent live investigation preserved partial metadata and its
independently verified evidence hash in 67.9 seconds.

Stale, partial, malformed-text and prompt-injection cases pass deterministic boundary tests. Ruff,
strict mypy, 101 non-integration tests and all six isolated PostgreSQL integration tests pass. This
completes the scoped failure-qualification increment, not WAN-disconnection, VM-reboot, sustained
load, backup, restore or production acceptance.

### فارسی

در خلاصهٔ محدود Zabbix، وضعیت ناقص‌بودن شاهد با دو فیلد صریح `is_partial` و
`partial_reasons` ثبت می‌شود. اتصال‌دهنده، محدودشدن فهرست سنجه‌ها، پرشدن صفحهٔ نتایج مسئله‌ها و
نبود سنجهٔ قابل‌استفاده را مشخص می‌کند. همین وضعیت در نتیجهٔ ماندگار بررسی و ممیزی فقط‌افزودنی
حفظ می‌شود و پنل دوزبانه نیز میزان پوشش شواهد را نشان می‌دهد. متن فیلدهای پایش، حتی وقتی از منبع
احرازهویت‌شده آمده باشد، برای مدل «دادهٔ غیرقابل‌اعتماد» است؛ بنابراین دستور جاسازی‌شده در نام
میزبان، سنجه یا مسئله مرجع تصمیم‌گیری نیست. متن بدساخت نیز فقط به خطای امن و ساخت‌یافتهٔ وابستگی
تبدیل می‌شود.

انتشار `nextops-0.1.0-3d7d725` برای اتصال‌دهنده و انتشار `nextops-0.1.0-13a3369` برای برنامه فعال
شد. یک توکن موقت متعلق به همان هویت خوانشگر، دامنهٔ مصوبِ شامل چهار میزبان را به ارث برد؛ پس از لغو
بلافاصله دسترسی‌اش قطع و سپس حذف شد، بی‌آنکه توکن فعال تغییر کند. هنگام قطع کنترل‌شدهٔ API زبیکس،
خلاصهٔ پایش و بررسی زنده خطای قابل‌تکرار و امن `503` با کلید `connector.summary_unavailable`
برگرداندند، اجرای ناموفق و رویداد ممیزی آن ماندگار شد و پاسخ‌گویی عمومی مدل محلی همچنان در دسترس
بود. پس از بازگشت رابط، دادهٔ تازه دوباره دریافت شد و یک بررسی زندهٔ بعدی، نشان ناقص‌بودن و هش
مستقلِ تأییدشدهٔ شاهد را طی ۶۷٫۹ ثانیه حفظ کرد.

سناریوهای شاهد قدیمی و ناقص، متن بدساخت و تزریق دستور در آزمون‌های قطعی مرزی موفق‌اند. Ruff،
mypy سخت‌گیرانه، ۱۰۱ آزمون غیر‌یکپارچه و هر شش آزمون PostgreSQL در پایگاه جداگانه عبور کردند.
این نتیجه فقط گام مشخص صلاحیت‌سنجی خطا را تکمیل می‌کند؛ قطع WAN، راه‌اندازی مجدد ماشین‌ها، بار
پایدار، پشتیبان، بازیابی و پذیرش تولید همچنان باز هستند.

## 2026-09-22 — Four-host Zabbix coverage / پوشش چهارمیزبانی Zabbix

### English

Added the application, AI and read-only connector guests to the existing approved Zabbix host
group. Each guest runs the exact cached Zabbix Agent 2 package `1:7.0.30-1+ubuntu24.04` with a
distinct PSK and outbound active checks only. Passive checks and remote commands are disabled, no
guest listens on port 10050, and the Zabbix trapper path is limited by host firewall rules to the
three approved sources. No repository refresh or unrelated package upgrade was performed.

The unchanged API-only reader can now see exactly the four approved hosts. Its existing
`host.get`, `item.get` and `problem.get` boundary remains in force: an unlisted read and a mutation
were both denied. Final reader validation observed fresh supported items for all three new hosts,
and the application monitoring endpoint continued to return eight fresh metrics, zero stale
metrics and zero active problems. All four systems remained in the `running` state with no failed
units; existing application, database, proxy, tunnel, AI, connector and monitoring services stayed
active.

### فارسی

مهمان‌های برنامه، هوش مصنوعی و اتصال فقط‌خواندنی به همان گروه میزبان مصوب در Zabbix افزوده شدند.
روی هر سه مهمان، بستهٔ دقیق Zabbix Agent 2 با نسخهٔ `1:7.0.30-1+ubuntu24.04`، کلید PSK مستقل و
فقط بررسی فعالِ خروجی اجرا می‌شود. بررسی غیرفعال و فرمان راه دور بسته است، هیچ مهمانی روی درگاه
۱۰۰۵۰ گوش نمی‌دهد و دیوارهٔ آتش مسیر دریافت داده در Zabbix را به همان سه مبدأ مصوب محدود می‌کند.
هیچ تازه‌سازی مخزن یا ارتقای نامرتبطی انجام نشد.

خوانشگر فقط‌ـAPI و بدون تغییر اکنون دقیقاً چهار میزبان مصوب را می‌بیند. مرز سه روش
`host.get`، `item.get` و `problem.get` پابرجا ماند و یک خواندن خارج از فهرست و یک روش نوشتنی هر دو
رد شدند. در بررسی نهایی، هر سه میزبان تازه دادهٔ پشتیبانی‌شده و تازه داشتند و مسیر پایش برنامه نیز
همچنان هشت سنجهٔ تازه، بدون سنجهٔ قدیمی و بدون مسئلهٔ فعال بازگرداند. وضعیت هر چهار سامانه
`running` و شمار واحد خراب صفر ماند و سرویس‌های برنامه، پایگاه، پراکسی، تونل‌ها، هوش مصنوعی،
اتصال و پایش همگی فعال باقی ماندند.

## 2026-09-22 — Durable live-investigation audit / ثبت ماندگار بررسی زنده و ممیزی

### English

Completed the missing Stage 1D durable linkage for `POST /api/v1/investigate`. The application now
creates a scoped PostgreSQL run before calling the connector or model, records the server-derived
actor and correlation ID, and atomically stores the bounded Zabbix summary, its canonical SHA-256
reference, the local-model result and an append-only completion audit event. Safe failure metadata
is persisted and audited without raw dependency errors, credentials or unrestricted payloads.

The monitoring response and bilingual panel now expose the durable run, evidence reference and
audit-event identifiers. The authenticated `GET /api/v1/runs/{run_id}` route returns the same stored
result within the actor's organization/environment scope. General assistant questions remain
model-only and do not create monitoring evidence.

Immutable app release `nextops-0.1.0-fde27bd` was promoted with `3d61bf6` retained for rollback; no
schema migration was required. All 95 non-integration tests and six isolated PostgreSQL tests pass.
Live acceptance returned eight fresh metrics, zero active problems and a 128-token local answer in
57.2 seconds; run retrieval, independent evidence-hash calculation and audit linkage all passed.
The production record showed one successful `live_monitoring` result, a 64-character evidence hash,
two linked audit events and a completion audit ID matching the stored result.

### فارسی

پیوند ماندگارِ باقی‌مانده از مرحلهٔ 1D برای مسیر `POST /api/v1/investigate` تکمیل شد. برنامه پیش
از فراخوانی اتصال یا مدل، یک اجرای محدود به دامنه در PostgreSQL می‌سازد و عامل استخراج‌شده در سمت
سرور و شناسهٔ هم‌بستگی را ثبت می‌کند. سپس خلاصهٔ محدود Zabbix، مرجع مبتنی بر SHA-256 محتوای آن،
پاسخ مدل محلی و رویداد تکمیل در ممیزیِ فقط‌افزودنی، در یک تراکنش ذخیره می‌شوند. در حالت خطا نیز
فقط اطلاعات امن و ساخت‌یافته ثبت و ممیزی می‌شود؛ خطای خام وابستگی، اعتبارنامه و payload نامحدود
وارد پایگاه نمی‌شود.

پاسخ پایش و پنل دوزبانه اکنون شناسهٔ اجرای ماندگار، مرجع شاهد و رویداد ممیزی را نشان می‌دهند.
مسیر احرازهویت‌شدهٔ `GET /api/v1/runs/{run_id}` همان نتیجهٔ ذخیره‌شده را فقط در دامنهٔ سازمان و
محیط کاربر بازمی‌گرداند. پرسش‌های دستیار عمومی همچنان مستقل و بدون ایجاد شاهد پایشی باقی مانده‌اند.

انتشار تغییرناپذیر `nextops-0.1.0-fde27bd` فعال و `3d61bf6` برای بازگشت نگه‌داری شد؛ این تغییر به
migration تازه نیاز نداشت. هر ۹۵ آزمون غیر‌یکپارچه و شش آزمون PostgreSQL در پایگاه جداگانه موفق
بودند. پذیرش زنده هشت سنجهٔ تازه، بدون مسئلهٔ فعال و پاسخ ۱۲۸ توکنی مدل محلی را در ۵۷٫۲ ثانیه
برگرداند؛ بازیابی اجرای ماندگار، محاسبهٔ مستقل هش شاهد و پیوند ممیزی نیز همگی موفق بودند. رکورد
عملیاتی یک نتیجهٔ موفق `live_monitoring`، هش ۶۴ نویسه‌ای، دو رویداد ممیزی پیوندخورده و تطبیق شناسهٔ
ممیزی تکمیل با نتیجهٔ ذخیره‌شده را نشان داد.

## 2026-09-22 — Relevant answer modes / تفکیک پاسخ عمومی از پایش زنده

### English

Corrected the semantic routing exposed by the first user test: the panel sent every question,
including a simple greeting, through the Zabbix investigation path. A successful HTTP response was
therefore still an unrelated answer.

The panel now has two explicit modes. **General assistant** is the default and sends only the
question to the local model; it does not retrieve or display live monitoring evidence. **Live
monitoring** is opt-in and retains the existing evidence-grounded Zabbix workflow. The server uses
separate prompts and endpoints for these modes, and the result badge states whether live evidence
was used.

Immutable app release `nextops-0.1.0-3d61bf6` was promoted with `8d31bcb` retained for rollback.
The exact general-mode request `Hi` returned HTTP 200 and “Hello! How can I assist you today?” in
14.0 seconds, with no Zabbix, problem or CPU-status content. A Persian greeting likewise returned a
Persian general answer with no monitoring content. The live monitoring regression still returned
eight fresh metrics and passed grounded English and Persian checks. Ruff, strict mypy and 94 tests
pass; five desktop PostgreSQL integration tests remain skipped.

### فارسی

اشکال معنایی آشکارشده در نخستین ارزیابی کاربر برطرف شد: پنل همهٔ پرسش‌ها، حتی یک سلام ساده، را
به مسیر بررسی Zabbix می‌فرستاد. در نتیجه، موفق بودن درخواست از نظر فنی لزوماً به معنای مرتبط بودن
پاسخ نبود.

پنل اکنون دو حالت روشن و مستقل دارد. **دستیار عمومی** حالت پیش‌فرض است؛ فقط پرسش کاربر را به مدل
محلی می‌فرستد و هیچ شاهد زندهٔ پایشی دریافت یا نمایش نمی‌دهد. **پایش زنده** با انتخاب صریح کاربر
فعال می‌شود و همان مسیر مستند به شواهد Zabbix را حفظ می‌کند. در سمت سرور نیز این دو حالت، مسیر و
پرامپت جدا دارند و نشان پاسخ به‌روشنی اعلام می‌کند که آیا از دادهٔ زنده استفاده شده است یا نه.

انتشار تغییرناپذیر `nextops-0.1.0-3d61bf6` فعال شد و `8d31bcb` برای بازگشت محفوظ ماند. درخواست
دقیق `Hi` در حالت عمومی طی ۱۴٫۰ ثانیه با HTTP 200 و پاسخ “Hello! How can I assist you today?”
برگشت؛ هیچ اشاره‌ای به Zabbix، مسئلهٔ فعال یا وضعیت CPU در آن نبود. سلام فارسی نیز پاسخ عمومی
فارسی و بدون محتوای پایشی دریافت کرد. آزمون بازگشت مسیر پایش زنده همچنان هشت سنجهٔ تازه برگرداند و
بررسی مستند انگلیسی و فارسی را گذراند. Ruff، بررسی سخت‌گیرانهٔ mypy و ۹۴ آزمون موفق‌اند؛ پنج آزمون
یکپارچهٔ PostgreSQL در محیط رومیزی همچنان کنار گذاشته شده‌اند.

## 2026-09-22 — User-test timeout repair / اصلاح پایان مهلت آزمون کاربر

### English

Resolved the first browser-reported investigation failure. The deployed page requested a 384-token
answer while the qualified CPU inference boundary allows 120 seconds; the request exhausted that
boundary and the application converted the internal timeout into a generic `503`. Live monitoring
and readiness remained healthy throughout the incident.

The investigation route now enforces the qualified 128-token output ceiling server-side, including
for an already-open browser that still submits the old larger value. The panel submits the same
bound and presents safe, localized timeout, overload and dependency messages. The loopback JSON
transport also preserves bounded upstream `429` and `504` outcomes instead of collapsing them into
a generic dependency error.

Immutable app release `nextops-0.1.0-8d31bcb` was promoted with the prior release retained for
rollback. A reproduction using the exact question `hi` and the old 384-token browser payload
returned HTTP 200, live Zabbix evidence and a 128-token local answer in 61.6 seconds. Ruff, strict
mypy over 57 files and 94 tests pass; five desktop PostgreSQL integration tests remain skipped.

### فارسی

نخستین خطای گزارش‌شده از رابط مرورگر برطرف شد. صفحهٔ مستقرشده پاسخ ۳۸۴ توکنی درخواست می‌کرد، در
حالی که مرز تأییدشدهٔ پردازش روی CPU برای هر درخواست ۱۲۰ ثانیه مهلت دارد؛ درخواست به پایان این
مهلت رسید و برنامه خطای داخلی را به یک `503` عمومی تبدیل کرد. در تمام این مدت، پایش زنده و نشانگرهای
آمادگی سالم بودند.

مسیر بررسی اکنون سقف تأییدشدهٔ ۱۲۸ توکن را در سمت سرور اعمال می‌کند؛ بنابراین حتی صفحه‌ای که پیش
از به‌روزرسانی باز مانده و هنوز مقدار بزرگ‌تر را می‌فرستد نیز از این مرز عبور نمی‌کند. پنل همین سقف
را درخواست می‌کند و برای پایان مهلت، اشباع و قطع وابستگی، پیام‌های روشن و بومی‌شده نشان می‌دهد.
لایهٔ ارتباط داخلی نیز پاسخ‌های محدود `429` و `504` را به‌درستی حفظ می‌کند و دیگر همه را به خطای
عمومی وابستگی تبدیل نمی‌کند.

انتشار تغییرناپذیر `nextops-0.1.0-8d31bcb` فعال شد و نسخهٔ قبلی برای بازگشت محفوظ ماند. بازآزمایی
با همان پرسش `hi` و payload قدیمی ۳۸۴ توکنی، کد HTTP 200، شاهد زندهٔ Zabbix و پاسخ محلی ۱۲۸ توکنی
را در ۶۱٫۶ ثانیه بازگرداند. Ruff، بررسی سخت‌گیرانهٔ mypy روی ۵۷ فایل و ۹۴ آزمون موفق‌اند؛ پنج
آزمون یکپارچهٔ PostgreSQL در محیط رومیزی همچنان کنار گذاشته شده‌اند.

## 2026-09-22 — Live evidence user-testing path / مسیر زندهٔ شاهد برای ارزیابی کاربران

### English

Delivered and deployed the controlled bilingual user-testing path. The app guest now runs the
authenticated panel/API behind private TLS and Nginx with PostgreSQL 16 state. The AI and connector
dependencies are reached through separate restricted SSH forwards with pinned host keys; their
service credentials never reach the browser. Bootstrap, recovery, API documentation and direct
backend listeners are not exposed by the reverse proxy.

Initialized Zabbix 7.0.30 with PostgreSQL 16, Nginx/PHP-FPM, Agent 2, private TLS and self-monitoring.
Rotated the default administrator password and created a frontend-disabled API reader whose role
allows only `host.get`, `item.get` and `problem.get` and whose group can read one approved host
group. Verified one-host visibility and denial of a non-allowlisted API method. The token is stored
only as a protected systemd credential on the connector guest.

Added the rootless read-only connector, strict HTTPS validation, bounded result contracts,
source/version/timestamp/staleness metadata and a protected application gateway. Updated the panel
to submit evidence-grounded investigations and display the exact evidence beside the local model
answer in English or Persian. Fixed the Zabbix version probe to remain unauthenticated as required
by the API and gave the CPU-bound investigation route its explicit Nginx timeout.

Live qualification returned eight fresh self-monitoring measurements with no stale metrics or
active problems. Desktop TLS/login/session checks and evidence-grounded English and Persian answers
passed end to end; observed synthesis times at the 128-token ceiling were 56.6 and 67.1 seconds.
Visual review confirmed the English and native RTL Persian login layouts. Ruff, strict mypy and the
local suite pass with 93 tests and 5 PostgreSQL skips. The live investigation route still needs
durable run/audit linkage; WAN-block, VM-reboot, failure, sustained-load and independent recovery
acceptance remain open.

### فارسی

مسیر کنترل‌شده و دوزبانهٔ ارزیابی کاربران پیاده‌سازی و مستقر شد. مهمان برنامه اکنون پنل و API
احرازهویت‌شده را پشت TLS خصوصی و Nginx اجرا می‌کند و وضعیت هویت و نشست در PostgreSQL 16 نگه‌داری
می‌شود. ارتباط با هوش مصنوعی و اتصال از دو تونل SSH جدا، با کلید میزبان ثابت‌شده و مقصد محدود
می‌گذرد؛ اعتبارنامهٔ این سرویس‌ها هرگز به مرورگر نمی‌رسد. مسیرهای راه‌اندازی اولیه و بازیابی،
مستندات API و درگاه مستقیم backend از reverse proxy در دسترس نیستند.

Zabbix 7.0.30 با PostgreSQL 16، Nginx/PHP-FPM، Agent 2، TLS خصوصی و خودپایشی راه‌اندازی شد.
گذرواژهٔ مدیر پیش‌فرض تغییر کرد و یک خوانشگر مخصوص API ساخته شد که به رابط کاربری دسترسی ندارد.
نقش آن فقط `host.get`، `item.get` و `problem.get` را می‌پذیرد و گروهش فقط یک گروه میزبان مصوب را
می‌خواند. دیدن دقیقاً یک میزبان و رد روش خارج از فهرست مجاز تأیید شد. توکن فقط به‌صورت اعتبارنامهٔ
محافظت‌شدهٔ systemd روی مهمان اتصال نگه‌داری می‌شود.

اتصال فقط‌خواندنی با هویت بدون امتیاز، اعتبارسنجی سخت‌گیرانهٔ HTTPS، قرارداد نتیجهٔ محدود، اطلاعات
منبع و نسخه و زمان و تازگی، و درگاه محافظت‌شدهٔ برنامه افزوده شد. پنل اکنون بررسی مبتنی بر شاهد را
ارسال و همان شاهد را کنار پاسخ مدل محلی به فارسی یا انگلیسی نمایش می‌دهد. بررسی نسخهٔ Zabbix طبق
قرارداد API بدون احراز هویت انجام می‌شود و مسیر CPU-محور بررسی نیز مهلت صریح و کافی در Nginx دارد.

صلاحیت‌سنجی زنده هشت سنجهٔ تازهٔ خودپایشی، بدون دادهٔ قدیمی و بدون مسئلهٔ فعال بازگرداند. آزمون
سراسری TLS، ورود، نشست، دریافت شاهد و پاسخ مستند فارسی و انگلیسی موفق بود؛ زمان مشاهده‌شده با سقف
۱۲۸ توکن به‌ترتیب ۵۶٫۶ و ۶۷٫۱ ثانیه بود. نمایش انگلیسی و چیدمان طبیعی راست‌به‌چپ فارسی نیز
بازبینی دیداری شد. Ruff، mypy سخت‌گیر و مجموعهٔ محلی با ۹۳ آزمون موفق و ۵ آزمون PostgreSQL
کنارگذاشته‌شده قبول شدند. پیوند ماندگار بررسی زنده با run و ممیزی، و نیز پذیرش قطع WAN، راه‌اندازی
مجدد ماشین، خطاها، بار پایدار و بازیابی مستقل همچنان باز است.

## 2026-09-22 — Controlled Stage 1B deployment / استقرار کنترل‌شدهٔ مرحلهٔ 1B

### English

Promoted the checksummed llama.cpp runtime, Qwen model, and Python API into immutable protected
release directories on the AI guest. Installed and enabled the two hardened native systemd units
with distinct root-owned credentials. Both services run as the unprivileged `nextops-ai` identity,
listen only on `127.0.0.1:8080` and `127.0.0.1:8090`, and retain the cgroup rule that denies
non-loopback IP traffic. The effective systemd security exposure score is `2.7 OK` for each unit.

The first live start exposed two deployment defects: the relocated llama.cpp executable could not
find its adjacent shared libraries, and evaluation could begin after the socket opened but before
the model was ready. The service profile now supplies the immutable runtime library directory, and
the controlled-start procedure waits for authenticated model health. A first prompt correction
fixed missing Persian evidence but weakened an English answer; commit `62de8d6` makes the evidence
preservation rule explicit and removes the repetition penalty that contributed to that regression.

Release `nextops-0.1.0-62de8d6` is active, with `417d888` retained as the tested application
rollback. Authentication denial, readiness, all four Persian/English evidence and safety cases, and
the bounded one-active/two-queued load behavior passed. Human review accepted two independent
four-case runs. A cold process restart returned both authenticated services in 109 seconds, and the
application rollback/restoration test returned `401` for unauthenticated generation and `200` for
readiness on both releases before restoring `62de8d6`. This qualifies the controlled Stage 1B
deployment; it does not claim full Phase 1, VM-reboot, independent restore, production performance,
or Zabbix acceptance.

All four Ubuntu guests subsequently reported healthy systemd state, no failed units, no pending
package upgrade, and no reboot requirement. After a narrow package simulation, four GLib security
upgrades on the app guest were applied through its configured package proxy; the deferred affected
service was restarted and rechecked. Direct root SSH remains disabled. The owner-authorized deployment account
now has full passwordless administrative access, which is operationally powerful and must remain
protected by the private key and host-key verification.

### فارسی

محیط اجرای بررسی‌شدهٔ llama.cpp، مدل Qwen و API پایتون در شاخه‌های تغییرناپذیر و محافظت‌شدهٔ
مهمان هوش مصنوعی مستقر شدند. دو واحد سخت‌سازی‌شدهٔ systemd با دو اعتبارنامهٔ جدا، متعلق به root،
نصب و فعال شده‌اند. هر دو سرویس با شناسهٔ بدون امتیاز `nextops-ai` اجرا می‌شوند، فقط روی
`127.0.0.1:8080` و `127.0.0.1:8090` گوش می‌دهند و در سطح cgroup اجازهٔ ارتباط IP بیرون از رابط
محلی را ندارند. امتیاز مواجههٔ امنیتی مؤثر systemd برای هر واحد `2.7 OK` است.

نخستین راه‌اندازی زنده دو نقص استقرار را آشکار کرد: فایل اجرایی جابه‌جاشدهٔ llama.cpp کتابخانه‌های
مشترک کنار خود را پیدا نمی‌کرد و ارزیابی می‌توانست پس از باز شدن درگاه، اما پیش از آماده شدن مدل،
آغاز شود. مسیر کتابخانهٔ محیط اجرای تغییرناپذیر به پروفایل سرویس افزوده شد و رویهٔ شروع کنترل‌شده
اکنون تا تأیید احرازهویت‌شدهٔ سلامت مدل صبر می‌کند. اصلاح نخستِ پیام راهنما، حذف جزئیات شاهد فارسی
را برطرف کرد، اما یک پاسخ انگلیسی را تضعیف کرد؛ commit `62de8d6` الزام حفظ دقیق شاهد را صریح کرده و
جریمهٔ تکراری را که در آن پس‌رفت نقش داشت حذف می‌کند.

انتشار `nextops-0.1.0-62de8d6` فعال است و `417d888` به‌عنوان نسخهٔ آزموده‌شدهٔ بازگشت برنامه حفظ
شده است. رد درخواست بدون احراز هویت، آمادگی سرویس، هر چهار مورد فارسی و انگلیسیِ شاهد و ایمنی، و
رفتار محدودِ یک درخواست فعال و دو درخواست در صف موفق بودند. بازبینی انسانی دو اجرای مستقلِ
چهارموردی را پذیرفت. پس از توقف فرایندها، هر دو سرویس احرازهویت‌شده در ۱۰۹ ثانیه دوباره آماده شدند.
آزمون بازگشت برنامه نیز روی هر دو انتشار، کد `401` برای تولید بدون احراز هویت و `200` برای آمادگی
دریافت کرد و در پایان `62de8d6` را بازگرداند. این نتیجه، استقرار کنترل‌شدهٔ 1B را تأیید می‌کند؛ اما
به‌معنای پذیرش کامل مرحلهٔ یک، راه‌اندازی مجدد ماشین، بازیابی از نسخهٔ پشتیبان مستقل، کارایی تولیدی
یا اتصال Zabbix نیست.

در بازبینی نهایی، هر چهار مهمان Ubuntu وضعیت سالم systemd، صفر واحد خراب، صفر بستهٔ قابل‌ارتقا و
بی‌نیازی از راه‌اندازی مجدد را گزارش کردند. چهار به‌روزرسانی امنیتی مرتبط با GLib روی مهمان برنامه،
پس از شبیه‌سازی محدود، از مسیر پراکسی تنظیم‌شده نصب شد؛ سرویس به‌تعویق‌افتاده نیز دوباره راه‌اندازی و
بررسی شد. ورود مستقیم root از راه SSH همچنان بسته است. حساب استقرار بنا بر دستور صریح مالک اکنون
دسترسی مدیریتی کامل و بدون گذرواژه دارد؛ بنابراین حفاظت از کلید خصوصی و کنترل سخت‌گیرانهٔ کلید
میزبان یک الزام عملیاتی است.

## 2026-09-21 — Stage 1B native service profile / پروفایل بومی سرویس مرحلهٔ 1B

### English

Added hardened, separate native systemd units for the pinned llama.cpp runtime and authenticated
NextOps inference API. Both services bind only to loopback, use file-backed systemd credentials,
clear proxy inheritance, enforce explicit CPU/memory/task limits, restrict cgroup network access,
and run under the existing non-login `nextops-ai` identity. The inference configuration now accepts
either direct development secrets or protected credential files and rejects ambiguous, linked,
world-accessible, oversized, multiline, or whitespace-padded secret material.

Added a versioned Persian/English Stage 1B evaluation corpus and a loopback-only qualification
runner that checks unauthenticated denial, readiness, bounded bilingual cases, and an optional load
probe without claiming acceptance automatically. Added unit tests and paired English/Persian
operator guidance; updated the deployment dossier, project state, next-task record, indexes, and
installation summaries.

Focused tests, lint, strict typing, artifact/dossier/document validation, and target-side Ubuntu
24.04 systemd syntax and security review pass. No live service was installed or started. A fresh
AI-guest preflight found pending security updates, while the deployment account lacks the narrowly
authorized privilege needed for protected installation and service control; both remain explicit
gates before live evaluation.

On the AI guest, a relocatable Python 3.12 API release for source commit `5de76ac` was assembled
through the required proxy and then rebuilt from the populated cache with networking disabled. It
passed imports, `uvicorn` execution, compatibility checking for all 25 installed packages, and a
second-path relocation check. The private staging archive is 14,209,478 bytes with SHA-256
`cf20dada68f2a56eeee7608790fd32c2119ca724ce81ed1cef7ac029f00ca20b`. It was not promoted,
installed, or started; ownership normalization, dependency-license approval, an independent copy,
and service acceptance remain open.

### فارسی

برای محیط ثابت llama.cpp و API احرازهویت‌شدهٔ پردازش مدل NextOps، دو واحد جدا و سخت‌سازی‌شدهٔ
systemd افزوده شد. هر دو سرویس فقط روی رابط محلی گوش می‌دهند، اعتبارنامه را از فایل محافظت‌شدهٔ
systemd می‌خوانند، تنظیمات proxy را به ارث نمی‌برند، سقف روشن CPU و حافظه و فرایند دارند، دسترسی
شبکه‌ای آن‌ها در سطح cgroup محدود است و با هویت بدون ورود `nextops-ai` اجرا می‌شوند. پیکربندی
پردازش مدل اکنون در محیط توسعه مقدار مستقیم یا در سرویس فایل اعتبارنامه را می‌پذیرد و منبع مبهم،
پیوند نمادین، فایل قابل‌خواندن برای همگان، مقدار بیش‌ازحد بزرگ، چندخطی یا دارای فاصلهٔ اضافی را رد
می‌کند.

مجموعهٔ نسخه‌دار سنجش فارسی و انگلیسی برای مرحلهٔ 1B و یک اجراکنندهٔ فقط محلی افزوده شد. این
اجراکننده رد درخواست بدون احراز هویت، آمادگی، موارد محدود دوزبانه و در صورت انتخاب، آزمون بار را
می‌سنجد؛ اما نتیجه را خودکار «پذیرفته‌شده» اعلام نمی‌کند. آزمون‌های واحد، راهنمای متناظر فارسی و
انگلیسی و رکوردهای تحویل، وضعیت پروژه، کار بعدی، فهرست‌ها و خلاصه‌های نصب نیز به‌روز شدند.

آزمون‌های متمرکز، تحلیل ایستا، بررسی نوع‌ها، اعتبارسنجی artifact و پرونده و مستندات، و بازبینی نحو
و سخت‌سازی systemd روی Ubuntu 24.04 موفق بوده‌اند. هیچ سرویس زنده‌ای نصب یا راه‌اندازی نشد.
پیش‌بررسی تازهٔ مهمان هوش مصنوعی چند به‌روزرسانی امنیتی معوق را نشان داد و حساب استقرار نیز مجوز
محدود لازم برای نصب در مسیرهای محافظت‌شده و کنترل سرویس را ندارد؛ هر دو مورد پیش از ارزیابی زنده
دروازهٔ صریح باقی می‌مانند.

روی مهمان هوش مصنوعی، یک انتشار جابه‌جاشوندهٔ Python 3.12 برای API و commit مبدأ `5de76ac` از مسیر
proxy لازم آماده و سپس با شبکهٔ غیرفعال از cache تکمیل‌شده بازسازی شد. importها، اجرای `uvicorn`،
سازگاری هر ۲۵ بستهٔ نصب‌شده و انتقال به مسیر آزمایشی دوم موفق بودند. بایگانی خصوصی staging با
اندازهٔ ۱۴٬۲۰۹٬۴۷۸ بایت، SHA-256 برابر
`cf20dada68f2a56eeee7608790fd32c2119ca724ce81ed1cef7ac029f00ca20b` دارد. این بایگانی به مسیر
محافظت‌شده منتقل، نصب یا راه‌اندازی نشد؛ تنظیم مالکیت، تأیید مجوز وابستگی‌ها، نسخهٔ مستقل artifact و
پذیرش سرویس همچنان باز هستند.

## 2026-09-21 — Bilingual project status brief / گزارش دوزبانهٔ وضعیت پروژه

### English

Added paired presentation-ready English and native-Persian status briefs plus an editable bilingual
Word document. The brief distinguishes verified repository work, four-server qualification,
role-package preparation, and bounded local CPU model smoke evidence from the production service,
Zabbix, connector, recovery, and Internet-blocked acceptance gates that remain open.

Updated the README, documentation indexes, development and testing summaries, project state, and
next-task record to remove older statements that predated the authorized server preparation and AI
smoke test. No server, package, service, database, network, credential, model, or runtime state was
changed by this documentation update.

Revised the Persian brief and the Persian half of the Word document as native executive prose.
Translation-heavy wording and unnecessary English operational terms were replaced with consistent
formal Persian while product names, code identifiers, measured results, and acceptance boundaries
were preserved.

### فارسی

گزارش‌های متناظر و آمادهٔ ارائه به فارسی طبیعی و انگلیسی، همراه یک فایل Word دوزبانه و قابل‌ویرایش
افزوده شدند. گزارش، کار تأییدشدهٔ مخزن، صلاحیت‌سنجی چهار سرور، آماده‌سازی packageهای هر نقش و
smoke test محدود مدل محلی روی CPU را از سرویس تولید، Zabbix، connector، بازیابی و پذیرش با اینترنت
قطع‌شده که هنوز باقی مانده‌اند، جدا می‌کند.

README، فهرست‌های مستندات، خلاصه‌های توسعه و آزمون، وضعیت پروژه و رکورد کار بعدی نیز اصلاح شدند تا
عبارت‌های قدیمیِ پیش از آماده‌سازی مجاز سرورها و smoke test مدل حذف شوند. این تغییر مستندات هیچ
سرور، package، سرویس، پایگاه، شبکه، credential، مدل یا وضعیت runtime را تغییر نداد.

متن گزارش فارسی و بخش فارسی فایل Word نیز از نو و با نثر رسمیِ مناسب ارائهٔ مدیریتی ویرایش شد.
عبارت‌های ترجمه‌وار و واژه‌های انگلیسیِ غیرضروری با معادل‌های یکدست فارسی جایگزین شدند؛ در عین حال،
نام محصولات، شناسه‌های فنی، نتایج اندازه‌گیری‌شده و مرز میان آزمون مقدماتی و پذیرش عملیاتی بدون
تغییر باقی ماندند.

## 2026-09-21 — Durable repository context / حافظهٔ ماندگار مخزن

### English

Added three repository-scoped Codex skills for general NextOps context, authorized server operations,
and bilingual documentation. Added a task-routing index that catalogs every project-owned Markdown
file without loading all documents into every task. Updated `AGENTS.md` and contributing guidance to
use Git and maintained artifacts as durable memory.

The documentation validator now excludes dependency/build trees and requires complete catalog
coverage. Three focused tests verify project Markdown discovery plus missing and stale entries. No
application behavior, package, VM, network, model, database, or service was changed.

### فارسی

سه skill مخصوص مخزن برای context عمومی NextOps، عملیات مجاز سرور و مستندات دوزبانه افزوده شد.
فهرست مسیردهی تازه، همهٔ فایل‌های Markdown متعلق به پروژه را ثبت می‌کند، بدون اینکه هر بار همهٔ
سندها وارد context شوند. `AGENTS.md` و راهنمای مشارکت نیز Git و artifact نگه‌داری‌شده را حافظهٔ
ماندگار پروژه می‌دانند.

اعتبارسنج مستندات اکنون پوشه‌های وابستگی و build را حذف و پوشش کامل catalog را الزامی می‌کند. سه
آزمون متمرکز discovery و ورودی غایب یا قدیمی را می‌سنجند. رفتار برنامه، package، VM، شبکه، مدل،
پایگاه یا سرویس تغییر نکرد.

## 2026-09-20 — Phase 0 report and threat model / گزارش مرحلهٔ صفر و مدل تهدید

### English

Added paired English/Persian Phase 0 architecture, gap and readiness reports plus a repository-grounded threat model. Recorded the verified local repository state, owner-confirmed single-organization/small-start/dedicated-Zabbix context, four-VM proposal, trust and data boundaries, CPU benchmark plan, resource/storage gates, all-connector roadmap, offline/recovery tests, blockers and the smallest denial-first Stage 1A slice. Updated project state, next task, indexes and traceability without marking architecture accepted or implementation complete.

Aligned stale offline wording so the first read-only Zabbix answer is a Phase 1 outcome and Linux enrichment follows in Phase 2. Updated current clone commands to `Omid-NextAI/nextops`; preserved historical provenance that names the earlier repository. No infrastructure, model, package, network, Zabbix, ESXi or storage change was performed.

### فارسی

گزارش متناظر فارسی و انگلیسی مرحلهٔ صفر دربارهٔ معماری، فاصله‌ها و آمادگی و نیز مدل تهدید مبتنی بر مخزن افزوده شد. وضعیت واقعی مخزن، فرض‌های تأییدشدهٔ تک‌سازمانی و شروع کوچک و Zabbix مستقل، چیدمان چهارماشینی، مرز اعتماد و داده، برنامهٔ سنجش CPU، کنترل منابع و دیسک، نقشهٔ همهٔ اتصال‌ها، آزمون آفلاین و بازیابی، موانع و کوچک‌ترین برش 1A با رد پیش‌فرض ثبت شدند. وضعیت پروژه، کار بعدی، فهرست‌ها و ردیابی بدون ادعای پذیرش معماری یا تکمیل پیاده‌سازی به‌روز شدند.

عبارت قدیمی راهنمای آفلاین اصلاح شد تا پاسخ فقط‌خواندنی نخست Zabbix خروجی مرحلهٔ یک و بررسی مستقیم Linux در مرحلهٔ دو باشد. فرمان‌های clone جاری به `Omid-NextAI/nextops` تغییر کردند و سابقهٔ تاریخی نام پیشین حفظ شد. هیچ زیرساخت، مدل، بسته، شبکه، Zabbix، ESXi یا دیسکی تغییر نکرد.

## 2026-09-20 — Startup order and Phase 1A–1E / ترتیب شروع و گام‌های مرحلهٔ یک

### English

Added English/native-Persian START_HERE guides and linked them from both documentation indexes. Revised both roadmaps and NEXT_TASK to specify the first VM order: nextops-app, nextops-ai, nextops-connectors-ro. Phase 1 is now decomposed into 1A application/safety foundation, 1B local CPU model, 1C read-only Zabbix evidence, 1D evidence-linked answer and 1E offline acceptance. VM budgets remain 8/32/200, 24/128/500 and 4/8/80 (vCPU/RAM GiB/disk GiB); corrected the stale initial 44-vCPU NEXT_TASK total to 36. Optional lab Zabbix and later database/write-executor VMs are counted separately.

Clarified remaining preflight, creation versus restart order, local service readiness, credential/network boundaries, separate disposable untrusted test environments and actual completion evidence. Updated PROJECT_STATE without marking any software phase complete. Preserved the master prompt, hardware evidence, existing diagrams, repository settings and G10 configuration. This is a documentation-only change; no VM, model, Zabbix or offline acceptance test was run. Direct clone was unavailable because GitHub hostname resolution failed in the editing environment; connected API reads/writes remained available.

### فارسی

راهنمای متناظر START_HERE و پیوند آن در هر دو فهرست اضافه شد. نقشه‌های راه و NEXT_TASK ترتیب ساخت را روشن می‌کنند: ابتدا برنامه، سپس AI و بعد اتصال فقط‌خواندنی. مرحلهٔ یک به 1A پایهٔ برنامه و ایمنی، 1B مدل CPU محلی، 1C شواهد فقط‌خواندنی Zabbix، 1D پاسخ دارای منبع و 1E پذیرش آفلاین تقسیم شد. منابع ماشین‌ها همان ۸/۳۲/۲۰۰، ۲۴/۱۲۸/۵۰۰ و ۴/۸/۸۰ با واحد vCPU، حافظهٔ GiB و دیسک GiB هستند؛ مجموع قدیمی ۴۴ vCPU در NEXT_TASK به ۳۶ اصلاح شد. نمونهٔ آزمایشگاهی Zabbix و ماشین‌های پایگاه و اجرای تغییرِ مراحل بعد جدا حساب می‌شوند.

پیش‌نیازهای باقی‌مانده، تفاوت ترتیب ساخت و شروع سرویس، آمادگی محلی، مرز اطلاعات ورود و شبکه، محیط موقت جدا برای آزمون غیرقابل‌اعتماد و شواهد پایان مشخص شدند. PROJECT_STATE بدون کامل اعلام کردن مرحلهٔ نرم‌افزاری به‌روز شد. پرامپت، شاهد سخت‌افزار، نمودارها، تنظیمات مخزن و G10 حفظ شدند. تغییر فقط مستندات است؛ هیچ آزمون VM، مدل، Zabbix یا پذیرش آفلاین اجرا نشد. clone مستقیم به‌دلیل نام‌یابی GitHub در محیط ویرایش ممکن نبود؛ اتصال API برای خواندن و نوشتن موجود بود.

## 2026-09-20 — Diagrams and technology choices / نمودارها و انتخاب فناوری

### English

Added paired `DIAGRAMS.md` and `TECH_STACK.md` guides. Seven Mermaid views per language cover system context, single-host deployment zones, read-only investigation, future exact-action approvals, conceptual data relationships, CPU scheduling and release delivery. Both READMEs now include an overview diagram, a stack summary and direct navigation. Both documentation indexes and project state are updated.

The stack guide separates the existing specification from supplemental recommendations, core choices from feature-gated tools, and local CPU candidates from unmeasured performance claims. It includes official references and RTL-aware frontend guidance. The master prompt, original requirement scope, repository visibility, host configuration and application implementation remain unchanged. Local guide-structure checks and rendering limitations are recorded in `docs/VISUAL_REVIEW.md`.

### فارسی

راهنماهای متناظر `DIAGRAMS.md` و `TECH_STACK.md` اضافه شدند. هفت نمودار در هر زبان نمای سامانه، ناحیه‌های استقرار روی یک میزبان، بررسی فقط‌خواندنی، تأیید دقیق اصلاحات آینده، ارتباط مفهومی داده‌ها، زمان‌بندی CPU و مسیر انتشار را پوشش می‌دهند. هر دو README اکنون نمودار خلاصه، جدول فناوری و پیوند مستقیم دارند. فهرست‌های مستندات و وضعیت پروژه نیز به‌روز شدند.

راهنمای فناوری‌ها مبنای موجود را از پیشنهاد تکمیلی، ابزار اصلی را از گزینهٔ وابسته به نیاز و نامزد مدل CPU را از ادعای کاراییِ سنجیده‌نشده جدا می‌کند. منابع رسمی و راهنمای رابط سازگار با RTL اضافه شده‌اند. پرامپت، دامنهٔ نیازهای اولیه، وضعیت عمومی مخزن، تنظیمات میزبان و پیاده‌سازی برنامه تغییر نکرده‌اند. کنترل ساختار راهنماها و محدودیت بررسی نمایش در `docs/VISUAL_REVIEW.md` ثبت شده است.

## 2026-09-20 — Documentation baseline / پایهٔ مستندات

### English

Initialized the existing empty `AmirMo10/nextops` repository without changing its public visibility. Added English and native-Persian documentation, architecture and execution boundaries, CPU-only evaluation plan, all eleven integration contracts, data/API/UI design, phases 0–8, security/testing/recovery requirements, traceability for all 51 original sections, agent/contributor rules and review templates. Retained the supplied master prompt without a new translation. Added a local documentation-structure checker.

No application, model deployment, G10 inspection, benchmark, real-device integration or production service is delivered by this baseline. Repository settings such as branch protection, Actions and private vulnerability reporting are not asserted to be configured.

### فارسی

مخزن خالیِ موجود `AmirMo10/nextops` بدون تغییر وضعیت عمومی آن مقداردهی شد. راهنماهای انگلیسی و فارسی، معماری و مرز اجرا، برنامهٔ ارزیابی CPU-only، قرارداد یازده اتصال، طراحی داده و API و رابط، مراحل صفر تا هشت، نیازهای امنیت و آزمون و بازیابی، ردیابی ۵۱ بخش اولیه، قواعد عامل و مشارکت و قالب بازبینی اضافه شدند. پرامپت دریافت‌شده بدون ترجمهٔ جدید حفظ شد و ابزار بررسی ساختار مستندات افزوده شد.

این نسخه برنامه، مدل مستقر، بررسی سرور G10، آزمون کارایی، اتصال واقعی یا سرویس عملیاتی تحویل نمی‌دهد. تنظیم بودن حفاظت شاخه، Actions یا گزارش خصوصی آسیب‌پذیری نیز ادعا نمی‌شود.
