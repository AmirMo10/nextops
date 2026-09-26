# AI answer integrity

**Status: accepted for controlled user testing; acceptance is release-specific.** NextOps cannot
guarantee that a generative model will never be wrong. It instead prevents the most dangerous
category error: presenting unsupported model text as live operational fact.

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

Application release `nextops-0.1.0-2397581` and inference API release
`nextops-0.1.0-fd3c353` are active. Their hosted workflow passed quality/unit, PostgreSQL 16,
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
