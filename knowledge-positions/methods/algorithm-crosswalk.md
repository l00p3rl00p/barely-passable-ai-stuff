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

**This table lists algorithms over the same knowledge, not alternative knowledge representations or separate ingestion tracks.** A search result through any connected method resolves a shared record ID; the investigator can next use any other method whose required values are present, reusing the same source, relationships and provenance. For example, a lexical match can feed a graph-neighbor traversal, then a numeric ranking, then an exact source read. Intermediate counts or rankings can themselves be sufficient answers; full content hydration is not mandatory.

**Not every method is useful on every item, and not every index needs to exist before the item is usable.** The shared record carries *available* values; algorithms use them directly, computing their own search scores as needed. One method's intermediate output never becomes a prerequisite for constructing another method's knowledge. A missing embedding does **not** mean proximity cannot be searched with filenames or lexical overlap. A binary may have no content-derived semantic vector yet still support location, containment-graph and name-similarity search.

