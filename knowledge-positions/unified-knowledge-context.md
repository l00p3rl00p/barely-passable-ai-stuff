# Unified Knowledge Context (UKC): The Knowledge Positions SDK

**Normative contract:** UKC/1 candidate. **Target:** any execution language. **Authority:** this file, the existing JITK paper, the two companion specifications and the original executable experiments.

# 0. FIRST LAW — the entire mechanism before any implementation detail

**ONE KNOWLEDGE IDENTITY. THREE POSITIONS: LOCATION · RELATION · PROXIMITY.**

**One common knowledge record contains the naturally occurring values necessary for LOCATION, RELATION and PROXIMITY methods to operate against it.** These are three ways to address **the same recorded knowledge**, not separate representations to construct, slots to fill, databases to synchronize, or stages to process. The fourth position, **RESONANCE**, is the planned extension; it will be another position of the same knowledge, not a new knowledge system.

Capture what the source already knows: literal values, structure, identity, locations, links, parent/child relationships, order, named references and available proximity values. Keep these values **together**, in one shared, source-backed, OKF-compatible knowledge representation. An AST is already a graph: parent, child, sibling and containment are actual relationships. A webpage, conversation, book, document, event or language parse likewise offers whatever structure it truly contains. No intelligence is required to turn an observed relationship into a graph-accessible edge.

**The retrieval method changes. The knowledge does not.** Structural/AST-style navigation uses position; NetworkX or another graph algorithm uses relations; fuzzy/lexical/vector search uses proximity or literal content. Each method returns the same knowledge identity and can lead to the same exact source evidence. The caller may switch methods freely. The number of fields or methods is not fixed: preserve the available values a different method may later need.

**The crosswalk is literal.** Think of a place recorded by a town name, postal code, and latitude/longitude. Those are multiple ways of addressing the *same place*, with different precision and usefulness. The correct result is **one record carrying its known, labeled values side by side**—not a postal-code object converted into a town object and then into a GPS object. Entering through any one known value resolves the shared record. The other known values are immediately available right beside it. A value that is not present must not be guessed; an authoritative lookup or deterministic computation may supply it when actually needed, and its origin and precision remain explicit.

**In UKC the same rule applies to structure, relation and proximity.** Read a source with any suitable faithful mechanism. **Copy the values it already contains, literally, into the corresponding common OKF-compatible fields or preserved extensions, right beside the original information.** Where the source provides a parent, child, title, link, offset or existing proximity value, copy and label it; the method receiving the record does not own or reinterpret it. Do not convert AST into graph, graph into vector, or one search method's product into another. The record is not built by completing positions in sequence. A retrieval method selects the needed values directly from the one record. Independently computed additional values, when appropriate, are recorded there with their provenance—not manufactured by a conversion chain.

