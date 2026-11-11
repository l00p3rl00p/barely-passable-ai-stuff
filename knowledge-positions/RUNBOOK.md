# Runbook

A human-facing guide to installing, running, using and experimenting with Knowledge Positions.

## 0. Agent capture workflow

Use the [README quick start](README.md#quick-start--capture-working-conversations) to install the library, initialize/load any caller-selected graph and execute capture.py. The capture command supports init, remember, link, verify, search, read and context. It explicitly uses the deterministic lexical-hash-512 encoder; the Python API supports other actual encoders. The source registry stores reviewed notes, not raw transcripts. Use one writer at a time. The README documents library mechanics, not a human's project workflow; the examples below also demonstrate the generic library.

## 1. Install

Clone the repository and enter the library folder:

```bash
git clone https://github.com/l00p3rl00p/barely-passable-ai-stuff.git
cd barely-passable-ai-stuff/knowledge-positions
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

## 2. Run the library

Create an example.py containing a simple Python function, then open Python:

```python
from knowledge_positions import KnowledgePositions
k = KnowledgePositions()
ids = k.ingest_python("example.py")
print(k.neighbors(ids[0]))
print(k.search("function"))
k.save("knowledge.json")
```

The first embedding run needs access to the configured model.

## 3. Experiment with notebooks

```bash
python -m pip install jupyterlab marimo
jupyter lab knowledge_positions_demo.ipynb
# Alternatively:
marimo edit knowledge_positions_demo.py
```

Run the cells to inspect source positions, vectors, graph persistence and the GPS fixture. The notebooks have not been validated end-to-end with the real model.

## 4. Reproduce the GPS experiment

```bash
cd examples/gps
python gps.py build --source source.txt
python gps.py search "SDK codebase"
```

Copy a returned node ID into the following commands (replace NODE_ID):

```bash
python gps.py neighbors NODE_ID
python gps.py read NODE_ID --source source.txt
```

For the independent cold-context trial, follow the [experiment guide](examples/gps/README.md). Keep the original source and recorded results separate from the test agent. Compare results with the documented trial.

## 5. Troubleshoot

- Import failure: use the environment in which the library was installed.
- Model unavailable: download or cache the configured model; do not silently substitute lexical vectors.
- FTS5 unavailable: use a Python distribution with SQLite FTS5 support.
- Source changed: retrieval rejects a mismatched source version. Preserve the old version if needed; rebuild against the new source. Explicit dependency-based cascading staleness is implemented; automatic source monitoring is not.
- Node ID differs from historical trial: use the ID returned by the current build.

See [Environment](ENVIRONMENT.md) for actual components and [Coverage](COVERAGE.md) for tested and untested behavior.

## 6. Verify lifecycle behavior

```bash
python -m unittest -v test_lifecycle test_graph_views test_chat_context
```

The library supports `mark_source_changed(source, new_version)`, `invalidate(node_id, reason)`, `deprecate(node_id, reason, replacement_id=...)`, and explicit `revalidate(node_id, evidence)`. Default search excludes stale and deprecated nodes; `include_historical=True` includes them. Source hashes and review evidence must be supplied by the caller. No automatic monitoring or automatic fact verification is implied.

## Core graph and vector operations

```bash
python core_operations.py /path/to/graph.json
```

This read-only example runs the ten core graph algorithms and basic vector operations on current nodes, using explicitly selected directed, undirected unit-cost and dependency views. Supply `--start` and `--target` node IDs to change the investigation, and `--threshold` to explore candidate similarity groups. See [core vocabulary](CORE_VOCABULARY.md). No source graph is overwritten.

### Use the named views directly

```python
import networkx as nx
from knowledge_positions import KnowledgePositions
k = KnowledgePositions.load('graph.json')
root = next(iter(k.graph))
print(k.GRAPH_VIEWS)
tree = k.graph_view('tree', name='investigation-tree', root=root)
print(list(nx.bfs_tree(tree, root)))
custom = k.derive_graph('relationship-line-graph', nx.line_graph, source='directed')
print(k.core_algorithms(root, list(k.graph)[-1]))
```

Select a view by purpose, not by a mandatory workflow. Weighted/forest views require explicit costs or `unit_cost=True`. Use `defer_embedding=True` at admission when a vector is not available; call `fill_vector(node_id, original_span)` when it is. Unknown vectors do not enter similarity rankings. See the core vocabulary for names, parameters and open-ended derivation.

## Bounded chat retrieval

```python
context = k.chat_context(root, direction='both', profile='balanced')
print(context['retrieval'])  # PPR parameters and transparent profile
print(context['other'])      # immediate boundary references not loaded
```

API writes clear the derived cache. After direct edits to k.graph, call k.invalidate_cache(). Full graph operations and dependency invalidation remain unrestricted. No raw chats or secrets in Git.


## Source-relative positions: actual library API

Use the same method for source code, web content, documents and other items. The *reader* supplies verified coordinates; the library stores them. No AST, embedding model or LLM is required for the generic method.

```python
from hashlib import sha256
from pathlib import Path
from knowledge_positions import KnowledgePositions

file = Path("example.txt")
raw = file.read_bytes()  # an authorized, actual source read
text = raw.decode("utf-8")
k = KnowledgePositions()
node = k.add(str(file), text, version=sha256(raw).hexdigest(),
             position={"start_byte": 0, "end_byte": len(raw)},
             defer_embedding=True)
k.record_item_position(node, coordinates={"start_byte": 0, "end_byte": len(raw)},
                       basis="reader", precision="parsed")
k.save("knowledge.json")
```

For Python source, use `k.ingest_python("example.py", defer_embedding=True)` to reuse its deterministic AST traversal and ordered hierarchy; it does **not** call the embedding model. Native structure, stable anchors and exact spans are alternative methods, chosen by the library's [location convention](LOCATION_ACCESS.md#shared-location-method-selection-source-agnostic). Other readers can supply a path or a coordinate map; neither is mandatory when the other is available.

When an LLM only identifies a possible location, use the **same method** with `basis="observation"` and the default `precision="locator_only"`. Resolve original evidence before promoting a clue. Register genuinely novel source coordinate conventions with `register_location_method` so they can be reused in the saved graph; this is not permission to read a private source. Maintenance belongs to the host/read hook/watchdog plus this Python library, not to the LLM.

## 7. Deterministic capture: enforce the execution boundary, not the prompt

**Why this matters.** In a cold-start observation, an assistant read AGENTS.md, Core Vocabulary and a documented graph, then completed the visible image-generation request without calling Knowledge Positions, reading original evidence, or persisting a finding. In a later lookup it parsed graph.json directly instead of executing the Python graph engine. These observations show that *this optional workflow was bypassed*; they are not a population-wide guarantee about every LLM.

An agent prompt is a preference, not a session-write hook. For reliable persistence, the host application needs a capture path that runs independently of the model choosing a tool call. The reusable library remains provider-neutral; applications bind the appropriate runtime seams.

### Host integration contract (proposed, not installed)

```text
session append / tool result / clear boundary
                  |
          [host capture hook]
                  |
          [durable source journal]   <--- permissions, retention, redaction
                  |
       [single writer / idempotent queue]
                  |
        [source spans + version hash]
                  |
          [Knowledge Positions]
                  |
       [source/graph/vector index]
                  |
       [verification + checkpoint]
                  |
       [MCP/API retrieve on next task]
                  |
             working context
```

1. **Hook the actual event boundary.** Discover the runtime's supported session append, tool result, clear/rotate or stop hooks. Capture an event before it can disappear from working context; do not assume a particular framework exposes all four. An OpenTelemetry span or log can carry observability metadata but is not, by itself, a guaranteed complete transcript. A host integration must be able to access the actual source event.
2. **Durably append original evidence.** A unique event identity, observed provider/session ID, event type, order/offset, source version, content digest and capture status go into an access-controlled journal. The exact event content stays in an appropriately protected store with consent, retention and redaction controls. Never commit raw session streams to this Git repository.
3. **Index independently of model decisions.** A bounded single-writer worker consumes journal offsets, verifies source spans, invokes Knowledge Positions to persist source positions and graph structures, and records completed offsets. Idempotency means an event retry does not duplicate its source identity. Indexing may defer vectors and optional model-derived interpretation.
4. **Keep optional inference optional.** A later LLM may add qualified semantic relationships using evidence; such enrichment is separate from the mandatory event-capture path. Unknown vectors remain unknown. Do not turn model-generated hypotheses into original evidence.

**Do not confuse initial ingestion with enrichment:** a fast AST/schema pass may index whole repositories without LLM interpretation. The default host integration enriches only what has already been provided to the intelligence during real work. Initial admission is touch 1; a node or explicit cluster may receive only touches 2 and 3 as later semantic mutation passes. After touch 3, freeze its payload and grow outward through new nodes/relationships. Verified source mutation starts a new epoch. This hard write budget is separate from retrieval, which uses graph-theoretic attenuation rather than a fixed hop ceiling. An explicit offline full-corpus enrichment request is a different workload, not the default architecture. See [location and application pattern](LOCATION_ACCESS.md#recommended-application-pattern).
5. **Make lookup observable and enforceable.** A host-managed task-entry tool/MCP boundary can request the relevant navigational context and source evidence rather than relying on an optional reminder to run search. Record the tool call, retrieved evidence, model-visible context and any bypass reason. Ordinary model-directed lookup is still allowed, but it is not evidence that mandatory lookup ran.
6. **Audit failure and recovery.** Compare observed source events to durable journal entries, accepted graph nodes and committed checkpoints. A failed write must remain visible and retryable; do not report success solely because a hook was invoked. Preserve ordering across session clear/rotation and use a bounded queue/backpressure policy that protects user work. If a runtime cannot expose a usable event seam, report that integration gap rather than claiming automatic capture.

**Acceptance demonstration:** With a real runtime event source, perform ordinary work, rotate/clear context, and show that the event journal, index and verified checkpoint advanced **without an LLM-issued save call**. Force one safe write failure, retry it without duplication, and retrieve the preserved knowledge through the actual library/MCP path. This proves the specific integration, not universal reliability across providers. Until that demonstration, manual `capture.py` remains available but should not be described as automatic persistence.

See the [paper's execution-boundary discussion](research/paper.md) for the observed failure mode and proposed integration contract.
