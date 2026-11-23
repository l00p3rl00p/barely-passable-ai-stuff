---
name: knowledge-positions
description: Generic just-in-time knowledge workflow: reuse, direct access, relationship exploration, discovery, and source-backed contribution. Choose available access methods and delegate engine operations to the selected implementation's own API, documentation, or skill.
---
# Knowledge Positions — just in time

**Knowledge = { Position. Relation. Proximity. Resonance. }**

Position is where and within where; relation is qualified association; proximity is clustering in a declared space; resonance is importance learned through use (research, not implemented).

## 0. Primary skill and startup context

**This is the primary knowledge-behavior skill.** It decides whether existing context is sufficient, whether to access a known source, whether to explore associations, and whether fresh discovery or source-backed contribution is needed. It does **not** duplicate the database engine's operational instructions.

**Host startup contract:** Make this generic `knowledge-positions` skill available at session start if the host uses JITK. Load the selected implementation's own skill or API documentation only when its operations are needed. The host/harness is responsible for installing and loading skills. Startup context availability is **not** an instruction to scan, connect, search, ingest, mutate, or re-read the SDK.

**Delegation:** This skill controls *whether, why and which knowledge* is needed, not how a particular engine operates. After selecting an available source reader, library, or store, use that implementation's actual APIs, tools, documentation, or skill for syntax, configuration, permissions, queries, writes, and recovery. Do not infer support from the UKC SDK or invent commands. For OmniGraph specifically, use the official [OmniGraph skill](https://github.com/ModernRelay/omnigraph/blob/main/skills/omnigraph/SKILL.md), preferably version-matched to the installed CLI. The selected implementation's access policy remains authoritative.

## 0. SDK reference in the knowledge graph

The [Unified Knowledge Context (UKC) SDK](../../../../unified-knowledge-context.md) is an optional reference for schema, record, adapter, or compatibility work, **not** a prerequisite for ordinary retrieval. Do not load the entire SDK to answer an ordinary knowledge question.

**Optional reference indexing:** When establishing a knowledge repository that should answer questions about the SDK, ingest the SDK **document collection** (the index plus relevant linked components) as source-backed material if the user or host chooses to. Reuse a current existing index; do not repeatedly ingest or re-embed it. Indexing is not needed for normal JITK retrieval.

When changing a schema, adapter, or Knowledge Positions record mapping, consult only the relevant SDK contract section if needed. The selected implementation remains authoritative for actual operations and permissions. Do not auto-run ingestion or block unrelated work waiting for it.

## 0. Available knowledge positions and composable traversal

**At the point of use, identify which access methods and original values are actually available for the same knowledge identity.** Do not assume all three are populated, require a sequence, or create substitute stores or independent identities.

**How to select an available access method:** (1) List the tools, native readers, APIs or search capabilities *actually exposed by the host or selected implementation*; do not infer support from a schema or the SDK. (2) If the source or identity is known and resolvable, select direct Position access. (3) If a node is known and observed/qualified edges are accessible, select Relation traversal. (4) If the subject is approximate or location unknown, select an available lexical, fuzzy, or compatible vector Proximity search. (5) Combine methods only when the next step adds evidence; stop when sufficient. If no method is available, state the capability gap rather than simulating an index or response. The source-specific API/skill supplies exact calls and permissions.

| Access method | Available when | What an agent can use |
|---|---|---|
| **Position / structure** | Source locator, byte/line/section coordinates, or a preserved native AST/parse structure exists | Direct source navigation, section/AST parent-child-sibling lookup, Tree-sitter or another suitable parser for a *specific* source when fresh parsing is needed |
| **Relation / graph** | Observed or qualified links, endpoints, labels, and their provenance exist | Available graph queries and bounded traversal; NetworkX or another algorithm over actual returned nodes and edges when useful |
| **Proximity / similarity** | Lexical terms, declared embedding/vector space, or supported similarity values are available | Exact/lexical discovery, vector similarity or nearest-neighbor search in the actual indexed space; compare vectors only when model/space and dimensions match |

