# Unified Knowledge Context (UKC): The Knowledge Positions SDK

**Normative contract:** UKC/1 candidate. **Target:** any execution language. **Authority:** this file, the existing JITK paper, the two companion specifications and the original executable experiments.

# 0. FIRST LAW — the entire mechanism before any implementation detail

**ONE KNOWLEDGE IDENTITY. THREE POSITIONS: LOCATION · RELATION · PROXIMITY.**

**One common knowledge record contains the naturally occurring values necessary for LOCATION, RELATION and PROXIMITY methods to operate against it.** These are three ways to address **the same recorded knowledge**, not separate representations to construct, slots to fill, databases to synchronize, or stages to process. The fourth position, **RESONANCE**, is the planned extension; it will be another position of the same knowledge, not a new knowledge system.

Capture what the source already knows: literal values, structure, identity, locations, links, parent/child relationships, order, named references and available proximity values. Keep these values **together**, in one shared, source-backed, OKF-compatible knowledge representation. An AST is already a graph: parent, child, sibling and containment are actual relationships. A webpage, conversation, book, document, event or language parse likewise offers whatever structure it truly contains. No intelligence is required to turn an observed relationship into a graph-accessible edge.

**The retrieval method changes. The knowledge does not.** Structural/AST-style navigation uses position; NetworkX or another graph algorithm uses relations; fuzzy/lexical/vector search uses proximity or literal content. Each method returns the same knowledge identity and can lead to the same exact source evidence. The caller may switch methods freely. The number of fields or methods is not fixed: preserve the available values a different method may later need.

**The crosswalk is literal.** Think of a place recorded by a town name, postal code, and latitude/longitude. Those are multiple ways of addressing the *same place*, with different precision and usefulness. The correct result is **one record carrying its known, labeled values side by side**—not a postal-code object converted into a town object and then into a GPS object. Entering through any one known value resolves the shared record. The other known values are immediately available right beside it. A value that is not present must not be guessed; an authoritative lookup or deterministic computation may supply it when actually needed, and its origin and precision remain explicit.

**In UKC the same rule applies to structure, relation and proximity.** Read a source with any suitable faithful mechanism. **Copy the values it already contains, literally, into the corresponding common OKF-compatible fields or preserved extensions, right beside the original information.** Where the source provides a parent, child, title, link, offset or existing proximity value, copy and label it; the method receiving the record does not own or reinterpret it. Do not convert AST into graph, graph into vector, or one search method's product into another. The record is not built by completing positions in sequence. A retrieval method selects the needed values directly from the one record. Independently computed additional values, when appropriate, are recorded there with their provenance—not manufactured by a conversion chain.

**Ingestion is deterministic, not semantic interpretation.** Same source, version, observations and declared rules produce the same IDs, recorded values, edges and positions. Use ordinary parsers, algorithms, hashes and indexes. Do not run an LLM to invent names, meanings, semantic layers or links already explicit in the source. If a relationship is **not** known, leave it unknown. When a human or intelligence later investigates and establishes a genuinely new, evidence-backed relationship, append only that discovery as an enrichment delta. Cheap, imperfect hashed proximity is valuable because it can lead to a node, its neighbors and an exact original passage. Vector calculation can happen independently and does not block use.

**If a system independently reinterprets each representation, requires an LLM to ingest known structure, invents missing relationships, or cannot move among methods using the same identity, it is NOT UKC.** This is an arithmetic-like, reproducible contract; do not replace it with a scanner architecture, graph engine, embedding model, agent framework or RAG workflow.

---

## 1. Purpose, sources of authority and normative language

UKC is an executable-language-independent SDK specification. Python, Rust, TypeScript, JavaScript, Java, Go, C/C++, C#, Swift, WASM or any other executable environment can implement it. A language, database, parser, framework, network service, model provider or UI is never an intrinsic requirement.

**MUST**, **MUST NOT**, **SHOULD** and **MAY** are normative. The first law and all Core requirements are mandatory. Advertised optional functions must pass their relevant conformance tests. Unsupported features must be reported, not faked.

