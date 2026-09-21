# Project state / وضعیت پروژه

Updated: 2026-09-21 — Phase 0 and Stage 1A accepted; Stage 1B repository foundation implemented and locally tested; server/model qualification is next. This is not a deployment report.

## English

### Requirements and preserved history

The directly verified Git remote is `Omid-NextAI/nextops`, branch `main`. Earlier records name `AmirMo10/nextops`; current README/install clone commands now use the verified remote, while historical statements remain preserved and the active prompt header still needs a separately versioned repository-identity correction. The owner requested English and native-Persian documentation, a single English active prompt, local CPU-only AI, continued operation after Internet loss, a first useful Zabbix status answer, phased VM allocations, storage limits and a dedicated Zabbix server recommendation. All eleven integrations and the 51 original specification sections remain in scope.

The active [master prompt v3.0](requirements/NEXTOPS_MASTER_PROMPT.md) and [v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) remain unchanged in this update. The new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md) explicitly supersedes only the old small-lab recommendation and combined budgets; non-conflicting security, acceptance and feature requirements remain mandatory. The archive still contains the original Persian specification.

The first deliverable is a new Persian/English question about authorized Zabbix status, answered by local CPU generation from actual evidence, with source times, scope and audit while Internet is blocked. Linux enrichment follows in Phase 2. Documentation publication does not complete a software phase or establish deployment approval.

The paired [Phase 0 report](en/PHASE_0_REPORT.md) and [Persian report](fa/PHASE_0_REPORT.md) record repository evidence, the accepted four-VM architecture, trust boundaries, module and data contracts, CPU benchmark plan, resource gate, connector roadmap, test plan, blockers and the Stage 1A increments. The repository-grounded [threat model](requirements/nextops-threat-model.md) records TM-001–TM-010. On 2026-09-21 the owner accepted Phase 0 and ADRs 0001–0006, confirming one organization initially, small initial scale with future growth, and the dedicated Zabbix path. Every infrastructure authorization remains separate and pending.

Stage 1A Increments 1 and 2 are implemented in repository source. In addition to the locked Python project, strict contracts and deterministic denial policy, the code now has a local FastAPI surface, Argon2id identity bootstrap/login/recovery, hashed opaque sessions, PostgreSQL/Alembic state, idempotent durable runs, expiring worker leases, append-restricted audit, and an explicit bilingual fixture result. Actor organization, environment, roles and scopes are derived from server-side session state. There is still no browser UI, deployable offline release/service definition, target connector or credential, model runtime, or production listener.

Stage 1B Increment 3 now adds a strict runtime-neutral `LLMProvider` contract, authenticated inference API, loopback-only llama.cpp adapter, one-active/two-queued scheduler, bounded input/output/timeouts, cancellation cleanup, safe readiness, and structured overload/dependency failures. A schema-validated YAML manifest pins the source candidate to llama.cpp `v0.4.1` and official `Qwen3-8B-Q4_K_M.gguf`. Neither artifact was downloaded, built, imported or executed; this is source/contract evidence only.

### Supplied hardware and storage evidence

The [hardware record](requirements/HARDWARE_BASELINE.json) preserves the owner's ESXCLI output: ESXi 8.0.3 build 24414501; 4 CPU packages, 112 physical cores, 224 logical threads, active hyperthreading, 4 NUMA nodes and 1,442,743,631,872 memory bytes (calculated about 1343.66 GiB). It includes the partial CPU 0/1 sample, reported speed/cache/microcode and reference mappings documented in [ESXI_BASELINE](en/ESXI_BASELINE.md). Exact marketing SKU, rated speed, all-package consistency, guest ISA and actual per-node distribution are not established by that sample. Arithmetic averages are not observed topology or free resources.

