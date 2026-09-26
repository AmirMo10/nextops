# Testing, model evaluation and release evidence

[فارسی](../fa/TESTING.md) · [Index](INDEX.md)

**Status: active test plan with repository, isolated PostgreSQL, live connector and bounded local-AI
evidence.** Authenticated browser-path, live read-only Zabbix, durable investigation, revoked-token,
unreachable-API, recovery, four-guest WAN isolation and serial clean-reboot checks have run in the
controlled environment. Change `stage1-completion-20260922-01` additionally passed a fresh
WAN-denied browser, application/runtime/model rollback, cancellation and dependency recovery,
missing/corrupt artifact handling, an isolated low-space staging case, five-minute bounded load and
logical isolated restores of both PostgreSQL 16 databases. Independent off-datastore backup,
WAL/PITR and production acceptance remain open. Source: master specification sections 10–14 and
21–23.

## Focused application release — 2026-09-26

PR #10 merged source tree `01755d1` into main after hosted run `36239227073` passed all five
jobs: quality, PostgreSQL 16, PostgreSQL 17, real-browser fixture and secret scan. On the Windows
checkout, 182 tests passed and ten were skipped (nine real-PostgreSQL cases without an isolated
test URL and one POSIX-only collector); Ruff format/lint, strict mypy, paired-document/local-link
validation and release-status validation passed. The two browser-fixture cases also passed. These
local skips are not relabelled as passes; the hosted PostgreSQL jobs exercised the database cases.

Under private change `user-testing-app-01755d1-20260926`, the exact
`nextops-0.1.0-01755d1` wheel matched SHA-256
`cb04cd3c0dc37370d956b65851de5bd7135b14cc0ea2881039bdd703b2839bfd`. A fresh virtualenv
was installed offline at its final immutable path from the unchanged hashed dependency wheelhouse.
The `uvicorn` launcher points inside the new release, not at the prior copied virtualenv. The old
app release remains present; AI API and connector remained `cdde129`. The app switched under a
15-minute automatic rollback timer. Release-file integrity, app/database/tunnel readiness,
`running` system state, zero failed units and loopback health `200` passed; the timer was disarmed
only after live qualification.

A fresh authenticated API session passed English `Hi` (6.19 seconds) and Persian `سلام`
(12.53 seconds) without unrelated Zabbix status. Fresh Zabbix monitoring returned `200` with
source time, evidence hash/reference and audit ID (41.88 seconds). The general system-file
question returned a scope limitation, not fabricated file names. English file-listing and
filesystem-capacity investigations and Persian filesystem capacity returned the expected focused
answer, source times, hash and durable audit IDs (14.86, 18.36 and 22.48 seconds). An
unauthenticated readiness request was denied; the test session logged out with server `204`.
A fresh Edge context then passed login, dependency readiness, greeting, focused file refusal,
filesystem capacity, Persian RTL/mobile width, logout/new-tab isolation and zero page requests to
external hosts under a deny proxy with normal TLS verification.

An initial login probe used an outdated private test password and failed; the current protected
credential then passed. Two initial browser harness runs incorrectly used `innerText` for an audit
field inside a collapsed disclosure, so they read an empty value. The corrected test used hidden
text content and passed. The two aborted sessions could not be individually revoked after their
test processes exited and are left to the configured server expiry; the passing browser run did
complete server-side logout. These are test limitations, not evidence that the app omitted audit.

The full held-out bilingual semantic corpus, owner's exact redacted question/answer reproduction,
exact-release rollback execution, server-side WAN-disconnection and VM reboot were **not run** on
this app revision. Earlier rollback/offline/reboot evidence remains historical. This promotion is
for controlled user testing, not production acceptance; independent recovery and the other
production gates remain open.

## Production-hardening evidence — 2026-09-26

