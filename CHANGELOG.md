# Changelog / تاریخچهٔ تغییرات

## Unreleased — controlled engineering foundation / بنیان مهندسی کنترل‌شده

### English

Closed credential-bearing HTTP redirect forwarding in the application/connector transports,
with a local 302 regression test that proves no second request. Commit `cdde129` passed all five
hosted CI jobs and was deployed as immutable app, AI API and connector releases
`nextops-0.1.0-cdde129` from SHA-256-verified offline wheels. Fresh WAN-denied bilingual browser
acceptance passed. All four serving guests now require key-only, non-root SSH; new handshakes and
restarted protected tunnels passed. The AI guest's UFW was enabled with a guarded rollback and
now matches the other guests' deny-incoming/OpenSSH policy. The owner confirmed that independent
recovery resources, licensing, notification delivery, replacement CA certificates and named
approvers are unavailable, so this remains controlled user testing rather than production
acceptance.

Audited WAN claims separately from live policy: the earlier four-guest denial was temporary and
removed after acceptance. Direct public IPv4 remains reachable from host shells, although the
app/AI/model units deny non-loopback IP egress. The connector now has a tested process-only LAN
allowlist; host-wide egress control remains partial pending a safe local DNS/time/maintenance-proxy
allowlist.

Added a parameterized connector systemd egress template without publishing the deployment LAN.
The live connector denies all IP destinations except loopback and its reviewed LAN. Four fresh
authenticated Zabbix-plus-Linux investigations passed under that policy, and a controlled public
HTTPS probe failed with the policy while the same destination answered without it. The connector
remained healthy and its guarded rollback was cancelled. This does not restrict general host
processes or replace independent recovery.

Aligned Zabbix Agent 2 on the app, AI and connector guests from `7.0.30` to the server's `7.0.31`
using the cached, repository-hash-matched package and serial offline installs. Each original
configuration hash remained stable; all four agents are active at `7.0.31`, with no passive
listener or pending reboot. A fresh WAN-denied browser monitoring run passed afterward. The three
offline-installed agents still need an explicit patch-import process for later releases.

Completed the safe portion of production hardening on the four existing serving guests under
change `production-hardening-20260926-01`. Serial updates used root-only exact-version rollback
packages, candidate-package manifests and verified local PostgreSQL safety dumps. Every guest now
reports `running`, zero failed units, zero pending packages and no reboot marker; Zabbix is
`7.0.31` and both PostgreSQL deployments remain `16.15`. A corrected WAN-denied Edge gate passed
fresh bilingual login, local general AI, evidence-grounded monitoring, provenance, server-side
session revocation and new-tab isolation. The harness now waits for asynchronous logout completion
and requires HTTP `204` instead of racing the unchanged deployed UI.

Generated private SPDX/CycloneDX SBOMs from the exact deployed application archive with
digest-verified Syft `1.52.0`; production dependency audit with `pip-audit 2.10.1` reported zero
known findings in 25 dependencies. The inventory identified the missing NextOps project license.
Independent recovery/restore infrastructure, a real named-recipient local notification route,
replacement CA-issued certificate pairs and custody, complete vulnerability/offline-signature
evidence, legal/security approval and final human production acceptance remain open. The local
rollback material is not represented as independent backup.

Added the bounded answer-integrity increment without changing the read-only architecture. General
answers now carry explicit model-only limitations, and current infrastructure questions cannot be
answered from model memory. Live monitoring and incident answers use consistent nested evidence
labels and pass deterministic checks for fabricated execution, unsupported root cause, missing
source identity and omitted stale/partial qualifiers before persistence. A failed check produces a
bilingual deterministic summary from typed evidence and excludes untrusted source names. The UI
explains unverified, evidence-bounded, fallback and redirect outcomes. The protected local
evaluation corpus now has eight balanced English/Persian cases with automated lexical safety gates
and retained human semantic review. At that checkpoint the owner deferred recovery work and
confirmed that no SMTP host existed; neither recovery nor notification delivery was claimed by that
increment.

Hosted CI passed all five jobs for the final source. Immutable application release
`nextops-0.1.0-2397581` and inference API release `nextops-0.1.0-fd3c353` were promoted with prior
releases preserved. The final private eight-case loopback corpus passed automated and engineering
semantic review. Live authenticated application checks passed greeting relevance, deterministic
current-status redirect, monitoring synthesis, composite incident fallback, evidence metadata and
test-session revocation. A serial reboot of all four guests loaded kernel `6.8.0-142`; each returned
running with zero failed units and no reboot marker. Pending Ubuntu and Zabbix 7.0.31 packages were
not fetched without the approved proxy/offline path.

Added paired English/Persian owner runbooks for every remaining production blocker. The guides map
the four machine-readable recovery blockers plus certificate delivery/rotation, supply-chain
approval and final production sign-off to explicit owner and engineering responsibilities. They
include a private decision template, independent recovery-host and restore-lab requirements, safe
capacity and SSH identity commands, recommended RPO/RTO/retention values, two-person key custody,
local Zabbix notification setup, protected certificate handoff, SBOM/license policy, stop
conditions and the exact sanitized checklist to return. No live infrastructure changed and no gate
was promoted by this documentation.

