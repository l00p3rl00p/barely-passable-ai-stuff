# Knowledge Positions examples and expected results

The examples below already exist. This page is a reading order and an output-comparison index; it does **not** add fixtures, implementations, or new claims of execution.

## Start with one real, runnable example

**GPS experiment: cold-context retrieval** — [instructions, commands, and source-backed outcomes](gps/README.md).

The existing example includes:

```bash
python gps.py build --source source.txt
python gps.py search "SDK codebase"
# Copy a node ID from the current search output:
python gps.py neighbors <NODE_ID>
python gps.py read <NODE_ID> --source source.txt
```

[Original GPS experiment and replay evidence](../research/EXPERIMENT.md) describes the observed 28 nodes, 42 edges and four requested source passages. This is a demonstration of the existing Python implementation, not proof of full UKC/1 conformance.

## Seven source-to-result recipes

The [existing source-to-common-record examples](source-mappings.md) contain input data, preserved values and expected Location / Relation / Proximity access for each example.

| Choose an existing example | Input | What the existing example shows |
|---|---|---|
| **A. Code** | `code/cart.py` | Real AST names, import, source span and observed relationships |
| **B. Webpage** | `web/recipe.html` | Preserved HTML, text and observed hyperlink |
| **C. Cooking** | `docs/flatbread.md` | Headings, section hierarchy, literal recipe text |
| **D. Writing a book** | `books/chapter2.md` | Original chapter and its actual `chapter3.md` link |
| **E. Marketing** | `marketing/launch.html` | Literal claims retained without treating them as verified |
| **F. CSV / shoe sizes** | `sheets/shoes.csv` | Exact table cells and row positions; strings remain strings |
| **G. Opaque binary** | `bin/renderer.wasm` | Discoverability from name, hash and location without content interpretation |

## Compare with the recorded result

[**Seven-source characterization and recorded output**](../conformance/characterization.md) contains the existing JSON result:

```json
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
```

This is the **previously recorded characterization output**, not a result newly executed or certified from this index. The characterization page explicitly records that its referenced runners are missing from `main`; do not use the JSON as proof of current executable UKC/1 conformance.

## Inspect what was actually parsed

- [Native parser observations](../readers/native-parser-fidelity.md) — selected real AST, HTML event, Markdown token and CSV observations, alongside source/adapter distinctions.
- [Native-to-common field mapping](../readers/native-to-common.md) — the recorded values and their destinations in the shared record.
- [Algorithm crosswalk](../methods/algorithm-crosswalk.md) — which recorded values each retrieval method consumes.
- [Conformance requirements](../conformance/requirements.md) — how a complete implementation must be validated.
