# Suggested technology stack

[فارسی](../fa/TECH_STACK.md) · [Index](INDEX.md) · [Diagram atlas](DIAGRAMS.md) · [CPU evaluation](CPU_AI.md)

> **Architecture recommendation with one implemented foundation slice.** Python 3.12, `uv`, Pydantic, Ruff, mypy and pytest are now declared and locked for Stage 1A contracts/policy. The remaining API, database, frontend, connector, inference and deployment choices below are not installed product services. No model or performance result has been validated on the G10.

## Recommended starting combination

**React + TypeScript + Vite → FastAPI + Pydantic → PostgreSQL + SQLAlchemy + Alembic**, with a bounded durable worker, an independently protected **MCP gateway**, and one local **llama.cpp CPU inference service**.

Build a modular application, not a service per library. The API and worker share domain code; the gateway and connector runners are separated to protect credentials. The browser receives static frontend assets from the reverse proxy. There is no requirement for a production Node.js application server or an external AI provider.

## 1. Core stack and ownership

Except for the locked Python contract/quality tooling noted above, entries remain proposed. “Core” means part of the initial implementation target, not a deployed service. Linked documentation establishes library capabilities, not measured suitability for this server.

| Layer | Suggested choice | Purpose in NextOps | Important constraint |
|---|---|---|---|
| Host | Ubuntu 24.04 LTS baseline | Initial single-host environment | Confirm installed OS, support and owner approval; do not reinstall a working host. |
| Python | Python 3.12 baseline + `uv` | Backend and connector environment; reproducible lock/sync [1] | Lock the interpreter and dependencies after compatibility checks. |
| API/contracts | FastAPI + Pydantic + Uvicorn | Versioned HTTP API, typed validation and OpenAPI [2] | Validation is not authorization; CPU inference runs outside API workers. |
| Persistence | PostgreSQL + SQLAlchemy + Alembic | Authoritative state, transactions and migrations [3] | Separate service roles; no shared superuser; use real PostgreSQL in integration tests. |
| Durable work | PostgreSQL-backed jobs + bounded Python workers | Leases, checkpoints, outbox and reconciliation | Application design, not a ready-made exactly-once guarantee. No web-process-only background jobs. |
| Generation | Pinned CPU build of `llama.cpp` / `llama-server` | Local quantized generation [4] | Disable accelerator backends/offload; verify CPU execution; no Internet fallback. |
| Tool protocol | Official MCP Python SDK | Actual protocol lifecycle, tools and transports [5] | Pin the SDK/protocol pair; policy remains trusted application code. |
| Web app | React + TypeScript + Vite | Typed operational UI and static production bundle [6] | Build with a compatible supported Node.js release; do not expose the Vite development server in production. |
| UI system | Tailwind CSS + reviewed shadcn/ui components | Shared tokens, forms, tables, dialogs and RTL-aware components [7] | Review copied components; keyboard, contrast and Persian usability still require tests. |
| Language | i18next + react-i18next | Local Persian/English dictionaries [8] | Bundle translations locally; no hosted translation dependency. |
| API state | TanStack Query | Query lifecycle, caching and invalidation [9] | Scope cache keys; clear on logout/scope changes; never trust cached approval state. |
| Edge and deployment | Nginx + Docker Compose; documented systemd alternative | TLS ingress and explicit processes/networks [10] | One failure domain; internal-only database/model/MCP; no Docker socket in the application. |
| Evidence storage | Restricted local filesystem + PostgreSQL metadata | Content hashes, provenance and permission-scoped retrieval | Redact before model exposure; controlled retention and off-host recovery. |
| Quality tooling | Ruff, mypy, pytest, HTTPX; Vitest and Playwright | Formatting/types, backend contracts and browser tests [11] | Simulator tests are not device validation; document failed/skipped/unrun tests. |

The original baseline selected Python/FastAPI, PostgreSQL, React/Vite, local CPU inference and MCP. Stage 1A now adopts `uv`, Pydantic, Ruff, mypy and pytest for the local contract/policy slice; FastAPI and the remaining UI, database, MCP and inference dependencies still require their own reviewed increments.

## 2. Visual and interaction stack

Use a small design system before building many screens. Define semantic tokens for spacing, typography, surfaces, focus rings and states: healthy, warning, critical, stale, denied, pending approval, overloaded and unknown outcome. Do not rely on color alone.

The proposed combination is **Tailwind CSS + shadcn/ui + react-i18next**. shadcn/ui documents RTL support [7], but translating labels does not automatically mirror layout correctly. Test navigation, dialogs, menus, tables and keyboard focus in both directions. Keep IP addresses, commands, file paths and model identifiers LTR-isolated. Treat localized dates as display values; store UTC timestamps.

Use TanStack Query for server state, not as a second authorization engine. SSE updates refresh run views through the authenticated API. Use React component state for local interface state before adding another global state library. Design explicit empty, loading, stale, partial, offline and denied states.

**Optional after the topology API exists:** React Flow for interactive asset/dependency views [12]. Render only authorized nodes; start with filtered incident-sized subgraphs, a read-only canvas and a keyboard-accessible table alternative. It is a UI renderer, not the topology database. Do not turn every asset into a continuously animated graph.

All frontend assets must be locally served at runtime. Font licensing and distribution are separate implementation checks. No CDN fonts, hosted icons, analytics or external translation calls are required by this recommendation.

## 3. CPU AI profile

