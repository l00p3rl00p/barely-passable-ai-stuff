# Independent SDF improvement review

Review the baseline and resulting commit directly. For each item record PASS / FAIL / BLOCKED, path/section or command, expected/observed result and evidence. Do not certify on prose or edit count.

- [ ] SDF entry point gives a natural reading path and direct shortcuts for users of existing kits; all links resolve.
- [ ] JITK, KP, UKC, OKF, SDF, kits and research retain their separate responsibilities.
- [ ] One capture reference answers all minimum fields, types/forms, conditions, provenance, unknowns, stages and validation; no hidden requirement in a kit or historical experiment.
- [ ] Canonical identity bytes, prefix and tuple unchanged; shared fixture tests confirm.
- [ ] One authoritative lifecycle; native ingestion unaffected; supplied edges at touch 0, derived deterministic structure at touch 1, qualified intelligence touches 2–3.
- [ ] Block grouping is required where source-supported; native groupings may be reused, improved or extended without overwriting evidence. Incomplete grouping and oversized inputs never silently discard information.
- [ ] Cookbook contains SIPOC boundaries, native capability assessment, assembly instructions, expected outputs and actual check-your-work steps.
- [ ] Scanner is universal; emitter, writer, enricher and optional MCP are destination-specific; standalone KP does not require JITK ingestion.
- [ ] Native capabilities are reused rather than rebuilt; support gaps are explicit.
- [ ] Pinned OKF interchange is validated; storage representation is not forced to be OKF YAML.
- [ ] Existing UKC IDs, working entry points, configurations, historical evidence and tests are preserved.
- [ ] All 28 handoff changes have an explicit disposition; any new behavioral restriction is distinguished from approved corrections.
- [ ] Run existing local tests before/after; record results and gaps, no CI required.
- [ ] Validate lifecycle and writer/enricher actual outputs against existing requirements; do not claim completion for unimplemented checks.
- [ ] Cold-reader test: given only the SDF entry point, an independent reviewer prepares a SQLite kit requirement inventory without reading OmniGraph implementation or historical experiments. Compare with capture and conformance contracts; report omissions.
- [ ] Compare baseline vs result: number of sources required to discover capture obligations, conflicting lifecycle definitions, navigation steps, code regressions and executed coverage.

A passing documentation review is distinct from kit certification. Blocked or unexecuted runtime checks remain open.

## Handoff disposition (SDK-EDITS-PLAN.md at quatrus-scratchpad 268605b)

| IDs | Disposition |
|---|---|
| E1–E6 | Consolidated normative lifecycle; corrected active references. E6 verified on published baseline and corrected. |
| E7, E24 | Specify interchange mapping without changing internal staleness. Preserve rejection of stale exact reads; runtime export mapping remains unverified. |
| E8–E14 | Outstanding implementation work: legacy Python uses old touch/status and cluster semantics. Do not change defaults alone or silently alter saved graphs and existing tests. D10: actual deterministic creation is touch 1; D11: do not infer draft exclusion from OKF status. |
| E15–E20 | Historical/research code unchanged; preserve original evidence and report its lifecycle as legacy. Update active consumers when their compatibility is tested. |
| E21–E22 | Consolidated event grouping and unit-key rules; capture unmatched native events without manufacturing a complete block. |
| E23 | Clarified interchange vs native storage. |
| E25 | Assigned span digests to reader with actual bytes; stage declared. |
| E26 | Consolidated capture table instead of pointer-only solution. |
| E27 | Established SDF entry and native target cookbook without directory moves. |
| E28 | Added executable conformance checks instead of mandatory new planning records. |

D6: follow upstream bundle-relative path resolution, with repository root only when it is the actual bundle root. D8: preserve internal source-change behavior; stable plus stale_after on interchange must be tested. D10/D11 as above. Re-pinning deployed scanner, verifying live OKF checkout, and completing target implementation are outside this documentation commit and remain unverified.

## Review execution — 2026-11-27

Baseline: existing navigation branch at e82a1fb66d12746a316aa84f84cdc01ac4c88319. The existing native-ingestion contract, scanner/emitter checklist and JITK architecture guide were brought forward unchanged from published main f3dc42e; no directory or runtime migration was performed.

