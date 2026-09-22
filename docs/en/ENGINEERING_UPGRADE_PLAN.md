# Engineering, documentation, reliability, and security upgrade plan

[فارسی](../fa/ENGINEERING_UPGRADE_PLAN.md) · [Specification workflow](SPECIFICATION_WORKFLOW.md) · [Release status](../status/current-release.yaml)

**Status: active brownfield program.** This plan classifies candidates; it is not an installation
list or production-readiness claim. The current architecture and evidence in `PROJECT_STATE.md`
remain authoritative.

## Decisions from the baseline audit

| Area | Decision | Boundary |
|---|---|---|
| Specification-driven work | **Adopt now, lightweight** | Use the existing-project sequence from [Spec Kit](https://github.com/github/spec-kit) for bounded features. Do not run project regeneration or create a competing constitution/source of truth. Spec Kit is MIT-licensed. |
| Agent workflows | **Adopt project-local skills** | The planner, acceptance reviewer, and documentation reviewer are original NextOps instructions. No file was copied from the now-deprecated `openai/skills` catalog; that catalog requires license review per individual skill. Agents never receive unrestricted infrastructure credentials. |
| ADR format | **Adopt for future decisions** | Preserve ADRs 0001–0006. New decisions may use [MADR](https://github.com/adr/madr) headings plus explicit security, operations, and rollback sections. MADR is MIT/CC0 dual-licensed. |
| Release truth | **Adopt now** | `docs/status/current-release.yaml` is the validated sanitized capability/gate manifest. Human narrative remains in project state; historical reports are not rewritten. |
| Documentation portal | **Prototype, do not deploy yet** | [Docusaurus](https://github.com/facebook/docusaurus) is an MIT-licensed candidate with static output, i18n, RTL, and versioning. Markdown stays authoritative. Algolia is prohibited by the offline contract; Docusaurus local search is community-maintained and must be pinned, licensed, bundled, and tested offline before selection. |
| Diátaxis | **Migrate incrementally** | Add tutorials, how-to guides, reference, and explanation navigation without moving every existing file or erasing historical structure. |
| Documentation quality | **Pilot** | Add project Vale rules first for English terminology/readiness claims; Persian requires custom rules and human review. Keep `check_docs.py` as the offline local-link/parity gate. Pilot Lychee as a separate Internet-dependent external-link maintenance job. |
| PostgreSQL/file recovery | **Next implementation candidate** | Evaluate pgBackRest (MIT) for each PostgreSQL cluster and restic (BSD-2-Clause) for permitted non-database files. The accepted outcome is isolated restoration, not backup command success. See `BACKUP_RESTORE_SPEC.md`. |
| Browser/accessibility | **Playwright adopted; accessibility expansion pending** | Playwright 1.63 is locked for the fresh private-origin WAN-denied workflow. Add axe-core, server-side logout/revocation, expiry and broader accessibility cases. Provision browser binaries offline; automation does not replace manual review. |
| Failure/load/API/property tests | **Pilot behind specifications** | Use Toxiproxy only in isolated tests; Locust for bounded queue/load metrics; Schemathesis for OpenAPI shape; Hypothesis only for named invariants. None replaces authorization, real WAN isolation, or restoration. |
| AI evaluation | **Preserve deterministic Python first** | Extend the existing local Python corpus/harness. Adopt promptfoo only after proving local-only execution and no remote provider/telemetry path. |
| Supply-chain evidence | **Pilot** | Evaluate Syft for release SBOMs, Trivy only for filesystem/artifact coverage it adds, and Cosign with pre-provisioned offline verification trust. Do not add containers solely for scanning. |
| Workflow and secret security | **Adopt focused controls** | Keep Gitleaks. Zizmor 1.29.0 offline/pedantic review found checkout credential persistence; the workflow now disables it and has no remaining findings. Pin any future CI integration by immutable artifact identity. |
| ASVS | **Map selectively** | Create test traceability for applicable authentication, authorization, session, validation, API, secret, cryptography, logging, data, and file requirements. Never claim OWASP certification. |

## Preserve or defer

- Preserve the pinned CPU-only `llama.cpp` runtime and model; benchmark before change.
- Keep current orchestration and authorization boundaries. The official MCP Python SDK is a protocol
  candidate behind those interfaces, not an authorization layer. Do not adopt PydanticAI without a
  bounded prototype proving less complexity.
- Treat HolmesGPT and Keep as product research for investigations and future incident workflows;
  they are not runtime dependencies.
- Defer pgvector until bilingual relevance, CPU/storage cost, and authorization filtering are
  benchmarked. Never mix retrieved documents and live monitoring evidence without provenance.
- Compare `python-zabbix-utils` with the narrow existing connector; do not replace the working
  allowlisted client merely to use an SDK.
- Defer pyVmomi, Netmiko, and Ansible to separate read-only connector specifications. Any later
  mutation requires deterministic policy and explicit approval outside the model.
- Add OpenTelemetry only for a concrete local diagnostic question, with redaction and no hosted
  exporter. It does not replace security audit.
- Evaluate shadcn/ui and react-i18next only with a reviewed frontend migration. The current static
  panel remains supported until its replacement passes offline, RTL/LTR, accessibility, and rollback
  gates.

## Controlled phases

1. **Truth and governance — implemented in repository:** release manifest/validator, specification
   workflow, three project agent workflows, documentation drift correction, PostgreSQL 16/17 CI
   strategy, and Zizmor findings fixed. Hosted CI results remain revision-specific.
2. **Recovery:** ADR and isolated pgBackRest/restic lab; full/WAL/file backups; independent restore;
   measured RPO/RTO; bilingual operator runbooks.
3. **Browser and accessibility — fresh-browser path passed:** retain the Playwright WAN-denied
   harness; add server-side logout/revocation, axe coverage and an offline browser bundle.
4. **Failure and capacity — core Stage 1 cases passed:** cancellation, dependency/artifact/low-space
   and five-minute bounded load have evidence; Toxiproxy, Locust and schema/property expansion remain
   candidates for broader environments.
5. **Release and documentation supply chain:** Docusaurus offline prototype, local search, Vale,
   external-link maintenance, ASVS traceability, SBOM, vulnerability-data freshness, and offline
   signature verification.
6. **Future capabilities:** retrieval, topology, additional read-only connectors, incident
   correlation, observability, and only then a separately approved remediation design.

Each phase needs a bounded specification, tests, rollback, paired documentation, and an explicit
manifest update. A candidate moves from evaluation to adoption only after its licensing, offline
artifacts, security boundary, operational cost, and removal/rollback path are evidenced.
