# Production blocker resolution runbook

[فارسی](../fa/PRODUCTION_BLOCKERS_RUNBOOK.md) · [Recovery contract](../../deploy/recovery/README.md) · [Current status](../status/current-release.yaml)

**Status: owner action required; this document does not close any gate.** Updated: 2026-09-26.

On 2026-09-26 the owner confirmed that none of the requested independent recovery/restore
resources, project-license decision, local delivery channel and recipients, replacement CA
certificate pairs, or named approvers are available. The steps below remain future handoff
instructions; no placeholder or serving-guest copy qualifies as a substitute.

This runbook lists every blocker that still prevents a production-acceptance claim and separates
what the owner must supply from what the NextOps engineering agent will implement and verify. Never
put an address, datastore identifier, password, token, private key, SMTP secret, CA key or raw
infrastructure inventory in Git, an issue, or chat. Keep those values in the private change record.

Commands below are either read-only or create a new account/file. No disk-format, database-delete,
certificate-promotion or firewall-mutation command is supplied without a resolved target. Stop when
an expected value is missing or different; do not substitute a guessed path or device.

## 1. Current blockers and ownership

| ID | Current state | Owner action | Engineering action after owner handoff | Exit condition |
|---|---|---|---|---|
| `independent_destination_not_approved` | Blocked | Provision and approve storage outside every serving VM, its datastore and its hypervisor | Qualify and configure separate pgBackRest/restic repositories | Independence evidence accepted |
| `recovery_objectives_not_approved` | Blocked | Approve RPO, RTO, retention, restore cadence, owners and key custody | Encode the sanitized values in the recovery profile | Policy is signed and profile validates |
| `offline_tool_bundles_not_verified` | Blocked | Approve connected build/staging and license policy | Acquire, hash, license-review and offline-test pgBackRest 2.59.1 and restic 0.19.1 | Exact bundles install/remove offline and hashes are recorded |
| `isolated_restore_not_run` | Blocked | Provide an isolated restore environment with no production route/credentials | Run full/differential/WAL/PITR, file, negative, offline and key-recovery drills | Every recovery gate passes with measured RPO/RTO |
| Certificate operator delivery | Partial | Choose a LAN-local notification route and named primary/backup recipients | Configure Zabbix media, user media, trigger action and recovery messages | Test and real controlled problem/recovery reach both recipients |
| Certificate rotation/rollback | Not run | Supply two CA-signed replacement pairs and approve a maintenance window | Stage, verify, rotate, test and roll back each frontend under a guard | Both rotation and rollback pass with ordinary TLS validation |
| Dependency/license/SBOM/release integrity | Open | Name the legal/security approver and approve the acceptance policy | Generate/review SBOMs, license inventory, vulnerability evidence and offline verification material | No unapproved dependency/license or unresolved release-integrity finding |
| Final production decision | Not run | Name the production approver and sign the bounded accepted profile | Re-run all production gates and publish only sanitized results | No required gate is failed, partial or not run |

The first four IDs are the exact machine-readable blockers in
`deploy/recovery/recovery-profile.yaml`. The other four are explicit current project-state gates.

## 2. Create the private owner record

Run this on the Windows development desktop. It creates a private location outside the repository.

```powershell
$QualificationDir = Join-Path $HOME '.nextops\production-qualification'
New-Item -ItemType Directory -Force -Path $QualificationDir | Out-Null
$DecisionFile = Join-Path $QualificationDir 'owner-decisions.txt'
New-Item -ItemType File -Force -Path $DecisionFile | Out-Null
notepad $DecisionFile
```

Place this template in that file and replace every `REQUIRED` value. The recommended policy is a
starting point, not an inferred business approval.

```text
change_id=REQUIRED
owner_approver=REQUIRED
recovery_operator=REQUIRED
rollback_owner=REQUIRED
maintenance_window=REQUIRED

destination_id=REQUIRED_NON_SECRET_ALIAS
destination_type=dedicated_physical_or_separate_hypervisor
independent_from_serving_guest=yes
independent_from_serving_datastore=yes
independent_from_serving_hypervisor=yes

rpo_minutes=15
rto_minutes=240
full_backups_to_keep=4
differential_backups_to_keep=14
wal_days_to_keep=14
file_snapshots_to_keep=30
restore_test_cadence=quarterly

key_custodian_primary=REQUIRED
key_custodian_secondary=REQUIRED_DIFFERENT_PERSON
offline_recovery_copy_location=REQUIRED_PRIVATE_REFERENCE

notification_type=internal_smtp_or_approved_lan_route
notification_owner_primary=REQUIRED
notification_owner_backup=REQUIRED
notification_recipient_primary=REQUIRED_PRIVATE_REFERENCE
notification_recipient_backup=REQUIRED_PRIVATE_REFERENCE

certificate_issuer=REQUIRED_PRIVATE_REFERENCE
certificate_change_window=REQUIRED
certificate_rollback_owner=REQUIRED

license_approver=REQUIRED
security_approver=REQUIRED
production_approver=REQUIRED
```

