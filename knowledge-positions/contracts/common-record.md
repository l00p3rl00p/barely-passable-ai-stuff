## 3. One logical record: the representation contract

**Lightweight by design.** The active knowledge record stores the identity, source/version locator, existing positional values and native relationships—not a duplicate of the source body or an exhaustive set of inferred connections. Deterministic capture is cheap; **on-touch enrichment** is selective. Untouched items remain lightweight. When an investigation reveals a useful, evidence-backed relation or attribute, it is added to the same identity. Existing native edges remain available; unrelated items are not enriched merely because one item was touched.

Every successfully admitted knowledge item has **one common logical knowledge record** under a stable identity. Record the available source-native navigational values once with a resolvable pointer to the authoritative original. The common record is an addressable map of knowledge, **not a requirement to duplicate the source body or precompute every future relationship**. Any separately retained source copy is optional for normal JITK access and has its own retention policy. The fields provide the data on which structural, relational, lexical and vector methods operate; the SDK MUST NOT require three separately filled position objects. If a value needed by a particular method is unavailable, that method reports the missing value rather than blocking admission, constructing an alternate representation or launching a conversion chain. A single source can contain many items. The natural grain is source-adapter-defined: file, symbol, AST/DOM node, document section, message, event, paragraph, observed relation or qualified finding.

**Complete capture reference.** The following table and capture rules are the authoritative checklist for a writer. Detailed identity, vocabulary and reader documents explain their respective mechanisms; they do not create additional hidden capture obligations.

**Minimum UKC/1 logical fields** (not a mandated programming-language struct or physical DB schema):

| Field | Logical form and capture requirement | Origin / check |
|---|---|---|
| **schema** | Required string: `ukc/1` | Framework constant. |
| **id** | Required canonical string, shared by all methods | [UKC-ID-1](../core/identity.md): compact UTF-8 JSON of the ordered six strings (schema, authority, source key, observed source version, native kind, native unit key), SHA-256, existing `ukc:v1:` prefix. Preserve recoverable native unit key and producer normalization version; retain legacy_id aliases for historical records and logical-unit aliases/supersession links when available. Compare exact bytes and digest. |
| **source** | Required mapping: authority/owner, source key, observed version/digest; preserve available route, realm and access requirements | Source resolver; verify source version and current authorization separately from identity. |
| **kind** | Required honest native item kind | Parser or source adapter; never impose a universal AST. |
| **location** | Known source and internal structural coordinates, basis, version, verification and units; unknown/not applicable otherwise. Preserve verified alternate coordinates, paths, parent paths, depth and sibling order when supplied. | Native parser/resolver. Exact UTF-8 byte spans are zero-based/end-exclusive; other systems declare units. Unresolved locator is a lead, not exact evidence. |
| **relations** | Zero or more observed or qualified relations with subject, predicate, target ID or unresolved locator, origin, qualification, evidence, native direction/order/attributes. Known empty differs from unknown. | Native source or qualified delta; [vocabulary](../CORE_VOCABULARY.md) and [relation rules](../core/relations-and-enrichment.md). |
| **proximity** | Available lexical/fuzzy inputs; zero or more vectors tagged with compatible space and explicit status. For a declared vector profile, retain space ID, dimensions, encoder algorithm/version, tokenization/Unicode/preprocessing, stop words, sign convention, input policy, normalization, numeric representation and source-content digest where applicable. Unknown values never invented. | Native values or declared encoder; no compulsory encoder or LLM. |
| **values** | Mapping of supplied names, titles, literal typed fields, attributes, flags, and order; preserve casing and precision. | Parser/source metadata; compare values and provenance. |
| **native** | Faithful native structural metadata and source/version reference; preserve all supplied fields, diagnostics, ordering and payload (or verified lossless reference). | Actual parser output; verify unindexed fields too, report limited direct query support. |
| **evidence** | Source version, available original byte/span digests, parser identity/version, coordinates, accepted finding/event provenance. | Reader with actual bytes computes digests at admission or deterministic enrichment; declare stage; never fabricate. |
| **lifecycle** | Admission 0; deterministic and intelligence enrichment per [lifecycle](../core/lifecycle.md). | Verify repeated admission, transition and budget. Logical requirement, not an added mandatory physical column. |
| **OKF interchange** | On export/import, nonempty type and pinned upstream representation; optional metadata obeys upstream rules when present. | See §3.2; validate round trip. Native storage may use its own types. |

