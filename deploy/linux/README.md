# Phase 2 Linux collector deployment assets

The four JSON files are public, non-secret allowlists for the matching logical targets. The
installer validates by default and changes a target only with `--apply`. See the paired
[English](../../docs/en/PHASE_2_OPERATIONS.md) and
[Persian](../../docs/fa/PHASE_2_OPERATIONS.md) operational guides before use.

Never place a private key, real address, host key, or completed environment registry in this
directory. The environment-specific registry belongs at `/etc/nextops/linux-targets.json` on the
connector server and must remain root-owned.
