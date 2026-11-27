## 12. Implementer's cookbook

Use the [SDF guide](../unified-knowledge-context.md) for navigation. The [First Law](../contracts/first-law.md), [complete capture reference](../contracts/common-record.md), [lifecycle](../core/lifecycle.md), [operations](../contracts/public-operations.md) and [conformance suite](../conformance/requirements.md) define correctness. This cookbook is assembly guidance, not a second specification.

### 12.1 Select the implementation path

The universal scanner is reusable across targets. For a new destination, assess its native capabilities before developing a target-specific emitter, KP writer, KP enricher and, where applicable, MCP integration. Standalone KP implementations need not implement native ingestion. Do not rebuild native operations or introduce wrappers solely to satisfy an implementation naming convention.

Record a coverage matrix for the target: requirement ID, actual native capability (with evidence), gap/custom work if needed, verification command, expected and observed result. A native capability satisfies a requirement only when verified; unsupported capabilities are reported honestly. See existing [adapters](../adapters/README.md), [language implementations](../languages/) and [source examples](../examples/source-mappings.md) for useful native approaches, not mandated dependencies.

### 12.2 SIPOC component assembly

| Component | Supplier | Input | Process | Output | Customer |
|---|---|---|---|---|---|
| Universal scanner | Original source | Source bytes/metadata | Native parse | Complete supplied parser observations | Emitter |
| Target emitter | Scanner | Native observations | Lossless native serialization/write | Native stored information and native acknowledgement | Destination |
| Target KP writer | Destination | Stored native information | Deterministic UKC admission | Touch-0 logical records | Enricher and retrieval consumers |
| Target KP enricher | Destination and evidence | KP records, preserved observations | Deterministic touch 1; selective later intelligence touches when appropriate | Evidence-backed updates and relationships | Knowledge consumers |
| Optional target MCP | Consumer and native target | Request plus authorized capabilities | Invoke supported native operations | Honest native results/errors | Agents and applications |

Native ingestion ends upon native acknowledgement. The writer and enricher operate independently after storage; MCP is an access mechanism, not another ingestion stage.

### Recipe A — Universal scanner
1. Choose an established native parser appropriate to the input and record its version and coordinate basis.
2. Preserve all actual outputs, including arbitrary fields, diagnostics, ordering and partial outputs. Avoid target-specific mappings or dependencies.
3. Expose native observations to emitters using the existing boundary.

**Check your work:** compare a real parser invocation with scanner output field-by-field; include malformed input, Unicode and large input. Assert no missing native values and no target dependency. See UKC-19 and the [native ingestion contract](../contracts/native-ingestion.md).

### Recipe B — Target emitter
1. Inspect actual native destination write/batch facilities, constraints and supported types.
2. Serialize every supplied property without filtering; retain unrepresentable native fields losslessly rather than substituting inferred values.
3. Use native writes and acknowledge only native success. Follow native retry semantics; report unresolved failure.

**Check your work:** outside the runtime path, compare actual scanner input with stored native output, including types, diagnostic fields, ordering and oversized payloads. Measure wall time, bytes and failed writes. No extra acknowledgement or read-back stage is introduced in production. See [native ingestion](../contracts/native-ingestion.md) and applicable UKC-19 fidelity checks.

### Recipe C — Target KP writer
1. Inspect native stored observations and declare the reader crosswalk.
2. Follow the [capture reference](../contracts/common-record.md) and [identity algorithm](../core/identity.md). Write a touch-0 representative record using native target operations; use native upsert/constraints if sufficient.
3. Preserve known observed relationships and honest missing values. Inspect native service limits, use deterministic pagination/field retrieval or lossless native payload references and transactions/batches as applicable. Reconcile every input and output; a limit is not a filter. Do not claim a skipped or partial write is complete.

**Check your work:** compare canonical ID bytes against the same fixture, reconcile admitted native input with logical records, compare all fields, rerun with zero duplicate records, and exercise known and unknown positions. Test actual input with oversized records. Expected: no required LLM calls, no lost input, stable identity; applicable UKC-01, 04, 05, 06, 14, 19, 20.

### Recipe D — Target KP enricher
1. Read existing touch-0 records and native observations. Use native grouping/traversal capabilities where sufficient.
2. Fulfill the [block grouping requirement](../core/lifecycle.md#block-grouping): assess native groupings, reuse sufficient grouping, improve or extend it deterministically when justified. Preserve supplied native edges and unmatched events; keep identities and original evidence intact.
3. When relevant work discovers qualified knowledge, apply touch 2 and 3 through the approved lifecycle. Reuse existing native search/traversal; do not force corpus-wide LLM passes.
4. For changed sources, preserve accepted discoveries and reconstruct affected records from source/version evidence.

**Check your work:** compare grouping and edges with actual parser observations (including already-grouped native trees and incomplete event pairs), verify evidence and unchanged original IDs, repeat without duplicating deltas, test freeze after touch 3 and source-version recovery. Applicable UKC-02, 07, 10, 11 and 16. A cluster's budget follows its actual creation stage.

### Recipe E — Retrieval and optional MCP
1. Map supported native exact, structural, graph, lexical and compatible vector capabilities to the [public operations](../contracts/public-operations.md).
2. Reuse existing native endpoints or MCP tools if sufficient. Expose actual capabilities and permissions, not speculative wrappers.
3. Return shared canonical IDs, evidence pointers and typed failures; resolve original evidence under current authorization.
4. Use native graph algorithms where available; the [graph contract](../methods/graph-contract.md) lists all twelve required operations and appropriate views. Exercise those operations using the same IDs and real edges; no mandatory NetworkX dependency. Declare and test a compatible deterministic vector profile for core certification (UKC-08); vector generation is not an admission prerequisite.

**Check your work:** retrieve one item by each supported route and compare ID/values; traverse observed edges, reject incompatible vector spaces and changed or inaccessible source reads. Check unsupported methods report failure. Applicable UKC-01, 02, 06, 08, 09, 10, 13, 14 and 20.

### Recipe F — Interchange, reconstruction and final verification
1. Map records to the pinned OKF representation using the capture reference; retain optional unknown extensions and actual native evidence.
2. Import without inference; preserve identities and known values.
3. Reconstruct disposable projections from original sources and accepted discoveries without repeating prior reasoning.
4. Execute the [conformance requirements](../conformance/requirements.md) against shared actual fixtures; publish commands, versions, inputs, expected/observed outputs and failures.

**Check your work:** compare round-trip original bytes, record IDs, fields and relationships; run reconstruction twice from the same evidence; verify advertised capabilities and parity only where actually tested. Applicable UKC-03, 10, 11, 12, 15, 17, 18, 19 and 20 as specified in the existing certification rules. Smoke tests alone do not establish certification.

**Completion:** Each recipe records pass, fail, blocked or justified not-applicable with inspectable evidence. No independent implementer should need to reverse engineer a reference kit or search historical research to discover missing mandatory requirements.
