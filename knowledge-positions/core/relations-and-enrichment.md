## 5. Relationship rules and enrichment boundary

A relation record MUST contain **subject ID, predicate, object ID or unresolved target locator, origin, qualification, evidence**, and preserve native direction/order/attributes. A source-supplied parent/child edge, sibling order, declared URI/link, import, dependency or literal “related_to” is an **observed fact of the source**, not AI enrichment. Record and index it immediately. No mandatory ontology normalization or invented “meaning layer.”

A similarity candidate is not a source relationship. Similar titles, shared terms, grammar parse features, cosine scores and co-visitation can provide **leads**. If an implementation stores them as edges, it must label them honestly as lexical/syntactic/similarity observations and never silently promote them to verified causes, prerequisites or semantic relationships.

Deterministic touch-1 enrichment can derive supported structure from preserved observations; already supplied native edges remain available at admission. Intelligence enrichment begins only where ordinary reading/investigation reveals new knowledge not already supplied. See the [touch lifecycle](lifecycle.md). A newly established relation is appended as a separate, source-backed delta with actor, evidence, qualification/status and time/source version where known. It must not rewrite original source facts or rebuild untouched records. Unreviewed candidates remain proposals. The companion Relationships and Evolution specifications define richer qualification/governance when implemented.

**Forbidden:** “Before graph search can work, the LLM must extract all semantic relationships.” The graph already has native relations. Intelligence may later discover more.

