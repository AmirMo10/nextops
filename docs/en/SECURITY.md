# Security, permissions and action approval

[فارسی](../fa/SECURITY.md) · [Index](INDEX.md)

**Status: required control set with a tested source-level subset.** Local identity, server-derived scopes, deterministic denial, secret checks, append-restricted audit and inference service authentication are implemented; complete gateway, connector, deployment and remediation controls remain unimplemented. Source: master specification sections 11–14, 18 and 20–21. See also the [repository security policy](../../SECURITY.md).

## Trust model

Protect device credentials, administrative authority, incident evidence, approvals and audit history. Users, browser input, model output, retrieved documents, logs, banners, alert fields and remote tool descriptions are separate trust domains. External content is evidence, never authority to change instructions or permissions.

| Threat | Required control | Required test |
|---|---|---|
| Prompt injection in logs/runbooks | Labeled evidence; deterministic execution policy | Malicious text cannot grant tools or retrieve credentials |
| Unauthorized target or evidence | Organization/environment/action/asset scope before retrieval and execution | Cross-scope requests denied server-side |
| Gateway bypass | Service authentication, network isolation, connector-side recheck | Direct unauthenticated connector call fails |
| Forged or replayed approval | Durable exact-action digest, expiry, nonce, atomic consume | Replay and changed arguments denied |
| Command/SQL injection | Named operations, strict schemas, fixed templates, least-privilege accounts | Metacharacters, target substitution, unsafe SQL rejected |
| Credential leakage | Reference-only configuration, boundary-local decryption, redaction | Secrets absent from prompts, logs, evidence, traces and errors |
| Resource exhaustion | Deadlines, output/row/byte/token caps, admission control | Control plane remains responsive under saturation |
| Uncertain remote mutation | Reconcile observed target state before retry | Timeout cannot silently duplicate a change |

## Identity and policy

Retain `viewer`, `operator`, `engineer`, and `admin`, combined with organization, environment, target and operation scopes. Default deny. Administrator status does not bypass audit or destructive-action controls. Start with one explicit organization scope; multi-tenant SaaS isolation is not a validated first-release capability.

Preserve risk classes `READ_ONLY`, `LOW_RISK`, `MEDIUM_RISK`, `HIGH_RISK`, `CRITICAL`. Trusted versioned policy assigns risk. A read can still disclose secrets or overload equipment. MVP permits only bounded allowlisted diagnostics; all infrastructure mutations remain disabled.

## Exact-action approval

When remediation is eventually enabled, approval covers a canonical digest of action, validated arguments, immutable target IDs, requester, environment, expected pre-state/config version, policy version, expiry and a single-use nonce. Store it durably and consume it atomically. Recheck requester and approver permissions plus preconditions at execution. Any material change invalidates consent.

High-risk/critical actions require independent approval and impact/maintenance-window checks. Critical destructive actions remain disabled without an explicit owner-reviewed configuration change. A chat message saying “yes” is not an execution credential. Rollback is a separate authorized action with its own risks.

## Credentials and transport

The controlled HTTP clients explicitly reject redirects. A redirecting internal AI/connector or
Zabbix endpoint cannot forward its bearer/API token to a second origin. Local 302 regression tests
cover both transport implementations. Four live guests now apply the project SSH drop-in
`deploy/ssh/00-nextops-hardening.conf`: password and keyboard-interactive authentication and direct
root login are disabled, while public-key authentication is required. Effective `sshd` policy and
new key-only connections were checked on each guest; newly established application tunnels and a
fresh authenticated browser session passed. The AI host also runs UFW with deny-incoming and
OpenSSH allowed. This UFW policy does not block host outbound Internet: direct IPv4 from an
administrator shell remains reachable on all four guests. The app/AI/model units have their own
loopback-only IP policy, and the connector now has a deny-all-except-approved-LAN process policy.
Persistent host-wide egress restriction remains partial. These
controls do not make the still-unaccepted recovery and certificate gates pass.

Configuration stores credential references only. Decrypt credentials only inside the authorized execution boundary. Keep encryption keys separate from ciphertext; `.env` is not a production vault. Use scoped SSH/API/database accounts, verified SSH host keys, validated TLS certificates, rotation and expiring sessions. No default administrator password, blanket host-key acceptance, `verify=False`, privileged container or engine-socket shortcut.

The source now implements an audited, server-side `POST /api/v1/logout` boundary. It hashes the
presented bearer, row-locks and revokes only that durable session, and records one correlated
append-only event. Replay is idempotent and an unknown bearer receives the same empty result as an
already-revoked session, avoiding a token-existence oracle. The offline panel always removes its
tab-local copy after attempting revocation. Hosted PostgreSQL 16/17 CI and controlled live
application/browser acceptance pass; see the
[session termination specification](../requirements/SESSION_TERMINATION_SPEC.md).

Certificate-expiry detection is local and read-only. The dedicated checker receives only the public
certificate path, has no network address family or Linux capability, and cannot read the root-only
private key. It emits no subject/SAN or endpoint identifier. Detection does not authorize renewal;
the [certificate lifecycle contract](../requirements/CERTIFICATE_LIFECYCLE_SPEC.md) keeps promotion,
rollback and alert ownership as explicit reviewed gates. Tagged local Zabbix items/triggers and a
guarded failure/recovery exercise now prove local detection; notification delivery and live-pair
rotation remain separate unaccepted controls.

SQL tools use predefined bounded diagnostic queries and narrow database identities. `SELECT` alone does not prove safety. Stored functions, output-to-file operations, locks, costly queries and execution-oriented EXPLAIN variants require their actual semantics to be considered.

## Audit and operational isolation

Audit requests, permission decisions, evidence access where needed, proposals, approvals/rejections, credential-use references, execution, verification, policy and release changes. Exclude secrets. Block mutations when durable audit is unavailable. Ordinary logs and security audit are not interchangeable.

A local hash chain cannot defeat a host administrator controlling both records and keys. Stronger tamper evidence requires an independently protected checkpoint/archive. Separate UI ingress, internal traffic and connector egress. Restrict destinations and revalidate DNS/redirect behavior; the gateway must not become an arbitrary network proxy.

Release acceptance includes secret-leak tests, stale/replayed approval tests, role revocation, cross-environment evidence, injection, gateway bypass, worker crash, unknown-outcome handling and audit/database failure. Passing a defined suite is evidence about those tests, not a claim of immunity to every attack.