Completed controlled acceptance of the bounded local certificate-lifecycle detection increment. A dependency-free Python checker uses
the pinned local OpenSSL binary and system clock to classify healthy, warning-window, expired and
not-yet-valid certificates, emitting only bounded public metadata. A hardened daily systemd timer
runs as a dedicated non-login identity with no network access and read permission for the public
certificate only; the private key remains root-only. The guarded installer verifies the
certificate/key match without printing either, installs non-secret configuration and fails unless
the timer and immediate check succeed. Thirteen focused parser/state tests and static unit/installer
checks are present. Commit `f540a9d` passed all five hosted CI jobs; change
`certificate-lifecycle-20260923-01` then installed the artifacts on both TLS frontends. Both timers
are enabled and active, both services scored `2.7 OK`, and the checker identities can read the
public certificates but not either root-owned mode-`0600` key. Both live certificates are healthy
under the 90-day policy; isolated one-day and malformed certificates returned `expiring` and
`error`. Four active-agent items and six tagged local Zabbix triggers now observe service result,
timer state and missing data. A guarded timer outage produced a problem and its recovery returned
all triggers to healthy with fresh values from both hosts. Normal TLS remained valid with no
external frontend requests. Operator notification delivery and an observed rotation/rollback drill
remain pending, so production acceptance is unchanged.

Closed and deployed the session-termination gap. The panel now calls an audited server-side logout
endpoint before clearing its tab-local bearer. PostgreSQL revokes exactly the presented session
under a row lock, emits one correlated append-only event, leaves other sessions valid and treats
replay or an unknown token idempotently without exposing a token-existence oracle. API, integration
and real-browser coverage verifies denial without a bearer, empty `204`, single-session isolation,
one audit event, local-token removal and localized return to login. All five hosted CI jobs passed;
immutable application release `nextops-0.1.0-eb57241` then passed live API and normal-TLS browser
logout, former-token rejection, second-session preservation and idempotent replay. Release
`nextops-0.1.0-54c8bb4` remains available for rollback; no schema migration was required.
A fresh full Phase 2 browser rerun on the promoted release also passed bilingual incident
generation, combined evidence provenance, durable audit identifiers, RTL mobile layout, audited
logout, new-tab isolation and zero external page requests under the WAN-deny proxy.

Added the guarded source contract for the next recovery phase without changing serving VMs. ADR
0008 proposes separate pgBackRest repositories for the application and Zabbix PostgreSQL 16
clusters and limits restic to approved non-database files. A schema-validated public profile,
validator, eight focused tests and CI checks reject duplicate YAML keys, shared database
repositories, secret-like material, database/WAL input to restic, and unsupported production
claims. The profile is intentionally valid but blocked: no independent destination, approved
RPO/RTO/retention, verified offline tool bundle, PITR, file restore, negative test or key-recovery
evidence exists yet. No package or backup job was installed on the live guests.

Completed controlled Phase 2 qualification against the live four-VM deployment. A fresh Edge
context used normal TLS verification and a deny proxy limited to the private application origin;
English and Persian incident investigations returned combined Zabbix/Linux provenance and durable
run/evidence/audit identifiers, with RTL mobile, logout, new-tab isolation and no application WAN
requests. A guarded connector outage returned a safe localized `503` while general local AI stayed
available, then monitoring and a fresh audited incident recovered. Zabbix, connector, AI and app
rebooted serially, returned their role health with zero failed units, and a fresh post-reboot
bilingual browser investigation passed.

The first live incident request exposed a reverse-proxy timeout defect: the Phase 2 endpoint fell
through to Nginx's 30-second default while CPU inference was still active. The versioned Nginx
profile now includes `/api/v1/incidents/investigate` in the bounded 180-second assistant location,
and the static proxy test prevents regression. Nginx validation and reload passed before the live
gate was repeated. Phase 2 is qualified for controlled user testing, not production; independent
backup, WAL/PITR, certificate lifecycle and disaster-recovery acceptance remain open.

Refined the controlled user-testing console from a development-only Figma foundation containing
the exact OCS palette, 48 design variables, 11 bilingual text styles and two elevation styles. The
implemented workspace now uses the shared spacing/radius scale, numbered answer-mode cards, compact
status pills, a high-contrast protected evidence boundary and a branded result accent. Application
behavior, authorization, evidence contracts and offline delivery are unchanged; no package or
external runtime asset was added. Focused API and real-browser checks pass for English desktop,
composite incident evidence, Persian RTL, reduced motion and 375-pixel mobile width. The Figma
Starter-plan MCP quota stopped complete product-screen composition, which is recorded without
claiming a finished Figma screen library; reviewed source remains authoritative.
All five jobs in GitHub Actions run `35838156738` passed. The exact source was promoted under change
`ui-figma-foundation-20260923-01` as immutable application release
`nextops-0.1.0-54c8bb4`; the prior `nextops-0.1.0-8d042cf` release remains available for rollback.
The deployed English desktop and Persian RTL mobile login checks passed with no horizontal
overflow, external request, failed response or console error. Application, AI tunnel, Nginx and
PostgreSQL 16 services were active with zero failed units and no post-promotion warnings. This
narrow deployed-login smoke check does not claim the still-unrun authenticated Phase 2 browser gate.

