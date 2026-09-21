# Development, GitHub and release workflow

[فارسی](../fa/DEVELOPMENT.md) · [Index](INDEX.md)

**Status: development policy. Application CI and deployment automation are not configured in this baseline.** Source: master specification sections 4, 7–8 and 21–26.

## Inspect before implementation

Read [AGENTS.md](../../AGENTS.md), the master specification, project state and next task. Inspect Git status, instructions, tracked files, manifests, locks, tests, migrations and deployment definitions. Preserve dirty changes and existing implementations. Review scripts before running them in an isolated environment without production credentials. Do not use destructive reset/clean, overwrite work or rewrite history.

Application work has begun with the tested Stage 1A typed-contract and deterministic-policy slice. It is not yet a runnable API, UI, database, connector, or AI service; do not treat its unit pass as a deployed application pass. Phase 0 architecture was accepted on 2026-09-21, while hardware discovery and every infrastructure authorization remain separate gates.

For the current Python slice, install the generated lock with `uv sync --extra dev --frozen`, then run `uv run --extra dev ruff check packages tests`, `uv run --extra dev mypy packages tests`, and `uv run --extra dev pytest`. Regenerate `uv.lock` only with reviewed dependency changes; run `uv audit --frozen` before release work.

## Module discipline

Keep domain invariants independent from framework I/O; application use cases depend on ports, infrastructure implements them. Define typed contracts across API, workflow, policy, gateway and connector boundaries. Python uses type hints, clear docstrings and handled exceptions; avoid duplicated logic and giant agent/utility files. English code identifiers remain stable; user-facing documentation and product strings support Persian and English.

Create source directories, manifests and locks when the corresponding implementation begins, not as misleading placeholders. Unsupported behavior must fail explicitly rather than return simulated success in production paths.

## Reviewable GitHub delivery

Use short-lived branches, small commits, clear acceptance criteria and pull requests. Link each feature to an original requirement and phase. Update both language guides, project state, next task and traceability with each delivered increment. CODEOWNERS and templates support review; they do not prove branch protection is enabled. Protected main and review rules must be explicitly configured and verified when available.

Future CI covers formatting/lint/types, unit and protocol/contract/security tests, real PostgreSQL integration tests, frontend build/browser tests, secret scanning, dependency checks and release manifests. Pin reviewed actions by commit SHA and use minimal workflow permissions. These are requirements, not claims of an existing green pipeline.

Untrusted pull-request code must run in disposable isolated workers with no production secrets or management-LAN access. Never attach a privileged persistent G10 runner to arbitrary PR execution. Do not execute an untrusted checkout under `pull_request_target` with secrets. Trusted hardware tests need a separate authorized and resource-limited workflow.

## Release and deployment

Tag verified releases and record application, dependency, container and model identities plus checksums and software/model bills of materials. The owner explicitly promotes a verified release; a push must not automatically deploy production. The host may pull approved artifacts through an outbound route without public SSH exposure.

Before deployment, verify artifact identity, configuration compatibility, backup state, serialized migrations and resource/port preflight. After deployment, verify health and expected behavior. Application rollback does not reverse a database migration; document schema compatibility or a tested restoration path. Offline bundles are explicit release artifacts, not runtime downloads.

## Multi-agent coordination and done

Parallel work is useful only for bounded independent tasks. The principal architect owns contracts; security reviews execution/credentials/approval; CPU/SRE reviews resources and operations; product/UX reviews native Persian and complete user flows. Use separate branches/worktrees when applicable. Do not let agents concurrently rewrite migrations, shared contracts or locks. No claim of parallel agents is permitted when tools did not run them.

An increment is complete only with functional code, boundary tests, recorded commands/results, security review, bilingual documentation, traceability and a meaningful commit. A mock is not a device test. Failed tests must be fixed or accurately reported, not weakened to make a check green.
