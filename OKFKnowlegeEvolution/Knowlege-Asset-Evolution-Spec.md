# Knowledge Asset Evolution: An OKF-Compatible Extension Profile
## Markdown knowledge assets that remain portable, enrich themselves safely, and propose schema changes under human control

**Version:** 1.5
**Date:** June 17, 2026
**Status:** Proposal
**Audience:** Developers, knowledge engineers, tool builders

> **This is not a competing format to OKF.** It is an OKF-compatible lifecycle
> profile. OKF defines the portable document shape. This specification defines
> *optional* governance, enrichment, and schema-evolution behavior for teams that
> want knowledge assets to remain current, auditable, and human-controlled over
> time. OKF explicitly allows producer-defined extra frontmatter keys and tells
> consumers not to reject unknown fields, so everything here is additive and
> non-breaking.

---
**TL;DR**
An Extenstion of Google's Open Knowledge Format (OKF for LLM knowledge graphs) with a two-hash ownership mechanism that solves two problems: enriching notes without self-triggering, and letting schemas learn their own structure—all while keeping humans in control.
Tool-independent, OKF-compatible. (see bottom for sources)

---


# Part I — The Gap

*Why a format and governance standard still leave two problems open.*


## The Problem

Four concerns exist for a living knowledge system. OKF answers one. wanderloots answers a second. Two were left open.

**1. Format** ✅ Solved — Google OKF v0.1: markdown + YAML frontmatter. Portable, minimal, intentionally incomplete.

**2. Governance** ✅ Solved — wanderloots: Raw/Wiki/Schema, deterministic gates (lint, doctor, build), derived catalog. Standards enforced through tooling.

**3. Enrichment** ❌ Open — How do you let a machine *add* knowledge to a note without (a) corrupting the human's content, or (b) the enricher waking itself up in a loop?

**4. Evolution** ❌ Open — How does the schema itself learn what structure actually works?

This profile defines 3 and 4. They share one idea applied twice.

---

## The Core Idea: Ownership Through Independent Hash Gates

> **Separate ownership with a boundary, and gate each side with its own hash.**

- A **boundary** divides a region the human owns from a region the machine owns.
- **Independent hash gates** each ask one question about one region.
- Because each gate hashes only its own region, the machine editing its side never changes the gate that governs the human's side — so the machine can never trigger *itself*.

The system uses several independent hash gates. The note-level enrichment case uses exactly two of them and is the pattern we call the **two-hash mechanism**.

---

---

# Part II — How It Works

*The mechanism: independent hash gates, the four layers, and a worked example.*


## The Independent Hash Gates (named, timed, sourced)

