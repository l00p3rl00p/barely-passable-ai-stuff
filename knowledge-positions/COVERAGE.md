# Coverage, evidence and warnings

This folder contains the small Python library, original reference specifications, runnable examples/tests, and the evolving research paper. Reference specifications describe the intended design; this file distinguishes what the implementation actually supports from what remains unimplemented.

## Traceability

| Concern | Existing design coverage | Executable evidence / remaining warning |
|---|---|---|
| Three positions | [Relationships, sections 3–4](Knowledge_Graph_Relationships_and_Enrichment.md) | [library](knowledge_positions.py): add, ingest_python, link, search; notebooks check AST spans, vectors, persistence. |
| Hashing original source | [Evolution, Part II](Knowledge-Asset-Evolution-Spec-v1.6.3.md) | ingest_python records whole-file SHA-256; add records span text SHA-256; GPS read verifies source and span. Notebook checks tampering rejection. Hash is integrity, not truth. |
| Independent author/file hash gates | Evolution Part II, Layer 3 | Not implemented by this library: whole-file and span hashes are NOT independent ownership gates. |
| Meaningful edges and provenance | Relationships sections 1–4 | `link` accepts qualified relation/evidence and implements status propagation for dependency edges; it does not independently establish that an asserted relation is true. GPS `shared_terms` remains lexical co-occurrence, not meaning. |
| Semantic search | Library design | Sentence Transformers supported; GPS trial used lexical hashed vectors. Notebook runs real model; paraphrase quality unmeasured. |
| Hybrid ranking / corpus-specific noise | Not explicitly specified in the two documents | Other LLM critique: merge lexical/semantic rankings optionally; downweight corpus-common terms; currently not implemented. |
| Context windows / top-N scaling | Relationships section 4 calls for smallest connected set | `chat_context` now defaults to Personalized PageRank / random-walk-with-restart attenuation with transparent conservative/balanced/aggressive profiles and boundary references in `other`; explicit ego radius remains available. Corpus-scale calibration and token-efficiency measurements remain incomplete. |
| Cold context retrieval | Relationships section 4 | [GPS experiment](examples/gps/README.md): observed four-passage independent-agent trial, not a benchmark. |
| Cascading invalidation | Relationships section 2 specifies invalidation and impact, Evolution Part II detects changes | **Implemented and regression-tested:** explicit `derived_from` / `depends_on` / `requires` dependencies cascade staleness independently of working-context retrieval scope; unrelated similarity edges do not. Caller supplies source changes; there is no automatic file watcher. Mechanism informed by [Noosphere Lite](https://github.com/Garyu-tt/noosphere-lite-mcp), with no upstream code imported. |
| Repeated enrichment / promotion | Evolution layers 3–4; Relationships section 4 | **Implemented mutation guard:** admission is touch 1; `enrich_node` permits only touches 2 and 3 on a node/cluster payload, then freezes it while allowing outward relationships. A verified new source version starts a fresh epoch. Node and cluster budgets are persisted through JSON save/load; regression coverage is committed, while the full current suite has not been executed in this review. Automatic host write-back remains separate and is not installed. |
| Hash omissions | — | Graph JSON, edge evidence, model revisions and generated FTS index are not independently integrity-verified; source read verifies whole file each time. No claim of tamper-proof storage. |

## Reusable structural positions — November 11, 2026

The existing Python AST reader now records `item_location`: ordered node path, parent path, depth, sibling index, source-version scope, basis and precision. The new generic `record_item_position` API accepts structural coordinates from other source readers and qualified model/human observations. It avoids changes to node IDs, stored vectors and original source hashes; parser-derived metadata is not downgraded by a later locator-only observation.

`positioned_embedding_input` verifies original text against its stored hash and composes optional positional context for an encoder. It does **not** automatically compute or replace vectors; any improvement from position-aware embeddings requires measured experiments.

[Regression test source](test_item_positions.py) now includes Python AST path tagging, structural-only ingestion without embedding calls, path-free line/anchor coordinates, method precedence, no-downgrade, novel-method catalog persistence, source-version conflicts and JSON round-trips. These test cases are **committed but have not been executed against the current complete GitHub library in this review**; earlier three-test smoke results predate the additional cases and cannot establish their success. No GitHub Actions workflow was enabled. Non-Python reader adapters, an automatic watchdog and direct LadybugDB persistence are not installed.

## Run

From this directory:
```bash
python -m pip install . jupyterlab marimo
jupyter lab knowledge_positions_demo.ipynb
marimo edit knowledge_positions_demo.py
```

Both notebooks are authored to exercise analogous checks; a current complete run with the real semantic embedding model has not been independently established here. First semantic-model use may require downloading the model unless cached. The GPS example builds a temporary index and tests hash failure; it never modifies the repository source. The published fixture is illustrative and not private. For the actual blind trial, give the agent only the index and tools, not source or recorded results. Use IDs returned by the current build, not historical IDs, if they differ.

## References

[Library README](README.md) · [GPS example](examples/gps/README.md) · [Evolution v1.6.3](Knowledge-Asset-Evolution-Spec-v1.6.3.md) · [Relationship vocabulary](Knowledge_Graph_Relationships_and_Enrichment.md).

Validation status: notebook source authored for reproducibility; full notebook execution requires local dependencies and model access. No new empirical claims from unexecuted cells.

## Reconciled design decisions and follow-up experiments

These notes record the missing decisions from the development discussion, not an additional implementation or disclosure of the wider project.

- **Agent-directed investigation:** the agent selects exact, fuzzy, semantic or graph discovery and decides when evidence is sufficient. NetworkX executes its chosen graph operations. Optional hybrid ranking and bounded context windows reduce tool calls, not agent autonomy. A deterministic initial lookup is optional, not a mandatory pre-inference pipeline.
- **Two retrieval modes:** known addresses can be supplied directly to a cold agent; unknown addresses are discovered by search and traversal. Both require a working source resolver. The GPS experiment demonstrated discovery with a human resolver, not automated cold-start injection or retrieval at ten-year scale.
- **Incremental enrichment:** reuse existing nodes and embeddings for unchanged source versions; record new qualified relationships and evidence from ordinary investigations. The sixth retrieval is a proposed promotion trigger, not a truth or confidence threshold. No automatic counter or write-back is implemented.
- **Temporal knowledge:** prefer the applicable current version, not simply the newest timestamp. Preserve historical versions, explicit supersession and contradictory evidence. On source drift, traverse explicit derivation dependencies and mark affected claims stale for review; do not cascade through lexical similarity or silently rewrite claims. See [architecture](ARCHITECTURE.md) and [Noosphere attribution](ATTRIBUTION.md).
- **Graph freedom:** the agent may create its own NetworkX graph, projections and traversal. AST/Tree-sitter are optional source extractors. The stored graph and its derived views are not a compulsory tree or ontology.
- **Hash boundaries:** original source version and passage hash establish integrity only. Independent author/file gates from v1.6.3 prevent self-triggered enrichment; they are not implemented by the current library. Edge provenance, index integrity, model identity and stale-source handling require separate checks.

### Minimal follow-up experiments (not implemented)

| Experiment | What would count as evidence |
|---|---|
| Cold address-only handoff | Fresh agent receives addresses and resolver access, retrieves requested originals without a transcript or summary. |
| Paraphrase and corpus noise | Compare exact and real semantic retrieval on questions without source vocabulary; report misses and false leads, including domain-common terms. |
| Agent-selected graph | Fresh agent constructs an appropriate NetworkX view and traversal without a prescribed search algorithm. |
| Enrichment reuse | Agent A persists a source-backed relationship; fresh agent B uses it to answer a different question; compare tool calls and retrieved bytes against the unenriched baseline. |
| Cascading staleness | Change a source version, mark explicit dependent descendants stale, leave unrelated/similarity-only nodes unchanged, retain history and revalidate explicitly. Include cycles and multiple dependencies. |
| Scale | Increase corpus size and distractors; measure retrieval success, evidence bytes, tool calls and latency rather than assume small-fixture behavior generalizes. |

The original independent-agent critique motivates the paraphrase, vocabulary-noise, hybrid-ranking and bounded-window checks. Existing specifications cover ownership, qualified relationships and evolution; these are not evidence that the executable library already implements them. Noosphere supplies the concrete cascading-staleness mechanism as an upstream reference. No additional upstream code or private project material is included.

## Lifecycle implementation update (2026-11-10)

The canonical library now implements explicit dependency-based staleness, deprecation, historical retrieval and guarded revalidation. Local tests against the exact current code blob passed for cascades, cycles, late dependencies, source-version mismatch and persistence. Earlier rows describing invalidation as unimplemented are historical. Automatic source monitoring, cycle revalidation and semantic-model evaluation remain open.

## Named graph capabilities and first-pass positions (2026-11-10)

The library implements ten named views, ten core algorithms, and open-ended named graph derivation. The [graph-view regression tests](test_graph_views.py) and lifecycle tests cover structural properties, cycles, parallel-edge evidence, costs, detached copies and unknown vectors. First pass retains location, relation and proximity slots; deferred vectors are null and excluded from similarity until source-verified completion. Semantic-model benchmarking remains separate. See [Core Vocabulary](CORE_VOCABULARY.md).

## Capture workflow verification

The exact library blob `6c02c308337a70fe2c84e70e4bc08e2f597e9243` passed all nine existing lifecycle, graph-view and chat-context tests. The exact capture.py blob `d0c05c1fe782cb525e6881e0351f1706b1ecf26f` passed a local CLI round-trip (init, remember, link, verify, search, read, context; deferred vector) using synthetic test-only records. A retained test snapshot of 15 nodes and 21 edges also passed source/span/vector verification with the capture implementation. No raw chat ingestion or semantic-model validation is implied. The research companion's complete Python reconstruction remains pending.
