# Rust SDK — existing native components

Rust source already exists in a separate development workspace: [JITK Rust workspace](https://github.com/l00p3rl00p/quatrus-scratchpad/tree/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph).

Its verified source paths include [workspace `Cargo.toml`](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph/Cargo.toml), [scanner manifest](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph/scanner/Cargo.toml), and [ingest manifest](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph/ingest/Cargo.toml). They declare `jitk-scan` and `jitk-ingest` **executables**, with native parsers, Parquet output and an OmniGraph loading path.

**Do not turn these binaries into a replacement SDK or claim they implement the full UKC/1 interface.** Their source exists; they are not a Rust library package distributed from this `languages/rust/` location. No build or functional acceptance was run as part of this SDK packaging work.

Rust integrations must preserve [canonical identity](../../core/identity.md), the [common record](../../contracts/common-record.md), and the [public operations](../../contracts/public-operations.md) without reimplementing Knowledge Positions authority or changing the existing native boundary. Use the [capability map](../../docs/component-and-capability-map.md) to identify available code and unverified gaps.
