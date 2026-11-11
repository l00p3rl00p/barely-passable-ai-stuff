"""Capture reviewed conversational knowledge using the actual Knowledge Positions library.

Run with --home pointing to YOUR provider folder. The default new graph uses
explicit lexical-hash-512 vectors, not semantic embeddings. No chat API is assumed.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from knowledge_positions import KnowledgePositions


class LexicalEncoder:
    """Same deterministic encoder as the existing GPT knowledge graph."""
    def encode(self, text, normalize_embeddings=True):
        v = np.zeros(512)
        for word in re.findall(r"\w+", text.lower()):
            h = hashlib.sha256(word.encode()).digest()
            v[int.from_bytes(h[:4], "big") % 512] += 1 if h[4] % 2 else -1
        norm = np.linalg.norm(v)
        return v / norm if norm else v


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(home):
    k = KnowledgePositions.load(home / "graph.json", LexicalEncoder())
    if k.model_name != "lexical-hash-512":
        raise ValueError("This CLI uses lexical-hash-512; use the library with the graph's actual encoder for other models")
    return k


def verify(home, k):
    """Verify record bytes, exact spans and known vectors; unknown is valid."""
    for n, d in k.graph.nodes(data=True):
        path = (home / d["source"]).resolve()
        if not path.is_relative_to((home / "sources").resolve()):
            raise ValueError("Source outside registry: " + n)
        raw = path.read_bytes()
        pos = d["position"]
        span = raw[pos["start_byte"]:pos["end_byte"]]
        if digest(raw) != d["version"] or digest(span) != d["content_hash"]:
            raise ValueError("Source/version/span mismatch: " + n)
        if json.loads(span) != d["locator"]:
            raise ValueError("Record mismatch: " + n)
        if d.get("vector") is not None:
            if d.get("embedding_model") != k.model_name or not np.allclose(LexicalEncoder().encode(span.decode()), d["vector"]):
                raise ValueError("Vector mismatch: " + n)
        elif d.get("vector_status") != "unknown":
            raise ValueError("Unmarked unknown vector: " + n)
    return {"nodes": len(k.graph), "edges": k.graph.number_of_edges()}


def reviewed(value):
    # A narrow guard, not a substitute for human/agent review of every field.
    if re.search(r"(?i)(password|bearer |access[_ -]?token|api[_ -]?key|private[_ -]?key|-----begin|gh[pousr]_[a-z0-9]+|sk-[a-z0-9]+)", value):
        raise ValueError("Potential secret; refusing to store")


def remember(home, k, record, defer=False):
    """Persist a reviewed note, not the raw original conversation."""
    required = ("key", "title", "provider", "source_type", "status", "claim", "qualification")
    allowed = set(required) | {"date", "url", "conversation_id", "message_id", "source_version", "source_position", "query", "source_key"}
    if not isinstance(record, dict) or set(record) - allowed:
        raise ValueError("Only reviewed knowledge and locator fields are accepted")
    if any(not isinstance(record.get(f), str) or not record[f].strip() for f in required):
        raise ValueError("Required fields: " + ", ".join(required))
    if any(not isinstance(v, str) or len(v) > 2000 for v in record.values()):
        raise ValueError("Use concise, reviewed string metadata only")
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    reviewed(raw.decode())
    version = digest(raw)
    relative = "sources/" + version + ".json"
    path = home / relative
    path.parent.mkdir(exist_ok=True)
    if not path.resolve().is_relative_to(home.resolve()) or path.is_symlink():
        raise ValueError("Registry path escapes provider home")
    if path.exists() and path.read_bytes() != raw:
        raise ValueError("Source collision")
    path.write_bytes(raw)
    n = k.add(relative, raw.decode(), version=version,
              position={"start_byte": 0, "end_byte": len(raw)},
              kind="knowledge_note", defer_embedding=defer)
    k.graph.nodes[n]["locator"] = record
    return n


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--home", required=True, type=Path)
    p.add_argument("action", choices=["init", "remember", "link", "verify", "search", "read", "context"])
    p.add_argument("value", nargs="?", default="")
    p.add_argument("--target")
    p.add_argument("--relation")
    p.add_argument("--reason")
    p.add_argument("--reviewed", action="store_true")
    p.add_argument("--defer-embedding", action="store_true")
    a = p.parse_args()
    home = a.home.resolve()
    graph = home / "graph.json"
    if a.action == "init":
        if graph.exists():
            raise FileExistsError("Load the existing graph; never overwrite it")
        home.mkdir(parents=True, exist_ok=True)
        (home / "sources").mkdir(exist_ok=True)
        KnowledgePositions("lexical-hash-512", LexicalEncoder()).save(graph)
        print(graph)
        return
    k = load(home)
    if a.action == "verify":
        print(json.dumps(verify(home, k)))
    elif a.action == "search":
        print(json.dumps([{"id": n, "score": s, "record": k.graph.nodes[n]["locator"]} for n, s in k.search(a.value)], indent=2))
    elif a.action == "read":
        verify(home, k)
        print(json.dumps(k.graph.nodes[a.value]["locator"], indent=2))
    elif a.action == "context":
        print(json.dumps(k.chat_context(a.value), indent=2))
    else:
        if not a.reviewed:
            raise ValueError("Review every field and relation for sensitive information; pass --reviewed")
        verify(home, k)
        if a.action == "remember":
            n = remember(home, k, json.loads(Path(a.value).read_text()), a.defer_embedding)
            print(n)
        else:
            if not all((a.value, a.target, a.relation, a.reason)):
                raise ValueError("Source ID, --target, --relation and --reason required")
            reviewed(a.reason + " " + a.relation)
            k.link(a.value, a.target, a.relation, evidence={"qualification": a.reason, "source_record": a.value})
        verify(home, k)
        k.save(graph)


if __name__ == "__main__":
    main()
