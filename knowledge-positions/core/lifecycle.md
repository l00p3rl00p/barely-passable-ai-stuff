## 11. Lifecycles, updates, concurrency, storage and performance

**Sources and accepted discoveries are durable. Projections are disposable.** An implementation MAY use JSON, SQLite, LadybugDB, OmniGraph, NetworkX, Rust containers, distributed storage or a vector DB. Its physical layout is immaterial provided the logical record and observable operations remain exact.

Admission MUST be idempotent. A source version change must preserve evidence and supersession history and update only affected positions/edges. Concurrent writers must use transactions or a coherent serialization strategy, not silently overwrite accepted deltas. Unknown or ambiguous source read failures remain visible.

**Deterministic ingestion captures available knowledge once, not representations in sequence.** Use any faithful source-native reader to preserve naturally occurring values together in the common record, beside source evidence. Retrieval methods directly consume those fields; no AST→graph→vector or other staged translation. Missing computed values may be calculated independently from the common recorded inputs, if actually required, without reconstructing earlier methods. Compute expensive vectors or optional new relationships separately as needed. Reuse unchanged hashes, records and positions. A large folder scan is not a whole-corpus intelligence job. Rebuild indexes instead of designing expensive recovery machinery whenever source reconstruction is faster and preserves all accepted knowledge.

Do not invent a benchmark threshold: measure with real input size, wall time, memory, store size, and LLM-call count. The zero-required-LLM-call condition for ordinary ingestion is normative.

