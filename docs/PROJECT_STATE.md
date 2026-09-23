# Project state / وضعیت پروژه

Updated: 2026-09-23 — the controlled user-testing path is live. The fresh-browser WAN-denied case,
application/runtime/model rollback, live cancellation and dependency recovery, missing/corrupt
artifact handling, isolated low-space staging case, five-minute bounded load and socket-only logical
restores of both PostgreSQL 16 databases passed under change
`stage1-completion-20260922-01`. App release `nextops-0.1.0-13a3369` and connector release
`nextops-0.1.0-3d7d725` remain active; all four guests ended `running`, with zero failed units and no
reboot requirement. The [paired Stage 1 report](en/STAGE_1_COMPLETION_REPORT.md) contains measured
results. Production acceptance remains blocked by the lack of a verified off-datastore backup
destination, WAL/PITR recovery and disaster-recovery sign-off.

Phase 2 has now started with a bounded source increment. The repository implements authenticated
incident-context reads for the configured Zabbix host: the accepted current summary plus limited
numeric history and trigger events, preserving source timestamps and explicit partial markers.
Focused repository tests pass. This increment is not deployed or live-accepted, does not yet enter
the durable model/browser workflow, and does not include direct Linux diagnostics. The open Phase 1
recovery blocker remains unchanged.

## English

### Current controlled user-testing checkpoint

Phase 2A is implemented only in the repository at this checkpoint. Its contract fixes the target and
bounded lookback at deployment, permits only named read operations, and enforces four-metric,
eight-point-per-metric and 25-event response ceilings. Live Zabbix role expansion, deployment,
offline/reboot/rollback qualification and direct Linux collection remain not run.

The authenticated application and bilingual panel are deployed as immutable release
`nextops-0.1.0-13a3369` on the app guest behind private TLS and Nginx. PostgreSQL 16 stores
application identity and session state on
its dedicated verified mount. Bootstrap and recovery endpoints, API documentation and the direct
application listener are not exposed through Nginx. The browser receives neither the AI service
credential nor the Zabbix token.

The dedicated Zabbix guest now runs Zabbix 7.0.30, PostgreSQL 16, Nginx/PHP-FPM and Agent 2. The
default administrator password was rotated. A separate API-only reader has no frontend access, an
allowlist limited to `host.get`, `item.get` and `problem.get`, read permission for one approved host
group and a token stored only on the connector guest. It now sees exactly four approved hosts: the
Zabbix guest plus app, AI and connector. An unlisted read and a mutation were both denied. The
connector uses verified TLS, bypasses inherited proxies, exposes only a named summary operation on
loopback and has no generic URL, JSON-RPC, shell or write surface.

The app, AI and connector guests run the exact cached Agent 2 package
`1:7.0.30-1+ubuntu24.04`. Each has a distinct PSK and sends active checks to the source-restricted
Zabbix trapper path. They expose no passive port 10050 and explicitly deny `system.run[*]`. Final
reader validation observed 65, 65 and 58 fresh supported items respectively; these counts are a
point-in-time observation, not a fixed template contract. No repository refresh or unrelated
package upgrade ran. All four hosts retained a `running` system state and zero failed units.

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

Stage 1E failure qualification promoted connector release `nextops-0.1.0-3d7d725` and app release
`nextops-0.1.0-13a3369`. `MonitoringSummary` now exposes `is_partial` and typed reasons; the current
eight-metric live view reports `metrics_truncated` while retaining separate per-measurement stale
flags. The prompt boundary treats host, metric, value, unit and problem text as untrusted data even
when the API source is authenticated. Isolated cases passed for stale values, partial/no-usable
metrics, over-limit malformed text and embedded prompt instructions.

A temporary token owned by the existing reader identity saw the same four approved hosts, was
denied immediately after revocation and was deleted without changing the live token. During a
brief Zabbix HTTPS/API frontend outage, monitoring summary and investigation returned safe,
retryable `503` responses labeled `connector.summary_unavailable`; the failed run and its audit
event were durably stored while general model-only Q&A still succeeded. The frontend restarted,
fresh monitoring recovered and a later live investigation persisted the partial marker and
independently verified evidence hash in 67.9 seconds. Stopping the Zabbix engine alone did not make
the PHP API unreachable, an important operational distinction. Ruff, strict mypy, 102
non-integration tests and six isolated PostgreSQL tests pass.

This is a controlled user-testing slice, not production acceptance. The four approved Phase 1
guests are now monitored; the wider estate is not. Explicit WAN disconnection passed for the
server/API path, including fresh bilingual model-only answers and new evidence-linked live
investigations. After correcting Zabbix's database shutdown ordering and the application's database
startup ordering, all four guests passed serial clean reboots under the early WAN-deny policy and
returned to `running` with zero failed units. A fresh Microsoft Edge context subsequently passed
with a deny proxy allowing only the private application origin. Cancellation, provider loss,
missing/corrupt artifacts, an isolated `ENOSPC` staging case, sustained load and logical isolated
restores also passed. Certificate-expiry, independent off-datastore backup, WAL/PITR recovery and
disaster-recovery promotion remain open. Private addresses, tokens, passwords, host keys and raw
evidence remain outside Git.

### Requirements and preserved history

The directly verified Git remote is `Omid-NextAI/nextops`, branch `main`. Earlier records name `AmirMo10/nextops`; current README/install clone commands now use the verified remote, while historical statements remain preserved and the active prompt header still needs a separately versioned repository-identity correction. The owner requested English and native-Persian documentation, a single English active prompt, local CPU-only AI, continued operation after Internet loss, a first useful Zabbix status answer, phased VM allocations, storage limits and a dedicated Zabbix server recommendation. All eleven integrations and the 51 original specification sections remain in scope.

The active [master prompt v3.0](requirements/NEXTOPS_MASTER_PROMPT.md) and [v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) remain unchanged in this update. The new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md) explicitly supersedes only the old small-lab recommendation and combined budgets; non-conflicting security, acceptance and feature requirements remain mandatory. The archive still contains the original Persian specification.

The first deliverable is a new Persian/English question about authorized Zabbix status, answered by local CPU generation from actual evidence, with source times, scope and audit while Internet is blocked. Linux enrichment follows in Phase 2. Documentation publication does not complete a software phase or establish deployment approval.

