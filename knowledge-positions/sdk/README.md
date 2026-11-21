# UKC/1 native Rust ingester

This implementation candidate targets the existing UKC/1 SDK contract and existing OmniGraph `KnowledgeItem`/`Relationship` native schema. It has **no LinkML runtime, no mandatory LLM, no embedding model**, and requires no MCP or hook.

## Build and run

```bash
cargo test --manifest-path knowledge-positions/sdk/Cargo.toml
cargo build --release --manifest-path knowledge-positions/sdk/Cargo.toml
knowledge-positions/sdk/target/release/ukc-ingest --root "$HOME/Developer/Github/quatrus-scratchpad" ingest --target kp-agent --graph knowledge --branch kp-working --deadline-seconds 30
```

The clock starts on invocation and stops after a native commit and exact-ID query. **30 seconds is a hard end-to-end limit**; a partial load, unknown reader error, or failed query is not a PASS. Results are emitted as JSON. The first run is a cold ingest, not a no-op rescan. Rust compilation is outside the ingestion clock.

A diagnostic scan without OmniGraph changes is available through `--root PATH scan`. The portable full logical records are saved atomically as NDJSON outside the source tree (use `--output` to override); the existing files remain the source authority. OmniGraph stores keyed, same-ID search/graph projections and native source locators, not a separate knowledge interpretation.

**Honest parser coverage:** Markdown = native pulldown-cmark event stream and actual byte offsets; Python, Rust, JavaScript/JSX/MJS/CJS, TypeScript/TSX = Tree-sitter native syntax nodes, byte ranges and field names; JSON = serde_json tree; CSV = native header and string cells. Supported code symbol types produce bounded source-structural nodes and observed containment edges. Other text formats are source-backed file records with no invented AST or semantic information. Unsupported binary formats are metadata/source backed. No classifier guesses semantic relationships. Real Markdown headings become bounded structural records with observed containment/sequence edges.

**Compatibility boundaries:** This is a new SDK candidate, not an automatic replacement for the current installed `~/.local/jitk-http/bin/jitk-scan`. That installed build's source is not present at the accessible GitHub path; its LinkML per-record call site cannot safely be edited by pretending the older checked-in scanner is the active one. The existing OmniGraph schema and stored `item($id)` query must be installed. The projected fields match that schema; full native parser output lives in the same-ID sidecar.

The ingester intentionally refuses to write protected `main`. It does not automatically import accepted prior enrichment or reconcile supersession/history yet, so **do not promote this candidate to production maintenance** until those lifecycle requirements and cross-language SDK conformance are demonstrated. The 30-second goal remains a measurement requirement, not a claimed achievement.

Generated paths `.git`, `node_modules`, `target`, `.venv`, `venv`, `__pycache__`, `.cache` are explicitly excluded; symlinks are noted but not followed. All other regular files, including unknown binary formats, are represented. Source byte counts, coverage, errors and exclusions must be reported rather than silently omitted.
