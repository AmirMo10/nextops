# Implementation plan: Stage 1B Increment 3 local CPU inference foundation

## Outcome

Deliver the repository-only foundation for one authenticated, CPU-only inference service:
a reviewed runtime/model candidate manifest, strict `LLMProvider` contracts, a bounded
single-active-request scheduler, a loopback-only llama.cpp provider adapter, a minimal
service API, and tests. Do not download model weights, build a runtime, provision a VM,
open a listener on infrastructure, or claim offline/model acceptance in this increment.

## Source-backed decisions

- Pin llama.cpp source tag `v0.4.1` and commit
  `b29c606e28a01b1bc8c1351026a0fa6e616bf6c4`; an authorized CPU build must later
  record compiler, flags, native libraries, binary SHA-256, and startup device evidence.
- Select the official Qwen evaluation artifact `Qwen3-8B-Q4_K_M.gguf` from repository
  revision `7c41481f57cb95916b40956ab2f0b139b296d974`, size 5,027,783,488 bytes,
  SHA-256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`,
  Apache-2.0. Selection permits controlled evaluation only; it is not import approval.
- llama.cpp remains behind a NextOps wrapper on loopback. The wrapper uses its documented
  OpenAI-compatible chat route and API-key support, while enforcing stricter NextOps
  limits and service authentication.
- Disable llama.cpp tools, agent/MCP, Web UI, external model resolution, context shifting,
  and accelerator offload. The model boundary receives no infrastructure credential.
- Start with one active generation request and a queue of two. Exact threads, affinity,
  context, memory, latency, and quality promotion thresholds require G10 evidence.

## Delivery slices

### Slice 1: candidate artifact contract

- [x] Add human-readable YAML manifest plus JSON Schema for the selected evaluation pair.
- [x] Validate immutable source revisions, license, model size/checksum, offline-only paths,
  and unresolved CPU binary checksum.
- [x] Update the AI deployment dossier without claiming import, install, or benchmark.

### Slice 2: strict inference boundary

- [x] Add immutable request/result/readiness contracts and an `LLMProvider` protocol.
- [x] Reject oversized prompts, excessive output/context limits, unknown fields, and
  client-supplied system/tool/provider settings.
- [x] Add failing tests first, then implement the contracts.

### Slice 3: bounded service and llama.cpp adapter

- [x] Implement one-active-request scheduling, bounded queue admission, queue timeout,
  provider timeout, cancellation cleanup, and explicit overload/dependency errors.
- [x] Implement a loopback-only OpenAI-compatible llama.cpp adapter with proxy bypass,
  API-key authentication, fixed model identity, non-thinking prompt mode, and strict
  response parsing.
- [x] Add an authenticated FastAPI surface for liveness, safe readiness, and generation.

### Slice 4: verification and handoff

- [x] Test accepted, unauthenticated, overloaded, timed-out, cancelled, malformed-provider,
  wrong-model, and degraded-readiness behavior without network/model dependencies.
- [x] Run format/lint, strict types, unit/API tests, document/dossier/artifact validation,
  build, dependency audit, and secret review.
- [x] Update paired docs, traceability, state and next task with exact pass/fail/not-run
  evidence; publish a PR but do not merge unreviewed work.

## Acceptance boundary

This increment can prove contracts, scheduling and adapter behavior with deterministic
fakes. It cannot prove CPU-only execution, Persian/English quality, cold-start latency,
offline startup, memory/NUMA fit, service TLS, backup/restore, or server readiness without
the separately authorized AI VM, imported artifacts and benchmark window.
