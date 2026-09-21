# Per-server deployment dossiers

[فارسی](../fa/DEPLOYMENT_DOSSIERS.md) · [Index](INDEX.md) · [Server plan](SERVER_PLAN.md) · [Storage gate](../STORAGE_PLAN.md)

For the exact first actions, provisioning order, read-only guest commands, and installation
holds, use the [server start checklist](SERVER_START_CHECKLIST.md) before opening a change.

**Status: deployer handoff contract, not an installer or deployment authorization.** The four human-readable YAML files under [`deploy/server-dependencies`](../../deploy/server-dependencies) collect the known sizing, proposed boundaries, dependencies, configuration paths, command templates, evidence requirements, and unresolved deployment inputs for the accepted initial profile. All runtime acceptance gates remain `not_run`.

## Files and ownership

| Server dossier | Responsibility | Resource proposal |
|---|---|---:|
| [`nextops-app.yaml`](../../deploy/server-dependencies/nextops-app.yaml) | Local TLS/UI/API, identity, durable worker/audit, and initial restricted NextOps PostgreSQL | 8 vCPU / 32 GiB / 200 GiB |
| [`nextops-ai.yaml`](../../deploy/server-dependencies/nextops-ai.yaml) | One isolated local CPU inference service and verified model/runtime artifacts | 24 vCPU / 128 GiB / 500 GiB |
| [`nextops-connectors-ro.yaml`](../../deploy/server-dependencies/nextops-connectors-ro.yaml) | Protected gateway and separately restricted read-only Zabbix runner | 4 vCPU / 8 GiB / 80 GiB |
| [`zabbix-server.yaml`](../../deploy/server-dependencies/zabbix-server.yaml) | Dedicated Zabbix 7.0 LTS proposal, PostgreSQL 16, frontend/API, Agent 2, and detailed LVM | 4 vCPU / 16 GiB / 200 GiB |
| [`server-dependency.schema.json`](../../deploy/server-dependencies/server-dependency.schema.json) | Version 1.0.0 public contract shared by every dossier | Not a server |

The combined proposal is 4 VMs, 40 vCPU, 184 GiB RAM, and 980 GiB of VMDKs. The provisional ESXi swap allowance is another 184 GiB, giving 1164 GiB before VMX, snapshots, thin growth, staging, maintenance, and restore space. These values are planning inputs, not reservations or proof of available resources.

## The deployer's first step

Create a **private deployment record outside this public repository**. Copy only the IDs from each dossier's `required_inputs` section, then resolve them with approved private evidence. Start with:

1. `authorization.*` — exact target, operator, operations, window, and rollback authority;
2. `vm.*` — current ESXi capacity/contention, VM compatibility, datastore health/free space, swap placement, and already-created VM reconciliation;
3. `artifact.*` — exact releases/packages/models, versions, signatures/checksums, licenses, and offline bundle paths;
4. `network.*` and `target.*` — private names/addresses, routes, ports, certificate trust, allowlists, Zabbix base path/version, and host-group scope;
5. `secrets.*` — reference-only delivery, consumer identity, rotation, revocation, redaction, and recovery;
6. `storage.*` and `recovery.*` — device/mount proof, growth/retention, independent backup, restore target, RPO/RTO, and last-known-good artifacts;
7. `acceptance.*` — approved quality, latency, load, failure, offline, and recovery cases.

Do not replace `null` with a convenient guess. Do not commit the completed private record, actual hostnames, addresses, datastore identifiers, tokens, passwords, certificate private keys, or backup endpoints.

## Command semantics

Every command entry has a mode:

| Mode | Meaning |
|---|---|
| `read_only` | A command that changes no intended system state, but still requires target authorization when it runs on infrastructure. Keep sensitive output private. |
| `guarded_template` | A reviewed pattern with named required inputs. Resolve and validate those inputs in the private record before an operator runs it. It is not an automatic script. |
| `blocked` | The repository does not yet have a safe exact command. `command` is deliberately `null`; the blocking inputs and failure rule explain what must exist first. |

Never build an executor that reads these YAML files and blindly runs the strings. The dossiers are handoff contracts for a reviewed change procedure. Re-resolve targets, permissions, mounts, artifacts, and authorization immediately before any state-changing step.

## Validation commands

Install the locked development dependencies, then run the repository validator:

