# Spec: per-server deployment dependency dossiers

Status: approved by the owner's 2026-09-21 request to create a dependency file for each approved server. This specification authorizes repository documentation only. It does not authorize provisioning, installation, target access, network changes, or service restarts.

## Objective

Give a deployer one self-contained, machine-readable dossier for each approved initial server:

- `nextops-app`
- `nextops-ai`
- `nextops-connectors-ro`
- `zabbix-server`

Each dossier must distinguish owner-supplied facts, accepted architecture, engineering proposals, missing private inputs, and runtime evidence that has not yet been collected. It must identify dependencies, configuration files, service identities, network/storage boundaries, artifacts, secret references, command templates, verification, backup, rollback, and acceptance gates without storing credentials or pretending that undeveloped installers exist.

## Commands

Validate every dossier as JSON:

```bash
python -m json.tool deploy/server-dependencies/nextops-app.json > /dev/null
python -m json.tool deploy/server-dependencies/nextops-ai.json > /dev/null
python -m json.tool deploy/server-dependencies/nextops-connectors-ro.json > /dev/null
python -m json.tool deploy/server-dependencies/zabbix-server.json > /dev/null
```

Validate repository documentation and the existing implementation:

```bash
python scripts/check_docs.py
uv run --extra dev pytest
uv run --extra dev ruff check packages tests
uv run --extra dev mypy packages tests
git diff --check
```

The dossier command entries are either read-only commands that can be reviewed now, guarded templates that require named inputs and authorization, or explicitly blocked commands with a reason. A missing installer is represented as `null`, never as an invented command.

## Project structure

```text
deploy/server-dependencies/
  server-dependency.schema.json  # versioned public contract
  nextops-app.json               # app/API/UI/database host dossier
  nextops-ai.json                # local CPU inference host dossier
  nextops-connectors-ro.json     # protected read-only gateway/runner dossier
  zabbix-server.json             # dedicated monitoring host dossier
docs/en/DEPLOYMENT_DOSSIERS.md  # English deployer workflow
docs/fa/DEPLOYMENT_DOSSIERS.md  # Persian deployer workflow
```

## Data style

- Use stable `snake_case` field names and kebab-case server IDs.
- Use `null` for an unknown value and explain it in `required_inputs`; do not use a plausible guess.
- Give every command a stable ID, execution mode, required input IDs, expected result, and failure rule.
- Use repository-relative paths for source documents and absolute guest paths for runtime locations.
- Keep versions as constraints or explicit unresolved locks. Never use `latest`.
- Treat IP addresses, DNS names, certificates, tokens, passwords, private datastore identifiers, and backup endpoints as external inputs.

## Testing strategy

1. Parse every manifest with Python's standard JSON parser.
2. Check each instance against `server-dependency.schema.json` with a Draft 2020-12 validator when one is available in the controlled toolchain; the schema remains useful without adding a runtime dependency to NextOps.
3. Run the repository documentation checker for bilingual parity, UTF-8, RTL wrappers, and local links.
4. Review arithmetic and cross-file values against `HARDWARE_BASELINE.json` and `ZABBIX_SERVER_PLAN.json`.
5. Run the existing Stage 1A quality gates to prove this documentation change did not regress the implemented slice.

## Boundaries

Always:

- preserve the four approved resource profiles and DS-C alias;
- require offline-capable local artifacts and certificate validation;
- use reference-only secrets and least-privilege service identities;
- label every not-run acceptance check honestly;
- keep the model isolated from target credentials and the management LAN.

Ask first:

- actual provisioning, package installation, partitioning, firewall changes, certificate issuance, target access, reboots, or restore tests;
- selecting exact application, MCP, model, image, package, or OS patch versions;
- changing storage layouts, VM allocations, exposure, retention, or backup destinations.

Never:

- commit a real secret, private infrastructure identifier, production inventory, or usable endpoint;
- publish destructive storage commands for an unidentified disk;
- imply that documentation, a VM definition, or a successful JSON parse is deployment acceptance;
- silently download dependencies or route AI work to an external provider at runtime.

## Success criteria

- Four self-contained JSON dossiers validate as JSON and against one versioned schema.
- Every dossier contains resource, dependency, configuration, identity, network, storage, artifact, secret-reference, command, verification, backup/rollback, required-input, and acceptance sections.
- Exact known values match the accepted Phase 0 records.
- Unknown private or not-yet-implemented values are explicit blockers rather than fabricated defaults.
- English and Persian deployer guides explain the safe execution order and evidence record.
- Repository documentation and Stage 1A checks remain green.

## Open questions intentionally left for the deployment gate

- Private addressing, DNS, VLAN/firewall rules, local time sources, certificate authorities, and administrative recovery paths.
- Actual ESXi free capacity, contention, VM compatibility, datastore health, swap placement, and backup destination at the change window.
- Exact release artifacts, container/native deployment choice, systemd/Compose definitions, package/image/model locks, checksums, and licenses.
- Application database layout, model/runtime build and quantization, connector protocol/transport limits, and Zabbix frontend/API version and base path.
