# Deterministic recovery of historical Knowledge Positions

> **Public technical evidence.** This document and its program use only the public manuscript, the committed historical companion, and a public Git blob. No private conversations, local-machine records or unpublished agent execution histories are part of this example.

## The question

When the research paper changed, the historical Knowledge Positions companion retained 28 source-addressed section records and 57 navigation relationships. It included **30 editorial links** in addition to 27 \`next_section\` links. The current paper has 29 EKC-tagged sections.

Strict SHA-256 equality safely recovered eight of the 30 historical editorial links: both original endpoint sections had exactly the same content bytes in the current paper. For the other **22 relationships**, at least one endpoint's section hash differed. A changed hash says **"not identical bytes"**, not **"the original record cannot be found"** and not **"the relationship is disproven"**.

The experiment asked whether the original locations, identifiers, source hashes, lexical vectors, and relationship endpoints could still deterministically **locate** the newer source-backed records—even where the paper had been edited.

## The saved program and repeatable test

**Program:** [\`relocate-historical-edges.py\`](relocate-historical-edges.py)  
**Existing source inputs:** [current manuscript](../../research/paper.md), [historical companion](../../research/evolving-knowledge-context.json), and [current section index](../../research/jit-index.json). The old companion contains the \`source_git_blob\` SHA used to fetch the **exact historical manuscript blob** from the official GitHub Git Blobs API.

Run from \`knowledge-positions/\`:

\`\`\`sh
python SDF/examples/relocate-historical-edges.py \
  --assert-paper \
  --output /tmp/paper-relocation-report.json
\`\`\`

The default historical-source fetch requires GitHub API access. In CI, the caller supplies the ordinary read-scoped \`GITHUB_TOKEN\` to avoid unauthenticated rate limits; this is **not** a database/LLM dependency. For fully offline reruns, pass \`--old-paper /path/to/exact-historical-paper.md\`; the program refuses that file unless its bytes match the companion's historical full-source SHA-256 and byte count. The program refuses to overwrite the input source/history/index. The generated JSON report is disposable.

The [\`paper-reconstruction.yml\` workflow](../../../.github/workflows/paper-reconstruction.yml) executes the real-program assertions alongside the prior Python/JavaScript common-record reconstruction and three-touch tests. A [successful historical-relocation run](https://github.com/l00p3rl00p/barely-passable-ai-stuff/actions/runs/45046720454) confirms the result; later runs also added a read-only GitHub token for reliable blob access.

## What the program does

1. **Verifies the old source, rather than substituting another paper.** Read the companion's \`source_git_blob\`, fetch those raw bytes, and require the whole-document SHA-256 and byte count to match the historical companion. The original source span of each old section must independently hash to that historical node's \`content_hash\`.
2. **Verifies the current source.** Read the current manuscript and require its full SHA-256 to match the current derived JIT index. Each indexed section must also hash to its saved section digest.
3. **Relocates old items using source positions.** Use the old edge's recorded source/target node IDs to recover the two original sections and byte spans. Locate the corresponding current sections through the stable \`EKC:NN\` source anchors. This gives a verified *current* span and ID for every historical endpoint.
4. **Measures rather than assumes content continuity.** Compute multiple deterministic old-to-current section measures: old-token occurrence retention, new-token coverage, unique-token Jaccard overlap, surviving exact nonheading lines, character-sequence ratio, and cosine similarity between the already recorded \`lexical-hash-512\` vectors. These are *comparison signals*, not calibrated probabilities and not semantic embeddings.
5. **Tests proximity without giving it the answer.** Independently rank **all 29** current-section vectors against each old section vector, *without passing its EKC tag into the ranking*. Only after ranking does the program check where the correct current section appeared. This distinguishes successful vector retrieval from the easy source-anchor lookup.
6. **Joins back through preserved relationships.** For every old editorial edge, map its recorded original source and target node IDs onto the respective current source-backed section. Preserve the exact old edge type and evidence label. Separate the eight exact-hash-compatible edges from the 22 changed-hash **relocated historical candidates**.
7. **Reports without rewriting history.** Output the original and current endpoint IDs, coordinates, section hashes, similarity measures, blind-vector ranks, relation type, historical qualification, and status. Source material and historical relationships are never edited by the tool. No LLM is called.

### What a vector contributed

The vector did **not** create a relationship. It helped find the current location corresponding to old material. After that, the unchanged source anchors, exact source-span hashes, and originally recorded graph endpoints supplied a deterministic confirmation path.

This is exactly the benefit of distinct **Location, Relation and Proximity** access methods over **one original source-backed knowledge identity**. If proximity produces an imperfect lead, positions and existing relationships narrow or confirm it; no extra semantic interpretation is necessary merely to recover the *place*.

## Executed measurements on the actual paper

| Measurement | Observed result |
|---|---:|
| Historical section records | 28 |
| Current section records | 29 |
| Historical sections still byte-identical | 15 |
| Historical sections changed but source-relocated | 13 |
| Editorial relationships with both endpoint hashes unchanged | 8 |
| Changed-hash editorial relationships with both endpoints source-relocated | **22 of 22** |
| Blind vector top-1 matches, all old sections | **27 of 28** |
| Blind vector top-5 matches, all old sections | **28 of 28** |
| Blind vector top-1 matches, changed sections only | **12 of 13** |
| Blind vector top-5 matches, changed sections only | **13 of 13** |
| Changed-hash editorial pairs with at least 80% of old token occurrences retained at *both* endpoints | **16 of 22** |
| Changed-hash editorial pairs with at least 90% retained at *both* endpoints | **13 of 22** |

The one old section that did not rank first by blind vector similarity was **EKC:25**, ranking **second**. It was also the substantially changed section: only about **40.5% of its historical token occurrences** remained in the current section. All six changed-hash editorial pairs falling below the 80%-at-both-ends criterion involve EKC:25. The saved stable section anchor disambiguated it without LLM reconstruction.

The exact recorded historical relationship labels are not replaced by guessed new relationships.

## What was recovered—and what was not claimed

**Recovered:** verified old/current source locations for the endpoints of **all 30 historical editorial links** (the earlier eight exact-hash matches plus these 22 relocated candidates). The original link labels and navigation-only qualification were preserved. This is deterministic *position recovery*, independent of whether a model would still endorse the link's meaning.

**Not automatically revalidated:** the semantic/editorial truth of the 22 changed-hash links. The historical companion labels them \`editorial manuscript structure / navigation only\`; it does not preserve edge-specific quoted evidence that would independently prove, for example, that a changed section still \`motivates\` another in the same sense. A good cosine score, a conserved heading, or a source pointer cannot on its own justify promoting that statement to a verified semantic fact.

**Not changed:** the original manuscript, the old 28/57 companion, the current JIT index, or the original knowledge. This experiment creates a separate derived report; it does **not** silently insert all 22 changed-hash links into the active current graph.

## Why this mattered

The earlier reconstruction used an intentionally strict test: **matching source hashes** determined what could be reused without any uncertainty. That is a sound fast path, but it missed the distinct question of **whether the old knowledge's present location could be rediscovered**.

The second pass proved that a changed hash need not force expensive rediscovery or discard the navigational lead. On this real manuscript, blind lexical proximity found 27/28 sections at rank one and all 28 within five; source anchors and original relation endpoints recovered every current destination. The result shows deterministic **reuse → locate → verify**, keeping evidence and qualified historical interpretation separate.

### Boundaries of this example

This is a **paper-specific EKC-anchored adapter**, not a universal parser or a complete SDK certification. The lexical vectors are deterministic retrieval features, not semantic embeddings. The blind-vector ranking is an evaluation of retrieval candidates; the main relocation path uses the known EKC anchors. Those two tests must not be conflated. The current paper still contains all historical EKC tags; an unanchored or reorganized document would require additional candidate adjudication and may have unresolved cases. That limitation is explicit rather than silently replacing the source or fabricating matches.
