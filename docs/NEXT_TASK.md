# Next task / کار بعدی

Updated: 2026-09-21 — the four Ubuntu 24.04 guests are qualified and proxy-connected role package preparation is complete; the pinned CPU runtime/model passed a bounded loopback smoke test. Service configuration, application release, Zabbix initialization, offline acceptance, backup, and recovery remain open.

## English — qualify Stage 1B on the local CPU server

Read the [active master prompt](requirements/NEXTOPS_MASTER_PROMPT.md) with the new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md), [Zabbix guide](en/ZABBIX_SERVER.md), [per-server deployer guide](en/DEPLOYMENT_DOSSIERS.md), [allocation record](requirements/ZABBIX_SERVER_PLAN.json), [START_HERE](en/START_HERE.md), [PROJECT_STATE](PROJECT_STATE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [STORAGE_PLAN](STORAGE_PLAN.md), [OFFLINE_RUNTIME](en/OFFLINE_RUNTIME.md), [ESXI_BASELINE](en/ESXI_BASELINE.md) and [hardware evidence](requirements/HARDWARE_BASELINE.json). Original detail remains in the [unchanged v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md); all 51 sections and eleven integrations remain in scope.

The new amendment supersedes the old small `zabbix-lab` fallback and combined totals in active-prompt v3.0 section 18 and older guide examples. It does not change the three initial NextOps core VMs or authorize provisioning. Inspect actual Git state, work already done and approval/test evidence before resuming; do not overwrite work or restart completed discovery indefinitely.

### Current checkpoint: Stage 1B server qualification

The owner accepted the paired [Phase 0 report](en/PHASE_0_REPORT.md), [Persian report](fa/PHASE_0_REPORT.md), ADRs 0001–0006, trust boundaries, and Stage 1A–1E roadmap on 2026-09-21. Stage 1A Increments 1–2 provide the locked Python project, typed boundary contracts, deterministic denial policy, local identity, PostgreSQL state, durable runs/leases, append-restricted audit, authenticated API, and explicit bilingual fixture result. Stage 1B Increment 3 now provides the source-pinned evaluation candidate, `LLMProvider` boundary, authenticated loopback adapter and one-active/two-queued scheduler. Four guarded per-server scripts provide the authenticated offline Ubuntu package layer, and repository context skills/catalog keep project documentation discoverable. Hosted CI passes 71 unit/API/schema/installer/context cases and 5 real-PostgreSQL cases. This is source/test evidence, not package, server, or model acceptance.

A sanitized read-only preflight reached all four clean replacement guests on 2026-09-21 after their new Ed25519 SSH fingerprints were independently supplied and matched against the live handshakes. All four run Ubuntu 24.04.5 LTS under VMware with the intended vCPU, memory, virtual-disk and dedicated-mount budgets. At that checkpoint, time was synchronized, VMware Tools and SSH were active, systemd reported `running`, no failed unit, pending upgrade or reboot was present, UFW was active, and the only wildcard TCP listener was SSH. The AI guest exposes the required SSE4.2, AVX, AVX2, AVX-512F, FMA and BMI2 flags. The previous host-key pins were replaced locally; addresses, fingerprints and raw output remain outside Git.

The owner explicitly authorized connected preparation through the preconfigured strict proxy chain. Exact observed role packages are now installed without broad OS upgrade or automatic service start: the app host has PostgreSQL 16.15 and Nginx 1.24; AI has GCC 13.3, CMake 3.28, Ninja 1.11 and OpenBLAS 0.3.26; connectors has Python 3.12 venv support; Zabbix has Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24 and PHP 8.3.6. Required service identities and protected paths exist, but every product/database/web service remains inactive and disabled, no PostgreSQL cluster exists, and SSH remains the only wildcard listener. No reboot/update was pending at that qualification checkpoint; a later Stage 1B preflight found the AI security-package updates recorded below. Docker was intentionally not installed because the selected native-package/systemd design does not require it and no service receives a container socket.

The pinned llama.cpp commit was built Release/CPU-native with OpenMP and OpenBLAS, no GPU linkage, and the promoted `llama-server` binary SHA-256 is recorded in the inference manifest. The 5,027,783,488-byte Qwen file was imported through the proxy, matched its pinned SHA-256, and was promoted to the dedicated protected model volume. A temporary authenticated loopback-only one-slot smoke test cold-started in 7 seconds and returned `READY` in 630 ms and `آماده` in 1,431 ms; it used 8K context, zero GPU layers, disabled Web UI/slots, and left no process or listener. This is smoke evidence, not a full benchmark or Internet-blocked acceptance. The reviewed systemd/auth/configuration source and bilingual qualification runner now exist; the next bounded change is their controlled live installation and load/failure/offline evaluation. No cloud fallback, target credential, management route, tool/agent/MCP mode, or Zabbix completion claim is allowed.

The native source profile for that change now exists: separate hardened `nextops-llama` and
`nextops-ai` units, two file-backed systemd credentials, loopback-only cgroup networking, explicit
resource limits, safe credential-file loading, and a versioned bilingual qualification runner. The
focused tests and Ubuntu 24.04 unit syntax/security review pass. Live installation has not started.
A fresh AI-guest preflight found pending security-package updates, and the SSH deployment account has
no narrow passwordless authority to install protected files or control these services. Apply the
reviewed updates through the existing proxy, re-run the guest baseline, then grant only the exact
approved Stage 1B install/service/evidence commands or execute the reviewed root runbook through the
private change process. Do not enable unrestricted root SSH or blanket passwordless sudo.

The four schema-validated YAML files under `deploy/server-dependencies` remain the public deployer handoff. Start with the paired [server-start checklist](en/SERVER_START_CHECKLIST.md): validate the clean replacements in order, beginning with `nextops-app` and then `nextops-ai`; do not reuse the old host-key pins. The package-layer scripts may be checked only with an exact authenticated role bundle and may be applied only under the separate authorization gates in their [operator guide](../deploy/installers/README.md). Do not install the application yet because offline releases, production service units, reverse proxy, backup/restore, and the production PostgreSQL patch are not accepted. Environment-specific values belong in an approved private deployment record keyed by `required_inputs`, never in these public files.

Acceptance evidence for server qualification:

- the authorized local runtime build records compiler, build flags, linked libraries, binary SHA-256, guest ISA and CPU-only/zero-offload startup evidence;
- the imported model matches the pinned filename, size and SHA-256 and is promoted only after staging verification;
- the inference service authenticates both boundaries, remains on loopback, and exposes no target credential, raw error, model path or Internet dependency;
- one active generation request and a queue of two preserve app capacity; timeout, cancellation, overload, malformed output and worker-restart states remain explicit;
- fresh Persian and English prompts run CPU-only from a cold local start while Internet is blocked, with latency, memory, CPU/thread settings, prompt/output token counts, and quality observations recorded;
- Ruff, strict mypy, pytest, documentation checks, frozen install, dependency audit, secret scan, and artifact-integrity checks pass with exact results recorded.

### Already supplied

ESXi 8.0.3 build 24414501; four packages, 112 physical cores, 224 threads, four NUMA nodes and 1,442,743,631,872 memory bytes; a partial Intel CPU sample; and point-in-time VMFS values. DS-C reports 3576.75 GiB total and 3166.8701171875 GiB free. These are owner-supplied observations, not a live capacity reservation or directly performed inspection. Do not ask for them again as missing. Exact CPU SKU, guest ISA, actual node distribution, current available CPU/RAM and competing workload still need evidence.

Keep real datastore names, UUIDs, addresses and credentials private. DS-C is the capacity-based initial placement; DS-A/DS-B and system/boot volumes remain outside this allocation. Retain the 3 TB project ceiling and refresh changing capacity at the execution window.

### Remaining private preflight and provisioning gate

Check available CPU/RAM, VM load/reservations, outstanding thin-disk commitments, actual ESXi swap placement, backing storage health/latency, VM compatibility and guest features, approved local network/admin recovery paths, offline package/model artifacts and agreed quality/latency targets. Map each dependency to local, approved LAN or provisioning-only.

For the new Zabbix path, prepare a separate monitoring VM; when an appropriate authorized installation already exists, inspect and reuse it instead of duplicating it. Confirm frontend base path/version, read-only host-group scope, protected token delivery, self-monitoring items, required monitored guests and sample questions. Do not put private details or tokens into the repository.

The active-prompt section 26 report, two Stage 1A increments and the Stage 1B repository foundation are complete in source/tests. Before any infrastructure operation, use only authorized read-only discovery to close the facts that affect that operation. Code approval does not imply VM creation, host installation, model download, target access, patch, stress test, network change or reboot.

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

After each increment, update PROJECT_STATE with actual work, created roles, exact versions/test commands/results, failed/skipped/not-run cases, remaining blockers and the next checkpoint. Increments 1–3 remain repository source/test evidence. Separate authorized server preparation later installed the role package layers, created protected service identities, built the pinned runtime, imported the verified model, and completed the bounded AI smoke test. No product service, production PostgreSQL or Zabbix state, public listener, network change, reboot, backup, restore, or server recovery has been completed.

## فارسی — صلاحیت‌سنجی 1B روی سرور CPU محلی

[پرامپت فعال](requirements/NEXTOPS_MASTER_PROMPT.md)، [اصلاحیهٔ تازهٔ چیدمان](requirements/DEPLOYMENT_UPDATE.md)، [راهنمای Zabbix](fa/ZABBIX_SERVER.md)، [راهنمای پرونده‌های استقرار](fa/DEPLOYMENT_DOSSIERS.md)، [رکورد تخصیص](requirements/ZABBIX_SERVER_PLAN.json)، [شروع کار](fa/START_HERE.md)، [وضعیت پروژه](PROJECT_STATE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [سرورها](fa/SERVER_PLAN.md)، [ذخیره‌سازی](STORAGE_PLAN.md)، [آفلاین](fa/OFFLINE_RUNTIME.md)، [ESXi](fa/ESXI_BASELINE.md) و [شاهد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خوانده شوند. جزئیات اولیه در [بایگانی ثابت نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) باقی است؛ ۵۱ بخش و یازده اتصال حذف نمی‌شوند.

اصلاحیه فقط نمونهٔ آزمایشگاهی کوچک و مجموع منابع وابسته به آن را در بخش ۱۸ پرامپت ۳.۰ و مثال‌های قدیمی جایگزین می‌کند؛ تعداد سه ماشین اولیهٔ خود NextOps و شروط مجوز تغییر نمی‌کنند. پیش از ادامه، Git، کار موجود، تأییدها و نتیجهٔ آزمون بررسی شوند؛ کار بازنویسی یا شناسایی تکمیل‌شده بی‌دلیل تکرار نشود.

### نقطهٔ فعلی: صلاحیت‌سنجی سرور Stage 1B

مالک در ۲۱ سپتامبر ۲۰۲۶ [گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md)، ADRهای 0001 تا 0006، مرزهای اعتماد و نقشهٔ 1A تا 1E را پذیرفت. Incrementهای 1 و 2 از 1A پروژهٔ Python قفل‌شده، قرارداد و سیاست، هویت محلی، PostgreSQL، run/lease ماندگار، audit محدود، API احرازهویت‌شده و نتیجهٔ fixture دوزبانه دارند. Increment 3 از 1B نیز نامزد منبع ثابت، مرز `LLMProvider`، adapter احرازهویت‌شدهٔ loopback و scheduler با یک درخواست فعال و دو مورد در صف دارد. چهار script محافظت‌شده برای هر سرور لایهٔ بسته‌های Ubuntu آفلاین و احرازشده را فراهم می‌کنند و skill و catalog مخصوص مخزن، مستندات پروژه را قابل بازیابی نگه می‌دارند. CI میزبانی‌شده ۷۱ آزمون unit/API/schema/installer/context و ۵ آزمون PostgreSQL واقعی را با موفقیت اجرا می‌کند؛ این شاهد source و test است، نه پذیرش package، سرور یا مدل.

در ۲۱ سپتامبر ۲۰۲۶، پس از آنکه مالک اثرانگشت‌های تازهٔ Ed25519 را از مسیر مستقل فرستاد و آن‌ها با ارتباط زنده برابر شدند، پیش‌بررسی پاک‌سازی‌شده و فقط‌خواندنی به هر چهار مهمان جایگزین تمیز رسید. هر چهار مهمان Ubuntu 24.04.5 LTS را زیر VMware با بودجهٔ موردنظر vCPU، حافظه، دیسک مجازی و محل‌های ذخیره‌سازی جدا اجرا می‌کنند. در آن نقطهٔ کنترل، زمان همگام، VMware Tools و SSH فعال و وضعیت systemd برابر `running` بود؛ واحد خراب، بستهٔ قابل‌ارتقا یا راه‌اندازی مجدد معلق وجود نداشت، UFW فعال بود و تنها شنوندهٔ عمومی TCP، SSH بود. مهمان هوش مصنوعی نیز قابلیت‌های لازم SSE4.2، AVX، AVX2، AVX-512F، FMA و BMI2 را دارد. اثرانگشت‌های قدیمی کلید میزبان به‌صورت محلی جایگزین شدند؛ نشانی، اثرانگشت و خروجی خام وارد Git نشده‌اند.

مالک آماده‌سازی متصل از طریق زنجیرهٔ سخت‌گیرانه و ازپیش‌تنظیم‌شدهٔ proxy را صریحاً مجاز کرد. بسته‌های مشاهده‌شدهٔ هر نقش بدون ارتقای کلی سیستم‌عامل یا شروع خودکار سرویس نصب شدند: میزبان app دارای PostgreSQL 16.15 و Nginx 1.24 است؛ هوش مصنوعی دارای GCC 13.3، CMake 3.28، Ninja 1.11 و OpenBLAS 0.3.26؛ connectors دارای پشتیبانی venv در Python 3.12؛ و Zabbix دارای Zabbix 7.0.30، PostgreSQL 16.15، Nginx 1.24 و PHP 8.3.6 است. هویت‌های سرویس و مسیرهای محافظت‌شده ساخته شدند، اما همهٔ سرویس‌های محصول، پایگاه و وب غیرفعال هستند؛ هیچ خوشه‌ای از PostgreSQL وجود ندارد و SSH تنها شنوندهٔ عمومی است. در آن نقطهٔ صلاحیت‌سنجی، به‌روزرسانی یا راه‌اندازی مجدد معلق نبود؛ پیش‌بررسی بعدی مرحلهٔ 1B، به‌روزرسانی‌های امنیتی مهمان هوش مصنوعی را که در ادامه آمده است شناسایی کرد. Docker عمداً نصب نشد، زیرا طراحی منتخبِ بسته‌های بومی و systemd به آن نیاز ندارد و هیچ سرویس نباید به سوکت کانتینر دسترسی داشته باشد.

نسخهٔ ثابت llama.cpp با تنظیم Release و اجرای بومی CPU، همراه OpenMP و OpenBLAS و بدون پیوند GPU ساخته شد و SHA-256 فایل ارتقایافتهٔ `llama-server` در manifest ثبت است. فایل Qwen با اندازهٔ ۵٬۰۲۷٬۷۸۳٬۴۸۸ بایت از مسیر proxy وارد شد، با SHA-256 ثابت برابر بود و به حجم محافظت‌شدهٔ مدل انتقال یافت. آزمون مقدماتی موقت و احرازهویت‌شده، با یک جایگاه و فقط روی رابط محلی، در ۷ ثانیه از حالت سرد آغاز شد و `READY` را در ۶۳۰ میلی‌ثانیه و `آماده` را در ۱۴۳۱ میلی‌ثانیه بازگرداند؛ زمینه برابر 8K، تعداد لایه‌های GPU برابر صفر و رابط وب و نمایش جایگاه‌ها غیرفعال بود و هیچ فرایند یا شنونده‌ای باقی نماند. این فقط شاهد آزمون مقدماتی است، نه سنجش کامل یا پذیرش با اینترنت قطع. کد مبدأ بازبینی‌شدهٔ systemd، احراز هویت و پیکربندی و نیز اجراکنندهٔ سنجش دوزبانه اکنون وجود دارند؛ تغییر محدود بعدی، نصب کنترل‌شدهٔ آن‌ها و ارزیابی بار، خطا و اجرای آفلاین است. جایگزین ابری، اعتبارنامهٔ مقصد، مسیر مدیریتی، حالت tools/agent/MCP و ادعای تکمیل Zabbix مجاز نیست.

پروفایل بومی این تغییر اکنون در کد منبع موجود است: دو واحد سخت‌سازی‌شدهٔ `nextops-llama` و
`nextops-ai`، دو اعتبارنامهٔ فایل‌محور systemd، محدودیت شبکه در سطح cgroup و فقط روی رابط محلی، سقف
صریح منابع، بارگذاری ایمن اعتبارنامه و اجراکنندهٔ نسخه‌دار ارزیابی دوزبانه. آزمون‌های متمرکز و بررسی
نحو و امنیت واحدها روی Ubuntu 24.04 موفق‌اند، اما نصب زنده آغاز نشده است. پیش‌بررسی تازهٔ مهمان هوش
مصنوعی چند به‌روزرسانی امنیتی معوق را نشان داد و حساب SSH استقرار نیز مجوز محدود و بدون گذرواژه برای
نصب فایل‌های محافظت‌شده یا کنترل سرویس‌ها ندارد. به‌روزرسانی‌های بازبینی‌شده از مسیر پراکسی موجود
اعمال و خط مبنا دوباره بررسی شود؛ سپس فقط فرمان‌های دقیق و مصوب نصب، کنترل سرویس و گردآوری شواهد
برای مرحلهٔ 1B مجاز شوند یا دستورالعمل root در فرایند خصوصی تغییر اجرا شود. ورود مستقیم root یا
sudo نامحدود و بدون گذرواژه فعال نشود.

چهار فایل YAML معتبرشده با schema قرارداد عمومی تحویل‌اند. کار سرور از [چک‌لیست شروع فارسی](fa/SERVER_START_CHECKLIST.md) آغاز شود: جایگزین‌های تمیز به‌ترتیب و از `nextops-app` و سپس `nextops-ai` اعتبارسنجی شوند و pin قدیمی کلید میزبان دوباره استفاده نشود. scriptهای لایهٔ package فقط با bundle دقیق و احرازشدهٔ همان role بررسی شوند و اجرای `--apply` نیز تنها با دروازه‌های مجوز جداگانه در [راهنمای مجری](../deploy/installers/README.md) مجاز است. برنامه هنوز نصب نشود، چون release آفلاین، unit تولید، reverse proxy، backup/restore و patch تولید PostgreSQL پذیرفته نشده‌اند. مقدار واقعی محیط در رکورد خصوصی بر اساس `required_inputs` بماند.

شاهد پذیرش صلاحیت‌سنجی سرور:

- build محلیِ مجاز runtime، compiler، flag، کتابخانهٔ پیوندی، SHA-256 فایل اجرایی، ISA مهمان و شاهد CPU-only/zero-offload را ثبت کند؛
- مدل واردشده با نام، اندازه و SHA-256 ثابت برابر باشد و فقط پس از بررسی staging ارتقا یابد؛
- سرویس inference هر دو مرز را احرازهویت کند، روی loopback بماند و credential مقصد، خطای خام، مسیر مدل یا وابستگی اینترنت را منتشر نکند؛
- یک generation فعال و صف دو موردی ظرفیت برنامه را حفظ کند و timeout، لغو، overload، خروجی خراب و restart حالت صریح داشته باشند؛
- prompt تازهٔ فارسی و انگلیسی در CPU، از cold start محلی و با اینترنت قطع اجرا و latency، حافظه، CPU/thread، token و مشاهدهٔ کیفیت ثبت شود؛
- Ruff، mypy سخت‌گیرانه، pytest، سند، نصب قفل‌شده، audit وابستگی، اسکن secret و یکپارچگی artifact با نتیجهٔ دقیق قبول شوند.

### اطلاعات موجود

ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ CPU، تعداد ۱۱۲ هسته و ۲۲۴ رشته، چهار گرهٔ NUMA، حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، نمونهٔ ناقص CPU و ظرفیت لحظه‌ای VMFSها قبلاً ارسال شده‌اند. DS-C ظرفیت 3576.75 GiB و فضای آزاد 3166.8701171875 GiB گزارش کرده است. این‌ها شاهد ارسالی‌اند، نه رزرو یا اتصال مستقیم. دوباره به‌عنوان دادهٔ غایب خواسته نشوند. مدل دقیق CPU، ISA مهمان، توزیع گره‌ها، منابع آزاد و بار رقابتی هنوز بررسی می‌خواهند.

نام واقعی datastore، UUID، نشانی و اطلاعات ورود خصوصی بمانند. DS-C محل پیشنهادی بر اساس ظرفیت است؛ DS-A و DS-B و حجم‌های سیستم و راه‌اندازی خارج از تخصیص‌اند. سقف سه‌ترابایتی حفظ و فضای آزاد هنگام اجرای تغییر تازه‌سازی شود.

### شرط خصوصیِ باقی‌مانده برای ساخت

CPU/RAM آزاد، بار و رزرو ماشین‌ها، رشد تعهدشدهٔ thin، محل swap، سلامت و تأخیر دیسک، سازگاری VM و ویژگی مهمان، شبکه و بازیابی مجاز، فایل آفلاین و هدف کیفیت و زمان پاسخ بررسی شوند. هر وابستگی محلی، شبکهٔ داخلیِ مجاز یا صرفاً زمان آماده‌سازی باشد.

برای مسیر جدید، ماشین پایش مستقل آماده شود؛ اگر Zabbix مناسب و مجاز موجود است، ابتدا بررسی و همان استفاده شود. مسیر پایه و نسخهٔ API، گروه‌های میزبان، روش امن توکن، خودپایشی، مهمان‌های هدف و سؤال نمونه معلوم شوند. جزئیات خصوصی در مخزن نباشند.

گزارش بخش ۲۶، دو برش 1A و پایهٔ مخزنی 1B در source/test کامل شده‌اند. پیش از هر عملیات زیرساخت، فقط با شناسایی مجاز و فقط‌خواندنی واقعیت مؤثر همان عملیات روشن شود. مجوز کد به معنی ساخت VM، نصب روی میزبان، دانلود مدل، دسترسی مقصد، وصله، فشار، شبکه یا reboot نیست.

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

پس از هر گام، کار واقعی، نقش ساخته‌شده، نسخه و فرمان و نتیجهٔ آزمون، شکست و اجرا‌نشده و مانع و یک گام بعد در وضعیت پروژه ثبت شوند. Incrementهای 1 تا 3 همچنان شاهد source و test مخزن هستند. در آماده‌سازی جداگانه و مجاز سرورها، packageهای هر نقش نصب، هویت‌های محافظت‌شده ساخته، runtime ثابت build، مدل تأییدشده وارد و smoke test محدود AI کامل شد. هیچ سرویس محصول، وضعیت تولیدی PostgreSQL یا Zabbix، listener عمومی، تغییر شبکه، reboot، backup، restore یا بازیابی سرور تکمیل نشده است.
