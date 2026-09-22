# Project state / وضعیت پروژه

Updated: 2026-09-22 — a controlled user-testing path is live across the app, AI, connector and Zabbix guests. Immutable app release `nextops-0.1.0-fde27bd` adds durable live-investigation runs: every started monitoring request now records its server-derived actor/scope and correlation ID, then atomically stores the bounded Zabbix snapshot and SHA-256 reference, local-model result and append-only audit outcome. General assistance remains separate and model-only. PostgreSQL, TLS/Nginx, both restricted SSH tunnels, the read-only connector, Zabbix 7.0.30 and self-monitoring are active. Live persistence/retrieval/hash/audit checks passed; broader host coverage and full failure, offline, reboot, recovery, scale and production acceptance remain open.

## English

### Current controlled user-testing checkpoint

The authenticated application and bilingual panel are deployed as immutable release
`nextops-0.1.0-fde27bd` on the app guest behind private TLS and Nginx. PostgreSQL 16 stores
application identity and session state on
its dedicated verified mount. Bootstrap and recovery endpoints, API documentation and the direct
application listener are not exposed through Nginx. The browser receives neither the AI service
credential nor the Zabbix token.

The dedicated Zabbix guest now runs Zabbix 7.0.30, PostgreSQL 16, Nginx/PHP-FPM and Agent 2. The
default administrator password was rotated. A separate API-only reader has no frontend access, an
allowlist limited to `host.get`, `item.get` and `problem.get`, read permission for one approved host
group and a token stored only on the connector guest. A non-allowlisted API call was denied and the
reader saw exactly one host. The connector uses verified TLS, bypasses inherited proxies, exposes
only a named summary operation on loopback and has no generic URL, JSON-RPC, shell or write surface.

The app reaches AI and connector loopback services through separate pinned-host-key SSH forwards.
Live qualification returned eight fresh self-monitoring measurements with zero stale metrics and no
active problems. The desktop end-to-end test passed login, session authentication, TLS validation,
live evidence retrieval and grounded English and Persian answers. The measured synthesis times were
56.6 seconds and 67.1 seconds for the 128-token ceiling. Visual review confirmed the English and
genuine RTL Persian login layouts. Source version, host, collection time, measurement time, stale
state and active-problem count are shown with the answer.

The first real browser request exposed a mismatch between the panel's 384-token request and the
qualified 120-second CPU generation boundary. It ended as a generic `503` even though readiness and
monitoring were healthy. The deployed repair caps live investigations to 128 tokens in both the
server and panel, preserves safe timeout/overload status across the internal boundary and displays
localized actionable errors. Replaying the exact `hi` request with the old 384-token payload passed
with HTTP 200, live evidence and 128 output tokens in 61.6 seconds. The previous immutable release
remains available for rollback.

That replay proved transport recovery but exposed a separate relevance defect: the panel routed
every question through `/api/v1/investigate`, so even `Hi` produced Zabbix status. Release
`nextops-0.1.0-3d61bf6` now makes **General assistant** the default and keeps **Live monitoring** as
an explicit opt-in mode. General questions use `/api/v1/assistant/generate`, receive no monitoring
evidence and carry a model-only badge; monitoring questions retain the evidence-grounded route and
panel. The exact default-mode request `Hi` returned “Hello! How can I assist you today?” in 14.0
seconds with no Zabbix or system-status content. A Persian greeting also returned a Persian general
answer without monitoring content. The monitoring regression passed with eight fresh metrics and
grounded English and Persian answers. Release `8d31bcb` remains available for rollback.

Release `nextops-0.1.0-fde27bd` completes the missing Stage 1D persistence link without a schema
migration. Before any connector or model call, `/api/v1/investigate` creates a scoped PostgreSQL run.
Successful completion atomically stores the already-bounded Zabbix summary, a canonical SHA-256
evidence reference, the model result and an append-only completion audit; safe failure code and
message metadata are likewise persisted and audited without raw exceptions. The panel exposes the
run, evidence and audit identifiers, and authenticated run retrieval returns the same scoped result.
All 95 non-integration tests and six isolated PostgreSQL tests pass. Live acceptance returned eight
fresh metrics, no active problems and a 128-token answer in 57.2 seconds; stored-run retrieval,
independent evidence-hash verification and audit linkage passed. A direct database check found the
successful `live_monitoring` result, two linked audit events, the 64-character hash and a matching
completion audit ID.

This is a controlled user-testing slice, not production acceptance. It currently monitors the
Zabbix server itself rather than the full estate. WAN-disconnection, VM-reboot, token revocation,
dependency-loss, stale/partial evidence, sustained load, independent backup/restore and disaster
recovery cases remain open. Private addresses, tokens, passwords, host keys and raw evidence remain
outside Git.

### Requirements and preserved history

The directly verified Git remote is `Omid-NextAI/nextops`, branch `main`. Earlier records name `AmirMo10/nextops`; current README/install clone commands now use the verified remote, while historical statements remain preserved and the active prompt header still needs a separately versioned repository-identity correction. The owner requested English and native-Persian documentation, a single English active prompt, local CPU-only AI, continued operation after Internet loss, a first useful Zabbix status answer, phased VM allocations, storage limits and a dedicated Zabbix server recommendation. All eleven integrations and the 51 original specification sections remain in scope.

The active [master prompt v3.0](requirements/NEXTOPS_MASTER_PROMPT.md) and [v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) remain unchanged in this update. The new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md) explicitly supersedes only the old small-lab recommendation and combined budgets; non-conflicting security, acceptance and feature requirements remain mandatory. The archive still contains the original Persian specification.

The first deliverable is a new Persian/English question about authorized Zabbix status, answered by local CPU generation from actual evidence, with source times, scope and audit while Internet is blocked. Linux enrichment follows in Phase 2. Documentation publication does not complete a software phase or establish deployment approval.

The paired [Phase 0 report](en/PHASE_0_REPORT.md) and [Persian report](fa/PHASE_0_REPORT.md) record repository evidence, the accepted four-VM architecture, trust boundaries, module and data contracts, CPU benchmark plan, resource gate, connector roadmap, test plan, blockers and the Stage 1A increments. The repository-grounded [threat model](requirements/nextops-threat-model.md) records TM-001–TM-010. On 2026-09-21 the owner accepted Phase 0 and ADRs 0001–0006, confirming one organization initially, small initial scale with future growth, and the dedicated Zabbix path. Every infrastructure authorization remains separate and pending.