The paired [Phase 0 report](en/PHASE_0_REPORT.md) and [Persian report](fa/PHASE_0_REPORT.md) record repository evidence, the accepted four-VM architecture, trust boundaries, module and data contracts, CPU benchmark plan, resource gate, connector roadmap, test plan, blockers and the Stage 1A increments. The repository-grounded [threat model](requirements/nextops-threat-model.md) records TM-001–TM-010. On 2026-09-21 the owner accepted Phase 0 and ADRs 0001–0006, confirming one organization initially, small initial scale with future growth, and the dedicated Zabbix path. Every infrastructure authorization remains separate and pending.

Stage 1A Increments 1 and 2 are implemented in repository source. The code has strict contracts and denial policy, FastAPI, Argon2id identity bootstrap/login/recovery, hashed sessions, PostgreSQL/Alembic state, durable runs, worker leases, append-restricted audit and a bilingual panel. Actor organization, environment, roles and scopes derive from server-side session state. Four guarded scripts define the authenticated offline Ubuntu package layer; they are not a complete product installer. A separately built immutable application release, private TLS listener and connector are live in the controlled environment, while a complete reproducible production bundle remains absent. The pinned AI runtime/model and source service profile are recorded below.

Stage 1B Increment 3 adds a strict runtime-neutral `LLMProvider` contract, authenticated inference API, loopback-only llama.cpp adapter, one-active/two-queued scheduler, bounded input/output/timeouts, cancellation cleanup, safe readiness, and structured overload/dependency failures. A schema-validated YAML manifest pins llama.cpp `v0.4.1` and the official `Qwen3-8B-Q4_K_M.gguf`. The pinned runtime and model are installed with the corrected API release on the qualified AI guest. Controlled live quality, process restart, application/runtime/model rollback, cancellation and dependency recovery, artifact failure, sustained bounded load, explicit WAN disconnection and a clean VM reboot are evidenced. Independent disaster backup and PITR remain production gates.

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

On 2026-09-21, authorized read-only SSH preflight reached all four clean replacement guests after the owner supplied their new Ed25519 fingerprints independently and each matched the live handshake. Key-only authentication, strict host-key checking and direct-root denial were verified. The configured vCPU, memory, virtual-disk and dedicated-mount layouts match the public role budgets. All guests run Ubuntu 24.04.5 LTS under VMware. On 2026-09-22 the fleet was rechecked after the AI deployment and a narrow GLib security update on app: every guest reported `running` systemd state, zero failed units, zero pending package upgrades and no reboot requirement. UFW is active on app, connector and Zabbix but inactive on AI; that drift remains a separate hardening item. The AI endpoints remain loopback-only; the later monitoring change added one Zabbix trapper listener on the private service interface with three source-specific firewall rules. The three monitored NextOps guests added no listener, and no public product listener exists.

After explicit owner authorization for connected preparation, each host used its existing strict proxy chain to refresh signed repositories and install only its role package layer. No broad OS upgrade ran. Exact observed direct versions are PostgreSQL 16.15 and Nginx 1.24 on app; GCC 13.3, CMake 3.28, Ninja 1.11 and OpenBLAS 0.3.26 on AI; Python 3.12 venv support on connectors; and Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24 and PHP 8.3.6 on Zabbix. The official Zabbix 7.0 Ubuntu 24.04 release bootstrap package was pinned by SHA-256 before repository import. Package post-install starts were blocked and, at that preparation checkpoint, all product/database/web services were inactive and disabled, no PostgreSQL cluster existed, and no listener was added. Since then, the application/database/proxy, AI, connector and Zabbix slices have been deliberately configured and activated for controlled testing, followed by the bounded Agent 2 host-coverage change recorded above. Docker was not installed because the selected native systemd design does not need it and a container socket would enlarge the trust boundary.

Protected non-login service identities and role directories now exist. The pinned llama.cpp commit was built on the qualified AI guest with Release, CPU-native, OpenMP and OpenBLAS settings and no GPU linkage; its promoted binary hash is in the inference manifest. The pinned 5,027,783,488-byte Qwen model matched its expected SHA-256 before and after protected-volume promotion. The active immutable API release is `nextops-0.1.0-62de8d6`; `417d888` remains the tested inference-application rollback. A cold process restart restored both services in 109 seconds. The 2026-09-23 campaign additionally verified protected runtime/model rollback copies, client-cancellation cleanup, dependency recovery, fail-closed missing/corrupt model handling and a five-minute two-client load: 98 of 99 requests succeeded, p95 total latency was 6.114 seconds, peak measured service memory was 4,885,475,328 bytes, and the scheduler never exceeded one active/one queued request. Both services remain enabled, unprivileged, CPU-only and limited to `127.0.0.1:8080` and `127.0.0.1:8090`; `systemd-analyze security` reports `2.7 OK` for each. Raw evidence, credentials, addresses and host keys remain outside Git. Dependency-license approval, an independent backup destination, WAL/PITR and production sign-off remain open.

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

These records expose rather than hide the deployment blockers. The controlled application,
PostgreSQL, private reverse proxy/UI, AI, connector, Zabbix state and four-host monitoring coverage
exist. Fresh-browser isolation, artifact rollback, the remaining scoped failure cases, sustained
bounded load and logical restores of both databases now have live evidence. A reproducible complete
production installer, independently stored pgBackRest/WAL repository, restic artifact repository,
PITR drill and disaster-recovery bundle do not. Private configuration, certificates and target
credentials remain only in protected deployment locations; complete production acceptance remains
open.

### Durable agent context

Six repository-scoped Codex skills under `.agents/skills` route project context, server operations, bilingual documentation, bounded change planning, acceptance review and documentation-drift review. [MARKDOWN_CONTEXT_INDEX](MARKDOWN_CONTEXT_INDEX.md) catalogs project-owned Markdown files and maps task types to the relevant sources without loading the entire documentation set into every context window. The documentation validator excludes dependency/build trees and fails on a missing or stale catalog entry; three focused tests cover discovery and catalog reconciliation. These skills are development aids, not application capability, authorization or infrastructure security boundaries.

### Milestones and actual evidence status