Redesigned the controlled user-testing frontend around the verified OCS identity: the exact company
mark is embedded for offline use, the OCS gold/teal palette now drives a light enterprise console,
and the same local artwork supplies the browser icon. General, monitoring and incident behavior,
evidence/audit identifiers and 128-token bounds are unchanged. The browser fixture passes English
LTR, Persian RTL, reduced motion, responsive mobile/desktop layouts and zero external asset
requests. The final source passed all five CI jobs and was promoted under change
`ui-ocs-brand-20260923-02` as immutable application release `nextops-0.1.0-8d042cf`. A fresh deployed
login check passed English desktop and Persian RTL at 375 pixels with no horizontal overflow,
external request, failed response or console error. This does not claim the still-unrun
authenticated Phase 2 live-browser gate.

Deployed Phase 2A under change `phase2a-incident-context-20260923-01` as immutable app and connector
release `nextops-0.1.0-1ab6586`. The Zabbix reader now permits exactly `host.get`, `item.get`,
`problem.get`, `history.get` and `event.get`; unrelated methods and all mutations remain denied. A
live Zabbix 7.0.30 request returned eight current metrics and 32 bounded history points with explicit
truncation reasons. Connector/application authentication boundaries, the protected tunnel,
release/role rollback and forward recovery, and guarded IPv4/IPv6 WAN isolation passed. The
temporary firewall table and rollback timers were removed and normal outbound state was restored.
Authenticated browser use, durable model/audit linkage, VM reboot and direct Linux diagnostics were
not run and are not claimed.

Started Phase 2 with a specification-bounded Zabbix incident-context increment. The connector now
builds a typed current-summary, recent numeric-history and trigger-event response for its single
configured host, with a 15–1,440-minute deployment window, four-metric/eight-point/25-event public
ceilings, source timestamps and explicit partial reasons. Authenticated connector and application
routes are additive; no arbitrary method, host selector, write operation, credential exposure,
direct Linux access or database migration was introduced.

Focused connector/API tests, Ruff and strict mypy passed at the source milestone. English and
Persian state, API, configuration, integration, testing and roadmap documents distinguished source
evidence from live acceptance. The later controlled deployment results are recorded above; durable
model/browser linkage, VM reboot and direct Linux diagnostics remain not run. The independent Phase
1 recovery destination and WAL/PITR blocker is unchanged.

Completed the executable controlled Stage 1 qualification under change
`stage1-completion-20260922-01`: a fresh WAN-denied Edge workflow, application and runtime/model
rollback, cancellation and dependency recovery, fail-closed missing/corrupt model behavior, an
isolated low-space staging failure, a five-minute bounded load profile, and socket-only logical
restores of the NextOps and Zabbix PostgreSQL 16 databases. All temporary restore and failure-test
resources were removed, and all four guests ended `running` with zero failed units.

Locked Playwright 1.63 as a development-only dependency and added the reproducible private-origin
browser harness. The release manifest and paired English/Persian reports now mark browser, rollback,
failure recovery, sustained load and isolated logical restore as passed. Independent backup remains
partial and production acceptance remains not run: no verified destination survives loss of the
serving guest, DS-C/G10 and host, and WAL/PITR/restic recovery still requires implementation.

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

Local validation passes Ruff format/lint, strict mypy over 59 source files, 103 non-integration tests,
documentation validation for 104 Markdown files and 32 bilingual guide pairs, release/deployment/
inference/installer validators, package build, locked-dependency audit, Gitleaks and pedantic
Zizmor 1.29.0 with no findings. The six
PostgreSQL integration tests retain prior isolated-database evidence but were not rerun in this
Windows session because no local server or working container runtime was available.

### فارسی

انتقال احتمالی اطلاعات احراز هویت در پی تغییرمسیر HTTP برای ارتباط برنامه و اتصال‌دهنده بسته شد؛
آزمون بازگشت محلی با پاسخ `302` ثابت می‌کند درخواست دوم ساخته نمی‌شود. تغییر `cdde129` هر پنج کار
CI را گذراند و با wheelهای آفلاینِ تطبیق‌داده‌شده با SHA-256 به‌صورت انتشار تغییرناپذیر
`nextops-0.1.0-cdde129` برای برنامه، API هوش مصنوعی و اتصال‌دهنده مستقر شد. پذیرش مرورگر تازهٔ
دوزبانه با WAN مسدود موفق بود. چهار مهمان اکنون SSH را فقط با کلید و بدون ورود مستقیم root
می‌پذیرند؛ اتصال‌های تازه و تونل‌های محافظت‌شدهٔ بازراه‌اندازی‌شده آزموده شدند. UFW میزبان AI با
حفاظ بازگشت فعال شد و سیاست رد ورودی به‌جز OpenSSH را مانند سایر مهمان‌ها دارد. مالک اعلام کرد
منابع مستقل بازیابی، تصمیم مجوز، تحویل اعلان، گواهی جایگزین CA و تأییدکنندگان نام‌دار هنوز موجود
نیستند؛ بنابراین وضعیت، ارزیابی کنترل‌شدهٔ کاربران است و پذیرش تولید نیست.

