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

**Reproduction:** Run the checked-in [seven-source characterization](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/conformance/probes/shared_record_examples.py) from any Python 3 standard-library environment:

~~~sh
python3 knowledge-positions/conformance/probes/shared_record_examples.py
~~~

It emits the original seven capture records and their source SHA-256 values, not just a green status. This runner is a **small language-independent behavior demonstration implemented in Python**, not the only permitted SDK implementation. Other-language authors must recreate its behavior using their native parsers; they MUST NOT be required to invoke Python in production. The separate [original Scratchpad OpenKC GPS probe](https://github.com/l00p3rl00p/barely-passable-ai-stuff/blob/main/knowledge-positions/conformance/probes/original_openkc_gps_probe.py) still characterizes the actual historical OKF roundtrip.

