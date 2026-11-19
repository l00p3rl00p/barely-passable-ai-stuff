// Native Knowledge Positions projection; writer enforces canonical invariants.
CREATE NODE TABLE IF NOT EXISTS KnowledgeItem (
 id STRING PRIMARY KEY, kind STRING, entity_type STRING, domain STRING,
 heading STRING, terms STRING, owner_namespace STRING,
 source_id STRING, source_address STRING, source_repo STRING, source_commit STRING,
 source_path STRING, source_version_sha256 STRING, observed_source_version STRING,
 source_precision STRING, position_unit STRING,
 start_byte INT64, end_byte INT64, start_line INT64, end_line INT64,
 position_coordinates STRING, span_sha256 STRING, ownership STRING,
 realm STRING, possible_routes STRING, within_path STRING[], sibling_index INT32,
 location_coordinates STRING, location_method STRING, location_basis STRING,
 location_precision STRING, vector_lexical_hash_512_status STRING,
 vector_lexical_hash_512 FLOAT[512], status STRING, status_history STRING[],
 enrichment STRING, enrichment_touches INT32, enrichment_touch_limit INT32,
 enrichment_frozen BOOL
);
CREATE NODE TABLE IF NOT EXISTS EnrichmentCluster (
 id STRING PRIMARY KEY, touches INT32, touch_limit INT32, frozen BOOL, source_versions STRING
);
CREATE NODE TABLE IF NOT EXISTS LocationMethod (
 name STRING PRIMARY KEY, source_kind STRING, description STRING, verification STRING, status STRING
);
CREATE REL TABLE IF NOT EXISTS Relationship (
 FROM KnowledgeItem TO KnowledgeItem, relation STRING, evidence_key STRING,
 evidence STRING, qualification STRING, status STRING, origin STRING,
 confidence DOUBLE, cost DOUBLE, weight DOUBLE
);
CREATE REL TABLE IF NOT EXISTS InEnrichmentCluster (
 FROM KnowledgeItem TO EnrichmentCluster, MANY_ONE
);