**The parser is a capture boundary, not an intelligence boundary.** It decides which existing values are recognized and labeled during that capture. A code AST parser will not normally label postal codes and geographic coordinates in prose; a geographic or structured-location parser may expose them directly. The generic parser's failure to recognize a field does **not** mean the knowledge is absent: the unchanged source and its known structure remain searchable. When an actual task touches that knowledge, an LLM or specialized enricher MAY read the source, recognize the missing location semantics, and append a qualified, source-evidenced field or relationship to the **same common record**. Do not enrich the entire corpus or retroactively alter unrelated items. A future native parser encountering those same facts may capture them immediately. **Parser-dependent capture and selective on-touch enrichment are complementary, not rival architectures.**

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
- [Official upstream OKF specification](https://github.com/open-knowledge-format/open-knowledge-format/blob/main/SPEC.md). This is the current upstream **OKF v0.3** specification; the previous GoogleCloudPlatform repository contains deprecated v0.2. UKC keys are **producer-defined extensions**, not fields standardized by OKF itself.

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

### 1.2 Woburn GPS characterization — actual original code, not a hypothetical example

A small reproducible source is [conformance/fixtures/woburn-gps.md](conformance/fixtures/woburn-gps.md):

~~~markdown
# Woburn, Massachusetts
- Postal code: 01801
- Latitude (illustrative city point): 42.479261
- Longitude (illustrative city point): -71.152278
~~~

The coordinates identify **an illustrative point**, not an exact universal location of the entire city. The probe at [conformance/probes/original_openkc_gps_probe.py](conformance/probes/original_openkc_gps_probe.py) **imports the original Scratchpad openkc_etl.py** and invokes its actual ast_from_bytes, ast_to_okf, split_note and okf_to_ast functions. It does not replace that code with a mock translation.

**Characterization observed with the same original functions:**
- Original source bytes preserved: **PASS**.
- Parsed AST exact round trip: **PASS**.
- Literal city, postal code and latitude/longitude retained in the source body and AST content: **PASS**.
- Separate first-class OKF metadata fields for postal_code, latitude, longitude: **NOT PRESENT**. The original metadata keys are type, openkc_id, openkc_source_sha256, openkc_ast and title.

The original code did exactly what the early proof promised: **losslessly preserved the already parsed source inside an OKF-compatible note**. It did **not** provide the additional field-level deterministic crosswalk from Markdown list labels to named geographic values. That absent mapping is a **real implementation gap**, not evidence that the preserved source knowledge is missing and not a reason to introduce a semantic LLM extraction pass.

**Normative UKC implication:** For a recognized source format or explicitly supported field convention, a deterministic adapter MUST expose the source's **existing labeled values** as named fields in the same common record, while keeping the original unchanged. For this fixture, an adapter advertising the convention must expose:
- Woburn, Massachusetts as the exact observed place label.
- 01801 as the literal observed postal-code string (retain the leading-zero rule for postal values generally).
- 42.479261 and -71.152278 as the declared observed coordinate values, explicitly typed and labeled as an illustrative point.

Those are **not three different knowledge records**, and copying these fields is **not** an AST→graph→vector conversion. The already observed values sit beside the source, and geographic/structural/graph/lexical consumers may use them directly if applicable. An adapter that does not recognize the field convention MUST report it unsupported rather than pretend it produced a complete named-value crosswalk.

Run this characterization against an actual checkout of the original Scratchpad script:

~~~bash
python knowledge-positions/conformance/probes/original_openkc_gps_probe.py \
  --openkc-script /path/to/quatrus-scratchpad/experiments/openkc-ast-okf-yanp/openkc_etl.py
# The original byte/AST preservation should pass and reports missing named GPS fields.
python knowledge-positions/conformance/probes/original_openkc_gps_probe.py \
  --openkc-script /path/to/quatrus-scratchpad/experiments/openkc-ast-okf-yanp/openkc_etl.py \
  --require-field-crosswalk
# Expected to fail on the untouched original code, revealing the exact missing mapping.
~~~

Do **not** report this characterization as a completed UKC SDK conformance run. It identifies the missing SDK behavior with an actual original implementation and a new literal source fixture. A future implementation must pass a separate assertion that its declared field adapter writes and retrieves those labeled values from the same common record, not merely from a reparse of the raw source.

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

### 3.2.1 Parser fidelity is mandatory: raw input → native parser output → copied OKF values

**NEVER skip the middle column.** A source example followed by hand-written metadata is not an executable parser specification. An SDK author MUST see (1) the exact source bytes, (2) the actual selected parser and its raw returned values, (3) the mechanical field-to-field mapping into the ONE shared OKF-compatible record, and (4) which retrieval methods consume those fields. This section records a real local parser audit of the seven examples below. It is **not** a claim that the original OpenKC script itself implements every adapter. The complete native parser-output snapshot from this audit is independently saved as an artifact; any implementation MUST be able to regenerate its own test evidence from the literal fixture bytes.

**Parser identity and positions cannot be hand-waved.** Specify parser name, grammar/mode, version at run time, original source hash, each returned field, and the coordinate convention. A parser token's map in lines is **not** a byte span; an HTMLParser event position is **not** a DOM node's byte span; a decoded CSV number is still originally a string. When a field is not emitted by the parser, DO NOT assert it came from the parser. Capture available source-path/byte metadata **separately** from actual parser observations. An adapter may deterministically add a value by reading the original bytes; label that operation as an adapter extraction, not raw parser output.

#### Actual native parser observation 1: Python AST

**Input:** the exact 94-byte code/cart.py source shown in Example A below.

**Actual CPython ast.parse tree fields, selected without inventing any nodes:**

~~~text
Module.body[0] = ImportFrom(
    module='decimal', level=0, lineno=1, col_offset=0,
    end_lineno=1, end_col_offset=27)
Module.body[1] = FunctionDef(
    name='total', lineno=3, col_offset=0,
    end_lineno=4, end_col_offset=36)
~~~

The actual ImportFrom has an alias child with name Decimal. The FunctionDef includes argument nodes price and quantity and a Return containing a multiplication; these are native AST children, not inferred semantic relations.

**One-record field crosswalk (and field origin):**

| Recorded field | Value | Exact origin |
|---|---|---|
| filename | cart.py | Filesystem path basename; **not** ast.parse |
| source byte length | 94 | len(original UTF-8 bytes); **not** AST coordinates |
| functions | [total] | Module.body[1].name |
| imports | [decimal] | Module.body[0].module |
| source location | code/cart.py | Source resolver/adapter |
| native structural relationships | Module contains ImportFrom and FunctionDef | Actual Module.body ordering and native node hierarchy |
| lexical proximity inputs | cart.py and preserved code text | Original source and filename |
| vector | unavailable until a declared encoder computes one | **Not** produced by ast.parse |

Location reads the source / AST coordinates; Relation traverses actual node containment and import declaration; Proximity matches names/code text and may calculate an optional vector. **All three address the one record.**

#### Actual native parser observation 2: HTML event parser, not a fabricated DOM

**Input:** the exact 113-byte web/recipe.html source shown below. **Actual Python html.parser.HTMLParser output, selected events:**

~~~text
('starttag', 'h1', [], (1,12))
('data', 'Flatbread', (1,16))
('starttag', 'a', [('href','/recipes/dough')], (1,30))
('data', 'Dough method', (1,55))
('starttag', 'p', [], (1,71))
('data', 'Mix flour with water.', (1,74))
~~~

Other start/end events (html, body, h1, a, p) also exist. HTMLParser.getpos() provides **one-based line and zero-based column** for each event, **not end-exclusive UTF-8 byte ranges**. The stdlib HTMLParser provides events; a DOM hierarchy would require a separate parser or an explicitly constructed stack. The example's title Flatbread is an **adapter-derived display title from the observed h1**, **not** an HTML title element that this source does not contain.

**Mapping:** original starttag/href value → observed href relation to /recipes/dough; text data → preserved literal text; source path → location; captured strings → lexical proximity input. Do not invent that the content describes a complete recipe or that the link destination exists. A real DOM parser may give parent/child node structure immediately, but this particular event parser does not.

#### Actual native parser observation 3: CommonMark recipe

**Input:** exact 93-byte docs/flatbread.md source shown below. **Actual markdown-it-py CommonMark top-level token excerpts:**

~~~text
heading_open   tag='h1' map=[0,1] content=''
inline         tag=''   map=[0,1] content='Flatbread'
heading_close  tag='h1' map=None content=''
heading_open   tag='h2' map=[1,2] content=''
inline         tag=''   map=[1,2] content='Ingredients'
bullet_list_open tag='ul' map=[2,4] content=''
list_item_open tag='li' map=[2,3] content=''
inline         tag=''   map=[2,3] content='2 cups flour'
list_item_open tag='li' map=[3,4] content=''
inline         tag=''   map=[3,4] content='1 cup water'
heading_open   tag='h2' map=[4,5] content=''
inline         tag=''   map=[4,5] content='Instructions'
inline         tag=''   map=[5,6] content='Mix flour and water.'
~~~

The actual parser returns **24 top-level tokens and 6 inline tokens** for this input; the printed rows are deliberately a **selection**, not a fictional complete token array. Inline tokens contain real child text nodes. The token map is a **zero-based, end-exclusive line interval**; many closing/inline child tokens have map=None. The parser does **not** independently emit structured recipe fields named ingredient, quantity, unit or cooking time.

**Mapping:** the actual inline content beside heading_open provides existing section labels; list tokens and observed nesting provide structural relationships; the original Markdown is retained verbatim for full-text/fuzzy lookup. Separately recognizing “2 cups flour” as an ingredient is a declared domain adapter extraction or source-backed on-touch enrichment, **not** an output of the generic CommonMark parser.

#### Actual native parser observation 4: book chapter with an inline hyperlink

**Input:** exact 91-byte books/chapter2.md source below.

~~~text
heading_open  tag='h1' map=[0,1]
inline        map=[0,1] content='Chapter 2: The Harbor'
paragraph_open tag='p' map=[1,3]
inline        map=[1,3]
  content='See [Chapter 3](chapter3.md).\nThe boat reached the harbor at dawn.'
  children:
    text('See ')
    link_open(tag='a', attrs={'href':'chapter3.md'})
    text('Chapter 3')
    link_close(tag='a')
    text('.')
    softbreak(tag='br')
    text('The boat reached the harbor at dawn.'
~~~

**Critical accuracy point:** the two subsequent source lines are **one paragraph** in this CommonMark parse, not two distinct paragraphs. The link is the actual link_open **child** of an inline token; it is not a top-level parser token. This parser reports 6 top-level tokens and 2 inline tokens.

**Mapping:** copy heading, native paragraph content, child href and source mapping. The source link becomes a graph-indexable observed relation to chapter3.md. No conversion into a separate semantic knowledge object is necessary; physical graph indexing merely copies the existing link.

#### Actual native parser observation 5: marketing HTML

**Input:** exact 115-byte marketing/launch.html source below. HTMLParser event excerpts:

~~~text
('starttag','section',[],(1,0))
('starttag','h1',[],(1,9))
('data','Autumn Launch',(1,13))
('starttag','a',[('href','/products/shoes')],(1,31))
('data','See shoes',(1,57))
('starttag','p',[],(1,70))
('data','Sizes 8, 9 and 10 available.',(1,73))
~~~

**Mapping:** copy the source claim exactly as text, the real href exactly as a relation, and the source path. No parser output says that the sizes are verified in stock. A domain enricher may later recognize advertised size values, sourced to that paragraph; it must not silently elevate an advertisement to current inventory truth.

#### Actual native parser observation 6: CSV, not inferred spreadsheet semantics

**Input:** exact 32-byte sheets/shoes.csv source below. Actual csv.DictReader output:

~~~python
fieldnames == ['sku', 'size', 'stock']
rows == [
    {'sku': 'S01', 'size': '8', 'stock': '12'},
    {'sku': 'S02', 'size': '9', 'stock': '6'}
]
~~~

**Mapping:** preserve string cell values and original columns. A table adapter may attach actual line/row numbers from its reader; csv.DictReader itself gives row dictionaries and fieldnames, **not** a typed Excel cell object, product database relationships, or a shoe-size standard. The relation “source contains row 2” comes from observed row order. Numeric comparisons require explicitly declared coercion and units; do not retype all size values automatically.

#### Actual native observation 7: unknown or opaque binary

**Input:** 8 bytes 00 61 73 6d 01 00 00 00, named bin/renderer.wasm.

There is **no native AST or DOM parse** in this test. The filesystem/source adapter supplies:

~~~json
{"filename":"renderer.wasm","extension":".wasm","byte_length":8,"path":"bin/renderer.wasm"}
~~~

It can additionally compute SHA-256 over those exact bytes, preserve the raw bytes, and record observed parent folder bin. **No claim of parsing WebAssembly symbols or behavior is made.** Location, observed filesystem relation and filename similarity still work. The file may later be touched with an actual binary-aware parser, without revisiting unrelated knowledge.

#### Validation rules for all language implementations

1. A documented parser claim MUST be traceable to actual returned native fields and an exact source fixture; save the full raw parse output, not merely a narrative excerpt.
2. A mapping MUST identify whether each value came from the parser, the source resolver/filesystem, a deterministic adapter extraction, an independently computed score/embedding, or evidence-backed on-touch enrichment. They must not be conflated.
3. Actual native parse fields, unrecognized attributes, order and source content MUST be retained losslessly. If a projection has a limited field vocabulary, preserve unrecognized native data without inventing equivalents.
4. The three search methods MUST consume the same accepted values/identity. Parser-specific missing fields do not prohibit retrieval through available source names, positions, recorded relations or text.
5. The expected test value is the **actual parser result** for the declared parser, grammar/mode and version. A deliberately simplified common-record view is acceptable **only if it is labeled a selection** and an exact full native record remains accessible.
6. Test passing means byte/AST/field equality where declared, not a marketing assertion of “99.999% accuracy.” A parser that returns different grammar structures from another parser can still conform by faithfully preserving its own **actual** observations, without claiming the token sequences are identical.

### 3.3 Source → common OKF record → Location / Relation / Proximity: executable examples

**This section is normative by example.** An implementation in any language must recognize what the source actually supplies, copy useful values into *one* source-backed record, retain the original, and make its methods consume those common values. **The method is a reader, not the author of another knowledge representation.** Example identities prefixed fixture: below are human-readable test IDs; they are **not** a substitute for the canonical hash IDs defined in §4. Each x_ukc mapping below is an **OKF producer-defined extension**, not an upstream standard field. The actual asset bytes, SHA and native parser output must be preserved/referenced even when only selected fields are shown here.

Every example explicitly supplies three available ways to find the item:
- **LOCATION:** source identity, actual path or anchor, recorded coordinates and original evidence.
- **RELATION:** a naturally existing hierarchy/parent, document link, code import, sequence or other explicitly observed edge. This can be as simple as contained_in → parent folder.
- **PROXIMITY:** available string/text/numeric inputs for fuzzy, lexical or mathematical similarity, with an optional computed vector. **A vector is not compulsory to preserve or search proximity.**

#### A. Code — actual parser shape, not invented software semantics

**Input: code/cart.py (94 UTF-8 bytes)**

~~~python
from decimal import Decimal

def total(price, quantity):
    return Decimal(price) * quantity
~~~

Python's real ast.parse exposes ImportFrom(module="decimal") and FunctionDef(name="total"), plus node hierarchy and original line/column coordinates. Store those actual fields, unmodified source bytes and the observed import edge. Do not infer that the function is correct or broken.

**Shared OKF-compatible record (selected preserved values):**

~~~yaml
---
type: Source Code
title: cart.py
x_ukc:
  id: "fixture:code/cart.py"
  source: "code/cart.py"
  values:
    filename: cart.py
    extension: .py
    byte_length: 94
    functions: [total]
    imports: [decimal]
  location: {path: "code/cart.py", byte_start: 0, byte_end: 94}
  relations:
    - {predicate: contained_in, target: "folder:code"}
    - {predicate: imports, target: decimal}
  proximity_input: "cart.py from decimal import Decimal def total price quantity"
---
Original source remains the separately retained code/cart.py.
~~~

**Location:** read code/cart.py, or use the retained AST to locate the function. **Relation:** traverse contained_in and imports; neither link is an invented semantic judgment. **Proximity:** fuzzy query “decimal total” compares against recorded filename/source text. **On touch:** “What's wrong with total?” requires inspecting actual code and tests, not an ingestion-time bug guess.

#### B. Webpage — DOM, actual hyperlink, exact page source

**Input: web/recipe.html (113 UTF-8 bytes)**

~~~html
<html><body><h1>Flatbread</h1><a href="/recipes/dough">Dough method</a><p>Mix flour with water.</p></body></html>
~~~

An ordinary HTML parser already knows the element hierarchy, text and href. No LLM is required to label those native fields.

**Same common-record shape, different native values:**

~~~yaml
---
type: Web Page
title: Flatbread
x_ukc:
  id: "fixture:web/recipe.html"
  source: "web/recipe.html"
  values:
    filename: recipe.html
    extension: .html
    byte_length: 113
    tags: [html, body, h1, a, p]
    text: [Flatbread, Dough method, "Mix flour with water."]
    links: ["/recipes/dough"]
  location: {path: "web/recipe.html", byte_start: 0, byte_end: 113}
  relations:
    - {predicate: contained_in, target: "folder:web"}
    - {predicate: href, target: "/recipes/dough"}
  proximity_input: "recipe.html Flatbread Dough method Mix flour with water."
---
Original HTML bytes remain at web/recipe.html.
~~~

**Location:** locate the source or the original h1/p DOM coordinates if present. For an actual online webpage, preserve its observed URL and snapshot version rather than inventing a URL. **Relation:** follow the real href. **Proximity:** “flatbread flour” can find this page by token overlap even without an exact matching phrase or a vector embedding.

#### C. Cooking — a document is not code, but its headings are structure

**Input: docs/flatbread.md (93 UTF-8 bytes)**

~~~markdown
# Flatbread
## Ingredients
- 2 cups flour
- 1 cup water
## Instructions
Mix flour and water.
~~~

A CommonMark parser returns actual headings, nesting, list nodes and source positions. A recipe-aware parser could additionally expose ingredient name and amount; a generic Markdown parser may not. Neither result loses the original text.

~~~yaml
---
type: Document
title: Flatbread
x_ukc:
  id: "fixture:docs/flatbread.md"
  source: "docs/flatbread.md"
  values:
    filename: flatbread.md
    extension: .md
    byte_length: 93
    headings: [Flatbread, Ingredients, Instructions]
  location: {path: "docs/flatbread.md", byte_start: 0, byte_end: 93}
  relations:
    - {predicate: contained_in, target: "folder:docs"}
  proximity_input: "flatbread.md Flatbread Ingredients 2 cups flour 1 cup water Instructions Mix flour and water"
---
# Flatbread
## Ingredients
- 2 cups flour
- 1 cup water
## Instructions
Mix flour and water.
~~~

**Location:** open the original Ingredients section. **Relation:** traverse native section nesting and the document's parent folder; only include section edges if the chosen parser actually supplied them. **Proximity:** “flatbread flour” uses recorded words. **On touch:** if quantities matter to a cooking task, a source-grounded enricher can add two ingredient fields and retain their paragraph evidence. Nothing else in the cookbook needs enrichment.

#### D. Writing a book — a useful lead may be the chapter, not the answer

**Input: books/chapter2.md (91 UTF-8 bytes)**

~~~markdown
# Chapter 2: The Harbor
See [Chapter 3](chapter3.md).
The boat reached the harbor at dawn.
~~~

**Common record:** id fixture:books/chapter2.md; values include filename chapter2.md, heading Chapter 2: The Harbor, original full text and literal link chapter3.md; location is books/chapter2.md bytes [0,91); relations are contained_in → folder:books and observed href → chapter3.md; proximity uses original title/text.

**Location:** a query can find the chapter and read the sentence. **Relation:** follow the real Chapter 3 link. **Proximity:** “ship arrives at port” need not hit perfectly; a source position or neighboring chapter can still lead to the evidence. The reader then reasons with what it learned. **Do not fabricate** the vessel's owner, a delayed arrival, or a character who wasn't in the passage.

#### E. Marketing — preserve a webpage's claim without declaring it true

**Input: marketing/launch.html (115 UTF-8 bytes)**

~~~html
<section><h1>Autumn Launch</h1><a href="/products/shoes">See shoes</a><p>Sizes 8, 9 and 10 available.</p></section>
~~~

**Common record:** id fixture:marketing/launch.html; values include title/text Autumn Launch, original sentence about sizes, actual href /products/shoes and source bytes; location is marketing/launch.html bytes [0,115); relations are contained_in → folder:marketing and observed href → /products/shoes; proximity uses filename and literal text.

**Location:** retrieve the real landing page. **Relation:** follow the real product hyperlink. **Proximity:** find by “autumn shoes sizes”. **On touch:** the intelligence may qualify the explicit page claim as advertised_sizes=[8,9,10] with its source span. That does **not** prove current inventory; a separate inventory source would be required. Do not parse every other campaign to answer this question.

#### F. Excel/CSV and shoe sizes — ordinary table semantics, no code AST

**Input: sheets/shoes.csv (32 UTF-8 bytes)**

~~~csv
sku,size,stock
S01,8,12
S02,9,6
~~~

**Common record:** id fixture:sheets/shoes.csv; values are the actual column names plus rows [{sku:"S01",size:"8",stock:"12"},{sku:"S02",size:"9",stock:"6"}]; location is sheets/shoes.csv and each actual row number; relations include contained_in → folder:sheets and observed contains_row → row1/row2; proximity uses the filename, column labels and values.

**Location:** open row2. **Relation:** traverse the document-to-row containment. **Proximity:** “shoes size 9” can find this source. **No interpretation:** the original source does not state US/UK/EU size units; the SDK must not invent one. An XLSX adapter uses real workbook/sheet/cell metadata exactly the same way, not synthetic Python AST.

#### G. Opaque binary — zero content understanding, nonzero useful knowledge

**Input: bin/renderer.wasm — 8 exact bytes:** 00 61 73 6d 01 00 00 00. This is a header-only WebAssembly fixture, **not a working renderer**.

~~~yaml
---
type: Binary Asset
title: renderer.wasm
x_ukc:
  id: "fixture:bin/renderer.wasm"
  source: "bin/renderer.wasm"
  values:
    filename: renderer.wasm
    extension: .wasm
    byte_length: 8
  location: {path: "bin/renderer.wasm", byte_start: 0, byte_end: 8}
  relations:
    - {predicate: contained_in, target: "folder:bin"}
  proximity_input: "renderer.wasm"
---
The original 8 binary bytes are retained as an external source asset, not Markdown.
~~~

**Location:** exact path lookup finds the binary. **Relation:** traverse the actual parent folder. **Proximity:** filename/path similarity finds a candidate even without parsed content or embeddings. **On touch:** if inspecting binary internals becomes necessary, run a real binary-aware parser then; append actual observations under the original identity. The “wrong parser” is **not** a reason to discard the known filename, location or hierarchy.

### 3.4 Same stored values, different algorithms — implementation crosswalk

| Method | Recorded values it directly consumes | Example and behavior |
|---|---|---|
| Exact ID, path, glob, substring | Item identity, filename, extension, source path | Search for renderer.wasm or any .wasm file |
| Source/AST/DOM/document navigation | Recorded structural paths, native nodes, byte spans | Find Python total or the recipe Ingredients section |
| Graph BFS, neighbors, path algorithms | Native edges/links and IDs | Follow chapter2.md → chapter3.md; HTML href → dough |
| FTS/BM25 or exact lexical search | Available literal source text and labels | Find “harbor dawn” or “size 9” |
| Fuzzy/trigram/edit distance | Existing names, headings, paths and text | “flatbred” may lead to “Flatbread” |
| Token overlap/Jaccard | Source words, names and titles | Compare “flatbread flour” to both cooking sources |
| Vector cosine/distance | Independently computed vector and exact encoder-space descriptor | Find approximate wording when that vector exists |
| Geographic distance | Actual source coordinates, if provided | Find an approximate Woburn point or nearby places |
| Numeric/filter query | Recorded typed table cells and units | Shoe-size row and stock |
| Chronological/order navigation | Actual message, chapter, event or section order | Find previous message/chapter |
| On-touch intelligent investigation | Retrieved source evidence + current task context | Connect SOUP's current defect to a prior fix |

**Not every method is useful on every item, and not every index needs to exist before the item is usable.** The shared record carries *available* values; algorithms use them directly, computing their own search scores as needed. One method's intermediate output never becomes a prerequisite for constructing another method's knowledge. A missing embedding does **not** mean proximity cannot be searched with filenames or lexical overlap. A binary may have no content-derived semantic vector yet still support location, containment-graph and name-similarity search.

### 3.5 Executed characterization — seven real inputs and one shared record per source

The seven literal fixtures above were run locally through real Python ast.parse, html.parser.HTMLParser, csv.DictReader, direct Markdown heading/link parsing, source-byte SHA-256 and a **set-based Jaccard token search over captured filename/text**. Each record retained its original source key, full-file byte position, observed hierarchy/links and available proximity text. This was **not** a mocked LLM, fabricated edge, transformer embedding, semantic explanation or claim of full SDK implementation.

~~~json
{
  "tests": "PASS",
  "fixture_count": 7,
  "methods": {
    "location": ["fixture:bin/renderer.wasm"],
    "relation": ["fixture:books/chapter2.md"],
    "proximity_top3": [
      [0.2222222222222222, "fixture:web/recipe.html"],
      [0.16666666666666666, "fixture:docs/flatbread.md"],
      [0.0, "fixture:sheets/shoes.csv"]
    ]
  }
}
~~~

**What this output means:** Exact location found the opaque binary. The observed graph edge found the chapter pointing to Chapter 3. An approximate query “flatbread flour” returned both the webpage and the recipe, using the stored source/name values without converting one retrieval representation into another. The third, zero-score candidate is merely the tail of a three-item diagnostic; production search must not present it as meaningfully similar. All seven source-byte digests and end-exclusive byte bounds were checked. **What is not yet demonstrated:** complete OKF v0.3 serialization, full UKC-ID-1 canonical hash parity, Rust/TypeScript implementation, a persistent vector index or model-driven enrichment. Keep that boundary explicit.

**Reproduction:** Run the checked-in [seven-source characterization](conformance/probes/shared_record_examples.py) from any Python 3 standard-library environment:

~~~sh
python3 knowledge-positions/conformance/probes/shared_record_examples.py
~~~

It emits the original seven capture records and their source SHA-256 values, not just a green status. This runner is a **small language-independent behavior demonstration implemented in Python**, not the only permitted SDK implementation. Other-language authors must recreate its behavior using their native parsers; they MUST NOT be required to invoke Python in production. The separate [original Scratchpad OpenKC GPS probe](conformance/probes/original_openkc_gps_probe.py) still characterizes the actual historical OKF roundtrip.

### 3.6 On-touch enrichment and cold reconstruction — essential operational example

**Question: “What's wrong with SOUP?”** A cold intelligence need not be handed the answer, and ingestion need not have extracted every entity. It can locate a likely source using any available value; follow recorded source, containment or conversation references; and read the exact relevant section. An imperfect first hit can be sufficient if it supplies a useful place to look.

**A later question:** The intelligence searches again, retrieves a different source, and combines that evidence with the relevant source passage already present in its *current* working context. The newly seen relationship may be useful enough to record. **Ordinary in-context reasoning is not itself a mandatory persistent graph write.**

**Enrichment admission:** When evidence supports a reusable new relationship, add a qualified event/delta with subject, predicate, object, source spans, actor and admission status under the *same knowledge identity*. Do not pretend a model's proposal was directly parsed source metadata. Do not revisit or enrich unrelated files merely because one item was touched. The original sources remain authoritative.

**Cold-start proof:** Delete disposable graph/lexical/vector indexes; keep the original source snapshot, sessions and accepted evidence-backed discoveries that were preserved durably. Rebuild by cheap, deterministic re-ingestion. Ask the identical SOUP question in two isolated runs from the same durable snapshot. Compare supported findings, retrieved locations, cited original passages and unsupported claims. Separately compare against a genuinely unindexed/no-source-access baseline if useful. **A reproducible answer need not use identical words or exact-ranked first hits.** If an accepted discovery existed only in the erased derived database, a failed rebuild reveals a durability defect—not a mandate to enrich the entire corpus.

**The lifecycle is intentionally small:** record available values once → use any suitable retrieval method → follow source evidence → reason in context → optionally admit a qualified useful delta → discard and reconstruct indexes whenever convenient. No initial whole-corpus intelligence job, mandatory positional filling or method-to-method conversion.

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

An adapter MUST output **source description + observed records + observed edges + actual positions + native payload** and no invented relationships. An adapter's recognized field vocabulary is explicitly limited by its parser; missing semantic labels do not invalidate preserved raw evidence or make it undiscoverable. **When a query touches the item**, a separately governed enricher MAY recognize useful source-supported attributes or relations not extracted by the parser, adding only those qualified observations to the common record. Do not mistake a new useful label for a newly discovered source or an ingestion failure. An unsupported native format may be admitted as raw bytes/text with unknown structural fields, not silently mislabeled as a parsed AST.

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
| **UKC-16 PARSER AND ON-TOUCH ENRICHMENT** | Admit Woburn fixture through unchanged generic CommonMark parser: full text/AST survives, but postal code and coordinates are not individually labeled. Touch the same record for a location task and run a separately declared location-aware parser or evidence-grounded LLM enricher: append the recognized existing location facts and any justified relationships to **that same ID**; do not rewrite original text, require full-corpus enrichment, or imply the original parser extracted those fields. A native location parser may capture the same fields immediately. Repeat enrichment without duplication. |
| **UKC-17 GENERAL SOURCE EXAMPLES** | Run the seven-source reference characterization against actual language-native parsers and its recorded bytes: code, two webpages, cookbook, chapter, CSV, opaque binary. All seven preserve one source identity, exact source position, observed containment/links and available lexical proximity input; queries select from the same records, with zero mandatory model calls or vector generation. |
| **UKC-18 COLD CONTEXT AND RECOVERY** | Hold sources and accepted findings constant, clear all derived indexes, reconstruct, ask an evidence-backed question twice in independent cold runs; verify useful evidence/identity recovery without asserting word-for-word answer identity. Then show an on-touch qualified discovery changes future knowledge while untouched sources and records remain unchanged. |
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