| Stage | Required result | Evidence status for this update |
|---|---|---|
| 0 | Architecture/gap/threat report and appropriate approvals | Owner accepted architecture/roadmap and ADRs on 2026-09-21; the clean replacement guests passed read-only qualification, while ESXi/storage refresh and operation-specific authorization remain separate |
| 1A | Local identity, policy, database, durable work and audit | Authenticated app, PostgreSQL migration, private TLS panel and session path are live for controlled testing; durable live-investigation and audit linkage now uses the existing scoped run model |
| 1B | New local CPU answers and offline model cold load | The pinned runtime/model and corrected API release are installed behind hardened loopback-only units; authentication, bilingual quality, five-minute bounded load, cold process restart, clean VM reboot, application/runtime/model rollback, cancellation/dependency/artifact recovery and four-guest WAN isolation passed. Independent disaster backup, PITR and production sign-off remain open |
| Zabbix prerequisite | Dedicated database mount, monitoring, frontend/API and scoped reader before 1C | Zabbix 7.0.30, PostgreSQL, TLS frontend/API and the scoped reader are active; the server plus app, AI and connector are monitored by PSK-authenticated active Agent 2 paths, and the API allowlist/host-scope denials pass |
| 1C | Real bounded read-only evidence with correct counts | Controlled live connector qualification passed with eight fresh measurements, explicit timestamps/staleness and zero active problems; the reader sees all four approved Phase 1 hosts with fresh items, while the full failure matrix remains |
| 1D | New evidence-linked Zabbix answer with audit | English/Persian grounded answers pass; every started live investigation now has a durable scoped run, bounded evidence snapshot/hash, model result, safe failure outcome and append-only audit linkage verified in isolated PostgreSQL and the live path |
| 1E | Offline fresh login/restart, security/failure/capacity tests | Fresh login, bilingual general Q&A, live evidence and audit passed while all four guests were WAN-blocked. A separately WAN-denied fresh browser, revocation, cancellation, dependency/artifact/low-space recovery and five-minute capacity profile pass. After correcting database-cluster ordering, all four guests passed the serial clean-reboot matrix. Production backup/PITR acceptance remains open |

The user may perform provisioning independently; verify their actual state before claiming a VM either exists or does not exist. A screenshot of VM settings is not proof of an accepted application workflow. Resume from the next evidenced, authorized incomplete stage rather than resetting progress.

### Scope of this publication and next action

This state records Phase 0 acceptance, the deployed controlled Stage 1A application slice, the qualified Stage 1B AI slice, the live Stage 1C read-only connector and the durable evidence-linked Stage 1D user-test path. It preserves the source requirements, archived prompt, diagrams and per-server handoff. It is not a host vulnerability audit, production acceptance, independent recovery proof or complete provisioning record.

The source slices use Python 3.12.10, uv 0.12.17, Pydantic 2.13.5, FastAPI 0.141.1, SQLAlchemy 2.0.54, Alembic 1.20.0, Psycopg 3.3.6, Ruff 0.16.8, mypy 1.20.2 and pytest 9.1.1 with a generated `uv.lock`; Playwright 1.63 is now a locked development-only browser dependency. The CI workflow defines digest-pinned PostgreSQL 16.15 and 17.6 jobs. Fresh browser automation, live rollback/failure recovery, five-minute load and temporary PostgreSQL 16.15 restores ran in the controlled environment. The temporary restore clusters and staging copies were removed. Dependency/license approval, independent backup/PITR and production promotion remain separate gates.

The next engineering checkpoint in [NEXT_TASK](NEXT_TASK.md) is the controlled Phase 2A deployment:
grant exactly two additional read methods, verify the bounded live contract, rollback and offline
behavior, then connect accepted context to the durable investigation path. In parallel, production
promotion remains blocked on an approved off-datastore recovery destination, PostgreSQL-aware
repositories/WAL archiving, permitted artifact backup, independent PITR, recorded RPO/RTO and key
recovery, and operational sign-off.

## فارسی

مرحلهٔ دو با یک گام محدود در کد منبع آغاز شده است. مخزن اکنون برای میزبان پیکربندی‌شدهٔ Zabbix،
خواندن احرازهویت‌شدهٔ «بافت رخداد» را پیاده می‌کند: خلاصهٔ جاریِ پذیرفته‌شده به‌همراه تاریخچهٔ
عددی و رویدادهای trigger با سقف ثابت، زمان منبع و نشان صریحِ نتیجهٔ ناقص. آزمون‌های متمرکز مخزن
موفق‌اند؛ اما این گام هنوز مستقر یا به‌صورت زنده پذیرفته نشده، وارد گردش ماندگار مدل و مرورگر نشده
و عیب‌یابی مستقیم Linux را در بر ندارد. مانع بازیابیِ باقی‌مانده از مرحلهٔ یک نیز بدون تغییر باز است.

### جمع‌بندی کنترل‌شدهٔ مرحلهٔ ۱ در ۱۴۰۵/۰۷/۰۱

در کارزار `stage1-completion-20260922-01`، مرورگر تازه با WAN مسدود، بازگشت برنامه و فایل‌های
محیط اجرا/مدل، لغو درخواست و بازیابی ظرفیت، قطع وابستگی، مدل مفقود یا خراب، کمبود فضای ایزولهٔ
آماده‌سازی، بار پایدار پنج‌دقیقه‌ای و بازیابی منطقی و فقط‌سوکتی هر دو پایگاه PostgreSQL 16 با موفقیت
انجام شدند. ۹۸ درخواست از ۹۹ درخواست بار موفق بود، p95 برابر ۶٫۱۱۴ ثانیه ثبت شد و زمان‌بند از یک
درخواست فعال و یک درخواست در صف فراتر نرفت. هر چهار مهمان در پایان `running`، بدون واحد خراب و
بدون نیاز به راه‌اندازی مجدد بودند. جزئیات در
[گزارش تکمیل مرحلهٔ ۱](fa/STAGE_1_COMPLETION_REPORT.md) آمده است.

این نتیجه به‌معنای پذیرش تولید نیست. dumpهای منطقی دارای checksum بازیابی شدند، اما مقصدی که
استقلال آن از مهمان سرویس‌دهنده، DS-C/G10 و میزبان فیزیکی اثبات شده باشد وجود ندارد؛ بایگانی WAL،
PITR، مخزن فایل با restic و تأیید نهایی بازیابی بحران نیز باقی مانده‌اند. بخش‌های قدیمی‌تر این سند
سوابق مرحله‌ای هستند و این جمع‌بندی و مانیفست وضعیت انتشار بر ادعاهای آمادگی پیشین مقدم‌اند.

