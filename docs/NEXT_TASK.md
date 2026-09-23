# Next task / کار بعدی

Updated: 2026-09-23 — the controlled Stage 1 campaign is complete for every currently executable
gate. Fresh-browser WAN denial, application/runtime/model rollback, cancellation and dependency
recovery, missing/corrupt artifact behavior, isolated low-space staging, five-minute bounded load
and logical isolated restores of both PostgreSQL 16 databases passed. App release
`nextops-0.1.0-13a3369` and connector release `nextops-0.1.0-3d7d725` remain active, and every guest
ended `running` with zero failed units. Independent recovery still requires a verified off-datastore
destination, WAL/PITR and artifact recovery. At the owner's direction, Phase 2 has started in
parallel with a bounded Zabbix incident-context source increment; it is tested in the repository but
not deployed or accepted live. Do not rebuild or repeat the accepted slice.

## English — harden the live user-testing slice

### Authoritative current checkpoint

The next operator must treat the following as completed and preserve it:

- the app release, PostgreSQL migration, private TLS reverse proxy and authenticated bilingual panel;
- the pinned CPU-only AI runtime/model and authenticated application-to-AI tunnel;
- Zabbix 7.0.30 with its PostgreSQL database, TLS frontend/API, Agent 2 and self-monitoring;
- an API-only Zabbix reader restricted to three read methods and one approved host group;
- the rootless read-only connector and pinned application-to-connector tunnel;
- explicit answer modes: default model-only general assistance and opt-in evidence-grounded live
  monitoring, with the exact `Hi` test returning a direct greeting and no Zabbix content;
- durable live-investigation runs with server-derived actor/scope, correlation ID, bounded evidence
  snapshot and SHA-256 reference, stored model result, safe failures and append-only audit linkage;
- live retrieval of eight fresh metrics, explicit source/timestamps/staleness and bilingual grounded
  answers through the desktop client; and
- exact-version Agent 2 coverage for the app, AI and connector guests using distinct PSKs,
  outbound active checks only, no passive listeners or remote commands, and three source-restricted
  Zabbix trapper firewall rules; the unchanged reader sees four approved hosts and fresh items for
  every added host; and
- the 128-token server-side investigation ceiling and localized timeout/overload/dependency states,
  with the reported old 384-token request verified as HTTP 200 after repair; and
- explicit partial-evidence metadata, an untrusted monitoring-text boundary, safe connector-specific
  outage errors, durable failed-run audit, live token-revocation denial and recovery while general
  model-only Q&A remains available; and
- explicit four-guest WAN isolation with direct IPv4 and IPv6 Internet denied while fresh login,
  English and Persian general answers, local-AI readiness, live Zabbix evidence, durable storage and
  linked audit remained available over the approved LAN; and
- serial clean reboots of Zabbix, connector, AI and application with the offline policy loaded before
  normal networking, explicit database-cluster ordering, role-specific recovery and zero failed
  units; and
- local quality gates: Ruff, strict mypy, 103 passing non-integration tests and all 6 PostgreSQL
  integration tests passing against an isolated temporary database.

The immediate implementation sequence is:

1. **Completed:** add approved app, AI and connector hosts to Zabbix with narrowly scoped agent
   paths; retain the reader method and host-group boundaries, and verify counts/timestamps after
   each addition.
2. **Completed:** qualify stale, partial, unreachable, revoked-token, malformed-text and
   prompt-injection cases. General local model use remained available when Zabbix was unavailable.
3. **Completed:** all four guests denied direct IPv4 and IPv6 Internet while local login, bilingual
   general Q&A and a fresh evidence-linked investigation passed. A separately WAN-denied fresh Edge
   context then passed login, LTR/RTL, general/monitoring, provenance, logout and new-tab checks.
4. **Completed:** correct the Zabbix shutdown dependency, prove one clean Zabbix reboot, then reboot
   connector, AI and application serially. The application boot exposed and received the equivalent
   real-cluster startup dependency; its clean retry passed.
