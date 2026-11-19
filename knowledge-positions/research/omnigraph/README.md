# OmniGraph representation of Knowledge Positions

**Knowledge = { Position. Relation. Proximity. Resonance. }**

This is a portable representation of the research, not a fork of OmniGraph or a new service. Native OmniGraph owns persistence, queries, ordinary writes, collaboration, history, branches and permissions. The canonical Knowledge Positions library owns capture rules. The adapter translates those rules to native writes.

- Position: verified source and within-source coordinates (AST where applicable).
- Relation: evidence-qualified directed graph relationships.
- Proximity: deterministic lexical-hash-512 (scanner space); no semantic inference.
- Resonance: experienced importance determined by use; research only, no invented implementation.

OKF documents are human-readable Markdown with YAML frontmatter. The schema projects knowledge into OmniGraph; the source document remains authoritative. Domain is optional and explicit, not an access rule. Meaning is contributed by intelligence during work, not calculated at ingestion. No JITK runtime or prompt hook, Rust bulk ingester, extra MCP, provider, or custom permissions included.

Start with [RUNBOOK.md](RUNBOOK.md) only to install or repair. The [independently installable skill](skills/knowledge-positions-omnigraph/SKILL.md) uses progressive disclosure: reuse, direct access, immediate relations, then discovery; never load the whole cookbook or graph by default. Keep original source documents, reviewed findings and evidence; the graph is a reconstructable projection only to the extent those materials survive. No bulk migration or destructive upgrade is included.

Canonical library: [knowledge_positions.py](../../knowledge_positions.py). The bundled copy in this folder is an unmodified distribution snapshot (source blob 3f6972980a669714dc359ca27df55c1a9e02cb9d), not a second maintained implementation. Refresh it from the canonical file when packaging a new release. The lexical encoder is the established scanner-compatible variant; it is not the distinct capture.py encoder with the same historical space name. Do not mix the two.

Status: package derived from existing code and native 0.15 CLI documentation; live acceptance requires the commands in the runbook on a machine with OmniGraph. No claim that this bundle has been executed against OmniGraph.
