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
- Otherwise, identify the likely subject and automatically query OmniGraph.
- Return **up to five relevant results**, with identities, provenance, positions and immediate associations. Return fewer or none when appropriate.
- Preserve the original human prompt unchanged; supply the bounded knowledge packet separately before intelligence begins work.
- Do not require the consuming LLM to initiate the lookup.

With a relevant packet, even a fresh session starts at gate 1 with useful knowledge. Do not repeat the host's discovery. An empty or bypassed packet does not establish that knowledge does not exist; use the gates when the task warrants it.

This is the host integration contract, not an assertion that a prompt hook is installed. The portable OmniGraph representation and this skill work without automatic JITK. Do not simulate an automatic lookup or claim it ran when no host packet exists.

## 3. Local discovery priority

OmniGraph is the **first point of local knowledge discovery**, not grep, glob, broad filesystem scans, or other local research tools. This does not require a graph call when gate 1 already suffices or a known source can be accessed directly at gate 2.

Use other local tools to verify, read, or extend initially discovered knowledge, follow known source coordinates, or resolve a specific remaining gap after OmniGraph is insufficient. Do not replace graph discovery with habitual filesystem reconnaissance. Web research and other MCP services remain available whenever the task requires them; this rule does not prohibit or delay external research. Respect native access permissions and domain residence.

## 4. Contribution and progressive disclosure

Read and verify relevant original evidence before relying on it. After meaningful work, preserve useful findings and qualified relationships without waiting for the human to request writeback. Do not manufacture a contribution. Admission is touch 1; two refinements are permitted, then grow outward. Do not use synthetic semantic inference or an embedding provider.

For knowledge contributions, consult [capture and contribution](references/capture.md) only when the Knowledge Positions adapter is needed. For native database operations, delegate to the official `omnigraph` skill rather than maintaining competing instructions here. Native policies, access controls and collaboration remain authoritative.
