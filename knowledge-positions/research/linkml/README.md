# Knowledge Positions — LinkML implementation

The architecture is defined by [the paper](../paper.md), [Core](../../CORE_VOCABULARY.md), [location/access](../../LOCATION_ACCESS.md) and [evolution profile](../../Knowledge-Asset-Evolution-Spec-v1.6.3.md). The [LinkML schema](knowledge-positions.linkml.yaml) is a machine-readable implementation, not a competing architecture. OKF remains the portable representation; producer-defined extensions are not normative OKF fields.

All 58 declared fields from [the native OmniGraph projection](../omnigraph/schema.pg) are retained, including enums, scalar and multivalue ranges, the lexical vector's 512-value cardinality, edge endpoints, edge identity and descriptions. A graph container provides a portable collection. The [Ladybug projection](../ladybug/schema.cypher) remains native. No database migration or mandatory indexing is introduced.

Core describes identity, location, graph position and compatible proximity. Unknown data is not fabricated. Optional attributes remain knowledge even when not indexed or populated. Enrichment, lifecycle and qualified edges have their defined places in the same schema; source parsing does not invent them. Resonance remains the existing research proposal, not a claimed implemented algorithm or invented mandatory field.

Read/parse/collect uses a LinkML parsing schema; the caller receives data. An independent connector receives, maps and emits through receivers' native interfaces. One LinkML format describes collection and destination data. The schema does not grant access or execute hashing, source verification, lifecycle transitions or database referential integrity. Use established application and database mechanisms.

Validation: run official `gen-json-schema knowledge-positions.linkml.yaml` and `linkml-lint knowledge-positions.linkml.yaml`, then validate actual file-derived records and native receivers. The source field translation was structurally checked; official runtime validation remains pending.
