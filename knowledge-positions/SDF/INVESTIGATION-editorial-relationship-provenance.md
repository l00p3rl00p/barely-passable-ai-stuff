# Public technical note — historical paper navigation

> **PUBLIC REPOSITORY NOTICE:** This document is intended for public release. Include only evidence available in this public repository. Do not add private conversations, agent transcripts, local machine paths, session IDs, unpublished data, personal details, or internal project notes.

## Scope and finding

The archived `research/evolving-knowledge-context.json` contains 28 section records and 57 links: 27 sequential links and 30 other editorial navigation links. Their evidence markers explicitly describe them as **navigation only**, not validated semantic facts.

The first repository commit containing the companion is [`1159be9`](https://github.com/l00p3rl00p/barely-passable-ai-stuff/commit/1159be9bc2e3317e3c2ac91628be1563694f3c5e), dated 2026-11-11. The file entered Git already containing the editorial links. The checked-in Git history does not establish how each link was originally authored. Do not infer the author or generation method from the import commit.

## Reproducible code observations

- [`build_companion.py`](../research/build_companion.py) reads the saved node/edge records and imports them into the Knowledge Positions graph. It **does not infer** editorial edges from the manuscript.
- [`jit_index.py`](../research/jit_index.py) reconstructs section boundaries, source digests, `next_section` and `part_of` relationships from the current paper. Its output is not a replacement for previously recorded editorial knowledge.
- The historical companion references a source Git blob distinct from the manuscript revision first committed beside it; historical positions should not be treated as current coordinates.
- The saved historical companion has no per-edge touch-event history or proof that the three-touch mechanism generated these editorial relationships.
- The paper-specific alpha is a separate, limited AST/OKF experiment with independently supplied annotations; it does not generate this companion's set of 30 editorial links.
- The materializer can create local SQLite and graph projections, but no checked-in database writer establishing the origin of the 30 editorial links was identified.

## Deterministic reconstruction boundary

Matching source-section hashes preserve compatibility across changed document offsets; they do not authenticate an editorial interpretation.

In the currently checked paper, 15 historical section digests match current sections. Of the 30 historical editorial relationships, eight have both endpoint hashes unchanged and are eligible to retain their original **navigation-only** qualification. Twenty-two involve at least one changed section and require review before reuse.

**This is a compatibility analysis, not an executed enriched-graph reconstruction or full UKC/1 conformance result.** No historical artifact was modified during this investigation.

## Publication boundary

Detailed investigative provenance, private conversations, nonpublic execution records, and personal work history do not belong in this public source tree. The repository can publish reproducible algorithms, sanitized technical observations, hashes of public repository artifacts, and verified limits. Any evidence that is not publicly shareable should be retained through a separately authorized private workflow, not copied here.
