# AI answer integrity

**Status: accepted for controlled user testing; acceptance is release-specific.** NextOps cannot
guarantee that a generative model will never be wrong. It instead prevents the most dangerous
category error: presenting unsupported model text as live operational fact.

## Answer-completion correction and controlled promotion — 2026-09-26

A fresh live browser review exposed a 128-token incident answer that appeared unfinished while the
interface displayed the `evidence_bounded` notice. A controlled repetition of the same question
returned `finish_reason=length` and `deterministic_fallback`; this confirms output truncation can
occur while the previous label varied with the model's wording. The existing source checker
required source and partial-evidence words but did not inspect the model's `finish_reason`.
Application release `nextops-0.1.0-01755d1` now rejects `length`-terminated completions and long
question echoes on live routes,
replaces them with an evidence-only fallback that states it may not answer the full question, and
asks the model to answer the actual question first in short plain text. The browser notice now
states that lexical/source checks do not certify factual correctness or relevance. Focused
API/browser-fixture tests and bounded live release checks pass: fresh English/Persian greetings,
current Zabbix evidence, file questions, provenance, audit and a fresh browser. The owner's exact
prompt/response pair and full held-out bilingual semantic corpus remain **not run**; automated
checks do not prove every answer relevant or true.

Fine-tuning is not a substitute for current Zabbix evidence or a release gate based on a single
example. A versioned set of real, redacted question/answer failures and held-out Persian/English
cases is needed before comparing prompt, output-budget, model or fine-tuning changes.

## What users see

General assistant mode has no live evidence. Its output is labelled `model_unverified`, and the UI
asks users to verify important facts. Questions about current infrastructure state are not answered
from model memory; the response directs the user to Live monitoring or Incident investigation.

Live modes return the exact typed evidence, provenance, durable run, SHA-256 evidence reference and
audit identifier beside the answer. The nested assistant metadata matches the outer evidence mode.
The UI distinguishes these outcomes:

| Outcome | Meaning |
|---|---|
| `model_unverified` | Model-only text; no current evidence and no factual guarantee |
| `scope_redirect` | The question requires live evidence and was not answered from memory |
| `evidence_bounded` | Mandatory source/freshness/partial/read-only checks passed; exact evidence still governs |
| `deterministic_fallback` | Generated wording failed a mandatory check and was replaced with a safe deterministic response |
| `deterministic_focus` | A file/filesystem question receives a source-built answer instead of unverified generated detail |

The deployed focused-answer increment distinguishes allowlisted filesystem capacity from actual
system-file names and contents. Its prompt excludes unrelated incident fields, and application code
builds the displayed answer from typed Linux observations or states that file listing is unavailable.
It preserves partial-evidence disclosure, authorization, complete evidence, provenance and audit.
The machine-readable `file_listing_unavailable` limitation prevents a generic live-evidence prompt
from implying that another mode can show file contents. This does not train the model or qualify
arbitrary generated answers. Live acceptance of this release is bounded to the named checks; full
semantic review remains outstanding.

## Deterministic boundary

Before a generated answer is stored or shown, application code checks for false execution claims,
unsupported root-cause assertions, missing evidence-source labels and omitted stale/partial
qualifiers. A failure never retries with a less restrictive prompt. It returns a localized template
derived from the validated evidence contract. Source-controlled names are excluded from that
fallback so a hostile metric or problem name cannot become an instruction.

A long answer that merely repeats the general question is also replaced with a localized retry
notice. This does not reject short natural greeting replies.

These checks are deliberately narrow. They do not certify every sentence as true, judge arbitrary
general knowledge or replace review of exact evidence. NextOps still performs no infrastructure
mutation and the model receives no target credential.

## Qualification

The local evaluation corpus covers English and Persian evidence preservation, refusal to claim
execution, greeting relevance and refusal to invent current health without live evidence. The
harness checks authentication, readiness, required/forbidden language and script presence while
rejecting prompt echo and keeping semantic review explicit. It uses only the protected loopback
inference API and writes its report to a private file.

The normative requirements, acceptance cases and rollback are in the
[answer integrity specification](../requirements/ANSWER_INTEGRITY_SPEC.md).

## Controlled acceptance — 2026-09-26

At that checkpoint, application release `nextops-0.1.0-2397581` and inference API release
`nextops-0.1.0-fd3c353` were active. Their hosted workflow passed quality/unit, PostgreSQL 16,
PostgreSQL 17, browser fixture and secret-scan jobs. The final private loopback report passed all
eight automated cases; engineering semantic review accepted every English and Persian answer,
including direct greetings, explicit unknown current state, preserved timeout evidence and no
claim of execution. The report still sets `acceptance_claimed=false` because this is a bounded
quality gate, not production acceptance.

A short-lived server-created test session then exercised the deployed application. `Hi` returned no
Zabbix content, the current-status question returned `scope_redirect`, live monitoring returned
`evidence_bounded`, and the composite incident route returned `deterministic_fallback` with exact
evidence metadata. The session was revoked immediately. A subsequent serial reboot of Zabbix,
connector, AI and application loaded kernel `6.8.0-142`; every guest returned `running`, zero failed
units and no reboot marker. No recovery or SMTP-delivery claim is included.
