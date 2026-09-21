# Implementation plan: per-server deployment dependency dossiers

## Overview

Add a versioned deployment-dossier contract, one self-contained JSON instance for each approved initial server, and paired deployer guidance. The deliverable records what is known, what is proposed, what remains private, and what blocks execution; it does not provision infrastructure.

## Architecture decisions

- JSON is the machine-readable format because it can be parsed with the Python standard library and matches the repository's existing hardware/allocation records.
- One shared JSON Schema defines the stable top-level contract, while every server instance remains self-contained for handoff.
- Commands are typed as read-only, guarded template, or blocked. A nonexistent installer is never replaced with a plausible shell command.
- Secret values and private infrastructure identifiers remain external references.

## Task list

### Phase 1: contract

- [x] Define the dossier specification and JSON Schema.
- [x] Validate the schema as JSON and review its required fields.

### Checkpoint: contract

- [x] Schema parses and represents commands, blockers, and secret references without executable secrets.

### Phase 2: server instances

- [x] Add the `nextops-app` and `nextops-ai` dossiers.
- [x] Add the `nextops-connectors-ro` and `zabbix-server` dossiers.
- [x] Reconcile resource and storage values with the accepted records.

### Checkpoint: instances

- [x] All four files parse and contain the required sections.
- [x] Known totals and Zabbix LVM values match source records.

### Phase 3: handoff and repository state

- [x] Add paired English/Persian deployer guidance and index links.
- [x] Update traceability, project state, and the next-task handoff.
- [x] Run documentation, implementation, lock, diff, and secret-review gates.

### Checkpoint: complete

- [x] Acceptance criteria in the dossier specification are met.
- [x] No infrastructure operation was performed or claimed.
- [ ] Changes are committed and published for review.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| A deployer treats a proposal as an approved command | High | Explicit authorization flags, command modes, and blocking inputs in every file |
| Sensitive values reach Git | High | Reference-only secret fields, null private values, staged-diff scan |
| Version-specific commands become stale | High | Pinning is a required input; installation remains blocked until a reviewed artifact lock exists |
| Four manifests drift | Medium | Shared schema, source links, consistent section names, cross-file review |
| Documentation is mistaken for acceptance | High | All runtime acceptance gates start as `not_run` and require evidence references |

## Open questions

The private deployment inputs and exact artifact locks listed in the specification remain intentionally unresolved and must be closed during an authorized deployment gate.
