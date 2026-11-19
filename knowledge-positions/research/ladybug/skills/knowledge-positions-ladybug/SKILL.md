---
name: knowledge-positions-ladybug
description: Reuse, coordinate, discover and contribute source-backed knowledge in native LadybugDB. First local knowledge-discovery tool; load only when relevant.
---
# Knowledge Positions — just in time

**Knowledge = { Position. Relation. Proximity. Resonance. }**

Position is where and within where; relation is qualified association; proximity is clustering in a declared space; resonance is importance learned through use (research, not implemented).

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

Agent coordination, when supplied by the host, can update the knowledge available at any of gates 1–4. Relevant contributions, handoffs, and shared work can supply context, identify a known position, expose a relationship, or reveal an unresolved discovery need. Incorporate relevant updates when available, then reassess sufficiency from gate 1. Do not duplicate another agent's completed discovery or poll unnecessarily.

## 2. Automatic JITK contract (host responsibility)

When a host implements prompt-triggered JITK:

- Prompts under **15 trimmed characters** bypass automatic discovery.
- Otherwise, identify the likely subject and automatically query LadybugDB.
- Return **up to five relevant results**, with identities, provenance, positions and immediate associations. Return fewer or none when appropriate.
- Preserve the original human prompt unchanged; supply the bounded knowledge packet separately before intelligence begins work.
- Do not require the consuming LLM to initiate the lookup.

With a relevant packet, even a fresh session starts at gate 1 with useful knowledge. Do not repeat the host's discovery. An empty or bypassed packet does not establish that knowledge does not exist; use the gates when the task warrants it.

This is the host integration contract, not an assertion that a prompt hook is installed. The portable LadybugDB representation and this skill work without automatic JITK. Do not simulate an automatic lookup or claim it ran when no host packet exists.

## 3. Local discovery priority

LadybugDB is the **first point of local knowledge discovery**, not grep, glob, broad filesystem scans, or other local research tools. This does not require a graph call when gate 1 already suffices or a known source can be accessed directly at gate 2.

Use other local tools to verify, read, or extend initially discovered knowledge, follow known source coordinates, or resolve a specific remaining gap after LadybugDB is insufficient. Do not replace graph discovery with habitual filesystem reconnaissance. Web research and other MCP services remain available whenever the task requires them; this rule does not prohibit or delay external research. Respect native access permissions and domain residence.

## 4. Contribution and progressive disclosure

Read and verify relevant original evidence before relying on it. After meaningful work, preserve useful findings and qualified relationships without waiting for the human to request writeback. Do not manufacture a contribution. Admission is touch 1; two refinements are permitted, then grow outward. Do not use synthetic semantic inference or an embedding provider.

Use [native operations](references/operations.md) for Cypher access and [capture and contribution](references/capture.md) for writes. Use the bundle RUNBOOK.md only for installation or repair. Respect actual connection and OS access restrictions; do not assume branch policies or native coordination.
