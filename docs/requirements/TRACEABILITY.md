# Original-requirement traceability / ردیابی نیازهای اولیه

Source: [master prompt, original Appendix A](NEXTOPS_MASTER_PROMPT.md). All 51 original sections are retained. Paths below are planned or now-started implementation locations. `P` = planned; `D` = documentation drafted; `A` = owner-accepted documentation gate, not runtime implementation; `I` = a tested implementation slice exists but the full requirement is incomplete. Phase numbers follow the revised roadmap, not the original fourteen-phase order.

Current delivery exception (2026-09-26): the owner deferred independent recovery from the local
delivery work queue and reports daily ESXi snapshots. The backup, restore and disaster-recovery
requirements below remain traceable and unaccepted; snapshot existence and restoration are not
verified. The active next task and release manifest identify non-recovery qualification separately.

منبع: پیوست اولیهٔ پرامپت. هر ۵۱ بخش حفظ شده است. مسیرها محل برنامه‌ریزی‌شده یا شروع‌شده‌اند. `P` یعنی برنامه‌ریزی‌شده، `D` یعنی مستندات آماده، `A` یعنی دروازهٔ مستندات با پذیرش مالک و بدون ادعای runtime، و `I` یعنی یک برش پیاده‌سازی آزموده وجود دارد ولی نیاز کامل نشده است. شمارهٔ مرحله بر اساس نقشهٔ راه جدید است.

استثنای تحویل جاری (۴ مهر ۱۴۰۵): مالک بازیابی مستقل را از صف کار تحویل محلی به تعویق انداخته و از
snapshot روزانهٔ ESXi خبر داده است. نیازهای پشتیبان و بازیابی و بحران در جدول همچنان قابل ردیابی و
پذیرفته‌نشده‌اند؛ وجود نسخه‌ها و بازیابی موفق تأیید نشده‌اند. کار فعال بعدی و مانیفست انتشار،
صلاحیت‌سنجی غیربازیابی را جدا نشان می‌دهند.

