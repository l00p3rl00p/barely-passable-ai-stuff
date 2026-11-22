# Reconstructing enrichment state — source and evidence survive; the database does not have to

> **PUBLIC REPOSITORY NOTICE:** This is a technical workflow based on publicly committed Knowledge Positions examples. Do not publish private conversations, unpublished evidence, local host details, or private project records.

## Permanent principle

**Never be afraid to erase the database.**

The original sources and **durably admitted enrichment evidence** are authoritative; graph, lexical and vector database projections are disposable. If the database disappears, rebuilding the useful map should be an ordinary deterministic operation, not a loss of knowledge.

**Important invariant:** Source text alone may not contain discoveries made during prior work. To rebuild *enrichment state*, previously accepted relation/enrichment deltas must survive **outside the disposable database** in durable source-addressed records, source-control artifacts or an equivalent evidence ledger. A delta that was saved only inside an erased database cannot be reconstructed as an established historical observation. We can rediscover a candidate, but we must not pretend that its missing provenance was preserved.

## What the live-paper experiment proved

The historical companion preserved source-linked editorial navigation enrichment. In the later manuscript, section hashes and offsets changed. Using the saved old source, node IDs, original positions/hashes, lexical vectors, stable anchors, and prior relation endpoints, a deterministic procedure located the corresponding current endpoints of **all 22 changed-hash editorial relationships**. The other eight editorial links retained both exact endpoint hashes.

A separate blind lexical-vector search ranked the correct current section first for **27 of 28** historical sections and within the top five for **all 28**. The single second-ranked section was resolved by its source anchor. The result demonstrates **deterministic reconstruction of the historical navigational enrichment state and its present source locations**, with source qualifications preserved.

The 22 changed-hash links are relocated *historical navigation records*; location recovery does **not** independently revalidate their semantic meaning or warrant automatically promoting them into current accepted facts. Recovery of stable-anchor sections in one paper is not proof of universal recovery across erased identities, arbitrary moves, or rewritten/deleted evidence.

[Reproducible reconstruction program](relocate-historical-edges.py) · [Actual measurements and explanation](DETERMINISTIC-HISTORICAL-RELOCATION.md)

## Human-authorized recovery workflow

1. **Notice a changed source or missing projection.** A changed hash means bytes changed; it does not imply all knowledge disappeared. Keep historical records and their qualification. Detect changes at the finest source grain already available.
2. **Ask the human once:** “The source has changed, but previous Knowledge Positions and enrichment evidence are available. Want me to reconstruct what I can and review just the uncertain parts?” A database-loss recovery may also be initiated under an already established user authorization or operating policy; do not imply the prompt is a universal runtime prerequisite.
3. **Rebuild deterministically first.** Re-ingest original source-native structure; resolve stored identity, version, offsets, anchors, links and available vector spaces. Reconstruct **one shared knowledge record per identity** and reapply surviving evidence-backed enrichment deltas with their original provenance and admission status. Use exact matches first, then structural/positional/relational and proximity candidates. No model inference required for this phase.
4. **Produce a compact exception report:** exact recovered, relocated qualified historical, ambiguous, unsupported/unresolved. Include only affected IDs, changed evidence spans and candidate neighborhoods. Never bulk-dump all records back into a model.
5. **If uncertainty remains, do a surgical LLM review.** Give only relevant changed old/new passages and relationship evidence, ask whether the relationship is still supported, changed or unknown, and require cited current-source spans. Treat the model response as a *proposal* pending applicable admission controls; no similarity threshold alone validates semantic meaning.
6. **Admit only reviewed changes when authorized.** Do not silently overwrite prior evidence or change the original source. Preserve original versions and delta history; validate record IDs, source hashes, edge endpoints, provenance and authorization. Persist accepted deltas **outside the disposable projection**.
7. **Finish with measured status, not artificial completeness.** Report how much enrichment state was rebuilt and how many candidates remain qualified, uncertain, or unresolved. An imperfect recoverable map is much better than zero.

### The operating loop

**Durable source + accepted evidence → deterministic rebuild → compact exceptions → optional surgical review → qualified durable deltas.**

The database can be dropped and rebuilt. The accumulated intellectual work must be captured in durable evidence first.

## Execution boundary

The [published paper-specific Python program](relocate-historical-edges.py) **already executes** old-source validation, endpoint relocation, vector ranking and evidence-preserving reporting. The [Python/JavaScript current-paper examples](README.md) already reconstruct source-backed UKC/1 records and the eight exact-hash-compatible editorial links.

The human approval prompt, automated compact LLM review and durable cross-project delta admission are **described here as a reusable workflow**, not misrepresented as existing runtime hooks. This document adds no mandatory automatic background work or database deletion.
