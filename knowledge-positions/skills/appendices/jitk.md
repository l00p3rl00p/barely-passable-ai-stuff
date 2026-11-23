<!-- knowledge-positions-jitk:start -->
## Optional integration: Just-in-time knowledge (Knowledge Positions)

This section governs **how an agent retrieves and reuses knowledge**. It does not select a storage engine, install a service, alter a schema or override this skill's native instructions.

**Knowledge Positions:** one source-backed knowledge identity; Location (where the original evidence is), Relation (observed or evidence-qualified links), and Proximity (literal, lexical, fuzzy, or compatible-vector candidates). Resonance is a future extension, not a required lookup step.

### Use this decision sequence, stopping at the first sufficient answer

1. **Reuse:** Is enough verified, relevant knowledge already in the current context or an existing host-provided JIT packet? If yes, use it. Do not repeat discovery just because a new tool or session begins.
2. **Direct access:** Is the source locator, item identity, or exact section already known? Use an authorized direct read, AST/tree position, or source resolver; confirm the source version when citing exact evidence.
3. **Explore:** Is a relevant identity already known and are observed or qualified relationships available? Navigate only the necessary parent/child, neighbor, dependency, or other supported links.
4. **Discover:** If no known position or immediate association suffices, use an actually available exact, lexical/fuzzy, structural, graph or compatible-vector search. Treat ranked hits as candidates; inspect the source before asserting a fact.

### Choose a real method, not a promised one

Inspect the **capabilities actually exposed** by this skill's implementation or the host: its callable tools, native readers, search functions, graph traversal, and source-resolution operations. Position is suitable when a location or native structure is known; Relation when recorded edges exist; Proximity when the name or subject is uncertain. Any method or combination may be selected in any order. A tool's availability does not imply permission to use it. If none is available, report the gap; do not fabricate a retrieval, index, relationship, or result.

**Execution boundary:** This skill's own documented APIs, commands, credentials, authorization rules, and failure handling remain authoritative. For another implementation, use *its* installed API documentation or skill. The [Knowledge Positions UKC SDK](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/README.md) is an optional, language-neutral reference for identity, data mapping, schema design and interoperability; ordinary retrieval must not require reading or ingesting the whole SDK. If source-backed SDK guidance is already indexed, retrieve only the relevant passage.

**Evidence and bounds:** Prefer the smallest useful packet (normally up to five identities and three relationship hops, unless the user or host sets another scope). Return identity, source/version, exact location where available, relation provenance, and compatible-space labels. Similarity is a lead, not an asserted edge. Do not confuse a locator with read authorization. Preserve unknowns and report source-changed or access-denied outcomes.

**Contribution:** After a meaningful new, reusable and evidenced finding, use the selected implementation's *authorized* admission/update operation, if available. Retain the original source and reviewed finding durably; never silently rewrite source facts, make speculative graph edges, initiate a global rescan, or retry an uncertain write without reconciling it first.

**Optional host prefetch:** If a host already supplies JIT knowledge before the agent starts, keep the human prompt unchanged and supply the knowledge packet separately. A bypassed or empty packet is not proof that knowledge is absent. This appendix does not install a prompt hook or imply one ran.
<!-- knowledge-positions-jitk:end -->
