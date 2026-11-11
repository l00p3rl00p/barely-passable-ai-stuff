# GPS experiment: cold-context retrieval

This is the 28-line representative fixture used in the original trial, not a full transcript. Install the parent library first, then from this directory run:

```bash
python gps.py build --source source.txt
python gps.py search "SDK codebase"
# Copy a node ID from the current search output:
python gps.py neighbors <NODE_ID>
python gps.py read <NODE_ID> --source source.txt
```

Build generates index.json and index.sqlite. Give a fresh LLM only those files, gps.py and the installed library (not source.txt or the results below). Keep the source with a separate resolver. Ask: "What did we establish about connecting an SDK to an application's codebase, and why is that useful?" The agent should search, traverse and request specific node IDs. Resolve them with the read command and return only the requested passages. Because this public example includes the source and results, use an isolated agent without repository access for a blind trial.

## Original experiment outcome

The independent agent first selected 7fca407d89dd7f1b78e0edf99cacd00f6ffe24f25912dec971c72500f150ee22 and 0d9ff06f1c71716a10ffa3ea6888eec1b46a68f297bb10bd3de37e7763a7684e. It then requested upstream 55f87710006b396c3dfecf3ca17a2bebaa258b2316295354035217a86f599f98 and downstream c185a2dd7dbb148264024c9de16bf4de66eda126d90bd5af099972efafcf0130. It concluded that connection enables navigation, navigation replaces bulk loading, and human and LLM can navigate the same knowledge. This is a recorded result from the original conversation, not an automated benchmark.

## Limits and next tests

The fixture uses hashed lexical vectors, not semantic embeddings. To try real embeddings build with --model all-MiniLM-L6-v2; this needs the actual model and has not been tested in the original trial. Shared-term edges are co-occurrence only. Exact search is not ranked by BM25 in this implementation, and the pairwise edge build is quadratic. The index is not a privacy boundary: FTS terms and embeddings expose derived information. Source hashes verify bytes, not truth. The read command verifies the entire source before slicing; at scale use a verified immutable source version and seek. The published script replaces assertion-based integrity checks with explicit errors so checks remain active under Python optimization.

Next: paraphrase retrieval, corpus-specific term weighting, optional hybrid ranking and bounded context windows, evidence-backed relationship write-back, and a large-corpus trial. Keep search/traversal choice with the LLM; the library executes the operations. No claim of production scaling.

See [coverage and warnings](../../COVERAGE.md) for the mapping to the original specifications and notebook checks. Historical IDs above describe the recorded trial; rebuilt IDs depend on the source version and identity algorithm. The current example is a reproducible implementation, not a byte-for-byte archive of the earlier executable.
