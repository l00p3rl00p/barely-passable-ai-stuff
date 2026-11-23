# Agent knowledge-access decisions (non-normative profile)

These are optional agent workflow gates, not additional UKC/1 methods or mandatory SDK calls.

Begin with the original human prompt, working context, and any JIT packet already supplied. Pass these four decision gates in order. They are not four mandatory retrieval operations.

| Gate | Question |
|---|---|
| 1. Reuse | Is the necessary knowledge already in context? |
| 2. Direct access | Is the location or node identity already known? |
| 3. Explore | Can a known node's immediate associations resolve the question? |
| 4. Discover | Is a new knowledge search necessary? |

**Stop if sufficient. Escalate only if insufficient.** Do not query again merely because a new tool call, agent, or turn begins. Reuse previously verified unchanged evidence and known coordinates. Do not reload the corpus, whole cookbook, or full graph inventory by default. Investigate only the additional knowledge needed for the task.

## Agentic coordination (continuous, not a fifth retrieval gate)

Native agent coordination can update the knowledge available at any of gates 1–4. Relevant contributions, handoffs, and shared work can supply context, identify a known position, expose a relationship, or reveal an unresolved discovery need. Incorporate relevant updates when available, then reassess sufficiency from gate 1. Do not duplicate another agent's completed discovery or poll unnecessarily.

