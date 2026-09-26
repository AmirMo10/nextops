# Mandatory offline operation and local AI

[فارسی](../fa/OFFLINE_RUNTIME.md) · [Index](INDEX.md) · [Technology stack](TECH_STACK.md) · [CPU-only AI](CPU_AI.md)

**Requirement confirmed by the owner: 2026-09-20. Current status: controlled Stage 1 acceptance, not production acceptance.** Four-guest WAN isolation, a fresh WAN-denied browser, server/API requests, serial clean reboots, artifact rollback, failure recovery, sustained bounded load and logical isolated restore passed. Independent backup, WAL/PITR and disaster recovery remain open. See the [release manifest](../status/current-release.yaml), [test evidence](TESTING.md) and [Stage 1 report](STAGE_1_COMPLETION_REPORT.md).

The four-guest WAN-denial results are controlled tests with a temporary egress policy, not a claim
that host-wide egress is permanently blocked. As checked on 2026-09-26, administrator shells on all
four guests can reach public IPv4. App/AI/model service units retain loopback-only IP restrictions,
and the connector process is limited to the approved LAN. The permanent host-wide egress gate
remains partial. Offline ability and permanent egress
enforcement are separate claims.

## 1. The operating contract

After approved provisioning, NextOps must continue answering questions in Persian and English when the server loses all Internet access. It must also start again from stopped services or a reboot while Internet access remains unavailable. An already-open browser session, a model left in RAM, or files cached under a developer's account is not sufficient evidence.

**Local CPU inference is the normal operating path, whether Internet access exists or not.** Do not implement a cloud-first path that switches to a local model only after a timeout. Generation, planning, embeddings, optional reranking and model-based evaluations must use local CPUs. There is no external AI fallback.

This clarification applies to every proposed technology and diagram. It strengthens original requirements 25–27 and the enhanced master specification's CPU/offline requirements. The archived master prompt remains unchanged; its original appendix's cloud-provider example does not authorize cloud AI in this deployment.

Offline operation does not imply limitless availability: the host, storage, installed artifacts and required local services must remain healthy. CPU capacity and answer quality require measurement; no throughput or response-time result is asserted here.

## 2. Three different network conditions

| Condition | Required behavior |
|---|---|
| Internet unavailable; management LAN and user-to-server route available | Login, new questions, local generation, local knowledge, history and audit continue. Approved LAN connectors can collect fresh evidence. |
| Internet and managed-device LAN unavailable; authorized local console/loopback access available | Local general Q&A and locally stored authorized knowledge/history remain usable. Device collection reports unavailable; past measurements are explicitly stale. Do not block local Q&A on an unreachable connector or LAN identity provider. |
| User has no network path to the server | A remote browser cannot reach this server. Provide a documented authorized local-access procedure; do not describe server-side inference as disconnected browser-side inference. |

Do not automatically give the model management-network access. The model remains isolated; only authenticated, policy-controlled connector runners reach approved devices.

## 3. What the AI can answer without Internet

The answer must identify its basis without exposing private internal reasoning:

- **Model knowledge:** general technical explanations drawn from the installed model. Say when a statement has not been checked against local documentation or current device state. Do not fabricate citations.
- **Local knowledge:** approved runbooks, manuals, topology records and earlier incidents retrieved from local storage. Cite the actual source/version and distinguish document age from current evidence.
- **Fresh local evidence:** successful authorized LAN tool results, with collection timestamps and target scope. A disconnected Internet connection does not make a reachable LAN result unavailable.

New arbitrary questions must reach actual local generation, not a cache of predefined answers. Persian, English and mixed technical identifiers must be evaluated. Missing evidence must produce an explicit limitation or a safe next diagnostic step, not an invented device state.

Requests for new Internet information cannot be verified online during the outage. The model may explain what it knows, but must not claim to have browsed, obtained current vendor advisories or checked live public services. Local documents can be updated through reviewed offline imports; offline does not mean permanently frozen knowledge.

## 4. Eliminate hidden runtime dependencies