The OS-origin audit found Zabbix Agent 2 `7.0.30` installed from offline packages on the app, AI
and connector guests while the Zabbix server and its own agent were `7.0.31`. The cached `7.0.31`
agent package matched the SHA-256 in the configured Zabbix apt repository metadata
(`c08d08bec9495616a5fe45d026c0ebecfe0246af30197f1b014aa72aee5c3dea`); the prior package
also matched its metadata (`d7e5ca70b5ff102e70e1e409a6459b2a210ba76316b96ecdddb889fe935cad69`).
Offline install simulations on all three targets showed one upgrade, no added packages and no
removals. The first connector `apt-get` attempt rejected the percent-encoded epoch pathname before
mutation; `dpkg --force-confold -i` then upgraded each guest serially under a rollback timer.
Original configuration hashes stayed unchanged, each agent reported `7.0.31` and `active`, no
passive `10050` listener or recent service warning appeared, and all hosts stayed `running`.
Root-only copies of both exact packages and the prior configuration remain on each guest. The
three Agent 2 installations still have no configured apt origin, so future offline patch imports
must be deliberately maintained; `apt list --upgradable` alone would miss a new Agent 2 release.
After the upgrades, another fresh WAN-denied Edge session passed login, English/Persian layout,
local AI, new Zabbix evidence with provenance, logout `204` and new-tab isolation.
A read-only Zabbix database check then found `agent.ping=1` for all four enabled hosts, with the
oldest ping 48 seconds old. The `agent.version` item runs hourly and still showed a mix of
`7.0.30`/`7.0.31` at that instant; local package and binary checks prove installed versions, but
the new version had not yet propagated through that scheduled Zabbix item. No immediate item
refresh or fabricated monitoring value was used.

Commit `cdde129` added a no-redirect HTTP boundary to credentialed application/connector clients.
A local 302 server test proved both transport implementations reject the redirect without making
a second request or forwarding Authorization. Selected local checks: 161 passed, one POSIX-only
skip and nine PostgreSQL integration deselections; Ruff, strict mypy and Bandit passed. Hosted run
`36231550331` passed quality/unit, PostgreSQL 16, PostgreSQL 17, browser and secret-scan jobs.
The exact pure-Python wheel and 25 locked Linux dependency wheels were transferred by SHA-256 and
installed offline into immutable app, AI and connector releases `nextops-0.1.0-cdde129`.

On all four guests, a staged SSH drop-in passed `sshd -t`; effective policy denied direct root,
password and keyboard-interactive logins and required public keys. New operator key connections
passed. The application-to-AI and application-to-connector tunnels were restarted and their
loopback readiness endpoints responded after startup. A fresh Edge context, with public WAN denied
and normal TLS verification, passed English/Persian login and layout, direct local answer, Zabbix
evidence/provenance, logout `204` and new-tab isolation through those new tunnels. The AI guest's
UFW was activated under a five-minute rollback guard; a new SSH session passed, then the guard was
cancelled. It now reports deny-incoming, allow-outgoing and OpenSSH ingress, with inference/model
listeners still loopback-only. An initial one-off composite-browser selector timed out before
submitting any incident request because native `<option>` elements are not visibly rendered;
that harness error is not an application acceptance result. The corrected fresh Edge run selected
one of four approved incident targets and passed a live Zabbix-plus-Linux investigation with an
answer and durable run/audit identifiers while public browser WAN requests were denied. After the
AI firewall change, a newly restarted app-to-AI tunnel regained local model readiness.

The earlier server-side offline qualification used a **temporary** outbound nftables table and
removed it after testing. A current direct IPv4 HTTPS probe from an administrator shell succeeds
on all four guests; direct IPv6 failed in this check. The app, AI API and model systemd units still
report `IPAddressDeny=any` with loopback allow. The connector now also denies all IP destinations
except loopback and its reviewed deployment LAN; general host processes remain unrestricted by a
permanent host-wide Internet deny. Thus the named offline acceptance tests remain historical
passes, while a permanent host egress policy is only partial. No permanent host-wide outbound
block was added without a verified DNS/time/maintenance-proxy allowlist and safe rollback route.

For the connector, the protected inventory and DNS resolution placed the Zabbix API and all four
forced-command targets inside the approved LAN range. A rendered, root-owned systemd drop-in
passed unit verification and reported `IPAddressDeny=any` with only loopback and that LAN allowed.
The connector restarted healthy under a rollback timer. Four fresh authenticated Edge incident
requests then passed, one per approved target, each returning Zabbix and Linux evidence with
durable run/audit identifiers while browser WAN access was denied. A controlled transient unit
using the same IP rules timed out to a public HTTPS destination that returned HTTP 200 without
the rules; the production connector was not modified by that negative probe. The service had no
new warnings and the rollback guard was cancelled. This proves the named connector process
boundary, not a host-wide outbound firewall.

Change `production-hardening-20260926-01` updated the four serving guests serially only after
reconstructing each installed package, staging every exact candidate package and writing SHA-256
manifests into root-only per-host rollback directories. The application and Zabbix PostgreSQL
clusters also received readable local custom-format safety dumps before package mutation. These
files are rollback inputs for this change, not independent recovery copies.

