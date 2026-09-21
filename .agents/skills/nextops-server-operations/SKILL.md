---
name: nextops-server-operations
description: Plan, review, or perform authorized NextOps server preflight, provisioning, offline package-layer installation, deployment, recovery, ESXi, storage, AI, connector, or Zabbix work.
---

# NextOps server operations

Load `nextops-project-context` first, then read the server and deployment routes in
`docs/MARKDOWN_CONTEXT_INDEX.md`.

## Required operator context

Read the matching server dossier plus:

- `docs/en/SERVER_START_CHECKLIST.md` or its Persian pair;
- `docs/en/DEPLOYMENT_DOSSIERS.md` or its Persian pair;
- `deploy/installers/README.md` for package-layer work;
- `docs/STORAGE_PLAN.md`, `docs/en/OFFLINE_RUNTIME.md`, and the relevant server/Zabbix guide;
- `docs/requirements/HARDWARE_BASELINE.json` and the private approved change record when the
  operation depends on live infrastructure facts.

## Operational boundaries

- Treat repository sizes and layouts as proposals until current private preflight confirms them.
- Never expose a real address, datastore identifier, credential, token, certificate key, or raw
  infrastructure inventory in Git or a model prompt.
- Package `--check` authenticates a complete role bundle without applying it. Package `--apply`
  requires the separate authorization, change ID, platform checks, and secure ownership defined by
  the installer guide.
- The package scripts do not deploy NextOps, initialize databases, configure or start services,
  import a model, or establish server readiness.
- Stop on missing authorization, unresolved dossier input, stale capacity evidence, unexpected
  listeners or mounts, checksum/signature mismatch, or unavailable rollback/recovery access.

Record sanitized evidence, exact commands, versions, failures, skips, and rollback outcome in the
approved private change record. Update repository state only for evidence that is safe and actually
observed.
