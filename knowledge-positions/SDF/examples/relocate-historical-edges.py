#!/usr/bin/env python3
"""Deterministic re-location experiment on historical paper editorial edges.

Uses source-backed historical paper blob and CURRENT manuscript. No LLM. Does
not alter the original source, index, or asserted relations. Reports positional
and lexical confidence separately from whether a historical editorial edge
still expresses a true claim.

Default historical fetch is from the exact Git blob recorded in the companion.
Supply --old-paper for reproducible offline operation; it MUST match source SHA.
"""
import argparse
import base64
import difflib
import hashlib
import json
import math
import re
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1] / "research"
AUTHORITY = "l00p3rl00p/barely-passable-ai-stuff"
TOKENS = re.compile(r"\w+", re.UNICODE)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source_bytes(history, optional_path=None):
    if optional_path is not None:
        data = Path(optional_path).read_bytes()
    else:
        blob = history["source_git_blob"]
        if not re.fullmatch(r"[a-f0-9]{40}", blob):
            raise ValueError("Invalid saved Git blob identifier")
        url = "https://api.github.com/repos/" + AUTHORITY + "/git/blobs/" + blob
        req = urllib.request.Request(
            url, headers={"Accept": "application/vnd.github+json",
                          "User-Agent": "public-knowledge-positions-reconstruction"})
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.load(response)
        if payload.get("encoding") != "base64":
            raise ValueError("Historical Git blob must use base64 encoding")
        data = base64.b64decode(payload["content"], validate=False)
    if sha(data) != history["source_sha256"] or len(data) != history["source_bytes"]:
        raise ValueError("The historical source does not match the saved companion")
    return data


def terms(raw):
    return TOKENS.findall(raw.decode("utf-8").casefold())


def fingerprints(raw):
    text = raw.decode("utf-8")
    lines = [line.strip() for line in text.splitlines()
             if line.strip() and not line.strip().startswith("#")]
    return lines


def similarity(old_bytes, current_bytes, old_vector, current_vector):
    previous = terms(old_bytes)
    current = terms(current_bytes)
    a, b = set(previous), set(current)
    overlap = len(a & b) / len(a | b) if a | b else 1.0
    counts_a, counts_b = Counter(previous), Counter(current)
    shared = sum((counts_a & counts_b).values())
    retained = shared / max(1, sum(counts_a.values()))
    new_covered = shared / max(1, sum(counts_b.values()))
    old_lines, new_lines = set(fingerprints(old_bytes)), set(fingerprints(current_bytes))
    old_line_survival = len(old_lines & new_lines) / max(1, len(old_lines))
    char_ratio = difflib.SequenceMatcher(
        None, old_bytes.decode("utf-8"), current_bytes.decode("utf-8"),
        autojunk=False).ratio()
    if (len(old_vector) != 512 or len(current_vector) != 512):
        raise ValueError("Wrong vector dimensionality")
    dot = sum(x * y for x, y in zip(old_vector, current_vector))
    norms = math.sqrt(sum(x*x for x in old_vector)) * math.sqrt(
        sum(y*y for y in current_vector))
    cosine = dot / norms if norms else 0.0
    return {"token_jaccard": round(overlap, 6),
            "old_token_retained": round(retained, 6),
            "new_token_covered": round(new_covered, 6),
            "old_line_survival": round(old_line_survival, 6),
            "char_sequence_ratio": round(char_ratio, 6),
            "vector_cosine": round(cosine, 6)}


