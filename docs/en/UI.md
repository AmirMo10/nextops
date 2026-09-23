# Bilingual operations console and design system

[فارسی](../fa/UI.md) · [Index](INDEX.md)

**Status: specification plus a delivered controlled user-testing subset.** Source: master specification sections 3, 7 and 17 plus original sections 3 and 30.

The controlled subset provides authenticated English/Persian login, genuine RTL/LTR switching,
AI and monitoring readiness and a bounded question form with three explicit answer modes. General
assistant is the default: it answers through the local model without retrieving or displaying live
monitoring evidence. Live monitoring is opt-in: it returns an evidence-grounded answer and a source
panel showing Zabbix version, host, collection time, measurement time, freshness and active-problem
count. Incident investigation adds one deployment-approved target and combines bounded Zabbix
history/events with the direct read-only Linux snapshot. The result badge always identifies whether
live evidence was used. A completed evidence-backed answer also shows its durable run, evidence
reference and audit-event identifiers; the full evidence SHA-256 is available as the
evidence-reference tooltip. Assets are served locally without a CDN.
The broader operations console described below—inventory, incident timelines, topology, approvals,
audit search and settings—remains specification work.

Live investigations are capped server-side at the qualified 128-token CPU budget; the browser uses
the same bound. Timeout, overload and local-dependency failures retain safe machine-readable status
and are presented as distinct actionable messages in both languages. This prevents a stale or
modified browser from raising the output limit beyond the qualified user-testing profile.

## Information architecture

Build an operations console, not just a chat page or decorative landing page. Primary areas are overview, asset inventory/details, incidents and evidence timeline, topology, approval requests, connector health, audit search, model/resource health, and settings. Chat is one way to start or inspect a durable investigation.

An investigation view shows affected assets, time window, permission scope, task progress, source-linked evidence, missing/partial data, alternative causes and a concise decision summary. Show tool activity and sanitized outputs, not unrestricted internal reasoning traces. Recommendations and actual execution outcomes must be visually distinct.

## Shared design system

Define semantic tokens for spacing, typography, colors, borders and component states before building many pages. Use reusable navigation, tables, filters, timelines, evidence cards, status badges, dialogs and approval panels. Status meaning must not rely on color alone. Keep labels, keyboard interaction, focus behavior and contrast accessible.

Use responsive layouts with long device names, mixed-language text, overflowing commands and dense operational data in mind. Prefer locally hosted licensed assets; runtime must not depend on font, icon or JavaScript CDNs.

### Current OCS visual identity

The current source redesign uses the company mark supplied through the owner's public OCS profile
reference and the observed OCS gold (`#D0A840`) and teal (`#0090A0`) as brand accents. The exact
logo is embedded locally and also supplies the browser icon; system fonts, CSS artwork and interface
icons are local, so the page issues no runtime request to LinkedIn, a font host or a CDN. The light
enterprise layout keeps semantic success, warning and failure colors separate from the brand.

A development-only [Figma design source](https://www.figma.com/design/fXtpP4xBQg3qovTDcchuHx)
now records the OCS cover, 48 primitive/semantic/dimension variables, 11 bilingual text styles and
two elevation styles. The implemented workspace mirrors its spacing, radii and brand tokens, with
numbered answer-mode cards, a high-contrast evidence boundary, compact service-status pills and a
branded result accent. Figma is not a runtime dependency or an authority for application behavior;
the reviewed source, tests and documentation remain authoritative. Full product-screen composition
inside Figma was not completed because the Starter-plan MCP call quota was reached, so the file
must not be represented as a complete screen library.

The real-browser fixture covers the branded login, authenticated workspace, composite incident
evidence, English LTR, Persian RTL, reduced motion and 375-pixel mobile width without horizontal
overflow or external requests. The source passed all five CI jobs and was promoted as immutable
application release `nextops-0.1.0-54c8bb4`. A fresh deployed login check passed English desktop and
Persian RTL at 375 pixels with no overflow, external request, failed response or console error. The
later authenticated Phase 2 live-browser workflow also passed English/Persian incident evidence,
normal TLS, WAN denial, mobile RTL, logout and new-tab isolation.

## Persian and English behavior

Persian uses a genuine RTL layout with natural wording; English uses LTR. Isolate code, IP addresses, interface names, timestamps and identifiers so bidirectional rendering cannot alter perceived technical meaning. Keep command bytes and raw diagnostic strings unchanged except explicit secret redaction. Do not localize protocol field values or store translated labels as business keys.

Use [the glossary](GLOSSARY.md) for consistency. Review Persian with realistic incident narratives, not merely automated detection of Persian characters. Language switches must preserve the same record, permissions, evidence and workflow state. The application stores UTC and lets the deployment choose display timezone.

## Required states

Explicitly represent loading, empty, stale, partial, offline, overloaded, access denied, awaiting approval and unknown outcome. Model unavailability must not block manual incident/evidence access. Read-only mode versus mutation-enabled mode must be obvious. Display connector capability status accurately: planned, simulated, lab-verified or production-validated.

## Approval interface

Present the exact target, named action, arguments or change diff, requester, policy/risk, expected pre-state, impact, freshness, approver requirement and expiry. A generic Approve button is insufficient. Changed details invalidate the old approval. Never display credential contents; the screen refers to the approval record, not an executable secret.

For a timed-out mutation, show that the outcome is unknown and requires reconciliation. Do not present a green success indicator or offer blind retry. Distinguish requested cancellation from verified remote cancellation.

## Acceptance

Browser tests cover both directions, keyboard navigation, mixed text, long commands, permission boundaries, approval expiry/changes, reconnecting progress, partial evidence and offline assets. Domain and language reviewers verify that wording does not overstate certainty or imply an unexecuted action succeeded.
