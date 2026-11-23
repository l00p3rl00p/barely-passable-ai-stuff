# Neuron Connector — receive, map, emit

An independent standard-library implementation, unrelated to the OTel library. Receives already admitted Knowledge Positions records, maps them through destination profiles, emits to one or multiple native surfaces. No scanner, model, daemon, custom MCP or extra datastore. The producer (Rust or another caller) owns canonical admission, identity, source lifecycle and batching. This connector implements **new admissions only**; it does not silently overwrite or reconcile existing records. Re-emission against an existing identity refuses; a production incremental caller must filter previously admitted records with native queries.

## Use

Copy this directory. Python 3.10+ is sufficient for the connector. The Rust producer can pipe one admitted JSON batch (nodes, edges) directly to stdin:
```bash
python3 connector.py --config destinations.json < admitted-batch.json
```
The file redirection is merely an example; pipe from Rust to avoid staging. Copy destinations.example.json and remove unused outputs, supply your real endpoint and existing authorization. Each output returns its own receipt; a partial multi-emission is not an atomic distributed transaction. Do not retry confirmed writes as if they failed. No fallback targets.

OmniGraph: native strict NDJSON load, explicit branch, append, bounded batch; existing graph/schema and authorized token environment. Ladybug: official API server POST /cypher with parameterized statements; existing schema and read-write server. Each node/edge is a native committed operation; partial failure needs reconciliation. Read back by ID to verify. No API service created by this package.

Codebase Memory: stock MCP query_graph is read-only, and index_repository performs its own scan. The included native bridge deliberately calls the real store functions rather than fabricate a database or re-scan. It requires a separately built CBM binary with the small entry point below; it is experimental and not a verified drop-in. Native label, qualified name, path and relation type are provided by the producer. The bridge appends to an existing isolated project, rebuilds native FTS, and does not pretend to generate all CBM language-resolution, file-manifest, vector or publication metadata. Stock CBM watchers/reindex may overwrite these additions; keep this test project offline and do not use production data. Native full pipeline publication parity is a separate acceptance gate.

## Codebase Memory bridge installation (experimental)

In a local CBM source checkout, copy cbm_neuron_import.h to src/. Add `#include "cbm_neuron_import.h"` beside the existing headers in src/main.c. Immediately after `cbm_alloc_init();` in main add:
```c
if (argc == 5 && strcmp(argv[1], "neuron-import") == 0)
    return neuron_import(argv[2], argv[3], argv[4]);
```
Build using the upstream Makefile.cbm instructions for your checkout. Do not replace your installed binary until verified. Use an already indexed isolated project with the daemon stopped; verify the configured database belongs to that project and root. This bridge does not verify the root itself. The native source must compile and accept real records before deployment.

## Sources / verification status

- https://github.com/ModernRelay/omnigraph/blob/main/docs/dev/ingestion.md
- https://github.com/LadybugDB/api-server
- https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c
- https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.h
- https://github.com/DeusData/codebase-memory-mcp/blob/main/src/graph_buffer/graph_buffer.h

Source inspected only; no live destination or CBM build was available in this environment. This is an implementation candidate, not a claim of three working integrations.