All four guests ended `running`, with zero failed units, zero pending packages and no reboot marker.
Application PostgreSQL and Zabbix PostgreSQL remain `16.15`; Zabbix is now `7.0.31`. Application,
AI/llama and connector services/listeners passed their role checks, and an authenticated request
through the application confirmed AI readiness and the protected connector path.

A new Microsoft Edge context then ran with a deny proxy for public WAN and a private-host bypass.
Fresh login, English LTR, Persian RTL, general local-AI output, evidence-grounded monitoring,
source/run/evidence/audit identifiers, server-side logout `204`, cleared tab state and fresh-tab
login isolation passed. The initial run failed only because the harness asserted the login view
before the asynchronous logout handler finished. The harness now waits for that transition and
requires the server response; the unchanged deployed JavaScript and the corrected live rerun
passed. Browser background traffic produced blocked proxy attempts, while the page itself requested
no external host.

The exact deployed application archive was hashed before inspection. Digest-verified Syft `1.52.0`
generated private SPDX and CycloneDX SBOMs with 27 packages and 26 components. A production-only
25-dependency input audited with `pip-audit 2.10.1` returned zero known findings. This does not
replace a full operating-system/runtime scan or human review. The project package and repository
also lack a declared NextOps license, so license, complete vulnerability, offline-signature and
named security/legal approval gates remain open.

## Answer-integrity qualification — 2026-09-26

The final source at `2397581` passed all five hosted jobs: quality/unit, PostgreSQL 16,
PostgreSQL 17, real-browser fixture and secret scan. Local checks reported 159 passed and ten
environment-specific skips; the skipped PostgreSQL cases were covered by both hosted database jobs,
and the POSIX collector retains its Linux evidence.

Inference release `nextops-0.1.0-fd3c353` passed a private loopback run of eight balanced
English/Persian cases. Authentication denial, readiness, evidence timestamp/failure preservation,
non-execution, greeting relevance, unknown current state, required/forbidden phrases, response
script and prompt-echo rejection all passed. Engineering semantic review accepted every final
answer. This is not a universal hallucination measurement; arbitrary model-only facts remain
unverified.

Application release `nextops-0.1.0-2397581` then passed live authenticated checks. `Hi` contained
no Zabbix result; a general request for current Zabbix state returned `scope_redirect`; live
monitoring returned consistent `live_zabbix` metadata and `evidence_bounded`; and the composite app
incident returned consistent `live_zabbix_linux` metadata with a safe `deterministic_fallback`. The
short-lived test session was revoked, leaving no active test session. A serial reboot of Zabbix,
connector, AI and app loaded kernel `6.8.0-142`; every role returned healthy with zero failed units,
no reboot marker and no warning-or-higher service journal entry. Six Ubuntu updates remain pending
on app/AI/connector and eleven on Zabbix; no package was fetched without the approved proxy/offline
path, and Zabbix 7.0.31 is not qualified.

## Phase 2 current qualification — 2026-09-23

Phase 2 connector release `nextops-0.1.0-e2dad3a` and current application release
`nextops-0.1.0-eb57241` passed the source quality/unit job, PostgreSQL 16 and 17 integration jobs,
real-browser fixture job and secret scan. The source suite includes forced-command parsing,
private-target validation, strict host-key/identity construction, provenance mismatch, output limits,
redaction, authentication, scope denial, unknown targets, safe dependency errors, prompt-injection
text, durable composite evidence, reversible scope migration and Persian/English RTL/LTR behavior.

On the controlled guests, each of the four direct Linux collectors and each composite connector
path returned schema-valid bounded evidence. Generic shell execution, unauthenticated access and an
unknown target were denied. Fresh English and Persian application API investigations returned local
CPU answers and durable run/evidence/audit IDs. App/connector restart, immutable rollback/forward,
server/API WAN denial, authenticated live browser, Phase 2 serial VM reboot and Phase 2 dependency
loss/recovery passed. The OCS frontend passed English desktop and Persian RTL mobile views with no
external request, failed response, console error or horizontal overflow. See the
[Phase 2 qualification record](PHASE_2_COMPLETION_SPEC.md).

The same release also passed the controlled session-termination gate. Direct API and normal-TLS
browser logout returned `204`, former tokens received `401`, a second session stayed valid, replay
was idempotent, and exactly one sanitized correlated audit event was present.