Owner-supplied mounted VMFS rows now establish point-in-time capacity: DS-A 149.75 GiB total / 148.34 GiB free; DS-B 1117.50 / 1109.87; DS-C 3576.75 / 3166.8701171875. Public aliases omit real names, UUIDs and mount paths. [STORAGE_PLAN](STORAGE_PLAN.md) excludes VMFSOS/boot volumes, leaves DS-A/DS-B outside the initial allocation and retains the 3 TB project ceiling. The proposed DS-C free target is 25%, exactly 894.1875 GiB or conservatively about 900 GiB. No datastore reservation, RAID/health inspection or I/O benchmark follows from the supplied listing.

Preserve ESXi; Ubuntu Server 24.04 LTS is a guest proposal, not a host replacement. Supplied totals/build/listing should not be requested as missing. Current available CPU/RAM, load/reservations, actual NUMA placement, VM compatibility and license limits, storage backing/health/latency, outstanding growth and swap placement remain to be checked at execution time. No direct assistant host access or compatibility certification was performed.

### Current proposed deployment

| Role | First needed | vCPU | RAM GiB | Disk GiB |
|---|---|---:|---:|---:|
| nextops-app | Phase 1 | 8 | 32 | 200 |
| nextops-ai | Phase 1 | 24 | 128 | 500 |
| nextops-connectors-ro | Phase 1 | 4 | 8 | 80 |
| **zabbix-server** | **Before Stage 1C live integration** | **4** | **16** | **200** |
| nextops-db | Phase 3, recommended | 8 | 64 | 300 |
| nextops-executor-rw | Phase 7, remediation only | 4 | 16 | 80 |

The new Zabbix VM runs its own monitoring database/frontend/API, not the AI model or the NextOps database. It replaces the earlier 4-vCPU/8-GiB/100-GiB lab fallback for the new-server path. Do not create both; inspect and reuse suitable existing local monitoring instead when available. NextOps-only counts remain 3/4/5; inclusive counts are 4/5/6.

The first combined profile is **40 vCPU / 184 GiB RAM / 980 GiB VMDKs**, plus provisional 184-GiB ESXi swap = **1164 GiB before other overhead**. Later combined profiles are 48/248/1280 (1528 GiB with provisional swap) and 52/264/1360 (1624 GiB). Against unchanged prior DS-C free space, projected free values are 2002.87, 1638.87 and 1542.87 GiB. These are alternative budgets, not cumulative additions, reservations, benchmarks or approval to consume all remaining headroom. Count growth/VMX/snapshot/staging/restore obligations separately and reconcile already-created VMs.

The [new English guide](en/ZABBIX_SERVER.md) and [Persian guide](fa/ZABBIX_SERVER.md) document the proposed native Zabbix 7.0 LTS / PostgreSQL 16 / Nginx / PHP-FPM / Agent 2 stack, full `vg_zabbix` LVM layout, 7-day history / 90-day numeric-trend starting policy, read-only API identity, self-monitoring, offline acceptance and single-host recovery limits. Exact packages, retention settings and VM/LVM configuration are not installed or tested by these documents. Machine-readable proposed values are in [ZABBIX_SERVER_PLAN.json](requirements/ZABBIX_SERVER_PLAN.json), separate from the supplied hardware evidence.

### Per-server deployer dossiers

The versioned [deployment-dossier specification](requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md), shared [JSON Schema](../deploy/server-dependencies/server-dependency.schema.json), and four human-readable YAML server instances now provide one handoff record for `nextops-app`, `nextops-ai`, `nextops-connectors-ro`, and `zabbix-server`. The paired [English](en/DEPLOYMENT_DOSSIERS.md) and [Persian](fa/DEPLOYMENT_DOSSIERS.md) guides define how a deployer resolves private inputs without committing them.

Each dossier includes authorization state, source records, VM sizing, service identities, software/artifact locks, configuration paths, reference-only secrets, network/storage boundaries, dependency order, read-only or guarded command templates, explicit blocked commands, observability, backup/rollback, required private inputs, acceptance gates, and known limitations. Exact known resources reconcile to 40 vCPU / 184 GiB RAM / 980 GiB VMDKs, and the Zabbix mount/LVM entries reconcile to the 200-GiB proposal. The owner-requested JSON-to-YAML conversion preserved every data value. The repository validator safely parses the four YAML files, checks schema 1.0.0 and the approved server IDs, rejects stale JSON dossier copies, and verifies the combined resource totals.

