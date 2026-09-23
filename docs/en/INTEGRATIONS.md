# Integration scope and capability status

[فارسی](../fa/INTEGRATIONS.md) · [Index](INDEX.md)

**The Zabbix status slice is accepted for controlled user testing. Phase 2A now implements and tests
bounded Zabbix history/event collection in source, but it is not yet deployed or live-accepted.
The other ten integration families remain planned.** Source: original specification sections 5 and
11–21; enhanced specification section 15. The rows preserve requirements, not claims that every
vendor API exposes every field.

| Family | Required diagnostic scope | Communication and compatibility checks | Phase |
|---|---|---|---|
| Linux | CPU/RAM/disk, load/uptime, processes, systemd/services, logs/journal, filesystems, users/packages, ports/sockets, routes/DNS/network | Verified SSH or approved local adapter; named bounded diagnostics; narrow permissions | 2 |
| Windows | CPU/RAM/disk, services/processes, Event Viewer, network/DNS/routes/ports, updates, users, PowerShell and AD-related diagnostics | Supported authenticated management transport; constrained commands/JEA where available; no unencrypted Basic auth | 3 |
| Cisco IOS/IOS-XE | Interfaces/errors, VLAN/trunk/STP, routes/ARP/MAC, BGP/OSPF/DHCP, ACL/NAT, health/logs/configuration | Supported NETCONF/RESTCONF or structured APIs where available, otherwise verified SSH; version-specific parsers | 3 |
| Juniper Junos | Interfaces/VLAN/routes/ARP/MAC, BGP/OSPF, firewall filters, health/logs, configuration/diff/commit status | NETCONF/PyEZ or supported API/SSH; commit/rollback only in a later controlled mutation path | 3 |
| FortiGate | Interfaces/routes/policies/objects/services, sessions, VPN/IPsec/SSL VPN, HA, DHCP/DNS, health/logs/configuration | Verify API/version/VDOM and permissions; API or restricted SSH; collect VPN phase/routing/policy evidence | 4 |
| Sophos | Firewall health, interfaces/routes/rules/NAT, VPN phases, DHCP/DNS, sessions, HA/logs/alerts | Distinguish Firewall from Central APIs; verify product version, API coverage and licensing; unavailable telemetry stays unsupported | 4 |
| Zabbix | Hosts/groups/templates/items/triggers/problems, events, history/trends, latest data and graph metadata | Authenticated API; bounded queries, pagination, retention awareness and event deduplication | 2 |
| Grafana | Dashboards/folders/panels/datasources, alerts/annotations and supported queries | Dashboard metadata is not the metric store; verify datasource query paths, permissions and scoped tokens | 3 |
| SQL Server | Health, databases/tables/indexes, sessions/connections, locks/blocking/deadlocks, waits, query performance, jobs/backups | Supported driver/TLS and least-privilege diagnostics; verify DMV access and server version | 5 |
| MySQL/MariaDB | Databases/tables/indexes/users, connections/processes/locks, slow queries, replication, health/status/variables | Detect engine/version; predefined bounded queries and read-only identities; no unrestricted SQL | 5 |
| VMware ESXi | Host health/CPU/RAM, datastores/network, VM inventory/power state/snapshots/disks/NICs, performance, alarms/events/logs | Verify API/version/license; preserve vCenter extension point; power/snapshot/delete changes are not implicitly permitted | 5 |

## Required connector dossier

For each family, record supported and explicitly unsupported actions, tested OS/vendor/API versions, minimum permissions, authentication and transport, secret-reference requirements, limits, schema versions, simulator fixtures, real-device test evidence, failure modes and known limitations. Do not use a green “healthy” response for an unimplemented adapter.

Status vocabulary is strict: **planned** means specified only; **simulated** means tested on fixtures; **lab-verified** requires authorized real equipment and a versioned test record; **production-validated** requires separately authorized deployment evidence. A family-level label never implies every operation or version has that status.

## Phase 2A source increment

The additive incident-context operation reuses the configured host and returns its current summary,
up to four numeric item histories with eight points each, and up to 25 trigger events from a fixed
60-minute window. It calls only named `history.get` and `event.get` reads, preserves source and
collection timestamps, and marks truncation or inherited summary gaps explicitly. Callers cannot
select a different host, arbitrary method or unbounded time range. The authenticated connector and
application routes are source-tested; live role expansion, deployment, durable investigation/model
integration, browser acceptance and direct Linux diagnostics remain Phase 2 work.

## Cross-system investigations

The first slice correlates Zabbix problems/history with Linux diagnostics and returns a Persian evidence-linked answer. Later network investigations combine time-bounded Zabbix/Grafana observations with interface errors and topology. Firewall investigations examine VPN phase, routing, policy and logs rather than guessing from one symptom. Database and ESXi diagnoses remain read-only by default.

Collect data within the user's allowed asset/environment scope, enforce query/time/output limits, preserve source timestamps, label redaction and partial results, and distinguish correlation from confirmed causation. NextOps-host maintenance needs separate protection against locking out its own operator.

## Future extensions

Active Directory, vCenter, Proxmox, MikroTik, Kubernetes, Docker, Sophos Central, cloud platforms, storage and backup systems remain extension points. They are not silently included in MVP. Adding an adapter should use existing contracts rather than rewriting core orchestration.