| Original | Requirement / نیاز | Planned owner/location | Phase | Acceptance evidence / شاهد پذیرش | Status |
|---|---|---|---|---|---|
| 1 | Inspect before changes / بررسی پیش از تغییر | `docs/en/PHASE_0_REPORT.md`, `docs/fa/PHASE_0_REPORT.md` | 0 | Owner-accepted repository report; private live preflight remains / گزارش پذیرفته‌شده؛ بررسی خصوصی باقی است | A |
| 2 | Product objective / هدف محصول | `apps/api`, `application` | 2–8 | Evidence-linked end-to-end flow / جریان کامل مستند | P |
| 3 | Persian/English / فارسی و انگلیسی | `localization`, `apps/web` | 1–8 | Native wording and RTL/LTR tests / آزمون زبان و جهت | P |
| 4 | Core architecture / معماری اصلی | `packages/nextops/domain`, `contracts`, `policy`; future `application`, `infrastructure` | 0–1 | Accepted boundaries plus tested contract/policy slice / مرز پذیرفته و برش آزموده | I |
| 5 | Independent integrations / اتصال مستقل | `connectors` | 2–5 | Eleven versioned capability records / پروندهٔ یازده اتصال | P |
| 6 | Central MCP gateway / درگاه مرکزی | `apps/mcp_gateway` | 1–2 | Auth, routing, limits, failure isolation / هویت و محدودیت و جداسازی | P |
| 7 | RBAC / نقش و دسترسی | `packages/nextops/policy`, `packages/nextops/application` | 1 | Deny-by-default policy plus server-derived durable actor/session and cross-scope tests; full administration remains / سیاست رد و هویت ماندگار سمت سرور؛ مدیریت کامل باقی است | I |
| 8 | Approval / تأیید عملیات | `application`, `policy` | 1,7 | Exact digest, replay and expiry tests / هش دقیق و انقضا و بازپخش | P |
| 9 | Secrets / اطلاعات محرمانه | `infrastructure` | 1 | Boundary-local credentials, no leaks / مرز اطلاعات ورود و عدم نشت | P |
| 10 | Audit / ممیزی | `packages/nextops/persistence`, `application`; future `observability` | 1 | Transactional append-restricted events and rollback tests exist; browsing/export/checkpoints remain / رخداد ماندگار و rollback آزموده؛ مرور و checkpoint باقی است | I |
| 11 | Linux MCP / اتصال لینوکس | `connectors/linux` | 2 | Bounded diagnostics, simulator/lab evidence / عیب‌یابی محدود و شاهد | P |
| 12 | Windows MCP / اتصال ویندوز | `connectors/windows` | 3 | Constrained authenticated operations / عملیات محدود و دارای هویت | P |
| 13 | Cisco MCP / اتصال سیسکو | `connectors/cisco` | 3 | Version-specific read diagnostics / خواندن وابسته به نسخه | P |
| 14 | Juniper MCP / اتصال جونیپر | `connectors/juniper` | 3 | Junos contract/diff/commit-state tests / قرارداد و وضعیت تنظیمات | P |
| 15 | FortiGate MCP / اتصال فورتی‌گیت | `connectors/fortigate` | 4 | Scoped VPN/routing/policy evidence / شواهد محدود شبکه و سیاست | P |
| 16 | Sophos MCP / اتصال سوفوس | `connectors/sophos` | 4 | Verified API coverage and explicit limits / پوشش و محدودیت روشن API | P |
| 17 | Zabbix MCP / اتصال زبیکس | `connectors/zabbix` | 1–2 | Phase 1 status reads and bounded Phase 2 history/events are live on the controlled server path; durable model/browser acceptance remains / خواندن وضعیت مرحلهٔ یک و تاریخچه و رویداد محدود مرحلهٔ دو در مسیر کنترل‌شدهٔ سرور زنده‌اند؛ پذیرش ماندگار مدل و مرورگر باقی است | I |
| 18 | Grafana MCP / اتصال گرافانا | `connectors/grafana` | 3 | Authorized datasource queries / پرس‌وجوی منبع مجاز | P |
| 19 | SQL Server MCP / اتصال SQL Server | `connectors/sqlserver` | 5 | Read-only identity, DMV/limits tests / هویت فقط‌خواندنی و محدودیت | P |
| 20 | MySQL MCP / اتصال MySQL | `connectors/mysql` | 5 | Engine/version and bounded SQL tests / موتور و نسخه و SQL محدود | P |
| 21 | ESXi MCP / اتصال ESXi | `connectors/esxi` | 5 | Version/license-aware diagnostics / تشخیص سازگار با نسخه و مجوز | P |
| 22 | Topology / توپولوژی | `knowledge` | 3,6 | Provenance/freshness on relationships / منبع و تازگی رابطه | P |
| 23 | Incident correlation / هم‌بستگی رخداد | `knowledge`, `application` | 2,6 | Time-windowed cross-source evidence / شواهد چندمنبعی زمان‌مند | P |
| 24 | RCA / تحلیل علت ریشه‌ای | `knowledge`, `application` | 2,6 | Hypotheses versus verified causes / تفکیک فرضیه و علت تأییدشده | P |
| 25 | LLM abstraction / رابط مدل | `packages/nextops/inference`, `packages/nextops/api/answer_integrity.py` | 1–2 | Pinned local CPU model and bounded scheduler remain deployed; app release `01755d1` rejects truncated replies and passed bounded live relevance cases, while full held-out bilingual review remains / مدل محلی و صف محدود مستقرند؛ انتشار برنامه `01755d1` پاسخ ناتمام را رد می‌کند و آزمون محدودِ زنده را گذرانده است؛ بازبینی کامل معنایی باقی است | I |
| 26 | Offline mode / حالت آفلاین | `deploy/server-dependencies`, `deploy/inference`, `scripts` | 1,2,8 | Earlier Internet-blocked cold start passed; current app release passed browser WAN denial, but server-side WAN/reboot were not rerun and permanent host egress remains partial / شروع سردِ بدون اینترنت در کارزار پیشین موفق بود؛ انتشار تازه منع WAN مرورگر را گذراند، اما آزمون سمت سرور و reboot تکرار نشد و سیاست دائمی خروج میزبان ناقص است | I |
| 27 | Memory / حافظه | `knowledge` | 6 | Scoped, fresh conversation/incident memory / حافظهٔ محدود و تازه | P |
| 28 | Database abstraction / رابط پایگاه داده | `packages/nextops/persistence`, `migrations` | 1 | Baseline, roles and durability tested on real PostgreSQL; production lock/backup and alternatives remain / migration و role آزموده؛ تولید و جایگزین باقی است | I |
| 29 | API / رابط برنامه | `packages/nextops/api`, `packages/nextops/inference`, `contracts` | 1–2 | Authenticated app and inference routes, correlation, safe readiness and structured errors tested; later domains remain / مسیر برنامه و inference و خطای ساخت‌یافته آزموده؛ دامنه‌های بعدی باقی است | I |
| 30 | UI / رابط کاربری | `packages/nextops/api/static`; future operations console | 2–8 | Controlled release `01755d1` serves the simpler bilingual question/answer flow with focused filesystem display and collapsed full evidence; fresh browser checks passed, wider operations views remain / انتشار کنترل‌شدهٔ `01755d1` پرسش‌وپاسخ دوزبانهٔ ساده، نمایش متمرکز فایل‌سیستم و شواهد کاملِ بازشونده دارد؛ مرورگر تازه موفق بود و نماهای گستردهٔ عملیات باقی‌اند | I |
| 31 | Configuration / پیکربندی | `packages/nextops/configuration.py`, `packages/nextops/inference/configuration.py`, `deploy/**/*.yaml` | 1 | Typed fail-closed app/inference settings plus schema-validated deployer records; production secrets remain private / تنظیم سخت‌گیر و پروندهٔ معتبر؛ secret تولید خصوصی است | I |
| 32 | Inventory / موجودی تجهیزات | `packages/nextops/contracts`, `persistence`; future connectors | 1–2 | Immutable scoped target plus persisted fixture and denial tests; real inventory synchronization remains / هدف محدود و fixture ماندگار؛ همگام‌سازی واقعی باقی است | I |
| 33 | Health checks / بررسی سلامت | `packages/nextops/api`, `packages/nextops/inference` | 1–5 | App liveness, AI and connector tunnel readiness passed on controlled release `01755d1`; broader production recovery/observability remains / سلامت برنامه و آمادگی تونل‌های AI و اتصال‌دهنده روی انتشار کنترل‌شدهٔ `01755d1` موفق بود؛ بازیابی و پایش تولیدی باقی است | I |
| 34 | Error handling / مدیریت خطا | `packages/nextops/contracts`, `application`, `api` | 1–5 | Typed application/API errors, correlation and dependency failure tested; broader retry/isolation remains / خطا و correlation آزموده؛ retry گسترده باقی است | I |
| 35 | Observability / مشاهده‌پذیری | `observability` | 1,8 | Metrics/logs and audit distinction / تفکیک متریک و لاگ و ممیزی | P |
| 36 | Testing / آزمون | `tests`, future `evals` | 1–8 | 111 non-integration tests plus 6 isolated PostgreSQL cases and CI quality/security gates; broader Phase 2 live/evaluation cases remain / ۱۱۱ آزمون غیر‌یکپارچه و ۶ مورد PostgreSQL؛ آزمون زنده و ارزیابی گستردهٔ مرحلهٔ دو باقی است | I |
| 37 | Docker / کانتینر | `deploy/compose` | 1,8 | Restricted clean install and offline test / نصب محدود و آفلاین | P |
| 38 | Installation docs / مستندات نصب | `docs/en/INSTALL.md`, `docs/fa/INSTALL.md`, paired `DEPLOYMENT_DOSSIERS.md`, `deploy/server-dependencies`, `deploy/installers` | 0–8 | Four validated handoffs and guarded offline OS-package workflows exist; approved role bundles, complete application installers and clean-server evidence remain / چهار پرونده و نصب بستهٔ محافظت‌شده موجود؛ bundle و نصب کامل و شاهد سرور تمیز باقی است | I |
| 39 | Native Persian docs / مستندات فارسی طبیعی | `docs/fa`, `docs/en` | 0–8 | Paired guides and language review / همتای دو زبان و بازبینی | D |
| 40 | Lifecycle scripts / اسکریپت چرخهٔ عمر | `scripts`, `deploy/server-dependencies/*.yaml`, `deploy/installers` | 1,8 | Exact offline OS-package installation is guarded, idempotent and tested; application setup/start/stop/test/backup/restore remain / نصب دقیق package آفلاین محافظت‌شده و آزموده است؛ چرخهٔ کامل برنامه باقی است | I |
| 41 | Systemd / سرویس بومی | `deploy/systemd` | 1,8 | Units, hardening, resource and recovery tests / آزمون واحد سرویس و بازیابی | P |
| 42 | Security docs / مستندات امنیت | `docs/en/SECURITY.md`, `docs/fa/SECURITY.md` | 0–8 | Documented RBAC/secrets/TLS/audit/backup / راهنمای کنترل‌های امنیت | D |
| 43 | README / معرفی پروژه | `README.md`, `README_FA.md` | 0–8 | Honest status and bilingual navigation / وضعیت واقعی و مسیر دو زبان | D |
| 44 | Development rules / قواعد توسعه | `AGENTS.md`, `.agents/skills`, `docs/MARKDOWN_CONTEXT_INDEX.md`, `CONTRIBUTING.md` | 0–8 | Six repo skills, complete Markdown routing/catalog tests, types, reviews and no credential commits / شش skill مخزن، catalog آزموده، نوع و بازبینی | I |
| 45 | Real MCP interface / پروتکل واقعی MCP | `contracts`, `connectors/base` | 1–2 | SDK/protocol conformance tests / آزمون انطباق | P |
| 46 | Tool risk / ریسک ابزار | `packages/nextops/domain`, `packages/nextops/policy` | 1 | Trusted risk registry; request/model actor and risk fields rejected; all mutation classes denied / ریسک معتبر و رد تغییر | I |
| 47 | Decision workflow / گردش تصمیم | `application` | 1–2 | Bounded persisted state machine / ماشین حالت محدود و ماندگار | P |
| 48 | Self-verification / بررسی نتیجه | `application`, `connectors` | 2,7 | Fresh postconditions; unknown-outcome reconciliation / نتیجهٔ تازه و رفع ابهام | P |
| 49 | Phased delivery / تحویل مرحله‌ای | `docs/en/ROADMAP.md`, `docs/fa/ROADMAP.md` | 0–8 | Revised gates, all original scope retained / معیار جدید و حفظ دامنه | D |
| 50 | Phase completion / پایان مرحله | `docs/PROJECT_STATE.md`, `tests` | 0–8 | Phase 0, two Stage 1A increments and the Stage 1B repository foundation have evidence; server qualification and later phases remain / مرحلهٔ صفر، دو برش 1A و پایهٔ 1B شاهد دارند؛ سرور و مراحل بعدی باقی است | I |
| 51 | First architecture report / گزارش معماری نخست | `docs/en/PHASE_0_REPORT.md`, `docs/fa/PHASE_0_REPORT.md` | 0 | Owner accepted on 2026-09-21; infrastructure authorization remains separate / پذیرش مالک؛ مجوز زیرساخت جداست | A |

## Explicit revisions / اصلاحات صریح

Early security and CPU/offline validation; complete integration slices; local providers only; PostgreSQL-first; no admin or read-only shortcut; qualified rather than invented RCA probabilities; concise decision summaries rather than unrestricted reasoning traces; and no false single-host HA. These revisions come from the supplied enhanced prompt. See [ADRs](../adr/README.md).

امنیت و آفلاین از ابتدا، جریان کامل اتصال، مدل صرفاً محلی، PostgreSQL اولیه، نبود میان‌بُر مدیر یا خواندن، اطمینان مستند به‌جای احتمال ساختگی، خلاصهٔ تصمیم به‌جای نمایش نامحدود استدلال و عدم ادعای HA تک‌میزبان، اصلاحات صریح پرامپت بهبودیافته‌اند.