ادعای WAN از سیاست زنده جدا بررسی شد: منع خروجی چهار مهمان در آزمون پیشین موقت بود و پس از پذیرش
برداشته شد. IPv4 عمومی از پوستهٔ میزبان هنوز در دسترس است، هرچند واحدهای برنامه، AI و مدل خروجی
غیر-loopback را رد می‌کنند. اتصال‌دهنده اکنون فهرست مجازِ آزموده‌شدهٔ شبکهٔ داخلی را در سطح
فرایند دارد؛ کنترل خروجی کل میزبان تا تعیین فهرست ایمن DNS، زمان و پراکسی نگه‌داری ناقص می‌ماند.

الگوی پارامتری سیاست خروجی systemd برای اتصال‌دهنده، بدون ثبت بازهٔ واقعی شبکه در مخزن، افزوده شد.
اتصال‌دهندهٔ زنده اکنون همهٔ مقصدهای IP به‌جز loopback و شبکهٔ داخلیِ بازبینی‌شده را رد می‌کند.
چهار بررسی تازه و احرازهویت‌شده با شواهد Zabbix و Linux زیر این سیاست موفق شدند؛ آزمون کنترل‌شدهٔ
HTTPS عمومی با همان سیاست شکست خورد، در حالی که همان مقصد بدون سیاست پاسخ داد. سرویس سالم ماند و
حفاظ بازگشت لغو شد. این تغییر فرایندهای عمومی میزبان را محدود و جای بازیابی مستقل را پر نمی‌کند.

Agent 2 زبیکس روی مهمان‌های برنامه، AI و اتصال‌دهنده با بستهٔ موجود و دارای هش مطابق فرادادهٔ
مخزن، به‌صورت آفلاین و ترتیبی از `7.0.30` به `7.0.31` سرور رسید. هش تنظیمات اصلی ثابت ماند؛ هر
چهار عامل با نسخهٔ `7.0.31` فعال‌اند و شنوندهٔ منفعل یا نیاز به reboot ندارند. آزمون تازهٔ مرورگر
و پایش با WAN مسدود پس از ارتقا موفق بود. ورود وصلهٔ نسخه‌های بعدی برای سه عامل آفلاین باید صریح
و بازبینی‌شده باشد.

بخش ایمن سخت‌سازی تولید روی چهار مهمان موجود با تغییر `production-hardening-20260926-01` تکمیل
شد. به‌روزرسانی ترتیبی با بسته‌های دقیق بازگشت، فهرست بسته‌های نامزد و dump محلی و بررسی‌شدهٔ
PostgreSQL در مسیرهای فقط‌خواندنی برای root انجام شد. اکنون هر چهار مهمان `running` هستند و واحد
خراب، بستهٔ در انتظار یا نشانگر reboot ندارند؛ Zabbix نسخهٔ `7.0.31` و هر دو PostgreSQL نسخهٔ
`16.15` هستند. دروازهٔ اصلاح‌شدهٔ Edge با WAN مسدود، ورود تازهٔ دوزبانه، AI عمومی محلی، پایش
مستند، منشأ، لغو نشست در سرور و جداسازی برگهٔ تازه را گذراند. ابزار به‌جای رقابت با رابط مستقر و
بدون تغییر، اکنون پایان خروج ناهمگام و HTTP `204` را الزام می‌کند.

SBOMهای خصوصی SPDX و CycloneDX از بایگانی دقیق برنامهٔ مستقر با Syft نسخهٔ `1.52.0` و digest
تأییدشده ساخته شدند؛ ممیزی وابستگی تولید با `pip-audit 2.10.1` در ۲۵ وابستگی یافتهٔ شناخته‌شده‌ای
نداشت. موجودی نبود مجوز پروژهٔ NextOps را روشن کرد. زیرساخت مستقل بازیابی و restore، مسیر واقعی
اعلان داخلی با گیرندهٔ نام‌دار، جفت گواهی تازهٔ CA و حضانت، شاهد کامل آسیب‌پذیری و امضای آفلاین،
تأیید حقوقی و امنیتی و پذیرش نهایی انسانی تولید همچنان بازند. مادهٔ بازگشت محلی پشتیبان مستقل
معرفی نمی‌شود.

