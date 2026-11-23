## 8. Public SDK operations — required semantics, arbitrary language syntax

An SDK MAY use idiomatic names, but must supply a conformance adapter offering these logical operations:

| Operation | Observable contract |
|---|---|
| **capabilities()** | Report actual supported adapters, methods, vector profiles, source resolvers, storage, export/import and unsupported features. |
| **admit(source, observations)** | Deterministic idempotent admission: one common record containing all observed native values and relationships alongside source information; no method-to-method conversion and **zero compulsory LLM calls**. |
| **get(id)** | Return the same complete logical record across any search route; explicit unknown positions. |
| **resolve(id, principal)** | Return exact original source span after source-version/integrity and current permission checks, otherwise typed failure. |
| **neighbors(id, filters)** | Return observed and qualified edges with original type, direction/order, evidence and canonical neighbor IDs. |
| **search(query, method, options)** | Support exact literal/structural, graph, lexical/fuzzy or vector access as advertised; results carry canonical IDs, method and source pointers. No mandatory semantic pipeline. |
| **put_vector(id, descriptor, values)** | Store a named vector position without changing the record identity or original edges. |
| **upsert_relation(edge, evidence)** | Idempotently add an observed edge or an admitted, qualified newly discovered edge; preserve provenance. |
| **export_okf(ids)** | Portable OKF assets with complete x_ukc records and included/verifiable native payloads. |
| **import_okf(assets)** | Recreate same identities, fields, positions, relations, vector descriptors and source-backed payloads with no inference. |
| **verify(ids)** | Check integrity, source and edge references, vector-space coherency, version consistency and round-trip preservation. |
| **rebuild(sources, accepted_findings)** | Restore disposable indexes from original source and accepted evidence without rerunning an LLM to rediscover prior results. |

Typed failures include **unsupported_adapter, unsupported_method, source_inaccessible, source_changed, unresolved_location, incomplete_native_payload, invalid_identity, vector_space_mismatch, unqualified_relation, corrupt_record, duplicate_conflict, version_conflict**. Never turn a failed read into a fabricated successful result.

The operations define **what** must happen, not **which package** implements it. An HTTP server, MCP plugin, CLI, UI, graph database, Python process or Rust binary is a deployment choice.