| Area | Required implementation |
|---|---|
| Model loading | Verified local weights, tokenizer, configuration, templates and any required auxiliary files. No runtime model-name resolution, downloads, external model registry or accelerator requirement. |
| Embeddings/retrieval | Local CPU encoder when enabled; persistent local indexes and documents. Ingestion and re-indexing must also work offline. Avoid remote OCR/reranking/document-processing dependencies if those features are introduced. |
| UI and API documentation | Serve JavaScript, CSS, translations, icons and permitted font assets locally. No CDN, hosted analytics or web-font call. Self-host enabled API documentation assets or disable that UI explicitly; FastAPI documents the self-hosting route [2]. |
| Identity | An explicitly provisioned local authentication path with scoped roles, local session validation, revocation and audited recovery. No mandatory GitHub/Google login, Internet token introspection, online CAPTCHA, email/SMS code or cloud activation. LAN SSO may be optional, but its loss cannot silently grant privileges. |
| Secrets | Local protected key access for core services. Optional LAN secret stores must have documented availability boundaries; their loss disables affected connectors rather than preventing general local Q&A. No fallback to plaintext secrets. |
| Names, clocks and TLS | Local service discovery; approved LAN DNS or a reviewed static mapping where needed. Plan trusted local time and certificate renewal/revocation for the outage horizon. Do not depend solely on public DNS, public NTP or an Internet certificate renewal endpoint. Do not disable certificate validation or extend expired sessions to make a test pass. |
| Data and observability | Local database, durable jobs, evidence, audit and required monitoring. No mandatory SaaS logging/tracing/storage/license heartbeat. Local diagnostics must remain usable when optional exports fail. |
| Releases and GitHub | GitHub is a development/release source, never a boot, login, inference or health dependency. Runtime must not execute `git pull`, package installs, image pulls or online update checks. |
| Alerts and backups | The local incident console is primary. Internet email, Telegram or cloud backup cannot be the only operational path. Off-host backup can use an approved reachable LAN destination; local staging is not disaster recovery. |

For a Hugging Face-based local embedding component, set the applicable offline and telemetry controls before importing its libraries: `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1`. The Hub documentation states that offline mode skips Hub HTTP calls and fails when required cached files are absent [1]. Still require verified explicit local artifacts and network enforcement: these settings are not a process-wide firewall and do not configure llama.cpp.

For a future Compose deployment, use imported pinned images with a tested no-pull runtime policy. Docker documents `pull_policy: never`, which uses local images and fails if they are absent [3]. Verify this with the pinned Compose version; a lockfile alone is not an offline installation bundle.

## 5. Provisioning, restart and maintenance

Controlled online provisioning or import from a separate connected workstation must prepare an inventory of all required artifacts: application release, native libraries or container images, Python dependencies, built frontend, model assets, connector drivers, migrations, local knowledge and verification material. Include versions, licenses and checksums; keep credentials and private inventories out of the public repository and general release bundle.

Install required artifacts under durable, service-owned paths, not an incidental interactive-user cache. Preflight checks identify missing or corrupt files before promotion. Recreating a service uses the already installed release; it must not rebuild from Internet package repositories. Container-only and systemd release profiles each need a complete tested procedure.

Prepare protected local administrator access, key-unlock/recovery procedures and certificate lifecycle before disconnecting. Do not wait for an Internet outage to discover that decrypting storage or signing in requires an unavailable service.

During an outage, updates are explicit, reviewed artifact imports. Verify integrity/authenticity through provisioned trust material, preserve backups and compatibility rules, and test rollback offline. Internet reconnection must not trigger automatic downloads, external AI routing, queued prompt/evidence uploads or infrastructure mutations.

## 6. Offline acceptance suite

Run only in an authorized isolated lab or approved maintenance window with a recovery path. Do not change production firewall rules or reboot the G10 as part of writing these documents.

Block external access for both the server workload and the test browser while allowing required loopback and explicitly approved LAN routes. Cover IPv4/IPv6 and any configured proxy/tunnel paths. Merely breaking public DNS is not an adequate test. Record process-scoped network attempts as well as successful connections; a blocked unwanted request is still a dependency/privacy defect.

