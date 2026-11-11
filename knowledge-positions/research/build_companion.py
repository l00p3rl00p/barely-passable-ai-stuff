"""Rebuild/verify the retained historical whole-paper companion; not the incremental maintenance path."""
import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path

import numpy as np
from knowledge_positions import KnowledgePositions

ROOT = Path(__file__).resolve().parent

class LexicalEncoder:
    def encode(self, text, normalize_embeddings=True):
        vec = np.zeros(512)
        for word in re.findall(r"\w+", text.lower()):
            h = hashlib.sha256(word.encode("utf-8")).digest()
            vec[int.from_bytes(h[:4], "big") % 512] += 1 if h[4] % 2 else -1
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load_source():
    spec = json.loads((ROOT / "evolving-knowledge-context.json").read_text())
    raw = (ROOT / "paper.md").read_bytes()
    if sha(raw) != spec["source_sha256"]:
        raise ValueError("Paper version differs from this historical companion; use the incremental maintenance path or intentionally regenerate/review this historical artifact")
    return spec, raw

def resolve(spec, raw, tag):
    node = next(n for n in spec["nodes"] if n["tag"] == tag)
    p = node["position"]
    span = raw[p["start_byte"]:p["end_byte"]]
    if sha(span) != node["content_hash"]:
        raise ValueError("Source span hash mismatch: " + tag)
    return span.decode("utf-8")

def build(semantic=False, output=None):
    spec, raw = load_source()
    model = "all-MiniLM-L6-v2" if semantic else "lexical-hash-512"
    k = KnowledgePositions(model, None if semantic else LexicalEncoder())
    output = Path(output or ROOT / ".ekc")
    output.mkdir(parents=True, exist_ok=True)
    db_path = output / "search.sqlite"
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as db:
        db.execute("CREATE VIRTUAL TABLE search USING fts5(text, content='')")
        db.execute("CREATE TABLE refs(rowid INTEGER PRIMARY KEY, node TEXT, tag TEXT)")
        for row, n in enumerate(spec["nodes"], 1):
            text = resolve(spec, raw, n["tag"])
            ident = k.add("paper.md", text, version=spec["source_sha256"],
                          position=n["position"], kind=n["kind"], node_id=n["id"])
            k.graph.nodes[ident].update(tag=n["tag"], heading=n["heading"],
                                        qualification=n["qualification"])
            if not semantic and not np.allclose(k.graph.nodes[ident]["vector"], n["vector"]):
                raise ValueError("Vector reproduction failed: " + n["tag"])
            db.execute("INSERT INTO search(rowid,text) VALUES (?,?)", (row, text))
            db.execute("INSERT INTO refs VALUES (?,?,?)", (row, ident, n["tag"]))
    for e in spec["edges"]:
        k.link(e["source"], e["target"], e["relation"], evidence=e["evidence"])
    k.save(output / "graph.json")
    reloaded = KnowledgePositions.load(output / "graph.json", None if semantic else LexicalEncoder())
    assert set(reloaded.graph.nodes) == set(k.graph.nodes)
    assert reloaded.graph.number_of_edges() == len(spec["edges"])
    print(f"Verified {len(spec['nodes'])} source spans; {len(spec['edges'])} relationships; model={model}")
    return k

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["build", "read", "search"])
    p.add_argument("value", nargs="?", default="")
    p.add_argument("--semantic", action="store_true")
    p.add_argument("--output", type=Path, default=ROOT / ".ekc")
    a = p.parse_args()
    if a.action == "build":
        build(a.semantic, a.output)
    elif a.action == "read":
        spec, raw = load_source()
        print(resolve(spec, raw, a.value))
    else:
        spec, raw = load_source()
        terms = re.findall(r"\w+", a.value)
        if not terms:
            raise SystemExit("Provide a search query")
        with sqlite3.connect(a.output / "search.sqlite") as db:
            hits = db.execute(
                "SELECT refs.tag,refs.node FROM search JOIN refs ON search.rowid=refs.rowid "
                "WHERE search MATCH ? ORDER BY bm25(search) LIMIT 10",
                (" OR ".join('"' + t + '"' for t in terms),)
            ).fetchall()
        print(json.dumps(hits, indent=2))
