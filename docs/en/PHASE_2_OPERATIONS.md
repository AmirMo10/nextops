# Phase 2 read-only incident operations

[فارسی](../fa/PHASE_2_OPERATIONS.md) · [Specification](PHASE_2_COMPLETION_SPEC.md) · [ADR 0007](../adr/0007-forced-command-linux-connector.md)

**Status:** deployed controlled-user-testing procedure with application release
`nextops-0.1.0-eb57241` and connector release `nextops-0.1.0-e2dad3a`. The application-only session
termination promotion did not change the connector contract, and a fresh bilingual Phase 2 browser
gate passed on this release. This document does not authorize target access, a service restart, or
a firewall change.

## What Phase 2 adds

The authenticated application now offers an explicit **Incident investigation** mode for the
configured logical targets `app`, `ai`, `connector`, and `zabbix`. One request combines:

- a bounded current Zabbix summary;
- at most 32 numeric history points and 25 trigger events from the fixed incident window;
- one direct, bounded Linux snapshot from the selected host; and
- one local CPU-model explanation linked to the exact evidence hash and append-only audit event.

General conversation and the simpler Zabbix-only mode remain separate. Phase 2 is read-only. It
does not add remediation, arbitrary SSH, caller-selected commands, a generic proxy, or credentials
to the model or browser.

## Security boundary

Each target has a distinct Ed25519 key held only by `nextops-connector.service`. The remote
`nextops-linux-ro` account has a locked password and a root-owned `authorized_keys` entry using
`restrict` and a fixed command. The collector accepts only
`nextops-linux-snapshot-v1`, reads only its root-owned allowlist, and emits schema-validated bounded
JSON. OpenSSH host identities are pinned with strict checking. The application sees logical target
IDs; it never accepts an address or command from the request.

The snapshot includes load, memory, swap, selected filesystem capacity, process names without
arguments, selected systemd state, redacted high-priority journal entries, bounded listening TCP
sockets, routes, name servers, local-user/session counts, and package count. It does not read file
contents, environment variables, command lines, credentials, or arbitrary logs.

## Controlled installation

1. Generate four distinct Ed25519 key pairs on the connector host. Store private keys as
   root-owned systemd credentials and never copy them into Git or an application release.
2. Verify each current SSH host fingerprint through the approved private inventory, then create the
   root-owned combined `linux_known_hosts` file.
3. On each target, copy the release, the matching file from `deploy/linux/`, and only that target's
   public key into a root-only staging directory.
4. Validate without changing the host:

   ```bash
   sudo ./deploy/linux/install-linux-readonly.sh \
     --config ./deploy/linux/app.json \
     --public-key ./linux-app-key.pub
   ```

5. Inside the authorized change window, repeat with `--apply`. The installer creates the locked
   identity, installs the root-owned collector/configuration, installs the restricted public key,
   and performs a local collector self-test.
6. Install an environment-specific `/etc/nextops/linux-targets.json` derived from the example. Use
   approved private addresses or names only in that protected server file.
7. Install the updated connector/app units and environment files, run `systemd-analyze verify`,
   apply the database migration, and restart one service at a time.

Do not use the existing administrative SSH identity as the runtime credential. Do not add the
collector account to `sudo`, Docker, or any target-credential group.

## Acceptance and evidence

For every target, prove:

- an unauthenticated connector request is denied;
- an unknown target ID is denied without an outbound SSH attempt;
- the fixed command succeeds and any other command is denied;
- the returned target ID matches the configured target;
- output limits, redaction, timeouts, and partial markers behave as designed;
- the authenticated application stores the exact composite evidence hash and audit event;
- English and Persian answers separate observations, hypotheses, unknowns, and safe read-only
  next checks;
- restart recovery works for connector and application services; and
- a fresh investigation works while WAN access is blocked and approved LAN routes remain available.

Record raw infrastructure output only in the private change record. The public release manifest may
record sanitized results, timestamps, release identifiers, and pass/fail state.

The 2026-09-23 controlled campaign completed this checklist: the authenticated WAN-denied browser,
safe connector loss/general-AI containment/recovery, serial four-VM reboot and fresh post-reboot
bilingual incident all passed. The incident endpoint was also added to Nginx's bounded 180-second
assistant location after the first live run exposed the missing route. These results qualify the
read-only Phase 2 slice; they do not satisfy independent backup, PITR, certificate lifecycle or
disaster-recovery acceptance.

## Rollback

Rollback the application and connector release links together, downgrade migration
`0002_phase2_linux_read` if the prior application requires it, restore the prior environment files,
and restart the two services. On targets, remove the Phase 2 public key or lock the account to revoke
access immediately. The collector and configuration may remain inert for forensic comparison; they
are not reachable after key revocation. Preserve failed-run audit records.