Stage 1A Increments 1 and 2 are implemented in repository source. In addition to the locked Python project, strict contracts and deterministic denial policy, the code now has a local FastAPI surface, Argon2id identity bootstrap/login/recovery, hashed opaque sessions, PostgreSQL/Alembic state, idempotent durable runs, expiring worker leases, append-restricted audit, and an explicit bilingual fixture result. Actor organization, environment, roles and scopes are derived from server-side session state. Four guarded scripts now define the authenticated offline Ubuntu package layer for the initial servers, but no approved package bundle, browser UI, deployable offline application release/service definition, target connector or credential, or production listener exists. The pinned AI runtime/model and its separate source service profile are recorded below.

Stage 1B Increment 3 adds a strict runtime-neutral `LLMProvider` contract, authenticated inference API, loopback-only llama.cpp adapter, one-active/two-queued scheduler, bounded input/output/timeouts, cancellation cleanup, safe readiness, and structured overload/dependency failures. A schema-validated YAML manifest pins llama.cpp `v0.4.1` and the official `Qwen3-8B-Q4_K_M.gguf`. The pinned runtime and model are now installed with the corrected API release on the qualified AI guest. Controlled live quality, bounded load, restart, and application-link rollback evidence exists; complete failure injection, VM reboot, runtime/model rollback, explicit WAN-disconnection, and isolated restore remain open.

The native Stage 1B slice supplies separate hardened `nextops-llama` and `nextops-ai` units, two
`LoadCredential` secrets, loopback-only cgroup networking, read-only release trees, explicit
CPU/memory/task limits, a strict credential-file loader, and a versioned Persian/English
qualification corpus and runner. It is now live on the AI guest. The first start exposed an invalid
relocated shared-library search path and an insufficient socket-only readiness gate; the unit now
uses the protected stable runtime library directory and controlled startup waits for authenticated
model health. The owner-authorized deployment account now has full passwordless administration;
direct root SSH remains disabled.

### Supplied hardware and storage evidence

The [hardware record](requirements/HARDWARE_BASELINE.json) preserves the owner's ESXCLI output: ESXi 8.0.3 build 24414501; 4 CPU packages, 112 physical cores, 224 logical threads, active hyperthreading, 4 NUMA nodes and 1,442,743,631,872 memory bytes (calculated about 1343.66 GiB). It includes the partial CPU 0/1 sample, reported speed/cache/microcode and reference mappings documented in [ESXI_BASELINE](en/ESXI_BASELINE.md). Exact marketing SKU, rated speed, all-package consistency, guest ISA and actual per-node distribution are not established by that sample. Arithmetic averages are not observed topology or free resources.

Owner-supplied mounted VMFS rows now establish point-in-time capacity: DS-A 149.75 GiB total / 148.34 GiB free; DS-B 1117.50 / 1109.87; DS-C 3576.75 / 3166.8701171875. Public aliases omit real names, UUIDs and mount paths. [STORAGE_PLAN](STORAGE_PLAN.md) excludes VMFSOS/boot volumes, leaves DS-A/DS-B outside the initial allocation and retains the 3 TB project ceiling. The proposed DS-C free target is 25%, exactly 894.1875 GiB or conservatively about 900 GiB. No datastore reservation, RAID/health inspection or I/O benchmark follows from the supplied listing.

Preserve ESXi; Ubuntu Server 24.04 LTS is the approved guest baseline, not a host replacement. Supplied totals/build/listing should not be requested as missing. Current available CPU/RAM, load/reservations, actual physical NUMA placement, VM compatibility and license limits, storage backing/health/latency, outstanding growth and swap placement remain to be checked at execution time. No direct ESXi host access or compatibility certification was performed.

### Sanitized replacement-guest qualification

On 2026-09-21, authorized read-only SSH preflight reached all four clean replacement guests after the owner supplied their new Ed25519 fingerprints independently and each matched the live handshake. Key-only authentication, strict host-key checking and direct-root denial were verified. The configured vCPU, memory, virtual-disk and dedicated-mount layouts match the public role budgets. All guests run Ubuntu 24.04.5 LTS under VMware. On 2026-09-22 the fleet was rechecked after the AI deployment and a narrow GLib security update on app: every guest reported `running` systemd state, zero failed units, zero pending package upgrades and no reboot requirement. UFW remains active. The only new product listeners are the two intended AI loopback endpoints; no public product listener was added.

After explicit owner authorization for connected preparation, each host used its existing strict proxy chain to refresh signed repositories and install only its role package layer. No broad OS upgrade ran. Exact observed direct versions are PostgreSQL 16.15 and Nginx 1.24 on app; GCC 13.3, CMake 3.28, Ninja 1.11 and OpenBLAS 0.3.26 on AI; Python 3.12 venv support on connectors; and Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24 and PHP 8.3.6 on Zabbix. The official Zabbix 7.0 Ubuntu 24.04 release bootstrap package was pinned by SHA-256 before repository import. Package post-install starts were blocked and, at that preparation checkpoint, all product/database/web services were inactive and disabled, no PostgreSQL cluster existed, and no listener was added. Only the AI slice has since been deliberately activated. Docker was not installed because the selected native systemd design does not need it and a container socket would enlarge the trust boundary.

Protected non-login service identities and role directories now exist. The pinned llama.cpp commit was built on the qualified AI guest with Release, CPU-native, OpenMP and OpenBLAS settings and no GPU linkage; its promoted binary hash is in the inference manifest. The pinned 5,027,783,488-byte Qwen model matched its expected SHA-256 before and after protected-volume promotion. The active immutable API release is `nextops-0.1.0-62de8d6`; `417d888` is the tested application rollback. Two independent qualification runs returned `401` for unauthenticated generation, `200` for readiness, and acceptable Persian/English evidence and safety answers under automated checks and human review. The bounded load probe observed one accepted request with the remaining concurrent requests rejected or timed out according to the scheduler/timeout boundary. A cold process restart restored both services in 109 seconds. Application rollback and forward restoration passed authentication/readiness checks and left `62de8d6` active. Both services are enabled, unprivileged, CPU-only, and limited to `127.0.0.1:8080` and `127.0.0.1:8090`; `systemd-analyze security` reports `2.7 OK` for each. Raw evidence, credentials, addresses and host keys remain outside Git. Runtime/model rollback, live cancellation and corrupt-artifact cases, VM reboot, explicit WAN-disconnection observation, dependency-license approval, independent backup/restore and production performance thresholds remain open. The general application release, PostgreSQL/Zabbix initialization, reverse proxy/TLS and end-to-end acceptance remain separate gates.

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

