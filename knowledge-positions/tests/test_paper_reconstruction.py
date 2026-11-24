#!/usr/bin/env python3
"""Public paper proof: independent Python/JS reconstruction and source verification."""
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
EX = BASE / "SDF" / "examples"
SOURCE = BASE / "research" / "paper.md"
HISTORY = BASE / "research" / "evolving-knowledge-context.json"
PY = EX / "reconstruct-enrichment.py"
JS = EX / "reconstruct-enrichment.mjs"


def call(*args):
    return subprocess.check_output([str(a) for a in args], text=True)


def equivalent(a, b, path="root"):
    if isinstance(a, dict):
        assert isinstance(b, dict) and a.keys() == b.keys(), path
        for k in a:
            equivalent(a[k], b[k], path + "." + k)
    elif isinstance(a, list):
        assert isinstance(b, list) and len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            equivalent(x, y, path + "." + str(i))
    elif isinstance(a, (int, float)) and not isinstance(a, bool):
        assert isinstance(b, (int, float)) and math.isclose(
            a, b, abs_tol=1e-12, rel_tol=1e-12), path
    else:
        assert a == b, (path, a, b)


def main():
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE, HISTORY)}
    with tempfile.TemporaryDirectory() as work:
        outpy = Path(work) / "python.json"
        outjs = Path(work) / "javascript.json"
        call(sys.executable, PY, "build", "--output", outpy)
        call("node", JS, "build", SOURCE, HISTORY, outjs)
        call(sys.executable, PY, "verify", "--output", outpy)
        call("node", JS, "verify", SOURCE, HISTORY, outjs)
        python_data = json.loads(outpy.read_text())
        js_data = json.loads(outjs.read_text())
        equivalent(python_data, js_data)
        r = python_data["report"]
        assert r["current_sections"] == 29, r
        assert r["source_hash_matches"] == 15, r
        assert len(r["compatible_legacy_vectors"]) == 15, r
        assert r["structural_edges"] == 38, r
        assert len(r["recovered_editorial_edges"]) == 8, r
        assert r["current_edges"] == 46, r
        assert len([x for x in r["inactive_historical_edges"]
                    if x["relation"] != "next_section"]) == 22, r
        assert len(r["inactive_historical_edges"]) == 39, r

        # Original bytes can be resolved by either implementation.
        pysection = call(sys.executable, PY, "resolve", "EKC:14",
                         "--output", outpy)
        jssection = call("node", JS, "resolve", "EKC:14",
                         SOURCE, HISTORY, outjs)
        assert pysection == jssection
        assert "[EKC:14]" in pysection
        pyrecord = json.loads(call(sys.executable, PY, "get", "EKC:14",
                                   "--output", outpy))
        jsrecord = json.loads(call("node", JS, "get", "EKC:14",
                                   SOURCE, HISTORY, outjs))
        equivalent(pyrecord, jsrecord)
        assert any(e["qualification"] == "historical_editorial_navigation"
                   for r in python_data["records"] for e in r["relations"])
        # OKF x_ukc frontmatter preserves every common-record field.
        for cmd in ((sys.executable, PY, "export-okf", "EKC:14", "--output", outpy),
                    ("node", JS, "export-okf", "EKC:14", SOURCE, HISTORY, outjs)):
            front = call(*cmd).split("---\n", 2)[1]
            parsed = json.loads(front.strip())
            equivalent(parsed["x_ukc"], pyrecord)
        # Read from a changed source must reject stale record before returning bytes.
        modified = Path(work) / "modified.md"
        modified.write_bytes(SOURCE.read_bytes() + b"\nNEW\n")
        proc = subprocess.run(["node", str(JS), "resolve", "EKC:14",
                               str(modified), str(HISTORY), str(outjs)],
                              capture_output=True)
        assert proc.returncode != 0 and b"source_changed" in proc.stderr
    for p, digest in before.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, "source mutated"
    print("PASS: 29 records; 15 matching sections and vectors; 38 structural "
          "+ 8 qualified editorial edges; 22 editorial edges held inactive; "
          "Python/JavaScript records, reads, OKF x_ukc export and failure mode agree.")


if __name__ == "__main__":
    main()
