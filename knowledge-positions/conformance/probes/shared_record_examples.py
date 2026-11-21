#!/usr/bin/env python3
"""UKC worked-example characterization: real parsers and source bytes, no mocks.

This is an executable source-to-record proof for the examples in
knowledge-positions/unified-knowledge-context.md section 3.3.
It is NOT a complete UKC SDK, OKF validator, LLM enricher or vector encoder.
Runs with the Python standard library only.
"""
import ast
import csv
import hashlib
import io
import json
import re
from html.parser import HTMLParser
from pathlib import Path

FIXTURES = {
    "code/cart.py": "from decimal import Decimal\n\ndef total(price, quantity):\n    return Decimal(price) * quantity\n",
    "web/recipe.html": '<html><body><h1>Flatbread</h1><a href="/recipes/dough">Dough method</a><p>Mix flour with water.</p></body></html>',
    "docs/flatbread.md": "# Flatbread\n## Ingredients\n- 2 cups flour\n- 1 cup water\n## Instructions\nMix flour and water.\n",
    "books/chapter2.md": "# Chapter 2: The Harbor\nSee [Chapter 3](chapter3.md).\nThe boat reached the harbor at dawn.\n",
    "marketing/launch.html": '<section><h1>Autumn Launch</h1><a href="/products/shoes">See shoes</a><p>Sizes 8, 9 and 10 available.</p></section>',
    "sheets/shoes.csv": "sku,size,stock\nS01,8,12\nS02,9,6\n",
    "bin/renderer.wasm": b"\x00asm\x01\x00\x00\x00",
}

class ObservedHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for key, value in attrs:
            if tag == "a" and key == "href":
                self.links.append(value)

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

def capture(path, payload):
    raw = payload if isinstance(payload, bytes) else payload.encode("utf-8")
    name = Path(path).name
    rec = {
        "id": "fixture:" + path,
        "source": path,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "values": {"filename": name, "extension": Path(path).suffix, "byte_length": len(raw)},
        "location": {"path": path, "byte_start": 0, "byte_end": len(raw)},
        "relations": [{"predicate": "contained_in", "target": "folder:" + str(Path(path).parent)}],
        "proximity_input": name,
    }
    if path.endswith(".py"):
        tree = ast.parse(raw.decode("utf-8"))
        rec["values"]["functions"] = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
        rec["values"]["imports"] = [n.module for n in tree.body if isinstance(n, ast.ImportFrom)]
        rec["relations"] += [{"predicate": "imports", "target": n.module} for n in tree.body if isinstance(n, ast.ImportFrom)]
        rec["proximity_input"] += " " + raw.decode("utf-8")
    elif path.endswith(".html"):
        parser = ObservedHTML()
        parser.feed(raw.decode("utf-8"))
        rec["values"].update(tags=parser.tags, links=parser.links, text=parser.text)
        rec["relations"] += [{"predicate": "href", "target": link} for link in parser.links]
        rec["proximity_input"] += " " + " ".join(parser.text)
    elif path.endswith(".md"):
        text = raw.decode("utf-8")
        headings = re.findall(r"^#{1,6} (.+)$", text, re.M)
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
        rec["values"].update(headings=headings, links=links)
        rec["relations"] += [{"predicate": "href", "target": link} for link in links]
        rec["proximity_input"] += " " + text
    elif path.endswith(".csv"):
        text = raw.decode("utf-8")
        rows = list(csv.DictReader(io.StringIO(text)))
        rec["values"]["rows"] = rows
        rec["relations"] += [{"predicate": "contains_row", "target": path + "#row" + str(i+1)} for i in range(len(rows))]
        rec["proximity_input"] += " " + text
    return rec

def token_set(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def characterize():
    records = [capture(path, data) for path, data in FIXTURES.items()]
    by_id = {r["id"]: r for r in records}

    def locate(fragment):
        return [r["id"] for r in records if fragment.lower() in r["location"]["path"].lower()]

    def relation(target):
        return [r["id"] for r in records if any(target in edge["target"] for edge in r["relations"])]

    def proximity(query):
        terms = token_set(query)
        return sorted([
            [len(terms & token_set(r["proximity_input"])) / len(terms | token_set(r["proximity_input"])), r["id"]]
            for r in records
        ], reverse=True)

    assert len(records) == 7
    assert locate("renderer.wasm") == ["fixture:bin/renderer.wasm"]
    assert relation("/recipes/dough") == ["fixture:web/recipe.html"]
    assert relation("chapter3.md") == ["fixture:books/chapter2.md"]
    assert by_id["fixture:code/cart.py"]["values"]["functions"] == ["total"]
    assert by_id["fixture:marketing/launch.html"]["values"]["links"] == ["/products/shoes"]
    assert by_id["fixture:sheets/shoes.csv"]["values"]["rows"][1]["size"] == "9"
    assert proximity("flatbread flour")[0][1] == "fixture:web/recipe.html"

    for path, source in FIXTURES.items():
        raw = source if isinstance(source, bytes) else source.encode("utf-8")
        record = by_id["fixture:" + path]
        assert record["source_sha256"] == hashlib.sha256(raw).hexdigest()
        assert record["location"]["byte_end"] == len(raw)
        assert len(record["relations"]) >= 1
        assert record["proximity_input"]

    return {
        "tests": "PASS",
        "fixture_count": len(records),
        "methods": {
            "location": locate("renderer.wasm"),
            "relation": relation("chapter3.md"),
            "proximity_top3": proximity("flatbread flour")[:3],
        },
        "records": records,
        "evidence_scope": "Real stdlib parsers and byte hashes; no OKF serializer, LLM, vector embedding or persistence",
    }

if __name__ == "__main__":
    print(json.dumps(characterize(), ensure_ascii=False, indent=2))
