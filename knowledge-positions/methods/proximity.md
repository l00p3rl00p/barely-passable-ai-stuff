## 7. Proximity: useful even when imperfect; never blocking

The common record may contain declared proximity values or indicate that a specific computed value is unavailable; it does not require a separately managed proximity slot. Cheap lexical/hash computation can be run from the recorded literal values when requested or as an independent derived calculation. Semantic/neural embedding, if used, is optional and can happen later. An incomplete vector does not invalidate source/location/relations and MUST NOT block searches available through those values.

**Required vector-space descriptor:** space ID, dimensions, exact encoder algorithm and version, tokenization/Unicode/preprocessing, stop words, sign convention, input policy, normalization, numeric representation and source-content digest where applicable. A query must use the same space as stored vectors. Mismatched spaces are rejected, not silently compared.

**Observed real incompatibility:** [original GPS encoder](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/examples/gps/gps.py) and [Rust-scanner-compatible encoder](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/research/omnigraph/encoder.py) both historically used the label “lexical-hash-512” but differ in stop-word and sign behavior. They are **NOT** interchangeable. Name their profiles distinctly (e.g. **lexical-hash-512/gps-legacy-v1** versus **lexical-hash-512/rust-scanner-v1**) and verify cross-language output with the same actual source strings. No language or ML model is pinned; exact behavioral compatibility is.

An approximate proximity result MUST return a candidate canonical ID and source/evidence route. Proximity score alone is not a verified relation or an answer.

