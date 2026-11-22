<!-- quatrus-ingestion:start -->
## Quatrus: scan, rescan and discover knowledge

Use the installed Rust ingester for requested files and folders; use native OmniGraph for discovery. Keep the existing MCP servers and permissions. No separate skill or MCP is needed.

Default shared destination: target `kp-agent`, graph `knowledge`, branch `kp-working`. Use the same branch across sessions unless the human specifies another authorized branch.

For a scan or rescan, invoke the existing **knowledge-positions MCP** tool `kp_rescan` with `{"source":"/absolute/path/to/folder","branch":"kp-working"}`. The tool calls the installed Rust ingester using existing credentials. Native OmniGraph creates the branch from main only if it is absent; it never recreates an existing branch. Do not invoke the old no-argument configured-corpus maintenance path for a folder request. Do not substitute shell ingestion for a failed MCP request; diagnose the actual failure. Use the local stdio workspace or explicitly configured `KP_LOCAL_READ_ROOTS` for source access.

Use the canonical installed Knowledge Positions LinkML schema. Reuse native admission/retry; never expose credentials, silently fall back to legacy ingestion, or replay uncertain writes. Report observed duration, files, items, relationships, failures and load receipts. Merge refresh does not yet reconcile deleted/changed IDs or preserve all prior enrichment; do not claim full lifecycle maintenance.

For discovery use the existing OmniGraph MCP stored query search on the same branch (inspect its actual parameter schema), or native CLI:

```bash
omnigraph query search --target kp-agent --graph knowledge --branch kp-working \
  --params '{"q":"subject to investigate"}' --json
```

Use parameterized queries. Verify the original using kp_read with the returned ID and matching branch. If an absolute local source is outside the MCP's configured allowed roots, read it with the local client's existing filesystem permissions; verify its stored byte span and hash. For native document coordinates, use the original native reader and verify the extracted span digest; do not claim verification when unavailable. Use existing stored item_rows to obtain the exact locator and hashes if needed. Do not confuse a graph locator with authorization.

Acceptance: a fresh Codex session ingests the requested folder; an independent fresh session discovers by subject on the shared branch and verifies the original evidence, without prior chat context. Follow the permanent mission and canonical Knowledge Positions research; do not invent a replacement framework.
<!-- quatrus-ingestion:end -->