| Checklist area | Result | Evidence |
|---|---|---|
| Entry point, conceptual separation, navigation | PASS | SDF/README.md is the guided entry; unified-knowledge-context.md is the detailed index. Local link/heading checks on changed Markdown: zero broken paths/anchors. |
| Capture requirements, identity, vocabulary | PASS (documentation) | One common-record table; general field crosswalk consolidated; conditional vector profile and legacy aliases included after independent review. core/identity.md byte-identical to baseline. |
| Lifecycle, grouping, native boundaries | PASS (documentation) | core/lifecycle.md owns touch model and grouping; no old admission-is-touch-1 statements in active core/contract/vocabulary/architecture guidance. Coverage explicitly labels legacy behavior. Required fixture cases documented separately. |
| Target independence and cookbook | PASS (documentation) | SIPOC and native capability matrix, native scanner reuse, target-specific assembly and recipe checks. Moved Python-only graph-view and retrieval examples to existing Python guide; retained anchors and links. |
| Existing code/config and historical evidence | PASS | Git staged diff contains only Markdown. No code, identity profile, research manuscript, existing examples, workflow or configuration altered. |
| Regression suite | PASS | Baseline and result: PYTHONPATH=. python -m unittest discover -s tests -q, 20/20 each. Reference smoke check: PYTHONPATH=. bash tools/check-sdk.sh passed. Existing paper test: PYTHONPATH=. python tests/test_paper_reconstruction.py passed before/after (29 records, 15 matching sections/vectors, 38 structural and 8 qualified editorial edges, 22 inactive); historical x_ukc export, not current OKF certification. |
| Conformance identifiers | PASS | UKC-01 through UKC-20 unchanged; git diff --check passed. Upstream pinned spec retrieved at exact commit and confirmed version 0.3. |
| Independent cold-reader test | PASS for architecture/discoverability after corrections; BLOCKED for runnable certification | Independent reader inventoried SQLite implementation from SDF entry without OmniGraph/research. Identified missing vector metadata, aliases, graph operations link, profile certification clarity and separate touch cases. Docs corrected; reader recheck confirmed first three corrections; touch cases explicitly specified afterward. Shared executable conformance fixture package/runner remains absent, as existing authority doc records; no invented substitute. |
| Current Rust writer native completeness | FAIL (source review) | quatrus-scratchpad commit 268605b, jitk/rust-scanner/omnigraph-writer/src/kp.rs explicitly catches payload_too_large, skips and reports addresses; no complete admission. Writer touch 0 is present in source. |
| Current Rust enricher/grouping | FAIL (source review) | Same commit, src/bin/kp-omnigraph-enricher.rs is legacy path re-key only, not touch-1 grouping. |
| Current live target runtime, full OKF round trip, complete coverage and idempotency | BLOCKED | No live OmniGraph or Rust toolchain in this review environment. Historic writer run reports idempotency for admitted records but skipped three addresses; no fresh live conformance claim. |

Review outcome: documentation improves discoverability and preserves existing code. Full UKC/kit certification is not achieved; shared fixtures, actual Rust grouping, oversized admission and live OKF round-trip validation remain open.


## Human operational readability review — follow-up

**Test:** Enter from the repository root, the Knowledge Positions directory, the SDF directory, or a framework subdirectory. A reader must discover a starting point, a single next action and a return path without reading all documents. A long directory listing is not a reading guide.

| Scenario | Expected path | Result |
|---|---|---|
| New reader at repository root | Knowledge Positions or SDF entry link | PASS — root now links both and separates unrelated design skills. |
| New reader at KP root | Choose one goal before Python/reference material | PASS — five routes, explicit default: SDF. |
| Builder at SDF | First Law → capture → lifecycle → cookbook → conformance | PASS — one primary link per step, stopping criteria and supporting links. |
| Reader browsing contracts, core, methods, readers, docs, conformance or languages | Folder README identifies primary starting point and return to SDF | PASS — seven short navigation indexes; no new requirement definitions. |
| Reader lands directly on a core requirement | Return to SDF, next step or corresponding recipe | PASS — navigation links on foundational documents. |
| Rust implementer | Rust source and limitations, not historical workspace or Python by default | PASS — pinned inspected source links; current installation and runtime not claimed. |
| Reader wants historical proof or optional profiles | Clearly separated from normative sources | PASS — examples, paper and legacy connector labelled; no need to interpret them to build a kit. |

The local link audit examined 107 Markdown files (repository README plus all Knowledge Positions Markdown files, including seven new folder navigation indexes), ignoring fenced illustrative source and excluding the separately archived and version-matched upstream skill bundle from active framework validation. All active local links/heading anchors resolved after correcting the historical quick-start entry and two relative investigation links. The bundled upstream skill references require its official companion directory, as the bundle README already explains; its upstream content was not modified. External Rust source references were inspected at the pinned revision. This is a navigation/readability check, not evidence of a new runtime implementation or full certification.

Measured navigation: from the repository root, the SDF guide is one click away and capture, lifecycle, cookbook, conformance and Rust source guide are each at most two. From the SDF guide, each is a direct link. Existing local reference-library tests passed 20/20; no code changed.