Each role now has an executable entry script under `deploy/installers`. A shared tested engine authenticates an all-file bundle manifest against a separately supplied SHA-256, requires exact Debian package versions including the dependency closure, isolates APT to the signed local repository, rejects unexpected installs/removals, blocks package-managed service startup and automatic PostgreSQL cluster creation, and verifies installed versions. Apply additionally requires root, Ubuntu 24.04 on VMware, root-owned/non-writable bundle contents, an explicit authorization marker and a change ID. Check mode performs bundle validation only. No real package lock, signing key, repository bundle, or clean-server apply evidence exists in this repository.

These records expose rather than hide the deployment blockers: the application source, migration and package-layer scripts exist, but no approved general offline application bundle, complete production installer, reverse proxy, browser UI, or tested backup/restore bundle exists. The hardened AI services and immutable releases are now installed and controlled qualification plus application rollback passed; dependency-license approval, the remaining failure matrix, runtime/model rollback, explicit WAN-disconnection/VM-reboot tests, independent restore, and production performance targets remain unresolved. The replacement guests and dedicated mounts are qualified, but private application/connector/Zabbix configuration, production PostgreSQL and Zabbix initialization, and complete server acceptance remain open. No production database, Zabbix state, public product listener, certificate, target token, backup, or restore was created.

### Durable agent context

Three repository-scoped Codex skills under `.agents/skills` now route general project work, server operations, and bilingual documentation. [MARKDOWN_CONTEXT_INDEX](MARKDOWN_CONTEXT_INDEX.md) catalogs all 93 project-owned Markdown files and maps task types to the relevant sources without loading the entire documentation set into every context window. The documentation validator excludes dependency/build trees and fails on a missing or stale catalog entry; three focused tests cover discovery and catalog reconciliation. This is development-context infrastructure, not application or deployment capability.

### Milestones and actual evidence status

| Stage | Required result | Evidence status for this update |
|---|---|---|
| 0 | Architecture/gap/threat report and appropriate approvals | Owner accepted architecture/roadmap and ADRs on 2026-09-21; the clean replacement guests passed read-only qualification, while ESXi/storage refresh and operation-specific authorization remain separate |
| 1A | Local identity, policy, database, durable work and audit | Authenticated app, PostgreSQL migration, private TLS panel and session path are live for controlled testing; durable live-investigation and audit linkage now uses the existing scoped run model |
| 1B | New local CPU answers and offline model cold load | The pinned runtime/model and corrected API release are installed behind hardened loopback-only units; authentication, bilingual quality, bounded load, cold process restart and application rollback/restoration passed. VM reboot, explicit WAN-disconnection, remaining failure/cancellation tests, runtime/model rollback, independent restore and production targets remain open |
| Zabbix prerequisite | Dedicated database mount, monitoring, frontend/API and scoped reader before 1C | Zabbix 7.0.30, PostgreSQL, TLS frontend/API, Agent 2, self-monitoring and the scoped reader are active; API allowlist, host scope and denial checks passed |
| 1C | Real bounded read-only evidence with correct counts | Controlled live connector qualification passed with eight fresh measurements, explicit timestamps/staleness and zero active problems; broader estate coverage and the full failure matrix remain |
| 1D | New evidence-linked Zabbix answer with audit | English/Persian grounded answers pass; every started live investigation now has a durable scoped run, bounded evidence snapshot/hash, model result, safe failure outcome and append-only audit linkage verified in isolated PostgreSQL and the live path |
| 1E | Offline fresh login/restart, security/failure/capacity tests | Fresh authenticated desktop use passed online on the private LAN; WAN-blocked, reboot, revocation, failure, recovery and sustained-capacity cases remain |

The user may perform provisioning independently; verify their actual state before claiming a VM either exists or does not exist. A screenshot of VM settings is not proof of an accepted application workflow. Resume from the next evidenced, authorized incomplete stage rather than resetting progress.

### Scope of this publication and next action

This state records Phase 0 acceptance, the deployed controlled Stage 1A application slice, the qualified Stage 1B AI slice, the live Stage 1C read-only connector and the durable evidence-linked Stage 1D user-test path. It preserves the source requirements, archived prompt, diagrams and per-server handoff. It is not a host vulnerability audit, production acceptance, independent recovery proof or complete provisioning record.

The source slices use Python 3.12.10, uv 0.12.17, Pydantic 2.13.5, FastAPI 0.141.1, SQLAlchemy 2.0.54, Alembic 1.20.0, Psycopg 3.3.6, Ruff 0.16.8, mypy 1.20.2 and pytest 9.1.1 with a generated `uv.lock`. Ruff, strict mypy over 57 files, 95 non-integration tests and all six tests against a temporary isolated PostgreSQL 16.15 database pass. The temporary database, login role, credential and SSH tunnel were removed after validation. Hosted CI evidence remains revision-specific. Documentation/catalog/dossier validation, dependency and license review, broader security/failure testing and recovery evidence remain merge or production gates. Visual bilingual login review and programmatic live end-to-end testing ran; full browser workflow automation, WAN-disconnection/VM-reboot acceptance, independent backup and isolated restore did not.

The next checkpoint in [NEXT_TASK](NEXT_TASK.md) is to harden the working user-test slice without reinstalling it: add the remaining approved hosts, exercise stale/partial/unreachable/revoked-token cases, then run explicit WAN-disconnection, VM-reboot, rollback and independent restore acceptance. Production promotion remains gated on those results, retention/backup decisions, sustained resource measurements and operational sign-off.

## فارسی

### نقطهٔ فعلی برای ارزیابی کنترل‌شدهٔ کاربران

برنامهٔ احرازهویت‌شده و پنل دوزبانه، در انتشار تغییرناپذیر `nextops-0.1.0-fde27bd` روی مهمان برنامه و پشت TLS خصوصی
و Nginx فعال‌اند. PostgreSQL 16 هویت و نشست برنامه را روی فضای ذخیره‌سازی مستقل و تأییدشده نگه
می‌دارد. مسیرهای راه‌اندازی اولیه و بازیابی، مستندات API و درگاه مستقیم برنامه از Nginx در دسترس
نیستند. هیچ‌یک از اعتبارنامه‌های سرویس هوش مصنوعی یا Zabbix به مرورگر تحویل نمی‌شود.