بخش محدود «صحت پاسخ» بدون تغییر معماری فقط‌خواندنی افزوده شد. پاسخ عمومی اکنون محدودیت نداشتن
شاهد زنده را به‌صراحت اعلام می‌کند و پرسش دربارهٔ وضعیت فعلی زیرساخت از حافظهٔ مدل پاسخ داده
نمی‌شود. برچسب شاهد در پاسخ داخلی حالت پایش و رخداد با پاسخ بیرونی یکسان است و پیش از ذخیره،
ادعای اجرای عملیات، علت ریشه‌ای بی‌پشتوانه، نبود نام منبع و پنهان‌شدن شاهد قدیمی یا ناقص به‌صورت
قطعی بررسی می‌شود. در صورت شکست، متن مدل با خلاصهٔ دوزبانهٔ ساخته‌شده از قرارداد معتبر شاهد
جایگزین می‌شود و نام‌های تحت کنترل منبع در آن تکرار نمی‌شوند. رابط نتیجهٔ بدون راستی‌آزمایی،
محدود به شاهد، جایگزین قطعی و هدایت به حالت زنده را توضیح می‌دهد. مجموعهٔ ارزیابی محلی اکنون هشت
مورد متوازن فارسی و انگلیسی با کنترل واژگانی خودکار و بازبینی معنایی انسانی دارد. در آن نقطه مالک
کارهای بازیابی را موقتاً کنار گذاشته و اعلام کرده بود میزبان SMTP در دسترس نیست؛ آن تغییر هیچ
ادعایی دربارهٔ بازیابی یا تحویل اعلان نداشت.

هر پنج کار CI برای منبع نهایی موفق بود. انتشار تغییرناپذیر برنامه
`nextops-0.1.0-2397581` و انتشار API هوش مصنوعی `nextops-0.1.0-fd3c353` با حفظ نسخه‌های قبلی
ارتقا یافتند. مجموعهٔ خصوصی و نهایی هشت‌موردی loopback، کنترل خودکار و بازبینی معنایی مهندسی را
گذراند. آزمون زنده و احرازهویت‌شدهٔ برنامه، مرتبط‌بودن سلام، هدایت قطعی پرسش وضعیت فعلی، جمع‌بندی
پایش، پاسخ جایگزین رخداد ترکیبی، فرادادهٔ شاهد و لغو نشست آزمایشی را تأیید کرد. reboot ترتیبی هر
چهار مهمان kernel `6.8.0-142` را بار کرد و همه با وضعیت running، صفر واحد خراب و بدون نشانگر reboot
بازگشتند. بسته‌های در انتظار Ubuntu و Zabbix 7.0.31 بدون مسیر مصوب پراکسی یا بستهٔ آفلاین دریافت
نشدند.

راهنمای جفت انگلیسی و فارسی برای همهٔ موانع باقی‌ماندهٔ تولید افزوده شد. این راهنما چهار مانع
ماشین‌خوان بازیابی را همراه تحویل و چرخش گواهی، تأیید زنجیرهٔ تأمین و امضای نهایی تولید به مسئولیت
روشن مالک و مهندسی نگاشت می‌کند. قالب تصمیم خصوصی، نیاز میزبان مستقل و آزمایشگاه restore، فرمان‌های
امن ظرفیت و هویت SSH، مقدارهای پیشنهادی RPO/RTO و نگه‌داری، حضانت دونفرهٔ کلید، اعلان محلی Zabbix،
تحویل محافظت‌شدهٔ گواهی، سیاست SBOM/مجوز، شرط توقف و checklist پالایش‌شدهٔ پاسخ در آن آمده است.
هیچ زیرساخت زنده‌ای تغییر نکرد و این مستندسازی وضعیت هیچ دروازه‌ای را ارتقا نداد.

پذیرش کنترل‌شدهٔ increment محدود تشخیص چرخهٔ محلی گواهی تکمیل شد. ابزار Python بدون وابستگی تازه، با OpenSSL ثابت و محلی
و ساعت سامانه، گواهی را در یکی از حالت‌های سالم، واردشده به بازهٔ هشدار، منقضی یا هنوز نامعتبر
قرار می‌دهد و فقط فرادادهٔ عمومی و محدود می‌نویسد. timer روزانه و سخت‌سازی‌شده با هویت مستقل و
بدون ورود یا دسترسی شبکه اجرا می‌شود؛ این هویت فقط گواهی عمومی را می‌خواند و کلید خصوصی فقط برای
root می‌ماند. installer محافظت‌شده، بدون چاپ محتوا تطبیق گواهی و کلید را بررسی، تنظیم غیرمحرمانه
را نصب و در صورت موفق‌نبودن timer و اجرای فوری متوقف می‌شود. سیزده آزمون متمرکز parser و وضعیت و
کنترل‌های ایستای واحد و installer افزوده شدند. commit `f540a9d` هر پنج کار CI را گذراند و تغییر
`certificate-lifecycle-20260923-01` آن را روی هر دو رابط TLS نصب کرد. هر دو timer فعال و enabled،
امتیاز سخت‌سازی هر دو سرویس `2.7 OK` و دسترسی هویت checker به هر دو کلید خصوصی رد است. گواهی‌های
زنده با سیاست ۹۰روزه سالم‌اند و fixture یک‌روزه و ورودی خراب به‌ترتیب `expiring` و `error` دادند.
چهار item فعال و شش trigger برچسب‌دار Zabbix وضعیت سرویس، timer و نبود داده را پایش می‌کنند؛ قطع
محافظت‌شدهٔ timer مشکل ساخت و بازیابی آن همهٔ triggerها را سالم کرد. TLS عادی بدون درخواست بیرونی
معتبر ماند. تحویل اعلان به بهره‌بردار و تمرین چرخش/بازگشت هنوز باقی‌اند؛ پذیرش تولید تغییری نکرد.

