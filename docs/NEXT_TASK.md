# Next task / کار بعدی

New source-only UI and relevance candidate, 2026-09-26 — Verify the focused file/filesystem
behavior and simplified bilingual chat-style workspace against held-out real user questions. Check
ambiguous mixed-topic questions, file-content refusal, approved mount capacity, partial evidence,
provenance, audit, keyboard/mobile/RTL and true offline operation on the exact candidate release.
Local checks passed (182 tests, 10 skips, lint, types, JavaScript syntax, paired-doc links/status).
The code is not deployed; obtain the controlled change authorization and record rollback/live
qualification before promotion. Do not describe deterministic focused summaries as newly trained
model output. The independent recovery destination/lab and remaining production gates below remain
open.

New owner-reported answer-quality priority, 2026-09-26 — Capture the exact user question, selected
mode/target/language and visible answer without secrets. Reproduce and classify the mismatch as
wrong mode, missing/partial evidence, model irrelevance, prompt echo, or output truncation. The
source-only `codex/answer-completion-guard` candidate now rejects length-limited completions and
question echoes and clarifies fallback/UI wording; it is **not deployed**. Before any promotion,
run held-out English/Persian semantic cases on the exact local CPU runtime/model, verify the
question-specific answer against the source/time/scope evidence, rerun API/browser tests and record
latency/quality and rollback evidence. Do not infer that fine-tuning is needed or train on raw
operational evidence. The independent recovery destination and isolated restore lab remain the
first outstanding production gate; all other production blockers below remain open.

Latest checkpoint, 2026-09-26 — All three application-layer releases are now
`nextops-0.1.0-cdde129`. Credentialed HTTP redirects fail closed; hosted CI and fresh WAN-denied
browser checks passed. All four guests require key-only, non-root SSH; the AI guest's firewall is
now active. Preserve these controls. The owner confirmed that none of the required independent
recovery/restore resources, license decision, local notification route and recipients, replacement
certificate pairs, or named approvers are presently available. Do not mark any corresponding
production gate passed or deploy a substitute on the serving guests. The first unfinished
checkpoint remains the independent recovery destination and isolated restore lab; once provided,
follow the private owner record and [blocker runbook](en/PRODUCTION_BLOCKERS_RUNBOOK.md).
Separately, current host shells can reach public IPv4 because prior WAN denial was a temporary
acceptance test. The connector now has a tested process-level allowlist for its approved LAN; a
permanent **host-wide** egress policy still needs a reviewed local DNS/time/proxy allowlist and
guarded verification. Do not treat the historical test as a deployed host firewall rule.
Zabbix Agent 2 is now `7.0.31` on all four guests. The three offline-installed agents require an
explicit verified package import for each future patch; an empty apt-upgrade list is not proof
that their upstream agent is current.

Updated: 2026-09-26 — The owner resumed the production-hardening and recovery objective. All work
that can be completed safely on the existing four serving guests is current: serial package
maintenance is rollback-protected and complete, Zabbix is `7.0.31`, all guests are `running` with
zero failed units, zero pending packages and no reboot marker, and the fresh WAN-denied bilingual
browser gate passes through server-side logout. At that package-maintenance checkpoint the active
application, inference and connector releases had not yet changed.

Do not manufacture the remaining production evidence on the serving guests. The first unfinished
checkpoint is still an approved recovery destination outside the guest, datastore and hypervisor
failure domains plus an isolated restore lab. When those real resources and the private owner record
are available, install the pinned offline pgBackRest/restic bundles, execute full/differential/WAL,
PITR, file, negative, key-recovery and cold-start drills, and record measured RPO/RTO. Until then,
the recovery profile must remain `BLOCKED` and production acceptance must remain `not_run`.

The answer-integrity priority is complete for controlled user testing. At that earlier checkpoint,
application release `nextops-0.1.0-2397581` and inference API release `nextops-0.1.0-fd3c353`
were active. Hosted CI,
the final eight-case local English/Persian corpus, engineering semantic review, live authenticated
general/monitoring/incident API checks, immediate test-session revocation and a fresh serial reboot
passed. Preserve the deterministic guard and do not turn this bounded evidence into a claim that
model-only answers are always true.