These records expose rather than hide the deployment blockers: the application source and migration now exist, but no approved offline release, installer, reverse proxy, production service definition, browser UI, or tested backup/restore bundle exists. The AI source candidate is pinned, while the built runtime checksum, imported model verification and benchmark remain unresolved; app/AI/connector disk layouts are not designed; the actual Zabbix disk and private networks/endpoints/credentials are unknown; and server acceptance evidence remains `not_run`. No VM, disk, package, account, route, token, certificate, production database, model, service, backup, restore, or target was changed or accessed while creating them.

### Milestones and actual evidence status

| Stage | Required result | Evidence status for this update |
|---|---|---|
| 0 | Architecture/gap/threat report and appropriate approvals | Owner accepted architecture/roadmap and ADRs on 2026-09-21; infrastructure preflight/authorization remains separate |
| 1A | Local identity, policy, database, durable work and audit | Increments 1–2 source-complete for contracts/policy, identity, PostgreSQL, durable runs/leases, audit and API fixture; 44 tests include 5 real-PostgreSQL cases; browser UI and deployment acceptance remain |
| 1B | New local CPU answers and offline model cold load | Source candidate, authenticated boundary and bounded scheduler implemented/tested; no model import, run, benchmark or offline cold start performed |
| Zabbix prerequisite | Dedicated database mount, monitoring, frontend/API and scoped reader before 1C | No VM, installation, account or API call performed here |
| 1C | Real bounded read-only evidence with correct counts | Live connector tests not run here |
| 1D | New evidence-linked Zabbix answer with audit | End-to-end answer not demonstrated here |
| 1E | Offline fresh login/restart, security/failure/capacity tests | ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 not run here |

The user may perform provisioning independently; verify their actual state before claiming a VM either exists or does not exist. A screenshot of VM settings is not proof of an accepted application workflow. Resume from the next evidenced, authorized incomplete stage rather than resetting progress.

### Scope of this publication and next action

This state records Phase 0 acceptance, two Stage 1A code increments, the Stage 1B repository foundation, isolated test evidence, and the schema-validated per-server deployer handoff while preserving the source requirements, archived prompt, diagrams and proposed Zabbix profile. It is not a host vulnerability audit, compatibility lock, or provisioning record.

The source slices use Python 3.12.10, uv 0.12.17, Pydantic 2.13.5, FastAPI 0.141.1, SQLAlchemy 2.0.54, Alembic 1.20.0, Psycopg 3.3.6, Ruff 0.16.8, mypy 1.20.2, and pytest 9.1.1 with a generated `uv.lock`. Hosted CI passes 53 unit/API/schema cases plus 5 integration cases against ephemeral PostgreSQL 17.6. Format/lint, strict types, documentation/dossier/artifact validation, package build, dependency audit, migration upgrade/downgrade, restricted grants, identity/recovery, idempotency, lease recovery, append-only audit, inference boundary/failure behavior, rollback behavior, and full-history secret scanning are merge gates. PostgreSQL 17.6 is CI evidence, not the production version selection. No browser, real model, CPU benchmark or server acceptance ran, and no VM, disk, network, ESXi patch, model, production database, or monitoring service was modified.

The next checkpoint is Stage 1B server qualification in [NEXT_TASK](NEXT_TASK.md): authorize read-only private preflight, build and hash the pinned CPU runtime, import and locally verify the pinned model, then measure fresh Persian/English generation from a cold start with Internet blocked. Stage 1A deployment work—browser UI, offline release, service units, reverse proxy, production PostgreSQL lock, backup/restore and VM acceptance—remains open and requires infrastructure authorization. Phase 0 approval does not grant provisioning or target access. Repo branch protection/private vulnerability reporting and a project software license are not asserted to be configured.