| Workload | Starting approach | Promotion gate |
|---|---|---|
| Parsing, permissions, scheduling and runbooks | Deterministic typed Python | Unit, policy and adversarial tests |
| Main language generation | One quantized multilingual candidate around 7–9B parameters through local llama.cpp | Persian/English task quality, tool arguments, time to first token, total latency and memory |
| Lightweight triage | Compare a smaller local model with deterministic classification | Measurable benefit over the simpler baseline |
| Higher-quality synthesis | Evaluate a roughly 14B candidate after the baseline | Quality gain justifies measured latency; not selected because RAM is available |
| Retrieval embeddings | One benchmarked multilingual CPU encoder, when retrieval needs it | Persian recall, offline loading, dimensions/versioning and CPU cost |
| Reranking | Disabled initially | Demonstrated retrieval benefit within the shared resource budget |

The existing `Qwen3-8B` and `Qwen3-Embedding-0.6B` examples remain **evaluation candidates from the specification**, not claims that they are the latest or best models. Model licenses, revisions, quantization, tokenizer/templates and checksums must be reviewed separately.

Begin with one generation service and one active request. Measure queue delay, prompt processing, generation, p50/p95 end-to-end latency, cancellation and pressure under mixed work. Set global CPU/thread limits; do not multiply a 90-thread pool across workers. Prefer explicit overload and deferred batch work to an unbounded queue. See [CPU-only AI](CPU_AI.md).

## 4. Add only when the relevant feature needs it

| Optional component | Add when | Keep out of the initial default because |
|---|---|---|
| pgvector | Scoped semantic retrieval is justified by bilingual evaluation [13] | Lexical retrieval and reliable evidence provenance come first; vector search does not implement authorization. |
| Prometheus + Grafana | The first operational slice needs local dashboards and alerts | They observe NextOps; they do not replace security audit or prove connector compatibility. |
| OpenTelemetry SDK/Collector | Cross-process tracing answers a concrete operational question [14] | Collect only required signals; redact content and keep export local. |
| Redis | Measured caching/rate-limit contention requires it | PostgreSQL already owns jobs and approvals; Redis must not become a second authority. |
| React Flow | A reviewed topology feature and bounded graph endpoint exist | Avoid a visualization dependency before the underlying evidence model is useful. |
| External secrets-manager adapter | An approved on-premises secret service is available | MVP still needs protected credentials and key recovery; never substitute plaintext `.env` storage in production. |

These are feature-gated options, not optional security. Authentication, scoped authorization, audit, approved-target checks, TLS/SSH verification and deny-by-default execution are foundations.

## 5. Alternatives and explicit non-goals

| Alternative | Decision for this deployment |
|---|---|
| Next.js instead of Vite | Revisit only for a demonstrated SSR/server-rendering requirement; keep one backend authority now. |
| Ollama / OpenVINO CPU / vLLM CPU instead of llama.cpp | Benchmark a replacement only after checking CPU ISA, models, templates and operating cost; never deploy all runtimes by default. |
| Celery, Temporal or another workflow framework | Revisit for demonstrated workflow complexity or scale; document recovery/approval migration before changing engines. |
| SQLite or MySQL as NextOps's internal database | Deferred parity work; managed MySQL/MariaDB remains an integration requirement. |
| Kubernetes, Kafka, service mesh or separate graph/vector services | No initial requirement has been established; require a new ADR and measured need. |
| Cloud AI / remote GPU services | Not permitted for this deployment, even as a fallback. |
| Foundation-model training | Not an MVP requirement. Invest first in evidence, retrieval, tool contracts and evaluation. |

## 6. Locking, packaging and adoption order

After Phase 0 approval, choose supported compatible versions rather than copying whatever an install command calls `latest`. Commit a backend lockfile and one frontend lockfile; record Node/Python versions, CPU runtime commit/build flags, container digests and model manifests. `uv` supports lock/sync workflows [1]; it does not eliminate offline artifact preparation.

First implement typed domain/policy contracts and denial tests. Next add PostgreSQL migrations, durable state and audit, followed by the local CPU benchmark and read-only Linux/Zabbix slice. Add UI components against reviewed API contracts, then retrieval/topology and optional observability as needed. Full sequencing remains in the [roadmap](ROADMAP.md).

Release artifacts need dependency inventories, licenses and checksums. Prepare model files, wheels/images, frontend assets, local API documentation assets and browser-test binaries in controlled provisioning. Missing runtime artifacts must fail preflight instead of downloading silently. Development tools are not automatically production dependencies.

## Official references

Reviewed 2026-09-20. These document capabilities, not G10 benchmarks or a compatibility lock. Model examples are inherited from the project specification.

[1]: https://docs.astral.sh/uv/concepts/projects/sync/
[2]: https://fastapi.tiangolo.com/features/
[3]: https://docs.sqlalchemy.org/en/20/intro.html
[4]: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
[5]: https://modelcontextprotocol.io/docs/sdk
[6]: https://vite.dev/guide/
[7]: https://ui.shadcn.com/docs/rtl
[8]: https://react.i18next.com/
[9]: https://tanstack.com/query/latest/docs/framework/react/overview
[10]: https://docs.docker.com/compose/intro/compose-application-model/
[11]: https://playwright.dev/docs/intro
[12]: https://reactflow.dev/learn
[13]: https://github.com/pgvector/pgvector
[14]: https://opentelemetry.io/docs/what-is-opentelemetry/