The next external inputs are concrete: provision the independent recovery/restore targets; select a
real LAN-local non-SMTP operator-delivery channel and name primary/backup recipients; hand over
replacement CA-issued application and Zabbix certificate pairs with custodians and rollback window;
choose and approve the NextOps project license; establish the offline release-signing trust root;
name legal, security and production approvers; and complete their sign-off. Syft SBOM and
production dependency-audit evidence now exist privately, but the operating-system/runtime scan,
offline signature verification and human license/security review are not complete.

Historical checkpoint: 2026-09-23 — Phase 2 implementation and controlled qualification were complete. Application release
`nextops-0.1.0-eb57241` and connector release `nextops-0.1.0-e2dad3a` were active. Four fixed targets then
provide bounded Zabbix history/events plus direct, redacted and forced-command Linux evidence to a
durable bilingual investigation workflow. Live English/Persian API investigations, authorization,
all four collectors, restart, rollback, server/API WAN denial, authenticated WAN-denied browser,
dependency loss/recovery and serial VM reboot checks passed; source CI is green.
Do not rebuild or repeat this accepted implementation.

The repository-side recovery qualification contract is now implemented: ADR 0008, a strict public
schema/profile, focused tests and CI select separate pgBackRest paths for the two PostgreSQL 16
clusters and restic only for approved non-database files. The profile reports `BLOCKED`, and its
production-only check fails intentionally. The immediate external prerequisite is an approved
destination outside the serving guest, datastore and hypervisor failure domains. Only then may the
offline bundles, separate backup/WAL paths, permitted artifact backup, isolated PITR/restore,
measured RPO/RTO and disaster-recovery sign-off be executed. Do not describe local dumps or a
same-datastore copy as an independent backup.

The paired [production blocker runbook](en/PRODUCTION_BLOCKERS_RUNBOOK.md) now gives the owner the
exact private decision template, recovery-host access procedure, safe capacity/preflight commands,
notification and certificate handoff, supply-chain approvals, stop conditions and sanitized
checklist required to unblock the remaining work. It performs no infrastructure change and closes
no acceptance gate by itself.

The first post-Phase-2 security increment is also accepted in the controlled deployment. Commit
`eb57241` passed all five hosted CI jobs; immutable app release `nextops-0.1.0-eb57241` then passed
normal-TLS browser and direct API logout, former-token `401`, other-session preservation,
idempotent replay and exactly one sanitized correlated audit event. This does not bypass the
independent-recovery prerequisite for production.

The certificate-expiry detection increment is accepted in the controlled deployment. Commit
`f540a9d` passed all five hosted CI jobs, and change `certificate-lifecycle-20260923-01` installed
the no-network least-privilege checker and persistent timer on both TLS frontends. Both live
certificates are healthy under the 90-day policy; isolated expiring and malformed fixtures failed
as designed; both private keys remained root-only and unreadable to the checker. Four Zabbix active
items and six tagged triggers observe checker result, timer state and missing data. A guarded timer
outage produced the expected local problem and recovery returned it to healthy. Complete an
approved operator notification route and an observed offline rotation/rollback drill before
promoting the certificate lifecycle gate beyond partial.

## English — harden the live user-testing slice

### Authoritative current checkpoint

The next operator must treat the following as completed and preserve it:

- the app release, PostgreSQL migration, private TLS reverse proxy and authenticated bilingual panel;
- the pinned CPU-only AI runtime/model and authenticated application-to-AI tunnel;
- Zabbix 7.0.30 with its PostgreSQL database, TLS frontend/API, Agent 2 and self-monitoring;
- an API-only Zabbix reader restricted to five named read methods and one approved host group;
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
- quality gates: Ruff, strict mypy, 137 passing local non-integration tests plus one POSIX-only
  collector test, PostgreSQL 16 and 17 CI integration jobs, real-browser fixture acceptance and
  secret scanning.

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
6. **Repository safeguard completed; external prerequisite remains:** ADR 0008, the recovery
   schema/profile, eight focused tests and CI now enforce separate pgBackRest repositories, restic
   database exclusions and fail-closed production qualification. Approve a recovery destination
   independent of the serving guest, DS-C/G10 and host; define RPO/RTO, retention and key custody;
   then verify offline bundles and execute the independent backup, PITR and restore drills.
