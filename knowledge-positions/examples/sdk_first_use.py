"""Portable, self-checking first use of the existing Knowledge Positions Python library.

Run from knowledge-positions/: python examples/sdk_first_use.py
No account, OmniGraph server, LLM, embedding download or user-specific paths.
This illustrates the EXISTING Python API, not full UKC/1 certification.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from knowledge_positions import KnowledgePositions


def demonstrate() -> dict:
    original = b"Alpha is a paragraph.\nBeta follows Alpha.\n"
    version = hashlib.sha256(original).hexdigest()
    lines = original.splitlines(keepends=True)
    assert len(lines) == 2
    first, second = (line.rstrip(b"\r\n") for line in lines)
    position_1 = {"start_byte": 0, "end_byte": len(first)}
    position_2 = {
        "start_byte": len(lines[0]),
        "end_byte": len(lines[0]) + len(second),
    }

    # Reuse the existing library. Defer embedding; no model or network required.
    k = KnowledgePositions()
    first_id = k.add(
        "example.txt", first.decode(), version=version,
        position=position_1, kind="passage", defer_embedding=True,
    )
    second_id = k.add(
        "example.txt", second.decode(), version=version,
        position=position_2, kind="passage", defer_embedding=True,
    )
    same_identity = k.add(
        "example.txt", first.decode(), version=version,
        position=position_1, kind="passage", defer_embedding=True,
    ) == first_id

    # The sequence is directly observed in the original source.
    k.link(first_id, second_id, "next_passage", evidence={"basis": "source_order"})
    edge = k.neighbors(first_id)["outgoing"]
    assert len(edge) == 1 and edge[0][1] == second_id
    assert edge[0][3]["relation"] == "next_passage"

    # Resolve recorded byte positions against the version-checked source.
    assert hashlib.sha256(original).hexdigest() == k.graph.nodes[first_id]["version"]
    selected = original[position_2["start_byte"]:position_2["end_byte"]].decode()
    assert hashlib.sha256(selected.encode()).hexdigest() == k.graph.nodes[second_id]["content_hash"]

    # A disposable saved graph can be loaded without recomputing identities.
    with tempfile.TemporaryDirectory() as temporary:
        dest = Path(temporary) / "graph.json"
        k.save(dest)
        loaded = KnowledgePositions.load(dest)
        reloaded = (
            set(loaded.graph.nodes) == {first_id, second_id}
            and loaded.graph.number_of_edges() == 1
        )

    result = {
        "same_identity": same_identity,
        "nodes": k.graph.number_of_nodes(),
        "edges": k.graph.number_of_edges(),
        "first_text": first.decode(),
        "next_text": selected,
        "vector_status": k.graph.nodes[first_id]["vector_status"],
        "source_verified": True,
        "reloaded": reloaded,
    }
    assert result == {
        "same_identity": True,
        "nodes": 2,
        "edges": 1,
        "first_text": "Alpha is a paragraph.",
        "next_text": "Beta follows Alpha.",
        "vector_status": "unknown",
        "source_verified": True,
        "reloaded": True,
    }
    return result


if __name__ == "__main__":
    print(json.dumps(demonstrate(), indent=2))
