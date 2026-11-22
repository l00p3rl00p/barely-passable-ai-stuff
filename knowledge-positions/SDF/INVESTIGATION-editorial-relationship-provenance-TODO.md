# Public checklist — historical relationship provenance

> **PUBLIC REPOSITORY NOTICE:** This checklist is public. Do not publish private conversations, model-session excerpts, local file paths, internal infrastructure, unpublished investigative notes, or personal details.

- [x] Inventory the committed historical companion: 28 sections, 57 edges, including 30 non-sequential editorial links.
- [x] Check available Git history for the first committed companion and associated paper/code revisions.
- [x] Compare source- and section-level hashes, relationship identifiers, evidence labels and indexed data.
- [x] Inspect the Python materializer, current section indexer and limited AST/OKF alpha for their actual inputs and outputs.
- [x] Establish that the materializer imports previously saved editorial links rather than deriving them from source text.
- [x] Check three-touch code chronology and saved records; no publicly committed touch history proves the origin of the 30 editorial links.
- [x] Review committed database materialization paths; no public database creation trace establishes the editorial links' authoring process.
- [x] Assess deterministic compatibility: 15 section hashes unchanged, eight editorial edges with both endpoints unchanged; 22 need separate review.
- [x] Record publicly reproducible findings and their limitations in [the technical note](INVESTIGATION-editorial-relationship-provenance.md).
- [x] Run independent Python and JavaScript reconstruction against the current public paper; assert same source-backed `ukc/1` identities, fields, lexical vectors, eight qualified recovered editorial edges and inactive mismatched history. Tested in [CI](../../../.github/workflows/paper-reconstruction.yml).
- [x] Check this paper example against the existing shared-record contract; it uses one `ukc/1` record per section and passes full-paper parity, source resolution, stale-source rejection, and `x_ukc` export checks. Full source-agnostic SDK certification was **not the scope of this example** and is not claimed.

**Evidence boundary:** The first committed companion contains the relationships already; the repository does not establish the authoring procedure for each editorial link. Do not invent a creator, a missing script, or a database-writing event.

**Public release rule:** Refer only to published repository artifacts. Any non-public investigative evidence must remain outside the public repo unless explicitly approved for publication.

## Closure — tested public example

The [complete SDF example](examples/README.md) and [CI test](../../../.github/workflows/paper-reconstruction.yml) passed on the current public paper: 29 records, 15 matching historic sections/vectors, eight recovered editorial relations, 22 inactive editorial relations, Python/JavaScript parity, source integrity, OKF `x_ukc`, and three-touch regression tests. Historical records were not modified. Publication safety: only public repository evidence appears in this note; working conversation material remains outside the public tree.