Read this contract together with:
- [Canonical JITK paper](research/paper.md): origin, principle and the original cold-context GPS experiment.
- [Knowledge Asset Evolution v1.6.3](Knowledge-Asset-Evolution-Spec-v1.6.3.md): portable OKF-compatible ownership, lifecycle, schema governance and durable events, when those profiles are selected.
- [Knowledge Graph Relationships and Enrichment](Knowledge_Graph_Relationships_and_Enrichment.md): observed versus qualified discovered relations and provenance.
- [OpenKC architecture](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/ARCHITECTURE.md), [deterministic mapping](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/MAPPING.md), [working code](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/openkc_etl.py), [proof](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/EVIDENCE.md).
- [Original GPS experiment and replay](research/EXPERIMENT.md).
- [Official upstream OKF specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). This governs valid OKF assets. UKC additions described below are **producer-defined extension keys**, not purported native Google OKF fields.

The OpenKC experiment proved source-preserving AST–OKF round trips and observed syntax graph edges. The original GPS experiment documented a fresh investigator following imperfect lookup leads and graph relationships to four precise source passages from a source withheld from the model. They establish the mechanism in real, bounded tests—not universal parser/vector or large-corpus performance. New claims require executable evidence.

**Durability principle:** original sources and accepted evidence-backed intellectual discoveries survive. Indexes, graph databases, vectors and caches are projections and can be reconstructed. Losing a derived database must not require reproducing an earlier intelligence's reasoning when its accepted discoveries were already preserved.

### 1.1 Verification against the actual experiments — executable evidence

**The SDK rule comes from real code, not an analogy. These are two complementary tests, with different proven boundaries.**

**Experiment A — Scratchpad OpenKC: copy existing values into OKF beside the original source.** In [openkc_etl.py](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/openkc_etl.py), the CommonMark parser supplies a real AST containing source path, original byte digest, original source bytes, and complete token fields. The actual mapping is:

~~~python
def ast_to_okf(ast):
    meta=dict(type='MarkdownDocument',
              openkc_id='repo:barely-passable-ai-stuff/'+ast['path'],
              openkc_source_sha256=ast['source_sha256'],
              openkc_ast=ast)
    title=heading(ast)
    if title: meta['title']=title
    return note(meta,base64.b64decode(ast['source_base64']).decode('utf-8'))
~~~

**The decisive copy is the assignment openkc_ast=ast.** The entire *already existing* AST is preserved as one metadata value while the note body retains the original source. There is no LLM semantic interpretation. The source title is copied from an actual heading **only when present**.

The reverse path verifies both original bytes and exact re-parsed AST:

~~~python
ast=meta['openkc_ast']
assert base64.b64decode(ast['source_base64'])==body.encode()
assert sha(body.encode())==ast['source_sha256']
assert ast_from_bytes(body.encode(),ast['path'])==ast
~~~

See the [original exact field mapping](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/MAPPING.md). The tested path was AST → OKF → YANP → OKF → AST; it recovered the same AST and original bytes. Projection-only YANP metadata was identified separately from source facts.

**The Scratchpad graph used the same identity and facts.** The actual [ladybug_load.py](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/ladybug_load.py) writes one KnowledgeAsset, under a document ID, carrying adjacent AST, OKF and YANP:

~~~python
connection.execute(
    'CREATE (:KnowledgeAsset {id:$id,path:$path,sha256:$sha,ast_json:$ast,okf_markdown:$okf,yanp_markdown:$yanp})',
    {'id':document,'path':source_path,'sha':item['sha256'],
     'ast':json.dumps(ast,ensure_ascii=False),'okf':okf,'yanp':yanp})
~~~

The loader walks real AST tokens and emits HAS_ROOT or AST_CHILD based on *existing parent/child structure*. Populating graph edge tables is **deterministic indexing of recorded values**, not an inferred semantic transformation. The [actual evidence](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/EVIDENCE.md) establishes **5 source assets, 1,597 AST nodes, 903 root edges, 694 child edges**, with a successful durable reopen. A later live read-only Cypher workflow executed 12 queries and returned 77 matches.

**Experiment B — original GPS: multiple retrieval methods use the same knowledge ID.** The published [gps.py](examples/gps/gps.py) admits each source passage once, with its original source version and exact byte position, then uses the returned identity for sequence edges and the lexical-search reference table:

~~~python
n=k.add(source.name,text,version=version,
        position={'start_byte':offset,'end_byte':end},kind='passage')
if prev: k.link(prev,n,'next_passage')
db.execute('INSERT INTO refs VALUES (?, ?)',(row,n))
~~~

The two search paths both return knowledge IDs; neither converts one method into another:

