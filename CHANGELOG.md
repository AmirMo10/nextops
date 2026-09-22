# Changelog / تاریخچهٔ تغییرات

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
