# OmniGraph agent startup and delegation (non-normative profile)

This is a host integration recommendation, not a required SDK initialization step.

**The Knowledge Positions skill is the primary knowledge-behavior skill.** It decides whether existing context is sufficient, whether to access a known source, whether to explore associations, and whether fresh discovery or source-backed contribution is needed. It does **not** duplicate the database engine's operational instructions.

**Host startup contract:** Make both this `knowledge-positions-omnigraph` skill and the official `omnigraph` skill available in agent context at session start, with this skill as the primary knowledge workflow. The host/harness is responsible for loading them; the host must explicitly configure skill injection; this documentation does not install or inject either skill. Startup loading is context availability, **not** an instruction to run a scan, open a connection, search, ingest, mutate a graph, or re-read the SDK.

**Delegation:** When the task needs OmniGraph CLI/MCP commands, graph configuration, schema or query authoring, bulk loading, branching, commits, permissions, recovery, or migrations, use the official [OmniGraph skill](https://github.com/ModernRelay/omnigraph/blob/main/skills/omnigraph/SKILL.md). Prefer the version-matched skill exported by the installed OmniGraph CLI when appropriate. The Knowledge Positions agent skill controls *why, when and which knowledge* is needed; the official skill controls *how the database operation works*. Do not invent commands from this skill or override native policy.