7. **Completed:** Phase 2 implementation and controlled qualification. Immutable app/connector
   release, exact `history.get`/`event.get` role expansion, four forced-command Linux targets,
   composite durable investigation, bilingual local-model answers, provenance/limits/partial
   behavior, service restart, release rollback, guarded server/API WAN denial, fresh authenticated
   browser workflow, dependency loss/recovery and the Phase 2 serial VM reboot passed. All mutation
   remains disabled.

The detailed material below preserves design rationale and earlier checkpoints. Where it describes
the app, PostgreSQL, Zabbix, connector or browser as not deployed, this authoritative checkpoint and
[PROJECT_STATE](PROJECT_STATE.md) supersede that older statement.

Read the [active master prompt](requirements/NEXTOPS_MASTER_PROMPT.md) with the new [deployment amendment](requirements/DEPLOYMENT_UPDATE.md), [Zabbix guide](en/ZABBIX_SERVER.md), [per-server deployer guide](en/DEPLOYMENT_DOSSIERS.md), [allocation record](requirements/ZABBIX_SERVER_PLAN.json), [START_HERE](en/START_HERE.md), [PROJECT_STATE](PROJECT_STATE.md), [ROADMAP](en/ROADMAP.md), [SERVER_PLAN](en/SERVER_PLAN.md), [STORAGE_PLAN](STORAGE_PLAN.md), [OFFLINE_RUNTIME](en/OFFLINE_RUNTIME.md), [ESXI_BASELINE](en/ESXI_BASELINE.md) and [hardware evidence](requirements/HARDWARE_BASELINE.json). Original detail remains in the [unchanged v2 archive](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md); all 51 sections and eleven integrations remain in scope.

The new amendment supersedes the old small `zabbix-lab` fallback and combined totals in active-prompt v3.0 section 18 and older guide examples. It does not change the three initial NextOps core VMs or authorize provisioning. Inspect actual Git state, work already done and approval/test evidence before resuming; do not overwrite work or restart completed discovery indefinitely.

### Current checkpoint: controlled AI deployment passed

The owner accepted the paired [Phase 0 report](en/PHASE_0_REPORT.md), [Persian report](fa/PHASE_0_REPORT.md), ADRs 0001–0006, trust boundaries, and Stage 1A–1E roadmap on 2026-09-21. Stage 1A Increments 1–2 provide the locked Python project, typed boundaries and denial policy, local identity, PostgreSQL state, durable runs/leases, append-restricted audit, authenticated API, and bilingual fixture result. Stage 1B Increment 3 provides the `LLMProvider` boundary, authenticated loopback adapter and one-active/two-queued scheduler. After the latest evidence-preservation and relocation fixes, formatting, Ruff, strict mypy over 46 files, and 80 non-integration tests pass; five database tests are skipped locally and retain their earlier real-PostgreSQL host evidence.

A sanitized read-only preflight reached all four clean replacement guests after their independently supplied Ed25519 fingerprints matched live handshakes. All four run Ubuntu 24.04.5 LTS under VMware with the intended public resource/mount budgets. On 2026-09-22, after the AI work and a narrow GLib security update on app, every guest reported `running`, zero failed units, zero pending packages and no reboot requirement. Direct root SSH remains disabled. The deployment account has the full passwordless administrative access explicitly requested by the owner; its private key and strict host-key pins are therefore security-critical and remain outside Git.

The role package layers remain as recorded: PostgreSQL 16.15 and Nginx 1.24 on app; GCC 13.3, CMake 3.28, Ninja 1.11 and OpenBLAS 0.3.26 on AI; Python 3.12 venv support on connectors; and Zabbix 7.0.30, PostgreSQL 16.15, Nginx 1.24 and PHP 8.3.6 on Zabbix. The controlled application/database/proxy, AI, connector and Zabbix/database/frontend slices are active and passed the named reboot checks. Docker was not installed because the native systemd design does not need it and a container socket would enlarge the trust boundary.

The pinned llama.cpp runtime and 5,027,783,488-byte Qwen model match their approved SHA-256 values and are promoted through stable links to immutable protected directories. At this earlier checkpoint, the inference API was `nextops-0.1.0-fd3c353`, the user application `nextops-0.1.0-2397581` and the connector `nextops-0.1.0-e2dad3a`. The two AI-guest services use the protected runtime path, wait for authenticated model health, run unprivileged on `127.0.0.1:8080` and `127.0.0.1:8090`, and each has a `2.7 OK` systemd security exposure result. Distinct root-owned credentials remain outside Git and logs. The [release manifest](status/current-release.yaml) is the machine-readable current summary.

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
- close certificate rotation/rollback, operator notification delivery and final operational sign-off.

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