The certificate-detection source at `f540a9d` passed all five hosted CI jobs: quality/unit,
PostgreSQL 16, PostgreSQL 17, browser fixture and secret scan. Controlled installation on both TLS
frontends passed immediate and persistent-timer checks, public-certificate-only access, private-key
denial, `2.7 OK` systemd security review, healthy 90-day classification, isolated expiring and
malformed fixtures, Nginx validation, normal application TLS and pinned-CA Zabbix HTTPS. Four local
Zabbix active-agent items received fresh one-minute values and six tagged triggers were healthy. A
five-minute recovery guard preceded an application-timer stop; its trigger entered problem, the
timer was restored, fresh `active` data arrived and the trigger recovered. Operator notification
delivery and live-pair rotation/rollback were not run.

## Historical Phase 2A controlled deployment evidence

The bounded incident-context contract is implemented and tested at connector and application API
boundaries. Deterministic tests verify the exact configured host, 15–1440-minute configuration
validation, fixed `history.get`/`event.get` parameters, four-metric/eight-point/25-event public
limits, timestamp provenance, partial-result markers, bearer authentication and safe dependency
errors. Under change `phase2a-incident-context-20260923-01`, immutable app and connector release
`nextops-0.1.0-1ab6586` was deployed and its checksums verified. The reader role was expanded by
exactly `history.get` and `event.get`; unrelated methods remain denied. A live Zabbix 7.0.30 request
returned eight current metrics and 32 bounded history points, no events in the observed window, and
the expected truncation reasons. Connector bearer denial, application-session denial, the protected
app-to-connector tunnel, application and connector release rollback/forward, and reader-role
rollback/forward passed.

A separately named temporary nftables table, armed with a five-minute automatic rollback timer,
blocked direct IPv4 and IPv6 WAN traffic on the app, connector and Zabbix guests while the live
incident-context request continued through the approved private path. The table and timer were then
removed; direct IPv4 TCP reachability returned, all four guests were `running`, failed-unit counts
were zero and no reboot was required. This proves the Phase 2A server path under guarded WAN denial,
not a fresh authenticated browser flow or cold start. Authenticated browser/session use, durable
model/audit linkage and Phase 2A VM reboot were `not_run` at that checkpoint. The current record
above supersedes that implementation state while preserving the dated evidence.

## Stage 1 controlled completion qualification

The [dated completion report](STAGE_1_COMPLETION_REPORT.md) is the evidence summary. Its browser
harness uses a fresh Edge context, normal TLS verification and a local deny proxy that bypasses only
the private application origin. Application traffic addressed no Internet host; 21 Edge background
requests were blocked. Login, both text directions, general and monitoring modes, provenance,
durable identifiers, logout and a new-tab login requirement passed.

Server-side logout source coverage now verifies missing-bearer denial, exact correlated revocation,
empty idempotent responses, isolation from the identity's other sessions, one sanitized append-only
audit event, browser `sessionStorage` removal and localized return to login. The PostgreSQL checks
run in the version 16/17 CI matrix. This becomes deployed acceptance only after a former live token
is rejected by a protected endpoint and the corresponding audit event is verified.

The application rolled back from `13a3369` to `fde27bd` and forward again. Hash-matched protected
runtime/model copies were selected through the stable links, generated through the actual NextOps
inference API, and then restored to the original paths. Live cancellation released capacity;
provider loss produced a sanitized retryable application `503`; missing and corrupt temporary model
targets failed closed; and an isolated 64 MiB artifact-copy target returned `ENOSPC` without changing
the serving model.

The five-minute two-client profile completed 99 requests with 98 successes and one bounded timeout.
Total latency p50/p95/max was 6.095/6.114/8.520 seconds, peak measured service memory was
4,885,475,328 bytes, and the scheduler maximum was one active and one queued request. TTFT is not
observable through the non-streaming API. Both checksummed logical dumps restored into temporary,
socket-only PostgreSQL 16.15 clusters; schema, application audit protection, Zabbix configuration and
history counts were verified before complete cleanup. This proves logical restore mechanics, not
independent disaster recovery or PITR.

## Stage 1E failure qualification

The scoped failure increment separates deterministic fixtures from live operational evidence:

- Isolated connector/API tests cover old measurements, bounded partial results, no usable metrics,
  malformed over-limit text and monitoring-field prompt injection. Authenticated source identity
  does not make host, metric, value, unit or problem text an instruction.