## فارسی

### نیازها و سابقهٔ محفوظ

remote بررسی‌شدهٔ مستقیم Git برابر `Omid-NextAI/nextops` و شاخه `main` است. فرمان‌های clone جاری در README و راهنمای نصب اکنون remote درست را دارند؛ رکوردهای تاریخی `AmirMo10/nextops` حفظ می‌شوند و عنوان پرامپت فعال هنوز به اصلاح جداگانه و نسخه‌دار نیاز دارد. مالک مستندات فارسی طبیعی و انگلیسی، یک پرامپت فعال انگلیسی، AI محلی روی CPU، ادامهٔ کار پس از قطع اینترنت، پاسخ وضعیت Zabbix در اولین تحویل، برنامهٔ ماشین‌ها و محدودیت ذخیره‌سازی و سرور مستقل Zabbix را خواسته است. یازده اتصال و ۵۱ بخش مشخصات اولیه در دامنه باقی‌اند.

[پرامپت فعال ۳.۰](requirements/NEXTOPS_MASTER_PROMPT.md) و [بایگانی نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) در این تغییر دست‌نخورده‌اند. [اصلاحیهٔ استقرار](requirements/DEPLOYMENT_UPDATE.md) فقط پیشنهاد آزمایشگاه کوچک و مجموع منابع وابسته را صریح جایگزین می‌کند؛ سایر نیازهای امنیت، پذیرش و قابلیت‌ها پابرجا هستند. مشخصات فارسی اولیه همچنان در بایگانی محفوظ است.

اولین خروجی، پاسخ تازهٔ فارسی یا انگلیسی دربارهٔ وضعیت مجاز Zabbix، تولیدشده روی CPU محلی و مستند به دادهٔ واقعی، همراه منبع و زمان و دامنه و ممیزی با اینترنت قطع است. بررسی مستقیم Linux در مرحلهٔ دو می‌آید. انتشار مستندات، پایان مرحلهٔ نرم‌افزاری یا اثبات مجوز استقرار نیست.

[گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md) و [مدل تهدید](requirements/nextops-threat-model.md) یافتهٔ مخزن، معماری چهارماشینی پذیرفته‌شده، مرز اعتماد، قرارداد ماژول و داده، برنامهٔ سنجش CPU، بودجه، نقشهٔ اتصال، آزمون و گام‌های 1A را ثبت می‌کنند. مالک در ۲۱ سپتامبر ۲۰۲۶ مرحلهٔ صفر و ADRهای 0001 تا 0006 را با تک‌سازمانی بودن فعلی، مقیاس کوچک اولیه با رشد آینده و Zabbix مستقل پذیرفت. همهٔ مجوزهای زیرساخت جدا و در انتظار باقی می‌مانند.

Incrementهای 1 و 2 از 1A در کد مخزن پیاده شده‌اند. علاوه بر پروژهٔ Python قفل‌شده، قراردادهای سخت‌گیر و سیاست رد قطعی، اکنون FastAPI محلی، bootstrap/login/recovery با Argon2id، session غیرشفافِ hash‌شده، PostgreSQL/Alembic، run ماندگار و idempotent، lease منقضی‌شونده، audit محدود به append و نتیجهٔ fixture دوزبانه وجود دارد. سازمان، محیط، role و scope از session سمت سرور ساخته می‌شوند. هنوز UI مرورگر، release آفلاین قابل‌استقرار، service definition، connector یا credential مقصد، مدل یا listener تولید وجود ندارد.

Increment 3 از 1B اکنون قرارداد سخت‌گیر و مستقل `LLMProvider`، API احرازهویت‌شدهٔ inference، adapter فقط-loopback برای llama.cpp، scheduler با یک درخواست فعال و دو درخواست در صف، حد ورودی و خروجی و زمان، پاک‌سازی لغو، readiness امن و خطاهای ساخت‌یافتهٔ overload/dependency دارد. manifest معتبرشدهٔ YAML نامزد منبع را به llama.cpp نسخهٔ `v0.4.1` و فایل رسمی `Qwen3-8B-Q4_K_M.gguf` ثابت می‌کند. هیچ artifact دانلود، build، import یا اجرا نشده است؛ این فقط شاهد source و contract است.