شکاف پایان‌دادن نشست بسته و مستقر شد. پنل اکنون پیش از پاک‌کردن bearer محلی برگه، مسیر ممیزی‌شدهٔ
خروج در سمت سرور را فراخوانی می‌کند. PostgreSQL فقط همان نشست ارائه‌شده را زیر قفل سطر لغو، یک
رویداد فقط‌افزودنی و دارای شناسهٔ هم‌بستگی ثبت و نشست‌های دیگر را معتبر نگه می‌دارد؛ تکرار درخواست
یا توکن ناشناخته نیز بدون افشای وجود توکن به‌صورت idempotent پاسخ می‌گیرند. پوشش API، یکپارچگی و
مرورگر واقعی، رد درخواست بدون bearer، پاسخ خالی `204`، جداسازی یک نشست، یک رویداد ممیزی، حذف توکن
محلی و بازگشت بومی‌شده به ورود را می‌سنجد. هر پنج کار CI میزبانی‌شده موفق شدند؛ سپس انتشار
تغییرناپذیر `nextops-0.1.0-eb57241` خروج زنده در API و مرورگر با TLS عادی، رد توکن پیشین، حفظ
نشست دوم و تکرار بدون اثر اضافی را گذراند. انتشار `nextops-0.1.0-54c8bb4` برای بازگشت حفظ شده است
و migration پایگاه لازم نبود.
بازاجرای کامل و تازهٔ مرورگر مرحلهٔ دو روی انتشار ترویج‌شده نیز تولید دوزبانهٔ رخداد، منشأ ترکیبی
شواهد، شناسه‌های ماندگار ممیزی، چیدمان موبایل راست‌به‌چپ، خروج ممیزی‌شده، جداسازی برگهٔ تازه و نبود
درخواست بیرونی صفحه زیر پراکسی مسدودکنندهٔ WAN را گذراند.

قرارداد محافظت‌شدهٔ مرحلهٔ بعدی بازیابی بدون تغییر VMهای سرویس‌دهنده افزوده شد. ADR 0008 برای دو
خوشهٔ PostgreSQL 16 برنامه و Zabbix مخزن‌های جداگانهٔ pgBackRest پیشنهاد می‌کند و restic را به
فایل‌های غیرپایگاهی مصوب محدود نگه می‌دارد. پروفایل عمومی دارای schema، validator، هشت آزمون
متمرکز و کنترل CI، کلید تکراری YAML، مخزن مشترک دو پایگاه، مادهٔ شبیه راز، ورود داده یا WAL پایگاه
به restic و ادعای بی‌پشتوانهٔ تولید را رد می‌کنند. پروفایل عمداً معتبر اما مسدود است: هنوز مقصد
مستقل، RPO/RTO و نگه‌داری مصوب، بستهٔ آفلاین معتبر ابزارها، PITR، بازیابی فایل، آزمون منفی یا شاهد
بازیابی کلید وجود ندارد. هیچ بسته یا job پشتیبان روی مهمان‌های زنده نصب نشد.

صلاحیت‌سنجی کنترل‌شدهٔ مرحلهٔ دو روی استقرار زندهٔ چهارماشینی تکمیل شد. یک نشست تازهٔ Edge با
اعتبارسنجی عادی TLS و پراکسیِ مسدودکننده‌ای اجرا شد که فقط مبدأ خصوصی برنامه را مستثنا می‌کرد.
بررسی رخداد به فارسی و انگلیسی، منشأ ترکیبی Zabbix/Linux و شناسه‌های ماندگار اجرا، شاهد و ممیزی را
برگرداند؛ نمایش موبایل راست‌به‌چپ، خروج، جداسازی برگهٔ تازه و نبود درخواست WAN از برنامه نیز موفق
بود. هنگام توقف محافظت‌شدهٔ اتصال‌دهنده، بررسی رخداد خطای امن و بومی‌شدهٔ `503` داد و دستیار عمومی
محلی فعال ماند؛ سپس پایش و بررسی تازهٔ ممیزی‌شده بازیابی شدند. Zabbix، اتصال‌دهنده، هوش مصنوعی و
برنامه یکی‌یکی reboot شدند، سلامت هر نقش با صفر واحد خراب بازگشت و بررسی دوزبانهٔ تازه پس از reboot
موفق بود.

