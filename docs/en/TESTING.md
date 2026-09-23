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

## Phase 2 current qualification — 2026-09-23

Phase 2 connector release `nextops-0.1.0-e2dad3a` and current application release
`nextops-0.1.0-54c8bb4` passed the source quality/unit job, PostgreSQL 16 and 17 integration jobs,
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
