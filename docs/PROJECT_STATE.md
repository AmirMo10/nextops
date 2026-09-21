# Project state / وضعیت پروژه

Updated: 2026-09-21 — Phase 0 accepted; Stage 1A Increment 1 implemented and tested locally. This is not a deployment report.

## English

### Requirements and preserved history

The directly verified Git remote is `Omid-NextAI/nextops`, branch `main`. Earlier records name `AmirMo10/nextops`; current README/install clone commands now use the verified remote, while historical statements remain preserved and the active prompt header still needs a separately versioned repository-identity correction. The owner requested English and native-Persian documentation, a single English active prompt, local CPU-only AI, continued operation after Internet loss, a first useful Zabbix status answer, phased VM allocations, storage limits and a dedicated Zabbix server recommendation. All eleven integrations and the 51 original specification sections remain in scope.

The active [master prompt v3.0](requirements/NEXTOPS_MASTER_PROMPT.md) and [v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) remain unchanged in this update. The new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md) explicitly supersedes only the old small-lab recommendation and combined budgets; non-conflicting security, acceptance and feature requirements remain mandatory. The archive still contains the original Persian specification.

The first deliverable is a new Persian/English question about authorized Zabbix status, answered by local CPU generation from actual evidence, with source times, scope and audit while Internet is blocked. Linux enrichment follows in Phase 2. Documentation publication does not complete a software phase or establish deployment approval.

The paired [Phase 0 report](en/PHASE_0_REPORT.md) and [Persian report](fa/PHASE_0_REPORT.md) record repository evidence, the accepted four-VM architecture, trust boundaries, module and data contracts, CPU benchmark plan, resource gate, connector roadmap, test plan, blockers and the Stage 1A increments. The repository-grounded [threat model](requirements/nextops-threat-model.md) records TM-001–TM-010. On 2026-09-21 the owner accepted Phase 0 and ADRs 0001–0006, confirming one organization initially, small initial scale with future growth, and the dedicated Zabbix path. Every infrastructure authorization remains separate and pending.

Stage 1A Increment 1 is implemented on the local development branch: Python 3.12 metadata, generated `uv.lock`, strict immutable actor/target/request/evidence/error contracts, trusted risk classes, and a deterministic one-organization/environment/target/action/scope policy. Authenticated actor context is separate from untrusted request/model intent. The policy denies unknown values and all non-`READ_ONLY` risk classes; no role, including admin, bypasses it. There is no runtime API, database, connector, credential, model, or network listener yet.

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

### Milestones and actual evidence status

| Stage | Required result | Evidence status for this update |
|---|---|---|
| 0 | Architecture/gap/threat report and appropriate approvals | Owner accepted architecture/roadmap and ADRs on 2026-09-21; infrastructure preflight/authorization remains separate |
| 1A | Local identity, policy, database, durable work and audit | Increment 1 contracts/policy tested locally; identity bootstrap, PostgreSQL, durable runs/audit and API/UI remain |
| 1B | New local CPU answers and offline model cold load | No model run or benchmark performed here |
| Zabbix prerequisite | Dedicated database mount, monitoring, frontend/API and scoped reader before 1C | No VM, installation, account or API call performed here |
| 1C | Real bounded read-only evidence with correct counts | Live connector tests not run here |
| 1D | New evidence-linked Zabbix answer with audit | End-to-end answer not demonstrated here |
| 1E | Offline fresh login/restart, security/failure/capacity tests | ZBX-01–ZBX-08 and applicable OFF-01–OFF-10 not run here |

The user may perform provisioning independently; verify their actual state before claiming a VM either exists or does not exist. A screenshot of VM settings is not proof of an accepted application workflow. Resume from the next evidenced, authorized incomplete stage rather than resetting progress.

### Scope of this publication and next action

This change records Phase 0 acceptance and adds the first Stage 1A code increment while preserving the source requirements, archived prompt, diagrams and proposed Zabbix profile. It is not a host vulnerability audit, compatibility lock, or provisioning record.

