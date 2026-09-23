# Configuration contracts

[فارسی](../fa/CONFIGURATION.md) · [Index](INDEX.md)

**Status: partial runtime configuration is implemented; the complete file-based contract remains proposed.** Typed fail-closed environment loaders now cover the app/database/session boundary, local llama.cpp service boundary and read-only Zabbix connector boundary. The filenames below come from the master specification; illustrative values are documentation, not executable configuration files.

## Separation of concerns

| Planned file | Responsibility |
|---|---|
| `app.example.yaml` | Environment, language, storage locations, service identities, local endpoints and limits |
| `models.example.yaml` | Local model paths/revisions/checksums, capabilities, templates and CPU budgets |
| `inventory.example.yaml` | Stable asset IDs, types, environment, approved endpoints, tags and credential references |
| `credentials.example.yaml` | References to secret-manager entries; no secrets or decrypting keys |
| `policies.example.yaml` | Deny-by-default scopes, named diagnostics, risk, approval and execution limits |
| `resource-profiles.example.yaml` | Measured CPU/memory/thread/concurrency profiles and queue limits |

Any additional file-based implementation must introduce typed schemas, validation errors, configuration versioning and documented loading rules. Current supported environment variables are defined by `AppSettings`, `LlamaCppSettings` and `ConnectorSettings`; avoid inventing others in installation commands. `NEXTOPS_INCIDENT_LOOKBACK_MINUTES` controls the Phase 2 incident window, defaults to 60, and fails closed outside 15–1440 minutes. It is deployment configuration, not caller input. Application state belongs in PostgreSQL, not mutable YAML used as a job queue.

## Language and identity

Support `fa` and `en`, with Persian as the original default requirement. Store semantic values separately from labels. Use UTC internally and configurable local display time. Do not translate device IDs, interface names, command strings or protocol fields. Preserve original diagnostic text except explicitly marked secret redaction.

Each asset needs an immutable ID, environment/organization scope, type, owner/tags, approved address, observed capability/version facts, last verification time and a credential reference. Name resolution must detect ambiguous assets instead of selecting one silently. Inventory changes affecting an approved operation invalidate its target assumptions.

## Model registry

Providers resolve to local CPU services or files only. Record generation/embedding/reranking capabilities separately; configuration does not imply health. Missing artifacts, checksum mismatch, unsupported templates or dimensions fail clearly. Changing embedding dimensions/model requires a compatible index migration, not mixed vectors in one index.

Do not infer thread budgets from installed CPU count. Resource profiles remain unvalidated until measured on the actual host. Enforce one global budget across inference, embedding workers, jobs, the API and database. Production, staging and development have separate identities, inventories and data stores.

## Secrets and storage

Keep production settings outside the checkout, with restricted ownership. Proposed configurable paths include `/etc/nextops`, `/var/lib/nextops`, and `/srv/nextops/models`. Verify mounts and free space before use. `.env` can serve restricted local development but is not a production secret vault. Encryption recovery keys must not sit beside encrypted credentials.

A repository example may use a synthetic asset name and a credential reference; it must not contain a usable account, token, private IP inventory or production hostname. Do not put weights, logs, dump files or backup archives in Git.

## Change control

Policy and model changes need versioned audit records, validation and a rollback plan. Recheck permissions and pre-state immediately before execution. No model output may edit the policy that authorizes its own actions. Runtime configuration must reject external inference and keep all mutations disabled until the separately approved remediation phase.