5. **Completed:** application and runtime/model rollback, live cancellation, provider loss,
   missing/corrupt model, isolated `ENOSPC`, five-minute load and socket-only logical restores of
   both databases passed. Exact latency and CPU/memory/NUMA observations are in the
   [Stage 1 report](en/STAGE_1_COMPLETION_REPORT.md).
6. **Next external prerequisite:** approve a recovery destination independent of the serving guest,
   DS-C/G10 and host; define RPO/RTO, retention and key custody; then implement separate pgBackRest
   repositories/WAL archiving, restic for permitted files, independent PITR and operational sign-off.
7. **Phase 2A in progress:** deploy the source-tested bounded incident-context contract, extend the
   API reader with exactly `history.get` and `event.get`, qualify live provenance/limits/partial
   behavior and rollback with WAN denied, then connect it to the durable investigation workflow.
   Direct read-only Linux diagnostics follow as Phase 2B; all mutation remains disabled.

The detailed material below preserves design rationale and earlier checkpoints. Where it describes
the app, PostgreSQL, Zabbix, connector or browser as not deployed, this authoritative checkpoint and
[PROJECT_STATE](PROJECT_STATE.md) supersede that older statement.

Read the [active master prompt](requirements/NEXTOPS_MASTER_PROMPT.md) with the new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md), [Zabbix guide](en/ZABBIX_SERVER.md), [per-server deployer guide](en/DEPLOYMENT_DOSSIERS.md), [allocation record](requirements/ZABBIX_SERVER_PLAN.json), [START_HERE](en/START_HERE.md), [PROJECT_STATE](PROJECT_STATE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [STORAGE_PLAN](STORAGE_PLAN.md), [OFFLINE_RUNTIME](en/OFFLINE_RUNTIME.md), [ESXI_BASELINE](en/ESXI_BASELINE.md) and [hardware evidence](requirements/HARDWARE_BASELINE.json). Original detail remains in the [unchanged v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md); all 51 sections and eleven integrations remain in scope.

The new amendment supersedes the old small `zabbix-lab` fallback and combined totals in active-prompt v3.0 section 18 and older guide examples. It does not change the three initial NextOps core VMs or authorize provisioning. Inspect actual Git state, work already done and approval/test evidence before resuming; do not overwrite work or restart completed discovery indefinitely.

### Current checkpoint: controlled AI deployment passed

The owner accepted the paired [Phase 0 report](en/PHASE_0_REPORT.md), [Persian report](fa/PHASE_0_REPORT.md), ADRs 0001–0006, trust boundaries, and Stage 1A–1E roadmap on 2026-09-21. Stage 1A Increments 1–2 provide the locked Python project, typed boundaries and denial policy, local identity, PostgreSQL state, durable runs/leases, append-restricted audit, authenticated API, and bilingual fixture result. Stage 1B Increment 3 provides the `LLMProvider` boundary, authenticated loopback adapter and one-active/two-queued scheduler. After the latest evidence-preservation and relocation fixes, formatting, Ruff, strict mypy over 46 files, and 80 non-integration tests pass; five database tests are skipped locally and retain their earlier real-PostgreSQL host evidence.

A sanitized read-only preflight reached all four clean replacement guests after their independently supplied Ed25519 fingerprints matched live handshakes. All four run Ubuntu 24.04.5 LTS under VMware with the intended public resource/mount budgets. On 2026-09-22, after the AI work and a narrow GLib security update on app, every guest reported `running`, zero failed units, zero pending packages and no reboot requirement. Direct root SSH remains disabled. The deployment account has the full passwordless administrative access explicitly requested by the owner; its private key and strict host-key pins are therefore security-critical and remain outside Git.

The role package layers remain as recorded: PostgreSQL 16.15 and Nginx 1.24 on app; GCC 13.3, CMake 3.28, Ninja 1.11 and OpenBLAS 0.3.26 on AI; Python 3.12 venv support on connectors; and Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24 and PHP 8.3.6 on Zabbix. The controlled application/database/proxy, AI, connector and Zabbix/database/frontend slices are active and passed the named reboot checks. Docker was not installed because the native systemd design does not need it and a container socket would enlarge the trust boundary.

The pinned llama.cpp runtime and 5,027,783,488-byte Qwen model match their approved SHA-256 values and are promoted through stable links to immutable protected directories. The active inference API is `nextops-0.1.0-62de8d6`; the active user application and connector are `nextops-0.1.0-13a3369` and `nextops-0.1.0-3d7d725`. The two AI-guest services use the protected runtime path, wait for authenticated model health, run unprivileged on `127.0.0.1:8080` and `127.0.0.1:8090`, and each has a `2.7 OK` systemd security exposure result. Distinct root-owned credentials remain outside Git and logs. The [release manifest](status/current-release.yaml) is the machine-readable summary.

Two independent four-case qualification runs passed unauthenticated denial, readiness, Persian and
English evidence preservation, and safe non-execution responses under both automated checks and
human review. The initial load probe demonstrated the one-active/two-queued boundary. A cold process
restart returned the authenticated services in 109 seconds while their unit policy denied
non-loopback traffic. Application rollback to `417d888` and restoration to `62de8d6` both returned
`401` for unauthenticated generation and `200` for readiness, leaving `62de8d6` active. This is
controlled Stage 1B qualification, not complete offline or production acceptance.

The four schema-validated YAML files under `deploy/server-dependencies` remain the public deployer handoff. Continue from the actual live state; do not reinstall the accepted AI release or repeat completed discovery. Environment-specific values and evidence stay in the approved private record keyed by `required_inputs`, never in these public files. The next infrastructure work starts only after an approved independent recovery destination and its policy inputs exist.

Completed AI evidence:

- runtime/model hashes, CPU-only loading, protected immutable links, distinct credentials, loopback listeners, authentication/readiness and systemd hardening;
- bounded load plus two manually reviewed Persian/English evidence/safety runs;
- cold process restart and application-release rollback/restoration.

Remaining production gates after the Stage 1 campaign:

- approve storage that survives loss of the serving guest, DS-C/G10 and its host;
- complete dependency/license approval and the final secret/SBOM/release-integrity review;
- configure separate pgBackRest repositories, continuous WAL, retention and repository checks;
- configure restic only for permitted non-database artifacts and verify hash-preserving restore;
- perform independent-host PITR, corrupt/missing-WAL and key-recovery drills with measured RPO/RTO;
- close certificate-expiry/rotation, alerting and final operational sign-off.

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

After each increment, update PROJECT_STATE with actual work, exact versions/results, failed/skipped/not-run cases, remaining blockers and the next checkpoint. The controlled application, AI, connector and four-host Zabbix path is live for user testing. It is not production-accepted: independent backup/PITR, certificate lifecycle, dependency/license approval and complete disaster recovery remain open.

## فارسی — سخت‌سازی مسیر زندهٔ ارزیابی کاربران

### نقطهٔ فعلی و ملاک ادامه

عامل یا بهره‌بردار بعدی باید موارد زیر را تکمیل‌شده بداند و بدون دلیل دوباره نسازد:

- انتشار برنامه، مهاجرت PostgreSQL، reverse proxy با TLS خصوصی و پنل دوزبانهٔ احرازهویت‌شده؛
- محیط اجرا و مدل فقط‌-CPU تثبیت‌شده و تونل احرازهویت‌شدهٔ برنامه به هوش مصنوعی؛
- Zabbix 7.0.30 با پایگاه PostgreSQL، رابط و API مبتنی بر TLS، Agent 2 و خودپایشی؛
- خوانشگر مخصوص API با سه روش فقط‌خواندنی و دامنهٔ یک گروه میزبان مصوب؛
- اتصال فقط‌خواندنی با هویت بدون امتیاز و تونل ثابت‌شدهٔ برنامه به اتصال؛
- دو حالت صریح پاسخ: دستیار عمومیِ پیش‌فرض و بدون شاهد پایشی، و پایش زندهٔ انتخابی و مستند به
  شواهد؛ آزمون دقیق `Hi` پاسخ مستقیم و بدون محتوای Zabbix دریافت کرد؛
- اجرای ماندگار برای هر بررسی زنده، همراه عامل و دامنهٔ استخراج‌شده در سرور، شناسهٔ هم‌بستگی،
  خلاصهٔ محدود شاهد و مرجع SHA-256، نتیجهٔ مدل، خطای امن و پیوند ممیزیِ فقط‌افزودنی؛
- دریافت زندهٔ هشت سنجهٔ تازه، نمایش صریح منبع و زمان و تازگی، و پاسخ مستند فارسی و انگلیسی از
  مسیر رایانهٔ کاربر؛
- پوشش میزبان‌های برنامه، هوش مصنوعی و اتصال با Agent 2 هم‌نسخه، PSK مستقل، فقط بررسی فعالِ
  خروجی، بدون شنوندهٔ غیرفعال یا فرمان راه دور، و سه قاعدهٔ محدود دیوارهٔ آتش در Zabbix؛ خوانشگر
  بدون تغییر دقیقاً چهار میزبان مصوب و دادهٔ تازهٔ هر میزبان افزوده‌شده را می‌بیند؛
- سقف ۱۲۸ توکن در سمت سرور و پیام‌های روشن پایان مهلت، اشباع و قطع وابستگی؛ درخواست قدیمی ۳۸۴
  توکنیِ گزارش‌شده پس از اصلاح با HTTP 200 موفق شد؛
- نشان صریح ناقص‌بودن شاهد، مرز متن پایشیِ غیرقابل‌اعتماد، خطای امن و مختص اتصال هنگام قطع، ثبت
  ماندگار شکست و ممیزی، رد توکن لغوشده و بازیابی؛ در زمان قطع Zabbix، پاسخ عمومی مدل محلی برقرار ماند؛
- قطع صریح WAN هر چهار مهمان؛ درحالی‌که دسترسی مستقیم IPv4 و IPv6 به اینترنت بسته بود، ورود تازه،
  پاسخ عمومی فارسی و انگلیسی، آمادگی مدل محلی، شاهد تازهٔ Zabbix، ذخیرهٔ ماندگار و ممیزی پیوندخورده
  روی شبکهٔ داخلی مجاز برقرار ماند؛
- راه‌اندازی مجدد سالم و ترتیبی Zabbix، اتصال، هوش مصنوعی و برنامه؛ سیاست آفلاین پیش از شبکهٔ عادی
  بار شد، ترتیب خوشه‌های واقعی پایگاه صریح بود، سرویس‌های هر نقش بازگشتند و واحد خراب وجود نداشت؛
- مرورگر تازه با WAN مسدود، بازگشت برنامه و محیط اجرا و مدل، لغو، قطع وابستگی، مدل مفقود/خراب،
  کمبود فضای ایزوله، بار پنج‌دقیقه‌ای و بازیابی منطقی هر دو پایگاه؛ جزئیات در
  [گزارش تکمیل مرحلهٔ ۱](fa/STAGE_1_COMPLETION_REPORT.md)؛
- عبور Ruff، بررسی سخت‌گیرانهٔ mypy، ۱۰۳ آزمون غیر‌یکپارچه و هر شش آزمون PostgreSQL در پایگاه
  موقت و جداگانه.

ترتیب مستقیم کار بعدی چنین است:

1. **تکمیل شد:** میزبان‌های مصوب برنامه، هوش مصنوعی و اتصال با مسیر محدود عامل به Zabbix افزوده
   شدند؛ مرز روش‌ها و گروه میزبان خوانشگر تغییر نکرد و شمار و زمان داده پس از هر افزوده تأیید شد.
2. **تکمیل شد:** حالت‌های دادهٔ قدیمی یا ناقص، مقصد قطع، توکن لغوشده، متن بدساخت و تزریق در متن
   رخداد آزموده شدند. هنگام قطع Zabbix، پرسش عمومی از مدل محلی همچنان پاسخ گرفت.
3. **تکمیل شد:** دسترسی مستقیم IPv4 و IPv6 هر چهار مهمان به اینترنت بسته شد و ورود محلی، پاسخ
   عمومی دوزبانه و بررسی تازهٔ مستند به شاهد موفق ماند. سپس یک context تازهٔ Edge با WAN مسدود،
   ورود، LTR/RTL، حالت عمومی و پایش، منشأ، خروج و الزام ورود در برگهٔ تازه را گذراند.
4. **تکمیل شد:** وابستگی خاموش‌شدن Zabbix اصلاح و راه‌اندازی مجدد سالم آن ثابت شد؛ سپس اتصال،
   هوش مصنوعی و برنامه یکی‌یکی راه‌اندازی مجدد شدند. نخستین بوت برنامه وابستگی مشابه خوشهٔ واقعی
   پایگاه را آشکار کرد؛ اصلاح انجام شد و تکرار سالم آزمون پذیرفته شد.
5. **تکمیل شد:** بازگشت برنامه و محیط اجرا و مدل، لغو زنده، قطع فراهم‌کننده، مدل مفقود/خراب،
   `ENOSPC` ایزوله، بار پنج‌دقیقه‌ای و بازیابی فقط‌سوکتی هر دو پایگاه با ثبت زمان و منابع موفق شد.
6. **پیش‌نیاز بیرونی بعدی:** مقصدی مستقل از مهمان سرویس‌دهنده، DS-C/G10 و میزبان تصویب شود؛ سپس
   RPO/RTO، نگه‌داری و متولی کلید تعیین، مخزن‌های جداگانهٔ pgBackRest و WAL، پشتیبان فایل مجاز با
   restic، PITR روی میزبان مستقل و تأیید نهایی عملیات اجرا شوند.
7. **گام 2A در حال انجام:** قرارداد آزموده‌شده و محدود «بافت رخداد» مستقر شود، نقش خوانشگر API
   دقیقاً با `history.get` و `event.get` گسترش یابد، منشأ و سقف و نقص و بازگشت آن در حالت WAN
   مسدود به‌صورت زنده سنجیده شود و سپس به گردش ماندگار بررسی وصل شود. عیب‌یابی مستقیم و
   فقط‌خواندنی Linux در گام 2B می‌آید و همهٔ عملیات تغییردهنده همچنان غیرفعال‌اند.

مطالب تفصیلی بعدی منطق طراحی و نقاط پیشین را حفظ می‌کند. هرجا برنامه، PostgreSQL، Zabbix، اتصال یا
رابط مرورگر را نصب‌نشده می‌نامد، این بخش و [وضعیت پروژه](PROJECT_STATE.md) جای آن عبارت قدیمی را
می‌گیرند.

[پرامپت فعال](requirements/NEXTOPS_MASTER_PROMPT.md)، [اصلاحیهٔ تازهٔ چیدمان](requirements/DEPLOYMENT_UPDATE.md)، [راهنمای Zabbix](fa/ZABBIX_SERVER.md)، [راهنمای پرونده‌های استقرار](fa/DEPLOYMENT_DOSSIERS.md)، [رکورد تخصیص](requirements/ZABBIX_SERVER_PLAN.json)، [شروع کار](fa/START_HERE.md)، [وضعیت پروژه](PROJECT_STATE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [سرورها](fa/SERVER_PLAN.md)، [ذخیره‌سازی](STORAGE_PLAN.md)، [آفلاین](fa/OFFLINE_RUNTIME.md)، [ESXi](fa/ESXI_BASELINE.md) و [شاهد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خوانده شوند. جزئیات اولیه در [بایگانی ثابت نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) باقی است؛ ۵۱ بخش و یازده اتصال حذف نمی‌شوند.

اصلاحیه فقط نمونهٔ آزمایشگاهی کوچک و مجموع منابع وابسته به آن را در بخش ۱۸ پرامپت ۳.۰ و مثال‌های قدیمی جایگزین می‌کند؛ تعداد سه ماشین اولیهٔ خود NextOps و شروط مجوز تغییر نمی‌کنند. پیش از ادامه، Git، کار موجود، تأییدها و نتیجهٔ آزمون بررسی شوند؛ کار بازنویسی یا شناسایی تکمیل‌شده بی‌دلیل تکرار نشود.

### نقطهٔ فعلی: استقرار کنترل‌شدهٔ هوش مصنوعی پذیرفته شد

مالک در ۲۱ سپتامبر ۲۰۲۶ [گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md)، ADRهای 0001 تا 0006، مرزهای اعتماد و نقشهٔ 1A تا 1E را پذیرفت. Incrementهای 1 و 2 از 1A پروژهٔ قفل‌شدهٔ پایتون، قرارداد و سیاست رد، هویت محلی، وضعیت PostgreSQL، اجرای ماندگار و lease، ممیزی محدود، API احرازهویت‌شده و نتیجهٔ دوزبانهٔ آزمایشی را دارند. Increment 3 از 1B مرز `LLMProvider`، رابط احرازهویت‌شده و فقط‌محلی و صف با یک درخواست فعال و دو درخواست در انتظار را فراهم می‌کند. پس از آخرین اصلاح حفظ شاهد و جابه‌جایی محیط اجرا، قالب‌بندی، Ruff، بررسی سخت‌گیرانهٔ mypy روی ۴۶ فایل و ۸۰ آزمون غیرپایگاهی موفق بوده‌اند؛ پنج آزمون پایگاه در محیط محلی کنار گذاشته شدند و شاهد پیشین اجرای واقعی PostgreSQL برای revision مربوط خود محفوظ است.

پیش‌بررسی پاک‌سازی‌شده پس از برابری اثرانگشت‌های Ed25519 با ارتباط زنده به هر چهار مهمان جایگزین رسید. همهٔ مهمان‌ها Ubuntu 24.04.5 LTS را زیر VMware و با بودجهٔ عمومی منابع و محل‌های ذخیره‌سازی اجرا می‌کنند. در ۲۲ سپتامبر ۲۰۲۶، پس از کار هوش مصنوعی و به‌روزرسانی محدود امنیتی GLib روی مهمان برنامه، هر چهار سرور وضعیت `running`، صفر واحد خراب، صفر بستهٔ قابل‌ارتقا و بی‌نیازی از راه‌اندازی مجدد را گزارش کردند. ورود مستقیم root از راه SSH بسته مانده است. حساب استقرار بنا بر دستور صریح مالک اکنون مدیریت کامل و بدون گذرواژه دارد؛ ازاین‌رو کلید خصوصی و کنترل سخت‌گیرانهٔ کلیدهای میزبان اهمیت امنیتی ویژه دارند و بیرون Git نگه‌داری می‌شوند.

لایهٔ بسته‌های هر نقش مطابق رکورد باقی است: PostgreSQL 16.15 و Nginx 1.24 روی برنامه؛ GCC 13.3، CMake 3.28، Ninja 1.11 و OpenBLAS 0.3.26 روی هوش مصنوعی؛ پشتیبانی محیط مجازی Python 3.12 روی connectors؛ و Zabbix 7.0.30، PostgreSQL 16.15، Nginx 1.24 و PHP 8.3.6 روی Zabbix. برش‌های کنترل‌شدهٔ برنامه و پایگاه و پراکسی، هوش مصنوعی، اتصال و Zabbix و پایگاه و رابط آن فعال‌اند و آزمون‌های نام‌بردهٔ راه‌اندازی مجدد را گذرانده‌اند. Docker نصب نشد، زیرا طراحی بومی systemd به آن نیاز ندارد و سوکت کانتینر مرز اعتماد را بزرگ می‌کند.

محیط اجرای ثابت llama.cpp و مدل Qwen با اندازهٔ ۵٬۰۲۷٬۷۸۳٬۴۸۸ بایت با SHA-256 مصوب برابرند و از راه پیوندهای پایدار به پوشه‌های تغییرناپذیر و محافظت‌شده رسیده‌اند. انتشار فعال API هوش مصنوعی `nextops-0.1.0-62de8d6` و انتشارهای فعال برنامه و اتصال به‌ترتیب `nextops-0.1.0-13a3369` و `nextops-0.1.0-3d7d725` هستند. دو سرویس مهمان هوش مصنوعی کتابخانه‌ها را از مسیر محافظت‌شده می‌خوانند، تا سلامت احرازهویت‌شدهٔ مدل منتظر می‌مانند و با هویت بدون امتیاز فقط روی `127.0.0.1:8080` و `127.0.0.1:8090` فعال‌اند؛ ارزیابی امنیتی systemd برای هرکدام `2.7 OK` است. دو اعتبارنامهٔ جدا و متعلق به root در Git یا گزارش‌ها ظاهر نمی‌شوند. [مانیفست انتشار](status/current-release.yaml) خلاصهٔ ماشین‌خوان این وضعیت است.

دو اجرای مستقلِ چهارموردی، رد درخواست بدون احراز هویت، آمادگی، حفظ شاهد فارسی و انگلیسی و پاسخ ایمن
بدون ادعای اجرا را هم در بررسی خودکار و هم در بازبینی انسانی گذراندند. آزمون بار اولیه، مرز یک
درخواست فعال و دو درخواست در انتظار را نشان داد. پس از توقف فرایندها، سرویس‌های احرازهویت‌شده در
۱۰۹ ثانیه دوباره آماده شدند و سیاست واحدها در تمام مدت ارتباط غیرمحلی را بست. بازگشت برنامه به
`417d888` و سپس بازگرداندن `62de8d6` در هر دو جهت، کد `401` برای تولید بدون احراز هویت و `200`
برای آمادگی داشت و در پایان `62de8d6` فعال ماند. این نتیجه، صلاحیت‌سنجی کنترل‌شدهٔ 1B است، نه
پذیرش کاملِ بدون اینترنت یا تولید.

چهار فایل YAML معتبرشده همچنان قرارداد عمومی تحویل‌اند. ادامه باید از وضعیت زندهٔ فعلی انجام شود؛ انتشار پذیرفته‌شدهٔ هوش مصنوعی دوباره نصب و شناسایی تکمیل‌شده تکرار نشود. مقدارهای محیط و شواهد در رکورد خصوصی بر پایهٔ `required_inputs` بمانند. کار زیرساختی بعدی فقط پس از تصویب مقصد مستقل بازیابی و تصمیم‌های سیاست پشتیبان آغاز می‌شود.

شواهد تکمیل‌شدهٔ هوش مصنوعی:

- چکیدهٔ محیط اجرا و مدل، بارگذاری فقط روی CPU، پیوند تغییرناپذیر، اعتبارنامه‌های جدا، درگاه‌های محلی، احراز هویت، آمادگی و سخت‌سازی systemd؛
- بار محدود و دو اجرای بازبینی‌شدهٔ فارسی و انگلیسی برای شاهد و ایمنی؛
- شروع سرد فرایندها و بازگشت و بازگردانی انتشار برنامه.

دروازه‌های باقی‌مانده برای تولید پس از کارزار مرحلهٔ ۱:

- تصویب ذخیره‌سازی مستقل از مهمان سرویس‌دهنده، DS-C/G10 و میزبان؛
- تأیید مجوز وابستگی‌ها و بازبینی نهایی راز، SBOM و یکپارچگی انتشار؛
- مخزن‌های جداگانهٔ pgBackRest، WAL پیوسته، نگه‌داری و راستی‌آزمایی مخزن؛
- restic فقط برای فایل‌های غیرپایگاهی مجاز و بازیابی منطبق با hash؛
- PITR روی میزبان مستقل، خرابی یا فقدان WAL و بازیابی کلید با RPO/RTO اندازه‌گیری‌شده؛
- چرخهٔ عمر گواهی، هشدار و تأیید نهایی بهره‌برداری.

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

پس از هر گام، کار واقعی، نسخه و نتیجهٔ آزمون، موارد شکست‌خورده یا اجرا‌نشده، مانع و گام بعد در وضعیت پروژه ثبت شوند. مسیر چهارمیزبانی برای ارزیابی کنترل‌شده زنده است، اما پذیرش تولیدی ندارد. مرورگر تازه، پایداری و بازیابی منطقی جدا شاهد دارند؛ پشتیبان مستقل، WAL/PITR، چرخهٔ عمر گواهی و بازیابی کامل بحران همچنان بازند.
