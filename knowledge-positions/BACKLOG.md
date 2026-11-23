# Backlog

Work remaining between the current [environment](ENVIRONMENT.md) and [mission](MISSION.md). See [roadmap](ROADMAP.md) for technical direction.

- [ ] Execute both notebooks with the actual semantic model; reproduce GPS and address-only handoff.
- [ ] Test paraphrases, distractors, corpus-specific weighting, hybrid ranking and bounded context windows.
- [ ] Implement durable qualified relationship write-back, independent hash gates and sixth-retrieval promotion.
- [x] Implement dependency-based cascading staleness, deprecation and explicit revalidation (mechanical tests passed).
- [x] Implement the ten named graph views, ten core algorithms and open-ended named derivation; exercise on an evolving test graph.
- [x] Support unknown/deferred vector positions and source-verified vector completion.
- [ ] Integrate real source monitoring and evidence-driven revalidation; test cycle recovery and multi-agent persistence.
- [ ] Evaluate larger-corpus persistence, OKF interchange and realistic SDK/codebase workflows.
- [ ] Test portable source owner/realm/route metadata against actual caller-specific discover/read/write permissions; never treat a locator as authorization.
- [ ] Exercise non-Python source-read/watchdog adapters against the generic `record_item_position` API; keep model-described webpage placement as `locator_only` until parser-confirmed. Measure optional position-aware embedding input against the ordinary model before claiming an improvement.
- [ ] Evaluate a **store-optional** transactional Knowledge Positions → LadybugDB adapter: scoped hash-gated changes, independent private owner stores, authorized cross-knowledge links, coordinated writer and durable readback. Preserve the existing JSON baseline.
- [ ] Integrate observed file/content reads at the real application boundary: cheap AST/structural ingestion without LLM enrichment, then qualify and persist only material already used in work. Respect a maximum of three useful enrichment levels; verify no LLM-wide enrichment when indexing large corpora.
- [ ] Record experiment results, limitations and source integrity checks in the relevant experiment documentation.

- [ ] Add on-demand source scanning and contentless lexical indexing for documents not yet enriched; test an unindexed document, then index and resolve it without persisting a full-text copy.
- [ ] Add optional natural-language and document extraction adapters with original source spans; test structured-source mappings and unchanged-source reuse.

- [x] Bound conversational retrieval to three hops, preserve deeper boundary references in `other`, and clear derived cache on API writes; regression tests pass.
- [ ] Create independent Git repository and register as a submodule once the new remote is available; preserve canonical history.
- [ ] Future security task: inject database credentials via environment variables from an encrypted vault/secret store; review database encryption, access controls and secret handling. Not part of the current implementation.

- [x] Provide a runnable agent capture procedure, Core reference and real GPT examples; verify capture/read/link/search/context round-trip.
- [x] Merge the research manuscript and companion into the canonical library folder on main (preserve research history).