| Gate | Hashes | Fires / controls | When it runs | Status |
|------|--------|------------------|--------------|--------|
| **`author_hash`** | content **above** the sentinel only | the enricher runs when the current `author_hash` differs from the **last-enriched baseline** stored for that note | on refresh-on-read, per note | **existing** (proven) |
| **`file_hash`** | the **whole file** | whether the **catalog/index** should re-index this note | on refresh-on-read, per note | **existing** (proven) |
| **`machine_hash`** *(optional)* | the `## AI Enrichment` section only | audit / diff / debug of machine output | on demand | **adding** (optional, audit aid) |
| **`schema_hash`** | approved `schema.yaml` | whether schema state changed (governs the evolution loop) | on observer run | **adding** (evolution layer) |
| **`suggestion_fingerprint`** | `schema_version` + `note_type` + `observed_field_or_type` + `suggestion_kind` | suppresses **duplicate** suggestions (don't re-file a suggestion already pending/approved/rejected) | before appending to `schema_suggestions/` | **adding** (evolution layer) |

Two append-only logs sit alongside the gates (they are not hashes, they are ledgers):

| Ledger | Holds | Owner | Status |
|--------|-------|-------|--------|
| `schema_suggestions/` | observer findings | machine | **adding** |
| `schema_reviews/` | human approve/reject decisions | human | **adding** |

**What's already built:** `author_hash` and `file_hash` (the two-hash enrichment mechanism) — reference implementation, 153 lines, 9 passing tests including adversarial no-self-retrigger cases.¹

> ¹ The line and test counts describe the reference enricher as recorded in working notes; verify them against the implementation repository before publishing externally.

**What this profile adds:** the optional `machine_hash` for audit, plus the whole evolution layer (`schema_hash` + the two ledgers).

---

## Layer 1: OKF Format Compatibility

Every profile-governed concept note is a valid OKF document.

```yaml
---
type: decision_record          # OKF: the ONLY required field
title: "Refactor the API?"     # OKF: SHOULD when known
description: "Whether to refactor the public API before v2"   # SHOULD
tags: [architecture, decision] # SHOULD
timestamp: 2026-06-17T14:30:00Z # SHOULD
---
```

OKF requires only a non-empty `type`. `title`, `description`, `resource`, `tags`, and `timestamp` are recommended/optional. Everything this profile adds lives in *additional* frontmatter keys and in the note body — both of which OKF consumers safely ignore.

---

## Layer 2: wanderloots Governance (Operational Constraints)

Requirements, not suggestions:

- **Markdown is truth; JSON is a derived cache** (rebuildable anytime, never authoritative).
- **Refresh-on-read currency:** before answering, re-hash the vault, re-index *only* the files whose `file_hash` changed, then answer. No stale results; cost stays near zero because unchanged files are skipped.
- **Deterministic gates:** `build`, `lint`, `doctor` run before commits.
- **Catalog contract:** one derived JSON record per note.

---

## Layer 3: Enrichment — The Proven Foundation (the two-hash mechanism)

Already built and tested. The evolution layer (Layer 4) rides on this one.

### The Sentinel: an ownership boundary inside every note

```markdown
# Refactor the API?

[Human-authored content. The TRUTH. Humans own everything above the sentinel.]

## End Index Hash

## AI Enrichment

[Machine-written: cross-links, contradictions found, "worth investigating"
notes. The machine owns everything below the sentinel.]
```

- **Above `## End Index Hash`** = human territory (authoritative).
- **Below the sentinel** = machine territory (the enricher writes here and *only* here).

This is closer to wanderloots than to OKF: OKF separates *human-readable* from *agent-readable* (readability). The sentinel separates *human-maintained* from *machine-maintained* (**ownership**). That difference is the point.

### The two-hash mechanism (why the enricher never loops)

```text
author_hash = hash(text ABOVE the sentinel)   # "did the author change anything?"
file_hash   = hash(WHOLE file)                # "did anything at all change?"
```

```python
def maybe_enrich(note):
    if note.author_hash == stored_author_hash(note):
        return            # author content unchanged -> do NOT enrich (no loop)
    enrichment = generate_enrichment(note.human_content)
    write_below_sentinel(note, enrichment)     # touches machine territory only
    store_author_hash(note, note.author_hash)  # remember what we enriched against
```

**The precise proof (three cases):**

1. **Enricher writes below the sentinel** → `author_hash` is unchanged (it only covers *above*) → the enricher does **not** run again. *No loop.* Note: this write **does** change `file_hash`, so it MAY trigger catalog re-indexing — which is correct and desired. The guarantee is narrow and exact: **machine edits below the sentinel may trigger re-indexing, but never trigger another enrichment run.**
2. **Human edits content above the sentinel** → `author_hash` changes → enricher re-runs exactly once.
3. **No edits** → both hashes stable → everything skipped.

These three are the adversarial tests in the reference implementation, and they pass.

### Backoff

After N clean runs with no changes, the enricher backs off so a stable vault stops waking it. Currency is preserved by refresh-on-read; backoff just stops needless polling.

---

## Layer 4: Schema Evolution — the same idea, applied to structure

Layer 3 lets a note learn *facts* without self-triggering. Layer 4 lets the *schema* learn *structure* without self-triggering, using the **same ownership-boundary idea** with a different boundary and its own gate (`schema_hash`).

### The loop

```
Observe → what fields/types recur across notes?
   ↓
Score   → confidence = frequency × approval_rate × downstream_effect × decay(time)
   ↓
Suggest → append to schema_suggestions/ (machine territory)
   ↓
Review  → human writes to schema_reviews/ (human territory)
   ↓
Approve → only a human edit promotes a change into schema.yaml
   ↓
Evolve  → schema_version increments; old notes stay valid
```

### Storage — boundary between machine and human territory

```
schema/
  schema.yaml            ← current APPROVED state (changes ONLY via human review)
schema_suggestions/      ← OBSERVER territory (append-only, machine-written)
schema_reviews/          ← HUMAN territory (append-only, immutable audit trail)
```

### The same anti-self-trigger guarantee, via schema_hash

```text
schema_hash = hash(schema.yaml)

# Observer may append NEW suggestions while schema_hash is unchanged.
# Appending to schema_suggestions/ NEVER mutates schema.yaml,
# so it NEVER changes schema_hash -> the observer cannot trigger itself.

# schema.yaml changes ONLY when a human review in schema_reviews/
# promotes a suggestion. Only that promotion changes schema_hash.
```

The observer writing suggestions is exactly like the enricher writing below the sentinel: it touches **machine territory only**, so it can't trigger the loop that governs **human territory** (`schema.yaml`).

### Observer algorithm

```python
def observe(catalog, current_schema):
    patterns = detect_recurring_structure(catalog)   # frontmatter + enriched headers
    for p in patterns:
        p.confidence = (
            (p.field_frequency / p.total_notes_of_type)
            * p.user_approval_rate
            * p.downstream_effect       # e.g. wikilinks created into these notes
            * decay(p.days_since_first_seen)
        )
    for p in patterns:
        if p.confidence > THRESHOLD:
            fp = suggestion_fingerprint(            # dedupe gate
                schema_version=current_schema.version,
                note_type=p.note_type,
                target=p.observed_field_or_type,
                kind=p.suggestion_kind,
            )
            if fp in seen_fingerprints():           # pending OR approved OR rejected
                continue                            # already filed once — skip
            append_to_suggestions(p, fingerprint=fp)  # MACHINE territory only
    # schema.yaml is updated elsewhere, ONLY after a human writes an approval
    # into schema_reviews/. The observer has no write access to schema.yaml.
```

> **Why the dedupe gate matters.** The observer *cannot* trigger schema
> evolution (only a human promotion changes `schema.yaml`). But without a
> fingerprint it would re-file the *same* suggestion every run — a
> suggestion-spam loop, not a schema loop. `suggestion_fingerprint` checks
> pending, approved, *and* rejected suggestions, so a rejected idea is not
> re-proposed on the next pass. This makes Layer 4 as quiet as Layer 3.

> **Note on `decay(time)`:** the direction is intentionally left unspecified in
> this profile — it is part of Open Question 1 (confidence weighting). A pattern that has
> been *stable and repeatedly approved* over time should plausibly score *higher*,
> not lower, so `decay` here may reward longevity rather than penalize age.
> Implementations should make their choice explicit.

---

## Worked Example: Decision Record Evolution

**Initial schema (human-authored):**
```yaml
type: decision_record
schema_version: 1
fields: [title, context, decision]
```

**Observation (machine territory: schema_suggestions/):**
```json
{
  "observation_date": "2026-07-17",
  "pattern": "decision_record",
  "observed_field": "rationale",
  "frequency": 18, "total_notes": 20, "frequency_ratio": 0.90,
  "user_approval_rate": 0.95, "downstream_effect": 0.80,
  "days_stable": 30, "confidence": 0.84,
  "suggestion": "Add 'rationale' as a standard field",
  "status": "pending_review"
}
```

**Review (human territory: schema_reviews/ — immutable):**
```json
{
  "suggestion_id": "2026-07-17__decision_record_rationale",
  "reviewer": "alice", "reviewed_at": "2026-07-17T14:22:00Z",
  "decision": "approve",
  "comment": "Every decision already has a rationale; formalize it.",
  "schema_version_change": "1 -> 2"
}
```

**Resulting schema (only now does schema.yaml change → schema_hash changes):**
```yaml
type: decision_record
schema_version: 2
fields: [title, context, decision, rationale]
schema_origin:
  title:    { origin: human_authored }
  context:  { origin: human_authored }
  decision: { origin: human_authored }
  rationale:
    origin: auto_suggested
    suggested_at: 2026-07-17
    confidence: 0.84
    approved_by: alice
    approved_at: 2026-07-17T14:22:00Z
```

Old `schema_version: 1` notes remain valid and queryable. New notes use v2.

---

---

# Part III — Extending Your Own KG

*A path you can walk: pick how far to go, build it, keep it safe, and see what a finished note looks like.*


## Adoption Path: Extending Your Own KG

Adopt incrementally. You do not need schema evolution to benefit.

```text
Level 0 — OKF Bundle
  Valid OKF (non-empty `type` on every concept document).

Level 1 — Governed Knowledge Asset
  Level 0 + markdown-as-truth + derived catalog + lint/build/doctor gates
  + refresh-on-read.

Level 2 — Enriched Knowledge Asset
  Level 1 + sentinel boundary + author_hash + file_hash
  + the no-self-retrigger proof (the two-hash mechanism).

Level 3 — Evolving Knowledge Asset
  Level 2 + schema observer + schema_suggestions/ + schema_reviews/
  + schema_hash + human approval gate.
```

---

## Recommendations for Implementation

Requirements are scoped by conformance level, so an OKF-only adopter is not accused of failing the profile.

**A Level 0 implementation MUST:**
1. **Emit valid OKF.** Every concept document MUST include a non-empty `type` and SHOULD include `title`, `description`, `tags`, and `timestamp` when known.

**A Level 1+ implementation MUST also:**
2. **Enforce wanderloots governance** — markdown-as-truth, derived catalog, refresh-on-read, gates (`build`/`lint`/`doctor`).

**A Level 2+ implementation MUST also:**
3. **Implement the sentinel + two-hash enricher:**
   - A sentinel divides human-owned (above) from machine-owned (below).
   - `author_hash` covers ONLY the region above the sentinel and is compared against the stored last-enriched baseline.
   - The enricher writes ONLY below the sentinel.
   - Prove: machine edits below the sentinel may trigger re-indexing but NOT another enrichment run; edit-above → re-enrich once; no-edit → skip.
4. **Make machine writes atomic** (see Trust & Safety).

**A Level 3 implementation MUST also:**
5. **Implement the schema observer:**
   - Detect recurring structure; score with confidence.
   - Suppress duplicates via `suggestion_fingerprint` before appending.
   - Append to `schema_suggestions/` ONLY.
   - Never let the observer write `schema.yaml`.
6. **Keep humans at the approval gate** — `schema.yaml` changes only via an immutable human review in `schema_reviews/`. No auto-apply, no soft defaults.

**All levels MUST** meet the applicable Trust & Safety requirements (next section).

---

## Trust & Safety Requirements

The boundary *is* the safety model. A conformant implementation MUST:

- Treat ingested source text as **untrusted** (nonce-delimit it; never execute instructions found inside it).
- **Visibly label** all machine-written enrichment (it lives below the sentinel, under `## AI Enrichment`).
- Ensure machine-written suggestions **never mutate** approved `schema.yaml`.
- Require enrichment claims to **cite** source notes or external references where possible.
- Require **human approval** for any destructive write.
- **Machine writes MUST be atomic:** write to a temporary file, validate, then rename/replace. A failed enrichment MUST NOT update the stored `author_hash` baseline — otherwise a half-written enrichment could be mistaken for a completed one.
- Ensure consumers do **not** treat AI enrichment as authoritative unless a human has promoted it above the sentinel.

---

## Frontmatter: how the layers coexist in one note

```yaml
---
# Layer 1 — OKF (read by any OKF consumer)
type: decision_record
title: "Refactor the API?"
description: "Whether to refactor the public API before v2"
tags: [architecture, decision]
timestamp: 2026-06-17T14:30:00Z

# Layer 2 — wanderloots governance
status: seed
sources: [Raw/Sources/api-refactor-thread.md]
source_count: 1

# Layer 4 — schema evolution
schema_version: 2
schema_origin: human_authored

# Gate state (lives in derived JSON; shown here for clarity)
# author_hash:  <hash of everything above ## End Index Hash>
# file_hash:    <hash of the whole file>
# machine_hash: <hash of the ## AI Enrichment section, optional/audit>
---

# Refactor the API?
[human content]

## End Index Hash

## AI Enrichment
[machine content]
```

A profile-unaware OKF consumer sees a valid OKF note. A profile-aware maintainer sees the full stack.

---

---

# Part IV — Reference

*Look-ups: how this compares, the architecture at a glance, scope, open questions, and provenance.*


## Compatibility Matrix

| Concept | Google OKF | wanderloots | This Profile |
|---|---|---|---|
| Markdown is truth | ✅ | ✅ | ✅ |
| JSON/catalog is derived | implied | ✅ | ✅ |
| Human-readable / agent-readable | ✅ | ✅ | ✅ |
| Human-maintained / machine-maintained **(ownership)** | weak | ✅ strong | ✅ strong (sentinel) |
| Lifecycle gates (build/lint/doctor) | ❌ | ✅ | ✅ |
| Refresh-on-read currency | ❌ | no explicit opinion | ✅ |
| **Enrichment with no self-retrigger (two-hash)** | ❌ | ❌ | ✅ **proven** |
| Schema evolution (observe→approve) | ❌ | not central | ✅ |
| Vendor-neutral exchange | ✅ primary | not primary | ✅ via OKF export |

---

## Architecture

```
Knowledge Asset  (the center — independent of any tool)
├── Format       — OKF: markdown + YAML frontmatter
├── Governance   — markdown truth, derived catalog, build/lint/doctor gates, refresh-on-read
├── Enrichment   — sentinel boundary + author_hash (two-hash) → no self-retrigger  [PROVEN]
├── Evolution    — schema observer proposes; humans approve (schema_hash + ledgers)
└── Consumers    — any agent, search index, editor, graph viewer, or runtime
```

The asset is the unit of portability. Tools are replaceable. The asset is not.

---

## Out of Scope (future extensions)

- **Relationship typing.** OKF links are intentionally untyped; relationship meaning is conveyed by surrounding prose, and graph consumers treat links as directed untyped edges. This profile keeps links as OKF-compatible markdown links in v1.5. Future versions may propose *optional* relationship metadata (`depends_on`, `contradicts`, `supports`, `refines`, `duplicates`, `derived_from`, `cites`) **without changing the underlying link format**.

---

## Open Questions

1. **Confidence weighting** — equal weights on frequency / approval / downstream / decay? Better formulas?
2. **Schema versioning** — auto-migrate old notes, keep them at their version, or make the new schema optional?
3. **Multi-team governance** — whose approval gate wins when several teams co-own one asset?
4. **Evolution scope** — may the observer propose new *types*, or only new *fields* (and deprecations) within existing types?
5. **Structural vs. semantic observation** — keep the observer purely structural, or allow an LLM pass to read field *meaning*?

---

## Sources & Lineage

- **Google OKF v0.1** — the portable format.
  https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
  Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

- **wanderloots LLM-Wiki** — the governance philosophy (standards enforced through tooling). Build on Obsidian
  - git- https://github.com/wanderloots-tutorials/vibe-coding/blob/main/wanderloots-llm-wiki-core-setup-v1.0.0.md
  - youtube explainer - https://www.youtube.com/watch?v=QbjAQFJJyt0&t=737s

- **Karpathy's LLM Wiki** — maintain a compiled wiki instead of re-retrieving; treat ingested sources as untrusted.
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

This profile fills the two gaps those sources intentionally left open: **enrichment without self-triggering**, and **schema that learns its own structure** — both under permanent human authority.

---

## License & Attribution

**License: MIT.** The MIT copyright/permission notice must be preserved in copies or substantial portions. The spec is intentionally permissive — use, implement, extend, adapt.

Credit for the ideas and sources this profile builds on is kept in `ATTRIBUTION.md` and summarized in the README's Lineage section. This profile is not affiliated with or endorsed by Google, wanderloots, Andrej Karpathy, or any other cited source.
