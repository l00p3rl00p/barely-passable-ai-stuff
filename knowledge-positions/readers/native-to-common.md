### 3.2.2 Recovered native-to-common translation contract (mandatory; from working code and original research)

**Do not stop at "use OKF."** Every declared reader/parser MUST publish its field crosswalk into the same UKC common-record vocabulary **before** advertising that reader as supported. The crosswalk is implemented at the existing input boundary: no per-search retranslation, no AST→graph→vector knowledge pipeline, no mandatory global ontology. Preserve **all native fields** even when only a subset is directly indexed. A missing recognized field is represented as unsupported or unknown, never invented.

The following is the binding vocabulary for all SDK implementations; the field paths are under producer-defined x_ukc (OKF itself standardizes only its own frontmatter fields and extension convention). **These are named semantic field families in one logical record, not additional objects or completion slots.**

| Common x_ukc field | Native source that supplies it | Invariant |
|---|---|---|
| id, source.authority, source.key, source.version | Source resolver, filesystem/provider/repository, content hash | One identity for all search methods; source route and current access are separate |
| kind, values, native | Exact native reader/parser output, including unknown keys | Retain original casing, types, structure and payload; never discard unrecognized fields |
| values.name / title / typed attributes | Native filename, explicit heading, symbol, column name, literal metadata | Record provenance per field; file name from filesystem ≠ AST-produced name |
| location.source_locator, source_version, spans | Filesystem/URI/provider, native span or qualified locator | Version and coordinate units mandatory; original source recoverable when access permits |
| location.item_path, parent_path, sibling_index, depth | Actual AST, DOM, document tree, workbook sheet/cell or native hierarchy | Structural position is distinct from external source location; **do not invent a tree** |
| relations[].{subject,predicate,target,direction,origin,evidence} | Actual parser child/parent, DOM href, imports, document links, filesystem containment, qualified delta | Exact direction and observed-vs-proposed status; native edges are graph-ready |
| proximity inputs | Existing names, literals, content, coordinates or vectors with declared encoder | Lexical/fuzzy similarity can work without an embedding; computed vector is a derived indexable value, not new source truth |
| evidence / native original | Original bytes or accessible hash-addressed original, parser version, source-hash and span hashes | The full parse/source can be checked and reconstructed; illustrative excerpts are never substitutes |

**The exact inherited OpenKC field crosswalk (from Scratchpad MAPPING.md and actual openkc_etl.py):**

| Native input | Actual historic destination | UKC common-record field / required preservation |
|---|---|---|
| Original source filename/path | AST path; OKF openkc_id path suffix | source.key; native.path; filename in values when supplied |
| Actual original bytes | AST source_base64; OKF note body | native source reference + source bytes and source hash; exact byte roundtrip |
| hashlib SHA-256 over raw bytes | AST source_sha256; OKF openkc_source_sha256 | source.version/evidence.source_sha256; preserve original field |
| Real CommonMark tokens | AST tokens copied wholesale into openkc_ast | native.parser_output; real hierarchy, values and token attributes; preserve the entire AST |
| CommonMark token map | token.map inside embedded AST | parser-native location spans **in source line units** (zero-based, end-exclusive); not fabricated byte offsets |
| Heading from heading_open followed by inline text | OKF title only when heading exists | values.title with origin=source_heading; do not generate a source title without evidence |
| YANP conversion date, author, status | YANP-only projection metadata | generated-projection fields **not source facts**; distinguish on import/export |

**Mandatory parser-specific adapters.** Map *what was actually returned*, not what a different parser might have returned:

| Reader | Native observation → UKC field(s) | Important negative proof |
|---|---|---|
| Python ast.parse | Module.body, FunctionDef.name, ImportFrom.module, lineno/col_offset/end positions → native + values, hierarchy, relations and native-coordinate location | Python AST does not return the filesystem filename; its UTF-8 column semantics are not CommonMark line maps |
| markdown-it-py CommonMark | full token attributes and children, heading_open/inline, link_open.attrs.href, map → native + actual hierarchy/link relations + source-line location | A recipe ingredient is an inline text token, **not** a parser-extracted numeric ingredient entity |
| Python html.parser.HTMLParser | handle_starttag, attrs, handle_data, getpos → native event stream + named attributes/observed href + event position | HTMLParser **does not produce a DOM tree**; a separate DOM parser may, but must declare which produced the hierarchy |
| csv.DictReader | fieldnames, rows, literal strings → native table and values; source file/row sequence → location and containment | The row values remain strings unless an explicit, qualified schema/adapter converts types; size units are unknown |
| Filesystem/no content parser | filename, extension, parent, path, byte count and actual content digest → values + source locator + containment edge + literal proximity | An opaque .wasm is discoverable before any WebAssembly parse; content semantics are **not** claimed |
| JSON/XML/TS/Rust/Word/Excel/etc. | Relevant native parser's real fields/coordinates mapped into the same common vocabulary | An unimplemented reader MUST report not_supported; naming an adapter is not evidence that it works |

**The parser’s actual output is the test oracle.** For every adapter: store original input bytes and parser identity/version; keep real original token/AST/event/row output; declare each copying/normalization rule and its coordinate basis; list native fields it intentionally exposes for direct lookup; verify lossless round-trip including all fields it does **not** expose directly. Verify representative relations and text/filename similarity against that *same* record. Cross-language conformity is evaluated against shared canonical input/expected-field fixtures, not vaguely similar examples.

**Do not over-claim compatibility with the existing Python library.** Current knowledge_positions.py is a working **NetworkX MultiDiGraph** implementation with add(source,text,version,position), source-hashed node identity, link, graph views, source location methods, optional/deferred vector, and an enrichment budget. Its **existing node hash differs from proposed UKC-ID-1**. Its add() requires nonempty text; opaque binary admission as such is an SDK requirement, not yet a demonstrated method on that existing class. Its nodes store text hashes and graph/position data, **not** an automatic full universal OKF record. The historic OpenKC script separately demonstrated exact AST/OKF round-trip for CommonMark. The shared SDK maps and coordinates these proven capabilities; do not falsely certify the legacy library as a complete UKC/1 implementation.

