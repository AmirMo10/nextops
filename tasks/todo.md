# Tasks: guarded per-server package installers

## Task 1: specify the installer safety contract

**Acceptance criteria:**

- [x] Exactly one executable entry script exists for each approved server role.
- [x] Every role declares its minimum direct Ubuntu package set.
- [x] Package locks require exact Debian versions and include every declared package.
- [x] The complete offline bundle is authenticated by an operator-approved SHA-256.

## Task 2: implement offline, idempotent package installation

**Acceptance criteria:**

- [x] Check mode performs no package or service changes.
- [x] Apply mode requires root, Ubuntu 24.04, VMware, an authorization marker, and a change ID.
- [x] APT can read only the authenticated local repository and rejects unlisted package changes.
- [x] Package-managed service starts and automatic PostgreSQL main-cluster creation are blocked.
- [x] A repeated run converges on the same exact package versions.

## Task 3: give the deployer a usable handoff

**Acceptance criteria:**

- [x] English and Persian installation docs explain bundle layout, check/apply commands, and holds.
- [x] Every server dossier points to its installer without claiming that deployment occurred.
- [x] CI validates Python, wrapper syntax, executable modes, and repository layout.

## Task 4: verify and deliver

**Acceptance criteria:**

- [x] Focused tests, full non-integration tests, lint, formatting, types, and documentation checks pass.
- [x] Security and code-quality review find no unresolved high-risk issue.
- [ ] The change is committed, pushed, reviewed in a pull request, and merged to `main` only after gates pass.
