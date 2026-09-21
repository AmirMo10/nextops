# Original-requirement traceability / ردیابی نیازهای اولیه

Source: [master prompt, original Appendix A](NEXTOPS_MASTER_PROMPT.md). All 51 original sections are retained. Paths below are planned or now-started implementation locations. `P` = planned; `D` = documentation drafted; `A` = owner-accepted documentation gate, not runtime implementation; `I` = a tested implementation slice exists but the full requirement is incomplete. Phase numbers follow the revised roadmap, not the original fourteen-phase order.

منبع: پیوست اولیهٔ پرامپت. هر ۵۱ بخش حفظ شده است. مسیرها محل برنامه‌ریزی‌شده یا شروع‌شده‌اند. `P` یعنی برنامه‌ریزی‌شده، `D` یعنی مستندات آماده، `A` یعنی دروازهٔ مستندات با پذیرش مالک و بدون ادعای runtime، و `I` یعنی یک برش پیاده‌سازی آزموده وجود دارد ولی نیاز کامل نشده است. شمارهٔ مرحله بر اساس نقشهٔ راه جدید است.

| Original | Requirement / نیاز | Planned owner/location | Phase | Acceptance evidence / شاهد پذیرش | Status |
|---|---|---|---|---|---|
| 1 | Inspect before changes / بررسی پیش از تغییر | `docs/en/PHASE_0_REPORT.md`, `docs/fa/PHASE_0_REPORT.md` | 0 | Owner-accepted repository report; private live preflight remains / گزارش پذیرفته‌شده؛ بررسی خصوصی باقی است | A |
| 2 | Product objective / هدف محصول | `apps/api`, `application` | 2–8 | Evidence-linked end-to-end flow / جریان کامل مستند | P |
| 3 | Persian/English / فارسی و انگلیسی | `localization`, `apps/web` | 1–8 | Native wording and RTL/LTR tests / آزمون زبان و جهت | P |
| 4 | Core architecture / معماری اصلی | `packages/nextops/domain`, `contracts`, `policy`; future `application`, `infrastructure` | 0–1 | Accepted boundaries plus tested contract/policy slice / مرز پذیرفته و برش آزموده | I |
| 5 | Independent integrations / اتصال مستقل | `connectors` | 2–5 | Eleven versioned capability records / پروندهٔ یازده اتصال | P |
| 6 | Central MCP gateway / درگاه مرکزی | `apps/mcp_gateway` | 1–2 | Auth, routing, limits, failure isolation / هویت و محدودیت و جداسازی | P |
| 7 | RBAC / نقش و دسترسی | `packages/nextops/policy` | 1 | Deny-by-default organization/environment/target/action/scope tests; durable identity remains / آزمون دامنه؛ هویت ماندگار باقی است | I |
| 8 | Approval / تأیید عملیات | `application`, `policy` | 1,7 | Exact digest, replay and expiry tests / هش دقیق و انقضا و بازپخش | P |
| 9 | Secrets / اطلاعات محرمانه | `infrastructure` | 1 | Boundary-local credentials, no leaks / مرز اطلاعات ورود و عدم نشت | P |
| 10 | Audit / ممیزی | `infrastructure`, `observability` | 1 | Durable sanitized decisions/effects / ثبت ماندگار و پالایش‌شده | P |
| 11 | Linux MCP / اتصال لینوکس | `connectors/linux` | 2 | Bounded diagnostics, simulator/lab evidence / عیب‌یابی محدود و شاهد | P |
| 12 | Windows MCP / اتصال ویندوز | `connectors/windows` | 3 | Constrained authenticated operations / عملیات محدود و دارای هویت | P |
| 13 | Cisco MCP / اتصال سیسکو | `connectors/cisco` | 3 | Version-specific read diagnostics / خواندن وابسته به نسخه | P |
| 14 | Juniper MCP / اتصال جونیپر | `connectors/juniper` | 3 | Junos contract/diff/commit-state tests / قرارداد و وضعیت تنظیمات | P |
| 15 | FortiGate MCP / اتصال فورتی‌گیت | `connectors/fortigate` | 4 | Scoped VPN/routing/policy evidence / شواهد محدود شبکه و سیاست | P |
| 16 | Sophos MCP / اتصال سوفوس | `connectors/sophos` | 4 | Verified API coverage and explicit limits / پوشش و محدودیت روشن API | P |
| 17 | Zabbix MCP / اتصال زبیکس | `connectors/zabbix` | 1–2 | Phase 1 status reads; Phase 2 bounded history correlation / خواندن وضعیت در مرحلهٔ یک و تاریخچه در مرحلهٔ دو | P |
| 18 | Grafana MCP / اتصال گرافانا | `connectors/grafana` | 3 | Authorized datasource queries / پرس‌وجوی منبع مجاز | P |
| 19 | SQL Server MCP / اتصال SQL Server | `connectors/sqlserver` | 5 | Read-only identity, DMV/limits tests / هویت فقط‌خواندنی و محدودیت | P |
| 20 | MySQL MCP / اتصال MySQL | `connectors/mysql` | 5 | Engine/version and bounded SQL tests / موتور و نسخه و SQL محدود | P |
| 21 | ESXi MCP / اتصال ESXi | `connectors/esxi` | 5 | Version/license-aware diagnostics / تشخیص سازگار با نسخه و مجوز | P |
| 22 | Topology / توپولوژی | `knowledge` | 3,6 | Provenance/freshness on relationships / منبع و تازگی رابطه | P |
| 23 | Incident correlation / هم‌بستگی رخداد | `knowledge`, `application` | 2,6 | Time-windowed cross-source evidence / شواهد چندمنبعی زمان‌مند | P |
| 24 | RCA / تحلیل علت ریشه‌ای | `knowledge`, `application` | 2,6 | Hypotheses versus verified causes / تفکیک فرضیه و علت تأییدشده | P |
| 25 | LLM abstraction / رابط مدل | `inference` | 1–2 | CPU-only provider contract; no cloud fallback / قرارداد محلی | P |
| 26 | Offline mode / حالت آفلاین | `deploy`, `scripts` | 1,2,8 | Internet-blocked end-to-end test / آزمون کامل بدون اینترنت | P |
| 27 | Memory / حافظه | `knowledge` | 6 | Scoped, fresh conversation/incident memory / حافظهٔ محدود و تازه | P |
| 28 | Database abstraction / رابط پایگاه داده | `infrastructure`, `migrations` | 1 | Real PostgreSQL tests; alternatives tracked / آزمون واقعی و پیگیری جایگزین | P |
| 29 | API / رابط برنامه | `apps/api`, `contracts` | 1–2 | Authenticated versioned routes / مسیر نسخه‌دار و دارای هویت | P |
| 30 | UI / رابط کاربری | `apps/web` | 2–8 | Operations views, summaries and accessibility / نماهای عملیات و دسترس‌پذیری | P |
| 31 | Configuration / پیکربندی | `config` | 1 | Typed external settings, no secrets / تنظیمات معتبر و بدون رمز | P |
| 32 | Inventory / موجودی تجهیزات | `packages/nextops/contracts`, future `infrastructure` | 1–2 | Immutable scoped target contract and denial tests; inventory persistence remains / قرارداد هدف و رد؛ ماندگاری باقی است | I |
| 33 | Health checks / بررسی سلامت | `apps`, `connectors` | 1–5 | Honest readiness/capability states / آمادگی و قابلیت واقعی | P |
| 34 | Error handling / مدیریت خطا | `packages/nextops/contracts`, future `application` | 1–5 | Typed error contract exists; retry/isolation behavior remains / قرارداد خطا موجود؛ رفتار اجرا باقی است | I |
| 35 | Observability / مشاهده‌پذیری | `observability` | 1,8 | Metrics/logs and audit distinction / تفکیک متریک و لاگ و ممیزی | P |
| 36 | Testing / آزمون | `tests`, future `evals` | 1–8 | 18 unit cases plus lint/type/lock/audit evidence; integration/evals remain / ۱۸ آزمون و کنترل؛ integration باقی است | I |
| 37 | Docker / کانتینر | `deploy/compose` | 1,8 | Restricted clean install and offline test / نصب محدود و آفلاین | P |
| 38 | Installation docs / مستندات نصب | `docs/en/INSTALL.md`, `docs/fa/INSTALL.md` | 0–8 | Guides drafted; clean-install commands pending / راهنما آماده، دستور آزموده در آینده | D |
| 39 | Native Persian docs / مستندات فارسی طبیعی | `docs/fa`, `docs/en` | 0–8 | Paired guides and language review / همتای دو زبان و بازبینی | D |
| 40 | Lifecycle scripts / اسکریپت چرخهٔ عمر | `scripts` | 1,8 | Idempotent install/setup/start/stop/test/backup/restore / اجرای تکرارپذیر | P |
| 41 | Systemd / سرویس بومی | `deploy/systemd` | 1,8 | Units, hardening, resource and recovery tests / آزمون واحد سرویس و بازیابی | P |
| 42 | Security docs / مستندات امنیت | `docs/en/SECURITY.md`, `docs/fa/SECURITY.md` | 0–8 | Documented RBAC/secrets/TLS/audit/backup / راهنمای کنترل‌های امنیت | D |
| 43 | README / معرفی پروژه | `README.md`, `README_FA.md` | 0–8 | Honest status and bilingual navigation / وضعیت واقعی و مسیر دو زبان | D |
| 44 | Development rules / قواعد توسعه | `AGENTS.md`, `CONTRIBUTING.md` | 0–8 | Types, reviews, tests, no credential commits / نوع و بازبینی و آزمون | D |
| 45 | Real MCP interface / پروتکل واقعی MCP | `contracts`, `connectors/base` | 1–2 | SDK/protocol conformance tests / آزمون انطباق | P |
| 46 | Tool risk / ریسک ابزار | `packages/nextops/domain`, `packages/nextops/policy` | 1 | Trusted risk registry; request/model actor and risk fields rejected; all mutation classes denied / ریسک معتبر و رد تغییر | I |
| 47 | Decision workflow / گردش تصمیم | `application` | 1–2 | Bounded persisted state machine / ماشین حالت محدود و ماندگار | P |
| 48 | Self-verification / بررسی نتیجه | `application`, `connectors` | 2,7 | Fresh postconditions; unknown-outcome reconciliation / نتیجهٔ تازه و رفع ابهام | P |
| 49 | Phased delivery / تحویل مرحله‌ای | `docs/en/ROADMAP.md`, `docs/fa/ROADMAP.md` | 0–8 | Revised gates, all original scope retained / معیار جدید و حفظ دامنه | D |
| 50 | Phase completion / پایان مرحله | `docs/PROJECT_STATE.md`, `tests` | 0–8 | Implement/test/fix/document/commit evidence / شاهد ساخت و آزمون و ثبت | P |
| 51 | First architecture report / گزارش معماری نخست | `docs/en/PHASE_0_REPORT.md`, `docs/fa/PHASE_0_REPORT.md` | 0 | Owner accepted on 2026-09-21; infrastructure authorization remains separate / پذیرش مالک؛ مجوز زیرساخت جداست | A |

## Explicit revisions / اصلاحات صریح

Early security and CPU/offline validation; complete integration slices; local providers only; PostgreSQL-first; no admin or read-only shortcut; qualified rather than invented RCA probabilities; concise decision summaries rather than unrestricted reasoning traces; and no false single-host HA. These revisions come from the supplied enhanced prompt. See [ADRs](../adr/README.md).

امنیت و آفلاین از ابتدا، جریان کامل اتصال، مدل صرفاً محلی، PostgreSQL اولیه، نبود میان‌بُر مدیر یا خواندن، اطمینان مستند به‌جای احتمال ساختگی، خلاصهٔ تصمیم به‌جای نمایش نامحدود استدلال و عدم ادعای HA تک‌میزبان، اصلاحات صریح پرامپت بهبودیافته‌اند.
