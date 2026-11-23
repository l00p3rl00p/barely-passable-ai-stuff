## 10. Mandatory conformance suite: no claims without execution

Implementations MUST publish a language-neutral fixture runner and real, inspectable outputs. Fixture input includes raw source bytes, source identity/version, parser observations, native attributes and observed edges. Output includes canonical ID input bytes/hash, logical records, relation lists, vector space, exact resolved source bytes and export/import verification.

| Test | Required behavior |
|---|---|
| **UKC-01 SAME ITEM** | Enter through a title/literal name, native structural selector, observed graph link, or available vector result for the same unit. Every path resolves **one exact canonical ID and the same known shared values** without converting one method's representation to another. |
| **UKC-02 TREE IS GRAPH** | Real parsed parent, child and sibling order are immediately traversable as observed edges. No invented semantic edges. |
| **UKC-03 LITERAL PRESERVATION** | Arbitrary native fields, Unicode, punctuation, source bytes and source hierarchy survive OKF export→import unchanged. |
| **UKC-04 HONEST UNKNOWN** | Missing vector, missing title and unknown relation/location remain explicitly unknown; no defaults invented as facts. |
| **UKC-05 IMMEDIATE INGEST** | Admit without any LLM/encoder/network dependency; source/graph/lexical access works before vectors are computed. |
| **UKC-06 KNOWN EDGE** | A real input link or named relation is queryable immediately, with original direction, type and provenance. |
| **UKC-07 ENRICHMENT DELTA** | A verified later relation adds only the evidence-backed relation, leaves source/native fields intact and is idempotent. |
| **UKC-08 VECTOR PROFILE** | A single implementation rejects mismatched declared vector profiles and deterministically reproduces its own declared encoder output on identical input. When cross-language implementations are available, equivalent profiles must produce equivalent vectors; cross-language parity itself is assessed under UKC-12. |
| **UKC-09 IMPERFECT LEAD** | A candidate with no direct answer leads via neighbor and source location to precise evidence; this is an end-to-end investigation test. |
| **UKC-10 SOURCE CHANGED** | Changed source bytes refuse stale exact reads while preserving prior evidence and versions. |
| **UKC-11 RECONSTRUCTION** | Recreate graph/lexical/vector projections from original sources and accepted discovery records; no re-reasoning of previous discoveries. |
| **UKC-12 CROSS-LANGUAGE** | Independent language implementations consume identical fixtures and agree on IDs, fields, observed edges, source bytes and encoder-specific vectors. |
| **UKC-13 ACCESS** | Knowing a private locator does not grant read access; current authorization controls resolution. |
| **UKC-14 SOURCE AGNOSTIC** | Code plus an HTML, Markdown, prose or conversation source preserve their actual values in the same common-record contract, accessible by applicable methods without fabricated universal AST or separate position records. |
| **UKC-16 PARSER AND ON-TOUCH ENRICHMENT** | Admit Woburn fixture through unchanged generic CommonMark parser: full text/AST survives, but postal code and coordinates are not individually labeled. Touch the same record for a location task and run a separately declared location-aware parser or evidence-grounded LLM enricher: append the recognized existing location facts and any justified relationships to **that same ID**; do not rewrite original text, require full-corpus enrichment, or imply the original parser extracted those fields. A native location parser may capture the same fields immediately. Repeat enrichment without duplication. |
| **UKC-17 GENERAL SOURCE EXAMPLES** | Run the seven-source reference characterization against actual language-native parsers and its recorded bytes: code, two webpages, cookbook, chapter, CSV, opaque binary. All seven preserve one source identity, exact source position, observed containment/links and available lexical proximity input; queries select from the same records, with zero mandatory model calls or vector generation. |
| **UKC-18 COLD CONTEXT AND RECOVERY** | Hold sources and accepted findings constant, clear all derived indexes, reconstruct, ask an evidence-backed question twice in independent cold runs; verify useful evidence/identity recovery without asserting word-for-word answer identity. Then show an on-touch qualified discovery changes future knowledge while untouched sources and records remain unchanged. |
| **UKC-19 NATIVE PARSER FIDELITY** | For each declared fixture, record the **actual returned parser tokens/events/AST/rows**, the exact parser and version, source bytes/hash and coordinate system. Verify native fields and original bytes survive common-record mapping. Distinguish raw parser output from filesystem metadata, adapter extraction and on-touch enrichment. In particular: CommonMark chapter link is an inline child; HTMLParser is an event stream; CSV cells are strings; opaque binary needs no content parser. |
| **UKC-20 FIELD CROSSWALK AND GRAPH READINESS** | For each reader, compare real native parser fields to a declared versioned x_ukc crosswalk; preserve fields not directly searchable; verify source-vs-parser provenance and original coordinate units. Exercise twelve graph algorithms on source-backed topology using their mathematically correct detached views; record valid empty/no-path/cycle/not-applicable outcomes without fabricating edges or weights. Repeat against new-language implementation using the same fixture. |
| **UKC-15 ORIGINAL PROOFS** | Re-execute real OpenKC lossless translation/observed-edge proof and GPS source navigation replay, recording what was actually tested. |

**Single-language core certification requires UKC-01 through UKC-08, UKC-10, UKC-11, UKC-13, UKC-14, UKC-19 and UKC-20, tested against that implementation and the shared fixtures.** A second language implementation is not a precondition for single-language certification. Only advertise capabilities actually implemented and tested. UKC-09 and UKC-15 are required end-to-end demonstration evidence; do not substitute a mocked trace for the original recorded experiments. **UKC-12 is required to claim parity between two language implementations.** If the conformance fixtures/runner do not yet exist, this spec is a defined contract, **not a claim of certified SDK completion**.

Maintain portable actual fixtures, expected IDs, encoded hash input bytes, original blobs, expected relations, encoder outputs and test reports under a shared **conformance/** directory. A future language must run the same fixtures rather than invent new “equivalent” ones. No pinning of a specific language implementation is required.

### Invalid implementations, regardless of apparent usefulness

A claimed UKC SDK **fails** when:
- It maintains separate AST, graph and vector *interpretations* with unrelated IDs.
- It needs an LLM to turn already supplied parent/child/links into observed graph edges.
- It loses source-native values during “conversion.”
- It invents relationships from title similarity or embeddings and presents them as observed.
- It cannot trace a candidate through the same ID and relation to the original source.
- It forces embedding or corpus-wide enrichment before indexing a source.
- It aliases incompatible vector algorithms under the same space name.
- It requires all source types to become synthetic Python AST.
- It uses only a disposable graph store for hard-won prior discoveries.
- It passes an example but cannot pass the common conformance contract.

