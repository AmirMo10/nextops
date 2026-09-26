# Answer integrity specification

Status: implemented in source; live qualification remains revision-specific.

## Problem

A small local language model can produce fluent text that is irrelevant, unsupported, stale or
wrong. Prompt instructions alone are not a security or truth boundary. NextOps must never present
model memory as live infrastructure evidence, must never imply that a read-only assistant performed
an operation, and must preserve stale/partial qualifiers even when generated prose fails.

## Requirements

- General mode remains useful for ordinary questions but is explicitly labelled as model-only and
  potentially incorrect.
- A general-mode question asking for current infrastructure state is redirected to a live evidence
  mode instead of being answered from model memory.
- Monitoring and incident responses label the nested assistant result with the same evidence mode
  as the enclosing response.
- Deterministic application code rejects generated operational-execution claims, unsupported
  root-cause assertions, missing source labels and omitted stale/partial qualifiers.
- A rejected monitoring or incident answer is replaced by a bilingual deterministic summary built
  only from typed evidence. Untrusted names are not copied into this fallback.
- Every result exposes a machine-readable integrity outcome and limitations. The browser explains
  the outcome without implying that automated checks prove factual correctness.
- The stored completion audit records the integrity outcome and limitations.
- Qualification remains local, CPU-only and offline-capable. No evaluator may silently call a
  remote model or telemetry service.
- Returning the user's prompt or instructions as the answer is a failed relevance case, even when
  the echoed text happens to contain required safety words.

## Non-goals

- Claiming that any generative model is free of hallucinations.
- Fact-checking arbitrary general knowledge without an approved local source.
- Treating lexical gates, model confidence or fluent wording as proof.
- Granting execution authority, credentials or mutation capability to the model.
- Replacing exact evidence, provenance, audit or operator judgment with generated prose.

## Threat considerations

The controls address prompt injection in source-controlled text, fabricated current state,
fabricated execution, unsupported root cause, hidden evidence truncation, stale-data laundering and
contradictory response metadata. They fail closed to deterministic evidence summaries. They do not
establish the truth of arbitrary model-only answers, so the UI must preserve the verification
warning.

## Implementation and tasks

1. Extend the assistant contract with consistent evidence mode, live-data marker, integrity status
   and bounded limitation codes.
2. Apply deterministic general, monitoring and incident answer assurance before persistence.
3. Add localized browser notices for unverified, evidence-bounded, fallback and redirect outcomes.
4. Expand the bilingual local evaluation corpus with relevance and no-live-evidence cases and add
   deterministic lexical safety gates while retaining manual semantic review.
5. Run source checks, PostgreSQL integration CI, live loopback model qualification and live browser/API
   acceptance for the exact deployed revision.

## Acceptance criteria

- `Hi` and `سلام` remain short greetings and do not introduce Zabbix state.
- General mode does not answer a current infrastructure-status question as fact.
- A generated claim that NextOps restarted, fixed, deployed or changed infrastructure is never
  returned to the user.
- Live responses carry `live_zabbix` or `live_zabbix_linux` in both enclosing and nested metadata.
- Stale or partial evidence cannot be presented without its qualifier; failure produces the
  deterministic fallback.
- Injected metric/problem names cannot cause instructions or secret disclosure and are absent from
  the deterministic fallback.
- Audit, evidence hash/reference and read-only authorization remain intact.
- The eight-case English/Persian loopback corpus passes deterministic checks; a human reviewer still
  inspects meaning and language quality.
- Prompt echo fails automatically and semantic review must reject an answer that merely restates the
  question.

## Tests and evidence

Unit/API tests cover contract consistency, scope redirect, false execution claims, evidence-bounded
acceptance, stale/partial fallback and prompt-injection containment. The existing private live
evaluation report remains outside Git because deployment evidence may contain operational metadata.
Passing tests qualify only the named cases and revision.

## Rollback

Retain the prior immutable application and inference releases. Roll back each `current` link
independently, restart the affected unit, and verify authentication, readiness and the exact `Hi`
relevance case. A rollback also removes the new integrity metadata and must therefore be recorded as
a security-significant downgrade.

## Documentation

The paired [English](../en/AI_INTEGRITY.md) and [Persian](../fa/AI_INTEGRITY.md) guides describe the
operator-visible behavior. Project state and the release manifest record only observed deployment
and acceptance results.
