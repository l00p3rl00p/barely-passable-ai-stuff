### 3.2.1 Parser fidelity is mandatory: raw input → native parser output → copied OKF values

**NEVER skip the middle column.** A source example followed by hand-written metadata is not an executable parser specification. An SDK author MUST see (1) the exact source bytes, (2) the actual selected parser and its raw returned values, (3) the mechanical field-to-field mapping into the ONE shared OKF-compatible record, and (4) which retrieval methods consume those fields. This section records a real local parser audit of the seven examples below. It is **not** a claim that the original OpenKC script itself implements every adapter. The complete native parser-output snapshot from this audit is independently saved as an artifact; any implementation MUST be able to regenerate its own test evidence from the literal fixture bytes.

**Evidence status:** The parser observations below record an earlier local audit, but the referenced `conformance/probes/native_parser_fidelity.py` runner is **not present on `main`**. The audit is therefore not reproducible from this SDK checkout as written. Treat the observations as recorded characterization, not a passing current SDK conformance run. The required future test remains: replay the literal inputs with the declared native parsers and preserve their full raw outputs, parser versions, source bytes, and crosswalk evidence.

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

