# Roadmap

The technical means by which Knowledge Positions intends to achieve its [mission](MISSION.md). The [architecture](ARCHITECTURE.md) defines the high-level design; the [environment](ENVIRONMENT.md) describes the actual implementation; the [runbook](RUNBOOK.md) explains how humans use it today. This roadmap describes planned engineering work and its validation.

| Mission objective | Planned technical means | Evidence of completion |
|---|---|---|
| Precise knowledge navigation | Source IDs, version hashes, source-relative ordered item paths and exact spans; optional position-aware embedding inputs with separate policy labels; NetworkX node/edge identities; exact source resolver | Cold agent retrieves verified originals from known addresses or search results |
| Agent-directed investigation | Build on implemented ten named native graph views, ten core algorithms and open-ended NetworkX derivation; optional exact/FTS5, fuzzy and vector retrieval; optional hybrid rank fusion, corpus-specific weighting and bounded context windows | Agent constructs its own graph and traversal; paraphrase and distractor tests |
| Continuity across sessions | Persist graph identities, coordinates, vectors and qualified edges; evaluate LadybugDB for larger stores; keep original sources external; portable OKF adapters | Reload in a fresh process and retrieve the same evidence without reingestion |
| Compounding knowledge | Idempotent node/edge writes; source/version hashes; independent author/index hash gates; retrieval counters with sixth-use promotion; evidence-backed write-back | Second agent benefits from first agent's discoveries without duplicate processing |
| Evolving knowledge | Explicit derived-from dependencies; NetworkX reverse dependency traversal; source-version change detection; stale markers and explicit revalidation; preserve historical versions | Changed source flags dependent descendants, leaves unrelated/similarity-only nodes unchanged, and preserves history |
| Demonstrable usefulness | Jupyter and Marimo experiments; cold-session SDK/application investigation; increasing corpus size and distractors; record retrieval success, tool calls, evidence bytes and latency | Reproducible evidence that the mission is being achieved |

## Engineering sequence

1. **Validate the existing library:** execute both notebooks with the actual semantic model, reproduce GPS retrieval and source rejection, and test address-only handoff.
2. **Strengthen retrieval:** implement and evaluate optional lexical/fuzzy/semantic combinations and context windows; retain agent control over graph construction and traversal.
3. **Persist and enrich on touch:** establish durable, idempotent source identities and qualified write-back; evaluate optional LadybugDB and portable OKF; use independent source/annotation hash gates. Let structural AST indexing run broadly without LLM enrichment. Qualify useful meaning only as work actually reads/touches a source, at most three contextual enrichment levels; bulk LLM enrichment is a separate explicit task.
4. **Maintain currency:** build on implemented dependency-based cascading staleness and deprecation, inspired by [Noosphere Lite MCP](ATTRIBUTION.md); integrate source monitoring, evidence-driven revalidation and cycle recovery.
5. **Validate real workflows:** connect SDKs, application code, documentation and decisions; measure cold-context retrieval and enrichment reuse at increasing scale.

The named graph capabilities, deferred vector slots and explicit dependency lifecycle are already implemented; see [Environment](ENVIRONMENT.md) and [Coverage](COVERAGE.md) for evidence and limitations. Remaining work is planned. These are technical directions, not dated release commitments. No mandatory custom graph-search engine, Tree-sitter parser or graph ontology is introduced.

## Unstructured-source path

Use source-specific extraction (Python AST for code, spaCy for language structure, document extraction for PDFs/text, deterministic schema mapping for structured sources). Map results to common source coordinates; build contentless FTS5 discovery indexes without duplicating originals, then generate semantic vectors and agent-selected NetworkX relationships for ingested knowledge. Use on-demand scans for previously unindexed sources and promote frequently retrieved knowledge on the sixth retrieval. Validate source resolution, hash reuse and dependency staleness across versions. This is planned, not current core functionality.

## Current deployment

The chat-only capture workflow and ten graph capabilities are implemented. The research manuscript now resides with the library on main. Future work: real source acquisition and cold-session reuse evaluation, semantic embeddings, independent submodule deployment and database security (see Backlog).