Do not paste this file into chat. Send only the non-secret decisions and tell the engineering agent
that the private record is complete.

## 3. Provision the independent recovery destination

### 3.1 Required design

The recommended design is a dedicated Ubuntu Server 24.04 LTS physical recovery host with protected
storage, or a VM on a different physical hypervisor and different backing storage. A fifth VM on
the current hypervisor, another virtual disk on the current datastore, an NFS export backed by that
same host, a snapshot, or a directory on any serving VM does **not** satisfy this gate.

The recovery target must remain reachable over the approved management LAN when the public Internet
is unavailable. It must not provide the model or application with credentials. Use separate
repositories and access identities for the application PostgreSQL cluster, Zabbix PostgreSQL
cluster and approved restic files.

Provision a separate disposable restore VM or isolated physical environment. It must have no route
to production targets and must not contain production connector, Zabbix API or application
credentials. Size it from measured source data plus at least 30% working headroom; do not guess from
thin-provisioned current usage.

### 3.2 Measure the protected capacity requirement

Run from the development desktop. Keep the output in the private record.

```powershell
$QualificationDir = Join-Path $HOME '.nextops\production-qualification'
$MeasureFile = Join-Path $QualificationDir 'source-capacity.txt'
@(
  '=== application PostgreSQL bytes ==='
  (ssh nextops-app 'sudo -n -u postgres psql --cluster 16/nextops -d postgres -Atc "SELECT COALESCE(sum(pg_database_size(datname)),0) FROM pg_database WHERE datistemplate = false;"')
  '=== Zabbix PostgreSQL bytes ==='
  (ssh nextops-zabbix 'sudo -n -u postgres psql --cluster 16/zabbix -d postgres -Atc "SELECT COALESCE(sum(pg_database_size(datname)),0) FROM pg_database WHERE datistemplate = false;"')
  '=== approved artifact candidate bytes ==='
  (ssh nextops-app "sudo -n du -sb /srv/nextops/releases /usr/local/share/doc/nextops 2>/dev/null")
  (ssh nextops-ai "sudo -n du -sb /srv/nextops/releases /srv/nextops/models 2>/dev/null")
  (ssh nextops-connectors "sudo -n du -sb /srv/nextops/releases 2>/dev/null")
) | Set-Content -Encoding utf8 $MeasureFile
Get-Content $MeasureFile
```

Use the measured database sizes, observed daily change rate, selected retention and restore working
space to size the destination. The engineering agent will calculate the final repository reserve
after WAL/change-rate measurements are available.

### 3.3 Create controlled administrative access

Create a dedicated recovery-host key on the Windows desktop. Do not reuse a connector, application
or ordinary administration key. `ssh-keygen` prompts for a passphrase; use a protected passphrase
and load the key into the Windows SSH agent.

```powershell
$RecoveryKey = Join-Path $HOME '.ssh\nextops_recovery_ed25519'
if (Test-Path -LiteralPath $RecoveryKey) { throw 'Recovery key already exists; inspect it instead of overwriting it.' }
ssh-keygen -t ed25519 -a 64 -f $RecoveryKey -C 'nextops-recovery-deployment'
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $RecoveryKey
Get-Content "$RecoveryKey.pub"
```

At the new recovery host's trusted local/virtual console, run:

