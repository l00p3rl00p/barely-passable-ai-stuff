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