- The live connector marks its eight-item bounded view as partial with
  `metrics_truncated`; all eight observed measurements were fresh. The marker survives model
  synthesis, canonical evidence hashing, durable storage, audit details and run retrieval.
- A disposable token owned by the existing reader identity saw only the four approved hosts,
  failed immediately after revocation and was deleted. The live connector token remained active.
- With the Zabbix HTTPS/API frontend briefly stopped, monitoring summary and investigation returned
  safe retryable `503` responses with `connector.summary_unavailable`. The failed run and matching
  append-only audit event were stored, while a model-only general question still completed locally.
  Restart restored fresh monitoring, and no raw dependency response or credential reached the API.
- Stopping the Zabbix engine alone did not make the PHP JSON-RPC API unreachable because the
  frontend reads the database directly. That observed distinction is retained rather than being
  mislabeled as an outage pass.

These results qualify the named cases only. They do not replace the remaining browser-isolated WAN,
certificate-expiry, timeout/cancellation, low-space, sustained-load, backup and restore matrix.

## Stage 1F WAN isolation and reboot qualification

A temporary, separately named nftables output policy was applied to all four guests after an
automatic rollback timer was armed. It preserved loopback, the approved private LAN and link-local
IPv6 while rejecting every other IPv4 and IPv6 destination. Direct Internet probes failed on all
four guests and rule counters recorded rejected packets. SSH and approved LAN paths remained
available, and every guest stayed in `running` system state with zero failed units.

While all four guests were isolated, a fresh authenticated session passed English and Persian
model-only questions without Zabbix contamination. Local-AI readiness passed, and a new live
investigation returned eight fresh measurements, the expected `metrics_truncated` marker, durable
storage, an independently verified evidence hash and linked audit. This passes the server/API
portion of OFF-01 and OFF-05. OFF-03 remains partial because the client used a fresh authenticated
API session rather than a separately WAN-isolated fresh browser process.

The initial Zabbix reboot attempts reached systemd's 30-minute job timeout. A corrected test harness
reproduced the delay and excluded itself as the cause. The previous-boot journal then showed the
actual race: the vendor Zabbix unit referenced the inert PostgreSQL meta-unit and had an infinite
stop timeout, so the real database cluster stopped first and the remaining Zabbix processes could
not finish. A reviewed drop-in now requires and orders around `postgresql@16-zabbix.service` and
bounds stop time at 90 seconds. A controlled stop completed in under one second with the database
still active; the next reboot stopped Zabbix before PostgreSQL and started PostgreSQL before Zabbix.

The connector, AI and application guests were then rebooted serially, never concurrently. Connector
and AI recovered without correction. The first application boot exposed the same meta-unit defect:
its PostgreSQL cluster remained down while the API process started. An application drop-in requiring
`postgresql@16-nextops.service` corrected the dependency, and the retry started the database before
the API. Every accepted reboot loaded the temporary WAN-deny policy before normal networking,
returned to `running` with zero failed units, passed its role-specific services, fresh login,
bilingual model-only Q&A and/or eight fresh monitoring metrics, then removed all temporary policy
files and restored direct HTTPS. A final durable investigation passed after the application reboot.
The server/API portion of clean offline-reboot acceptance passed at this checkpoint. The later
`stage1-completion-20260922-01` campaign closed the fresh-browser subcase recorded above.

## Phase 2 live qualification

On 2026-09-23 a fresh Microsoft Edge context reached only the private application origin while a
deny proxy blocked WAN traffic and normal TLS verification remained enabled. Fresh English and
Persian incident requests selected deployment-owned `app` and `ai` targets, returned combined
Zabbix/Linux provenance and new durable run, evidence and audit identifiers, and passed RTL mobile,
logout and new-tab isolation checks. The application made no external page request.

The first attempt returned HTTP `504` after 30 seconds even though llama.cpp was still generating.
The request path `/api/v1/incidents/investigate` was missing from Nginx's bounded 180-second
assistant location and fell through to the 30-second default. The versioned profile and its static
test were corrected, `nginx -t` passed before reload, and the complete live-browser gate then
passed twice, including once after the VM reboot sequence.

For dependency recovery, a five-minute automatic restart guard was armed before the read-only
connector stopped. The incident route returned a safe localized `503` with
`dependency_unavailable`, while a general local-AI question returned `200`. After connector
`/healthz` recovered, monitoring returned `200` and a fresh combined incident with durable audit
identifiers passed. The guard was removed and the connector ended active.

