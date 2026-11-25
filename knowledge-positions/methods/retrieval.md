## 9. Retrieval and investigative loop

Retrieval is not an LLM-only operation. A human, script or application may invoke a supported lookup, traversal, ranking or count directly and receive structured results without any model inference. See [LLM-independent retrieval in the JITK architecture guide](../docs/jitk-architecture-and-ingestion.md#example-answering-without-an-llm).

**Answer first; preserve the path forward.** A successful JITK response MUST address the original query with an answer or the best evidence-supported likely answer, explicitly qualifying uncertainty. It also returns enough relevant identity, source location, known relationships or other navigational positions to verify, expand, narrow, rank or continue the investigation. Do not return positions alone when the available evidence supports an answer, and do not load whole sources merely to supply navigational context. If the evidence cannot support even a provisional answer, state that limitation and return the strongest grounded leads rather than inventing one.

An agent may choose any route:
1. Exact location known → read that original span.
2. Name/title known → literal search resolves a record ID.
3. “What connects to this?” → graph traversal of already-recorded edges.
4. Approximate concept → fuzzy/lexical/vector candidates → inspect candidate neighborhood → resolve source.
5. Missing relationship discovered during reading → qualify evidence → add one new relation delta.
6. Reuse the resulting record and relationship on the next investigation.

**No prescribed search sequence—and no single method owns the investigation.** Under a Knowledge Positions implementation, each connected search, source reader, tree/AST navigator, graph traversal, filter or similarity algorithm addresses the **same knowledge identity** through the available values in its shared record. A method can return a matching identity, count, score, verified span or related set; the investigator may stop there or pivot immediately to another applicable method without creating a second interpretation of that item. A search result does not need to be expanded into full source text until the question requires it. Graph algorithms may be NetworkX, native Cypher, other graph libraries or plain adjacency operations. Structural search may use Tree-sitter, native AST/DOM paths or a document parser. A fast imperfect lead is enough when the source can be reached and checked.

**Example:** “How many turkey recipes are recorded?” may be answered by a scoped count of matched identities; no thousand-document read is required. “Which ten are most relevant?” can then filter or rank those identities using known fields and supported methods. “How are they related?” can pivot to existing edges; “show me the steps” can resolve source spans. Every step reuses the same records and evidence. Scores and inferred relationships must not silently become source facts; missing values remain unknown. Without a Knowledge Positions implementation, ordinary JITK can still use available retrieval tools, but cross-method identity continuity is not automatic.

The illustrative principle is: **“A fuzzy match may open a door; the investigator can then use any available recorded position.”** The agent formulates searches and traversals; ordinary tools execute; evidence is inspected when needed; novel verified discoveries are admitted separately.