Reader-specific crosswalks belong in [reader mappings](../readers/native-to-common.md). Preserve already supplied native edges and values at touch 0. The [grouping requirement](../core/lifecycle.md#block-grouping) governs deterministic touch-1 enrichment; it does not change canonical identity inputs.

Use **one shared logical record**, even if runtime performance calls for multiple physical indexes. A graph table row and a vector-index entry referencing the same ID are not independent bodies of knowledge. They are materializations over the record. A consumer can read all **recorded** positions without another AI inference or a second import, and can resolve the original source on demand when authorized. Native edges and factual structure can be present immediately; unknown semantic relationships remain unknown until evidenced enrichment is admitted.

### 3.1 What “complete” means

**Entry-point invariance (mandatory):** Given identical source-backed observations, whether an adapter first encounters a node through a title, an AST node, a relationship, or a vector result, it MUST resolve the same canonical knowledge identity and expose the same known common-record values. No entry route may generate a distinct knowledge record or require rebuilding fields through its own retrieval engine. The source-native name, relation, path and numeric value remain individually labeled, with original precision and provenance preserved. **Record once; label deterministically; read through any applicable method.**

Record the **available positional, native structural and identifying values** faithfully at the input boundary; do not require exhaustive extraction of all content or speculative relationships. Never add a title, causal edge, actor, location or meaning not supplied. Missing fields stay unknown. Preserve native path, child order, UTF-8 offsets, explicit attributes and any source-specific field actually admitted, even if no current search method needs them. The **original source remains authoritative outside the index**; a source reference and version/digest suffice for normal source-resolvable JITK use. An implementation **may** retain a full payload in a content-addressed sidecar for offline operation or lossless interchange. If it advertises a **self-contained, lossless export**, that package must actually contain or resolve all claimed source/native bytes; a dangling external pointer does not meet that stronger guarantee. Do not mistake this export requirement for a rule to copy every source into every active knowledge record.

The SDK does not impose a universal AST schema. A deterministic adapter describes source-native structure; UKC records it.

### 3.2 OKF-compatible interchange

Pinned upstream: [OKF v0.3 SPEC.md at 527e81aff55992be21507e97004286789126f88c](https://github.com/open-knowledge-format/open-knowledge-format/blob/527e81aff55992be21507e97004286789126f88c/SPEC.md). The framework requires this representation at interchange, not a particular physical storage schema. A concept export has nonempty type, YAML mapping without duplicate keys, and the producer extension; optional sources, generated, verified, status and stale_after follow upstream definitions. Bundle roots, path resolution and index metadata follow the pinned upstream spec. Do not invent an unavailable resource path or verification event. On interchange, map internal current to stable, deprecated to deprecated and source-changed to stable plus stale_after at the detection instant; the latter does not make the original evidence current. Retain draft where warranted by actual status. Internal lifecycle and access checks remain authoritative.

UKC records MUST have a **valid OKF-compatible representation** on export and import. Use upstream-recognized OKF fields correctly, plus a producer-defined **x-ukc** extension for identity, positions, original native values, evidence and optional sidecar references. The original source body and its exact bytes must remain recoverable **from the authoritative source or a specifically retained copy** when exact reconstruction is claimed; ordinary knowledge records may carry verified references rather than inline bodies. Unknown YAML keys, native fields and unrelated OKF content must round-trip without being silently discarded.

**OKF is the common translation vocabulary and portable packaging, not a semantic extraction service.** Translating observed parser values to an equivalent OKF field/extension is a copy or deterministic mapping; it does not make an LLM think about their meaning. If a destination representation cannot express a native source value, preserve it losslessly in a native extension or sidecar and report limited direct query support. Do not manufacture equivalent meaning.

An illustrative asset (not a normative upstream OKF schema, and digest placeholders are intentionally not executable fixtures):

~~~yaml
---
type: SourceUnit
title: Example
x-ukc:
  schema: ukc/1
  id: "ukc:v1:<computed-digest>"
  source:
    authority: repo:example
    key: docs/example.md
    version: "sha256:<source-bytes-digest>"
  kind: heading
  values: {title: Example}
  location:
    status: known
    basis: parser
    path: ["document", "heading[0]"]
    spans: [{unit: utf8-byte, start: 0, end: 10}]
  relations: []
  proximity: [{space: "lexical-hash-512/rust-scanner-v1", status: unknown, vector: null}]
  native: {storage: inline}
  evidence: {source_sha256: "<source-bytes-digest>"}
---
# Example
~~~

A “knowledge graph” with an OKF note containing only a generated summary but not the original supplied structure does not meet this contract.