### نقطهٔ فعلی برای ارزیابی کنترل‌شدهٔ کاربران

گام 2A در این نقطه فقط در مخزن پیاده شده است. قرارداد آن مقصد و بازهٔ محدود را در استقرار ثابت
می‌کند، فقط خواندن‌های نام‌دار را می‌پذیرد و خروجی را به چهار سنجه، هشت نقطه برای هر سنجه و ۲۵
رویداد محدود می‌سازد. گسترش نقش زندهٔ Zabbix، استقرار، آزمون آفلاین و راه‌اندازی مجدد و بازگشت، و
گردآوری مستقیم Linux هنوز اجرا نشده‌اند.

برنامهٔ احرازهویت‌شده و پنل دوزبانه، در انتشار تغییرناپذیر `nextops-0.1.0-13a3369` روی مهمان برنامه و پشت TLS خصوصی
و Nginx فعال‌اند. PostgreSQL 16 هویت و نشست برنامه را روی فضای ذخیره‌سازی مستقل و تأییدشده نگه
می‌دارد. مسیرهای راه‌اندازی اولیه و بازیابی، مستندات API و درگاه مستقیم برنامه از Nginx در دسترس
نیستند. هیچ‌یک از اعتبارنامه‌های سرویس هوش مصنوعی یا Zabbix به مرورگر تحویل نمی‌شود.

مهمان مستقل پایش اکنون Zabbix 7.0.30، PostgreSQL 16، Nginx/PHP-FPM و Agent 2 را اجرا می‌کند.
گذرواژهٔ مدیر پیش‌فرض عوض شده است. خوانشگر جداگانهٔ API به رابط کاربری دسترسی ندارد؛ فقط سه روش
`host.get`، `item.get` و `problem.get` برایش مجاز است و تنها یک گروه میزبان مصوب را می‌بیند. اکنون
دقیقاً چهار میزبان مصوب، یعنی Zabbix، برنامه، هوش مصنوعی و اتصال، در دامنهٔ دید آن هستند. یک روش
خواندن خارج از فهرست و یک روش نوشتنی هر دو رد شدند. توکن فقط روی مهمان اتصال نگه‌داری می‌شود.
اتصال نیز فقط از TLS معتبر استفاده می‌کند، پراکسی موروثی را کنار می‌گذارد و روی رابط محلی صرفاً یک
عملیات نام‌دار برای خلاصهٔ پایش ارائه می‌دهد؛ نشانی دلخواه، JSON-RPC عمومی، shell یا عملیات نوشتنی
در اختیار مصرف‌کننده نیست.

روی مهمان‌های برنامه، هوش مصنوعی و اتصال، بستهٔ دقیق Agent 2 با نسخهٔ
`1:7.0.30-1+ubuntu24.04` نصب است. هر مهمان PSK مستقل دارد و فقط بررسی فعال را به مسیر محدودشدهٔ
Zabbix می‌فرستد. هیچ‌کدام روی درگاه ۱۰۰۵۰ گوش نمی‌دهند و `system.run[*]` صریحاً بسته است. در بررسی
نهایی خوانشگر، تعداد نقطه‌ای سنجه‌های تازه و پشتیبانی‌شده به‌ترتیب ۶۵، ۶۵ و ۵۸ بود؛ این اعداد
مشاهدهٔ همان لحظه‌اند، نه قرارداد ثابت template. مخزن بسته تازه نشد و ارتقای نامرتبطی انجام نشد.
وضعیت هر چهار میزبان `running` و شمار واحد خراب صفر باقی ماند.

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

در صلاحیت‌سنجی خطای مرحلهٔ 1E، انتشار `nextops-0.1.0-3d7d725` برای اتصال‌دهنده و
`nextops-0.1.0-13a3369` برای برنامه فعال شد. `MonitoringSummary` اکنون با `is_partial` و دلیل‌های
دارای نوع، ناقص‌بودن شاهد را اعلام می‌کند. نمای زندهٔ هشت‌سنجه‌ای فعلی دلیل `metrics_truncated`
دارد و در عین حال قدیمی‌بودن هر اندازه‌گیری را جداگانه نگه می‌دارد. در مرز پرامپت نیز نام میزبان،
سنجه، مقدار، واحد و مسئله، حتی با منبع احرازهویت‌شده، فقط دادهٔ غیرقابل‌اعتمادند. آزمون‌های جداشده
برای مقدار قدیمی، شاهد ناقص یا بدون سنجهٔ قابل‌استفاده، متن بیش‌ازحد بلند و دستور جاسازی‌شده موفق
بودند.

یک توکن موقت متعلق به همان هویت خوانشگر، فقط چهار میزبان مصوب را دید؛ بلافاصله پس از لغو از
دسترسی افتاد و حذف شد، بی‌آنکه توکن فعال تغییر کند. هنگام قطع کوتاه رابط HTTPS و API زبیکس، خلاصه
و بررسی زنده خطای امن و قابل‌تکرار `503` با کلید `connector.summary_unavailable` برگرداندند. اجرای
ناموفق و رویداد ممیزی آن ماندگار شد و هم‌زمان پاسخ‌گویی عمومی و بدون شاهد مدل محلی ادامه یافت.
پس از بازگشت رابط، دریافت دادهٔ تازه برقرار شد و بررسی زندهٔ بعدی، نشان ناقص‌بودن و هش مستقلِ
تأییدشدهٔ شاهد را طی ۶۷٫۹ ثانیه حفظ کرد. توقف موتور Zabbix به‌تنهایی API مبتنی بر PHP را قطع نکرد؛
این تفاوت برای عملیات مهم است. Ruff، mypy سخت‌گیرانه، ۱۰۲ آزمون غیر‌یکپارچه و شش آزمون PostgreSQL
در پایگاه جداگانه موفق‌اند.