```bash
id nextops-dev >/dev/null 2>&1 || sudo adduser --disabled-password --gecos '' nextops-dev
sudo passwd -l nextops-dev
sudo install -d -o nextops-dev -g nextops-dev -m 0700 /home/nextops-dev/.ssh
sudoedit /home/nextops-dev/.ssh/authorized_keys
sudo chown nextops-dev:nextops-dev /home/nextops-dev/.ssh/authorized_keys
sudo chmod 0600 /home/nextops-dev/.ssh/authorized_keys
printf '%s\n' 'nextops-dev ALL=(ALL:ALL) NOPASSWD: ALL' \
  | sudo tee /etc/sudoers.d/90-nextops-dev >/dev/null
sudo chmod 0440 /etc/sudoers.d/90-nextops-dev
sudo visudo -cf /etc/sudoers.d/90-nextops-dev
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Paste exactly one public-key line into `authorized_keys`. The last command prints the host
fingerprint. Send only that fingerprint through a separately verified channel.

On the Windows desktop, collect but do not trust the network key until its fingerprint exactly
matches the console fingerprint:

```powershell
$RecoveryHost = Read-Host 'Recovery host IP or FQDN'
$Candidate = Join-Path $env:TEMP 'nextops-recovery-hostkey'
ssh-keyscan -t ed25519 $RecoveryHost 2>$null | Set-Content -Encoding ascii $Candidate
ssh-keygen -lf $Candidate
```

After manually confirming an exact match:

```powershell
Get-Content $Candidate | Add-Content -Encoding ascii "$HOME\.ssh\nextops_known_hosts"
Remove-Item -LiteralPath $Candidate
notepad "$HOME\.ssh\config"
```

Add this host block, substituting only the private address/name:

```sshconfig
Host nextops-recovery
    HostName RECOVERY_HOST_OR_IP
    User nextops-dev
    IdentityFile ~/.ssh/nextops_recovery_ed25519
    UserKnownHostsFile ~/.ssh/nextops_known_hosts
    IdentitiesOnly yes
    StrictHostKeyChecking yes
    BatchMode yes
    ConnectTimeout 10
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ForwardAgent no
```

Verify the account without changing the host:

```powershell
ssh -o BatchMode=yes nextops-recovery "id; sudo -n true; systemd-detect-virt; systemctl is-system-running"
```

Full passwordless sudo is deliberately temporary for controlled provisioning. After recovery
qualification, replace it with reviewed command-scoped rules or remove it:

```bash
sudo rm -f /etc/sudoers.d/90-nextops-dev
sudo visudo -c
```

Do not remove it until a separately tested emergency administration path exists.

### 3.4 Record independence and health evidence

Run on the recovery host and store the unredacted output only in the private record:

```bash
cat /etc/os-release
uname -r
systemd-detect-virt
sudo dmidecode -s system-manufacturer
sudo dmidecode -s system-product-name
sudo dmidecode -s system-uuid
lsblk -e7 -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL,SERIAL
findmnt -T /srv/nextops-recovery -o SOURCE,TARGET,FSTYPE,OPTIONS
df -B1 /srv/nextops-recovery
timedatectl status
ip -brief address
ip route
ss -H -lntup
systemctl --failed --no-legend
```

The owner must additionally record the physical hypervisor/asset identifier and backing-storage
identifier from the management plane. Guest commands alone cannot prove failure-domain
independence. Do not send those identifiers to public Git or chat. Do not run `mkfs`, `wipefs`,
`fdisk`, `parted`, LVM creation, mount changes or firewall changes until the exact unused target and
rollback path are reviewed.

### 3.5 Required network decisions

Approve only these flows initially:

- management workstation → recovery host: SSH TCP 22;
- application PostgreSQL host ↔ recovery host: the reviewed pgBackRest SSH protocol path;
- Zabbix PostgreSQL host ↔ recovery host: the reviewed pgBackRest SSH protocol path;
- approved file-backup clients → recovery host: the selected restic transport path;
- recovery host/restore lab → approved local DNS, time and monitoring services only.

No public Internet ingress, application UI ingress, model access, generic connector route, or
production-target route from the restore lab is allowed. Record the firewall owner and rule IDs
privately. Engineering will supply exact source/destination rules after the destination and
transport are approved.

## 4. Approve recovery objectives and custody

The recommended initial values are RPO 15 minutes, RTO 240 minutes, four full backups, fourteen
differential backups, fourteen days of WAL, thirty file snapshots and a quarterly restore drill.
These values must be checked against measured change rate, destination capacity and business need.
The owner must explicitly write `approved` or provide replacements; silence is not approval.

Two different people must be able to recover the repository encryption material. Neither the
encryption password nor its recovery copy may be stored in Git, the backup repository itself, the
same password manager account as the repository credential, or chat. Record only private references
and the date of a successful key-recovery exercise.

When the owner record is complete, send this non-secret summary:

```text
destination_alias=<non-secret alias>
independence=guest:yes,datastore:yes,hypervisor:yes
rpo_minutes=<approved integer>
rto_minutes=<approved integer>
retention=full:<n>,diff:<n>,wal_days:<n>,files:<n>
restore_cadence=<approved cadence>
key_custody=two-person-approved
recovery_host_access=ready
restore_lab=ready
```

## 5. Offline backup-tool bundle gate

After sections 2–4 are complete, engineering will prepare exact pgBackRest 2.59.1 and restic
0.19.1 bundles in a disposable connected build environment. The owner must approve the MIT and
BSD-2-Clause licenses and the use of that connected staging environment. Do not run `apt install`,
`curl | sh`, compile tools on a serving VM, or let a serving VM download packages.

Engineering must then provide and verify:

- exact artifact and dependency inventory with SHA-256;
- license record;
- matching pgBackRest version on repository and database hosts;
- offline install, version, removal and reinstall tests;
- no service start or database mutation during package staging;
- immutable retained copy of the accepted bundles.

The official pgBackRest guide requires matching local/remote versions. A package install or backup
command alone does not close this gate.

## 6. Isolated backup and restore acceptance

Once the destination, policies and bundles are approved, engineering—not the owner—will install and
configure the following under a separately recorded change:

1. Separate pgBackRest identities/repositories for `nextops-application-postgresql` and
   `nextops-zabbix-postgresql`.
2. Full and differential schedules, continuous WAL archiving, retention and repository checks.
3. Restic for approved configuration, documentation, permitted evidence, releases and manifests
   only. PostgreSQL data directories, live database snapshots, WAL and unapproved secrets remain
   forbidden.
4. An isolated restore of both PostgreSQL 16 clusters and every approved file class.
5. Point-in-time recovery with Internet disconnected.
6. Interrupted backup, corruption, missing WAL, wrong key, incompatible version and insufficient
   space tests.
7. Key recovery by the secondary custodian.
8. Application/Zabbix compatibility, identity, authorization, session, audit and evidence checks.
9. Measured RPO, RTO, CPU, memory, storage and cleanup evidence.

The owner must provide the maintenance window and be available for the key-recovery step and final
restore observation. Production remains blocked until this command succeeds:

```powershell
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe scripts/check_recovery_profile.py --require-qualified
```

## 7. Configure an owned certificate notification route

The recommended offline-safe route is an internal SMTP relay reachable on the management LAN. A
cloud-only mailbox, Slack/Teams webhook or Internet SMS gateway cannot be the only route. If no
internal SMTP exists, approve another locally operated Zabbix media type and document its owner,
availability boundary and recovery path.

Record privately:

- SMTP host, port, TLS mode and CA trust path;
- authentication method and protected credential reference, if required;
- sender, primary recipient and backup recipient;
- 24×7 or approved active schedule;
- acknowledgement and escalation owner.

From the Zabbix host, test TLS reachability without sending credentials. Enter the values
interactively so they do not enter shell history:

```bash
read -r -p 'SMTP host: ' SMTP_HOST
read -r -p 'SMTP STARTTLS port: ' SMTP_PORT
timeout 15 openssl s_client -starttls smtp \
  -connect "${SMTP_HOST}:${SMTP_PORT}" -servername "$SMTP_HOST" \
  -verify_return_error </dev/null
