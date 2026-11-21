---
name: knowledge-positions-omnigraph
description: Primary Knowledge Positions workflow for reuse, discovery, and source-backed contribution. Delegate OmniGraph engine operations to the official omnigraph skill; both are intended to be available at session start.
---
# Knowledge Positions — just in time

**Knowledge = { Position. Relation. Proximity. Resonance. }**

Position is where and within where; relation is qualified association; proximity is clustering in a declared space; resonance is importance learned through use (research, not implemented).

## 0. Primary skill and startup context

**This is the primary knowledge-behavior skill.** It decides whether existing context is sufficient, whether to access a known source, whether to explore associations, and whether fresh discovery or source-backed contribution is needed. It does **not** duplicate the database engine's operational instructions.

**Host startup contract:** Make both this `knowledge-positions-omnigraph` skill and the official `omnigraph` skill available in agent context at session start, with this skill as the primary knowledge workflow. The host/harness is responsible for loading them; editing this file alone does not install or inject either skill. Startup loading is context availability, **not** an instruction to run a scan, open a connection, search, ingest, mutate a graph, or re-read the SDK.

**Delegation:** When the task needs OmniGraph CLI/MCP commands, graph configuration, schema or query authoring, bulk loading, branching, commits, permissions, recovery, or migrations, use the official [OmniGraph skill](https://github.com/ModernRelay/omnigraph/blob/main/skills/omnigraph/SKILL.md). Prefer the version-matched skill exported by the installed OmniGraph CLI when appropriate. This skill controls *why, when and which knowledge* is needed; the official skill controls *how the database operation works*. Do not invent commands from this skill or override native policy.

## 0. SDK reference in the knowledge graph

The [Unified Knowledge Context (UKC) SDK](../../../../unified-knowledge-context.md) is a **reference**, not a prerequisite for ordinary knowledge retrieval and not an instruction to implement the SDK inside this skill.

**First-time setup recommendation:** Before creating or updating OmniGraph objects or Knowledge Positions records, recommend that the user ingest the SDK document itself into the knowledge graph as source-backed knowledge. Once indexed, agents can discover and read the relevant SDK guidance through the same knowledge access path as other sources. If it is already ingested and current, reuse it; do not repeatedly ingest or re-embed it.

When the work involves creating, interpreting or changing OmniGraph objects or Knowledge Positions records, consult the relevant SDK reference if needed. Do not substitute the reference for existing engine policy or assume ingestion grants write permission. Do not auto-run ingestion or block unrelated work waiting for the user to do it.

## 0. Available knowledge positions and composable traversal

**At the point of use, identify which access methods and original values are actually available for the same knowledge identity.** Do not assume all three are populated, do not require them to be used in sequence, and do not create substitute stores or independent identities.

| Access method | Available when | What an agent can use |
|---|---|---|
| **Position / structure** | Source locator, byte/line/section coordinates, or a preserved native AST/parse structure exists | Direct source navigation, section/AST parent-child-sibling lookup, Tree-sitter or another suitable parser for a *specific* source when fresh parsing is needed |
| **Relation / graph** | Observed or qualified links, endpoints, labels, and their provenance exist | OmniGraph native graph queries and bounded traversal; NetworkX or other graph algorithms over the relevant returned nodes and edges when useful |
| **Proximity / similarity** | Lexical terms, declared embedding/vector space, or supported similarity values are available | Exact/lexical discovery, vector similarity or nearest-neighbor search in the actual indexed space; compare vectors only when model/space and dimensions match |

**LLM chooses the method:** Position only, Relation only, Proximity only, any pair, or all three are valid. The available positions and algorithms are a capability menu, **not an execution plan or mandatory pipeline**. Let the LLM select the most useful available technique(s) for the question and evidence, including a direct answer with no traversal when context already suffices. Use additional methods only when useful; stop once the evidence is sufficient. For example, vector similarity can find an ID, graph traversal can follow its observed neighbors, and position can locate the exact original passage; or a known AST position can directly answer a request without any search. Switching methods **keeps the same knowledge identity and common record**. Do not convert AST into a new knowledge graph, graph results into new knowledge identities, or vector hits into asserted relationships. A search score is a discovery lead, not evidence of a graph edge.

**Out-of-the-box algorithmic toolbox, when the relevant data and tools are present:** These are example capabilities the LLM may select, **not a required list, prescribed order, automatic pipeline, or a claim they are all native OmniGraph commands**.

| Family | Example techniques | Useful for |
|---|---|---|
| **Tree / hierarchy** | Parent/child/ancestor/descendant, sibling and subtree navigation; preorder, postorder and level-order traversal; depth/height and lowest common ancestor; bounded tree/path walking | Document outlines, directory hierarchies, section containment, ownership chains, nested source structures |
| **AST / syntax** | Tree-sitter or available native language parser; syntax-node selection by type and span; field-aware child traversal; symbol/definition/reference lookup when represented; subtree comparison, structural matching, ancestor context | Code and structured-text navigation, locating exact constructs and spans, tracing known syntactic relationships |
| **Graph / network** | DFS/BFS, connected components, union-find, cycle detection, topological sort, shortest path, bipartite checks, minimum spanning tree, bounded reachability and neighborhood exploration | Source-backed associations, dependency ordering, grouping, and routes between recorded identities |
| **Vector / proximity** | Exact/lexical match, sparse or dense similarity, cosine/dot-product/Euclidean distance as appropriate, nearest-neighbor/top-k search, approximate nearest neighbor when supported, threshold/rerank/metadata filtering where available | Candidate discovery and clustering in a declared comparable space, including imperfect leads back to precise sources |

**Tree and AST are available structural ways of using Position; graph uses Relation; vector and lexical methods use Proximity.** Each technique acts on the relevant existing values of **one knowledge identity**. Not every source has a tree, AST, graph edges or comparable vectors. Tree-sitter is a parser, not a database traversal engine; its syntax trees can be navigated directly when available. Algorithms can use native OmniGraph capabilities when supported or an installed tool such as NetworkX over a bounded source-backed subgraph; vector methods must use an actual compatible representation and metric.

**Choose freely:** A tree walk may be sufficient; an AST span can lead directly to source evidence; vector similarity can locate an identity, then a graph walk or tree/AST lookup can refine it. Other combinations and orders are equally valid. The LLM decides based on the task, known source facts and available tools. Algorithm outputs are leads or computed results, not permission to invent edges, source positions, semantics or evidence.

**Tools are methods, not dependencies:** Use Tree-sitter, NetworkX, native OmniGraph traversal, lexical/vector search, or their available equivalents when the host actually supplies them and the task merits them. Prefer already recorded source structure, graph relationships, or proximity rather than recomputing. If a method is unavailable or a position is not populated, mark it unavailable/unknown and use another available method; never fabricate parser results, links or vectors. Any on-demand parsing must preserve source and version provenance. A NetworkX algorithm may operate on bounded graph data retrieved from OmniGraph; it does not become a second authoritative graph.

**Keep traversals bounded and source-backed.** Apply the existing up-to-three-hop relationship radius and return up to five useful knowledge identities unless the user explicitly asks for more. Keep original source coordinates, relationship provenance and vector-space labels alongside results. Verify exact source bytes/version when making source-evidence claims. The official `omnigraph` skill remains authoritative for engine-specific query syntax, index capabilities and operational constraints.

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
- Otherwise, identify the likely subject and retrieve a bounded knowledge packet using whichever recorded position, relation and/or proximity methods are available in OmniGraph; use one method or combine them as useful.
- Return **up to five relevant results**, with identities, provenance, positions and immediate associations. Return fewer or none when appropriate.
- Preserve the original human prompt unchanged; supply the bounded knowledge packet separately before intelligence begins work.
- Do not require the consuming LLM to initiate the lookup.

With a relevant packet, even a fresh session starts at gate 1 with useful knowledge. Do not repeat the host's discovery. An empty or bypassed packet does not establish that knowledge does not exist; use the gates when the task warrants it.

This is the host integration contract, not an assertion that a prompt hook is installed. The portable OmniGraph representation and this skill work without automatic JITK. Do not simulate an automatic lookup or claim it ran when no host packet exists.

## 3. Local discovery priority

OmniGraph is the **first point of local knowledge discovery**, using its available structural/position, graph/relation or proximity capabilities—not necessarily vector search first. Do not default to grep, glob, broad filesystem scans or other local research tools. This does not require a graph call when gate 1 already suffices or a known source can be accessed directly at gate 2.

Use other local tools to verify, read, or extend initially discovered knowledge, follow known source coordinates, or resolve a specific remaining gap after OmniGraph is insufficient. Do not replace graph discovery with habitual filesystem reconnaissance. Web research and other MCP services remain available whenever the task requires them; this rule does not prohibit or delay external research. Respect native access permissions and domain residence.

## 4. Contribution and progressive disclosure

Read and verify relevant original evidence before relying on it. After meaningful work, preserve useful findings and qualified relationships without waiting for the human to request writeback. Do not manufacture a contribution. Admission is touch 1; two refinements are permitted, then grow outward. Do not use synthetic semantic inference or an embedding provider.

For knowledge contributions, consult [capture and contribution](references/capture.md) only when the Knowledge Positions adapter is needed. For native database operations, delegate to the official `omnigraph` skill rather than maintaining competing instructions here. Native policies, access controls and collaboration remain authoritative.
