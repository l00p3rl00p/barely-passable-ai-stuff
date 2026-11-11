# Core Knowledge Vocabulary

The minimum common vocabulary for named references, graph structures and algorithms, and vector operations. This is an enabling vocabulary, not an exhaustive ontology, mandated workflow, or independent instruction system. Existing domain relationships remain available as extensions.

## 1. Relationships

Core defines permitted relationships between named references.

| Layer | Relationship | Direction and ordinary meaning |
|---|---|---|
| Structural hierarchy | is_a | subtype → broader type |
| Structural hierarchy | instance_of | instance → type |
| Structural hierarchy | part_of | part → whole |
| Practical context | has_property | entity → property or named value |
| Practical context | used_for | entity → purpose |
| Practical context | located_in | entity → location |
| Action and provenance | manufactured_by | product → manufacturer |
| Action and provenance | works_for | person or organization → employer |
| Action and provenance | competitor_of | competitor ↔ competitor |
| Process and logic | requires | dependent → prerequisite |
| Process and logic | causes | cause → effect |
| Process and logic | related_to | entity ↔ related entity |

Relations are directional unless their ordinary meaning is reciprocal. Reciprocal relationships may be represented by one undirected edge or explicitly paired directed edges in a derived view. Do not infer symmetry or transitivity for arbitrary relations. The labels retain their ordinary meanings; they do not introduce independent instructions, modify original human intent, or bypass verification and approval gates.

Core does not prohibit domain extensions. [Knowledge Graph Relationships](Knowledge_Graph_Relationships_and_Enrichment.md) describes the richer software, evidence and decision vocabulary. A similarity lead is not an established cause, dependency or factual relationship.

## 2. Graph structures

| Core term | Meaning |
|---|---|
| Node / vertex | Named reference, with common identity and source position |
| Edge / relation | Connection between two nodes, with type, direction and optional evidence |
| Directed / undirected | Whether the edge has an orientation |
| Weighted / unweighted | Whether a numeric edge attribute is used by an algorithm |
| Simple / multigraph | At most one edge per pair, or multiple distinct relationships per pair |
| Path / walk | Connected sequence of vertices and edges; a path does not repeat vertices |
| Tree / forest | Connected acyclic undirected graph / collection of trees |
| DAG | Directed acyclic graph |
| Bipartite graph | Two vertex sets with edges only across sets |
| Connected component | Maximal connected group; directed graphs distinguish weak and strong connectivity |
| Subgraph / projection | Selected nodes, edges or relationship types; explicitly state any direction, weight or edge-collapse transformation |
| Neighborhood | Nodes adjacent to a reference; expansion may include a selected number of hops |

A weighted graph and a DAG are properties/views, not separate mandatory stores. Knowledge Positions exposes its NetworkX MultiDiGraph; the intelligence creates the appropriate view. Never discard direction or parallel evidence accidentally.

## 3. Core graph algorithms

Use NetworkX directly. These are the ten fundamental algorithms from the supplied reference, plus the minimal dependency and neighborhood operations already used by the library.

| Algorithm | Native operation | Use over our work |
|---|---|---|
| Depth-first search | nx.dfs_preorder_nodes | Follow a chain of relationships |
| Breadth-first search | nx.bfs_tree | Explore nearby knowledge level by level |
| Topological sort | nx.topological_sort | Order a DAG; reverse dependent→prerequisite edges to put prerequisites first |
| Union-find | nx.utils.UnionFind | Group connected references incrementally |
| Cycle detection | nx.find_cycle | Find circular dependencies or cyclic graph paths |
| Connected components | nx.connected_components / weakly_connected_components / strongly_connected_components | Identify connected groups and isolated knowledge |
| Bipartite check | nx.is_bipartite | Test whether a selected graph admits two partitions |
| Flood fill | nx.node_connected_component or descendants | Expand from a seed through permitted edges |
| Minimum spanning tree/forest | nx.minimum_spanning_tree | Connect an undirected weighted view at minimum total cost |
| Shortest path | nx.shortest_path | Find a route by hops or justified nonnegative edge cost |
| Ancestors / descendants | nx.ancestors / nx.descendants | Trace impact or prerequisites along explicit dependency direction |
| Neighborhood / subgraph | nx.ego_graph / G.subgraph | Select a working knowledge neighborhood |

