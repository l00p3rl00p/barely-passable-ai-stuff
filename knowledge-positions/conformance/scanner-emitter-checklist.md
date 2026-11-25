# Scanner-to-Neuron Connector validation checklist

Conformance checklist for the link between a **Scanner** (parses every native output without filtering) and a **Neuron Connector** (the emitter, which serializes and writes those outputs through the destination's native interface). Use it for any destination. A result is only a result when the real path was run: a real input, the real destination, and the real failure modes. Mocks do not count.

Status of any particular implementation belongs in that project's own status record, not in this file. Follow the [native ingestion contract](../contracts/native-ingestion.md). All read-back, comparisons and fault injection below are external acceptance tests, never normal ingestion responsibilities. Use authorized, isolated test destinations.

## 1. The checklist

Each item says what must be true, how to check it, and what counts as evidence.

| # | Requirement | How to check | Evidence that counts |
|---|---|---|---|
| 1 | Every native output variant is accepted without Neuron Connector filtering | Scan one real file per variant the parser can emit (text, markdown, syntax tree, image, PDF, Office archive, binary member). Also scan an unsupported type. | Every supplied output and its kind are recoverable from storage, regardless of native row layout or fragmentation. |
| 2 | All exposed supplied information survives serialization | Compare reconstructed stored outputs against the actual complete exposed parser outputs for the same parser, grammar and version. | All exposed fields, types, values and relationships match; counts and spot checks alone are insufficient. |
| 3 | Native ordering and source coordinates are preserved | Check native ordering and coordinates against parser output, using the actual destination representation. | Order and coordinates match the supplied output. |
| 4 | Explicit relationships are preserved without inference | Find a native output that carries relationships. Check they are stored as given, with no edge the parser did not emit. | Stored relationships equal the parser's. If the scanner emits none, mark N/A. |
| 5 | Binary payloads survive without loss | Scan a file with a binary member (for example an Office archive with an image). Base64-decode the stored member and compare bytes. | Decoded bytes equal the original member. |
| 6 | Structured native diagnostics and metadata are preserved | Scan a file that produces a parser error and a file with metadata (image colour, EXIF). Read the stored diagnostic or metadata row. | The error variant and metadata fields are present in storage. |
| 7 | Oversized payloads fragment and reconstruct exactly | Scan a payload exceeding the actual native transport limit, where applicable. Reconstruct using the implementation's documented fragment representation. | All fragments present; reconstructed payload equals the supplied payload exactly. |
| 8 | Persistent identifiers stay stable for unchanged inputs and parser versions | Scan the same file twice. Compare ids. If the parser version is part of the identity, change it and compare again. | Identical ids on unchanged input. Document what a parser change does to ids. |
| 9 | Repeat ingestion causes no unintended duplication or stale information | Re-scan unchanged input: rows must not duplicate. Change a file and re-scan: check what remains. | No duplicates on rerun. Stale rows are either removed by a rule or kept by a documented decision. |
| 10 | Scanner and Neuron Connector compile | Build both. | Clean build. |
| 11 | Scanner and Neuron Connector tests pass | Run the unit tests of each crate or package. Record the count. | All pass; a zero-test package is reported as zero, not as pass. |
| 12 | Authorized native writes succeed | Scan into the real destination with a valid credential and branch. Read the rows back. | Rows present and matching the source. |
| 13 | Native write failures propagate correctly | Force real failures without mocks: a bad credential (auth error), an unknown graph or table (not found), a protected branch (refused by the applicable authorization boundary). Check the exit status and that nothing was written. | Non-zero exit with the actual error; no effects for a refused write. Previously acknowledged batches may remain; do not claim atomicity across independent writes. |
| 14 | Explicitly retryable failures are handled correctly | Trigger a retryable failure from the destination (for example a conflict or rate limit that the destination marks as having no effect). Check whether the Neuron Connector retries, how many times, and with what delay. | Retry happens only for responses the destination marks as safe to retry, within a limit. |
| 15 | Unknown write outcomes are not blindly replayed | Interrupt the connection after submission or induce a timeout with an uncertain write outcome. Distinguish failures known to occur before submission. Check the Neuron Connector reports "outcome unknown" and does not resend. | One attempt; error names the uncertainty; the operator reconciles before retrying. |
| 16 | No additional confirmation write occurs | Count writes per scan in the destination's history. | One load per batch; no extra marker writes. |
| 17 | No separate confirmation report exists | Search the Neuron Connector's output for receipt or report files. | None written by the Neuron Connector. |
| 18 | No Neuron Connector-generated admission bookkeeping exists | Search the Neuron Connector for admission, marker, or receipt logic. | None; the only confirmation is the destination's own commit identity. |
| 19 | No Knowledge Positions processing occurs in the Neuron Connector | Search the Neuron Connector for knowledge-record or enrichment logic. | None. Knowledge Positions belong to the KP Writer and KP Enricher. |
| 20 | Execution time and memory overhead are measured | Time and measure peak memory of real scans over several runs, release build, with and without the Neuron Connector where possible. | Median and peak values with the build type and input size named. |
| 21 | Architecture documentation matches the implementation | Read the architecture doc against the code and the folder names. | Names, responsibilities and claims agree with the code. |

## 2. How to run the failure tests without mocks

- Use the real destination and the real credential path. Inject faults through the configuration the destination already reads (a bad token, a wrong endpoint, a wrong graph name, a protected branch), not through a fake server.
- Keep failure runs free of success side effects. Use a unique test file for each run so any accidental write is traceable.
- Never hide stderr on a run meant to fail. A run that was meant to fail and succeeded has written real data.
- Count rows before and after. A test designed to refuse all writes must leave the count unchanged. For mid-run failures, account for previously acknowledged writes and reconcile uncertain outcomes.
- Record the exit code and the destination's error body for each run.

## 3. Common errors and where the fix belongs

Each entry names the component that owns the fix. Errors that disappear when the owning component is fixed are marked.

| Symptom | Cause | Owner of the fix |
|---|---|---|
| Rows for a file look missing when querying | Query used a different path spelling than the stored canonical path | Query side (use the stored address; the scanner resolves to the on-disk path) |
| Parallel writes to one branch fail with a conflict on some files | Each file is a separate load; concurrent loads move the branch head | Neuron Connector (batch rows into fewer loads; retry only responses marked as having no effect) |
| A directory scan stops at the first failing file and the rest are never written | A per-file error propagates to directory traversal | Scanner (owns traversal and continue/stop policy); Neuron Connector propagates native write failures |
| The same file scanned twice produces a second set of rows after it changed | Identity is per version; changed content makes new ids and old rows stay | Destination policy (keep history, or define a removal rule) |
| An unsupported format exits with an error and writes an `unsupported` marker row | The scanner has no parser for the format | Scanner (add a parser, or document the format as unsupported) |
| Tree-sitter node counts differ between two runs | Two different grammar or library versions | Scanner (pin the versions used for the parse) |
| A status query prints a line before its JSON output | The CLI prints the target line first | Query side (parse from the first `{`) |
| Fault-injection run wrote data | A failure test was run without suppressing the success path | Test procedure (see section 2) |
| A destination's retry advice is ignored | The Neuron Connector only retries one specific code | Neuron Connector (read the destination's disposition field, not only the status code) |

## 4. Lessons from executing the checklist

- **Refuse before you write.** Reject invalid operations at the earliest applicable authorization boundary; the destination remains authoritative for its own permissions.
- **Batching beats retrying.** Forty single-file loads at once caused conflicts; the fix is fewer, larger loads, with a bounded retry for responses the destination marks as safe.
- **Stop on structure, record on content.** Directory traversal and its continue/stop policy belong to the Scanner, not the Neuron Connector. Record failures under the chosen Scanner policy.
- **Canonical identity.** Stored addresses use the on-disk path. Queries that use another spelling return nothing and look like a failed write.
- **Test sources are real writes.** Keep a list of every test source written to a live destination, so it can be removed deliberately.