**LLM chooses the method:** Position only, Relation only, Proximity only, any pair, or all three are valid. The available positions and algorithms are a capability menu, **not an execution plan or mandatory pipeline**. Let the LLM select the most useful available technique(s) for the question and evidence, including a direct answer with no traversal when context already suffices. Use additional methods only when useful; stop once the evidence is sufficient. For example, vector similarity can find an ID, graph traversal can follow its observed neighbors, and position can locate the exact original passage; or a known AST position can directly answer a request without any search. Switching methods **keeps the same knowledge identity and common record**. Do not convert AST into a new knowledge graph, graph results into new knowledge identities, or vector hits into asserted relationships. A search score is a discovery lead, not evidence of a graph edge.

**Available algorithmic toolbox (examples, not a pipeline):** The LLM should recognize these standard methods, check which are available through recorded knowledge, the selected implementation's advertised capabilities, and installed tools, then **choose any useful single method or combination**. This menu neither installs them nor claims every one is implemented by the selected source or store.

| Family | Algorithms and access patterns | Common uses |
|---|---|---|
| **Tree / hierarchy (Position)** | Parent/child, ancestor/descendant and sibling navigation; subtree and path lookup; **preorder** (node before children), **postorder** (children before node), **inorder** (left–node–right for ordered binary trees), **breadth-first/level-order**, **depth-first**, lowest common ancestor, depth/height | Inspecting document outlines, directory/section containment, nested structures and hierarchy-local evidence |
| **AST / syntax (Position)** | Native source positions and Tree-sitter or an available parser; node-by-type or named-field selection, byte/line range lookup, parent/child/sibling/ancestor navigation, preorder/postorder walks, subtree/structural pattern matching, symbol/definition/reference traversal **when the source actually records those links** | Finding code constructs, definitions, usages, sections or source-exact spans without interpreting text semantically |
| **Graph / network (Relation)** | BFS/DFS, bounded neighborhood/reachability, connected components, union-find/DSU, cycle detection, topological sort (directed acyclic graphs), shortest path (weighted or unweighted as appropriate), bipartite check, minimum spanning tree (weighted undirected graphs), flood fill | Tracing evidenced associations, dependency chains, groups, cycles, routes and connectivity |
| **Vector / proximity (Proximity)** | **Exact/brute-force kNN** (score all comparable vectors), **IVF** (inverted-file cluster candidates), **HNSW** (approximate navigable proximity graph), **PQ** (product quantization/compression), filtered or **hybrid lexical + vector** retrieval, sparse/dense search, top-k, thresholds and reranking; cosine, dot-product or Euclidean metrics when appropriate | Finding candidate identities from imperfect similarity leads, narrowing large candidate sets, and trading recall against speed/storage when supported |

**Method-specific boundaries:**
- **Tree order matters.** Inorder is defined for a binary tree with left/right child order; a general hierarchy need not support it. BFS and DFS can apply to trees *or* graphs. Traversal order helps select evidence; it does not establish new semantic relationships.
- **AST is recorded structure.** Reuse existing syntax nodes and coordinates first. Tree-sitter can supply faithful syntax structure when it is installed and a source must be parsed; it does not automatically establish semantic references, call graphs or embeddings.
- **Graph algorithms need actual edges.** Use the selected implementation's graph features where supported, or an available tool such as NetworkX on a bounded returned subgraph. Respect edge direction, weights and provenance. An HNSW neighbor graph is **search-index machinery**, not a qualified Knowledge Positions relation.
- **Vector methods have different roles.** Brute-force is an exact baseline; IVF and HNSW are approximate candidate-selection/index approaches; PQ is quantization/compression often combined with an index; hybrid search combines signals and may rank/rerank them. Do **not** assume these index types are installed, expose commands for them, or build separate authoritative knowledge stores. First inspect the actual vector field/space, index and supported query capabilities. Compare vectors only when space, dimensions and metric are compatible; a similarity hit is a lead, not proof.
- **One knowledge identity throughout.** Tree/AST Position, graph Relation and vector/lexical Proximity access the **same source-backed common record**, singly or together, in whichever order the LLM finds helpful. Existing values are reused; no compulsory conversion or enrichment chain. When a method cannot be used, use the others without fabricating structure, relationships, vectors or results.

**Examples, not recipes:** A direct AST span may answer a question by itself; preorder may enumerate a hierarchy; shortest path may connect known related records; hybrid or HNSW search (if actually available) may discover a candidate whose original source is then read through Position. The LLM is free to choose another method or to stop with existing context.

