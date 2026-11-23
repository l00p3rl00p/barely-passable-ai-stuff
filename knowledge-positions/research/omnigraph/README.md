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

## Ingestion extension contract

**Every parser feeds the same Knowledge Positions representation. Adding support for a new file format requires adding a reader, not changing the ingestion architecture.**

**The architectural rule is: detect → select parser → extract → establish knowledge → persist.**

Parsing is not understanding. For example, an image reader can establish dimensions, format, metadata, source location and other mechanically observable characteristics without interpreting what the image depicts. Intelligence can interpret the image later, when needed, and contribute qualified findings through the existing knowledge contract. This distinction applies to every format: ingestion establishes discoverability and observable structure; contextual meaning emerges through use. No inference or semantic embedding is a prerequisite for admission.


Readers detect and extract source-native structure, exact locators, observable relationships and available content or metadata. All readers use the same canonical admission and representation contract: Position, Relation, Proximity; Resonance remains research. Parser-specific coordinates are expressed through the existing location fields, not a separate ontology. Deterministic lexical proximity uses the declared compatible space; no synthetic semantic embedding. Unsupported or unreadable assets remain discoverable by name, location, identity and available metadata; unknown information stays unknown. Archives may expose member listings and member coordinates without executing or extracting unsafe payloads. Rust is an independent ingestion utility; OmniGraph persists the resulting records through its native write interface. Adding a reader must not require modifying the graph schema, write adapter, orchestration, permissions or existing readers. A genuine change to the universal knowledge contract is a separate, deliberate research decision, not a parser addition.

## Deployment examples and Rust prerequisites

See [RUNBOOK.md](RUNBOOK.md#native-permission-configuration-and-semantic-provider-removal) for the three native permission YAMLs and provider-free cluster examples. These illustrate the agreed role configuration; the universal representation remains permission-agnostic. See [Rust build prerequisites](rust-dependencies/README.md) for separate dependency preparation. The Rust ingestion implementation is independent of this bundle.