~~~python
print(json.dumps({'exact':[x[0] for x in exact],
                  'vector':k.search(a.value)},indent=2))
~~~

Original source retrieval operates on the same node and recorded span:

~~~python
d=k.graph.nodes[n]
p=d['position']
b=raw[p['start_byte']:p['end_byte']]
~~~

The real read function additionally verifies the original source version and span content hash. The [preserved GPS replay](research/EXPERIMENT.md) verified **28 nodes, 42 edges (27 sequence, 15 lexical-shared-term), four requested source passages and exact source-backed reads**. Its hash-based vector offered cheap imperfect leads rather than new facts.

**What the experiments prove together, and what they do not:** Scratchpad proved **literal source/AST/OKF preservation, deterministic structural graph projection and verified retrieval**; it did not prove a complete vector SDK over OKF. GPS proved **same-ID lexical/vector/graph/source navigation**; it did not use OKF. The Tree-sitter-only proof independently parsed the same source corpus but was not a tested bridge from Tree-sitter to all these methods. This SDK specifies their **combined language-neutral invariant**, which still requires unified conformance testing before claiming the entire UKC/1 SDK is implemented.

**Normative interpretation:** Preserve each already-known native value **once**, directly alongside the original information in the common OKF-compatible record; deterministically materialize indexes or graph edge rows from that same record if a chosen search engine requires them. Do **not** convert an AST into a different knowledge graph interpretation, then convert that into vector knowledge. **Physical indexing is allowed; separate interpretations and method-to-method conversion are forbidden.** Unknown facts remain unknown. Any separately computed new value retains its origin and same record identity.

## 2. The three positions and fourth-position extension

| Position | Literal or computed values | Direct operations |
|---|---|---|
| **LOCATION** | Original source authority, identity, observed version, source span/anchor, native structural path and order (when known). | Resolve evidence; exact source/AST/DOM/document navigation. |
| **RELATION** | Same item ID, observed source links and native structural edges, plus separately admitted qualified findings. Preserve direction, type, multiplicity, order and provenance. | Traverse, inspect neighbors, select graph algorithms. |
| **PROXIMITY** | Declared lexical/fuzzy signals and zero or more specifically identified vector spaces. Unknown/queued vectors remain unknown. | Approximate candidate lookup and similarity. |
| **RESONANCE** (future) | Evidence-supported activity→knowledge→observed-consequence position. | Conditional importance from experience; not an implemented requirement of UKC/1. |

**Location, Relation and Proximity classify how the common values can be accessed; they are not independently maintained positional records.** There is no position-filling workflow. A retrieval method selects existing shared values and applies its ordinary deterministic algorithm. Individual unavailable values may be marked **unknown** or **not_applicable**; this is not an instruction to create three placeholder objects. A known empty set differs from missing data; a known zero vector differs from an uncomputed vector.

A tree is a graph from the moment its actual nodes and native edges are available. Existing title, identifier, href, message order and declared dependency values can support literal lookup and relation navigation immediately. The same record may also have native structured attributes not listed above. They must be preserved, not trimmed to three fields.

A vector never creates a causal or semantic relation by itself. Fuzzy overlap may indicate where to look. The source location closes the loop with verified evidence.

## 3. One logical record: the representation contract

Every successfully admitted knowledge item has **one common logical knowledge record** under a stable identity. Record the naturally occurring values once and preserve them alongside the original information. The fields provide the data on which structural, relational, lexical and vector methods operate; the SDK MUST NOT require three separately filled position objects. If a value needed by a particular method is unavailable, that method reports the missing value rather than blocking admission, constructing an alternate representation or launching a conversion chain. A single source can contain many items. The natural grain is source-adapter-defined: file, symbol, AST/DOM node, document section, message, event, paragraph, observed relation or qualified finding.

**Minimum UKC/1 logical fields** (not a mandated programming-language struct or physical DB schema):

| Name | Meaning |
|---|---|
| **schema** | Literal version label **ukc/1**. |
| **id** | Version-scoped deterministic knowledge identity (§4), shared by all methods. |
| **source** | Authority/owner namespace, source key, observed version/digest, original route/realm and current-access requirements. |
| **kind** | Honest native item kind. Never force HTML or prose to pretend to be Python AST. |
| **location** | Known source/structural coordinates and verification method, or explicit unknown. Keep all independently verified alternate coordinates. |
| **relations** | Zero or more native observed links/edges and qualified discovered relations (§5). |
| **proximity** | Zero or more space-ID-tagged vectors, with explicit status; lexical/fuzzy candidate access may use source text directly. |
| **values** | All supplied names, titles, typed fields, text, order, attributes, flags and literal facts; do not silently drop fields. |
| **native** | Complete supplied native parse/structure and/or immutable hash-addressed payload, sufficient for exact reconstruction of admitted inputs. |
| **evidence** | Source version, coordinates, original byte/span digests and separately accepted finding/event provenance. |

