# Tasks: per-server deployment dependency dossiers

## Task 1: define the dossier contract

**Acceptance criteria:**

- [x] A versioned JSON Schema requires the deployer-facing top-level sections.
- [x] The specification defines commands, boundaries, verification, and success criteria.

**Verification:** parse the schema with `python -m json.tool` and inspect required fields.

**Dependencies:** none.

**Files:** `docs/requirements/SERVER_DEPENDENCY_DOSSIER_SPEC.md`, `deploy/server-dependencies/server-dependency.schema.json`.

## Task 2: add the four server dossiers

**Acceptance criteria:**

- [x] Each approved server has one self-contained YAML file.
- [x] Known values match the accepted plans and all missing/private values are explicit.
- [x] Commands are classified and no usable secret is present.

**Verification:** parse all four files, validate them against the schema, and reconcile resource/LVM values.

**Dependencies:** Task 1.

**Files:** four YAML files under `deploy/server-dependencies/`.

## Task 3: publish the deployer handoff

**Acceptance criteria:**

- [x] Paired English/Persian guides explain execution order, gates, rollback, and evidence.
- [x] Index, traceability, project state, and next-task references are current.
- [x] Repository quality and secret-review gates pass.

**Verification:** run the commands in the specification and review the staged diff.

**Dependencies:** Task 2.

**Files:** paired guides plus focused repository-control updates.
