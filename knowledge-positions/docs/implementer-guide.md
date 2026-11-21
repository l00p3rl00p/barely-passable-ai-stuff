## 12. Implementer's exact procedure

1. Read and implement **First Law**. No parser, DB or language choice changes it.
2. Use any suitable faithful source-native reader to obtain naturally occurring literal values, relationships, structure, coordinates and source evidence.
3. Establish one canonical ID and record all observed values **once** in the common OKF-compatible record, preserving the original information beside them. Do **not** create independent structural, graph and vector versions.
4. Have structural, graph, fuzzy/lexical and vector methods select their needed shared values directly from that record. If a required computed value is missing, the particular operation can calculate or request that value independently; it must not convert another retrieval representation or delay unrelated operations.
5. Prove complete lossless OKF-compatible import/export; preserve native extension values.
6. Add cheap lexical/fuzzy discovery and declared compatible vectors independently of record admission.
7. Implement qualified on-touch enrichment as **additive evidence-backed deltas**, not a mandatory scan phase.
8. Support version-verified exact source resolution, privacy boundaries, incremental updates and reconstruction from durable evidence.
9. Run and publish the conformance suite; show failures honestly. Compare Python, Rust and every new implementation against identical fixtures.
10. Wire OmniGraph, MCP, a CLI, an agent or a UI **after** the contract works, as consumers—not as alternative definitions of knowledge.

**Finished means:** an independent implementer can write the SDK in any execution language and obtain the same identities, captured values, observed edges, known/unknown positions, exact source evidence and cross-method navigation from identical fixtures. If the result requires interpretive re-ingestion or loses the common identity, it is not UKC.