مهمان مستقل پایش اکنون Zabbix 7.0.30، PostgreSQL 16، Nginx/PHP-FPM و Agent 2 را اجرا می‌کند.
گذرواژهٔ مدیر پیش‌فرض عوض شده است. خوانشگر جداگانهٔ API به رابط کاربری دسترسی ندارد؛ فقط سه روش
`host.get`، `item.get` و `problem.get` برایش مجاز است و تنها یک گروه میزبان مصوب را می‌بیند.
فراخوانی خارج از فهرست مجاز رد شد و دامنهٔ دید آن دقیقاً یک میزبان بود. توکن فقط روی مهمان اتصال
نگه‌داری می‌شود. اتصال نیز فقط از TLS معتبر استفاده می‌کند، پراکسی موروثی را کنار می‌گذارد و روی
رابط محلی صرفاً یک عملیات نام‌دار برای خلاصهٔ پایش ارائه می‌دهد؛ نشانی دلخواه، JSON-RPC عمومی، shell
یا عملیات نوشتنی در اختیار مصرف‌کننده نیست.

برنامه از دو تونل SSH جدا با کلید میزبان ثابت‌شده به سرویس‌های محلی هوش مصنوعی و اتصال می‌رسد.
صلاحیت‌سنجی زنده، هشت سنجهٔ تازهٔ خودپایشی، بدون سنجهٔ قدیمی و بدون مسئلهٔ فعال بازگرداند. آزمون
سراسری از رایانهٔ کاربر، TLS، ورود و نشست، دریافت شاهد و پاسخ مستند فارسی و انگلیسی را با موفقیت
گذراند. زمان تولید با سقف ۱۲۸ توکن برای انگلیسی ۵۶٫۶ ثانیه و برای فارسی ۶۷٫۱ ثانیه بود. نمایش
انگلیسی و چیدمان راست‌به‌چپ فارسی نیز به‌صورت دیداری بازبینی شد. نسخهٔ منبع، میزبان، زمان گردآوری،
زمان اندازه‌گیری، وضعیت تازگی و شمار مسئله‌های فعال کنار پاسخ نمایش داده می‌شود.

نخستین درخواست واقعی مرورگر، ناسازگاری میان درخواست ۳۸۴ توکنی پنل و مهلت تأییدشدهٔ ۱۲۰ ثانیه‌ای
پردازش روی CPU را آشکار کرد. با وجود سلامت آمادگی و پایش، درخواست در پایان به خطای عمومی `503`
رسید. اصلاح مستقرشده سقف بررسی زنده را در سرور و پنل به ۱۲۸ توکن محدود می‌کند، وضعیت امن پایان
مهلت و اشباع را در مرز داخلی حفظ می‌کند و پیام خطای روشن و بومی‌شده نشان می‌دهد. بازاجرای همان
پرسش `hi` با payload قدیمی ۳۸۴ توکنی، در ۶۱٫۶ ثانیه با HTTP 200، شاهد زنده و ۱۲۸ توکن خروجی موفق
شد. انتشار تغییرناپذیر قبلی نیز برای بازگشت نگه‌داری می‌شود.

این بازآزمایی، ترمیم مسیر فنی را ثابت کرد؛ اما یک اشکال جدا در ارتباط معنایی پاسخ را نیز نشان داد:
پنل همهٔ پرسش‌ها را به `/api/v1/investigate` می‌فرستاد و به همین دلیل حتی `Hi` با گزارش Zabbix
پاسخ داده می‌شد. در انتشار `nextops-0.1.0-3d61bf6`، **دستیار عمومی** حالت پیش‌فرض است و **پایش
زنده** فقط با انتخاب صریح کاربر فعال می‌شود. پرسش عمومی از مسیر `/api/v1/assistant/generate`
می‌گذرد، هیچ شاهد پایشی دریافت نمی‌کند و با نشان «مدل محلی، بدون شاهد زنده» نمایش داده می‌شود؛
مسیر پایش همچنان پاسخ را به شواهد Zabbix مستند می‌کند. درخواست دقیق `Hi` در حالت پیش‌فرض طی ۱۴٫۰
ثانیه پاسخ “Hello! How can I assist you today?” گرفت و هیچ اشاره‌ای به Zabbix یا وضعیت سامانه
نداشت. سلام فارسی نیز پاسخ عمومی فارسی و بدون محتوای پایشی دریافت کرد. آزمون بازگشت پایش زنده با
هشت سنجهٔ تازه و پاسخ مستند انگلیسی و فارسی موفق بود. انتشار `8d31bcb` برای بازگشت محفوظ است.

انتشار `nextops-0.1.0-fde27bd` پیوند ماندگارِ باقی‌مانده از 1D را بدون migration تازه تکمیل می‌کند.
مسیر `/api/v1/investigate` پیش از فراخوانی اتصال یا مدل، اجرای محدود به دامنه را در PostgreSQL
می‌سازد. هنگام موفقیت، خلاصهٔ ازپیش‌محدودشدهٔ Zabbix، مرجع SHA-256 شاهد، نتیجهٔ مدل و رخداد تکمیل
ممیزی به‌صورت اتمی ثبت می‌شوند. در حالت شکست نیز فقط کد و کلید پیام امن ذخیره و ممیزی می‌شود و
خطای خام وارد پایگاه نمی‌شود. پنل شناسهٔ اجرا، شاهد و ممیزی را نمایش می‌دهد و بازیابی
احرازهویت‌شدهٔ اجرا همان نتیجهٔ محدود به دامنه را برمی‌گرداند. هر ۹۵ آزمون غیر‌یکپارچه و شش آزمون
PostgreSQL در پایگاه موقت و جداگانه موفق بودند. آزمون زنده هشت سنجهٔ تازه، بدون مسئلهٔ فعال و پاسخ
۱۲۸ توکنی را در ۵۷٫۲ ثانیه بازگرداند؛ بازیابی نتیجه، محاسبهٔ مستقل هش و پیوند ممیزی نیز موفق بود.
بررسی مستقیم پایگاه، نتیجهٔ `live_monitoring`، دو رویداد ممیزی پیوندخورده، هش ۶۴ نویسه‌ای و تطبیق
شناسهٔ ممیزی تکمیل با نتیجهٔ ذخیره‌شده را تأیید کرد.

