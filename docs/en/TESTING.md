# Testing, model evaluation and release evidence

[فارسی](../fa/TESTING.md) · [Index](INDEX.md)

**Status: application test plan. No application, device or G10 benchmark tests have run.** Source: master specification sections 10–14 and 21–23. Repository documentation checks are separate from application validation.

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

## Documentation checks available with this baseline

Run `python3 scripts/check_docs.py` after cloning. It checks local Markdown links, language-pair filenames, Persian RTL wrappers and required project-control files. It does not execute application tests, contact equipment, fetch links, validate technical claims or assess native-language quality. Its successful result must not be reported as a platform test pass.
