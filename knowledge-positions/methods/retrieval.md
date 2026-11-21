## 9. Retrieval and investigative loop

An agent may choose any route:
1. Exact location known → read that original span.
2. Name/title known → literal search resolves a record ID.
3. “What connects to this?” → graph traversal of already-recorded edges.
4. Approximate concept → fuzzy/lexical/vector candidates → inspect candidate neighborhood → resolve source.
5. Missing relationship discovered during reading → qualify evidence → add one new relation delta.
6. Reuse the resulting record and relationship on the next investigation.

**No prescribed search sequence.** Graph algorithms may be NetworkX, native Cypher, other graph libraries or plain adjacency operations. Structural search may use Tree-sitter, native AST/DOM paths or a document parser. A fast imperfect lead is enough when the source can be reached and checked.

The experimental principle is: **“The fuzzy match opens the door. The structure does the rest.”** The model formulates a search/traversal; deterministic tools execute; evidence is inspected; novel discoveries are admitted separately.