unset SMTP_HOST SMTP_PORT
```

Then use the Zabbix frontend:

1. `Alerts → Media types`: create/enable the approved internal media type, enable peer and host
   verification for TLS, then use **Test**.
2. `Users → Users → <operator> → Media`: add both recipients, the approved time period and at least
   High/Disaster severities.
3. `Alerts → Actions → Trigger actions`: create a dedicated action limited to tag
   `component=nextops-certificate`; send a problem message and a recovery message through only the
   approved media type.
4. Re-run the guarded certificate-timer failure/recovery test. Both recipients must confirm both
   messages; Zabbix `Alerts` must show successful delivery.

Do not export a media type containing an SMTP password: Zabbix documents that exported email media
configuration can contain the password in clear text.

## 8. Supply replacement certificates for the rotation/rollback drill

Use the organization's offline/internal CA. Do not create an untrusted self-signed production
certificate and do not send the CA private key or leaf private keys through chat or Git.

On each frontend, identify the current certificate path and current SAN set privately:

```bash
sudo sed -n 's/^NEXTOPS_CERTIFICATE_PATH=//p' /etc/nextops/certificate-check.env
sudo sh -c '. /etc/nextops/certificate-check.env; openssl x509 \
  -in "$NEXTOPS_CERTIFICATE_PATH" -noout -issuer -dates -ext subjectAltName'
```

Request a new leaf certificate with the same required names, an approved key algorithm and a
validity period compatible with the 90-day warning policy. Prefer generating the private key on the
target or an approved offline PKI workstation. The owner/CA operator must deliver for each frontend:

- leaf certificate and required intermediate chain;
- matching private key through a protected channel;
- issuing CA chain already trusted by the intended clients;
- non-secret certificate fingerprint and expiry;
- issuer/change reference and revocation procedure.

Before handoff, verify on the protected PKI workstation:

```bash
CERT_FILE='replacement.crt'
KEY_FILE='replacement.key'
CA_FILE='approved-ca-chain.crt'
openssl x509 -in "$CERT_FILE" -noout -dates -ext subjectAltName
openssl verify -CAfile "$CA_FILE" "$CERT_FILE"
CERT_KEY_SHA="$(openssl x509 -in "$CERT_FILE" -pubkey -noout \
  | openssl pkey -pubin -outform DER 2>/dev/null | sha256sum | awk '{print $1}')"
