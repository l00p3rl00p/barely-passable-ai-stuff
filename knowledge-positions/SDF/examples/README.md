# Reconstructing Knowledge Positions in another language

## What actually happened

While checking the completed JITK paper, we discovered that its **derived** section-scoped Knowledge Positions index no longer matched its **authoritative** Markdown source. We had an existing Python indexer (`research/jit_index.py`) and instructions, but the assistant's connected GitHub execution environment did not provide a way to run that Python program against the repository.

Instead of demanding that Python run, translating the manuscript's meaning with an LLM, or recovering an old graph, the assistant read the existing method and index format and implemented the reconstruction in JavaScript. It used the original paper's stable `[EKC:NN]` identities, exact UTF-8 positions and section hashes, regenerated the navigational data, and wrote the repaired index. The paper's prose was not changed.

**Observed in that reconstruction:** 29 identities survived; 38 structural relationships resolved; 23 unchanged section vectors were preserved; six changed sections were recalculated. The regenerated index passed independent section-coordinate, SHA-256, identity and edge-reference checks. That specific reconstruction was performed in a JavaScript execution environment, not by running the Python indexer.

**What this demonstrates:** Knowledge Positions here is a source-backed **method** whose navigational representation is reconstructible from original evidence. The language and executable that perform the reconstruction can change. The map is disposable; the source and its stable identities are not.

**What it does not demonstrate:** universal interchangeability of arbitrary parsers, semantic embedding equivalence, preservation of unverifiable relationships, or the complete UKC/1 conformance contract. The lexical-hash-512 vectors are deterministic lookup features, **not semantic embeddings**. Unchanged, previously verified values can be reused; changed information must be recalculated or treated as unknown.

## Run the JavaScript example

`SDF/examples/rebuild-paper-index.mjs` is a self-contained Node.js script: no external npm packages, Python runtime, graph database, or LLM required. It accepts a Markdown paper using the same `[EKC:NN]` section-heading convention and produces the same section-scoped index **shape** as the repository's Python example.

From `knowledge-positions/`:

```sh
# Verify the current derived paper index against the manuscript.
node SDF/examples/rebuild-paper-index.mjs verify

# Reconstruct it from paper.md, preserving unchanged indexed sections.
node SDF/examples/rebuild-paper-index.mjs build

# Verify the regenerated result.
node SDF/examples/rebuild-paper-index.mjs verify
```

To try it with your own tagged document, specify **both** source and output; don't overwrite the repository's research index:

```sh
node SDF/examples/rebuild-paper-index.mjs build /path/to/my-paper.md /path/to/my-index.json
node SDF/examples/rebuild-paper-index.mjs verify /path/to/my-paper.md /path/to/my-index.json
```

A section in the input looks like `## Introduction [EKC:01]`. Use distinct stable tags throughout the paper. This example intentionally uses the original paper's `paper.md#EKC:NN` ID namespace in its output, even when passed another filename; it illustrates the original contract, not a generalized cross-document identity scheme. Keep indexes for different documents separate.

Compare with the [original Python implementation](../../research/jit_index.py) and [paper maintenance guide](../../paper/README.md). Both express the same reconstruction method but are **independent implementations**; the SDF does not prescribe either language.

## Reuse without accidentally changing the experiment

This is a **framework example**, not an additional result of the original cold-context research trial. It was observed during maintenance of the living paper after the manuscript had been written. It belongs here as a practical demonstration and is linked from the paper's companion materials for provenance. Do not revise the research paper to incorporate this later example unless the explicit Paper Lock review process authorizes a correction.


## Current-paper Knowledge Positions reconstruction — verified, source-backed UKC/1 example

> **PUBLIC REPOSITORY NOTICE:** This example uses only the public manuscript and previously published companion. Do not publish session transcripts, unreviewed discoveries, private worktrees, machine paths, personal context, or confidential evidence.

The heading index above is an **earlier stage** of the method. The completed live-paper example is:

