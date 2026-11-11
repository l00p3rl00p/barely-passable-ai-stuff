# Just-in-Time Knowledge — research manuscript

**Working research paper, not submitted or peer reviewed.**

- [Read the manuscript](paper.md)
- [Current section-scoped JIT index](jit-index.json) — derived navigation over the evolving paper; stable EKC identities, exact section spans/hashes, structural relationships
- [JIT index tool](jit_index.py) — build, verify, search, read and inspect section neighbors without treating the whole paper as one mutable knowledge item
- [Historical Evolving Knowledge Context](evolving-knowledge-context.json) — retained whole-document navigational artifact; not the authority for the evolving theory
- [Experiment evidence and replay](EXPERIMENT.md)
- [Historical whole-paper index generator](build_companion.py) — retained for comparison, not the incremental method
- [Incremental Markdown AST + OKF alpha](alpha/README.md) — executable two-section test and actual generated concept examples

## Current JIT maintenance, historical index and incremental alpha

**Incremental source-version caution:** this manuscript has received surgical updates after the earlier whole-paper companion was generated. Its historical whole-document hash and byte offsets must not be mistaken for current original-source coordinates. The current [section-scoped JIT index](jit-index.json) covers all EKC sections with stable section identities and exact current spans/hashes. The [two-section alpha](alpha/README.md) separately demonstrates richer Markdown AST + OKF delta processing; it is still only a two-section alpha.

**Enrichment policy:** parsing and locating a large corpus is structural ingestion, not LLM interpretation. The standard architecture enriches only work-touched, already-read material and applies a hard three-touch mutation budget to a node or explicit cluster: admission is touch 1, touches 2 and 3 may revise semantic payload, then the core freezes until verified source mutation starts a new epoch. Later knowledge grows outward by relationship. Retrieval is independent and graph-theoretically bounded rather than fixed to a magic hop count. The current alpha demonstrates caller-supplied annotations, not an automatic read-event hook.

The `evolving-knowledge-context.json` companion below is the earlier **whole-document-version index**. It rewrites node identities across document versions, so it is *not* the maintenance method we standardize. The current `jit-index.json` is the lightweight full-paper navigation artifact: all 28 EKC sections have stable IDs, exact current spans and section-scoped hashes. The [alpha](alpha/README.md) goes deeper on only two sections with real Markdown AST syntax, source-addressed paragraphs, portable OKF concept documents, separate section-content and annotation hashes, and stable section identities.

## One evolving paper; navigation artifacts are derived

The manuscript is the single authority for the evolving theory. Stable EKC section tags provide source-relative anchors. Historical companions may contain exact spans, hashes, vectors and editorial/navigation relationships for the source revision from which they were generated, but they are derived navigation artifacts—not parallel authorities and not current coordinates after the paper changes.

The historical whole-paper companion can still be reconstructed with the supplied Python script to replay that earlier representation. Current maintenance should update only affected knowledge and verified source locations through the section-scoped/incremental method; unchanged knowledge keeps its identity and existing vectors. Editorial section links are navigation, not empirical facts.

## Reproduce

From this directory, after installing the parent library:

```bash
python -m pip install ..
python jit_index.py verify
python jit_index.py search "enrichment retrieval"
python jit_index.py neighbors EKC:12
python jit_index.py read EKC:12
```

The historical whole-paper companion remains reproducible separately with `python build_companion.py build`; use it only when intentionally replaying that historical representation.

`jit_index.py` does not require an embedding model. It preserves compatible vector state if present, but vectors may remain explicitly unknown. Use `python build_companion.py build --semantic` only to replay the historical companion with real embeddings; it requires model access and is not part of normal incremental maintenance.

If the paper changes, do not silently reuse old source positions. Re-resolve and update the affected source locations and relationships through the current incremental method. Rebuild the historical whole-paper companion only when intentionally replaying that historical artifact.

## Review boundaries

The paper presents a single exploratory trial, not a controlled benchmark. It reports source bytes, not token savings. Related work is intentionally limited to relevant precedents and contributions. Private drafting notes and unrelated project discussions are excluded. The research branch has been merged into main; the manuscript and companion now live with the canonical library. No automatic publishing/submission is included.

## Follow-up: living public knowledge

The manuscript preserves the original cold-context experiment and adds [Section 12](paper.md#12-follow-up-from-a-retrieval-experiment-to-living-knowledge-ekc25), documenting subsequent public library growth and the current section-scoped JIT maintenance proof. The historical whole-paper companion remains evidence about its own revision and does not become the authority for later paper changes. `jit-index.json` is the current lightweight navigation artifact; `paper.md` remains the theory authority.

## Architecture in motion

[Section 13](paper.md#13-architecture-in-motion-ekc26) adds the working-conversation scope and the new architecture figure. [Four architecture views](ARCHITECTURE_VIEWS.md) includes Mermaid diagrams, an ASCII representation, and the runtime/network boundary. The [figure](figures/knowledge-loop.svg) is an actual SVG. Historical companion counts describe the revision that produced them; they are not a requirement or authority for incremental paper updates.

## Getting started: theory and application

[Section 14 (EKC:27)](paper.md#14-getting-started-from-an-empty-graph-to-working-knowledge-ekc27) describes the reusable bootstrap method, distinguishes library mechanics from human/application policy, and connects it to the original GPS pilot and living GPT case study. Earlier experimental claims and sections remain preserved in the manuscript and Git history; incremental updates do not require regenerating the historical whole-paper companion.

## ASCII figures

The manuscript's Section 14 now includes Figures 6 and 7: the context window as a desk rather than the warehouse, and the growth of knowledge from one useful discovery. Both are conceptual illustrations, not measured graph topology. Historical companion hashes/counts remain evidence about the revision that generated them, not a current-paper maintenance contract.

## Execution-boundary finding

[Section 15 (EKC:28)](paper.md#15-execution-boundary-capture-persistence-cannot-be-an-optional-thought-ekc28) records the observed cold-start failure: the model read instructions and a network overview but skipped capture, then used JSON directly rather than the Python graph library. The proposed host hook / durable journal / indexing worker / MCP retrieval boundary is **not deployed**; see the [Runbook integration contract](../RUNBOOK.md#7-deterministic-capture-enforce-the-execution-boundary-not-the-prompt). Current updates maintain the evolving paper and affected navigation/source positions incrementally; the historical whole-paper reconstruction is not required for section-scoped work.
