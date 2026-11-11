# Precise location and access signals

**Portable design guidance, not an installed access-control system or a new OKF standard.** The [mission](MISSION.md) and the library's [three positions](CORE_VOCABULARY.md) stay unchanged.

## Three distinct facts

1. **Location:** retain owner/authority namespace, stable source identifier, actual address or opaque locator, observed source version and verified position (UTF-8 span, AST node, message ID, page/region, event offset) and span hash when available. A heading or search result is a `locator_only` lead, not verified evidence.
2. **Possible access:** describe the source realm and potential routes—`public_web`, `authenticated_web`, `provider_private`, `local_file`, `ssh_host`, `cloud_workspace`, or `repository`. Routes depend on environment: a workstation may reach a source unavailable to a web client. Labels are hints, never credentials or permissions.
3. **Actual current access:** verify *discover*, *read* and *write* separately using the real current principal, environment, connector and authorization. Unknown stays unknown. Knowledge of a location, a shared graph pointer or past access never grants present access.

Keep source content and write authority under the owner's control. A shared cross-knowledge graph may contain permitted summaries and qualified references, but never implicitly expose private transcripts, secrets or original source bytes. Use separate physical stores where required by real trust boundaries; an `owner` property within a universally readable database is not access control.

## Source location versus position inside a source

The external location (`x_jit_location`) answers *which authority/source/version/span and possible access route*. A separate per-node `item_location` answers *where within that item*: ordered structural path, parent path, sibling index and depth, with a basis and precision signal. The same information can be projected into portable producer-defined OKF fields, without pretending they are normative OKF keys.

`KnowledgePositions.record_item_position(node_id, path=[...], ...)` or `record_item_position(node_id, coordinates={'start_line': 12, 'end_line': 16}, ...)` maintains source-relative positions without changing source identity or vectors. A reader/parser supplies real structure, anchors or offsets with `basis='reader'`/`'parser'` and `precision='parsed'` only after verifying the original source; the library checks consistency against stored positions and source versions, but cannot independently certify an untrusted caller's claim. When only an LLM observation is available, use `basis='observation'` and `precision='locator_only'` without inventing a tree. The library, not the model, owns updates when called by a host reader or watchdog; no universal watcher is installed.

`positioned_embedding_input` provides source-hash-checked text with its structural path for an optional positional embedding input policy. Existing vectors stay unchanged unless explicitly regenerated under a separately declared representation policy.

## Shared location-method selection (source-agnostic)

Use the **strongest available verified method**, without forcing every source into a syntax tree. This is the library's ordered default; it is not a ranking of truth or a claim that all formats supply these coordinates.

| Order | Method ID | Source-appropriate examples |
|---|---|---|
| 1 | `native_structure` | DOM path, Python AST fields, XML/JSON tree, document object hierarchy |
| 2 | `stable_anchor` | Native heading/section identifier, named anchor, stable record key |
| 3 | `source_span` | Exact version-scoped UTF-8 byte offset, line/column span, page/region or time window |
| 4 | `observed_locator` | Descriptive visual/text clue with no source-reader verification |

**Rule:** verification precedes precision claims. Choose the highest supported method for the *actual source*, retain complementary verified coordinates (including line/byte spans), and never create an imaginary hierarchy just to fill a field. A known source revision is necessary to interpret offsets. An inaccessible source or LLM-described location remains provisional, even when its description sounds specific. DOM, AST and paragraph are examples, **not mandatory formats**.

`KnowledgePositions.record_item_position(...)` accepts `path` **or** `coordinates`, with `basis='reader'|'parser'|'observation'`, `precision='parsed'|'locator_only'` and an optional `method`. For example, a deterministic file reader may pass `coordinates={'start_line': 12, 'end_line': 16}` without a path. It adds/reuses source-version-scoped metadata without changing the content hash, node ID or stored vector.

**Unfamiliar coordinate system:** reuse an existing method whenever possible. If none fits, call `register_location_method('custom:<slug>', source_kind=..., description=..., verification=...)` and record the convention as **provisional**; `location_method_catalog()` returns the canonical order and those registered descriptions. The optional `location_methods` property is persisted with the graph JSON, so later readers get the same meaning. A custom method does not automatically acquire parser-verified status or priority. Publishing a sanitized method convention to other independently owned knowledge stores requires an authorized shared channel; registration does not synchronize private provider graphs.

**Maintenance ownership:** the host reader/watchdog supplies observed source changes, the library verifies/idempotently maintains positions. A model can submit a lead through this same API when necessary, ideally as an early verification task; it is not responsible for periodically repairing positions. No watchdog is currently installed.

