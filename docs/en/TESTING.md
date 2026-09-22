# Testing, model evaluation and release evidence

[فارسی](../fa/TESTING.md) · [Index](INDEX.md)

**Status: active test plan with repository, isolated PostgreSQL, live connector and bounded local-AI
evidence.** Ruff, strict mypy, 101 non-integration cases and six PostgreSQL integration cases pass.
Authenticated browser-path, live read-only Zabbix, durable investigation, revoked-token,
unreachable-API and recovery checks have run on the controlled four-guest environment. Explicit
WAN-disconnection, VM reboot, sustained load, independent restore and production acceptance have
not run. Source: master specification sections 10–14 and 21–23.

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

These results qualify the named cases only. They do not replace the remaining WAN, reboot,
certificate-expiry, timeout/cancellation, low-space, sustained-load, backup and restore matrix.

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
uv run python scripts/check_deployment_dossiers.py
uv run python scripts/check_inference_artifacts.py
uv run python scripts/check_server_installers.py
```

The PostgreSQL integration suite requires an isolated database URL in
`NEXTOPS_TEST_DATABASE_URL`; the current suite contains six cases.
The documentation checker covers local links, paired guide filenames, Persian RTL wrappers and
required control files. These checks do not contact equipment, apply a package bundle, fetch a
model, assess natural-language quality, or establish deployment acceptance.
