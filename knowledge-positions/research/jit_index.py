"""Current section-scoped JIT navigation index for the evolving research paper.

This is a derived navigation artifact, not a second theory. It indexes stable EKC
sections independently so unchanged sections retain identity and optional vector
state when another section changes.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
PAPER = ROOT / "paper.md"
INDEX = ROOT / "jit-index.json"
HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s+\[(EKC:\d+)\]\s*$")
WORDS = re.compile(r"[a-z0-9][a-z0-9_-]{2,}")
STOP = {
    "the","and","that","this","with","from","for","are","was","were","into","not",
    "but","can","may","its","their","they","our","has","have","had","only","than",
    "when","what","which","while","where","how","use","uses","using","used","one",
    "two","three","more","also","does","each","such","these","those","been","being",
    "should","would","could","will","must","all","any","per","through","without"
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def parse_sections(raw):
    lines = raw.splitlines(keepends=True)
    out, current, offset = [], None, 0
    for line_no, raw_line in enumerate(lines, 1):
        line = raw_line.decode("utf-8").rstrip("\r\n")
        match = HEADING.match(line)
        if match:
            if current is not None:
                current["end_byte"] = offset
                current["end_line"] = line_no - 1
                out.append(current)
            current = {
                "level": len(match.group(1)),
                "heading": match.group(2),
                "tag": match.group(3),
                "start_byte": offset,
                "start_line": line_no,
            }
        offset += len(raw_line)
    if current is not None:
        current["end_byte"] = len(raw)
        current["end_line"] = len(lines)
        out.append(current)
    return out

def term_map(text):
    counts = Counter(w for w in WORDS.findall(text.lower()) if w not in STOP)
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:24])

def lexical_hash_vector(text):
    """Deterministic 512-d fallback used elsewhere in Knowledge Positions."""
    v = np.zeros(512)
    for word in re.findall(r"\w+", text.lower()):
        h = hashlib.sha256(word.encode()).digest()
        v[int.from_bytes(h[:4], "big") % 512] += 1 if h[4] % 2 else -1
    norm = np.linalg.norm(v)
    return (v / norm if norm else v).tolist()

def build():
    raw = PAPER.read_bytes()
    old = {}
    if INDEX.exists():
        prior = json.loads(INDEX.read_text(encoding="utf-8"))
        old = {n["id"]: n for n in prior.get("nodes", [])}
    nodes, edges, parent = [], [], None
    sections = parse_sections(raw)
    for i, section in enumerate(sections):
        span = raw[section["start_byte"]:section["end_byte"]]
        node_id = "paper.md#" + section["tag"]
        digest = sha(span)
        prior = old.get(node_id, {})
        same = prior.get("source_version_sha256") == digest
        node = {
            "id": node_id,
            "tag": section["tag"],
            "heading": section["heading"],
            "heading_level": section["level"],
            "source": "paper.md",
            "source_position": {
                "start_byte": section["start_byte"],
                "end_byte": section["end_byte"],
                "start_line": section["start_line"],
                "end_line": section["end_line"],
                "unit": "utf8_byte",
            },
            "source_version_scope": "section",
            "source_version_sha256": digest,
            "terms": prior.get("terms") if same and prior.get("terms") else term_map(span.decode("utf-8")),
            "vector": prior.get("vector") if same and prior.get("vector") is not None
                      else lexical_hash_vector(span.decode("utf-8")),
            "vector_status": "known",
            "embedding_model": prior.get("embedding_model", "lexical-hash-512")
                               if same and prior.get("vector") is not None
                               else "lexical-hash-512",
        }
        nodes.append(node)
        if i:
            edges.append({"source": nodes[i-1]["id"], "target": node_id,
                          "relation": "next_section", "qualification": "manuscript_structure"})
        if section["level"] == 2:
            parent = node_id
        elif parent:
            edges.append({"source": node_id, "target": parent,
                          "relation": "part_of", "qualification": "manuscript_heading_structure"})
    payload = {
        "schema_version": 1,
        "authority": "paper.md",
        "maintenance": "section_scoped_incremental",
        "notes": "Derived JIT navigation index. Stable EKC identity; exact section spans/hashes; deterministic lexical-hash-512 fallback vectors when no semantic encoder is used.",
        "paper_sha256": sha(raw),
        "nodes": nodes,
        "edges": edges,
    }
    INDEX.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload

def load_verified():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    raw = PAPER.read_bytes()
    for node in data["nodes"]:
        p = node["source_position"]
        span = raw[p["start_byte"]:p["end_byte"]]
        if sha(span) != node["source_version_sha256"]:
            raise ValueError("Stale JIT position/hash: " + node["tag"])
        first = span.decode("utf-8").splitlines()[0]
        if node["tag"] not in first:
            raise ValueError("JIT span does not begin at expected EKC section: " + node["tag"])
    return data, raw

def search(query, limit=7):
    data, _ = load_verified()
    q = [w for w in WORDS.findall(query.lower()) if w not in STOP]
    scored = []
    for node in data["nodes"]:
        score = sum(node["terms"].get(w, 0) for w in q)
        heading = node["heading"].lower()
        score += 4 * sum(1 for w in q if w in heading)
        if score:
            scored.append((score, node["tag"], node["heading"], node["id"]))
    return sorted(scored, key=lambda x: (-x[0], x[1]))[:limit]

def read(tag):
    data, raw = load_verified()
    node = next(n for n in data["nodes"] if n["tag"] == tag)
    p = node["source_position"]
    return raw[p["start_byte"]:p["end_byte"]].decode("utf-8")

def neighbors(tag):
    data, _ = load_verified()
    node_id = "paper.md#" + tag
    return [e for e in data["edges"] if e["source"] == node_id or e["target"] == node_id]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["build","verify","search","read","neighbors"])
    p.add_argument("value", nargs="?", default="")
    a = p.parse_args()
    if a.action == "build":
        result = build()
        print(f"{len(result['nodes'])} sections; {len(result['edges'])} structural relationships")
    elif a.action == "verify":
        result, _ = load_verified()
        print(f"verified {len(result['nodes'])} section-scoped JIT nodes")
    elif a.action == "search":
        print(json.dumps(search(a.value), indent=2))
    elif a.action == "read":
        print(read(a.value))
    else:
        print(json.dumps(neighbors(a.value), indent=2))
