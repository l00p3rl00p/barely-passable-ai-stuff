# Unified Knowledge Context (UKC): The Knowledge Positions SDK

**Normative contract:** UKC/1 candidate. **Target:** any execution language. **Authority:** this file, the existing JITK paper, the two companion specifications and the original executable experiments.

The UKC/1 specification is organized into the component documents below. The original sections retain their order and wording; only source-relative link destinations have been adjusted for relocated files. This is a documentation reorganization, not a new SDK implementation.

## Contract sections

- [0. FIRST LAW — the entire mechanism before any implementation detail](contracts/first-law.md)
- [1. Purpose, sources of authority and normative language](docs/authority-and-evidence.md)
- [2. The three positions and fourth-position extension](contracts/positions.md)
- [3. One logical record: the representation contract](contracts/common-record.md)
- [3.2.1 Parser fidelity is mandatory: raw input → native parser output → copied OKF values](readers/native-parser-fidelity.md)
- [3.2.2 Recovered native-to-common translation contract (mandatory; from working code and original research)](readers/native-to-common.md)
- [3.2.3 Recovered graph contract: ten algorithms, two additional operations, ten views](methods/graph-contract.md)
- [3.2.4 Existing location, evolution and recovery: selective behavior, not another ingestion phase](core/known-location-and-recovery.md)
- [3.3 Source → common OKF record → Location / Relation / Proximity: executable examples](examples/source-mappings.md)
- [3.4 Same stored values, different algorithms — implementation crosswalk](methods/algorithm-crosswalk.md)
- [3.5 Executed characterization — seven real inputs and one shared record per source](conformance/characterization.md)
- [3.6 On-touch enrichment and cold reconstruction — essential operational example](core/on-touch-recovery.md)
- [4. Identity, exact source positions and deterministic equality](core/identity.md)
- [5. Relationship rules and enrichment boundary](core/relations-and-enrichment.md)
- [6. Deterministic source acquisition and adapters](readers/source-adapters.md)
- [7. Proximity: useful even when imperfect; never blocking](methods/proximity.md)
- [8. Public SDK operations — required semantics, arbitrary language syntax](contracts/public-operations.md)
- [9. Retrieval and investigative loop](methods/retrieval.md)
- [10. Mandatory conformance suite: no claims without execution](conformance/requirements.md)
- [11. Lifecycles, updates, concurrency, storage and performance](core/lifecycle.md)
- [12. Implementer's exact procedure](docs/implementer-guide.md)
- [13. Future fourth position: Resonance](docs/resonance.md)

## Existing agent-skill guidance, organized by SDK component

The following documents preserve guidance copied from the existing [Knowledge Positions OmniGraph skill](research/omnigraph/skills/knowledge-positions-omnigraph/SKILL.md). They describe agent/host use of the SDK and are not additional UKC/1 conformance requirements. The original skill remains unchanged.

- [Skill overview and knowledge vocabulary](docs/agent-knowledge-overview.md)
- [Agent startup and official OmniGraph delegation](adapters/omnigraph/agent-startup.md)
- [SDK reference and graph-ingestion recommendation](docs/sdk-reference-usage.md)
- [Position, tree/AST, graph and vector capability selection](methods/agent-capabilities.md)
- [Knowledge access gates and agent coordination](methods/agent-knowledge-access.md)
- [JITK host contract](adapters/omnigraph/jitk-host-contract.md)
- [Local discovery priority](methods/local-discovery-priority.md)
- [Contribution and progressive disclosure](core/agent-contribution.md)

## Language locations

- [Rust](languages/rust/README.md)
- [TypeScript](languages/typescript/README.md)
- [Python](languages/python/README.md)

## Other component locations

- [Adapters](adapters/README.md)
- [Tools](tools/README.md)

Existing implementation, skills, tests, experiments, and research remain in their original locations.