After each increment, update PROJECT_STATE with actual work, exact versions/results, failed/skipped/not-run cases, remaining blockers and the next checkpoint. The controlled application, AI, connector and four-host Zabbix path is live for user testing. It is not production-accepted: independent backup/PITR, certificate rotation and operator notification, dependency/license approval and complete disaster recovery remain open.

## فارسی — سخت‌سازی مسیر زندهٔ ارزیابی کاربران

### نقطهٔ فعلی و ملاک ادامه

آخرین نقطه، ۴ مهر ۱۴۰۵ — هر سه انتشار لایهٔ برنامه اکنون `nextops-0.1.0-cdde129` هستند.
تغییرمسیر HTTP دارای اطلاعات احراز هویت به‌صورت ایمن رد می‌شود؛ CI و مرورگر تازه با WAN مسدود
موفق بودند. چهار مهمان SSH را فقط با کلید و بدون ورود مستقیم root می‌پذیرند و دیوارهٔ آتش AI
فعال شده است. این کنترل‌ها حفظ شوند. مالک اعلام کرد مقصد و آزمایشگاه مستقل بازیابی، تصمیم مجوز،
مسیر اعلان داخلی و گیرندگان، جفت گواهی جایگزین و تأییدکنندگان نام‌دار هنوز موجود نیستند. هیچ
دروازهٔ تولیدیِ وابسته به این موارد نباید پذیرفته اعلام شود یا به‌جای بازیابی مستقل، نسخه‌ای روی
مهمان سرویس‌دهنده ساخته شود. نخستین گام ناتمام همچنان فراهم‌کردن مقصد مستقل و محیط restore
ایزوله طبق [راهنمای موانع](fa/PRODUCTION_BLOCKERS_RUNBOOK.md) است.
افزون بر آن، پوستهٔ مدیریتی مهمان‌ها اکنون به IPv4 عمومی دسترسی دارد؛ آزمون قبلی منع WAN موقت
بود. اتصال‌دهنده اکنون در سطح فرایند فقط به شبکهٔ داخلی مجاز دسترسی دارد؛ سیاست دائمی خروجی
**کل میزبان** همچنان به فهرست بازبینی‌شدهٔ DNS، زمان و پراکسی محلی و راستی‌آزمایی همراه بازگشت
نیاز دارد. آزمون تاریخی نباید قاعدهٔ نصب‌شدهٔ کل میزبان فرض شود.
Agent 2 زبیکس اکنون روی هر چهار مهمان `7.0.31` است. سه عامل نصب‌شده از بستهٔ آفلاین، برای هر
وصلهٔ بعدی به ورود صریح و تأییدشدهٔ بسته نیاز دارند؛ خالی بودن فهرست ارتقای apt به معنی به‌روز
بودن نسخهٔ بالادستی آن‌ها نیست.

به‌روزرسانی ۴ مهر ۱۴۰۵ — مالک هدف سخت‌سازی تولید و بازیابی را دوباره فعال کرد. همهٔ کارهایی که روی
چهار مهمان سرویس‌دهندهٔ موجود با ایمنی قابل انجام بود، جاری است: نگه‌داری بسته‌ها به‌صورت ترتیبی و
با امکان بازگشت تکمیل شد، Zabbix به `7.0.31` رسید، هر چهار مهمان `running` هستند و واحد خراب، بستهٔ
در انتظار یا نشانگر reboot ندارند. آزمون مرورگر تازه و دوزبانه با WAN مسدود تا لغو نشست در سرور
موفق است. در آن نقطهٔ نگه‌داری بسته‌ها، انتشار برنامه، استنتاج و اتصال‌دهنده هنوز تغییر نکرده بود.

شاهد تولید با اجرای نمایشی روی مهمان‌های سرویس‌دهنده ساخته نشود. نخستین گام ناتمام همچنان مقصد
بازیابی خارج از دامنهٔ خرابی مهمان، datastore و hypervisor همراه آزمایشگاه restore ایزوله است.
پس از فراهم‌شدن این منابع واقعی و تکمیل رکورد خصوصی مالک، بسته‌های آفلاین و ثابت pgBackRest و
restic نصب و تمرین‌های full، differential، WAL، PITR، فایل، حالت منفی، بازیابی کلید و cold-start
اجرا شوند و RPO/RTO اندازه‌گیری‌شده ثبت شود. تا آن زمان پروفایل بازیابی باید `BLOCKED` و پذیرش
تولید `not_run` بماند.

