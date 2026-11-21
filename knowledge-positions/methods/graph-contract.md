### 3.2.3 Recovered graph contract: ten algorithms, two additional operations, ten views

The original CORE_VOCABULARY.md records **ten graph algorithms** from the user-supplied reference picture, **plus** Ancestors/Descendants and Neighborhood/Subgraph. The actual Python KnowledgePositions.GRAPH_VIEWS provides the ten named views below. This SDK MUST make every algorithm **invocable on the appropriate view** of the same graph records, using ordinary algorithms, without reconstructing new knowledge or fabricating missing edges.

| Required algorithm | Necessary input/view | Honest outcome when conditions do not hold |
|---|---|---|
| DFS | directed adjacency; chosen root | Reachable nodes, possibly only the root |
| BFS | directed adjacency; chosen root | Reachable breadth-first tree, possibly only the root |
| Topological sort | selected directed acyclic dependency graph | Cycle diagnostic / not applicable, never delete edges to force an order |
| Union-find / DSU | undirected connectivity view | Existing components; isolated node is its own set |
| Cycle detection | selected directed or declared undirected view | Cycles or correctly empty result |
| Connected components | undirected or explicitly weak/strong-directed view | Actual components, including isolated nodes |
| Bipartite check | declared undirected view | True/false about the view, not a forced partition |
| Flood fill | selected connectivity view and seed | Actual reachable component |
| Minimum spanning tree/forest | undirected weighted view; explicit finite costs or declared unit-cost policy | Forest/disconnected results; missing costs flagged, not invented |
| Shortest path | graph and endpoints; declared cost or hop policy | Path or no-path, never fabricated |
| Ancestors / descendants | directed view, native edge direction | Actual predecessors/successors with selected semantics |
| Neighborhood / subgraph | selected seed, relations and radius/selector | Real bounded neighborhood, including empty edge set |

**Actual implemented view names:** directed, undirected, weighted, multigraph, tree, forest, dag, bipartite, similarity, neighborhood. The source graph is a MultiDiGraph; the library’s graph_view() returns detached **derived views**, not ten distinct knowledge stores. Minimum spanning tree, topological sort, union-find and bipartite tests operate on their mathematically appropriate views. Direction, parallel-edge evidence, weighting aggregation and any unit-cost assumption MUST be disclosed rather than silently modified. Similarity-view edges are explicitly candidates, not factual causation. An isolated binary with a known parent still has graph position and filename proximity even if no semantic edge exists.

The first ten are exercised by current KnowledgePositions.core_algorithms(root,target) (source: knowledge_positions.py), while the additional two use standard NetworkX ancestor/descendant and neighborhood/subgraph operations. **Do not claim all twelve have passed a new UKC integration suite merely because the original code has the operations.**

