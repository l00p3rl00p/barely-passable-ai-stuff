# UKC SDK component and capability map

**Purpose:** Package and expose existing capabilities under the [UKC/1 contract](../unified-knowledge-context.md). This is a **source inventory and integration map**, not a runtime, a new knowledge implementation, or a certification claim. No component changes authority merely by appearing here.

## Public contract and implementations

The [public operations](../contracts/public-operations.md) define the language-neutral behavior. Existing code has its **own** functions and identity rules; similarly named functions are **not automatically UKC/1-compliant**. The [UKC-ID-1 identity profile](../core/identity.md), [native-record mapping](../readers/native-to-common.md), and [conformance suite](../conformance/requirements.md) remain the test of compatibility.

| Component | Actual existing entry point | Exposed responsibility | Integration status |
|---|---|---|---|
| Python library | [`knowledge_positions.py`](../knowledge_positions.py), [`pyproject.toml`](../pyproject.toml) | `KnowledgePositions.add`, `link`, `neighbors`, `search`, `record_item_position`, `fill_vector`, `graph_view`, `core_algorithms`, `save`, `load`; source-backed graph and positions | Existing installable experimental Python package; **not a certified UKC/1 implementation** |
| Python graph/vector tools | [`core_operations.py`](../core_operations.py) | Existing NetworkX algorithms and vector analysis over existing graph data | Existing tool, not a new SDK service |
| Python capture workflow | [`capture.py`](../capture.py) | Reviewed-record capture, lexical-hash encoding, verification and CLI operations | Application workflow; not a required SDK transport |
| Historical Python OmniGraph adapter | [`research/omnigraph/adapter.py`](../research/omnigraph/adapter.py) | Map existing Knowledge Positions operations to native OmniGraph persistence and queries | Existing adapter; engine behavior remains the official OmniGraph skill's responsibility |
| Historical OmniGraph schema and queries | [`schema.pg`](../research/omnigraph/schema.pg), [`queries/kp.gq`](../research/omnigraph/queries/kp.gq) | Graph types, retrieval and mutations | Existing engine-specific artifacts, **not the common UKC schema** |
| Historical OmniGraph query encoder | [`encoder.py`](../research/omnigraph/encoder.py) | Scanner-compatible lexical vector calculation | Existing declared space; do not conflate with the different historical `capture.py` lexical-hash profile |
| Rust universal scanner and target kit | [Current inspected Rust sources](../languages/rust/README.md) | Native extraction, emitter, touch-0 writer, legacy re-key enricher | Separate development workspace; see source links and known gaps. Not UKC/1 certified. |
| TypeScript | [TypeScript language location](../languages/typescript/README.md) | Future language-idiomatic consumer of the same contract | No existing TypeScript SDK binding verified; do not advertise one |

## UKC/1 operation exposure versus existing Python code

| Contract operation | Existing related capability | Gap or caution |
|---|---|---|
| `capabilities()` | Existing methods and [location catalog](../knowledge_positions.py) | No demonstrated UKC/1 capability-descriptor endpoint |
| `admit(source, observations)` | `KnowledgePositions.add`, `ingest_python`; Rust scanning/admission separately | Python's historic hash differs from UKC-ID-1; no universal native-payload/OKF mapping demonstrated |
| `get(id)` | `KnowledgePositions.graph.nodes[id]`, adapter item query | Native graph node is not yet shown to contain the complete UKC common record |
| `resolve(id, principal)` | Original source-version/span checks in [GPS proof](../examples/gps/gps.py), capture verification | No common principal-aware, source-authorized UKC resolver verified |
| `neighbors(id, filters)` | `KnowledgePositions.neighbors`, graph queries | Filter/provenance parity requires conformance |
| `search(query, method, options)` | `KnowledgePositions.search`, graph views, OmniGraph search query | Different exposed methods are not yet one proven portable search interface |
| `put_vector(id, descriptor, values)` | `fill_vector` with existing encoder/model | No demonstrated general named-vector-profile UKC contract |
| `upsert_relation(edge, evidence)` | `KnowledgePositions.link` and adapter link | Evidence qualification, idempotence and identity parity need verification |
| `export_okf(ids)`, `import_okf(assets)` | Historic OpenKC proof (separate project) | Not implemented as a verified full UKC/1 round-trip interface here |
| `verify(ids)` | Capture verify and existing source checks | Not a complete common-record and cross-method conformance verifier |
| `rebuild(sources, accepted_findings)` | Existing scans, persisted sources, graph save/load | No verified UKC/1 recovery of all accepted qualified findings |

## Dependency direction

`UKC/1 contract → existing language/library functions and adapters → existing host/engine tools`.

This describes contract ownership, **not a required execution pipeline**. Consumers choose any supported structural/position, graph/relation or lexical/vector/proximity method independently or in combination, using the same logical knowledge identity wherever compatibility has actually been established.

Do not relocate, wrap, reimplement, or claim certification for existing implementations merely to complete this catalog. Package availability, behavior and cross-language identity equivalence must be demonstrated, not inferred from matching labels.