**Tools are methods, not dependencies:** Use Tree-sitter, NetworkX, available graph traversal, lexical/vector search, or their available equivalents when the host actually supplies them and the task merits them. Prefer already recorded source structure, graph relationships, or proximity rather than recomputing. If a method is unavailable or a position is not populated, mark it unavailable/unknown and use another available method; never fabricate parser results, links or vectors. Any on-demand parsing must preserve source and version provenance. A NetworkX algorithm may operate on bounded graph data retrieved from any authorized source; it does not become a second authoritative graph.

**Keep traversals bounded and source-backed.** Default to up to three relationship hops and up to five useful knowledge identities unless the task or host policy specifies otherwise. Preserve source coordinates, relation provenance and vector-space labels. Verify exact source bytes/version for source-evidence claims. The selected implementation's own skill, APIs and policies remain authoritative for query syntax, indexing, permissions and operational limits.

## 1. Knowledge access escalation

Begin with the original human prompt, working context, and any JIT packet already supplied. Pass these four decision gates in order. They are not four mandatory retrieval operations.

| Gate | Question |
|---|---|
| 1. Reuse | Is the necessary knowledge already in context? |
| 2. Direct access | Is the location or node identity already known? |
| 3. Explore | Can a known node's immediate associations resolve the question? |
| 4. Discover | Is a new knowledge search necessary? |

**Stop if sufficient. Escalate only if insufficient.** Do not query again merely because a new tool call, agent, or turn begins. Reuse previously verified unchanged evidence and known coordinates. Do not reload the corpus, whole cookbook, or full graph inventory by default. Investigate only the additional knowledge needed for the task.

### 5. Agentic coordination (continuous, not a fifth retrieval gate)

Native agent coordination can update the knowledge available at any of gates 1–4. Relevant contributions, handoffs, and shared work can supply context, identify a known position, expose a relationship, or reveal an unresolved discovery need. Incorporate relevant updates when available, then reassess sufficiency from gate 1. Do not duplicate another agent's completed discovery or poll unnecessarily.

## 2. Automatic JITK contract (host responsibility)

When a host implements prompt-triggered JITK:

- Prompts under **15 trimmed characters** bypass automatic discovery.
- Otherwise, identify the likely subject and retrieve a bounded knowledge packet using whichever recorded Position, Relation and/or Proximity methods are actually available through the host's selected implementation; use one method or combine them as useful.
- Return **up to five relevant results**, with identities, provenance, positions and immediate associations. Return fewer or none when appropriate.
- Preserve the original human prompt unchanged; supply the bounded knowledge packet separately before intelligence begins work.
- Do not require the consuming LLM to initiate the lookup.

With a relevant packet, even a fresh session starts at gate 1 with useful knowledge. Do not repeat the host's discovery. An empty or bypassed packet does not establish that knowledge does not exist; use the gates when the task warrants it.

This is the host integration contract, not an assertion that a prompt hook is installed. This skill works without an automatic JITK hook or any particular storage engine. Do not simulate an automatic lookup or claim it ran when no host packet exists.

## 3. Local discovery priority

After the Reuse and Direct access gates, prefer an **available, already indexed knowledge service or qualified source locator** for discovery instead of broad filesystem reconnaissance. Select the service by actual capability, scope and authorization—not by a hard-coded database name. Graph, AST/tree, lexical, vector and direct-source methods are all valid; do not automatically prefer embeddings or a graph query.

Use other local tools for targeted verification, direct source reads or an unresolved gap after the preferred method is insufficient. Web research and external MCP services remain available when appropriate. Respect native access permissions, source residence and any host-defined method priority.

## 4. Contribution and progressive disclosure

Read and verify relevant original evidence before relying on it. After meaningful work, preserve useful findings and qualified relationships without waiting for the human to request writeback. Do not manufacture a contribution. Admission is touch 1; two refinements are permitted, then grow outward. Do not use synthetic semantic inference or an embedding provider.

For qualified contributions, consult the **selected implementation's** evidence-admission API or skill only when a write is warranted and authorized. For example, the [OmniGraph Knowledge Positions adapter capture reference](references/capture.md) applies only when that adapter is selected. Native policies, access controls and collaboration remain authoritative; do not invent a universal write command.