اولویت صحت پاسخ برای ارزیابی کنترل‌شده تکمیل شد. در آن نقطهٔ پیشین، انتشار برنامه
`nextops-0.1.0-2397581` و انتشار API هوش مصنوعی `nextops-0.1.0-fd3c353` فعال بودند. CI میزبانی‌شده، مجموعهٔ نهایی هشت‌موردی فارسی
و انگلیسی، بازبینی معنایی مهندسی، آزمون زنده و احرازهویت‌شدهٔ API در حالت عمومی، پایش و رخداد، لغو
فوری نشست آزمایشی و reboot ترتیبی تازه موفق بودند. این کنترل قطعی باید حفظ شود، اما شاهد محدود آن
نباید به ادعای «درستی همیشگی پاسخ بدون شاهد» تبدیل شود.

ورودی‌های بیرونی بعدی روشن‌اند: مقصد مستقل بازیابی و محیط restore ساخته شود؛ مسیر واقعی و داخلی
غیر SMTP برای تحویل اعلان انتخاب و گیرندگان اصلی و جایگزین نام‌گذاری شوند؛ جفت گواهی تازهٔ برنامه
و Zabbix از CA همراه متولیان کلید و بازهٔ بازگشت تحویل شود؛ مجوز پروژهٔ NextOps انتخاب و تصویب
شود؛ ریشهٔ اعتماد آفلاین امضای انتشار شکل بگیرد؛ و مسئولان حقوقی، امنیتی و پذیرش تولید تعیین و
تأییدشان ثبت شود. شاهد خصوصی SBOM با Syft و ممیزی وابستگی تولید اکنون موجود است، اما پویش کامل
سیستم‌عامل و محیط اجرا، راستی‌آزمایی آفلاین امضا و بازبینی انسانی مجوز و امنیت تکمیل نشده‌اند.

نقطهٔ تاریخی ۲۳ سپتامبر ۲۰۲۶: پیاده‌سازی و صلاحیت‌سنجی کنترل‌شدهٔ مرحلهٔ دو تکمیل شده بود؛ انتشار برنامه `nextops-0.1.0-eb57241` و انتشار اتصال‌دهنده
`nextops-0.1.0-e2dad3a` فعال بودند. چهار مقصد ثابت در آن زمان تاریخچه و رویداد محدود Zabbix را همراه شواهد مستقیم،
پالایش‌شده و مبتنی بر فرمان اجباری Linux به گردش ماندگار بررسی دوزبانه می‌رسانند. بررسی زندهٔ API
به فارسی و انگلیسی، مجوزدهی، هر چهار گردآورنده، راه‌اندازی مجدد، بازگشت انتشار، مسیر سرور/API با
WAN مسدود، مرورگر احرازهویت‌شده، قطع و بازیابی وابستگی و reboot ترتیبی VMها موفق بوده و CI سبز
است. این پیاده‌سازی پذیرفته‌شده نباید از نو ساخته شود.

قرارداد صلاحیت‌سنجی سمت مخزن اکنون پیاده شده است: ADR 0008، schema و پروفایل سخت‌گیر عمومی،
آزمون‌های متمرکز و CI برای دو خوشهٔ PostgreSQL 16 مسیرهای جداگانهٔ pgBackRest را الزام می‌کنند و
restic را فقط برای فایل‌های غیرپایگاهی مصوب می‌پذیرند. پروفایل `BLOCKED` گزارش می‌دهد و کنترل ویژهٔ
تولید عمداً شکست می‌خورد. پیش‌نیاز بیرونی فوری، تصویب مقصدی خارج از دامنهٔ خرابی مهمان، datastore
و hypervisor سرویس‌دهنده است. پس از آن بسته‌های آفلاین، مسیرهای جداگانهٔ پشتیبان و WAL، پشتیبان
artifact مجاز، PITR و restore ایزوله، RPO/RTO اندازه‌گیری‌شده و تأیید بازیابی بحران اجرا می‌شوند.
dump محلی یا نسخه‌ای روی همان datastore نباید پشتیبان مستقل نامیده شود.