نخستین درخواست زندهٔ رخداد یک نقص مهلت در پراکسی معکوس را آشکار کرد: مسیر مرحلهٔ دو هنگام ادامهٔ
استنتاج CPU به مهلت پیش‌فرض ۳۰ثانیه‌ای Nginx می‌افتاد. پروفایل نسخه‌دار اکنون
`/api/v1/incidents/investigate` را در محل محدود ۱۸۰ثانیه‌ای دستیار قرار می‌دهد و آزمون ایستای
پراکسی از بازگشت نقص جلوگیری می‌کند. اعتبارسنجی و بارگذاری مجدد Nginx پیش از تکرار دروازهٔ زنده
موفق بود. مرحلهٔ دو برای ارزیابی کنترل‌شدهٔ کاربران واجد شرایط است، نه تولید؛ پشتیبان مستقل،
WAL/PITR، چرخهٔ عمر گواهی و پذیرش بازیابی بحران همچنان بازند.

ظاهر کنسول ارزیابی کنترل‌شده با تکیه بر یک مبنای طراحی در Figma بهبود یافت. این مبنا رنگ‌های دقیق
OCS، چهل‌وهشت متغیر طراحی، یازده سبک نوشتاری دوزبانه و دو سبک سایه را ثبت می‌کند. فضای کاری اکنون
مقیاس مشترک فاصله و گوشه‌گردی، کارت‌های شماره‌دار برای شیوهٔ پاسخ، نشان‌های فشردهٔ وضعیت، مرز
محافظت‌شدهٔ شاهد با تضاد بالا و نوار هویتی نتیجه را به کار می‌گیرد. رفتار برنامه، مجوزدهی، قرارداد
شواهد و ارائهٔ آفلاین تغییر نکرده و هیچ بسته یا دارایی بیرونیِ زمان اجرا افزوده نشده است. آزمون‌های
متمرکز API و مرورگر واقعی، نمای رومیزی انگلیسی، شاهد ترکیبی رخداد، چیدمان راست‌به‌چپ فارسی، کاهش
حرکت و عرض ۳۷۵ پیکسل را می‌پوشانند و موفق‌اند. سقف فراخوانی MCP در طرح Starter مانع تکمیل آرایش
همهٔ صفحه‌ها در Figma شد؛ این محدودیت ثبت شده است و ادعایی دربارهٔ کتابخانهٔ کامل صفحه‌ها وجود
ندارد. کد بازبینی‌شده همچنان مرجع است.
هر پنج کار اجرای `35838156738` در GitHub Actions موفق بودند. همین کد با شناسهٔ تغییر
`ui-figma-foundation-20260923-01` به‌صورت انتشار تغییرناپذیر برنامه
`nextops-0.1.0-54c8bb4` مستقر شد و انتشار پیشین `nextops-0.1.0-8d042cf` برای بازگشت نگه داشته
شد. بررسی صفحهٔ ورودِ مستقرشده در نمای رومیزی انگلیسی و فارسی راست‌به‌چپ موبایل، بدون سرریز
افقی، درخواست بیرونی، پاسخ ناموفق یا خطای console موفق بود. سرویس‌های برنامه، تونل هوش مصنوعی،
Nginx و PostgreSQL 16 فعال بودند؛ واحد خراب یا هشدار پس از استقرار مشاهده نشد. این آزمون محدود
صفحهٔ ورود، جای دروازهٔ هنوز اجرا‌نشدهٔ مرورگر احرازهویت‌شدهٔ مرحلهٔ دو را نمی‌گیرد.

رابط ارزیابی کنترل‌شده بر پایهٔ هویت تأییدشدهٔ OCS بازطراحی شد: نشان اصلی شرکت برای کار آفلاین
درون برنامه قرار گرفت، رنگ‌های طلایی و فیروزه‌ای OCS مبنای کنسول روشن و سازمانی شدند و آیکون برگهٔ
مرورگر نیز از همان تصویر محلی استفاده می‌کند. رفتار دستیار عمومی، پایش و بررسی رخداد، شناسه‌های
شاهد و ممیزی و سقف ۱۲۸ توکن تغییری نکرده است. آزمون مرورگر، چیدمان چپ‌به‌راست انگلیسی،
راست‌به‌چپ فارسی، کاهش حرکت، نمایش واکنش‌گرا در موبایل و دسکتاپ و نبود درخواست دارایی بیرونی را
تأیید می‌کند. کد نهایی هر پنج کار CI را گذراند و با شناسهٔ تغییر
`ui-ocs-brand-20260923-02` به‌صورت انتشار تغییرناپذیر برنامه `nextops-0.1.0-8d042cf` مستقر شد.
بررسی تازهٔ صفحهٔ ورود مستقرشده، نمای رومیزی انگلیسی و فارسی راست‌به‌چپ با عرض ۳۷۵ پیکسل را بدون
سرریز افقی، درخواست بیرونی، پاسخ ناموفق یا خطای console گذراند. این نتیجه به‌معنای اجرای دروازهٔ
کامل و احرازهویت‌شدهٔ مرورگر در مرحلهٔ دو نیست.

