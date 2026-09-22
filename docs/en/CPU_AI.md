# Local CPU-only AI and capacity planning

[فارسی](../fa/CPU_AI.md) · [Index](INDEX.md)

**Status: bounded runtime/model smoke evidence and a repository-tested native service profile; full benchmark and deployment acceptance are not complete.** Source: master specification sections 2, 9–10 and 21. The pinned runtime/model pair has run on the qualified AI guest, but sustained throughput, production service behavior, rollback, restore, and Internet-blocked acceptance remain unmeasured.

## Non-negotiable execution boundary

Generation, planning, embeddings, reranking, AI anomaly processing and optional automated model judging run on local CPUs. No external AI endpoint or silent cloud fallback is permitted. An OpenAI-compatible request format is only a protocol shape, not authorization to call an external provider. GitHub is not a runtime AI dependency.

Use deterministic parsers, inventory resolution, policy checks, scheduling, basic correlation and known runbooks wherever possible. Logical planner/collector/analyst/verifier roles do not require multiple simultaneous models.

## Runtime and model candidates

The baseline is one dedicated service built from a pinned llama.cpp CPU revision. Verify the selected build's GPU-disable options, zero offload configuration and startup device report. Do not install CUDA/ROCm, GPU containers, accelerator-only dependencies or remote-code model loaders.

| Workload | Starting evaluation, not a final selection |
|---|---|
| General diagnostics | Approximately 7–9B multilingual quantized model; Qwen3-8B is one candidate |
| Triage | Smaller model versus deterministic classification |
| More difficult synthesis | Roughly 14B candidate after the baseline |
| Larger generation | 24–32B only when measured quality improvement justifies latency |
| Embeddings | Small multilingual encoder versus a candidate such as Qwen3-Embedding-0.6B |
| Reranking | Optional; enable only with measured retrieval gains within budget |

Compare supported Q4_K_M/Q5_K_M quantizations where available. Verify chat templates, structured-output behavior, tool arguments and Persian quality on the exact model/runtime combination. Do not choose 70B+ solely because weights fit in RAM. Ollama, OpenVINO CPU and vLLM CPU are alternatives to evaluate, not three additional mandatory services.

### Stage 1B repository candidate

The source-level evaluation pair is now recorded in the schema-validated
[`qwen3-8b-q4-k-m.yaml`](../../deploy/inference/qwen3-8b-q4-k-m.yaml): llama.cpp
`v0.4.1` at commit `b29c606e28a01b1bc8c1351026a0fa6e616bf6c4`, plus the official
`Qwen3-8B-Q4_K_M.gguf` at repository revision
`7c41481f57cb95916b40956ab2f0b139b296d974`. The model source records size
5,027,783,488 bytes and SHA-256
`d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`.

The pinned runtime was built with the recorded compiler/flags and OpenBLAS/OpenMP, promoted with its
binary SHA-256, and the model matched its expected filename, size, and SHA-256 before and after
promotion. A bounded authenticated CPU-only loopback smoke test succeeded. The repository now also
contains the paired hardened native units documented in [AI_SYSTEMD](AI_SYSTEMD.md), two file-backed
credential boundaries, fixed loopback origins, one llama.cpp slot, and the one-active/two-queued API
scheduler. These are source and smoke-test results, not full bilingual quality, latency, memory,
failure, offline cold-start, backup, restore, rollback, or production acceptance.

## Hardware discovery before tuning

Confirm CPU model, physical/logical cores, sockets, NUMA nodes, effective affinity/cgroup allocation, instruction sets, available RAM, storage and existing workload contention. “G10” and “90 CPU” establish none of these details. Discovery must not install packages or stress the host; see [installation](INSTALL.md).

## Staged benchmark

Begin with one small candidate, one active request and a bounded prompt/output. Compare generation and prompt-processing thread counts, physical-core versus SMT placement and NUMA-local versus controlled multi-node execution. Then compare model sizes and quantizations using the same versioned corpus. Increase active requests from one to two and then four only when latency and resource pressure remain acceptable. Initially evaluate representative 2K/4K/8K input contexts and verify total-versus-per-slot context semantics. Finally test bounded mixed traffic: chat, incident synthesis, embeddings, ingestion, database work and builds.

Record exact model/build/revision, flags, CPU mask, memory placement, input/output token counts, sample count, cold/warm state, queue delay, time to first token, prompt and generation throughput, total latency, p50/p95, peak memory, CPU pressure, swap/page faults, cancellations and errors. Evaluate complete answers and correct tool arguments, not tokens/second alone.

## Resource policy

Maintain one budget across all services. Reserving roughly 20% of effective CPU capacity for the OS/control plane is only an unvalidated starting experiment from the specification. Replace it with measured allocations. Do not allocate 90 threads per request or start 90 API workers. Cap runtime/BLAS/OpenMP thread pools, worker counts, queue lengths, context, output, tool fan-out and investigation concurrency.

Enforce limits through validated container controls or systemd/cgroups. Give interactive work priority over re-indexing; use backpressure and cancellation. API access, audit and manual incident views must remain usable when inference is saturated or absent.

## Artifact and acceptance record

Every model record includes source, immutable revision, license, quantization, tokenizer/template, dimensions where relevant, file size and checksum. Provision or import artifacts explicitly; missing files must fail preflight rather than trigger downloads. Keep weights outside Git.

Select the production candidate only after held-out bilingual quality and latency tests, explicit CPU execution verification, no-Internet acceptance tests and a documented operating envelope. Capacity targets must be labeled targets until measured.