[راهنمای دوزبانهٔ رفع موانع تولید](fa/PRODUCTION_BLOCKERS_RUNBOOK.md) اکنون قالب دقیق تصمیم خصوصی،
روش دسترسی میزبان بازیابی، فرمان‌های امن ظرفیت و پیش‌بررسی، تحویل اعلان و گواهی، تأییدهای زنجیرهٔ
تأمین، شرط توقف و checklist پالایش‌شدهٔ لازم برای ادامه را در اختیار مالک می‌گذارد. این سند هیچ
تغییر زیرساختی اجرا نمی‌کند و به‌تنهایی هیچ دروازهٔ پذیرشی را نمی‌بندد.

نخستین increment امنیتی پس از مرحلهٔ دو نیز در استقرار کنترل‌شده پذیرفته شد. commit `eb57241` هر
پنج کار CI میزبانی‌شده را گذراند؛ سپس انتشار تغییرناپذیر `nextops-0.1.0-eb57241` در مرورگر دارای
TLS عادی و API مستقیم، خروج، `401` برای توکن قبلی، حفظ نشست دیگر، تکرار idempotent و وجود دقیقاً
یک رویداد ممیزی پالایش‌شده و دارای شناسهٔ هم‌بستگی را ثابت کرد. این کار پیش‌نیاز بازیابی مستقل برای
تولید را کنار نمی‌زند.

increment تشخیص انقضای گواهی در استقرار کنترل‌شده پذیرفته شد. commit `f540a9d` هر پنج کار CI را
گذراند و تغییر `certificate-lifecycle-20260923-01`، checker کم‌اختیار و بدون شبکه و timer ماندگار
را روی هر دو رابط TLS نصب کرد. گواهی‌های زنده با سیاست ۹۰روزه سالم‌اند؛ fixtureهای نزدیک انقضا و
خراب طبق قرارداد شکست خوردند؛ کلیدها فقط برای root ماندند و هویت checker نتوانست آن‌ها را بخواند.
چهار item فعال و شش trigger برچسب‌دار Zabbix، نتیجهٔ checker، وضعیت timer و نبود داده را می‌سنجند.
قطع محافظت‌شدهٔ timer مشکل مورد انتظار را ساخت و بازیابی آن trigger را سالم کرد. پیش از ارتقای
دروازهٔ چرخهٔ گواهی از حالت ناقص، مسیر اعلان مصوب بهره‌بردار و تمرین مشاهده‌شدهٔ چرخش/بازگشت را
تکمیل کنید.

عامل یا بهره‌بردار بعدی باید موارد زیر را تکمیل‌شده بداند و بدون دلیل دوباره نسازد:

- انتشار برنامه، مهاجرت PostgreSQL، reverse proxy با TLS خصوصی و پنل دوزبانهٔ احرازهویت‌شده؛
- محیط اجرا و مدل فقط‌-CPU تثبیت‌شده و تونل احرازهویت‌شدهٔ برنامه به هوش مصنوعی؛
- Zabbix 7.0.30 با پایگاه PostgreSQL، رابط و API مبتنی بر TLS، Agent 2 و خودپایشی؛
- خوانشگر مخصوص API با پنج روش نام‌دار و فقط‌خواندنی و دامنهٔ یک گروه میزبان مصوب؛
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
- عبور Ruff، بررسی سخت‌گیرانهٔ mypy، ۱۳۷ آزمون غیر‌یکپارچهٔ موفق در محیط محلی به‌همراه یک آزمون
  ویژهٔ POSIX، کارهای یکپارچگی PostgreSQL 16 و 17 در CI، fixture واقعی مرورگر و پویش راز.

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
6. **محافظ مخزن تکمیل شد؛ پیش‌نیاز بیرونی باقی است:** ADR 0008، schema و پروفایل بازیابی، هشت
   آزمون متمرکز و CI اکنون جدایی مخزن‌های pgBackRest، منع ورود دادهٔ پایگاه به restic و شکست امن
   ادعای تولید را اعمال می‌کنند. مقصدی مستقل از مهمان سرویس‌دهنده، DS-C/G10 و میزبان تصویب و
   RPO/RTO، نگه‌داری و متولی کلید تعیین شود؛ سپس بسته‌های آفلاین راستی‌آزمایی و پشتیبان، PITR و
   بازیابی مستقل اجرا شوند.