Use **one shared logical record**, even if runtime performance calls for multiple physical indexes. A graph table row and a vector-index entry referencing the same ID are not independent bodies of knowledge. They are materializations over the record. A consumer can read all known positions without another AI inference or a second import.

### 3.1 What “complete” means

**Entry-point invariance (mandatory):** Given identical source-backed observations, whether an adapter first encounters a node through a title, an AST node, a relationship, or a vector result, it MUST resolve the same canonical knowledge identity and expose the same known common-record values. No entry route may generate a distinct knowledge record or require rebuilding fields through its own retrieval engine. The source-native name, relation, path and numeric value remain individually labeled, with original precision and provenance preserved. **Record once; label deterministically; read through any applicable method.**

Record all values actually available at the input boundary. Never add a title, causal edge, actor, location or meaning not supplied. Missing fields stay unknown. Preserve native path, child order, UTF-8 offsets, explicit attributes and any source-specific field, even if no current search method needs them. An implementation may retain a large native payload in a content-addressed sidecar, but the record must have a verified pointer and portable export must include or resolve that payload. A dangling external payload is not a lossless record.

The SDK does not impose a universal AST schema. A deterministic adapter describes source-native structure; UKC records it.

### 3.2 OKF-compatible interchange

UKC records MUST have a **valid OKF-compatible representation** on export and import. Use upstream-recognized OKF fields correctly, plus a producer-defined **x_ukc** extension for identity, positions, original native values, evidence and optional sidecar references. The source body and its exact bytes must be preserved where available. Unknown YAML keys, native fields and unrelated OKF content must round-trip without being silently discarded.

**OKF is the common translation vocabulary and portable packaging, not a semantic extraction service.** Translating observed parser values to an equivalent OKF field/extension is a copy or deterministic mapping; it does not make an LLM think about their meaning. If a destination representation cannot express a native source value, preserve it losslessly in a native extension or sidecar and report limited direct query support. Do not manufacture equivalent meaning.

An illustrative asset (not a normative upstream OKF schema, and digest placeholders are intentionally not executable fixtures):

~~~yaml
---
type: SourceUnit
title: Example
x_ukc:
  schema: ukc/1
  id: "ukc:v1:<computed-digest>"
  source:
    authority: repo:example
    key: docs/example.md
    version: "sha256:<source-bytes-digest>"
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

## 4. Identity, exact source positions and deterministic equality

For new source-backed UKC/1 records, define a deterministic ID from **(schema, authority, source_key, observed_source_version, native_kind, native_unit_key)**. Exact same normalized inputs must produce exact same identity bytes in every language; no random UUID, database auto-ID or machine-specific temporary checkout path is allowed as a canonical identity.

**Canonical ID bytes profile UKC-ID-1:**
1. Construct the ordered six-element array of UTF-8 strings: **["ukc/1", authority, source_key, source_version, native_kind, unit_key]**.
2. Encode as compact UTF-8 JSON with no spaces, using literal non-ASCII Unicode (rather than optional ASCII escapes), escaping JSON quotes, backslashes and control characters. Adapter normalization of authority/path/unit is an explicitly versioned producer contract; input to ID hashing must be identical across languages.
3. SHA-256 the exact encoded bytes; output **ukc:v1:** followed by 64 lowercase hexadecimal characters.

For already existing historical identities, retain a stable **legacy_id** alias mapping to an unambiguous canonical record. Never silently claim a historical hash was computed by this new scheme. A new source version may produce a new source-versioned ID; retain stable logical-unit aliases and supersession links when available. Do not change unrelated IDs because another file changed.

**Coordinates:** exact UTF-8 byte ranges are zero-based, end-exclusive; all other coordinate systems declare their unit, basis and version. Prefer source-native hierarchy/anchor over guessed line numbers; preserve complementary verified spans. Model-described positions are candidate leads until deterministic reader/source evidence confirms them.

