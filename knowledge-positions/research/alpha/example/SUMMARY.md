# Alpha evidence — two real manuscript excerpts

The generated OKF files below are from the *verbatim selected excerpts* in [`../fixture/paper.md`](../fixture/paper.md), not from the entire original manuscript. Their source byte positions and section content hashes therefore address that fixture. Running `section_alpha.py` against `research/paper.md` gives exact original-manuscript positions and full-section hashes.

```text
  EKC:27                         EKC:28
  | summary/tags                  | summary/tags
  | source SHA                    | source SHA
  | knowledge SHA                 | knowledge SHA
  v                               v
  real Markdown token tree        real Markdown token tree
        +-------------+-------------+
                      |
                KnowledgePositions
                 NetworkX graph
                      |
           18 syntactic AST_CHILD edges
            2 proposed related_to edges
```

**Actual fixture execution:** 20 nodes, 20 edges, one connected component. Both OKF files have valid YAML frontmatter (`type: Research Section`, `sources`, `tags`, `description`) and a section-scoped source hash plus a separate annotation hash. The full token trees retain parser nesting and exact source byte offsets when available; parser children without independent offsets remain in the AST but are not invented as separately source-located nodes.

**Delta proof (four Python tests):** Initial admission creates only the two selected sections; rerunning an unchanged section writes zero files; changing EKC:28 annotations leaves EKC:27 and EKC:28 source AST/vectors intact; changing EKC:28 source text rebuilds its syntax structure without touching EKC:27. Annotation relationships are inspectable *proposals*, not asserted to have been human-reviewed.

Inspect [EKC:27 OKF](okf/EKC-27.md), [EKC:28 OKF](okf/EKC-28.md), [EKC:27 AST](ast/EKC-27.json) and [EKC:28 AST](ast/EKC-28.json).
