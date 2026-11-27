## 1. Purpose, sources of authority and normative language

UKC is an executable-language-independent SDK specification. Python, Rust, TypeScript, JavaScript, Java, Go, C/C++, C#, Swift, WASM or any other executable environment can implement it. A language, database, parser, framework, network service, model provider or UI is never an intrinsic requirement.

**MUST**, **MUST NOT**, **SHOULD** and **MAY** are normative. The first law and all Core requirements are mandatory. Advertised optional functions must pass their relevant conformance tests. Unsupported features must be reported, not faked.

The [SDF guide](../SDF/README.md) is the starting point. The linked UKC contracts own normative requirements; the following sources provide research evidence, optional profiles or the external interchange standard. Read them when needed, not as a prerequisite for building a kit:
- [Canonical JITK paper](../research/paper.md): origin, principle and the original cold-context GPS experiment.
- [Knowledge Asset Evolution v1.6.3](../Knowledge-Asset-Evolution-Spec-v1.6.3.md): portable OKF-compatible ownership, lifecycle, schema governance and durable events, when those profiles are selected.
- [Knowledge Graph Relationships and Enrichment](../Knowledge_Graph_Relationships_and_Enrichment.md): observed versus qualified discovered relations and provenance.
- [OpenKC architecture](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/ARCHITECTURE.md), [deterministic mapping](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/MAPPING.md), [working code](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/openkc_etl.py), [proof](https://github.com/l00p3rl00p/quatrus-scratchpad/blob/main/experiments/openkc-ast-okf-yanp/EVIDENCE.md).
- [Original GPS experiment and replay](../research/EXPERIMENT.md).
- [Official upstream OKF specification](https://github.com/open-knowledge-format/open-knowledge-format/blob/527e81aff55992be21507e97004286789126f88c/SPEC.md). This is the current upstream **OKF v0.3** specification; the previous GoogleCloudPlatform repository contains deprecated v0.2. UKC keys are **producer-defined extensions**, not fields standardized by OKF itself.

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

**Experiment B — original GPS: multiple retrieval methods use the same knowledge ID.** The published [gps.py](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/examples/gps/gps.py) admits each source passage once, with its original source version and exact byte position, then uses the returned identity for sequence edges and the lexical-search reference table:

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

The real read function additionally verifies the original source version and span content hash. The [preserved GPS replay](../research/EXPERIMENT.md) verified **28 nodes, 42 edges (27 sequence, 15 lexical-shared-term), four requested source passages and exact source-backed reads**. Its hash-based vector offered cheap imperfect leads rather than new facts.

**What the experiments prove together, and what they do not:** Scratchpad proved **literal source/AST/OKF preservation, deterministic structural graph projection and verified retrieval**; it did not prove a complete vector SDK over OKF. GPS proved **same-ID lexical/vector/graph/source navigation**; it did not use OKF. The Tree-sitter-only proof independently parsed the same source corpus but was not a tested bridge from Tree-sitter to all these methods. This SDK specifies their **combined language-neutral invariant**, which still requires unified conformance testing before claiming the entire UKC/1 SDK is implemented.

**Normative interpretation:** Preserve each already-known native value **once**, directly alongside the original information in the common OKF-compatible record; deterministically materialize indexes or graph edge rows from that same record if a chosen search engine requires them. Do **not** convert an AST into a different knowledge graph interpretation, then convert that into vector knowledge. **Physical indexing is allowed; separate interpretations and method-to-method conversion are forbidden.** Unknown facts remain unknown. Any separately computed new value retains its origin and same record identity.

### 1.2 Woburn GPS characterization — actual original code, not a hypothetical example

The following literal Woburn fixture is reproduced inline. The separately referenced `conformance/fixtures/woburn-gps.md` is **not present on `main`**; the inline text is the available source for this illustrative example:

~~~markdown
# Woburn, Massachusetts
- Postal code: 01801
- Latitude (illustrative city point): 42.479261
- Longitude (illustrative city point): -71.152278
~~~

The coordinates identify **an illustrative point**, not an exact universal location of the entire city. An earlier characterization used the original Scratchpad `openkc_etl.py` functions (`ast_from_bytes`, `ast_to_okf`, `split_note`, `okf_to_ast`), not a substitute translation. Its associated `conformance/probes/original_openkc_gps_probe.py` runner is **not present on `main`**, so the observation cannot currently be rerun from this SDK checkout.

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

**Reproduction status:** No executable command is supplied here because the referenced probe is not checked into this branch. Reproduction requires an available probe or equivalent independently verified run against the unchanged original Scratchpad code. The results above are historical characterization claims, not current executable proof.

Do **not** report this characterization as a completed UKC SDK conformance run. It identifies the missing SDK behavior with an actual original implementation and a new literal source fixture. A future implementation must pass a separate assertion that its declared field adapter writes and retrieves those labeled values from the same common record, not merely from a reparse of the raw source.