The table below remains the normative acceptance suite. Current outcomes are recorded in the release manifest and test evidence: the server/API portions of OFF-01 and OFF-05 pass, the reboot/startup evidence covers a bounded part of OFF-02, and OFF-03 remains partial because the browser process was not independently WAN-isolated. All other unrecorded portions remain `not_run`. Define numeric sustained-test targets before execution and report samples rather than inferred performance.

| ID | Scenario | Required evidence |
|---|---|---|
| OFF-01 | Remove Internet while services are running | New Persian/English questions complete through the local CPU model; no fallback, external call or public-DNS wait. |
| OFF-02 | Start model/worker/API from stopped state; separately test an authorized reboot without Internet | Complete startup from durable installed artifacts, including CPU inference. Document any intended local key-unlock step; no developer home cache or online fetch. |
| OFF-03 | Fresh browser profile and new local login, then session renewal | UI assets, translations, authorization and permitted session renewal work without cached login, CDN access or disabled security. Revoked sessions remain denied. |
| OFF-04 | Load a new approved local document and ask a grounded question | Local ingestion/retrieval works; enabled embedding/reranking uses CPU. Source citation points to the imported document, not invented evidence. |
| OFF-05 | Run the read-only Linux/Zabbix lab investigation with WAN blocked | Fresh authorized LAN evidence, bounded tool calls, evidence-linked answer and durable audit. |
| OFF-06 | Remove managed-device LAN reachability too, retaining authorized local console access | General local Q&A and stored knowledge remain available. Tool failures are bounded and labeled; no fabricated live state. |
| OFF-07 | In an isolated copy, omit or corrupt a required model/tokenizer artifact | Explicit failed AI readiness and useful operator error. No download, cloud fallback, fake AI answer or corruption of existing data. Other safe functions report their actual readiness. |
| OFF-08 | Ask for Internet-only current information or introduce a hosted-only integration | Explain unavailable verification. The optional integration cannot block local answers or cause scope/security bypass. |
| OFF-09 | Restart during durable work, simulate session/certificate expiry, and perform offline restore | Recover workflow state without replaying uncertain mutations; enforce expiry; use approved local recovery; restore is actually tested. |
| OFF-10 | Sustained mixed workload, followed by Internet reconnection | Record latency/resource use and the agreed test duration. No successful or attempted prohibited external request, accumulated export backlog, silent provider switch or automatic update. |

Zero prohibited requests and all defined functional/security cases passing are release gates for the tested profile—not proof of immunity to every future failure. A hardware benchmark, a blocked-network setting or this checklist alone is not an offline acceptance result.

## 7. Implementation and traceability

Phase 0 must map every runtime dependency to `local`, `approved LAN` or `provisioning only`, including frontend calls, model artifacts, auth, keys, time and certificates. Reject Internet-required components for the offline runtime. Preserve the master prompt and update paired guides together.

Phase 1 establishes local authentication, durable state, CPU loading and the first read-only Zabbix investigation with actual bilingual local generation while Internet is blocked. Phase 2 adds direct Linux enrichment and broader history/event diagnostics. Later enabled components must pass the relevant offline cases before release. Production qualification includes offline restart, restore and sustained tests, with security approvals unchanged.

Original requirements 3, 25–27, 29–30, 35–39 and 48 are relevant; enhanced sections 2, 9, 17–21 and 22 govern the CPU, deployment and testing baseline. The existing [traceability matrix](../requirements/TRACEABILITY.md) remains in place. This document adds test identifiers rather than silently rewriting archived requirements.

## References and validation status

The owner clarification defines the requirement. The primary references below support only the named implementation details; they do not verify NextOps's behavior. Consulted 2026-09-20. No server inspection, package installation, model run, network isolation test or reboot has been performed for this documentation update.

[1]: https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables
[2]: https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/
[3]: https://docs.docker.com/reference/compose-file/services/#pull_policy
