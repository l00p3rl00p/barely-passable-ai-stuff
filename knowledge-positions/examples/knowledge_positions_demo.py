import marimo
app = marimo.App()
@app.cell
def _():
    import marimo as mo
    mo.md("# Knowledge Positions — executable checks\nRun from knowledge-positions. Install: python -m pip install . marimo. See COVERAGE.md.")
    return (mo,)
@app.cell
def _():
    from pathlib import Path
    import hashlib, tempfile, sys, subprocess, json
    from knowledge_positions import KnowledgePositions
    root = Path.cwd()
    assert (root / "examples/gps/source.txt").exists(), "Run from knowledge-positions"
    work = tempfile.TemporaryDirectory()
    path = Path(work.name)
    fixture = path / "example.py"
    fixture.write_text("def connect():\n    return 42\n")
    k = KnowledgePositions()
    ids = k.ingest_python(fixture)
    assert ids and all(k.graph.nodes[n]["vector"] for n in ids)
    print("AST nodes:", len(ids), "vector dimensions:", len(k.graph.nodes[ids[0]]["vector"]))
    return fixture, ids, k, path, root, sys, subprocess, json, hashlib, KnowledgePositions, work
@app.cell
def _(fixture, ids, k, path, hashlib, KnowledgePositions):
    # Identity, hashes and persistence
    assert k.ingest_python(fixture) == ids
    assert all(k.graph.nodes[n]["version"] == hashlib.sha256(fixture.read_bytes()).hexdigest() for n in ids)
    k.save(path / "graph.json")
    loaded = KnowledgePositions.load(path / "graph.json")
    assert set(loaded.graph.nodes) == set(k.graph.nodes)
    assert set(loaded.graph.edges(keys=True)) == set(k.graph.edges(keys=True))
    print(loaded.search("connect function"))
    print("Source version, repeat ingestion and persistence checks passed")
    return
@app.cell
def _(path, root, sys, subprocess, json):
    # GPS trial, isolated temporary directory (never alter repository fixture)
    import shutil
    gps = path / "gps"
    shutil.copytree(root / "examples/gps", gps)
    def run(*args):
        return subprocess.check_output([sys.executable, str(gps/"gps.py"), *args], text=True)
    print(run("build"))
    hits = json.loads(run("search", "SDK codebase"))
    print(hits)
    assert hits["exact"]
    node = hits["exact"][0]
    print(run("neighbors", node))
    print(run("read", node))
    original = (gps/"source.txt").read_bytes()
    (gps/"source.txt").write_bytes(original + b"changed")
    try:
        result = subprocess.run([sys.executable,str(gps/"gps.py"),"read",node],capture_output=True,text=True)
        assert result.returncode != 0 and "source changed" in result.stderr
    finally:
        (gps/"source.txt").write_bytes(original)
    print("Changed source rejected")
    return
if __name__ == "__main__":
    app.run()