گام 2A با شناسهٔ تغییر `phase2a-incident-context-20260923-01` و انتشار تغییرناپذیر
`nextops-0.1.0-1ab6586` روی برنامه و اتصال‌دهنده مستقر شد. خوانشگر Zabbix اکنون دقیقاً پنج روش
`host.get`، `item.get`، `problem.get`، `history.get` و `event.get` را مجاز می‌داند؛ روش‌های نامرتبط
و همهٔ عملیات تغییردهنده همچنان رد می‌شوند. یک درخواست زنده از Zabbix 7.0.30، هشت سنجهٔ جاری و
۳۲ نقطهٔ تاریخی محدود را با دلیل صریحِ محدودشدن برگرداند. مرزهای احرازهویت برنامه و اتصال‌دهنده،
تونل محافظت‌شده، بازگشت و بازگردانی انتشار و نقش، و قطع محافظت‌شدهٔ WAN روی IPv4 و IPv6 موفق
بودند. جدول موقت دیوارهٔ آتش و زمان‌سنج‌های بازگشت حذف و وضعیت عادی دسترسی خروجی بازیابی شد.
استفادهٔ مرورگر احرازهویت‌شده، پیوند ماندگار مدل و ممیزی، راه‌اندازی مجدد VM و عیب‌یابی مستقیم
Linux اجرا نشده‌اند و ادعای پذیرش آن‌ها وجود ندارد.

مرحلهٔ دو با گام محدود «بافت رخداد» Zabbix آغاز شد. اتصال‌دهنده برای تنها میزبان
پیکربندی‌شده، خلاصهٔ جاری، تاریخچهٔ عددی اخیر و رویدادهای trigger را در قرارداد دارای نوع
برمی‌گرداند. بازهٔ استقرار میان ۱۵ تا ۱۴۴۰ دقیقه است و خروجی عمومی به چهار سنجه، هشت نقطه برای
هر سنجه و ۲۵ رویداد محدود می‌شود؛ زمان منبع و دلیل صریحِ ناقص‌بودن نیز حفظ می‌گردد. مسیرهای
احرازهویت‌شدهٔ اتصال‌دهنده و برنامه افزوده شده‌اند، بی‌آنکه روش یا میزبان دلخواه، عملیات نوشتن،
افشای اطلاعات ورود، دسترسی مستقیم Linux یا migration پایگاه ایجاد شود.

آزمون‌های متمرکز اتصال و API، Ruff و mypy سخت‌گیرانه در نقطهٔ تکمیل کد موفق بودند. مستندات متناظر
انگلیسی و فارسی، شاهد کد را از پذیرش زنده جدا کردند. نتیجهٔ استقرار کنترل‌شدهٔ بعدی در بندهای بالا
ثبت شده است؛ پیوند ماندگار با مدل و مرورگر، راه‌اندازی مجدد VM و عیب‌یابی مستقیم Linux هنوز اجرا
نشده‌اند. مانع مقصد مستقل بازیابی و WAL/PITR مرحلهٔ یک نیز بدون تغییر باز است.

همهٔ دروازه‌های اجراییِ صلاحیت‌سنجی کنترل‌شدهٔ مرحلهٔ ۱ با شناسهٔ
`stage1-completion-20260922-01` تکمیل شدند: مرورگر تازه با WAN مسدود، بازگشت برنامه و محیط
اجرا/مدل، بازیابی پس از لغو و قطع وابستگی، توقف امن مدل مفقود یا خراب، شکست ایزولهٔ آماده‌سازی در
کمبود فضا، بار محدود پنج‌دقیقه‌ای و بازیابی منطقی و فقط‌سوکتی پایگاه‌های PostgreSQL 16 برنامه و
Zabbix. همهٔ منابع موقت آزمون حذف شدند و هر چهار مهمان در پایان `running` و بدون واحد خراب بودند.

Playwright 1.63 به‌عنوان وابستگی صرفاً توسعه‌ای قفل و ابزار بازتولیدپذیر مرورگر با مبدأ خصوصی افزوده
شد. مانیفست انتشار و گزارش‌های همتای فارسی و انگلیسی، مرورگر، بازگشت، بازیابی خطا، بار پایدار و
بازیابی منطقی جدا را موفق ثبت می‌کنند. پشتیبان مستقل همچنان ناقص و پذیرش تولید اجرا‌نشده است؛
مقصدی که از بین‌رفتن مهمان سرویس‌دهنده، DS-C/G10 و میزبان را تاب بیاورد تأیید نشده و بازیابی
WAL/PITR/restic هنوز باید اجرا شود.

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

در محیط محلی، قالب و lint با Ruff، نوع‌سنجی سخت‌گیرانهٔ ۵۹ فایل منبع، ۱۰۳ آزمون غیر‌یکپارچه، اعتبارسنجی
۱۰۴ فایل Markdown و ۳۲ جفت راهنمای دوزبانه، اعتبارسنج‌های انتشار، استقرار، هوش مصنوعی و نصب، ساخت
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
