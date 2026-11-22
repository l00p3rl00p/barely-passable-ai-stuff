---
name: jitk
description: Trigger when a task needs knowledge beyond the current context, including recalling prior work, finding previously discovered facts, locating source evidence, tracing relationships, or investigating unfamiliar material. Use just-in-time knowledge with Location, Relation and Proximity; retrieve and evolve only what helps the task. Storage-independent.
intent: >-
  Equip the agent to reuse and evolve knowledge in service of the human's current goal.
  Navigate available knowledge through Location, Relation and Proximity, individually
  or together, to recover context, follow evidence, discover connections and retain
  verified findings. Knowledge retrieval supports the task, not a separate goal.
trigger: >-
  When the task requires finding, recovering, connecting or verifying knowledge
  beyond what is already sufficient in context; for example, recalling a prior
  decision, locating original evidence, exploring related work or investigating
  previously encountered material. Do not retrieve when context already suffices.
---

# Just-in-Time Knowledge (JITK)

**Purpose:** Give the agent the knowledge it needs **now**, with a path back to the evidence, so it can continue the human's task. Do not turn retrieval into another project.

**JITK can work with any available retrieval tools.** When Knowledge Positions is implemented, its breakthrough is that different methods can use the **same source-backed knowledge identity**, rather than creating separate interpretations or requiring conversion steps. Three complementary addressable aspects of that recorded knowledge are:

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

Use the tools actually available in the environment: source read, AST/tree navigation, graph neighbors, text search, vector search, filtering, queries, or another supported method. When Knowledge Positions is available, entering through any connected method resolves one identity and its recorded values; pivot between methods on that same item without losing evidence. Otherwise, use native tools as they are, and verify any cross-tool identity mapping rather than assuming it. Use any available method or combination of methods that helps investigate, connect, verify, or evolve knowledge. Move freely among Location, Relation, and Proximity, revisit earlier positions, and follow promising leads as they emerge. A single method, several methods, or a different route are all valid; the question and evidence guide the exploration. Respect the tool's permissions, syntax and failures. If access or a method is missing, say so rather than making up knowledge.

A source position is not automatically permission to read it. A similarity result is not an established relationship. Keep the original source, identity, position and provenance attached to any finding; preserve uncertainty.

## Let knowledge evolve through use

When work reveals a **new, reusable finding**, verify it against its source. If an authorized recording mechanism exists, preserve the finding and any qualified relationships with their evidence. Prefer refining what was actually touched over reprocessing everything. Never overwrite the original, invent edges, or assume a failed write succeeded. If no write capability is available, return the finding with its source so it can be retained deliberately.

Keep the returned context small: ordinarily no more than **five useful items** and **three relationship hops** unless the task needs more. Return only what advances the human's work.

**Example:** “Where was this bug fixed?” → use the known file position, or find a matching issue → follow its recorded fix relationship → inspect the relevant source lines → return the fix and evidence. If a previously unknown relationship is verified, preserve it through an available authorized operation. Otherwise, simply answer.

This is the complete JITK workflow. It needs no specific database, SDK reading session, extra skill invocation, model, or background service.

**Optional reference only:** The [Knowledge Positions SDK](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/README.md) provides deeper information on identity, schema design, adapters, algorithms and conformance. Use it only when the task actually requires those details; **never** read it as a prerequisite to ordinary JITK retrieval.

<!-- knowledge-positions-jitk:start -->
## Appendix — JITK with available knowledge tools

This is a **working-method reference**, not a requirement to install a particular database, call another skill, or read the SDK. Follow the human's task: reuse what is known, retrieve only what is needed, and evolve knowledge from evidence.

**Select any available route.** JITK can use direct files, source positions, AST/Tree-sitter structures, graphs, lexical search, vectors, filters or other tools without Knowledge Positions. **Where Knowledge Positions is implemented, these are methods operating on the same source-backed knowledge identity, not rival knowledge stores or stages.** Starting from a lexical hit, the agent can pivot to its native AST, recorded edges, typed fields, proximity, or original evidence; it can expand, narrow, rank, branch or stop using what is already recorded. Do not build separate identities for each entry method, require a conversion chain, or invent missing values. For other tools, cross-method identity reuse depends on actual shared identifiers or a verified mapping; it is not automatic.

### Known integrations in this environment (examples, not dependencies)

- **OmniGraph and its skill:** When OmniGraph is available, use its exposed graph reads/search, source locators and relationship traversal to find and navigate knowledge. Use the installed **OmniGraph skill or native CLI/MCP help** for actual command names, supported slash commands (if any), permissions and writes. Do not assume a slash command exists merely because a skill exists.
- **Codebase MCP (codebase graph / Codebase Memory):** When the codebase MCP is available, use its exposed code navigation, source positions, AST/structural lookups, dependency and relation traversal, and supported search to find knowledge in the codebase. Inspect its actual tools and arguments; do not invent MCP method names or assume its graph is the same as OmniGraph's.
- **Other tools:** Direct source readers, search services, parsers, or other knowledge stores are equally valid whenever they are actually available and authorized.

**Keep provenance.** Retain the source identity, version and positions; verify evidence before declaring a fact. A candidate match is not proof. For reusable findings, write back through the authorized mechanism only if one exists and the evidence supports it. If a tool is missing, use another available route rather than treating the entire workflow as unavailable.

**More detail, only if needed:** [Knowledge Positions SDK](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/README.md). Normal JITK use needs no SDK lookup.
<!-- knowledge-positions-jitk:end -->