The Stage 1A slice uses Python 3.12.10, uv 0.12.17, Pydantic 2.13.5, Ruff 0.16.8, mypy 1.20.2, pytest 9.1.1, and a generated `uv.lock`. Eighteen unit cases pass. `ruff check packages tests`, strict `mypy packages tests`, `pytest`, `uv lock --check`, a clean `uv sync --extra dev --frozen`, `uv pip check`, and `uv audit --frozen` passed; the audit reported no known vulnerabilities. Documentation validation and `git diff --check` are part of the final repository gate. No browser/runtime service test passed, and no VM, disk, network, ESXi patch, model, database or monitoring service was modified.

The next checkpoint is Stage 1A Increment 2 in [NEXT_TASK](NEXT_TASK.md): local identity bootstrap/recovery, real isolated PostgreSQL migrations and roles, durable idempotent runs, leases, append-restricted audit, minimal authenticated API, and one bilingual fixture result. Phase 0 approval does not grant provisioning or target access. Retain deterministic policy, scoped credential handling, no external AI, local assets/login/keys/certificates, independent backups and host-outage limits. Repo protection/CI/private vulnerability reporting and a software license are not asserted to be configured.

## فارسی

### نیازها و سابقهٔ محفوظ

remote بررسی‌شدهٔ مستقیم Git برابر `Omid-NextAI/nextops` و شاخه `main` است. فرمان‌های clone جاری در README و راهنمای نصب اکنون remote درست را دارند؛ رکوردهای تاریخی `AmirMo10/nextops` حفظ می‌شوند و عنوان پرامپت فعال هنوز به اصلاح جداگانه و نسخه‌دار نیاز دارد. مالک مستندات فارسی طبیعی و انگلیسی، یک پرامپت فعال انگلیسی، AI محلی روی CPU، ادامهٔ کار پس از قطع اینترنت، پاسخ وضعیت Zabbix در اولین تحویل، برنامهٔ ماشین‌ها و محدودیت ذخیره‌سازی و سرور مستقل Zabbix را خواسته است. یازده اتصال و ۵۱ بخش مشخصات اولیه در دامنه باقی‌اند.

[پرامپت فعال ۳.۰](requirements/NEXTOPS_MASTER_PROMPT.md) و [بایگانی نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) در این تغییر دست‌نخورده‌اند. [اصلاحیهٔ استقرار](requirements/DEPLOYMENT_UPDATE.md) فقط پیشنهاد آزمایشگاه کوچک و مجموع منابع وابسته را صریح جایگزین می‌کند؛ سایر نیازهای امنیت، پذیرش و قابلیت‌ها پابرجا هستند. مشخصات فارسی اولیه همچنان در بایگانی محفوظ است.

اولین خروجی، پاسخ تازهٔ فارسی یا انگلیسی دربارهٔ وضعیت مجاز Zabbix، تولیدشده روی CPU محلی و مستند به دادهٔ واقعی، همراه منبع و زمان و دامنه و ممیزی با اینترنت قطع است. بررسی مستقیم Linux در مرحلهٔ دو می‌آید. انتشار مستندات، پایان مرحلهٔ نرم‌افزاری یا اثبات مجوز استقرار نیست.

[گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md) و [مدل تهدید](requirements/nextops-threat-model.md) یافتهٔ مخزن، معماری چهارماشینی پذیرفته‌شده، مرز اعتماد، قرارداد ماژول و داده، برنامهٔ سنجش CPU، بودجه، نقشهٔ اتصال، آزمون و گام‌های 1A را ثبت می‌کنند. مالک در ۲۱ سپتامبر ۲۰۲۶ مرحلهٔ صفر و ADRهای 0001 تا 0006 را با تک‌سازمانی بودن فعلی، مقیاس کوچک اولیه با رشد آینده و Zabbix مستقل پذیرفت. همهٔ مجوزهای زیرساخت جدا و در انتظار باقی می‌مانند.

Increment 1 از 1A در شاخهٔ محلی پیاده شده است: metadata برای Python 3.12، `uv.lock` تولیدشده، قراردادهای سخت‌گیر و ثابت actor، هدف، درخواست، شاهد و خطا، کلاس ریسک معتبر و سیاست قطعی سازمان/محیط/هدف/action/scope. Actor احرازشده از intent نامطمئن کاربر یا مدل جداست. مقدار ناشناخته و همهٔ کلاس‌های غیر `READ_ONLY` رد می‌شوند و admin میان‌بُر ندارد. هنوز API اجرایی، پایگاه، connector، credential، مدل یا listener شبکه وجود ندارد.