این خروجی برای ارزیابی کنترل‌شده است، نه پذیرش تولید. هر چهار مهمان مصوب مرحلهٔ یک پایش می‌شوند،
اما دامنهٔ گسترده‌تر تجهیزات هنوز وارد نشده است. آزمون صریح قطع WAN در مسیر سرور و API موفق بود:
هنگامی که دسترسی مستقیم IPv4 و IPv6 هر چهار مهمان به اینترنت بسته بود، ورود تازه، پاسخ عمومی فارسی
و انگلیسی، آمادگی مدل محلی، دریافت شاهد تازه و پیوند ثبت و ممیزی برقرار ماند. پس از اصلاح ترتیب
خاموش‌شدن پایگاه Zabbix و ترتیب آغاز پایگاه برنامه، هر چهار مهمان یکی‌یکی و زیر سیاست قطع زودهنگام
WAN راه‌اندازی مجدد شدند، با وضعیت `running` و صفر واحد خراب بازگشتند و آزمون سلامت نقش خود را
گذراندند. جداسازی مستقل مرورگر، انقضای گواهی، پایان مهلت یا لغو درخواست، کمبود فضا، بار پایدار،
پشتیبان مستقل، بازیابی و سناریوی بحران همچنان بازند. نشانی‌ها، توکن‌ها، گذرواژه‌ها، کلیدهای میزبان و
شواهد خام بیرون Git مانده‌اند.

### نیازها و سابقهٔ محفوظ

remote بررسی‌شدهٔ مستقیم Git برابر `Omid-NextAI/nextops` و شاخه `main` است. فرمان‌های clone جاری در README و راهنمای نصب اکنون remote درست را دارند؛ رکوردهای تاریخی `AmirMo10/nextops` حفظ می‌شوند و عنوان پرامپت فعال هنوز به اصلاح جداگانه و نسخه‌دار نیاز دارد. مالک مستندات فارسی طبیعی و انگلیسی، یک پرامپت فعال انگلیسی، AI محلی روی CPU، ادامهٔ کار پس از قطع اینترنت، پاسخ وضعیت Zabbix در اولین تحویل، برنامهٔ ماشین‌ها و محدودیت ذخیره‌سازی و سرور مستقل Zabbix را خواسته است. یازده اتصال و ۵۱ بخش مشخصات اولیه در دامنه باقی‌اند.

[پرامپت فعال ۳.۰](requirements/NEXTOPS_MASTER_PROMPT.md) و [بایگانی نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) در این تغییر دست‌نخورده‌اند. [اصلاحیهٔ استقرار](requirements/DEPLOYMENT_UPDATE.md) فقط پیشنهاد آزمایشگاه کوچک و مجموع منابع وابسته را صریح جایگزین می‌کند؛ سایر نیازهای امنیت، پذیرش و قابلیت‌ها پابرجا هستند. مشخصات فارسی اولیه همچنان در بایگانی محفوظ است.

اولین خروجی، پاسخ تازهٔ فارسی یا انگلیسی دربارهٔ وضعیت مجاز Zabbix، تولیدشده روی CPU محلی و مستند به دادهٔ واقعی، همراه منبع و زمان و دامنه و ممیزی با اینترنت قطع است. بررسی مستقیم Linux در مرحلهٔ دو می‌آید. انتشار مستندات، پایان مرحلهٔ نرم‌افزاری یا اثبات مجوز استقرار نیست.

[گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md) و [مدل تهدید](requirements/nextops-threat-model.md) یافتهٔ مخزن، معماری چهارماشینی پذیرفته‌شده، مرز اعتماد، قرارداد ماژول و داده، برنامهٔ سنجش CPU، بودجه، نقشهٔ اتصال، آزمون و گام‌های 1A را ثبت می‌کنند. مالک در ۲۱ سپتامبر ۲۰۲۶ مرحلهٔ صفر و ADRهای 0001 تا 0006 را با تک‌سازمانی بودن فعلی، مقیاس کوچک اولیه با رشد آینده و Zabbix مستقل پذیرفت. همهٔ مجوزهای زیرساخت جدا و در انتظار باقی می‌مانند.

Incrementهای 1 و 2 از 1A در کد مخزن پیاده شده‌اند: قرارداد سخت‌گیر، سیاست رد، FastAPI، هویت Argon2id، نشست hash‌شده، PostgreSQL/Alembic، اجرای ماندگار، lease، ممیزی فقط‌افزودنی و پنل دوزبانه. سازمان، محیط، role و scope از نشست سمت سرور ساخته می‌شوند. چهار اسکریپت محافظت‌شده فقط لایهٔ بستهٔ Ubuntu را تعریف می‌کنند و installer کامل محصول نیستند. انتشار تغییرناپذیر برنامه، TLS خصوصی و اتصال‌دهنده در محیط کنترل‌شده جداگانه فعال‌اند؛ بستهٔ کامل و بازتولیدپذیر تولید هنوز وجود ندارد. محیط اجرا و مدل ثابت هوش مصنوعی در ادامه ثبت شده‌اند.

Increment 3 از 1B قرارداد مستقل و سخت‌گیر `LLMProvider`، API احرازهویت‌شده، رابط فقط‌محلی llama.cpp، صف با یک درخواست فعال و دو درخواست در انتظار، کران ورودی و خروجی و زمان، پاک‌سازی لغو و خطاهای ساخت‌یافته را فراهم می‌کند. پروندهٔ YAML معتبرشده، llama.cpp نسخهٔ `v0.4.1` و فایل رسمی `Qwen3-8B-Q4_K_M.gguf` را تثبیت می‌کند. کیفیت زنده، راه‌اندازی مجدد، بازگشت برنامه/محیط اجرا/مدل، لغو و قطع وابستگی، artifact خراب یا مفقود، بار محدود پنج‌دقیقه‌ای، قطع WAN و مرورگر تازه شاهد دارند. پشتیبان مستقل و PITR همچنان دروازهٔ تولیدند.

