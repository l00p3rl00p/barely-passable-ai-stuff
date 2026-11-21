#!/usr/bin/env python3
"""UKC parser-fidelity probe: actual native parser outputs, not invented records.

Python 3 + markdown-it-py + PyYAML (original OpenKC dependencies).
The examples are literal fixed fixtures in the normative SDK specification.
Use --original-openkc-script /path/to/quatrus-scratchpad/.../openkc_etl.py
to also execute ORIGINAL Scratchpad conversion and round-trip in process.

This probe is not an LLM, vector encoder, WebAssembly parser, full UKC SDK,
or a claim of completed cross-language conformance.
"""
import argparse
import ast
import csv
import hashlib
from html.parser import HTMLParser
import importlib.util
import io
import json
from pathlib import Path
from markdown_it import MarkdownIt

FIXTURES = {
    "code/cart.py": b"from decimal import Decimal\n\ndef total(price, quantity):\n    return Decimal(price) * quantity\n",
    "web/recipe.html": b'<html><body><h1>Flatbread</h1><a href="/recipes/dough">Dough method</a><p>Mix flour with water.</p></body></html>',
    "docs/flatbread.md": b"# Flatbread\n## Ingredients\n- 2 cups flour\n- 1 cup water\n## Instructions\nMix flour and water.\n",
    "books/chapter2.md": b"# Chapter 2: The Harbor\nSee [Chapter 3](chapter3.md).\nThe boat reached the harbor at dawn.\n",
    "marketing/launch.html": b'<section><h1>Autumn Launch</h1><a href="/products/shoes">See shoes</a><p>Sizes 8, 9 and 10 available.</p></section>',
    "sheets/shoes.csv": b"sku,size,stock\nS01,8,12\nS02,9,6\n",
    "bin/renderer.wasm": bytes.fromhex("0061736d01000000"),
}

# Mirrors the exact token fields used by the original OpenKC script.
def token_fields(t):
    return dict(type=t.type, tag=t.tag, attrs=t.attrs, map=t.map,
                nesting=t.nesting, level=t.level,
                children=[token_fields(c) for c in t.children or []],
                content=t.content, markup=t.markup, info=t.info, meta=t.meta,
                block=t.block, hidden=t.hidden)


class ParserEvents(HTMLParser):
    def __init__(self):
        super().__init__()
        self.events = []

    def handle_starttag(self, tag, attrs):
        self.events.append(["starttag", tag, attrs, list(self.getpos())])

    def handle_endtag(self, tag):
        self.events.append(["endtag", tag, list(self.getpos())])

    def handle_data(self, data):
        self.events.append(["data", data, list(self.getpos())])


def read_original(path):
    spec = importlib.util.spec_from_file_location("openkc_original", path)
    if spec is None or spec.loader is None:
        raise ValueError("Original OpenKC code could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(original_script=None):
    output = {}
    original = read_original(original_script) if original_script else None
    for path, raw in FIXTURES.items():
        name = path.rsplit("/", 1)[-1]
        record = {
            "source": path,
            "filename_from_source_path": name,
            "source_bytes": len(raw),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "native_parser": None,
            "native_output": None,
            "origin_annotations": {
                "filename": "filesystem/source path",
                "source_bytes": "original byte length",
                "source_sha256": "original bytes SHA-256",
            },
        }
        if path.endswith(".py"):
            tree = ast.parse(raw.decode("utf-8"))
            record["native_parser"] = "CPython ast.parse"
            record["native_output"] = ast.dump(tree, include_attributes=True, indent=2)
            imp, fn = tree.body
            assert isinstance(imp, ast.ImportFrom) and imp.module == "decimal"
            assert (imp.lineno, imp.col_offset, imp.end_lineno, imp.end_col_offset) == (1, 0, 1, 27)
            assert isinstance(fn, ast.FunctionDef) and fn.name == "total"
            assert (fn.lineno, fn.col_offset, fn.end_lineno, fn.end_col_offset) == (3, 0, 4, 36)
        elif path.endswith(".html"):
            parser = ParserEvents()
            parser.feed(raw.decode("utf-8"))
            record["native_parser"] = "Python html.parser.HTMLParser (event stream, not DOM)"
            record["native_output"] = parser.events
            hrefs = [attr[1] for event in parser.events if event[0] == "starttag"
                     for attr in event[2] if attr[0] == "href"]
            if path.startswith("web/"):
                assert hrefs == ["/recipes/dough"]
                assert ["data", "Flatbread", [1, 16]] in parser.events
            else:
                assert hrefs == ["/products/shoes"]
                assert ["data", "Sizes 8, 9 and 10 available.", [1, 73]] in parser.events
        elif path.endswith(".md"):
            tokens = MarkdownIt("commonmark", {"html": True}).parse(raw.decode("utf-8"))
            record["native_parser"] = "markdown-it-py CommonMark"
            record["native_output"] = [token_fields(t) for t in tokens]
            if path.startswith("docs/"):
                assert len(tokens) == 24
                assert sum(t.type == "inline" for t in tokens) == 6
                assert [(t.type, t.map, t.content) for t in tokens if t.type == "inline"] == [
                    ("inline", [0, 1], "Flatbread"),
                    ("inline", [1, 2], "Ingredients"),
                    ("inline", [2, 3], "2 cups flour"),
                    ("inline", [3, 4], "1 cup water"),
                    ("inline", [4, 5], "Instructions"),
                    ("inline", [5, 6], "Mix flour and water."),
                ]
            else:
                assert len(tokens) == 6
                assert sum(t.type == "inline" for t in tokens) == 2
                chapter = [t for t in tokens if t.type == "inline"][1]
                assert chapter.map == [1, 3]
                assert [(c.type, c.attrs) for c in chapter.children if c.type == "link_open"] == [
                    ("link_open", {"href": "chapter3.md"})
                ]
                assert [c.type for c in chapter.children if c.type == "softbreak"] == ["softbreak"]
            if original:
                original_ast = original.ast_from_bytes(raw, path)
                assert original_ast["tokens"] == record["native_output"]
                note = original.ast_to_okf(original_ast)
                recovered = original.okf_to_ast(note)
                assert recovered == original_ast
                record["original_openkc_ast_okf_roundtrip"] = "PASS"
        elif path.endswith(".csv"):
            reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
            rows = list(reader)
            record["native_parser"] = "Python csv.DictReader"
            record["native_output"] = {"fieldnames": reader.fieldnames, "rows": rows}
            assert reader.fieldnames == ["sku", "size", "stock"]
            assert rows == [{"sku": "S01", "size": "8", "stock": "12"},
                            {"sku": "S02", "size": "9", "stock": "6"}]
        else:
            record["native_parser"] = "none (filesystem/source metadata only)"
            record["native_output"] = {
                "filename": name,
                "extension": Path(path).suffix,
                "byte_length": len(raw),
                "header_hex": raw.hex(),
            }
            assert len(raw) == 8 and raw == bytes.fromhex("0061736d01000000")
        output[path] = record
    return {
        "status": "PASS",
        "fixture_count": len(FIXTURES),
        "actual_source_bytes_checked": True,
        "original_openkc_executed": bool(original),
        "parser_outputs": output,
        "note": "Source path is not a parser token; Markdown maps are line ranges; HTMLParser outputs events; CSV cell values remain strings.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original-openkc-script", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    if args.original_openkc_script and not args.original_openkc_script.is_file():
        p.error("The exact original OpenKC script is unavailable")
    result = run(args.original_openkc_script)
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
