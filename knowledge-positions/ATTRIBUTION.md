# Attribution

This document credits intellectual contributions that shaped the design. Technical dependencies and components are documented in [Environment](ENVIRONMENT.md), not listed here as contributions.

## Google — Open Knowledge Format (OKF)

[Official specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) · [Google's introduction](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

**Contribution:** The portable knowledge-asset format that underpins the project's design lineage: Markdown, frontmatter and portable knowledge structure. The project's knowledge lifecycle and three-position navigation build on this foundation. OKF is a format, not a graph engine. The current library uses JSON persistence and does not yet implement OKF interchange.

## Garyu-tt — Noosphere Lite MCP

[Upstream project](https://github.com/Garyu-tt/noosphere-lite-mcp) · [Git drift documentation](https://github.com/Garyu-tt/noosphere-lite-mcp/blob/main/docs/GIT_DRIFT_R03.md)

**Contribution:** Explicit cascading staleness/invalidation through knowledge dependencies. When a source changes, dependent knowledge can be marked for review while preserving history. This supplied the concrete mechanism missing from the initial Knowledge Positions design. No upstream code was copied; explicit dependency-based staleness and deprecation are implemented in Knowledge Positions. Upstream's current code is GPL-3.0-or-later.

## Python standard library AST — source-location traversal precedent

[Python AST documentation](https://docs.python.org/3/library/ast.html) describes the existing `ast.iter_fields`, `ast.get_source_segment`, line/column coordinates and hierarchical syntax nodes. Knowledge Positions originally used this traversal to establish Python source spans and containment. The new `item_location` metadata reuses its **method for ordering and positioning children within an item**, not the Python AST schema or parser as a universal knowledge format. The generic metadata API works with other deterministic parsers or explicitly qualified source observations. This is a standard-library facility, not third-party code copied into the project.

## Existing design lineage

The original [Knowledge Asset Evolution v1.6.3](Knowledge-Asset-Evolution-Spec-v1.6.3.md) and [Knowledge Graph Relationships](Knowledge_Graph_Relationships_and_Enrichment.md) retain their own sources and attribution. The independent GPS experiment critique is recorded in [Coverage](COVERAGE.md) as experimental feedback, not an upstream software dependency.