**Resolution:** to read exact original evidence, check access for the present principal, source authority and version, span bounds and content hash. Changed or inaccessible sources return typed failure/lead status, never substitute a new source and claim exact evidence. A locator is not an access grant.

**Hashes:** SHA-256 of original bytes and specific spans is an integrity identity, not semantic understanding. Reuse unchanged work. Source and accepted enrichment hashes must have distinct ownership and update rules when optional lifecycle governance is enabled.

## 5. Relationship rules and enrichment boundary

A relation record MUST contain **subject ID, predicate, object ID or unresolved target locator, origin, qualification, evidence**, and preserve native direction/order/attributes. A source-supplied parent/child edge, sibling order, declared URI/link, import, dependency or literal “related_to” is an **observed fact of the source**, not AI enrichment. Record and index it immediately. No mandatory ontology normalization or invented “meaning layer.”

A similarity candidate is not a source relationship. Similar titles, shared terms, grammar parse features, cosine scores and co-visitation can provide **leads**. If an implementation stores them as edges, it must label them honestly as lexical/syntactic/similarity observations and never silently promote them to verified causes, prerequisites or semantic relationships.

**Enrichment** begins only where ordinary reading/investigation reveals new knowledge not already supplied. A newly established relation is appended as a separate, source-backed delta with actor, evidence, qualification/status and time/source version where known. It must not rewrite original source facts or rebuild untouched records. Unreviewed candidates remain proposals. The companion Relationships and Evolution specifications define richer qualification/governance when implemented.

**Forbidden:** “Before graph search can work, the LLM must extract all semantic relationships.” The graph already has native relations. Intelligence may later discover more.

## 6. Deterministic source acquisition and adapters

Input is allowed from **any source with an honest adapter**. Examples:

| Source | Existing tools that may read it | Native observations to keep |
|---|---|---|
| Code | Python ast, Tree-sitter, compiler parser, Rust syn, TypeScript compiler API | Node kinds, names, declared references, hierarchy, order, actual spans and attributes. |
| Web/HTML | DOM/HTML parser | Elements, attributes, links, hierarchy, anchors and text coordinates. |
| Markdown / documents | CommonMark, document parser, PDF text/page extractor | Headings, blocks, links, order, actual spans, pages/regions. |
| Natural language | Tokenizer, spaCy or equivalent language parser | Tokens, sentence positions, syntactic dependency relations and observed entity spans; inferred world facts remain proposals. |
| Conversations | Provider transcript/export parser | Session/message IDs, roles, timestamps, sequence, explicit references and source passages. |
| Structured sources | JSON/XML/CSV/schema reader | Native fields, order, keys, declared relations and pointers. |
| Events | Structured log/OTLP/event reader | IDs, timestamps, native fields and actually supplied causal links. |

An adapter MUST output **source description + observed records + observed edges + actual positions + native payload** and no invented relationships. An unsupported native format may be admitted as raw bytes/text with unknown structural fields, not silently mislabeled as a parsed AST.

Adapters are not compulsory at the core boundary; applications may supply already-structured data directly. Parser selection is an implementation detail. Reuse native libraries for efficiency rather than reinventing parsing, graph algorithms or fuzzy mathematics.

## 7. Proximity: useful even when imperfect; never blocking

The common record may contain declared proximity values or indicate that a specific computed value is unavailable; it does not require a separately managed proximity slot. Cheap lexical/hash computation can be run from the recorded literal values when requested or as an independent derived calculation. Semantic/neural embedding, if used, is optional and can happen later. An incomplete vector does not invalidate source/location/relations and MUST NOT block searches available through those values.

**Required vector-space descriptor:** space ID, dimensions, exact encoder algorithm and version, tokenization/Unicode/preprocessing, stop words, sign convention, input policy, normalization, numeric representation and source-content digest where applicable. A query must use the same space as stored vectors. Mismatched spaces are rejected, not silently compared.

**Observed real incompatibility:** [original GPS encoder](examples/gps/gps.py) and [Rust-scanner-compatible encoder](research/omnigraph/encoder.py) both historically used the label “lexical-hash-512” but differ in stop-word and sign behavior. They are **NOT** interchangeable. Name their profiles distinctly (e.g. **lexical-hash-512/gps-legacy-v1** versus **lexical-hash-512/rust-scanner-v1**) and verify cross-language output with the same actual source strings. No language or ML model is pinned; exact behavioral compatibility is.