A topological sort is valid only for a DAG; a cycle is a result to investigate, not silently remove. Union-find, bipartite and spanning tree operations use explicit undirected views. Unit costs are a valid demonstration, not measured strength. A similarity score is not a path cost; define the transformation before using weights. Flood fill follows selected connectivity, not arbitrary semantic similarity. [NetworkX algorithms](https://networkx.org/documentation/stable/reference/algorithms/index.html).

## 4. Core vector vocabulary

| Core term | Meaning / operation |
|---|---|
| Embedding | Numeric representation of a knowledge item produced by a named model and preprocessing |
| Dimension | Number of coordinates; not a measure of truth or importance |
| Embedding space | Vectors from a compatible model, revision and preprocessing |
| Normalize / norm | Scale a nonzero vector to unit length; handle zero vectors explicitly |
| Dot product | Sum of coordinate products; equals cosine similarity for unit vectors |
| Cosine similarity / distance | Angular similarity; distance = 1 − cosine similarity |
| Euclidean distance | Straight-line distance in the embedding space |
| Nearest neighbors / top-k | Rank candidates by an explicitly chosen similarity or distance |
| Threshold | Select candidates meeting a specified criterion; calibrate to the corpus |
| Centroid | Mean representation of a selected group, optionally normalized |
| Cluster | Group similar vectors using a selected method; a candidate grouping, not established knowledge |
| Similarity graph | Nodes connected by a declared neighbor/threshold rule; edges are discovery leads, not facts or dependencies |

Sentence Transformers supplies semantic embeddings; NumPy supports basic vector operations. The current library implements cosine top-k; the other operations can be performed directly on its vectors. Compare only compatible vector spaces; lexical hashed vectors are not semantic embeddings. Do not interpret a vector score as confidence in truth. Clustering may use an appropriate external algorithm if the investigator needs it; no mandatory clustering dependency.

## 5. Working rule

Choose the graph, relationship types, direction, weights and algorithm that answer the question. Use vector discovery to find candidates, graph operations to investigate connections, and source positions to verify original evidence. Save useful qualified discoveries; preserve history and deprecate outdated knowledge. No custom graph engine, mandatory ontology, or new database is required.

## First pass: Core + three required positions

Every admitted knowledge item first receives one common identity and three positional slots: **location** (original source address, version and exact coordinates), **relation** (graph node identity and any known qualified relationships), and **proximity** (a compatible embedding/vector position). Proximity is computed against other vectors when needed; it is not a factual relationship. A graph position is required even when no relationship has yet been established. Do not invent edges to fill a graph.

The twelve core relationship types are the first-pass relationship vocabulary. Record only relationships actually supported by the source or qualified as candidates. Additional domain-specific relationships and deeper discoveries belong to enrichment. Enrichment extends the first pass without replacing original evidence or changing human intent. A required slot may be unknown: use a separate status and a null value, never a fabricated coordinate. The library implements deferred embeddings (`vector=null`, `vector_status='unknown'`) and source-verified `fill_vector`. Unknown vectors remain graph nodes but do not participate in similarity calculations. Source-backed admission still requires the actual source identity, version and coordinates; unresolved original-source locators are recorded as leads, not exact source spans.

**Location is not access or ownership.** A source record retains its owner, observed version and verified coordinates separately from possible access realms/routes. Current discover/read/write rights must be checked by the current environment; a graph reference to a private provider chat or an SSH-only source is not an access grant. See the [portable location guidance](LOCATION_ACCESS.md). Structural indexing may cover many sources cheaply, but **LLM enrichment is performed only when work has already touched and read relevant source content**. Initial admission counts as enrichment touch 1; a node or explicit cluster can receive only two more semantic mutation passes. After touch 3 its payload freezes until verified source mutation starts a new epoch; later discoveries link outward as new knowledge/relationships.

### Item-internal structural position

An item's **source position** (owner/source/version/span) and its **internal structural position** (ordered node path, parent path, depth, sibling index) answer distinct questions. The library can attach a source-version-scoped `item_location` using a native structural path, stable anchor or exact line/byte coordinate from a deterministic reader, or an explicitly qualified observer. It selects methods in the [standard priority order](LOCATION_ACCESS.md#shared-location-method-selection-source-agnostic), preserving other verified coordinates; new locator conventions are provisional and recorded for consistent future reads. Python AST uses its *existing traversal method*, not an AST requirement for every source. Webpage paragraph placements described by an LLM are `locator_only` until a trusted source adapter can resolve them. Structural metadata can inform retrieval and optional embedding input; merely storing a path does not recompute or improve existing vectors. The library updates this metadata independently of source node IDs or content hashes, and a host/watchdog may invoke it when files are read.

### Capture knowledge that enables graph algorithms

Do not merely project whatever edges happen to exist. When work establishes a prerequisite, source derivation, or meaningful workflow ordering, retain that information at the appropriate source/version/event identity. Core `requires` records the dependent → prerequisite direction; reverse it in a prerequisite-first DAG for topological ordering. Enrichment may add qualified derivation or execution relationships. Distinguish an actual experiment, its evidence, and a later note documenting it; a note about a paper is not the original experiment. Check the selected DAG for cycles and investigate conflicts rather than deleting legitimate relationships. The full knowledge graph may contain cycles; only a graph intended to encode acyclic precedence must satisfy this invariant. Do not invent prerequisites or timestamps to make an algorithm succeed.

## Named graph capabilities — out of the box

These are the ten native views available through `KnowledgePositions.graph_view(kind, name=...)`. The names are discoverable in `KnowledgePositions.GRAPH_VIEWS`. They are conveniences, not a closed graph language.

| View name | What it is for | How to select it |
|---|---|---|
| directed | Directional navigation and cycle checks | graph_view('directed') |
| undirected | Connectivity, reciprocal navigation, union-find | graph_view('undirected') |
| weighted | Cost-aware paths and spanning trees | graph_view('weighted', unit_cost=True) or provide actual edge costs |
| multigraph | Preserve parallel relationships and evidence | graph_view('multigraph') |
| tree | Rooted investigation/hierarchy traversal | graph_view('tree', root=node_id) |
| forest | Minimum spanning forest across connected groups | graph_view('forest', unit_cost=True) |
| dag | Prerequisite-first ordering from explicit dependencies | graph_view('dag') |
| bipartite | Reference–relationship incidence, or caller-selected disjoint sets | graph_view('bipartite') |
| similarity | Candidate proximity links from compatible known vectors | graph_view('similarity', threshold=0.25) |
| neighborhood | Bounded local investigation | graph_view('neighborhood', root=node_id, radius=2) |

Use an investigation-specific name for reproducibility. The optional relation filter restricts the input; costs must be justified or explicitly unit cost. A DAG reports cycles rather than hiding them. The default bipartite view uses real relationship records as incidence nodes, not invented factual edges. Tree and forest views are calculated structures, not claims that the full knowledge graph is a hierarchy. Unknown vectors remain nodes without similarity edges.

If a graph structure is not listed, calculate it from the data: use ordinary NetworkX operations on the detached graph, or call `derive_graph(name, transform, source=...)`. For example, `k.derive_graph('navigation-components', nx.condensation, source='directed')` calculates a condensation DAG; `k.derive_graph('relationship-line-graph', nx.line_graph, source='directed')` calculates a line graph. An investigator may use other libraries as appropriate. The original graph is never rewritten merely to satisfy a structural property. If the data do not support a requested *meaning* (e.g., verified causation, measured cost, a real partition), capture missing evidence rather than fabricate it.

`k.core_algorithms(root, target)` runs the ten core algorithms and reports which named view each used. Record useful results, selected views, parameters, original source version and evidence in the evolving knowledge graph; retain only qualified relationships, not every temporary derived edge.

## Working-context retrieval

Use `chat_context` for working conversations. The default policy is Personalized PageRank / random-walk-with-restart attenuation from the selected root, with a transparent `conservative`, `balanced`, or `aggressive` profile. No fixed hop depth is imposed. When an ego radius is genuinely the desired graph operation, request `retrieval='ego'` and an explicit radius. `other` contains immediate boundary references not loaded into the working set. Graph calculations and cascading dependency staleness remain full-graph operations. API writes clear the derived cache; direct NetworkX mutations require `invalidate_cache()`.
