#!/usr/bin/env python3
"""Paper-specific deterministic UKC/1 reconstruction using existing Python indexer.

Input: immutable current paper and historical companion.
Output: version-scoped common records + qualified hash-compatible relations.
No LLM, no historical/source mutation, no dependency beyond existing numpy indexer.
This is a paper example, not broad UKC SDK conformance certification.

python reconstruct-enrichment.py build [--source ... --history ... --output ...]
python reconstruct-enrichment.py verify [--source ... --history ... --output ...]
python reconstruct-enrichment.py get EKC:14 [--output ...]
python reconstruct-enrichment.py neighbors EKC:14 [--output ...]
python reconstruct-enrichment.py resolve EKC:14 [--source ... --output ...]
python reconstruct-enrichment.py export-okf EKC:14 [--output ...]
"""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1] / "research"
sys.path.insert(0, str(RESEARCH))
import jit_index

AUTHORITY = "repo:l00p3rl00p/barely-passable-ai-stuff"
SOURCE_KEY = "knowledge-positions/research/paper.md"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(tag, digest):
    raw = json.dumps([AUTHORITY, SOURCE_KEY, tag, digest],
                     ensure_ascii=False, separators=(",", ":")).encode()
    return "ukc:v1:" + sha(raw)


def reconstruct(paper_bytes, history):
    # The preexisting Python source parser and lexical-hash encoder are authoritative
    # for this Python example. Use only a temporary generated index.
    with tempfile.TemporaryDirectory() as tmp:
        old_paper, old_index = jit_index.PAPER, jit_index.INDEX
        try:
            tmp_paper = Path(tmp) / "paper.md"
            tmp_paper.write_bytes(paper_bytes)
            jit_index.PAPER, jit_index.INDEX = tmp_paper, Path(tmp) / "jit-index.json"
            index = jit_index.build()
            jit_index.load_verified()
        finally:
            jit_index.PAPER, jit_index.INDEX = old_paper, old_index
    old_by_id = {n["id"]: n for n in history["nodes"]}
    by_tag = {n["tag"]: n for n in index["nodes"]}
    if len(old_by_id) != len(history["nodes"]) or len(by_tag) != len(index["nodes"]):
        raise ValueError("Duplicate historical identity or current tag")
    matching = {
        n["id"]: by_tag[n["tag"]] for n in history["nodes"]
        if n["tag"] in by_tag
        and n["content_hash"] == by_tag[n["tag"]]["source_version_sha256"]
    }
    records = []
    for order, n in enumerate(index["nodes"]):
        digest = n["source_version_sha256"]
        p = n["source_position"]
        records.append({
            "schema": "ukc/1",
            "id": canonical(n["tag"], digest),
            "source": {
                "authority": AUTHORITY, "key": SOURCE_KEY,
                "realm": "public_repository",
                "version": "sha256:" + index["paper_sha256"],
                "unit_version": "sha256:" + digest,
                "access": "public"
            },
            "kind": "markdown_section",
            "location": {
                "status": "known", "basis": "ekc_heading_parser",
                "anchor": n["tag"],
                "spans": [{"unit": "utf8_byte", "start": p["start_byte"],
                           "end": p["end_byte"]}],
                "start_line": p["start_line"], "end_line": p["end_line"]
            },
            "relations": [],
            "proximity": [{"space": "lexical-hash-512",
                           "status": "known", "vector": n["vector"]}],
            "values": {"title": n["heading"], "tag": n["tag"],
                       "order": order, "terms": n["terms"]},
            "native": {"parser": "ekc_heading_regex",
                       "heading_level": n["heading_level"],
                       "source_ref": n["id"], "source_bytes_retained": False},
            "evidence": {"source_sha256": index["paper_sha256"],
                         "span_sha256": digest,
                         "precision": "verified_utf8_span"}
        })
    record_by_tag = {r["values"]["tag"]: r for r in records}
    old_to_current = {oid: record_by_tag[n["tag"]] for oid, n in matching.items()}
    used = set()
    accepted = []

    def link(a, b, relation, qualification, evidence, provenance):
        key = (a["id"], b["id"], relation, qualification)
        if key in used:
            return False
        used.add(key)
        edge = {"source": a["id"], "target": b["id"], "relation": relation,
                "qualification": qualification, "evidence": evidence,
                "provenance": provenance}
        a["relations"].append({**edge, "direction": "out", "neighbor": b["id"]})
        b["relations"].append({**edge, "direction": "in", "neighbor": a["id"]})
        return True

    for e in index["edges"]:
        a = record_by_tag[e["source"].removeprefix("paper.md#")]
        b = record_by_tag[e["target"].removeprefix("paper.md#")]
        link(a, b, e["relation"], e["qualification"],
             {"origin": "parsed_heading_structure"},
             {"source": SOURCE_KEY, "source_sha256": index["paper_sha256"]})

    compatible_vectors = []
    for oid, n in matching.items():
        old = old_by_id[oid]
        v = record_by_tag[n["tag"]]["proximity"][0]["vector"]
        if (old.get("embedding_model") == "lexical-hash-512"
                and isinstance(old.get("vector"), list)
                and len(v) == len(old["vector"])
                and all(abs(x - y) < 1e-12 for x, y in zip(v, old["vector"]))):
            compatible_vectors.append(n["tag"])

    inactive, matched_sequence = [], []
    for e in history["edges"]:
        a_old = old_by_id.get(e["source"])
        b_old = old_by_id.get(e["target"])
        if a_old is None or b_old is None:
            raise ValueError("Historical edge has missing endpoint")
        a, b = old_to_current.get(e["source"]), old_to_current.get(e["target"])
        item = {"from": a_old["tag"], "to": b_old["tag"], "relation": e["relation"],
                "old_source_hash": a_old["content_hash"],
                "old_target_hash": b_old["content_hash"]}
        if a is None or b is None:
            inactive.append({**item, "reason": "one_or_both_source_hashes_changed"})
            continue
        if e["relation"] == "next_section":
            matched_sequence.append(item)
            continue
        if not link(a, b, e["relation"], "historical_editorial_navigation",
                    e.get("evidence"),
                    {"artifact": "evolving-knowledge-context.json",
                     "source_sha256": history["source_sha256"],
                     "source_span_sha256": a_old["content_hash"],
                     "target_span_sha256": b_old["content_hash"]}):
            raise ValueError("Duplicate editorial edge")
        accepted.append(item)
    for r in records:
        r["relations"].sort(
            key=lambda e: (e["direction"], e["relation"], e["neighbor"]))
    report = {
        "current_sections": len(records),
        "source_hash_matches": len(matching),
        "compatible_legacy_vectors": sorted(compatible_vectors),
        "structural_edges": len(index["edges"]),
        "recovered_editorial_edges": accepted,
        "inactive_historical_edges": inactive,
        "matched_historical_sequence_edges": len(matched_sequence),
        "current_edges": len(index["edges"]) + len(accepted),
        "qualification": "Historical editorial links are navigation only"
    }
    return {"schema": "ukc-reconstruction/1",
            "source_sha256": index["paper_sha256"],
            "records": records, "report": report}