Zabbix, connector, AI and app then rebooted serially. Every accepted reboot changed its boot ID,
returned the role-specific services and local health checks, reached `running`, reported zero
failed units and cleared the reboot-required marker. Connector, AI and app recovery took 15.109,
29.031 and 19.531 seconds respectively. The initial Zabbix verifier used the wrong PostgreSQL unit
and web bind; the actual `postgresql@16-zabbix` cluster, Zabbix listener and CA-verified TLS frontend
passed the corrected post-reboot checks, so no artificial Zabbix latency is reported. A final fresh
bilingual browser investigation passed across the restarted stack.

## Test layers

| Layer | Required evidence |
|---|---|
| Unit | Domain invariants, deterministic policy, scope checks, argument validation |
| PostgreSQL integration | Migrations, constraints, durable jobs, leases, atomic approvals and recovery |
| MCP contract | Negotiation, tools/schemas, auth, cancellation, errors, bounded/partial output |
| Connector simulator | Supported diagnostics and explicit unsupported behavior without real credentials |
| API/browser | Authentication, permissions, streaming/reconnect, pagination, both text directions |
| Security | Injection, target substitution, secret redaction, gateway bypass and replay protection |
| Reliability | Restarts, duplicate jobs, full disk, failed audit/database/model and uncertain remote results |
| Offline | Local assets/models/auth/retrieval and permitted LAN operations without Internet |
| CPU/load | Bounded mixed workloads, latency distributions and resource limits on verified hardware |
| Recovery/release | Restore drill, version/schema compatibility, rollback conditions |

Use actual PostgreSQL for database behavior, not SQLite substituted for convenience. Simulators are the default; lab/production tests require explicit authorization and recorded vendor versions. A mocked response is not proof that a device API works.

## Mandatory adversarial cases

Include instructions hidden in logs/runbooks/tool descriptions; cross-organization/environment evidence; unauthorized targets; command and SQL injection; secret-bearing errors; stale, forged or replayed approvals; argument/target/pre-state changes after consent; revoked user roles; duplicate jobs; direct gateway bypass; DNS/redirect substitution; malformed model output; connector crash; unavailable audit; and cancellation or timeout after possible mutation.

Assert policy outcomes, not merely polite refusal text. No unauthorized executions in the defined suite is a release gate, not proof that future attacks are impossible. Do not reduce test coverage or weaken permission checks to obtain a passing result.

## Bilingual evaluation corpus

Version Persian, English and mixed-language synthetic cases: Linux/network/firewall/database/ESXi incidents, ambiguous names, incomplete evidence, malicious text and approval/refusal boundaries. Split development and held-out evaluation and record sample counts. Keep source identifiers and executable commands intact. Domain and native-Persian review are necessary; automated judges are optional local CPU tools and not the sole decision maker.

Measure correct tool/argument selection, policy outcomes, unsupported-claim rate, evidence references, retrieval quality, recovery behavior, Persian readability, schema validity, queue delay, time to first token and total latency. A good overall average must not hide catastrophic failure in one action category.

## Evidence report

Each report records commit, commands, test counts, failures/skips, dataset and model versions, hardware/runtime identity, measurements, limitations and sanitized reproduction steps. Preserve raw benchmark samples where safe. Targets are distinct from observations. Health, simulated capability and production qualification are distinct statuses.

## Repository checks available now

After cloning, install the frozen development environment and run the same core checks as CI:

```bash
uv sync --extra dev --frozen
uv run ruff format --check packages migrations tests scripts deploy/installers
uv run ruff check packages migrations tests scripts deploy/installers
uv run mypy packages tests deploy/installers
uv run pytest -m "not integration" -q
uv run python scripts/check_docs.py
uv run python scripts/check_release_status.py
uv run python scripts/check_deployment_dossiers.py
uv run python scripts/check_inference_artifacts.py
uv run python scripts/check_server_installers.py
```

The PostgreSQL integration suite requires an isolated database URL in
`NEXTOPS_TEST_DATABASE_URL`; the current suite contains six cases. CI is configured to run the same
suite against the deployed PostgreSQL 16.15 major/version and the future-compatibility PostgreSQL
17.6 image. Each container image is digest-pinned; a workflow definition is not a passing result.
The documentation checker covers local links, paired guide filenames, Persian RTL wrappers and
required control files. These checks do not contact equipment, apply a package bundle, fetch a
model, assess natural-language quality, or establish deployment acceptance.
