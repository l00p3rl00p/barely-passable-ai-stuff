# Native operations

Use the configured database, not a second graph. Existing native client or official MCP query tool. Bind parameters where supported; with query-text-only tools safely encode literals, never concatenate untrusted input.

```cypher
MATCH (k:KnowledgeItem {id:$id}) RETURN k.*;
MATCH (k:KnowledgeItem {source_id:$source}) RETURN k.id,k.heading,k.source_address,k.status;
MATCH (a:KnowledgeItem {id:$id})-[r:Relationship]->(b:KnowledgeItem)
RETURN b.id,b.heading,r.relation,r.qualification,r.evidence,r.status LIMIT 50;
MATCH (a:KnowledgeItem)-[r:Relationship]->(b:KnowledgeItem {id:$id})
RETURN a.id,a.heading,r.relation,r.qualification,r.evidence,r.status LIMIT 50;
MATCH (k:KnowledgeItem)
WHERE k.status='current' AND k.vector_lexical_hash_512_status='known'
RETURN k.id,k.heading,k.source_address,array_cosine_similarity(k.vector_lexical_hash_512,$vq) AS score
ORDER BY score DESC LIMIT 5;
```

Bind nonzero FLOAT[512] in the declared lexical space. Indexed discovery uses QUERY_VECTOR_INDEX on KnowledgeItem/kp_lexical; oversample candidates, filter current and known, return up to five for JITK. See https://docs.ladybugdb.com/extensions/vector/ for the installed-version call. Exact similarity is a separate native operation, not silent substitution for a failed intended index. No text embedding. Read originals and verify hashes. No schema updates during ordinary work.
