---
name: jitk
description: Use just-in-time knowledge to answer a task by reusing, locating, exploring, and discovering source-backed information only as needed. Evolve useful knowledge through its positions without depending on a particular storage engine.
---

# Just-in-Time Knowledge (JITK)

**Purpose:** Give the agent the knowledge it needs **now**, with a path back to the evidence, so it can continue the human's task. Do not turn retrieval into another project.

Knowledge has three useful positions, all referring to the **same knowledge**:

- **Location:** Where is it in the original source? File, message, section, AST node, line or byte span.
- **Relation:** What is actually connected to it? Parent, child, dependency, reference, supported or contradicted claim.
- **Proximity:** What might be nearby or similar? Names, words, fuzzy matches or compatible vectors. Similarity suggests where to look; it does not prove a fact.

## Do the smallest useful lookup

1. **Reuse.** If the answer or relevant evidence is already in the working context, use it. Do not search again.
2. **Go directly.** If the source or identity is known, read that position. Check its source/version when exact evidence matters.
3. **Explore.** If a related position is known, follow its existing, evidence-backed relationships only as far as useful.
4. **Discover.** Otherwise, use an available lexical, structural, graph or similarity search to find candidates, then inspect the real source.

**Stop when the evidence is sufficient.** These are decision gates, not four required tool calls.

## Choose the method that exists

Use the tools actually available in the environment: source read, AST/tree navigation, graph neighbors, text search, vector search, or another supported method. Use any available method or combination of methods that helps investigate, connect, verify, or evolve knowledge. Move freely among Location, Relation, and Proximity, revisit earlier positions, and follow promising leads as they emerge. A single method, several methods, or a different route are all valid; the question and evidence guide the exploration. Respect the tool's permissions, syntax and failures. If access or a method is missing, say so rather than making up knowledge.

A source position is not automatically permission to read it. A similarity result is not an established relationship. Keep the original source, identity, position and provenance attached to any finding; preserve uncertainty.

## Let knowledge evolve through use

When work reveals a **new, reusable finding**, verify it against its source. If an authorized recording mechanism exists, preserve the finding and any qualified relationships with their evidence. Prefer refining what was actually touched over reprocessing everything. Never overwrite the original, invent edges, or assume a failed write succeeded. If no write capability is available, return the finding with its source so it can be retained deliberately.

Keep the returned context small: ordinarily no more than **five useful items** and **three relationship hops** unless the task needs more. Return only what advances the human's work.

**Example:** “Where was this bug fixed?” → use the known file position, or find a matching issue → follow its recorded fix relationship → inspect the relevant source lines → return the fix and evidence. If a previously unknown relationship is verified, preserve it through an available authorized operation. Otherwise, simply answer.

This is the complete JITK workflow. It needs no specific database, SDK reading session, extra skill invocation, model, or background service.

**Optional reference only:** The [Knowledge Positions SDK](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/README.md) provides deeper information on identity, schema design, adapters, algorithms and conformance. Use it only when the task actually requires those details; **never** read it as a prerequisite to ordinary JITK retrieval.
