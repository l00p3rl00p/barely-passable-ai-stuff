#!/usr/bin/env python3
"""Reconstruct paper navigation + safely reusable historical editorial edges.

Source and historical artifact are READ-ONLY; output and report are separate.
This is a paper-specific example of source/hash-qualified reconstruction, NOT
UKC/1 conformance or semantic revalidation. No LLM is used.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1] / "research"
sys.path.insert(0, str(RESEARCH))
import jit_index  # reuse the existing canonical Python source indexer


def reconstruct(source: Path, historical: Path, output: Path, report_path: Path):
    source, historical, output, report_path = (
        p.resolve() for p in (source, historical, output, report_path)
    )
    if len({source, historical, output, report_path}) != 4:
        raise ValueError("Source, history, index output, and report paths must be distinct")
    if not source.is_file() or not historical.is_file():
        raise FileNotFoundError("Missing authoritative source or historical companion")
    history = json.loads(historical.read_text(encoding="utf-8"))

    # Build from the CURRENT source. Never mutate the manuscript or historical artifact.
    jit_index.PAPER = source
    jit_index.INDEX = output
    base = jit_index.build()
    jit_index.load_verified()

    old_by_id = {node["id"]: node for node in history["nodes"]}
    if len(old_by_id) != len(history["nodes"]):
        raise ValueError("Historical records contain duplicate identities")
    current_by_tag = {node["tag"]: node for node in base["nodes"]}
    if len(current_by_tag) != len(base["nodes"]):
        raise ValueError("Current sections contain duplicate tags")

    matches = {
        node["id"]: current_by_tag.get(node["tag"])
        for node in history["nodes"]
        if current_by_tag.get(node["tag"]) is not None
        and node["content_hash"] == current_by_tag[node["tag"]]["source_version_sha256"]
    }
    # A hash match authorizes reusing old values only in a compatible declared
    # profile; the fresh vectors are independently reconstructed from current bytes.
    vector_verified, vector_incompatible = [], []
    for old_id, now in matches.items():
        previous = old_by_id[old_id]
        old_vector = previous.get("vector")
        new_vector = now.get("vector")
        if (
            previous.get("embedding_model") == now.get("embedding_model")
            and isinstance(old_vector, list)
            and isinstance(new_vector, list)
            and len(old_vector) == len(new_vector)
            and all(abs(a - b) < 1e-12 for a, b in zip(old_vector, new_vector))
        ):
            vector_verified.append(now["tag"])
        else:
            vector_incompatible.append(now["tag"])

    existing = {(e["source"], e["target"], e["relation"]) for e in base["edges"]}
    recovered, inactive, already_structural = [], [], []
    for edge in history["edges"]:
        src = old_by_id.get(edge["source"])
        dst = old_by_id.get(edge["target"])
        if src is None or dst is None:
            raise ValueError("Historical relation has an unknown endpoint")
        present = edge["source"] in matches and edge["target"] in matches
        item = {
            "from": src["tag"], "to": dst["tag"], "relation": edge["relation"],
            "historical_evidence": edge.get("evidence"),
            "source_hash": src["content_hash"], "target_hash": dst["content_hash"],
        }
        if not present:
            item["reason"] = "one_or_both_source_section_hashes_changed"
            inactive.append(item)
            continue
        new_src, new_dst = matches[edge["source"]]["id"], matches[edge["target"]]["id"]
        key = (new_src, new_dst, edge["relation"])
        if key in existing:
            already_structural.append(item)
            continue
        # Preserve exactly the earlier editorial assertion and its original
        # qualification; do not promote navigation-only into semantic fact.
        base["edges"].append({
            "source": new_src, "target": new_dst, "relation": edge["relation"],
            "qualification": "historical_editorial_navigation",
            "evidence": edge.get("evidence"),
            "reused_from": {
                "artifact": historical.name,
                "source_sha256": history.get("source_sha256"),
                "source_section_sha256": src["content_hash"],
                "target_section_sha256": dst["content_hash"],
            },
        })
        existing.add(key)
        recovered.append(item)
    report = {
        "method": "deterministic_source_hash_qualified_reconstruction",
        "source": str(source), "historical": str(historical),
        "current_sections": len(base["nodes"]), "matching_historical_sections": len(matches),
        "matching_section_tags": sorted(node["tag"] for node in matches.values()),
        "verified_legacy_vectors": sorted(vector_verified),
        "incompatible_legacy_vectors": sorted(vector_incompatible),
        "base_structural_edges": len(base["edges"]) - len(recovered),
        "recovered_editorial_edges": recovered, "already_structural_edges": already_structural,
        "inactive_historical_edges": inactive,
        "result_edges": len(base["edges"]),
        "qualification": "Historical editorial links retained as navigation only, not semantic proof",
    }
    # Derived output can be discarded and reconstructed. No historic input is rewritten.
    output.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Verify against original after adding only supported edge references.
    jit_index.load_verified()
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=RESEARCH / "paper.md")
    p.add_argument("--history", type=Path, default=RESEARCH / "evolving-knowledge-context.json")
    p.add_argument("--output", type=Path, default=HERE / "reconstructed-index.json")
    p.add_argument("--report", type=Path, default=HERE / "reconstruction-report.json")
    a = p.parse_args()
    result = reconstruct(a.source, a.history, a.output, a.report)
    print(json.dumps({
        "sections": result["current_sections"],
        "source_hash_matches": result["matching_historical_sections"],
        "recovered_editorial": len(result["recovered_editorial_edges"]),
        "inactive_historical": len(result["inactive_historical_edges"]),
        "edges": result["result_edges"],
    }, indent=2))


if __name__ == "__main__":
    main()
