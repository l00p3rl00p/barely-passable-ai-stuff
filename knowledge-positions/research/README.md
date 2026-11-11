# Just-in-Time Knowledge — research manuscript

**Working research paper, not submitted or peer reviewed.**

- [Read the manuscript](paper.md)
- [Historical Evolving Knowledge Context](evolving-knowledge-context.json) — retained whole-document navigational artifact; not the authority for the evolving theory
- [Experiment evidence and replay](EXPERIMENT.md)
- [Historical whole-paper index generator](build_companion.py) — retained for comparison, not the incremental method
- [Incremental Markdown AST + OKF alpha](alpha/README.md) — executable two-section test and actual generated concept examples

## Two distinct experiments: historical index and incremental alpha

**Incremental source-version caution:** this manuscript has received surgical updates after the earlier whole-paper companion was generated. Its historical whole-document hash and byte offsets must not be mistaken for current original-source coordinates. The [two-section alpha](alpha/README.md) demonstrates scoped change processing; unchanged sections should retain their identities rather than triggering a full rebuild.

**Enrichment policy:** parsing and locating a large corpus is structural ingestion, not LLM interpretation. The standard architecture enriches only work-touched, already-read material and applies a hard three-touch mutation budget to a node or explicit cluster: admission is touch 1, touches 2 and 3 may revise semantic payload, then the core freezes until verified source mutation starts a new epoch. Later knowledge grows outward by relationship. Retrieval is independent and graph-theoretically bounded rather than fixed to a magic hop count. The current alpha demonstrates caller-supplied annotations, not an automatic read-event hook.

The `evolving-knowledge-context.json` companion below is the earlier **whole-document-version index**. It rewrites node identities across document versions, so it is *not* the method we intend to standardize. The [new alpha](alpha/README.md) uses real Markdown AST syntax, source-addressed paragraphs, portable OKF concept documents, separate section-content and annotation hashes, and stable section identities. It proves that a local annotation change need not regenerate source AST or unrelated knowledge. Only two excerpted paper sections are admitted so far; the full 28-section manuscript has **not** been migrated.

## One evolving paper; navigation artifacts are derived

The manuscript is the single authority for the evolving theory. Stable EKC section tags provide source-relative anchors. Historical companions may contain exact spans, hashes, vectors and editorial/navigation relationships for the source revision from which they were generated, but they are derived navigation artifacts—not parallel authorities and not current coordinates after the paper changes.

The historical whole-paper companion can still be reconstructed with the supplied Python script to replay that earlier representation. Current maintenance should update only affected knowledge and verified source locations through the section-scoped/incremental method; unchanged knowledge keeps its identity and existing vectors. Editorial section links are navigation, not empirical facts.

## Reproduce

From this directory, after installing the parent library:

```bash
python -m pip install ..
python build_companion.py build
python build_companion.py search "cascading staleness"
python build_companion.py read EKC:13
```

Use `python build_companion.py build --semantic` to generate real embeddings with the configured model; it requires model access and has not been executed in the manuscript preparation environment. Python verification of the complete manuscript companion is also pending; the published source manifest and vectors were generated directly from the repository bytes, and the original GPS experiment was replayed separately.

If the paper changes, do not silently reuse old source positions. Re-resolve and update the affected source locations and relationships through the current incremental method. Rebuild the historical whole-paper companion only when intentionally replaying that historical artifact.

## Review boundaries

The paper presents a single exploratory trial, not a controlled benchmark. It reports source bytes, not token savings. Related work is intentionally limited to relevant precedents and contributions. Private drafting notes and unrelated project discussions are excluded. The research branch has been merged into main; the manuscript and companion now live with the canonical library. No automatic publishing/submission is included.

## Follow-up: living knowledge in ordinary ChatGPT

The manuscript preserves the original cold-context experiment and adds [Section 12](paper.md#12-follow-up-from-a-retrieval-experiment-to-living-knowledge-ekc25), documenting subsequent library growth and a human-directed live private-graph experiment in ordinary ChatGPT. At the historical revision represented by the whole-paper companion, its section spans and lexical vectors were recalculated. That historical artifact does not become the authority for later paper revisions. The original experimental results and limitations remain intact. The complete Python reconstruction test is still pending. Git history preserves the historical experimental baseline, while main contains the evolving manuscript and implementation together.

## Architecture in motion

[Section 13](paper.md#13-architecture-in-motion-ekc26) adds the working-conversation scope and the new architecture figure. [Four architecture views](ARCHITECTURE_VIEWS.md) includes Mermaid diagrams, an ASCII representation, and the runtime/network boundary. The [figure](figures/knowledge-loop.svg) is an actual SVG. Historical companion counts describe the revision that produced them; they are not a requirement or authority for incremental paper updates.

## Getting started: theory and application

[Section 14 (EKC:27)](paper.md#14-getting-started-from-an-empty-graph-to-working-knowledge-ekc27) describes the reusable bootstrap method, distinguishes library mechanics from human/application policy, and connects it to the original GPS pilot and living GPT case study. Earlier experimental claims and sections remain preserved in the manuscript and Git history; incremental updates do not require regenerating the historical whole-paper companion.

## ASCII figures

The manuscript's Section 14 now includes Figures 6 and 7: the context window as a desk rather than the warehouse, and the growth of knowledge from one useful discovery. Both are conceptual illustrations, not measured graph topology. Historical companion hashes/counts remain evidence about the revision that generated them, not a current-paper maintenance contract.

## Execution-boundary finding

[Section 15 (EKC:28)](paper.md#15-execution-boundary-capture-persistence-cannot-be-an-optional-thought-ekc28) records the observed cold-start failure: the model read instructions and a network overview but skipped capture, then used JSON directly rather than the Python graph library. The proposed host hook / durable journal / indexing worker / MCP retrieval boundary is **not deployed**; see the [Runbook integration contract](../RUNBOOK.md#7-deterministic-capture-enforce-the-execution-boundary-not-the-prompt). Current updates maintain the evolving paper and affected navigation/source positions incrementally; the historical whole-paper reconstruction is not required for section-scoped work.
