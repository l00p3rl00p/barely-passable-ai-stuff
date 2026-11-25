# Scanner-to-Emitter validation checklist

Conformance checklist for the link between a **Scanner** (parses every native output without filtering) and an **Emitter** (serializes those outputs into one destination, OmniGraph first). Use it for any destination. A result is only a result when the real path was run: a real input, the real destination, and the real failure modes. Mocks do not count.

Status of any particular implementation belongs in that project's own status record, not in this file.

## 1. The checklist

Each item says what must be true, how to check it, and what counts as evidence.

| # | Requirement | How to check | Evidence that counts |
|---|---|---|---|
| 1 | Every native output variant is accepted without emitter filtering | Scan one real file per variant the parser can emit (text, markdown, syntax tree, image, PDF, Office archive, binary member). Also scan an unsupported type. | One stored row per output, with the output's kind. The emitter never drops a variant. |
| 2 | All exposed supplied information survives serialization | Compare stored event or node counts with the parser's own count, run independently (a second parser build, or the unit test that counts events). Read the stored payload back and compare fields. | Counts equal; a field-level spot check matches the source bytes. |
| 3 | Native ordering and source coordinates are preserved | Check `seq` is contiguous from 0 for each source. Check a byte range against the source text. | Contiguous `seq`; ranges point at the expected bytes. |
| 4 | Explicit relationships are preserved without inference | Find a native output that carries relationships. Check they are stored as given, with no edge the parser did not emit. | Stored relationships equal the parser's. If the scanner emits none, mark N/A. |
| 5 | Binary payloads survive without loss | Scan a file with a binary member (for example an Office archive with an image). Base64-decode the stored member and compare bytes. | Decoded bytes equal the original member. |
| 6 | Structured native diagnostics and metadata are preserved | Scan a file that produces a parser error and a file with metadata (image colour, EXIF). Read the stored diagnostic or metadata row. | The error variant and metadata fields are present in storage. |
| 7 | Oversized payloads fragment and reconstruct exactly | Scan a text file over the emitter's size limit. Check ids of the parts (`<source>:<seq>:<i>/<n>`). Join the parts in order, decode, compare with the original. | All `n` parts present; decoded join equals the original. |
| 8 | Persistent identifiers stay stable for unchanged inputs and parser versions | Scan the same file twice. Compare ids. If the parser version is part of the identity, change it and compare again. | Identical ids on unchanged input. Document what a parser change does to ids. |
| 9 | Repeat ingestion causes no unintended duplication or stale information | Re-scan unchanged input: rows must not duplicate. Change a file and re-scan: check what remains. | No duplicates on rerun. Stale rows are either removed by a rule or kept by a documented decision. |
| 10 | Scanner and emitter compile | Build both. | Clean build. |
| 11 | Scanner and emitter tests pass | Run the unit tests of each crate or package. Record the count. | All pass; a zero-test package is reported as zero, not as pass. |
| 12 | Authorized native writes succeed | Scan into the real destination with a valid credential and branch. Read the rows back. | Rows present and matching the source. |
| 13 | Native write failures propagate correctly | Force real failures without mocks: a bad credential (auth error), an unknown graph or table (not found), a protected branch (refused before network). Check the exit status and that nothing was written. | Non-zero exit with the destination's own error; no partial write. |
| 14 | Explicitly retryable failures are handled correctly | Trigger a retryable failure from the destination (for example a conflict or rate limit that the destination marks as having no effect). Check whether the emitter retries, how many times, and with what delay. | Retry happens only for responses the destination marks as safe to retry, within a limit. |
| 15 | Unknown write outcomes are not blindly replayed | Make the destination unreachable mid-write (refused connection, timeout). Check the emitter reports "outcome unknown" and does not resend. | One attempt; error names the uncertainty; the operator reconciles before retrying. |
| 16 | No additional confirmation write occurs | Count writes per scan in the destination's history. | One load per batch; no extra marker writes. |
| 17 | No separate confirmation report exists | Search the emitter's output for receipt or report files. | None written by the emitter. |
| 18 | No emitter-generated admission bookkeeping exists | Search the emitter for admission, marker, or receipt logic. | None; the only confirmation is the destination's own commit identity. |
| 19 | No Knowledge Positions processing occurs in the emitter | Search the emitter for knowledge-record or enrichment logic. | None. Knowledge Positions belong to the KP Writer and KP Enricher. |
| 20 | Execution time and memory overhead are measured | Time and measure peak memory of real scans over several runs, release build, with and without the emitter where possible. | Median and peak values with the build type and input size named. |
| 21 | Architecture documentation matches the implementation | Read the architecture doc against the code and the folder names. | Names, responsibilities and claims agree with the code. |

## 2. How to run the failure tests without mocks

- Use the real destination and the real credential path. Inject faults through the configuration the destination already reads (a bad token, a wrong endpoint, a wrong graph name, a protected branch), not through a fake server.
- Keep failure runs free of success side effects. Use a unique test file for each run so any accidental write is traceable.
- Never hide stderr on a run meant to fail. A run that was meant to fail and succeeded has written real data.
- Count rows before and after. A failed run must leave the count unchanged.
- Record the exit code and the destination's error body for each run.

## 3. Common errors and where the fix belongs

Each entry names the component that owns the fix. Errors that disappear when the owning component is fixed are marked.

| Symptom | Cause | Owner of the fix |
|---|---|---|
| Rows for a file look missing when querying | Query used a different path spelling than the stored canonical path | Query side (use the stored address; the scanner resolves to the on-disk path) |
| Parallel writes to one branch fail with a conflict on some files | Each file is a separate load; concurrent loads move the branch head | Emitter (batch rows into fewer loads; retry only responses marked as having no effect) |
| A directory scan stops at the first failing file and the rest are never written | The emitter propagates the first error out of the loop | Emitter (decide: continue and collect failures, or stop) |
| The same file scanned twice produces a second set of rows after it changed | Identity is per version; changed content makes new ids and old rows stay | Destination policy (keep history, or define a removal rule) |
| An unsupported format exits with an error and writes an `unsupported` marker row | The scanner has no parser for the format | Scanner (add a parser, or document the format as unsupported) |
| Tree-sitter node counts differ between two runs | Two different grammar or library versions | Scanner (pin the versions used for the parse) |
| A status query prints a line before its JSON output | The CLI prints the target line first | Query side (parse from the first `{`) |
| Fault-injection run wrote data | A failure test was run without suppressing the success path | Test procedure (see section 2) |
| A destination's retry advice is ignored | The emitter only retries one specific code | Emitter (read the destination's disposition field, not only the status code) |

## 4. Lessons from executing the checklist

- **Refuse before you write.** Checks that fail before any network call (protected branch, unknown credentials) are the right shape.
- **Batching beats retrying.** Forty single-file loads at once caused conflicts; the fix is fewer, larger loads, with a bounded retry for responses the destination marks as safe.
- **Stop on structure, record on content.** A directory scan should keep going past a bad file and record the failure in a list for a later pass, instead of stopping.
- **Canonical identity.** Stored addresses use the on-disk path. Queries that use another spelling return nothing and look like a failed write.
- **Test sources are real writes.** Keep a list of every test source written to a live destination, so it can be removed deliberately.