An approximate proximity result MUST return a candidate canonical ID and source/evidence route. Proximity score alone is not a verified relation or an answer.

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

## 9. Retrieval and investigative loop

An agent may choose any route:
1. Exact location known → read that original span.
2. Name/title known → literal search resolves a record ID.
3. “What connects to this?” → graph traversal of already-recorded edges.
4. Approximate concept → fuzzy/lexical/vector candidates → inspect candidate neighborhood → resolve source.
5. Missing relationship discovered during reading → qualify evidence → add one new relation delta.
6. Reuse the resulting record and relationship on the next investigation.

**No prescribed search sequence.** Graph algorithms may be NetworkX, native Cypher, other graph libraries or plain adjacency operations. Structural search may use Tree-sitter, native AST/DOM paths or a document parser. A fast imperfect lead is enough when the source can be reached and checked.

The experimental principle is: **“The fuzzy match opens the door. The structure does the rest.”** The model formulates a search/traversal; deterministic tools execute; evidence is inspected; novel discoveries are admitted separately.

## 10. Mandatory conformance suite: no claims without execution

Implementations MUST publish a language-neutral fixture runner and real, inspectable outputs. Fixture input includes raw source bytes, source identity/version, parser observations, native attributes and observed edges. Output includes canonical ID input bytes/hash, logical records, relation lists, vector space, exact resolved source bytes and export/import verification.

| Test | Required behavior |
|---|---|
| **UKC-01 SAME ITEM** | Enter through a title/literal name, native structural selector, observed graph link, or available vector result for the same unit. Every path resolves **one exact canonical ID and the same known shared values** without converting one method's representation to another. |
| **UKC-02 TREE IS GRAPH** | Real parsed parent, child and sibling order are immediately traversable as observed edges. No invented semantic edges. |
| **UKC-03 LITERAL PRESERVATION** | Arbitrary native fields, Unicode, punctuation, source bytes and source hierarchy survive OKF export→import unchanged. |
| **UKC-04 HONEST UNKNOWN** | Missing vector, missing title and unknown relation/location remain explicitly unknown; no defaults invented as facts. |
| **UKC-05 IMMEDIATE INGEST** | Admit without any LLM/encoder/network dependency; source/graph/lexical access works before vectors are computed. |
| **UKC-06 KNOWN EDGE** | A real input link or named relation is queryable immediately, with original direction, type and provenance. |
| **UKC-07 ENRICHMENT DELTA** | A verified later relation adds only the evidence-backed relation, leaves source/native fields intact and is idempotent. |
| **UKC-08 VECTOR PROFILE** | Mismatched GPS/Rust lexical-hash profiles are rejected; equal, declared profiles produce equivalent vectors in different languages. |
| **UKC-09 IMPERFECT LEAD** | A candidate with no direct answer leads via neighbor and source location to precise evidence; this is an end-to-end investigation test. |
| **UKC-10 SOURCE CHANGED** | Changed source bytes refuse stale exact reads while preserving prior evidence and versions. |
| **UKC-11 RECONSTRUCTION** | Recreate graph/lexical/vector projections from original sources and accepted discovery records; no re-reasoning of previous discoveries. |
| **UKC-12 CROSS-LANGUAGE** | Independent language implementations consume identical fixtures and agree on IDs, fields, observed edges, source bytes and encoder-specific vectors. |
| **UKC-13 ACCESS** | Knowing a private locator does not grant read access; current authorization controls resolution. |
| **UKC-14 SOURCE AGNOSTIC** | Code plus an HTML, Markdown, prose or conversation source preserve their actual values in the same common-record contract, accessible by applicable methods without fabricated universal AST or separate position records. |
| **UKC-15 ORIGINAL PROOFS** | Re-execute real OpenKC lossless translation/observed-edge proof and GPS source navigation replay, recording what was actually tested. |

**Core certification requires UKC-01 through UKC-08, UKC-10, UKC-11, UKC-13 and UKC-14.** UKC-09 and UKC-15 are required end-to-end demonstration evidence; do not substitute a mocked trace for the original recorded experiments. **UKC-12 is required to claim parity between two language implementations.** If the conformance fixtures/runner do not yet exist, this spec is a defined contract, **not a claim of certified SDK completion**.