### شواهد ارسالی سخت‌افزار و دیسک

[رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خروجی ESXCLI مالک را حفظ می‌کند: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هسته، ۲۲۴ رشته، Hyperthreading فعال، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، تقریباً ۱۳۴۳٫۶۶ GiB. نمونهٔ ناقص CPU 0 و 1، سرعت و cache و microcode ارسالی و نگاشت‌های مرجع در [یادداشت ESXi](fa/ESXI_BASELINE.md) ثبت‌اند. مدل تجاری دقیق، فرکانس اسمی، یکسان بودن همهٔ بسته‌ها، ISA مهمان و توزیع واقعی گره‌ها از نمونه ثابت نمی‌شوند. میانگین حسابی، توپولوژی یا ظرفیت آزاد مشاهده‌شده نیست.

ظرفیت لحظه‌ای VMFS ارسالی: DS-A برابر ۱۴۹٫۷۵ GiB کل و ۱۴۸٫۳۴ آزاد؛ DS-B برابر ۱۱۱۷٫۵۰ و ۱۱۰۹٫۸۷؛ DS-C برابر ۳۵۷۶٫۷۵ و 3166.8701171875. نام واقعی، UUID و مسیر در رکورد عمومی نیستند. [برنامهٔ دیسک](STORAGE_PLAN.md) حجم‌های سیستم و راه‌اندازی را کنار می‌گذارد، DS-A و DS-B را تخصیص نمی‌دهد و سقف سه‌ترابایتی را حفظ می‌کند. هدف پیشنهادی فضای آزاد DS-C برابر ۲۵ درصد، دقیقاً 894.1875 GiB و با گردکردن حدود ۹۰۰ GiB است. فهرست ارسالی، رزرو، سلامت RAID یا سنجش I/O نیست.

ESXi حفظ شود؛ Ubuntu Server 24.04 LTS مهمان پیشنهادی است. مجموع‌ها و نسخه و فهرست دوباره به‌عنوان دادهٔ غایب خواسته نشوند. CPU/RAM آزاد فعلی، بار و رزرو، جای‌گذاری NUMA، سازگاری و محدودیت مجوز، سلامت و تأخیر دیسک، رشد و محل swap باید هنگام اجرا بررسی شوند. اتصال مستقیم دستیار یا تأیید سازگاری انجام نشده است.

### چیدمان فعلیِ پیشنهادی

برنامهٔ NextOps همان ۸ vCPU و ۳۲ GiB و ۲۰۰ GiB؛ AI همان ۲۴ و ۱۲۸ و ۵۰۰؛ اتصال همان ۴ و ۸ و ۸۰ است. **سرور مستقل `zabbix-server` با ۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB پیش از اتصال زندهٔ 1C** اضافه می‌شود. پایگاه NextOps از مرحلهٔ سه با ۸ و ۶۴ و ۳۰۰ پیشنهاد می‌شود؛ اجرای تغییر فقط در مرحلهٔ هفت و با مجوز، ۴ و ۱۶ و ۸۰ است.

سرور Zabbix پایگاه پایش، رابط و API خودش را دارد، نه مدل یا پایگاه NextOps. در مسیر جدید، جایگزین آزمایشگاه ۴ vCPU و ۸ GiB و ۱۰۰ GiB می‌شود؛ هر دو ساخته نشوند. Zabbix محلی موجودِ مناسب و مجاز ابتدا بررسی و استفاده شود. تعداد ماشین‌های خود NextOps همچنان ۳، ۴ و ۵ و مجموع شامل پایش ۴، ۵ و ۶ است.

چیدمان اولیه **۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** دارد؛ با سهم موقت ESXi swap برابر ۱۸۴ GiB، جمع پیش از سربار **۱۱۶۴ GiB** است. چیدمان‌های بعدی به‌ترتیب ۴۸ و ۲۴۸ و ۱۲۸۰، با جمع ۱۵۲۸ GiB؛ و ۵۲ و ۲۶۴ و ۱۳۶۰، با جمع ۱۶۲۴ GiB هستند. با مصرف قبلی ثابت، فضای آزاد فرضی DS-C برابر ۲۰۰۲٫۸۷، ۱۶۳۸٫۸۷ و ۱۵۴۲٫۸۷ GiB می‌شود. این‌ها بودجه‌های جایگزین‌اند، نه جمع‌شونده، رزرو، سنجش یا مجوز مصرف همهٔ فضا. رشد، VMX، snapshot، ورود فایل و بازیابی جدا و ماشین موجود بدون دوباره‌شماری حساب شوند.

راهنمای [فارسی](fa/ZABBIX_SERVER.md) و [انگلیسی](en/ZABBIX_SERVER.md) نرم‌افزار پیشنهادی Zabbix 7.0 LTS، PostgreSQL 16، Nginx، PHP-FPM و Agent 2، چیدمان کامل `vg_zabbix`، پیشنهاد history هفت‌روزه و trends عددی نودروزه، هویت API محدود، خودپایشی، پذیرش آفلاین و خطر تک‌میزبان را ثبت می‌کنند. بستهٔ دقیق، تنظیم نگهداری و VM/LVM از طریق این مستندات نصب یا آزموده نشده‌اند. اعداد پیشنهادی در [رکورد Zabbix](requirements/ZABBIX_SERVER_PLAN.json) جدا از شاهد سخت‌افزار آمده‌اند.

### پروندهٔ هر سرور برای مسئول استقرار

[مشخصات پرونده](requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md)، [JSON Schema مشترک](../deploy/server-dependencies/server-dependency.schema.json) و چهار فایل YAML خوانا برای `nextops-app`، `nextops-ai`، `nextops-connectors-ro` و `zabbix-server` اکنون تحویل ماشین‌خوان هر سرور را فراهم می‌کنند. راهنمای [فارسی](fa/DEPLOYMENT_DOSSIERS.md) و [انگلیسی](en/DEPLOYMENT_DOSSIERS.md) روش تکمیل ورودی خصوصی بدون commit آن را شرح می‌دهند.

هر پرونده وضعیت مجوز، منبع، منابع VM، هویت سرویس، قفل نرم‌افزار و artifact، مسیر تنظیمات، secret reference، مرز شبکه و storage، ترتیب سرویس، فرمان فقط‌خواندنی یا الگوی محافظت‌شده، فرمان مسدود، مشاهده‌پذیری، backup و rollback، ورودی لازم، دروازهٔ پذیرش و محدودیت را دارد. مقدارهای معلوم با مجموع ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB سازگارند و mountهای Zabbix با طرح ۲۰۰ GiB تطبیق دارند. تبدیل درخواستی JSON به YAML همهٔ مقدارها را بدون اتلاف حفظ کرد. اعتبارسنج مخزن چهار فایل YAML را ایمن parse می‌کند، schema نسخهٔ ۱.۰.۰ و شناسه‌های پذیرفته‌شده را می‌سنجد، باقی‌ماندن نسخهٔ قدیمی JSON را رد می‌کند و مجموع منابع را تطبیق می‌دهد.

این پرونده‌ها مانع را پنهان نمی‌کنند: کد برنامه و migration ساخته شده، اما release آفلاین تأییدشده، installer، reverse proxy، service definition تولید، UI مرورگر و بستهٔ backup/restore آزموده وجود ندارد. نامزد منبع model/runtime ثبت شده، اما هش binary ساخته‌شده، بررسی مدل واردشده و benchmark حل نشده‌اند؛ layout دیسک app و AI و connector طراحی نشده، دیسک واقعی زبیکس و شبکه و endpoint و credential خصوصی معلوم نیست و شاهد پذیرش سرور `not_run` است. هیچ VM، دیسک، بسته، حساب، route، token، گواهی، پایگاه تولید، مدل، سرویس، backup، restore یا مقصدی تغییر یا استفاده نشد.

### گام‌ها و وضعیت شواهد

معماری، نقشه و ADRهای مرحلهٔ صفر پذیرفته شده‌اند؛ بررسی خصوصی تازهٔ میزبان، مجوز دسترسی و ظرفیت همچنان پیش از زیرساخت لازم‌اند. Incrementهای 1 و 2 از 1A برای قرارداد، هویت، PostgreSQL، run/lease، audit و API fixture در CI جدا آزموده شده‌اند؛ UI مرورگر و پذیرش استقرار باقی است. در 1B نامزد منبع، مرز احرازهویت‌شده و صف محدود پیاده و آزموده شده، اما مدل وارد یا اجرا نشده و benchmark و cold start آفلاین انجام نشده‌اند. VM، نصب، حساب یا API مربوط به پیش‌نیاز Zabbix انجام نشده؛ اتصال زندهٔ 1C، پاسخ کامل 1D و موارد ZBX و OFF مربوط به 1E آزموده نشده‌اند.

ممکن است مالک مستقل ماشین ساخته باشد؛ پیش از ادعای وجود یا نبود آن، وضعیت واقعی بررسی شود. تصویر تنظیمات VM به معنای قبولی مسیر برنامه نیست. ادامه از نخستین گام ناتمامِ دارای شاهد و مجوز باشد، نه پاک کردن پیشرفت.

### دامنهٔ انتشار و کار بعدی

این وضعیت پذیرش مرحلهٔ صفر، دو برش کد 1A، پایهٔ مخزنی 1B، شاهد آزمون جدا و پروندهٔ معتبرشدهٔ تحویل هر سرور را ثبت می‌کند. نیازهای منبع، پرامپت بایگانی‌شده، نمودارها و طرح Zabbix حفظ شده‌اند. ممیزی امنیت میزبان، تثبیت سازگاری یا استقرار انجام نشده است.

برش‌های منبع با Python 3.12.10، uv 0.12.17، Pydantic 2.13.5، FastAPI 0.141.1، SQLAlchemy 2.0.54، Alembic 1.20.0، Psycopg 3.3.6، Ruff 0.16.8، mypy 1.20.2 و pytest 9.1.1 آزموده شدند. CI میزبانی‌شده ۵۳ آزمون unit/API/schema و ۵ آزمون integration را روی PostgreSQL موقت 17.6 با موفقیت اجرا می‌کند و format/lint/type، سند و dossier و artifact، build، audit وابستگی، migration، grant محدود، هویت، idempotency، lease، audit append-only، رفتار خطای inference، rollback و اسکن secret را شرط merge می‌داند. PostgreSQL 17.6 شاهد CI است، نه قفل تولید. آزمون مرورگر، مدل واقعی، benchmark CPU یا پذیرش سرور انجام نشد و هیچ VM، دیسک، شبکه، وصلهٔ ESXi، مدل، پایگاه تولید یا سرویس پایش تغییر نکرد.

نقطهٔ بعد در [کار بعدی](NEXT_TASK.md) صلاحیت‌سنجی سرور 1B است: preflight خصوصی فقط‌خواندنی مجاز شود، runtime ثابت CPU ساخته و هش شود، مدل ثابت وارد و محلی بررسی شود، سپس تولید تازهٔ فارسی و انگلیسی از cold start با اینترنت قطع اندازه‌گیری شود. کار استقرار 1A شامل UI مرورگر، release آفلاین، unit سرویس، reverse proxy، قفل PostgreSQL تولید و backup/restore همچنان باز و مجوز جدا می‌خواهد. پذیرش مرحلهٔ صفر مجوز ساخت یا دسترسی مقصد نیست. حفاظت شاخه، گزارش خصوصی آسیب‌پذیری و مجوز پروژه تنظیم‌شده فرض نشده‌اند.
