# Offline server package installers

These four entry scripts install the exact Ubuntu package lock for one approved server role:

| Server | Script | Minimum direct packages |
| --- | --- | --- |
| `nextops-app` | `install-nextops-app.sh` | CA certificates, Python 3.12/venv, PostgreSQL 16 client/server, libpq, Nginx |
| `nextops-ai` | `install-nextops-ai.sh` | CA certificates, C/C++ build tools, CMake, Ninja, pkg-config, OpenBLAS development/runtime, libgomp |
| `nextops-connectors-ro` | `install-nextops-connectors-ro.sh` | CA certificates, Python 3.12/venv |
| `zabbix-server` | `install-zabbix-server.sh` | Zabbix 7 server/frontend/SQL/Agent 2 packages, PostgreSQL 16 client/server, Nginx, PHP 8.3 FPM/PostgreSQL support, CA certificates |

The bundle's `packages.lock` must also list every transitive package as an exact Debian
`name=version` entry. APT is isolated from the guest's configured repositories, accepts only the signed
local repository, simulates the transaction, rejects unlisted package changes/removals, downloads the
complete lock, installs it, and verifies every installed version.

## Scope

This is the package layer, not a complete NextOps deployment. The scripts deliberately do **not**:

- partition disks, create filesystems, initialize PostgreSQL, import a schema, or create credentials;
- build or install the NextOps application, connector, browser UI, llama.cpp binary, or model;
- write Nginx, PHP, Zabbix, application, inference, connector, firewall, or systemd configuration;
- start or enable services; or
- download from the Internet.

Those inputs are still missing or separately gated in the matching file under
`deploy/server-dependencies`. PostgreSQL package installation leaves
`/etc/postgresql-common/createcluster.conf` with `create_main_cluster = false`; database initialization
must be a later reviewed change after the intended mount is proven.

## Required bundle

Prepare one role-specific bundle in an approved connected build environment, transfer it through the
approved offline process, and retain its build evidence. The imported layout is:

```text
<bundle>/
├── manifest.sha256
├── packages.lock
├── keyrings/
│   └── nextops-archive-keyring.gpg
└── apt/
    ├── dists/stable/InRelease
    └── pool/.../*.deb
```

Requirements:

1. `packages.lock` contains one exact `name=version` entry per line, including the complete dependency
   closure. Blank lines and full-line comments are allowed.
2. `apt` is a complete `stable/main` Debian repository whose `InRelease` is signed by the imported
   keyring. It contains every locked package; public repository URLs are not accepted.
3. `manifest.sha256` lists every other regular file in the bundle exactly once using
   `<lowercase-sha256><two spaces><relative-path>`. Symlinks and unlisted files are rejected.
4. The SHA-256 of `manifest.sha256` is copied to the private approved change record through a channel
   separate from the bundle. It is the operator-supplied trust anchor.
5. Before apply, the complete bundle tree and every parent directory are owned by root and are not
   group/world writable. This closes the file-swap window between verification and APT.

The repository intentionally does not contain a package lock or signing key because exact maintained
Ubuntu/Zabbix patch versions and the private signing process have not been approved yet.

## Validate without changes

Run from the reviewed repository checkout. Replace the example paths and digest with values from the
private change record:

```bash
./deploy/installers/install-nextops-app.sh \
  --check \
  --bundle-dir /srv/nextops/import/nextops-app \
  --bundle-manifest-sha256 "$APP_BUNDLE_MANIFEST_SHA256"
```

`--check` authenticates the complete bundle and checks the role lock. It does not call APT or modify the
host. Repeat with the entry script and bundle for each server.

## Apply in an approved change window

First finish the matching dossier's guest, storage, time, listener, backup, and rollback preflight. Then
make the imported tree immutable to non-root users and execute the role's script:

```bash
sudo chown -R root:root /srv/nextops/import/nextops-app
sudo chmod -R go-w /srv/nextops/import/nextops-app

sudo env NEXTOPS_PROVISIONING_AUTHORIZED=YES \
  ./deploy/installers/install-nextops-app.sh \
  --apply \
  --bundle-dir /srv/nextops/import/nextops-app \
  --bundle-manifest-sha256 "$APP_BUNDLE_MANIFEST_SHA256" \
  --change-id CHG-APP-PACKAGES
```

Apply fails unless the guest is Ubuntu 24.04 under VMware, the process is root, the explicit authorization
marker and safe change ID are present, all bundle paths are root-owned/non-writable by other users, and
the local repository transaction matches the exact lock. A temporary `policy-rc.d` prevents package
post-install scripts from starting services and is removed only if it remains unchanged. A pre-existing
`policy-rc.d` causes a fail-closed stop for separate review; the installer never overwrites it.

After a successful package run, capture the command result and installed-version evidence in the private
change record. Stop there: do not initialize databases, deploy artifacts, open ports, or start services
until the next dossier gates have reviewed implementation and acceptance evidence.

## Reference basis

- [Ubuntu package-management guidance](https://ubuntu.com/server/docs/how-to/software/package-management/)
- [Zabbix 7.0 installation from packages](https://www.zabbix.com/documentation/7.0/en/manual/installation/install_from_packages)
- [PostgreSQL packages for Ubuntu](https://www.postgresql.org/download/linux/ubuntu/)
- [llama.cpp build instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)

These references identify package families and supported build mechanisms. They do not select the exact
maintained versions, authenticate a private bundle, or prove compatibility on the target servers.
