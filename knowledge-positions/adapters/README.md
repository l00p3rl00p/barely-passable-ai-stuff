# SDK adapters — existing integrations

Adapters bind the language-neutral [UKC/1 public contract](../contracts/public-operations.md) to an existing source, parser, graph engine or application. **They do not own or redefine the knowledge record.**

## Existing source and graph boundaries

For the current Rust extractor and OmniGraph kit source, start at [Rust components](../languages/rust/README.md). The Python adapters below are historical/reference implementations, not the active Rust kit.

- [Deterministic reader/adapter contract](../readers/source-adapters.md) — required native-field fidelity and source evidence.
- [Existing OmniGraph adapter](../research/omnigraph/adapter.py) — source rows, native queries and mutations through an existing engine.
- [Existing OmniGraph schema](../research/omnigraph/schema.pg) and [queries](../research/omnigraph/queries/kp.gq) — engine-specific projection and retrieval.
- [Official OmniGraph skill](https://github.com/ModernRelay/omnigraph/blob/main/skills/omnigraph/SKILL.md) — authoritative native operational guidance.
- [OmniGraph agent startup profile](omnigraph/agent-startup.md) and [JITK host profile](omnigraph/jitk-host-contract.md) — **optional host behavior**, not UKC/1 conformance conditions.

The [capability map](../docs/component-and-capability-map.md) documents what is demonstrably present and what has **not** been proven. No adapter was built, moved or installed for this documentation package.