PRIVATE_KEY_SHA="$(openssl pkey -in "$KEY_FILE" -pubout -outform DER 2>/dev/null \
  | sha256sum | awk '{print $1}')"
test "$CERT_KEY_SHA" = "$PRIVATE_KEY_SHA"
unset CERT_KEY_SHA PRIVATE_KEY_SHA
```

After protected staging and owner approval, engineering will arm an automatic rollback guard,
preserve the current pair, verify ownership and pair/chain/SAN/expiry, validate Nginx, atomically
promote and reload, test normal browser/API TLS with Internet denied, then restore the old pair and
repeat all checks. The exercise must end on the explicitly approved pair; it is not an opportunity
to change names, trust roots or validation policy.

## 9. Dependency, license, SBOM and release-integrity approval

Name one legal/license approver and one security approver in the private record. Approve or replace
these recommended policies:

```text
sbom_formats=SPDX_JSON_and_CycloneDX_JSON
release_license_rule=no_unknown_or_unapproved_license
vulnerability_database_max_age_days=7
critical_vulnerability_rule=zero_unresolved_without_written_exception
high_vulnerability_rule=zero_unresolved_without_written_exception
signature_verification=offline_required
signing_key_custody=separate_from_release_builder
```

The currently pinned headline artifacts declare MIT for llama.cpp and pgBackRest, Apache-2.0 for
the Qwen model artifact, and BSD-2-Clause for restic. That is not the complete transitive license
inventory. Engineering will generate SBOMs, resolve every package/license, scan artifacts with a
recorded offline vulnerability-data timestamp, retain Gitleaks, evaluate offline release signing,
and present exceptions for explicit approval. Do not approve the headline list as if it covered all
dependencies.

## 10. Final production acceptance

After every preceding gate passes, the production approver must review the sanitized evidence and
sign a dated decision containing the accepted release identifiers, scope, RPO/RTO, known residual
risks, rollback owner and expiry/review date. Engineering will then re-run:

```powershell
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe -m ruff format --check packages migrations tests scripts deploy/installers
.\.venv\Scripts\python.exe -m ruff check packages migrations tests scripts deploy/installers
.\.venv\Scripts\python.exe -m mypy packages tests scripts deploy/installers
.\.venv\Scripts\python.exe -m pytest -m "not integration and not browser" -q
.\.venv\Scripts\python.exe -m pytest -m browser -q
.\.venv\Scripts\python.exe scripts/check_docs.py
.\.venv\Scripts\python.exe scripts/check_release_status.py
.\.venv\Scripts\python.exe scripts/check_recovery_profile.py --require-qualified
```

Hosted PostgreSQL 16/17 integration, browser and secret-scan jobs must also pass for the exact final
commit. A final offline fresh login/generation/evidence retrieval, service restart, serial VM
reboot, dependency recovery, backup/restore, certificate notification/rotation and rollback must be
recorded against that release. Production is not accepted while any required gate is `failed`,
`partial` or `not_run`.

## 11. What to send back after completing owner actions

Send only this sanitized checklist—never the private record or credentials:

```text
[ ] Independent recovery host provisioned
[ ] Different hypervisor/storage failure domain privately verified
[ ] Restore lab isolated and ready
[ ] SSH host fingerprint independently verified
[ ] nextops-recovery access tested
[ ] RPO/RTO/retention/cadence approved
[ ] Two-person key custody approved
[ ] Connected offline-bundle staging approved
[ ] Internal notification route and two recipients approved
[ ] Replacement app and Zabbix certificate pairs available through protected handoff
[ ] License approver named
[ ] Security approver named
[ ] Production approver named
change_id=<non-secret identifier>
```

Once this checklist is complete, engineering can continue without requesting passwords or private
keys in chat.

## Official references

- [pgBackRest 2.59.1 user guide](https://pgbackrest.org/user-guide.html)
- [restic 0.19.1 repository checks and restores](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)
- [Zabbix 7.0 media types](https://www.zabbix.com/documentation/7.0/en/manual/config/notifications/media)
- [Zabbix 7.0 email media](https://www.zabbix.com/documentation/7.0/en/manual/config/notifications/media/email)