def run(old_raw, new_raw, history, current):
    if sha(new_raw) != current["paper_sha256"]:
        raise ValueError("Current paper differs from its verified JIT index")
    old_nodes = history["nodes"]
    new_nodes = current["nodes"]
    old_id = {n["id"]: n for n in old_nodes}
    new_tag = {n["tag"]: n for n in new_nodes}
    if len(old_id) != len(old_nodes) or len(new_tag) != len(new_nodes):
        raise ValueError("Duplicate node identities")
    records = {}
    for n in old_nodes:
        current_node = new_tag.get(n["tag"])
        if current_node is None:
            raise ValueError("Unresolved historical section anchor: " + n["tag"])
        op, np = n["position"], current_node["source_position"]
        a = old_raw[op["start_byte"]:op["end_byte"]]
        b = new_raw[np["start_byte"]:np["end_byte"]]
        if sha(a) != n["content_hash"] or sha(b) != current_node["source_version_sha256"]:
            raise ValueError("Section source digest verification failed: " + n["tag"])
        same = n["content_hash"] == current_node["source_version_sha256"]
        metrics = similarity(a, b, n["vector"], current_node["vector"])
        # Relocation is supported by matching stable anchor and verified bytes.
        # This does not imply semantic relation evidence has been revalidated.
        records[n["tag"]] = {
            "old_id": n["id"], "current_id": current_node["id"],
            "old_content_sha256": n["content_hash"],
            "current_content_sha256": current_node["source_version_sha256"],
            "exact_content_match": same,
            "old_position": op, "current_position": np,
            "heading_match": n["heading"] == current_node["heading"],
            **metrics,
        }
    changed_editorial = []
    recovered_editorial = []
    for edge in history["edges"]:
        if edge["relation"] == "next_section":
            continue
        o = old_id.get(edge["source"])
        d = old_id.get(edge["target"])
        if o is None or d is None:
            raise ValueError("Unknown editorial edge source/target")
        a, b = records[o["tag"]], records[d["tag"]]
        item = {"source_tag": o["tag"], "target_tag": d["tag"],
                "relation": edge["relation"], "historical_evidence": edge["evidence"],
                "source": a, "target": b}
        if a["exact_content_match"] and b["exact_content_match"]:
            item["status"] = "unchanged_source_hashes"
            recovered_editorial.append(item)
        else:
            # Relocated *records*, not independently verified relationship meaning.
            item["status"] = "located_changed_record_relationship_not_revalidated"
            changed_editorial.append(item)
    return {
        "method": "historical_git_blob_exact_span_and_current_EKC_anchor_relocation",
        "historical_source_sha256": history["source_sha256"],
        "current_source_sha256": current["paper_sha256"],
        "old_sections": len(old_nodes), "current_sections": len(new_nodes),
        "exact_matching_sections": sum(v["exact_content_match"] for v in records.values()),
        "relocated_changed_sections": sum(not v["exact_content_match"] for v in records.values()),
        "unchanged_editorial": len(recovered_editorial),
        "changed_editorial": len(changed_editorial),
        "records": records,
        "relocated_editorial_candidates": changed_editorial,
        "recovered_exact_editorial": recovered_editorial,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-paper", type=Path)
    parser.add_argument("--current-paper", type=Path, default=RESEARCH / "paper.md")
    parser.add_argument("--history", type=Path,
                        default=RESEARCH / "evolving-knowledge-context.json")
    parser.add_argument("--index", type=Path, default=RESEARCH / "jit-index.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--assert-paper", action="store_true",
                        help="Assert expected outcomes for the checked-in live paper")
    args = parser.parse_args()
    history = json.loads(args.history.read_text())
    current = json.loads(args.index.read_text())
    report = run(source_bytes(history, args.old_paper), args.current_paper.read_bytes(),
                 history, current)
    if args.assert_paper:
        candidates = report["relocated_editorial_candidates"]
        two80 = sum(e["source"]["old_token_retained"] >= .8 and
                    e["target"]["old_token_retained"] >= .8 for e in candidates)
        two90 = sum(e["source"]["old_token_retained"] >= .9 and
                    e["target"]["old_token_retained"] >= .9 for e in candidates)
        low = [e for e in candidates if (e["source"]["old_token_retained"] < .8
                                         or e["target"]["old_token_retained"] < .8)]
        assert (report["exact_matching_sections"],
                report["relocated_changed_sections"],
                report["unchanged_editorial"], report["changed_editorial"]) == (
                    15, 13, 8, 22)
        assert two80 == 16 and two90 == 13
        assert len(low) == 6 and all(
            "EKC:25" in (e["source_tag"], e["target_tag"]) for e in low)
        assert all(e["source"]["heading_match"] and
                   e["target"]["heading_match"] for e in candidates)
        print("ASSERT PASS: all 22 relocated; 16 retain >=80% old tokens on "
              "both ends, 13 >=90%; six weaker pairs all involve EKC:25.")
    if args.output:
        if args.output.resolve() in {p.resolve() for p in (
                args.old_paper, args.current_paper, args.history, args.index)
                if p is not None}:
            raise ValueError("Report output cannot overwrite authoritative sources")
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    concise = {
        "old_sections": report["old_sections"],
        "current_sections": report["current_sections"],
        "exact_matching_sections": report["exact_matching_sections"],
        "relocated_changed_sections": report["relocated_changed_sections"],
        "unchanged_editorial": report["unchanged_editorial"],
        "changed_editorial": report["changed_editorial"],
        "candidates": [
            {**{k: e[k] for k in ("source_tag", "target_tag", "relation")},
             "source_jaccard": e["source"]["token_jaccard"],
             "target_jaccard": e["target"]["token_jaccard"],
             "source_retained": e["source"]["old_token_retained"],
             "target_retained": e["target"]["old_token_retained"],
             "source_cosine": e["source"]["vector_cosine"],
             "target_cosine": e["target"]["vector_cosine"],
             "both_headings_match": e["source"]["heading_match"] and e["target"]["heading_match"]}
            for e in report["relocated_editorial_candidates"]
        ],
    }
    print(json.dumps(concise, indent=2))


if __name__ == "__main__":
    main()