- [Python common-record reconstruction](reconstruct-enrichment.py), using the existing \`research/jit_index.py\` section parser and lexical-hash implementation.
- [Independent JavaScript reconstruction](reconstruct-enrichment.mjs), using the source parser in \`rebuild-paper-index.mjs\`.
- [Shared full-paper test](../../tests/test_paper_reconstruction.py) and [CI run definition](../../../.github/workflows/paper-reconstruction.yml), which execute both on the actual paper.

Both languages construct one logical \`ukc/1\` record per paper section containing **identity, authoritative source version, verified byte/line location, observed native heading fields, qualified graph relationships, lexical vector, and evidence**. The old \`paper.md#EKC:NN\` tag is preserved as a native source anchor, while the \`ukc:v1:...\` canonical identity is derived from repository source key, section tag and verified section digest. This allows unchanged sections to retain canonical identity when other parts of the paper move.

**Actual current-paper record example:**

\`\`\`yaml
schema: ukc/1
id: ukc:v1:b9fa995de1a79bb5ee7be349a588f06585a14d50c84e399dab8dd8107467b72f
kind: markdown_section
source:
  authority: repo:l00p3rl00p/barely-passable-ai-stuff
  key: knowledge-positions/research/paper.md
  realm: public_repository
  access: public
  # whole-paper and section-scoped SHA-256 versions are stored separately
location:
  status: known
  basis: ekc_heading_parser
  anchor: EKC:14
  spans: [{unit: utf8_byte, start: 43428, end: 45359}]
  start_line: 271
  end_line: 302
values:
  title: "5. Reference implementation: Knowledge Positions"
  tag: EKC:14
native:
  parser: ekc_heading_regex
  heading_level: 2
  source_ref: "paper.md#EKC:14"
proximity:
  - space: lexical-hash-512
    status: known
    # the actual 512-component vector is stored in the generated record
evidence:
  span_sha256: 11c9b6134de4f447a39c353abb36093b7b3601eb248b65af3b05f0af165fdbc4
relations:
  # Real generated output includes current structural and compatible
  # historical navigation edges with direction, canonical neighbor ID,
  # evidence and qualification.
\`\`\`

This is a shortened display; use \`get\` to inspect the **complete actual record** including its vector, incoming/outgoing relations and evidence.

**Run without changing the manuscript or historical companion:**

\`\`\`sh
# From knowledge-positions/; outputs are derived files outside the source tree.
python SDF/examples/reconstruct-enrichment.py build --output /tmp/paper-ukc-python.json
node SDF/examples/reconstruct-enrichment.mjs build \
  research/paper.md research/evolving-knowledge-context.json /tmp/paper-ukc-js.json

python SDF/examples/reconstruct-enrichment.py verify --output /tmp/paper-ukc-python.json
node SDF/examples/reconstruct-enrichment.mjs verify \
  research/paper.md research/evolving-knowledge-context.json /tmp/paper-ukc-js.json

python SDF/examples/reconstruct-enrichment.py get EKC:14 --output /tmp/paper-ukc-python.json
node SDF/examples/reconstruct-enrichment.mjs neighbors EKC:14 \
  research/paper.md research/evolving-knowledge-context.json /tmp/paper-ukc-js.json
python SDF/examples/reconstruct-enrichment.py resolve EKC:14 --output /tmp/paper-ukc-python.json

# Self-contained parity, source resolution, stale-source rejection and OKF x_ukc checks:
python tests/test_paper_reconstruction.py
\`\`\`

The live-paper test verifies: **29 current UKC/1 section records**, **15 matching historical section hashes**, **15 matching previously stored lexical vectors**, **38 current observed structural edges**, **eight recovered historical editorial navigation edges**, and **22 historical editorial edges held inactive**. The recovered edges keep their original \`navigation only\` qualification; a hash match is not a fresh semantic review. The two languages agree on common-record fields, canonical identities, original resolved bytes and portable \`x_ukc\` frontmatter values. Source bytes and the archived companion are unchanged.

### Touch behavior and limits

The historical Python reference (not the current [SDF touch lifecycle](../../core/lifecycle.md)) has [three-touch regression tests](../../tests/test_enrichment_budget.py) establish that admission is touch 1; touches 2 and 3 may update a semantic payload; the third freezes it, while new qualified links can still grow outward. A source-version change starts a new budget. **Touches do not create links automatically.** Neither the companion nor the present example contains proof of per-edge historical touch events; the companion's editorial edges are treated as prior recorded navigational knowledge, not retroactively attributed to touches.

### Conformance boundary

**Yes, this example uses Knowledge Positions:** it reconstructs actual shared source-backed UKC/1 logical records and accesses their location, relation, and proximity values from the same identity. No LLM is required for reconstruction. It also makes both-language results directly comparable and inspectable.

**Not claimed:** a general source-agnostic UKC SDK implementation, native full CommonMark AST capture, active authorization for private content, arbitrary-parser fidelity, or complete UKC certification. This is an EKC-anchored paper adapter, deliberately limited to the structure it actually parses. Other SDF contracts and conformance fixtures remain separate requirements, not hidden capabilities of this example.


> Full worked explanation: [Deterministic historical relocation — what, why, how, results, and limits](DETERMINISTIC-HISTORICAL-RELOCATION.md). The reusable program is [relocate-historical-edges.py](relocate-historical-edges.py).

## Reconstruction of enrichment state, not database preservation

**Never be afraid to erase the database.** Treat the graph/index/vector store as a disposable projection of durable original sources **and previously accepted evidence-backed enrichment deltas**. The [human-authorized reconstruction workflow](DETERMINISTIC-RECONSTRUCTION-HUMAN-REVIEW.md) explains how to recover deterministically first, ask the human whether to proceed, and reserve a small LLM review for genuinely unresolved relationships. The original source does not necessarily contain earlier derived discoveries; keep those accepted deltas outside the disposable database, or rebuilding them as previously established knowledge will not be possible.

## Deterministic relocation of the 22 changed historical editorial links

The initial strict-hash reconstruction activated eight editorial links and marked 22 historical links inactive because at least one endpoint section had changed. **Inactive does not mean unfindable.** The [source-only relocation experiment](relocate-historical-edges.py) resolves the older paper from the exact saved Git blob SHA and verifies its complete SHA-256, then reads the current authoritative paper. For every historical node it checks its original exact byte span/hash and finds the current EKC-anchored section. It measures historical token retention, exact surviving lines, lexical Jaccard, character sequence overlap, and declared lexical-vector cosine. **No LLM and no semantic relationship inference** are involved.

In the actual executed public-paper test:
- All **22 of 22** editorial links with changed endpoint hashes had both endpoints relocated to verified current source spans and identities.
- All 22 retained their source headings/anchors.
- **16 of 22** retained at least 80% of old tokens at **both** endpoints; **13 of 22** retained at least 90%.
- **Six weaker links** all touch **EKC:25**, where the historical-to-current token retention is approximately **40.5%**. This is a specific heavy revision, not a failure to locate the knowledge.
- In a **blind vector ranking across all 29 current sections**, the historical vectors ranked the correct section **first for 27 of 28 old sections**, and **within the top five for all 28**. Among the 13 hash-changed sections, **12 ranked first** and **all 13 ranked in the top five**. The sole second-place result was the heavily rewritten **EKC:25**; its exact anchor and relational neighbors disambiguated it without an LLM.
- The previously recovered eight hash-exact editorial links remain distinct from these 22 **relocated historical candidates**. No historical link was silently promoted from \`navigation only\` to verified semantic fact.

Try the same experiment (requires access to the official public GitHub Git-blob endpoint, or supply a byte-identical historical source with \`--old-paper\`):

\`\`\`sh
python SDF/examples/relocate-historical-edges.py --assert-paper \
  --output /tmp/paper-relocation-report.json
\`\`\`

The report preserves old and new source/target positions, hashes, section IDs, original relation labels and qualification, and measured similarity. It is enough to **navigate the old relationship to its present-day sections** even when hashes differ. It does **not** prove that the relation's editorial meaning is unchanged; the saved relationship evidence does not contain an exact quoted rationale for each edge. This distinction is part of Knowledge Positions' evidence contract, not a need to reconstruct the entire paper with an LLM.