برش بومی 1B دو واحد جدا و سخت‌سازی‌شدهٔ `nextops-llama` و `nextops-ai`، دو اعتبارنامهٔ فایل‌محور، محدودیت شبکه به رابط محلی در سطح cgroup، درخت انتشار فقط‌خواندنی، سقف صریح منابع، بارگذاری سخت‌گیرانهٔ اعتبارنامه و مجموعهٔ نسخه‌دار سنجش فارسی و انگلیسی را فراهم می‌کند و اکنون روی مهمان هوش مصنوعی فعال است. نخستین اجرا، مسیر نادرست کتابخانه‌های مشترک پس از جابه‌جایی و ناکافی بودن بررسی صرفِ باز شدن درگاه را آشکار کرد؛ واحد اصلاح‌شده از مسیر ثابت و محافظت‌شدهٔ کتابخانه‌ها استفاده می‌کند و شروع کنترل‌شده تا سلامت احرازهویت‌شدهٔ مدل منتظر می‌ماند. حساب استقرار بنا بر دستور مالک اکنون مدیریت کامل و بدون گذرواژه دارد؛ ورود مستقیم root از راه SSH همچنان بسته است.

### شواهد ارسالی سخت‌افزار و دیسک

[رکورد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خروجی ESXCLI مالک را حفظ می‌کند: ESXi 8.0.3 با ساخت 24414501، چهار بستهٔ پردازنده، ۱۱۲ هسته، ۲۲۴ رشته، Hyperthreading فعال، چهار گرهٔ NUMA و حافظهٔ ۱٬۴۴۲٬۷۴۳٬۶۳۱٬۸۷۲ بایت، تقریباً ۱۳۴۳٫۶۶ GiB. نمونهٔ ناقص CPU 0 و 1، سرعت و cache و microcode ارسالی و نگاشت‌های مرجع در [یادداشت ESXi](fa/ESXI_BASELINE.md) ثبت‌اند. مدل تجاری دقیق، فرکانس اسمی، یکسان بودن همهٔ بسته‌ها، ISA مهمان و توزیع واقعی گره‌ها از نمونه ثابت نمی‌شوند. میانگین حسابی، توپولوژی یا ظرفیت آزاد مشاهده‌شده نیست.

ظرفیت لحظه‌ای VMFS ارسالی: DS-A برابر ۱۴۹٫۷۵ GiB کل و ۱۴۸٫۳۴ آزاد؛ DS-B برابر ۱۱۱۷٫۵۰ و ۱۱۰۹٫۸۷؛ DS-C برابر ۳۵۷۶٫۷۵ و 3166.8701171875. نام واقعی، UUID و مسیر در رکورد عمومی نیستند. [برنامهٔ دیسک](STORAGE_PLAN.md) حجم‌های سیستم و راه‌اندازی را کنار می‌گذارد، DS-A و DS-B را تخصیص نمی‌دهد و سقف سه‌ترابایتی را حفظ می‌کند. هدف پیشنهادی فضای آزاد DS-C برابر ۲۵ درصد، دقیقاً 894.1875 GiB و با گردکردن حدود ۹۰۰ GiB است. فهرست ارسالی، رزرو، سلامت RAID یا سنجش I/O نیست.

ESXi حفظ شود؛ Ubuntu Server 24.04 LTS خط مبنای تأییدشدهٔ مهمان است، نه جایگزین میزبان. مجموع‌ها و نسخه و فهرست دوباره به‌عنوان دادهٔ غایب خواسته نشوند. CPU/RAM آزاد فعلی، بار و رزرو، جای‌گذاری فیزیکی NUMA، سازگاری و محدودیت مجوز، سلامت و تأخیر دیسک، رشد و محل swap باید هنگام اجرا بررسی شوند. اتصال مستقیم به میزبان ESXi یا تأیید سازگاری انجام نشده است.

### صلاحیت‌سنجی پاک‌سازی‌شدهٔ مهمان‌های جایگزین

در ۲۱ سپتامبر ۲۰۲۶، پس از ارسال مستقل اثرانگشت‌های تازهٔ Ed25519 توسط مالک و برابری هرکدام با ارتباط زنده، پیش‌بررسی فقط‌خواندنی مجاز از راه SSH به هر چهار مهمان جایگزین رسید. احراز هویت فقط با کلید، کنترل سخت‌گیرانهٔ کلید میزبان و رد ورود مستقیم root تأیید شد و منابع هر نقش با بودجهٔ عمومی برابر بود. در ۲۲ سپتامبر، پس از استقرار هوش مصنوعی و یک به‌روزرسانی محدود امنیتی GLib روی مهمان برنامه، همهٔ مهمان‌ها دوباره بررسی شدند: وضعیت systemd در هر چهار مورد `running`، شمار واحد خراب و بستهٔ قابل‌ارتقا صفر و راه‌اندازی مجدد لازم نبود. UFW روی مهمان‌های برنامه، اتصال و Zabbix فعال و روی مهمان هوش مصنوعی غیرفعال است؛ اصلاح این ناهمگونی یک کار سخت‌سازی جداگانه است. درگاه‌های هوش مصنوعی همچنان فقط روی رابط محلی‌اند. تغییر بعدی پایش، یک شنوندهٔ دریافت داده را روی رابط خصوصی Zabbix با سه قاعدهٔ دیوارهٔ آتشِ مختص مبدأ افزود؛ سه مهمان NextOps هیچ شنونده‌ای اضافه نکردند و شنوندهٔ عمومی محصول وجود ندارد.

پس از مجوز صریح مالک برای آماده‌سازی متصل، هر میزبان از زنجیرهٔ پراکسی سخت‌گیرانهٔ موجود برای تازه‌سازی مخزن‌های امضاشده و نصب فقط لایهٔ بستهٔ نقش خود استفاده کرد. ارتقای کلی سیستم‌عامل اجرا نشد. نسخه‌های مستقیم مشاهده‌شده عبارت‌اند از PostgreSQL 16.15 و Nginx 1.24 در برنامه؛ GCC 13.3، CMake 3.28، Ninja 1.11 و OpenBLAS 0.3.26 در هوش مصنوعی؛ پشتیبانی محیط مجازی Python 3.12 در connectors؛ و Zabbix 7.0.30، PostgreSQL 16.15، Nginx 1.24 و PHP 8.3.6 در Zabbix. بستهٔ راه‌انداز رسمی Zabbix 7.0 برای Ubuntu 24.04 پیش از افزودن مخزن با SHA-256 ثابت شد. شروع خودکار پس از نصب مسدود بود و در همان نقطهٔ آماده‌سازی، همهٔ سرویس‌های محصول، پایگاه و وب غیرفعال بودند، خوشهٔ PostgreSQL ساخته نشده بود و درگاه تازه‌ای باز نشد. پس از آن، برش‌های برنامه و پایگاه و پراکسی، هوش مصنوعی، اتصال و Zabbix به‌صورت کنترل‌شده تنظیم و فعال شدند و سپس تغییر محدود پوشش چهارمیزبانی Agent 2 اجرا شد. Docker نصب نشد، چون طراحی بومی systemd به آن نیاز ندارد و سوکت کانتینر مرز اعتماد را بزرگ می‌کند.

هویت‌های بدون ورود و مسیرهای محافظت‌شدهٔ نقش ساخته شده‌اند. llama.cpp با Release، اجرای بومی CPU، OpenMP و OpenBLAS و بدون GPU ساخته شد و مدل ۵٬۰۲۷٬۷۸۳٬۴۸۸ بایتی با SHA-256 مصوب برابر است. انتشار فعال API، `nextops-0.1.0-62de8d6` است و `417d888` به‌عنوان بازگشت آزموده‌شدهٔ لایهٔ API باقی مانده است. توقف و شروع سرد، بازگشت برنامه و artifact، لغو، قطع وابستگی، مدل خراب/مفقود و تولید پس از بازیابی موفق بودند. در بار پنج‌دقیقه‌ای، ۹۸ درخواست از ۹۹ درخواست موفق، p95 برابر ۶٫۱۱۴ ثانیه و بیشینهٔ زمان‌بند یک فعال/یک صف بود. هر دو سرویس فقط روی CPU و `127.0.0.1:8080` و `127.0.0.1:8090` اجرا می‌شوند و امتیاز systemd آن‌ها `2.7 OK` است. شواهد خام و رازها بیرون Git مانده‌اند. مجوز وابستگی‌ها، پشتیبان مستقل، WAL/PITR و تأیید تولید بازند.

### چیدمان فعلیِ پیشنهادی

برنامهٔ NextOps همان ۸ vCPU و ۳۲ GiB و ۲۰۰ GiB؛ AI همان ۲۴ و ۱۲۸ و ۵۰۰؛ اتصال همان ۴ و ۸ و ۸۰ است. **سرور مستقل `zabbix-server` با ۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB پیش از اتصال زندهٔ 1C** اضافه می‌شود. پایگاه NextOps از مرحلهٔ سه با ۸ و ۶۴ و ۳۰۰ پیشنهاد می‌شود؛ اجرای تغییر فقط در مرحلهٔ هفت و با مجوز، ۴ و ۱۶ و ۸۰ است.

سرور Zabbix پایگاه پایش، رابط و API خودش را دارد، نه مدل یا پایگاه NextOps. در مسیر جدید، جایگزین آزمایشگاه ۴ vCPU و ۸ GiB و ۱۰۰ GiB می‌شود؛ هر دو ساخته نشوند. Zabbix محلی موجودِ مناسب و مجاز ابتدا بررسی و استفاده شود. تعداد ماشین‌های خود NextOps همچنان ۳، ۴ و ۵ و مجموع شامل پایش ۴، ۵ و ۶ است.

چیدمان اولیه **۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** دارد؛ با سهم موقت ESXi swap برابر ۱۸۴ GiB، جمع پیش از سربار **۱۱۶۴ GiB** است. چیدمان‌های بعدی به‌ترتیب ۴۸ و ۲۴۸ و ۱۲۸۰، با جمع ۱۵۲۸ GiB؛ و ۵۲ و ۲۶۴ و ۱۳۶۰، با جمع ۱۶۲۴ GiB هستند. با مصرف قبلی ثابت، فضای آزاد فرضی DS-C برابر ۲۰۰۲٫۸۷، ۱۶۳۸٫۸۷ و ۱۵۴۲٫۸۷ GiB می‌شود. این‌ها بودجه‌های جایگزین‌اند، نه جمع‌شونده، رزرو، سنجش یا مجوز مصرف همهٔ فضا. رشد، VMX، snapshot، ورود فایل و بازیابی جدا و ماشین موجود بدون دوباره‌شماری حساب شوند.

راهنمای [فارسی](fa/ZABBIX_SERVER.md) و [انگلیسی](en/ZABBIX_SERVER.md) نرم‌افزار پیشنهادی Zabbix 7.0 LTS، PostgreSQL 16، Nginx، PHP-FPM و Agent 2، چیدمان کامل `vg_zabbix`، پیشنهاد history هفت‌روزه و trends عددی نودروزه، هویت API محدود، خودپایشی، پذیرش آفلاین و خطر تک‌میزبان را ثبت می‌کنند. بستهٔ دقیق، تنظیم نگهداری و VM/LVM از طریق این مستندات نصب یا آزموده نشده‌اند. اعداد پیشنهادی در [رکورد Zabbix](requirements/ZABBIX_SERVER_PLAN.json) جدا از شاهد سخت‌افزار آمده‌اند.

### پروندهٔ هر سرور برای مسئول استقرار

[مشخصات پرونده](requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md)، [JSON Schema مشترک](../deploy/server-dependencies/server-dependency.schema.json) و چهار فایل YAML خوانا برای `nextops-app`، `nextops-ai`، `nextops-connectors-ro` و `zabbix-server` اکنون تحویل ماشین‌خوان هر سرور را فراهم می‌کنند. راهنمای [فارسی](fa/DEPLOYMENT_DOSSIERS.md) و [انگلیسی](en/DEPLOYMENT_DOSSIERS.md) روش تکمیل ورودی خصوصی بدون commit آن را شرح می‌دهند.

هر پرونده وضعیت مجوز، منبع، منابع VM، هویت سرویس، قفل نرم‌افزار و artifact، مسیر تنظیمات، secret reference، مرز شبکه و storage، ترتیب سرویس، فرمان فقط‌خواندنی یا الگوی محافظت‌شده، فرمان مسدود، مشاهده‌پذیری، backup و rollback، ورودی لازم، دروازهٔ پذیرش و محدودیت را دارد. مقدارهای معلوم با مجموع ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB سازگارند و mountهای Zabbix با طرح ۲۰۰ GiB تطبیق دارند. تبدیل درخواستی JSON به YAML همهٔ مقدارها را بدون اتلاف حفظ کرد. اعتبارسنج مخزن چهار فایل YAML را ایمن parse می‌کند، schema نسخهٔ ۱.۰.۰ و شناسه‌های پذیرفته‌شده را می‌سنجد، باقی‌ماندن نسخهٔ قدیمی JSON را رد می‌کند و مجموع منابع را تطبیق می‌دهد.

برای هر role یک script اجرایی در `deploy/installers` وجود دارد. موتور مشترک و آزموده، manifest همهٔ فایل‌های bundle را با SHA-256 جداگانه تطبیق می‌دهد، نسخهٔ دقیق همهٔ packageها و وابستگی‌ها را لازم می‌داند، APT را فقط به repository محلی امضاشده محدود می‌کند، نصب یا حذف پیش‌بینی‌نشده را رد می‌کند، شروع خودکار سرویس و ساخت خودکار cluster در PostgreSQL را می‌بندد و نسخهٔ نصب‌شده را می‌سنجد. `--apply` علاوه بر این به root، Ubuntu 24.04 روی VMware، bundle متعلق به root و غیرقابل‌نوشتن برای دیگران، نشان مجوز و change ID نیاز دارد. حالت check فقط bundle را بررسی می‌کند. هیچ lock واقعی package، کلید امضا، bundle مخزن یا شاهد اجرای موفق روی سرور تمیز در این مخزن وجود ندارد.

این پرونده‌ها مانع را پنهان نمی‌کنند. برنامهٔ کنترل‌شده، PostgreSQL، پراکسی خصوصی، هوش مصنوعی،
اتصال، Zabbix و پایش چهار میزبان وجود دارند. مرورگر تازه، بازگشت artifact، خطاهای باقی‌مانده، بار
محدود و بازیابی منطقی هر دو پایگاه نیز شاهد زنده دارند. نصب‌کنندهٔ کامل تولید، مخزن مستقل
pgBackRest/WAL، مخزن restic، آزمون PITR و بستهٔ بازیابی بحران هنوز آماده نیستند. تنظیم خصوصی،
گواهی و اعتبارنامهٔ مقصد در محل محافظت‌شده باقی می‌مانند و پذیرش تولید تکمیل نشده است.

### context ماندگار عامل

شش skill مخصوص مخزن در `.agents/skills`، context پروژه، عملیات سرور، مستندات دوزبانه، برنامه‌ریزی تغییر محدود، بازبینی پذیرش و بررسی انحراف مستندات را مسیردهی می‌کنند. [فهرست context Markdown](MARKDOWN_CONTEXT_INDEX.md) فایل‌های Markdown متعلق به پروژه را ثبت و نوع کار را به منبع مرتبط وصل می‌کند، بدون اینکه همهٔ مستندات هم‌زمان وارد context شوند. اعتبارسنج مستندات پوشه‌های وابستگی و build را حذف می‌کند و نبود یا قدیمی بودن ورودی فهرست را شکست می‌دهد؛ سه آزمون متمرکز نیز discovery و تطبیق فهرست را پوشش می‌دهند. این skillها ابزار توسعه‌اند، نه قابلیت برنامه، مرز مجوز یا مرز امنیت زیرساخت.

### گام‌ها و وضعیت شواهد

معماری و ADRهای مرحلهٔ صفر پذیرفته شده‌اند و چهار مهمان جایگزین از صلاحیت‌سنجی عبور کرده‌اند. برش کنترل‌شدهٔ 1A با برنامه، PostgreSQL، TLS و پنل دوزبانه فعال است؛ 1B مدل محلی را فراهم می‌کند؛ مسیر فقط‌خواندنی 1C فعال و آزموده است؛ و 1D شاهد محدود، اجرای ماندگار و ممیزی پیوندخورده دارد. گام 1E اکنون مرورگر تازه با WAN مسدود، بازگشت، لغو و قطع وابستگی، artifact مفقود/خراب، کمبود فضای ایزوله، بار پنج‌دقیقه‌ای و بازیابی منطقی جدا را نیز گذرانده است. پشتیبان مستقل، WAL/PITR و پذیرش تولید بازند.

ممکن است مالک مستقل ماشین ساخته باشد؛ پیش از ادعای وجود یا نبود آن، وضعیت واقعی بررسی شود. تصویر تنظیمات VM به معنای قبولی مسیر برنامه نیست. ادامه از نخستین گام ناتمامِ دارای شاهد و مجوز باشد، نه پاک کردن پیشرفت.

### دامنهٔ انتشار و کار بعدی

این وضعیت پذیرش مرحلهٔ صفر، برش مستقرشدهٔ 1A، هوش مصنوعی صلاحیت‌سنجی‌شدهٔ 1B، اتصال زنده و فقط‌خواندنی 1C و مسیر ماندگار و مستند به شاهد 1D را ثبت می‌کند. نیازهای منبع، پرامپت بایگانی‌شده، نمودارها و پرونده‌های تحویل حفظ شده‌اند. این رکورد به‌معنای ممیزی امنیت میزبان، پذیرش تولیدی یا اثبات بازیابی مستقل نیست.

برش‌های منبع با Python 3.12.10، uv 0.12.17 و زنجیرهٔ قفل‌شده آزموده شدند؛ Playwright 1.63 نیز وابستگی صرفاً توسعه‌ای است. Ruff، mypy سخت‌گیرانه و ۱۱۱ آزمون غیر‌یکپارچه موفق‌اند. مرورگر تازه، بازگشت و بازیابی خطا، بار پنج‌دقیقه‌ای و خوشه‌های موقت PostgreSQL 16.15 در محیط کنترل‌شده اجرا شدند و خوشه‌ها و نسخه‌های موقت پاک شدند. بررسی وابستگی و مجوز، پشتیبان مستقل/PITR و ارتقا به تولید همچنان دروازه‌اند.

نقطهٔ مهندسی بعدی در [کار بعدی](NEXT_TASK.md)، استقرار کنترل‌شدهٔ گام 2A است: افزودن دقیق دو
روش خواندن، بررسی زندهٔ قرارداد محدود و بازگشت و رفتار آفلاین، و سپس پیوند با مسیر ماندگار بررسی.
هم‌زمان، ارتقا به تولید تا تصویب مقصد پشتیبان مستقل، مخزن و WAL آگاه از PostgreSQL، پشتیبان
فایل مجاز، PITR مستقل، ثبت RPO/RTO و بازیابی کلید و تأیید عملیات متوقف می‌ماند.
