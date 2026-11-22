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
