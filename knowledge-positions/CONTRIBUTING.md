# Contributing

This is an experimental framework with a historical reference library, not a finalized universal standard. Start with the [SDF guide](SDF/README.md). Contributions should serve the [mission](MISSION.md) and preserve the [architecture](ARCHITECTURE.md).

1. Start with a concrete question, failure or reproducible experiment.
2. Describe the source, expected outcome, and smallest useful change.
3. Use the target’s native graph operations where possible (NetworkX for the Python reference); do not impose a fixed graph ontology or custom graph-search framework. Parsers are optional adapters.
4. Keep original sources immutable; preserve source/version/span, evidence and relationship qualification. Never present inferred relationships as verified facts.
5. Add a focused test or notebook check; document actual results and limitations in COVERAGE.md. Do not claim that a design document proves an implementation.
6. Credit upstream ideas and code in ATTRIBUTION.md; respect licenses and do not include private material.
7. Submit a pull request with rationale, reproducible commands and test results. Avoid unrelated repository changes.

Pre-standard status: interfaces and terminology may evolve. The existing knowledge documents are design references, not conformance certification.