این خروجی برای ارزیابی کنترل‌شده است، نه پذیرش تولید. فعلاً فقط خود سرور Zabbix پایش می‌شود و همهٔ
تجهیزات وارد دامنه نشده‌اند. آزمون قطع WAN، راه‌اندازی مجدد ماشین، لغو توکن، قطع وابستگی، دادهٔ
قدیمی یا ناقص، بار پایدار، پشتیبان مستقل، بازیابی و سناریوی بحران همچنان بازند. نشانی‌ها، توکن‌ها،
گذرواژه‌ها، کلیدهای میزبان و شواهد خام بیرون Git مانده‌اند.

### نیازها و سابقهٔ محفوظ

remote بررسی‌شدهٔ مستقیم Git برابر `Omid-NextAI/nextops` و شاخه `main` است. فرمان‌های clone جاری در README و راهنمای نصب اکنون remote درست را دارند؛ رکوردهای تاریخی `AmirMo10/nextops` حفظ می‌شوند و عنوان پرامپت فعال هنوز به اصلاح جداگانه و نسخه‌دار نیاز دارد. مالک مستندات فارسی طبیعی و انگلیسی، یک پرامپت فعال انگلیسی، AI محلی روی CPU، ادامهٔ کار پس از قطع اینترنت، پاسخ وضعیت Zabbix در اولین تحویل، برنامهٔ ماشین‌ها و محدودیت ذخیره‌سازی و سرور مستقل Zabbix را خواسته است. یازده اتصال و ۵۱ بخش مشخصات اولیه در دامنه باقی‌اند.

[پرامپت فعال ۳.۰](requirements/NEXTOPS_MASTER_PROMPT.md) و [بایگانی نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) در این تغییر دست‌نخورده‌اند. [اصلاحیهٔ استقرار](requirements/DEPLOYMENT_UPDATE.md) فقط پیشنهاد آزمایشگاه کوچک و مجموع منابع وابسته را صریح جایگزین می‌کند؛ سایر نیازهای امنیت، پذیرش و قابلیت‌ها پابرجا هستند. مشخصات فارسی اولیه همچنان در بایگانی محفوظ است.

اولین خروجی، پاسخ تازهٔ فارسی یا انگلیسی دربارهٔ وضعیت مجاز Zabbix، تولیدشده روی CPU محلی و مستند به دادهٔ واقعی، همراه منبع و زمان و دامنه و ممیزی با اینترنت قطع است. بررسی مستقیم Linux در مرحلهٔ دو می‌آید. انتشار مستندات، پایان مرحلهٔ نرم‌افزاری یا اثبات مجوز استقرار نیست.

[گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md) و [مدل تهدید](requirements/nextops-threat-model.md) یافتهٔ مخزن، معماری چهارماشینی پذیرفته‌شده، مرز اعتماد، قرارداد ماژول و داده، برنامهٔ سنجش CPU، بودجه، نقشهٔ اتصال، آزمون و گام‌های 1A را ثبت می‌کنند. مالک در ۲۱ سپتامبر ۲۰۲۶ مرحلهٔ صفر و ADRهای 0001 تا 0006 را با تک‌سازمانی بودن فعلی، مقیاس کوچک اولیه با رشد آینده و Zabbix مستقل پذیرفت. همهٔ مجوزهای زیرساخت جدا و در انتظار باقی می‌مانند.

Incrementهای 1 و 2 از 1A در کد مخزن پیاده شده‌اند. علاوه بر پروژهٔ Python قفل‌شده، قراردادهای سخت‌گیر و سیاست رد قطعی، اکنون FastAPI محلی، bootstrap/login/recovery با Argon2id، session غیرشفافِ hash‌شده، PostgreSQL/Alembic، run ماندگار و idempotent، lease منقضی‌شونده، audit محدود به append و نتیجهٔ fixture دوزبانه وجود دارد. سازمان، محیط، role و scope از session سمت سرور ساخته می‌شوند. چهار اسکریپت محافظت‌شده لایهٔ بسته‌های آفلاین و معتبر Ubuntu را برای سرورهای اولیه تعریف می‌کنند؛ اما بستهٔ تأییدشده، رابط مرورگر، انتشار آفلاین یا تعریف سرویس قابل‌استقرار برنامه، اتصال یا اعتبارنامهٔ مقصد و شنوندهٔ تولید وجود ندارد. محیط اجرا و مدل ثابت هوش مصنوعی و پروفایل مبدأ و مستقل سرویس آن در ادامه ثبت شده‌اند.

Increment 3 از 1B قرارداد مستقل و سخت‌گیر `LLMProvider`، API احرازهویت‌شدهٔ پردازش مدل، رابط فقط‌محلی llama.cpp، صف با یک درخواست فعال و دو درخواست در انتظار، کران ورودی و خروجی و زمان، پاک‌سازی لغو، اعلام آمادگی ایمن و خطاهای ساخت‌یافتهٔ اضافه‌بار و وابستگی را فراهم می‌کند. پروندهٔ YAML معتبرشده، llama.cpp نسخهٔ `v0.4.1` و فایل رسمی `Qwen3-8B-Q4_K_M.gguf` را تثبیت می‌کند. محیط اجرا و مدل ثابت اکنون همراه انتشار اصلاح‌شدهٔ API روی مهمان هوش مصنوعی نصب شده‌اند. کیفیت زندهٔ کنترل‌شده، بار محدود، راه‌اندازی دوبارهٔ فرایندها و بازگشت پیوند انتشار برنامه شاهد دارند؛ تزریق کامل خطا، راه‌اندازی مجدد ماشین، بازگشت محیط اجرا و مدل، مشاهدهٔ صریح هنگام قطع WAN و بازیابی جداگانه همچنان باز است.

برش بومی 1B دو واحد جدا و سخت‌سازی‌شدهٔ `nextops-llama` و `nextops-ai`، دو اعتبارنامهٔ فایل‌محور، محدودیت شبکه به رابط محلی در سطح cgroup، درخت انتشار فقط‌خواندنی، سقف صریح منابع، بارگذاری سخت‌گیرانهٔ اعتبارنامه و مجموعهٔ نسخه‌دار سنجش فارسی و انگلیسی را فراهم می‌کند و اکنون روی مهمان هوش مصنوعی فعال است. نخستین اجرا، مسیر نادرست کتابخانه‌های مشترک پس از جابه‌جایی و ناکافی بودن بررسی صرفِ باز شدن درگاه را آشکار کرد؛ واحد اصلاح‌شده از مسیر ثابت و محافظت‌شدهٔ کتابخانه‌ها استفاده می‌کند و شروع کنترل‌شده تا سلامت احرازهویت‌شدهٔ مدل منتظر می‌ماند. حساب استقرار بنا بر دستور مالک اکنون مدیریت کامل و بدون گذرواژه دارد؛ ورود مستقیم root از راه SSH همچنان بسته است.