7. **تکمیل شد:** پیاده‌سازی و صلاحیت‌سنجی کنترل‌شدهٔ مرحلهٔ دو. انتشار تغییرناپذیر برنامه و
   اتصال‌دهنده، افزودن دقیق `history.get` و `event.get`، چهار مقصد Linux با فرمان اجباری، بررسی
   ترکیبی و ماندگار، پاسخ دوزبانهٔ مدل محلی، منشأ و سقف و نشان نقص، راه‌اندازی مجدد سرویس، بازگشت
   انتشار، قطع محافظت‌شدهٔ WAN در مسیر سرور/API، گردش کامل و احرازهویت‌شدهٔ مرورگر، reboot ترتیبی
   مرحلهٔ دو و قطع و بازیابی وابستگی موفق بودند. همهٔ عملیات تغییردهنده همچنان غیرفعال‌اند.

مطالب تفصیلی بعدی منطق طراحی و نقاط پیشین را حفظ می‌کند. هرجا برنامه، PostgreSQL، Zabbix، اتصال یا
رابط مرورگر را نصب‌نشده می‌نامد، این بخش و [وضعیت پروژه](PROJECT_STATE.md) جای آن عبارت قدیمی را
می‌گیرند.

[پرامپت فعال](requirements/NEXTOPS_MASTER_PROMPT.md)، [اصلاحیهٔ تازهٔ چیدمان](requirements/DEPLOYMENT_UPDATE.md)، [راهنمای Zabbix](fa/ZABBIX_SERVER.md)، [راهنمای پرونده‌های استقرار](fa/DEPLOYMENT_DOSSIERS.md)، [رکورد تخصیص](requirements/ZABBIX_SERVER_PLAN.json)، [شروع کار](fa/START_HERE.md)، [وضعیت پروژه](PROJECT_STATE.md)، [نقشهٔ راه](fa/ROADMAP.md)، [سرورها](fa/SERVER_PLAN.md)، [ذخیره‌سازی](STORAGE_PLAN.md)، [آفلاین](fa/OFFLINE_RUNTIME.md)، [ESXi](fa/ESXI_BASELINE.md) و [شاهد سخت‌افزار](requirements/HARDWARE_BASELINE.json) خوانده شوند. جزئیات اولیه در [بایگانی ثابت نسخهٔ ۲](requirements/archive/NEXTOPS_MASTER_PROMPT_v2.0.md) باقی است؛ ۵۱ بخش و یازده اتصال حذف نمی‌شوند.

اصلاحیه فقط نمونهٔ آزمایشگاهی کوچک و مجموع منابع وابسته به آن را در بخش ۱۸ پرامپت ۳.۰ و مثال‌های قدیمی جایگزین می‌کند؛ تعداد سه ماشین اولیهٔ خود NextOps و شروط مجوز تغییر نمی‌کنند. پیش از ادامه، Git، کار موجود، تأییدها و نتیجهٔ آزمون بررسی شوند؛ کار بازنویسی یا شناسایی تکمیل‌شده بی‌دلیل تکرار نشود.

### نقطهٔ فعلی: استقرار کنترل‌شدهٔ هوش مصنوعی پذیرفته شد

مالک در ۲۱ سپتامبر ۲۰۲۶ [گزارش مرحلهٔ صفر انگلیسی](en/PHASE_0_REPORT.md)، [نسخهٔ فارسی](fa/PHASE_0_REPORT.md)، ADRهای 0001 تا 0006، مرزهای اعتماد و نقشهٔ 1A تا 1E را پذیرفت. Incrementهای 1 و 2 از 1A پروژهٔ قفل‌شدهٔ پایتون، قرارداد و سیاست رد، هویت محلی، وضعیت PostgreSQL، اجرای ماندگار و lease، ممیزی محدود، API احرازهویت‌شده و نتیجهٔ دوزبانهٔ آزمایشی را دارند. Increment 3 از 1B مرز `LLMProvider`، رابط احرازهویت‌شده و فقط‌محلی و صف با یک درخواست فعال و دو درخواست در انتظار را فراهم می‌کند. پس از آخرین اصلاح حفظ شاهد و جابه‌جایی محیط اجرا، قالب‌بندی، Ruff، بررسی سخت‌گیرانهٔ mypy روی ۴۶ فایل و ۸۰ آزمون غیرپایگاهی موفق بوده‌اند؛ پنج آزمون پایگاه در محیط محلی کنار گذاشته شدند و شاهد پیشین اجرای واقعی PostgreSQL برای revision مربوط خود محفوظ است.