### شواهد ارسالی سخت‌افزار و دیسک

[رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خروجی ESXCLI مالک را حفظ می‌کند: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هسته، ۲۲۴ رشته، Hyperthreading فعال، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، تقریباً ۱۳۴۳٫۶۶ GiB. نمونهٔ ناقص CPU 0 و 1، سرعت و cache و microcode ارسالی و نگاشت‌های مرجع در [یادداشت ESXi](fa/ESXI_BASELINE.md) ثبت‌اند. مدل تجاری دقیق، فرکانس اسمی، یکسان بودن همهٔ بسته‌ها، ISA مهمان و توزیع واقعی گره‌ها از نمونه ثابت نمی‌شوند. میانگین حسابی، توپولوژی یا ظرفیت آزاد مشاهده‌شده نیست.

ظرفیت لحظه‌ای VMFS ارسالی: DS-A برابر ۱۴۹٫۷۵ GiB کل و ۱۴۸٫۳۴ آزاد؛ DS-B برابر ۱۱۱۷٫۵۰ و ۱۱۰۹٫۸۷؛ DS-C برابر ۳۵۷۶٫۷۵ و 3166.8701171875. نام واقعی، UUID و مسیر در رکورد عمومی نیستند. [برنامهٔ دیسک](STORAGE_PLAN.md) حجم‌های سیستم و راه‌اندازی را کنار می‌گذارد، DS-A و DS-B را تخصیص نمی‌دهد و سقف سه‌ترابایتی را حفظ می‌کند. هدف پیشنهادی فضای آزاد DS-C برابر ۲۵ درصد، دقیقاً 894.1875 GiB و با گردکردن حدود ۹۰۰ GiB است. فهرست ارسالی، رزرو، سلامت RAID یا سنجش I/O نیست.

ESXi حفظ شود؛ Ubuntu Server 24.04 LTS مهمان پیشنهادی است. مجموع‌ها و نسخه و فهرست دوباره به‌عنوان دادهٔ غایب خواسته نشوند. CPU/RAM آزاد فعلی، بار و رزرو، جای‌گذاری NUMA، سازگاری و محدودیت مجوز، سلامت و تأخیر دیسک، رشد و محل swap باید هنگام اجرا بررسی شوند. اتصال مستقیم دستیار یا تأیید سازگاری انجام نشده است.

### چیدمان فعلیِ پیشنهادی

برنامهٔ NextOps همان ۸ vCPU و ۳۲ GiB و ۲۰۰ GiB؛ AI همان ۲۴ و ۱۲۸ و ۵۰۰؛ اتصال همان ۴ و ۸ و ۸۰ است. **سرور مستقل `zabbix-server` با ۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB پیش از اتصال زندهٔ 1C** اضافه می‌شود. پایگاه NextOps از مرحلهٔ سه با ۸ و ۶۴ و ۳۰۰ پیشنهاد می‌شود؛ اجرای تغییر فقط در مرحلهٔ هفت و با مجوز، ۴ و ۱۶ و ۸۰ است.

سرور Zabbix پایگاه پایش، رابط و API خودش را دارد، نه مدل یا پایگاه NextOps. در مسیر جدید، جایگزین آزمایشگاه ۴ vCPU و ۸ GiB و ۱۰۰ GiB می‌شود؛ هر دو ساخته نشوند. Zabbix محلی موجودِ مناسب و مجاز ابتدا بررسی و استفاده شود. تعداد ماشین‌های خود NextOps همچنان ۳، ۴ و ۵ و مجموع شامل پایش ۴، ۵ و ۶ است.

چیدمان اولیه **۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** دارد؛ با سهم موقت ESXi swap برابر ۱۸۴ GiB، جمع پیش از سربار **۱۱۶۴ GiB** است. چیدمان‌های بعدی به‌ترتیب ۴۸ و ۲۴۸ و ۱۲۸۰، با جمع ۱۵۲۸ GiB؛ و ۵۲ و ۲۶۴ و ۱۳۶۰، با جمع ۱۶۲۴ GiB هستند. با مصرف قبلی ثابت، فضای آزاد فرضی DS-C برابر ۲۰۰۲٫۸۷، ۱۶۳۸٫۸۷ و ۱۵۴۲٫۸۷ GiB می‌شود. این‌ها بودجه‌های جایگزین‌اند، نه جمع‌شونده، رزرو، سنجش یا مجوز مصرف همهٔ فضا. رشد، VMX، snapshot، ورود فایل و بازیابی جدا و ماشین موجود بدون دوباره‌شماری حساب شوند.

راهنمای [فارسی](fa/ZABBIX_SERVER.md) و [انگلیسی](en/ZABBIX_SERVER.md) نرم‌افزار پیشنهادی Zabbix 7.0 LTS، PostgreSQL 16، Nginx، PHP-FPM و Agent 2، چیدمان کامل `vg_zabbix`، پیشنهاد history هفت‌روزه و trends عددی نودروزه، هویت API محدود، خودپایشی، پذیرش آفلاین و خطر تک‌میزبان را ثبت می‌کنند. بستهٔ دقیق، تنظیم نگهداری و VM/LVM از طریق این مستندات نصب یا آزموده نشده‌اند. اعداد پیشنهادی در [رکورد Zabbix](requirements/ZABBIX_SERVER_PLAN.json) جدا از شاهد سخت‌افزار آمده‌اند.

### گام‌ها و وضعیت شواهد

معماری، نقشه و ADRهای مرحلهٔ صفر پذیرفته شده‌اند؛ بررسی خصوصی تازهٔ میزبان، مجوز دسترسی و ظرفیت همچنان پیش از زیرساخت لازم‌اند. Increment 1 از 1A پیاده و آزموده شده، اما هویت ماندگار، پایگاه، audit و API/UI آن باقی است. مدل و سنجش 1B اجرا نشده؛ VM، نصب، حساب یا API مربوط به پیش‌نیاز Zabbix انجام نشده؛ اتصال زندهٔ 1C، پاسخ کامل 1D و موارد ZBX و OFF مربوط به 1E آزموده نشده‌اند.

ممکن است مالک مستقل ماشین ساخته باشد؛ پیش از ادعای وجود یا نبود آن، وضعیت واقعی بررسی شود. تصویر تنظیمات VM به معنای قبولی مسیر برنامه نیست. ادامه از نخستین گام ناتمامِ دارای شاهد و مجوز باشد، نه پاک کردن پیشرفت.

### دامنهٔ انتشار و کار بعدی

این تغییر پذیرش مرحلهٔ صفر و نخستین برش کد 1A را ثبت و کار بعدی و ردیابی را به‌روز می‌کند. نیازهای منبع، پرامپت بایگانی‌شده، نمودارها و طرح Zabbix حفظ شده‌اند. ممیزی امنیت میزبان یا تثبیت سازگاری انجام نشده است.

برش 1A با Python 3.12.10، uv 0.12.17، Pydantic 2.13.5، Ruff 0.16.8، mypy 1.20.2، pytest 9.1.1 و `uv.lock` تولیدشده آزموده شد. ۱۸ آزمون unit و فرمان‌های Ruff، mypy سخت‌گیرانه، pytest، بررسی lock، نصب پاک قفل‌شده، `uv pip check` و audit وابستگی قبول شدند و audit آسیب‌پذیری شناخته‌شده‌ای گزارش نکرد. بررسی مستندات و `git diff --check` در دروازهٔ نهایی اجرا می‌شوند. آزمون سرویس یا مرورگر انجام نشده و هیچ VM، دیسک، شبکه، وصلهٔ ESXi، مدل، پایگاه یا سرویس پایش تغییر نکرده است.

نقطهٔ بعد Increment 2 از 1A در [کار بعدی](NEXT_TASK.md) است: bootstrap و recovery هویت محلی، migration و role واقعی PostgreSQL در محیط جدا، run و lease ماندگار، audit محدود، API حداقلی احرازشده و یک نتیجهٔ fixture دوزبانه. پذیرش مرحلهٔ صفر مجوز ساخت یا دسترسی مقصد نیست. سیاست قطعی، credential محدود، منع AI خارجی، دارایی و ورود و کلید و گواهی محلی، پشتیبان مستقل و محدودیت خرابی میزبان حفظ شوند. حفاظت مخزن، CI، گزارش خصوصی آسیب‌پذیری و مجوز نرم‌افزاری تنظیم‌شده فرض نشده‌اند.
