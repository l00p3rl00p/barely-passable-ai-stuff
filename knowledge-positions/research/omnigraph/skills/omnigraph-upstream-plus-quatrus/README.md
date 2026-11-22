# OmniGraph skill + append-only Knowledge Positions integration

This directory provides a **version-matched official OmniGraph skill with appended guidance**, not an OmniGraph fork or a replacement engine.

## What this package contains

- [`SKILL.md`](SKILL.md) — the **unchanged official upstream `v0.15.0` `skills/omnigraph/SKILL.md`** followed at EOF by the two appendices listed below.
- [Generic JITK appendix](../../../../skills/appendices/jitk.md) — reuse → direct source → evidenced relationships → discovery; choose actual available access methods, verify original evidence, and delegate execution to the selected implementation.
- [`quatrus-ingestion.appendix.md`](quatrus-ingestion.appendix.md) — the existing, user-supplied Quatrus section copied as a separate optional deployment-specific appendix.
- [Append-only helper](../../../../skills/appendices/append-to-skill.sh) — adds either/both sections to an existing installed skill without editing its original instructions.

**Original source:** [ModernRelay OmniGraph `v0.15.0` official SKILL.md](https://github.com/ModernRelay/omnigraph/blob/v0.15.0/skills/omnigraph/SKILL.md). The original upstream content ends immediately before `<!-- knowledge-positions-jitk:start -->`. The Quatrus-specific instructions are enclosed by `<!-- quatrus-ingestion:start -->` and `<!-- quatrus-ingestion:end -->` and do not modify any upstream paragraph.

## Why version `v0.15.0`?

The supplied active OmniGraph skill declares **version `0.15.0`**. Using its matching upstream release separates upstream instructions from the local additions without silently upgrading command contracts. The upstream `main` skill may be newer. For an installed different version, **keep the official version-matched skill** (e.g. from `omnigraph skill export`), then append these sections. Do not replace a current, matching official skill with the older bundled file.

## Install without touching upstream instructions

Obtain or retain the **entire official OmniGraph skill directory**, including its `references/` files. This repository's combined `SKILL.md` is a reviewable assembled artifact; its upstream `references/` links still require the official companion files. The installed CLI's version-matched export is preferred when available.

From a checkout of this repository:

```sh
# Generic JITK behavior for ANY already installed skill:
bash knowledge-positions/skills/appendices/append-to-skill.sh /path/to/your/SKILL.md

# Add both generic behavior and the existing Quatrus OmniGraph profile
# (only to an OmniGraph skill in the explicitly configured Quatrus environment):
bash knowledge-positions/skills/appendices/append-to-skill.sh /path/to/omnigraph/SKILL.md --quatrus
```

The helper changes the destination only by **appending text at EOF**. It refuses a nonexistent target or a non-OmniGraph target for `--quatrus`. It detects the section markers and skips already-added appendices, making repeat application idempotent. It neither launches the CLI nor starts an ingestion operation.

## What stays generic, and what stays local

**Generic JITK:** The same appendix works with a parser, AST reader, filesystem source resolver, graph store, structured database, embedding index or agent tool. It asks which actual capabilities are accessible, selects the useful method, and resolves original evidence. It neither assumes OmniGraph nor requires loading the entire [UKC SDK](../../../unified-knowledge-context.md).

**Quatrus profile:** Target `kp-agent`, graph `knowledge`, branch `kp-working`, `kp_rescan`, `kp_read`, LinkML, credentials and source-allowed-root rules are **existing local deployment choices**, not generic JITK or OmniGraph defaults. They are meaningful only where those installed services and permissions are present. Keep them outside the portable appendix.

**Native OmniGraph operations:** The official skill remains authoritative for `.pg` schemas, `.gq` queries, security, branching, loads, retries and native CLI behavior. The JITK appendix never overrides that policy.

## Validation and update rule

1. Compare everything before the first `<!-- knowledge-positions-jitk:start -->` marker with the matching official release file. They must be byte-for-byte identical.
2. Verify each appendix is present once and begins after the entire upstream document.
3. Verify the installed CLI version and permissions before executing any listed OmniGraph command; this documentation assembly does not prove the configured Quatrus services are available.
4. On an upstream upgrade, export/obtain its **new official skill and references first**, then append the same sections. Never patch its internal paragraphs, silently apply old command assumptions, or overwrite other local additions.

This package does **not** create a new SDK implementation, ingestion runtime, graph schema, tool server, or background process.
