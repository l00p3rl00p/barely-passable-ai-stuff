# Runbook — install by copying files

Prerequisites: an ordinary OmniGraph installation (reference API/CLI 0.15), Python 3.10+, and an authorized native target. See https://www.omnigraph.dev/docs/cli and https://github.com/ModernRelay/omnigraph-cookbooks. No embedding provider.

## 1. Copy this folder anywhere

Keep schema.pg, queries/kp.gq, adapter.py, knowledge_positions.py, encoder.py, requirements.txt and tests together. Copy the entire skill/ directory (including references/) to your agent's normal skill directory as knowledge-positions-omnigraph; record the actual bundle location in the agent configuration. Keep the upstream OmniGraph skill.

From the copied directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
omnigraph lint --schema schema.pg --query queries/kp.gq
```

## 2. Choose where the graph lives

Standalone (new graph only):

```sh
omnigraph init ./knowledge.omni --schema schema.pg
```

For a cluster: copy schema.pg and queries/kp.gq into your existing cluster configuration directory (choose distinct filenames if other graphs already use them); add/update the graph's schema and queries references in cluster.yaml, retaining all unrelated graphs, policies, storage and actors. The included cluster.example.yaml illustrates a separate new graph, not a replacement for your cluster configuration. Use the current native CLI:

```sh
omnigraph cluster validate --config /path/to/cluster-config
omnigraph cluster plan --config /path/to/cluster-config --target YOUR_ADMIN_TARGET
omnigraph cluster apply --config /path/to/cluster-config --target YOUR_ADMIN_TARGET
```

Inspect the plan before applying. Do not replace an existing incompatible schema or remove populated semantic columns blindly: keep existing data, back up and use native migration instructions. For an existing graph, merge compatible schema/query declarations rather than replacing unrelated types. Existing graph credentials and permissions are unchanged. Use an authorized native target on the graph/branch where work belongs; no special identity required.

## 3. Capture and use real knowledge

Use actual reviewed UTF-8 source files, not example data. The adapter reads and hashes the specified span; it does not write source files. Source path must be accessible to the consuming machine (or use a stable shared source ID and put the source at its recorded path). Restrict private data to its authorized graph. The graph includes derived lexical terms, not a privacy boundary.

```sh
python adapter.py --target ./knowledge.omni capture /path/to/actual.md --domain my-domain --reviewed
python adapter.py --target ./knowledge.omni search "actual subject"
python adapter.py --target ./knowledge.omni item ITEM_ID
python adapter.py --target ./knowledge.omni read ITEM_ID
python adapter.py --target ./knowledge.omni neighbors ITEM_ID
python adapter.py --target ./knowledge.omni link ITEM_ID OTHER_ID related_to "Actual evidence" --reviewed
python adapter.py --target ./knowledge.omni enrich ITEM_ID "Actual new understanding" --reviewed
```

For a server/cluster, replace --target ./knowledge.omni with --target YOUR_TARGET --graph YOUR_GRAPH; add --branch YOUR_BRANCH if appropriate. Native stored queries are used there. Direct graph targets use queries/kp.gq. For capture, --start/--end select inclusive source lines; --kind and --heading describe the actual unit. Capture a second actual source before linking. The CLI uses a transient native NDJSON request file, not a parallel knowledge store. No manual JSON authoring.

Enrichment uses native --if-commit conditional mutation. On a conflict, re-read and reconsider; never blindly retry. Native merges remain governed by OmniGraph; cross-branch budget validation is not supplied. Native permissions still govern every operation.

## 4. Acceptance (real engine, no mock)

Using a dedicated new graph, run Step 3 with two actual documents. Repeat capture with the same file/coordinates/domain and verify the same ID and no new row. Open a new process, locate the ID directly, search by actual terms, follow the relation in both directions, and read the source. Enrich twice with different findings; a third enrichment must fail. Repeat the same finding before freezing: no additional touch. Modify a source only in your own disposable test copy and confirm read refuses the changed hash. Inspect the native graph and ensure the recorded vector has 512 entries and no provider fields, and the native skill can query the new graph. Do not call this accepted if any command fails. No automatic bulk scan, lifecycle reconciliation, cross-branch enrichment enforcement, OKF conversion or resonance implementation is supplied by this minimal adapter.

## 5. Updates

Keep these files separate from OmniGraph engine installation. After an engine upgrade, follow native upgrade instructions, rerun lint/plan and acceptance; copy or redeploy the schema and queries only if needed. Never initialize over live data. Preserve reviewed meaning and relationship evidence before rebuilding. No installer or batch file.