## Example: OKF v0.2 location extension

[OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) permits custom YAML frontmatter fields. `x_jit_location` is an **illustrative producer-defined extension**, *not* a standardized OKF key. This intentionally represents an **unverified lead**, not a real private document or fabricated exact coordinates.

```yaml
---
type: Knowledge Reference
title: Illustrative document section
description: Source is identified, but read access is not established.
resource: https://example.org/private/guide#section-2
sources:
  - id: guide
    resource: https://example.org/private/guide
x_jit_location:
  owner_namespace: workspace:example
  realm: authenticated_web
  source_id: guide#section-2
  source_version_sha256: null
  position:
    selector: section-2
    start_byte: null
    end_byte: null
    unit: utf8_byte
    span_sha256: null
    precision: locator_only
  possible_routes:
    - environment: authorized_browser
      via: authenticated_https
  last_resolution: unknown
---
```

If a source is actually read, record its observed version, precise span/unit and digest, with supporting evidence. Do not guess missing offsets, leak keys or store global `accessible: true`. A resolver can keep per-environment observations outside portable OKF. Machine-proposed annotations are not human-reviewed facts, and the source remains authoritative.

## Recommended application pattern

**Two costs, not two mandatory import stages:** deterministic structural ingestion is cheap enough to operate across broad accessible sources (AST/schema, spans, identity, hashes, structural relationships). It does **not** call an LLM to interpret the corpus. Semantic enrichment is a separate *on-touch* operation: the host observes source material actually supplied for work, and the application captures useful, evidence-backed knowledge from that already-read material.

The default enrichment ceiling is **three useful contextual levels**, not three automatic reprocessing passes. Stop earlier when the task has enough evidence; don't expand unrelated neighbors or enrich on repository open. Additional levels happen only as future work needs them. This limit governs LLM interpretation, whereas the library's three-hop conversational retrieval ceiling governs the context returned; independent structural parsing, full graph algorithms and dependency invalidation remain unrestricted.

```python
# Architecture sketch: adapters below are application responsibilities,
# not methods already installed in Knowledge Positions.
def ingest_structure(source):
    # Deterministic parser/AST, IDs and source hashes; NO LLM call.
    return parse_and_index_changed_structure(source)

def on_model_source_used(observed_event):
    # Invoked by the host when source contents enter real model work,
    # not because a prompt suggested optional capture.
    if not observed_event.content_was_supplied:
        return
    item = resolve_verified_source(observed_event)
    relevant = retrieve_bounded_existing_knowledge(item, hops=3)
    delta = qualify_useful_meaning_from_current_work(
        observed_event, relevant, enrichment_levels_at_most=3
    )
    if delta:
        verify_and_commit_changed_records_only(delta)  # JSON or Ladybug adapter
```

A host must establish which file/span the model actually received; a repository listing, filename or search hit does not establish a read. Hash-gate the source and machine annotations separately. Reuse unchanged knowledge rather than making the LLM re-explain it, and keep proposed inferences distinct from observed evidence. A deliberate offline *bulk-enrichment* batch is an opt-in, different workload—never the default for a large repository.

## Optional graph persistence

```text
Original source -> authorized Python parser / AST + OKF
                -> Knowledge Positions: source/hash/graph/vector
                -> [optional LadybugDB changed-record transaction]
                -> bounded graph query -> NetworkX
                -> authorized original-source resolution
```

- **One operation, not a two-stage copy:** a Python backend can write directly to embedded [LadybugDB](https://docs.ladybugdb.com/). The general Knowledge Positions → Ladybug adapter is **not implemented** in the library. A separate prior experiment demonstrated actual AST/OKF storage and query in Ladybug; it is outside this repository.
- **Incremental:** compare source/annotation hashes per stable knowledge item, change only affected records and qualified edges, preserve unchanged vectors and provenance. Document-wide version changes or shifted offsets must not rotate every unchanged knowledge ID.
- **Safe writes:** Ladybug's on-disk store uses a WAL and checkpoints. Coordinate writers; checkpoint/close before external snapshots. A binary `.lbdb` does not produce meaningful Git text diffs—inspect logical record deltas.
- **Enforcement remains separate:** database persistence does not make a model volunteer to save. Reliable capture requires an actual host hook or application-controlled invocation. A connector may only resolve authorized source locations.

**Implemented today:** Knowledge Positions uses Python, NetworkX, JSON persistence and versioned source positions. The [two-section AST/OKF alpha](research/alpha/README.md) has section-scoped hash/update tests. The richer access checks and generic LadybugDB adapter above remain proposed.
