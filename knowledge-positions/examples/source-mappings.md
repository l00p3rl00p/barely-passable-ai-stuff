### 3.3 Source → common OKF record → Location / Relation / Proximity: executable examples

**These examples illustrate the normative [capture contract](../contracts/common-record.md).** Historical snippets use the old x_ukc spelling; current interchange uses x-ukc. Examples do not establish additional requirements. An implementation in any language must recognize what the source actually supplies, copy useful values into *one* source-backed record, retain the original, and make its methods consume those common values. **The method is a reader, not the author of another knowledge representation.** Example identities prefixed fixture: below are human-readable test IDs; they are **not** a substitute for the canonical hash IDs defined in §4. Each x_ukc mapping below is an **OKF producer-defined extension**, not an upstream standard field. The actual asset bytes, SHA and native parser output must be preserved/referenced even when only selected fields are shown here.

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