def verify(paper_bytes, result):
    if sha(paper_bytes) != result["source_sha256"]:
        raise ValueError("source_changed")
    ids = {r["id"] for r in result["records"]}
    if len(ids) != len(result["records"]):
        raise ValueError("duplicate_conflict")
    for r in result["records"]:
        p = r["location"]["spans"][0]
        span = paper_bytes[p["start"]:p["end"]]
        if (r["schema"] != "ukc/1"
                or r["id"] != canonical(r["values"]["tag"], r["evidence"]["span_sha256"])
                or sha(span) != r["evidence"]["span_sha256"]):
            raise ValueError("corrupt_record: " + r["values"]["tag"])
        if len(r["proximity"][0]["vector"]) != 512:
            raise ValueError("vector_space_mismatch")
        if any(e["neighbor"] not in ids for e in r["relations"]):
            raise ValueError("invalid edge endpoint")
    return True


def lookup(data, key):
    for r in data["records"]:
        if r["id"] == key or r["values"]["tag"] == key:
            return r
    raise KeyError(key)


def export_okf(record):
    # JSON is valid YAML 1.2 flow syntax; preserve all x_ukc fields exactly.
    frontmatter = json.dumps({"type": "SourceUnit",
                              "title": record["values"]["title"],
                              "x_ukc": record},
                             ensure_ascii=False, indent=2)
    return ("---\n" + frontmatter + "\n---\n\n"
            + "# " + record["values"]["title"] + "\n\n"
            + "Source-backed knowledge position; resolve original bytes through "
              "x_ukc.source and x_ukc.location.\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=[
        "build", "verify", "get", "resolve", "neighbors", "export-okf"])
    p.add_argument("tag", nargs="?")
    p.add_argument("--source", type=Path, default=RESEARCH / "paper.md")
    p.add_argument("--history", type=Path, default=RESEARCH / "evolving-knowledge-context.json")
    p.add_argument("--output", type=Path, default=HERE / "paper-ukc.json")
    a = p.parse_args()
    if a.output.resolve() in {a.source.resolve(), a.history.resolve()}:
        p.error("Output must not overwrite authoritative source or history")
    raw = a.source.read_bytes()
    if a.action == "build":
        history = json.loads(a.history.read_text())
        result = reconstruct(raw, history)
        verify(raw, result)
        a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"current_sections": result["report"]["current_sections"],
                          "matching": result["report"]["source_hash_matches"],
                          "recovered": len(result["report"]["recovered_editorial_edges"]),
                          "inactive": len(result["report"]["inactive_historical_edges"]),
                          "edges": result["report"]["current_edges"]}, indent=2))
        return
    data = json.loads(a.output.read_text())
    verify(raw, data)
    if a.action == "verify":
        history = json.loads(a.history.read_text())
        fresh = reconstruct(raw, history)
        if fresh != data:
            raise ValueError("Saved output differs from deterministic rebuild")
        print(f"verified {len(data['records'])} UKC/1 paper records")
        return
    if not a.tag:
        p.error("Section tag or canonical ID required")
    r = lookup(data, a.tag)
    if a.action == "get":
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif a.action == "neighbors":
        print(json.dumps(r["relations"], ensure_ascii=False, indent=2))
    elif a.action == "resolve":
        span = r["location"]["spans"][0]
        print(raw[span["start"]:span["end"]].decode())
    else:
        print(export_okf(r))


if __name__ == "__main__":
    main()
