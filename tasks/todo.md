# Tasks: Stage 1B Increment 3 local CPU inference foundation

## Task 1: lock the evaluation candidate metadata

**Acceptance criteria:**

- [x] YAML manifest is human-readable and validates against a versioned JSON Schema.
- [x] llama.cpp source tag/commit/license and Qwen repository revision/file/size/SHA-256/
  license are exact.
- [x] Binary checksum, build flags, guest ISA and benchmark evidence remain explicit
  blockers rather than guessed values.

**Files:** `deploy/inference`, validator/tests, `deploy/server-dependencies/nextops-ai.yaml`.

## Task 2: define and implement the provider boundary

**Acceptance criteria:**

- [x] Strict request/result/readiness contracts forbid extra fields and bound prompt,
  output, sampling and timing values.
- [x] `LLMProvider` is runtime-neutral and exposes generation plus safe readiness.
- [x] Client requests cannot supply system prompts, tools, URLs, model IDs or credentials.

**Files:** `packages/nextops/inference`, `tests/unit`.

## Task 3: enforce bounded authenticated execution

**Acceptance criteria:**

- [x] One active request and queue depth two are enforced atomically.
- [x] Overload, queue timeout, provider timeout, cancellation and malformed output have
  explicit safe outcomes and release capacity.
- [x] llama.cpp transport is loopback-only, ignores environment proxies, authenticates,
  calls a fixed model, and validates the response.
- [x] Only the configured app service secret can call generation; readiness discloses no
  path, key, prompt or raw provider error.

**Files:** inference scheduler/provider/API/configuration and unit/API tests.

## Task 4: publish truthful evidence

**Acceptance criteria:**

- [x] All repository quality/security gates pass and no secret/model binary is committed.
- [x] English/Persian docs and project state distinguish candidate selection/source tests
  from not-run runtime/server acceptance.
- [x] PR records remaining inputs for authorized model import, CPU build and benchmark.

**Files:** CI, paired docs, project state, traceability and PR.