Maintain portable actual fixtures, expected IDs, encoded hash input bytes, original blobs, expected relations, encoder outputs and test reports under a shared **conformance/** directory. A future language must run the same fixtures rather than invent new “equivalent” ones. No pinning of a specific language implementation is required.

### Invalid implementations, regardless of apparent usefulness

A claimed UKC SDK **fails** when:
- It maintains separate AST, graph and vector *interpretations* with unrelated IDs.
- It needs an LLM to turn already supplied parent/child/links into observed graph edges.
- It loses source-native values during “conversion.”
- It invents relationships from title similarity or embeddings and presents them as observed.
- It cannot trace a candidate through the same ID and relation to the original source.
- It forces embedding or corpus-wide enrichment before indexing a source.
- It aliases incompatible vector algorithms under the same space name.
- It requires all source types to become synthetic Python AST.
- It uses only a disposable graph store for hard-won prior discoveries.
- It passes an example but cannot pass the common conformance contract.

## 11. Lifecycles, updates, concurrency, storage and performance

**Sources and accepted discoveries are durable. Projections are disposable.** An implementation MAY use JSON, SQLite, LadybugDB, OmniGraph, NetworkX, Rust containers, distributed storage or a vector DB. Its physical layout is immaterial provided the logical record and observable operations remain exact.

Admission MUST be idempotent. A source version change must preserve evidence and supersession history and update only affected positions/edges. Concurrent writers must use transactions or a coherent serialization strategy, not silently overwrite accepted deltas. Unknown or ambiguous source read failures remain visible.

**Deterministic ingestion captures available knowledge once, not representations in sequence.** Use any faithful source-native reader to preserve naturally occurring values together in the common record, beside source evidence. Retrieval methods directly consume those fields; no AST→graph→vector or other staged translation. Missing computed values may be calculated independently from the common recorded inputs, if actually required, without reconstructing earlier methods. Compute expensive vectors or optional new relationships separately as needed. Reuse unchanged hashes, records and positions. A large folder scan is not a whole-corpus intelligence job. Rebuild indexes instead of designing expensive recovery machinery whenever source reconstruction is faster and preserves all accepted knowledge.

Do not invent a benchmark threshold: measure with real input size, wall time, memory, store size, and LLM-call count. The zero-required-LLM-call condition for ordinary ingestion is normative.

## 12. Implementer's exact procedure

1. Read and implement **First Law**. No parser, DB or language choice changes it.
2. Use any suitable faithful source-native reader to obtain naturally occurring literal values, relationships, structure, coordinates and source evidence.
3. Establish one canonical ID and record all observed values **once** in the common OKF-compatible record, preserving the original information beside them. Do **not** create independent structural, graph and vector versions.
4. Have structural, graph, fuzzy/lexical and vector methods select their needed shared values directly from that record. If a required computed value is missing, the particular operation can calculate or request that value independently; it must not convert another retrieval representation or delay unrelated operations.
5. Prove complete lossless OKF-compatible import/export; preserve native extension values.
6. Add cheap lexical/fuzzy discovery and declared compatible vectors independently of record admission.
7. Implement qualified on-touch enrichment as **additive evidence-backed deltas**, not a mandatory scan phase.
8. Support version-verified exact source resolution, privacy boundaries, incremental updates and reconstruction from durable evidence.
9. Run and publish the conformance suite; show failures honestly. Compare Python, Rust and every new implementation against identical fixtures.
10. Wire OmniGraph, MCP, a CLI, an agent or a UI **after** the contract works, as consumers—not as alternative definitions of knowledge.

**Finished means:** an independent implementer can write the SDK in any execution language and obtain the same identities, captured values, observed edges, known/unknown positions, exact source evidence and cross-method navigation from identical fixtures. If the result requires interpretive re-ingestion or loses the common identity, it is not UKC.

## 13. Future fourth position: Resonance

**Resonance** represents experienced importance conditioned on task/activity, knowledge and observed consequence, as proposed in the research paper. It is *soon to be the fourth position*, not a fourth mandatory ingestion phase or a new semantic knowledge store. UKC/1 reserves the extension; full rules, evidence, algorithms, qualification and conformance must be defined before implementation claims. Adding Resonance MUST preserve the existing identity and deterministic first-three-position contract.

---

**Permanent statement:** **The knowledge was already there. Record its naturally occurring shared values once, beside the original source, in one common OKF-compatible knowledge record. Retrieval methods decide how to use those same values. Let intelligence add only what it genuinely learns.**
