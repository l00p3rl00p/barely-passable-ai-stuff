<!-- knowledge-positions-jitk:start -->
## Appendix — JITK with available knowledge tools

This is a **working-method reference**, not a requirement to install a particular database, call another skill, or read the SDK. Follow the human's task: reuse what is known, retrieve only what is needed, and evolve knowledge from evidence.

**Select any available route.** JITK can use direct files, source positions, AST/Tree-sitter structures, graphs, lexical search, vectors, filters or other tools without Knowledge Positions. **Where Knowledge Positions is implemented, these are methods operating on the same source-backed knowledge identity, not rival knowledge stores or stages.** Starting from a lexical hit, the agent can pivot to its native AST, recorded edges, typed fields, proximity, or original evidence; it can expand, narrow, rank, branch or stop using what is already recorded. Do not build separate identities for each entry method, require a conversion chain, or invent missing values. For other tools, cross-method identity reuse depends on actual shared identifiers or a verified mapping; it is not automatic.

**Return an answer and a way forward.** Address the current question with the best evidence-supported answer or likely answer, labeling uncertainty. Alongside it, return enough known identities, source positions, relationships or other useful leads for the agent to verify or continue if needed. If no defensible answer is available, say so and provide the strongest grounded leads. Do not replace an answer with raw navigation results or invent certainty.

### Known integrations in this environment (examples, not dependencies)

- **OmniGraph and its skill:** When OmniGraph is available, use its exposed graph reads/search, source locators and relationship traversal to find and navigate knowledge. Use the installed **OmniGraph skill or native CLI/MCP help** for actual command names, supported slash commands (if any), permissions and writes. Do not assume a slash command exists merely because a skill exists.
- **Codebase MCP (codebase graph / Codebase Memory):** When the codebase MCP is available, use its exposed code navigation, source positions, AST/structural lookups, dependency and relation traversal, and supported search to find knowledge in the codebase. Inspect its actual tools and arguments; do not invent MCP method names or assume its graph is the same as OmniGraph's.
- **Other tools:** Direct source readers, search services, parsers, or other knowledge stores are equally valid whenever they are actually available and authorized.

**Keep provenance.** Retain the source identity, version and positions; verify evidence before declaring a fact. A candidate match is not proof. For reusable findings, write back through the authorized mechanism only if one exists and the evidence supports it. If a tool is missing, use another available route rather than treating the entire workflow as unavailable.

**More detail, only if needed:** [Knowledge Positions SDK](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/README.md). Normal JITK use needs no SDK lookup.
<!-- knowledge-positions-jitk:end -->
