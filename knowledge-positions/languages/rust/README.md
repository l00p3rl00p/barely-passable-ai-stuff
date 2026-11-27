# Rust — existing native components
[Back to the SDF guide](../../SDF/README.md) · [Implementation cookbook](../../docs/implementer-guide.md)

The active native Rust implementation lives in a separate development workspace. Do not rebuild the universal scanner when adding a target. The following source links were inspected at quatrus-scratchpad commit [268605b](https://github.com/l00p3rl00p/quatrus-scratchpad/commit/268605b); they identify actual code, not claims of current installed binary versions.

| Component | Actual source | Status at inspected revision |
|---|---|---|
| Universal extractor | [extract.rs](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/extractor-review/extract.rs), [Cargo.toml](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/extractor-review/Cargo.toml) | Target-independent native extraction. |
| OmniGraph emitter | [lib.rs](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/jitk/rust-scanner/omnigraph-writer/src/lib.rs), [Cargo.toml](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/jitk/rust-scanner/omnigraph-writer/Cargo.toml) | Native serialization and bulk writes. |
| KP writer | [binary](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/jitk/rust-scanner/omnigraph-writer/src/bin/kp-omnigraph-writer.rs), [kp.rs](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/jitk/rust-scanner/omnigraph-writer/src/kp.rs) | Touch 0 exists; oversized addresses skipped at inspected revision. |
| KP enricher | [binary](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/268605b/jitk/rust-scanner/omnigraph-writer/src/bin/kp-omnigraph-enricher.rs) | Legacy re-key only at inspected revision; required grouping not implemented. |

See the [review evidence](../../conformance/sdf-independent-review.md) for verification limits and the [capture](../../contracts/common-record.md), [lifecycle](../../core/lifecycle.md), [operations](../../contracts/public-operations.md) and [conformance](../../conformance/requirements.md) contracts for expected behavior. The older [Rust workspace](https://github.com/l00p3rl00p/quatrus-scratchpad/tree/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph) remains a historical development reference. No current install, build or live database run is claimed here.
