## 11. Lifecycles, updates, concurrency, storage and performance

**Sources and accepted discoveries are durable. Projections are disposable.** An implementation MAY use JSON, SQLite, LadybugDB, OmniGraph, NetworkX, Rust containers, distributed storage or a vector DB. Its physical layout is immaterial provided the logical record and observable operations remain exact.

### Authoritative touch lifecycle

| Stage | Touch | Required behavior |
|---|---|---|
| Native parse and emit | None | Independent of KP; native output is preserved. |
| Writer | 0 | Deterministic admission; preserve supplied observed edges and fields, no interpretation. |
| Enricher | 1 | Deterministic block grouping, structure and supported evidence-backed fields; no manufactured facts. |
| Intelligence enrichment | 2, 3 | Qualified later semantic deltas; after 3 freeze payload and grow outward through new knowledge and supported links. |

Reads, retrieval and reconstruction do not consume touches. A verified source-version change opens a new epoch. Existing native relations are available without additional enrichment. Grouping an incomplete event stream must not erase the admitted native observations. A cluster created during deterministic enrichment starts at touch 1; a mere admission grouping identifier is not itself enrichment. Preserve source-change rejection and evidence history. OKF interchange uses upstream lifecycle vocabulary; internal lifecycle representations may differ if stale source evidence cannot be treated as current. The legacy Python reference retains its historical admission/status behavior until an explicitly tested compatibility change; it is not proof of this updated lifecycle.

### Block grouping

A kit MUST support evidence-backed, navigable grouping of knowledge blocks where the source supports grouping. This is a framework requirement, not a prescription for a particular parser or database. The enricher at touch 1 evaluates native grouping first, reuses it where sufficient, and may improve or extend it deterministically when useful. Preserve the original hierarchy, ordering, values, identities and provenance; additional grouping must not overwrite them. Record the grouping rule and the evidence supporting its boundaries and relationships. Report unsupported/not-applicable cases honestly.

For Start/End event streams, a matched Start(tag)…End(tag) pair defines a candidate block; containers may contain blocks and inline events fold into the nearest applicable block. A reader declares its stable unit-key convention (Start sequence or verified byte range). An incomplete or unmatched block remains ungrouped until supported; all original events and diagnostics remain preserved. Do not fabricate groupings or delete ungrouped observations. Native AST, DOM or other already-grouped inputs need no redundant reconstruction, but may support useful additional groupings. Verify grouping and relationship behavior using actual observations and the common identity contract.

Admission MUST be idempotent. A source version change must preserve evidence and supersession history and update only affected positions/edges. Concurrent writers must use transactions or a coherent serialization strategy, not silently overwrite accepted deltas. Unknown or ambiguous source read failures remain visible.

**Deterministic ingestion captures available knowledge once, not representations in sequence.** Use any faithful source-native reader to preserve naturally occurring values together in the common record, beside source evidence. Retrieval methods directly consume those fields; no AST→graph→vector or other staged translation. Missing computed values may be calculated independently from the common recorded inputs, if actually required, without reconstructing earlier methods. Compute expensive vectors or optional new relationships separately as needed. Reuse unchanged hashes, records and positions. A large folder scan is not a whole-corpus intelligence job. Rebuild indexes instead of designing expensive recovery machinery whenever source reconstruction is faster and preserves all accepted knowledge.

Do not invent a benchmark threshold: measure with real input size, wall time, memory, store size, and LLM-call count. The zero-required-LLM-call condition for ordinary ingestion is normative.