پیش‌بررسی پاک‌سازی‌شده پس از برابری اثرانگشت‌های Ed25519 با ارتباط زنده به هر چهار مهمان جایگزین رسید. همهٔ مهمان‌ها Ubuntu 24.04.5 LTS را زیر VMware و با بودجهٔ عمومی منابع و محل‌های ذخیره‌سازی اجرا می‌کنند. در ۲۲ سپتامبر ۲۰۲۶، پس از کار هوش مصنوعی و به‌روزرسانی محدود امنیتی GLib روی مهمان برنامه، هر چهار سرور وضعیت `running`، صفر واحد خراب، صفر بستهٔ قابل‌ارتقا و بی‌نیازی از راه‌اندازی مجدد را گزارش کردند. ورود مستقیم root از راه SSH بسته مانده است. حساب استقرار بنا بر دستور صریح مالک اکنون مدیریت کامل و بدون گذرواژه دارد؛ ازاین‌رو کلید خصوصی و کنترل سخت‌گیرانهٔ کلیدهای میزبان اهمیت امنیتی ویژه دارند و بیرون Git نگه‌داری می‌شوند.

لایهٔ بسته‌های هر نقش مطابق رکورد باقی است: PostgreSQL 16.15 و Nginx 1.24 روی برنامه؛ GCC 13.3، CMake 3.28، Ninja 1.11 و OpenBLAS 0.3.26 روی هوش مصنوعی؛ پشتیبانی محیط مجازی Python 3.12 روی connectors؛ و Zabbix 7.0.30، PostgreSQL 16.15، Nginx 1.24 و PHP 8.3.6 روی Zabbix. برش‌های کنترل‌شدهٔ برنامه و پایگاه و پراکسی، هوش مصنوعی، اتصال و Zabbix و پایگاه و رابط آن فعال‌اند و آزمون‌های نام‌بردهٔ راه‌اندازی مجدد را گذرانده‌اند. Docker نصب نشد، زیرا طراحی بومی systemd به آن نیاز ندارد و سوکت کانتینر مرز اعتماد را بزرگ می‌کند.

محیط اجرای ثابت llama.cpp و مدل Qwen با اندازهٔ ۵٬۰۲۷٬۷۸۳٬۴۸۸ بایت با SHA-256 مصوب برابرند و از راه پیوندهای پایدار به پوشه‌های تغییرناپذیر و محافظت‌شده رسیده‌اند. در آن نقطهٔ پیشین، انتشار API هوش مصنوعی `nextops-0.1.0-fd3c353`، برنامه `nextops-0.1.0-2397581` و اتصال‌دهنده `nextops-0.1.0-e2dad3a` بود. دو سرویس مهمان هوش مصنوعی کتابخانه‌ها را از مسیر محافظت‌شده می‌خوانند، تا سلامت احرازهویت‌شدهٔ مدل منتظر می‌مانند و با هویت بدون امتیاز فقط روی `127.0.0.1:8080` و `127.0.0.1:8090` فعال‌اند؛ ارزیابی امنیتی systemd برای هرکدام `2.7 OK` است. دو اعتبارنامهٔ جدا و متعلق به root در Git یا گزارش‌ها ظاهر نمی‌شوند. [مانیفست انتشار](status/current-release.yaml) خلاصهٔ ماشین‌خوان وضعیت جاری است.

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
- چرخش/بازگشت گواهی، تحویل اعلان به بهره‌بردار و تأیید نهایی بهره‌برداری.

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

پس از هر گام، کار واقعی، نسخه و نتیجهٔ آزمون، موارد شکست‌خورده یا اجرا‌نشده، مانع و گام بعد در وضعیت پروژه ثبت شوند. مسیر چهارمیزبانی برای ارزیابی کنترل‌شده زنده است، اما پذیرش تولیدی ندارد. مرورگر تازه، پایداری، بازیابی منطقی جدا و تشخیص محلی گواهی شاهد دارند؛ پشتیبان مستقل، WAL/PITR، چرخش/اعلان گواهی و بازیابی کامل بحران همچنان بازند.
