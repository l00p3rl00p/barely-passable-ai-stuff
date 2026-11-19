// Run once after admitting compatible nonzero vectors.
INSTALL VECTOR;
LOAD VECTOR;
CALL CREATE_VECTOR_INDEX('KnowledgeItem', 'kp_lexical', 'vector_lexical_hash_512', metric := 'cosine');
