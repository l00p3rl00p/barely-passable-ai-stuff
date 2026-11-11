## 14. Getting started: from an empty graph to working knowledge [EKC:27]

The library and the instructions for using it are different things. The library supplies the mechanics. The human supplies the purpose, source-access boundary, and instructions for the work. Confusing the two would turn a reusable capability into somebody else's prescribed workflow.

A person with no knowledge of any originating project should be able to use Knowledge Positions. They should not need a private project repository, prior conversation history, or a particular model provider.

### The theoretical starting procedure

The starting state need not contain an archive, a precomputed ontology, or a fully enriched graph. An empty knowledge store and one accessible working conversation are sufficient to begin.

## 15. Execution-boundary capture: persistence cannot be an optional thought [EKC:28]

The cold-start test exposed a gap between **a working knowledge library** and **an application that reliably uses it**. An assistant read AGENTS.md, Core Vocabulary and a network diagram, produced two images, and finished without capturing any new knowledge. In a later question it parsed graph.json and filtered edges directly in JavaScript instead of traversing with NetworkX. These are observed bypasses in our own workflow, not a measured failure rate across all models.

Instructions describe desired behavior; they do not necessarily make it part of execution. The assistant was permitted to complete the human-visible task through a shorter path. Longer prompts and agent instruction files can influence behavior, but they cannot make an optional save operation a deterministic event.

Our engineering hypothesis is that **the more capture resembles an application transaction rather than a model choice, the more reliable it becomes**. Where the host exposes session append, tool result, clear or stop events, attach a programmatic hook at the actual boundary. Persist the original source event independently of model-selected tool calls, then update Knowledge Positions with source coordinates and version hashes. Optional LLM interpretation may enrich relationships later. An MCP read/write interface is useful, but an optional MCP call alone does not compel capture.