### شواهد ارسالی سخت‌افزار و دیسک

[رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خروجی ESXCLI مالک را حفظ می‌کند: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هسته، ۲۲۴ رشته، Hyperthreading فعال، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، تقریباً ۱۳۴۳٫۶۶ GiB. نمونهٔ ناقص CPU 0 و 1، سرعت و cache و microcode ارسالی و نگاشت‌های مرجع در [یادداشت ESXi](fa/ESXI_BASELINE.md) ثبت‌اند. مدل تجاری دقیق، فرکانس اسمی، یکسان بودن همهٔ بسته‌ها، ISA مهمان و توزیع واقعی گره‌ها از نمونه ثابت نمی‌شوند. میانگین حسابی، توپولوژی یا ظرفیت آزاد مشاهده‌شده نیست.

ظرفیت لحظه‌ای VMFS ارسالی: DS-A برابر ۱۴۹٫۷۵ GiB کل و ۱۴۸٫۳۴ آزاد؛ DS-B برابر ۱۱۱۷٫۵۰ و ۱۱۰۹٫۸۷؛ DS-C برابر ۳۵۷۶٫۷۵ و 3166.8701171875. نام واقعی، UUID و مسیر در رکورد عمومی نیستند. [برنامهٔ دیسک](STORAGE_PLAN.md) حجم‌های سیستم و راه‌اندازی را کنار می‌گذارد، DS-A و DS-B را تخصیص نمی‌دهد و سقف سه‌ترابایتی را حفظ می‌کند. هدف پیشنهادی فضای آزاد DS-C برابر ۲۵ درصد، دقیقاً 894.1875 GiB و با گردکردن حدود ۹۰۰ GiB است. فهرست ارسالی، رزرو، سلامت RAID یا سنجش I/O نیست.

ESXi حفظ شود؛ Ubuntu Server 24.04 LTS خط مبنای تأییدشدهٔ مهمان است، نه جایگزین میزبان. مجموع‌ها و نسخه و فهرست دوباره به‌عنوان دادهٔ غایب خواسته نشوند. CPU/RAM آزاد فعلی، بار و رزرو، جای‌گذاری فیزیکی NUMA، سازگاری و محدودیت مجوز، سلامت و تأخیر دیسک، رشد و محل swap باید هنگام اجرا بررسی شوند. اتصال مستقیم به میزبان ESXi یا تأیید سازگاری انجام نشده است.

### صلاحیت‌سنجی پاک‌سازی‌شدهٔ مهمان‌های جایگزین

در ۲۱ سپتامبر ۲۰۲۶، پس از ارسال مستقل اثرانگشت‌های تازهٔ Ed25519 توسط مالک و برابری هرکدام با ارتباط زنده، پیش‌بررسی فقط‌خواندنی مجاز از راه SSH به هر چهار مهمان جایگزین رسید. احراز هویت فقط با کلید، کنترل سخت‌گیرانهٔ کلید میزبان و رد ورود مستقیم root تأیید شد و منابع هر نقش با بودجهٔ عمومی برابر بود. در ۲۲ سپتامبر، پس از استقرار هوش مصنوعی و یک به‌روزرسانی محدود امنیتی GLib روی مهمان برنامه، همهٔ مهمان‌ها دوباره بررسی شدند: وضعیت systemd در هر چهار مورد `running`، شمار واحد خراب و بستهٔ قابل‌ارتقا صفر و راه‌اندازی مجدد لازم نبود. UFW فعال مانده است. تنها شنونده‌های تازهٔ محصول، دو درگاه محلی و موردانتظار هوش مصنوعی‌اند و هیچ شنوندهٔ عمومیِ محصول ایجاد نشده است.

پس از مجوز صریح مالک برای آماده‌سازی متصل، هر میزبان از زنجیرهٔ پراکسی سخت‌گیرانهٔ موجود برای تازه‌سازی مخزن‌های امضاشده و نصب فقط لایهٔ بستهٔ نقش خود استفاده کرد. ارتقای کلی سیستم‌عامل اجرا نشد. نسخه‌های مستقیم مشاهده‌شده عبارت‌اند از PostgreSQL 16.15 و Nginx 1.24 در برنامه؛ GCC 13.3، CMake 3.28، Ninja 1.11 و OpenBLAS 0.3.26 در هوش مصنوعی؛ پشتیبانی محیط مجازی Python 3.12 در connectors؛ و Zabbix 7.0.30، PostgreSQL 16.15، Nginx 1.24 و PHP 8.3.6 در Zabbix. بستهٔ راه‌انداز رسمی Zabbix 7.0 برای Ubuntu 24.04 پیش از افزودن مخزن با SHA-256 ثابت شد. شروع خودکار پس از نصب مسدود بود و در همان نقطهٔ آماده‌سازی، همهٔ سرویس‌های محصول، پایگاه و وب غیرفعال بودند، خوشهٔ PostgreSQL ساخته نشده بود و درگاه تازه‌ای باز نشد. پس از آن فقط برش هوش مصنوعی آگاهانه فعال شده است. Docker نصب نشد، چون طراحی بومی systemd به آن نیاز ندارد و سوکت کانتینر مرز اعتماد را بزرگ می‌کند.

هویت‌های بدون ورود و مسیرهای محافظت‌شدهٔ نقش ساخته شده‌اند. llama.cpp با تنظیم Release، اجرای بومی CPU، OpenMP و OpenBLAS و بدون پیوند GPU ساخته شد و مدل Qwen با اندازهٔ ۵٬۰۲۷٬۷۸۳٬۴۸۸ بایت پیش و پس از انتقال به فضای محافظت‌شده با SHA-256 موردانتظار برابر بود. انتشار تغییرناپذیر و فعال API، `nextops-0.1.0-62de8d6` است و `417d888` به‌عنوان نسخهٔ آزموده‌شدهٔ بازگشت برنامه نگه‌داری می‌شود. در دو اجرای مستقل، تولید بدون احراز هویت با `401` رد، آمادگی با `200` تأیید و پاسخ‌های فارسی و انگلیسیِ شاهد و ایمنی هم در بررسی خودکار و هم در بازبینی انسانی پذیرفته شدند. آزمون بار محدود، یک درخواست پذیرفته‌شده و مهار درخواست‌های هم‌زمان اضافه را مطابق صف و پایان مهلت ثبت کرد. توقف و شروع سرد فرایندها هر دو سرویس را در ۱۰۹ ثانیه بازگرداند. بازگشت برنامه و سپس بازگرداندن نسخهٔ پذیرفته‌شده نیز موفق بود و در پایان `62de8d6` فعال ماند. هر دو سرویس با هویت بدون امتیاز، فقط روی CPU و فقط روی `127.0.0.1:8080` و `127.0.0.1:8090` اجرا می‌شوند و ارزیابی امنیتی systemd برای هرکدام `2.7 OK` است. شواهد خام، اعتبارنامه‌ها، نشانی‌ها و کلیدهای میزبان بیرون Git مانده‌اند. بازگشت محیط اجرا و مدل، لغو زنده و فایل خراب، راه‌اندازی مجدد ماشین، مشاهدهٔ صریح هنگام قطع WAN، مجوز وابستگی‌ها، پشتیبان مستقل و بازیابی جدا و هدف کارایی تولیدی هنوز باز است. استقرار عمومی برنامه، ایجاد PostgreSQL و Zabbix، reverse proxy/TLS و پذیرش سراسری نیز دروازه‌های جدا هستند.

### چیدمان فعلیِ پیشنهادی

برنامهٔ NextOps همان ۸ vCPU و ۳۲ GiB و ۲۰۰ GiB؛ AI همان ۲۴ و ۱۲۸ و ۵۰۰؛ اتصال همان ۴ و ۸ و ۸۰ است. **سرور مستقل `zabbix-server` با ۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB پیش از اتصال زندهٔ 1C** اضافه می‌شود. پایگاه NextOps از مرحلهٔ سه با ۸ و ۶۴ و ۳۰۰ پیشنهاد می‌شود؛ اجرای تغییر فقط در مرحلهٔ هفت و با مجوز، ۴ و ۱۶ و ۸۰ است.

سرور Zabbix پایگاه پایش، رابط و API خودش را دارد، نه مدل یا پایگاه NextOps. در مسیر جدید، جایگزین آزمایشگاه ۴ vCPU و ۸ GiB و ۱۰۰ GiB می‌شود؛ هر دو ساخته نشوند. Zabbix محلی موجودِ مناسب و مجاز ابتدا بررسی و استفاده شود. تعداد ماشین‌های خود NextOps همچنان ۳، ۴ و ۵ و مجموع شامل پایش ۴، ۵ و ۶ است.

چیدمان اولیه **۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** دارد؛ با سهم موقت ESXi swap برابر ۱۸۴ GiB، جمع پیش از سربار **۱۱۶۴ GiB** است. چیدمان‌های بعدی به‌ترتیب ۴۸ و ۲۴۸ و ۱۲۸۰، با جمع ۱۵۲۸ GiB؛ و ۵۲ و ۲۶۴ و ۱۳۶۰، با جمع ۱۶۲۴ GiB هستند. با مصرف قبلی ثابت، فضای آزاد فرضی DS-C برابر ۲۰۰۲٫۸۷، ۱۶۳۸٫۸۷ و ۱۵۴۲٫۸۷ GiB می‌شود. این‌ها بودجه‌های جایگزین‌اند، نه جمع‌شونده، رزرو، سنجش یا مجوز مصرف همهٔ فضا. رشد، VMX، snapshot، ورود فایل و بازیابی جدا و ماشین موجود بدون دوباره‌شماری حساب شوند.

راهنمای [فارسی](fa/ZABBIX_SERVER.md) و [انگلیسی](en/ZABBIX_SERVER.md) نرم‌افزار پیشنهادی Zabbix 7.0 LTS، PostgreSQL 16، Nginx، PHP-FPM و Agent 2، چیدمان کامل `vg_zabbix`، پیشنهاد history هفت‌روزه و trends عددی نودروزه، هویت API محدود، خودپایشی، پذیرش آفلاین و خطر تک‌میزبان را ثبت می‌کنند. بستهٔ دقیق، تنظیم نگهداری و VM/LVM از طریق این مستندات نصب یا آزموده نشده‌اند. اعداد پیشنهادی در [رکورد Zabbix](requirements/ZABBIX_SERVER_PLAN.json) جدا از شاهد سخت‌افزار آمده‌اند.

### پروندهٔ هر سرور برای مسئول استقرار

[مشخصات پرونده](requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md)، [JSON Schema مشترک](../deploy/server-dependencies/server-dependency.schema.json) و چهار فایل YAML خوانا برای `nextops-app`، `nextops-ai`، `nextops-connectors-ro` و `zabbix-server` اکنون تحویل ماشین‌خوان هر سرور را فراهم می‌کنند. راهنمای [فارسی](fa/DEPLOYMENT_DOSSIERS.md) و [انگلیسی](en/DEPLOYMENT_DOSSIERS.md) روش تکمیل ورودی خصوصی بدون commit آن را شرح می‌دهند.

هر پرونده وضعیت مجوز، منبع، منابع VM، هویت سرویس، قفل نرم‌افزار و artifact، مسیر تنظیمات، secret reference، مرز شبکه و storage، ترتیب سرویس، فرمان فقط‌خواندنی یا الگوی محافظت‌شده، فرمان مسدود، مشاهده‌پذیری، backup و rollback، ورودی لازم، دروازهٔ پذیرش و محدودیت را دارد. مقدارهای معلوم با مجموع ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB سازگارند و mountهای Zabbix با طرح ۲۰۰ GiB تطبیق دارند. تبدیل درخواستی JSON به YAML همهٔ مقدارها را بدون اتلاف حفظ کرد. اعتبارسنج مخزن چهار فایل YAML را ایمن parse می‌کند، schema نسخهٔ ۱.۰.۰ و شناسه‌های پذیرفته‌شده را می‌سنجد، باقی‌ماندن نسخهٔ قدیمی JSON را رد می‌کند و مجموع منابع را تطبیق می‌دهد.

برای هر role یک script اجرایی در `deploy/installers` وجود دارد. موتور مشترک و آزموده، manifest همهٔ فایل‌های bundle را با SHA-256 جداگانه تطبیق می‌دهد، نسخهٔ دقیق همهٔ packageها و وابستگی‌ها را لازم می‌داند، APT را فقط به repository محلی امضاشده محدود می‌کند، نصب یا حذف پیش‌بینی‌نشده را رد می‌کند، شروع خودکار سرویس و ساخت خودکار cluster در PostgreSQL را می‌بندد و نسخهٔ نصب‌شده را می‌سنجد. `--apply` علاوه بر این به root، Ubuntu 24.04 روی VMware، bundle متعلق به root و غیرقابل‌نوشتن برای دیگران، نشان مجوز و change ID نیاز دارد. حالت check فقط bundle را بررسی می‌کند. هیچ lock واقعی package، کلید امضا، bundle مخزن یا شاهد اجرای موفق روی سرور تمیز در این مخزن وجود ندارد.

این پرونده‌ها مانع را پنهان نمی‌کنند: کد برنامه، مهاجرت و اسکریپت‌های لایهٔ بسته‌ها ساخته شده‌اند؛ اما بستهٔ عمومی و تأییدشدهٔ برنامه برای اجرای آفلاین، نصب‌کنندهٔ کامل تولید، reverse proxy، رابط مرورگر و بستهٔ آزمودهٔ پشتیبان‌گیری و بازیابی وجود ندارد. سرویس‌های سخت‌سازی‌شده و انتشارهای تغییرناپذیر هوش مصنوعی اکنون نصب شده‌اند و صلاحیت‌سنجی کنترل‌شده و بازگشت برنامه موفق بوده است؛ بااین‌حال تأیید مجوز وابستگی‌ها، بقیهٔ ماتریس خطا، بازگشت محیط اجرا و مدل، آزمون صریح قطع WAN و راه‌اندازی مجدد ماشین، بازیابی مستقل و هدف کارایی تولیدی باقی مانده‌اند. تنظیم خصوصی برنامه، اتصال و Zabbix، ایجاد PostgreSQL و Zabbix تولیدی و پذیرش کامل سرورها نیز باز است. هنوز هیچ پایگاه تولید، وضعیت Zabbix، شنوندهٔ عمومی محصول، گواهی، توکن مقصد، نسخهٔ پشتیبان یا بازیابی ایجاد نشده است.

### context ماندگار عامل

سه skill مخصوص مخزن در `.agents/skills` اکنون کار عمومی پروژه، عملیات سرور و مستندات دوزبانه را مسیردهی می‌کنند. [فهرست context Markdown](MARKDOWN_CONTEXT_INDEX.md) هر ۹۳ فایل Markdown متعلق به پروژه را ثبت و نوع کار را به منبع مرتبط وصل می‌کند، بدون اینکه همهٔ مستندات هم‌زمان وارد context شوند. اعتبارسنج مستندات پوشه‌های وابستگی و build را حذف می‌کند و نبود یا قدیمی بودن ورودی فهرست را شکست می‌دهد؛ سه آزمون متمرکز نیز discovery و تطبیق فهرست را پوشش می‌دهند. این زیرساخت context توسعه است، نه قابلیت برنامه یا استقرار.

### گام‌ها و وضعیت شواهد

معماری و ADRهای مرحلهٔ صفر پذیرفته شده‌اند و چهار مهمان جایگزین از صلاحیت‌سنجی عبور کرده‌اند. برش کنترل‌شدهٔ 1A اکنون با برنامه، PostgreSQL، TLS و پنل دوزبانه فعال است؛ 1B مدل محلی پذیرفته‌شده را فراهم می‌کند؛ پیش‌نیاز Zabbix و مسیر فقط‌خواندنی 1C نیز فعال و آزموده شده‌اند. مسیر 1D پاسخ فارسی و انگلیسی اکنون شاهد محدود، اجرای ماندگار و ممیزی پیوندخورده دارد و به‌صورت زنده آزموده شده است. راه‌اندازی مجدد ماشین، قطع صریح WAN، سناریوهای خطا و لغو، بار پایدار، بازیابی مستقل و پذیرش کامل 1E همچنان باز هستند.

ممکن است مالک مستقل ماشین ساخته باشد؛ پیش از ادعای وجود یا نبود آن، وضعیت واقعی بررسی شود. تصویر تنظیمات VM به معنای قبولی مسیر برنامه نیست. ادامه از نخستین گام ناتمامِ دارای شاهد و مجوز باشد، نه پاک کردن پیشرفت.

### دامنهٔ انتشار و کار بعدی

این وضعیت پذیرش مرحلهٔ صفر، برش مستقرشدهٔ 1A، هوش مصنوعی صلاحیت‌سنجی‌شدهٔ 1B، اتصال زنده و فقط‌خواندنی 1C و مسیر ماندگار و مستند به شاهد 1D را ثبت می‌کند. نیازهای منبع، پرامپت بایگانی‌شده، نمودارها و پرونده‌های تحویل حفظ شده‌اند. این رکورد به‌معنای ممیزی امنیت میزبان، پذیرش تولیدی یا اثبات بازیابی مستقل نیست.

برش‌های منبع با Python 3.12.10، uv 0.12.17، Pydantic 2.13.5، FastAPI 0.141.1، SQLAlchemy 2.0.54، Alembic 1.20.0، Psycopg 3.3.6، Ruff 0.16.8، mypy 1.20.2 و pytest 9.1.1 آزموده شدند. Ruff، بررسی سخت‌گیرانهٔ mypy روی ۵۷ فایل، ۹۵ آزمون غیر‌یکپارچه و هر شش آزمون روی پایگاه موقت و جداگانهٔ PostgreSQL 16.15 موفق بودند. پایگاه، login role، credential و تونل SSH موقت پس از آزمون حذف شدند. شاهد CI به revision خودش وابسته می‌ماند. اعتبارسنجی مستندات و پرونده‌ها، بررسی وابستگی و مجوز، آزمون گسترده‌تر امنیت و خطا و شاهد بازیابی همچنان دروازه‌اند. بازبینی دیداری ورود دوزبانه و آزمون سراسری زنده انجام شد؛ پذیرش کامل مرورگر، قطع WAN، راه‌اندازی مجدد ماشین، پشتیبان مستقل و بازیابی جدا هنوز اجرا نشده است.

نقطهٔ بعد در [کار بعدی](NEXT_TASK.md) سخت‌سازی همین مسیر سالم است، نه نصب دوبارهٔ آن: میزبان‌های مصوب بعدی افزوده شوند؛ دادهٔ قدیمی یا ناقص، قطع مقصد و لغو توکن آزموده شود؛ سپس پذیرش قطع WAN، راه‌اندازی مجدد ماشین، بازگشت و بازیابی مستقل انجام گیرد. ارتقا به تولید به نتیجهٔ این آزمون‌ها، تصمیم نگهداری و پشتیبان، سنجش پایدار منابع و تأیید عملیات وابسته است.
