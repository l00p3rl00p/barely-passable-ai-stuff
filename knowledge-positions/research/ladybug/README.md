# Knowledge Positions — LadybugDB

**Knowledge = { Position. Relation. Proximity. Resonance. }**

Native declarative storage projection of the [research](../paper.md). Independent of OmniGraph. No application code, custom service, MCP implementation, embedding provider, or ingester is included. LadybugDB owns persistence, Cypher, transactions and indexing. The [canonical Knowledge Positions library](../../knowledge_positions.py) and research govern admission and lifecycle; writers must conform. Resonance remains research.

- schema.cypher — native tables.
- vector-index.cypher — native index for the scanner-compatible lexical-hash-512 space.
- RUNBOOK.md — load and connect.
- ACCESS.md — native access and concurrency.
- skills/knowledge-positions-ladybug/ — portable skill and native operation references.

Every reader feeds the same Knowledge Positions representation. Adding a reader does not change the architecture. Detect → select parser → extract → establish knowledge → persist. Parsing is not understanding. Original evidence remains authoritative. No synthetic semantic embedding.

Fresh schema for the current contract, not migration of an older database. DDL and commands follow official documentation; live execution not verified.
