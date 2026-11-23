# Section-addressed JIT Knowledge — alpha

**A working two-section test of the method, not a substitute for the manuscript.** The original `../paper.md` remains read-only. The committed `fixture/paper.md` contains verbatim excerpts from its EKC:27 and EKC:28 sections to make the cold alpha deterministic and small. The actual paper is the intended source for real usage.

This implementation uses MarkdownIt's `CommonMark` token stream, projects knowledge into [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) Markdown with real YAML frontmatter, and uses the actual `KnowledgePositions`/NetworkX graph. It does **not** use an LLM to decide source structure. The YAML notes are explicit, inspectable **agent-proposed annotations** in this alpha. They are not parser-invented facts and are not represented as human-reviewed until a human actually reviews them.

## Run

From the `knowledge-positions/` directory:

```bash
python -m pip install '.[paper-alpha]'
python -m unittest discover -v -s research/alpha -p 'test_section_alpha.py'
python research/alpha/section_alpha.py \
  --source research/paper.md \
  --notes research/alpha/notes.yaml \
  --output research/alpha/.output
```

The program looks up **only EKC:27 and EKC:28** in the real paper. It parses document headings to locate their original UTF-8 byte positions, but calculates content hashes and regenerates AST/OKF/graph knowledge **only for selected sections**. It leaves `paper.md` alone. The two generated concept documents each contain their content hash and separate knowledge-annotation hash, provenance, tags, summary, exact paragraph anchors, and qualified relationships. Actual parser tokens, nested syntax and source positions live side-by-side in `ast/`; the Knowledge Positions graph contains source-backed section/structural nodes and the reviewed semantic edges.

After an observed change to EKC:28, restrict processing to that section:

```bash
python research/alpha/section_alpha.py \
  --source research/paper.md \
  --notes research/alpha/notes.yaml \
  --output research/alpha/.output \
  --changed EKC:28
```

If the section's source and annotations are unchanged, **zero files are rewritten**. If only tags, summary, or relationships change, only the OKF concept and graph annotations change; the source hash, vector, AST, and untouched sections are reused. If the section text changes, only that section's AST and source-backed nodes are rebuilt. The stable section ID remains `paper.md#EKC:28`; prior section hashes are recorded in its history. Content-addressed parser-token IDs are not a promise of stable identity for *edited* tokens. Unknown original node/span coordinates are not invented for inline token children that lack independent parser offsets.

**The current test covers a two-section slice**, not automated host/session capture, a full document reindex, or an automatic reviewer.

**Location metadata:** generated OKF now carries a producer-defined `x_jit_location` block with the actual section-scoped SHA-256, exact observed UTF-8 source byte span, a `local_file` realm and the current Python process's observed read. It does not grant other providers or environments read/write access. The `owner_namespace` is intentionally unknown, not invented; see [portable location guidance](../../LOCATION_ACCESS.md). A byte-offset move of an otherwise unchanged section requires a future position-only rebase mechanism; the alpha does not yet implement that case. In particular, this alpha does **not** automatically enrich documents when a model opens them: notes are explicit caller-proposed input. Structural AST extraction can be broad, but the recommended application policy enriches only content actually used in work, within at most three useful semantic levels (not an eager bulk task). A hook or application integration is required if capture is mandatory independently of model choices. No database or service was deployed in this alpha. `graph.json` is a materialized Knowledge Positions representation, not a hidden guarantee that an LLM will use it.

## Actual alpha evidence

With verbatim excerpts of the real EKC:27/EKC:28 text, Python tests exercise initial admission, no-op reuse, annotation-only changes, and source changes; all four pass. The first fixture creates **20 source-backed nodes / 20 edges**, including true `AST_CHILD` and reviewed `related_to` links. The test asserts that EKC:27's stored nodes, vectors, AST and OKF bytes are unchanged after updating EKC:28. The full canonical paper source is exercised by the command above when the script is run in the repository checkout; this alpha fixture does not claim to reproduce every paragraph of the full two sections.