```bash
uv sync --extra dev --frozen
uv run --extra dev python scripts/check_deployment_dossiers.py
```

The validator safely parses all four YAML documents, checks them against the Draft 2020-12 JSON Schema, rejects stale JSON dossier copies, verifies the approved server IDs, and reconciles the 40-vCPU / 184-GiB-RAM / 980-GiB-disk total.

Repository documentation validation:

```bash
python scripts/check_docs.py
```

A successful parse or schema check proves structure only. It does not verify private values, artifact authenticity, infrastructure capacity, service behavior, or authorization.

## Safe deployment workflow

1. **Reconcile reality.** Determine whether each VM or a suitable Zabbix instance already exists. Never subtract or create it twice. Refresh host and DS-C evidence at the approved change window.
2. **Close required inputs.** A server cannot advance while any input required for its next phase is `missing`, `pending_authorization`, or `not_run`.
3. **Lock artifacts.** Record immutable versions, checksums/signatures, licenses, transitive dependencies, build flags, and one compatible rollback set. Prepare a complete offline bundle with no production credentials.
4. **Write and test the exact runbook.** Convert only the selected profile and private inputs into environment-specific install/start/stop/backup/restore commands. First prove them in an isolated lab or clean restore target.
5. **Run read-only preflight.** Capture OS, kernel, CPU/memory, mounts, free space, time, listeners, certificates, and service conflicts. Stop on differences; do not normalize them away.
6. **Execute one server at a time.** Preserve the order `nextops-app` → `nextops-ai` → `nextops-connectors-ro`; finish Zabbix readiness before Stage 1C. Use dependency-based readiness, not fixed sleeps.
7. **Verify boundaries.** Only the app serves users; inference/database/gateway stay internal; only the isolated runner receives the Zabbix token; Zabbix PostgreSQL stays local; Internet runtime egress and all Phase 1 mutations are denied.
8. **Record acceptance evidence.** Attach sanitized command output, release IDs, timestamps, scopes, test results, failures/skips, resource measurements, and backup/restore references to the private change record. Change an acceptance gate from `not_run` only in the evidence system, not by editing a planning file without proof.
9. **Promote or roll back.** Promotion requires the dossier gates plus ZBX/OFF cases applicable to the milestone. Roll back on the listed triggers; reconcile unknown outcomes instead of retrying blindly.

## Server-specific stop conditions

### `nextops-app`

Stop before installation because the repository has no runnable API/UI, PostgreSQL migrations/roles, worker, installer, Compose stack, or systemd units yet. Stage 1A Increment 2 must supply and test these. Do not invent environment variables or expose PostgreSQL to compensate.

### `nextops-ai`

Stop before import/start until the llama.cpp commit/build flags, guest CPU ISA, model revision/quantization/template/license/checksums, resource profile, internal authentication, and bilingual evaluation targets are locked. The 24-vCPU/128-GiB VM is an experiment budget, not an inference thread count or performance promise.

### `nextops-connectors-ro`

Stop before target access until the gateway/runner implementation, MCP protocol lock, Zabbix endpoint/version/base path, certificate, host-group permissions, method/field allowlists, limits, and runner-only token delivery pass tests. Never give the model, app, gateway, browser, or logs the target token.

### `zabbix-server`

First check for a suitable authorized existing installation. For a new VM, stop before storage changes until the actual new empty 200-GiB guest disk is proven and destructive authority names that exact disk. Stop before database initialization unless `/var/lib/postgresql` is the intended 112-GiB LV mount. Exact package locks, secure database credential delivery, monitored workload, retention, backup, and restore procedures remain required.

## Required handoff evidence

For each server, the deployer returns a private record containing:

- dossier schema/version and Git commit;
- change/authorization ID, operator, target identity, start/end time, and exact operations;
- resolved input IDs with evidence references and classification;
- actual VM/OS/resource/storage/network values and differences from the proposal;
- artifact versions, checksums/signatures, licenses, and offline-bundle inventory;
- created service identities/permissions and secret-reference consumers—never secret values;
- exact commands/runbook revision and exit outcomes;
- service/readiness, security-boundary, offline, load, failure, backup, restore, and rollback results;
- remaining blockers, skipped/not-run cases, and the next approved step.

The repository remains the public contract. The private deployment record remains the source of truth for environment-specific values and operational evidence.
