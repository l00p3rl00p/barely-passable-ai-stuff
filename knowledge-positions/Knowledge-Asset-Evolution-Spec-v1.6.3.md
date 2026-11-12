# Knowledge Asset Evolution: An OKF-Compatible Extension Profile
## Markdown knowledge assets that remain portable, enrich themselves safely, and propose schema changes under human control

**Version:** 1.6.3
**Date:** July 7, 2026 (1.6-draft) — revised July 9, 2026 (1.6.2) — revised July 9, 2026 (1.6.3)
**Status:** Proposal
**Audience:** Developers, knowledge engineers, tool builders

> **1.6.2 changelog (2026-07-09, code-reconciliation revision).** Verified against
> loomyn v3.20.3 and the V12.3 roadmap. Four changes, all in Part IV:
> (1) the packet `governance` block is now explicitly **advisory** — admission
> means independent re-verification by the ingest gate, never trust in
> producer-signed booleans; (2) a **tiered durability policy** replaces the
> single fsync-and-rename recipe (the old pseudocode lacked directory fsync and
> ignored macOS `F_FULLFSYNC`); (3) a **tamper rule** for depth/budget counters:
> the spawner stamps them into the child's frozen frame, and child self-reported
> values are ignored at admission — with matching `ledger` fields added to the
> packet schema; (4) an explicit **cross-reference lock** to the Loomyn V12.3
> roadmap §21.2.2: the roadmap's `EvidencePacket` entries are references to
> packets admitted under this profile — one evidence physics, two documents.
> Version stamp fixed (the file circulated as "v1.6.1" while its header still
> said 1.6-draft).

> **1.6.3 changelog (2026-07-09, truth-layer revision).** Three changes, all in
> Part IV: (1) a new "Truth, Meaning, and Learning layers" section states Part
> IV is the Truth layer only — it must stay boring and notary-like, and is
> never the Meaning layer (KG/index projection) or Learning layer (weights,
> priors, model/tool performance, out of scope here); (2) a clarifying
> paragraph in "Tiered durability policy" states SQLite/WAL is one
> interchangeable Truth-layer storage choice, not an elevation to Meaning or
> Learning status — the direct fix for an ambiguity in the prior round where
> SQLite was floated without this framing; (3) a cross-reference sentence
> after the runtime packet example points to Loomyn roadmap V12.4 §21.2.4,
> which states the same minting-rule principle as a standalone rule with
> `admitted_read_file` as its first concrete instance.

> **This is not a competing format to OKF.** It is an OKF-compatible lifecycle
> profile. OKF defines the portable document shape. This specification defines
> *optional* governance, enrichment, and schema-evolution behavior for teams that
> want knowledge assets to remain current, auditable, and human-controlled over
> time. OKF explicitly allows producer-defined extra frontmatter keys and tells
> consumers not to reject unknown fields, so everything here is additive and
> non-breaking.

---
**TL;DR**
An Extension of Google's Open Knowledge Format (OKF for LLM knowledge graphs) with a two-hash ownership mechanism that solves two problems: enriching notes without self-triggering, and letting schemas learn their own structure—all while keeping humans in control.
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

*The mechanism: independent hash gates, the four knowledge layers, the optional runtime profile, and a worked example.*


## The Independent Hash Gates (named, timed, sourced)

| Gate | Hashes | Fires / controls | When it runs | Status |
|------|--------|------------------|--------------|--------|
| **`author_hash[]`** | independently addressable author-owned sections above the sentinel | compare each section against its last successfully evaluated baseline; evaluate materiality before changing enrichment | after a changed `file_hash` | **section-scoped refinement; original proof was whole-author-region** |
| **`file_hash`** | the **whole file** | cheap watchdog: if unchanged, stop; if changed, inspect section hashes without automatically regenerating knowledge | on refresh-on-read, per note | **existing watchdog; unchanged purpose** |
| **`machine_hash[]`** | each independently addressable AI enrichment section below the sentinel | detect actual machine changes, retain unaffected tags, relationships, and conclusions | after changed `file_hash` and successful machine writes | **required in section-scoped refinement; not part of original two-hash tests** |
| **`schema_hash`** | approved `schema.yaml` | whether schema state changed (governs the evolution loop) | on observer run | **adding** (evolution layer) |
| **`suggestion_fingerprint`** | `schema_version` + `note_type` + `observed_field_or_type` + `suggestion_kind` | suppresses **duplicate** suggestions (don't re-file a suggestion already pending/approved/rejected) | before appending to `schema_suggestions/` | **adding** (evolution layer) |
| **`event_hash`** | one immutable runtime event packet | idempotency and replay safety for high-volume blossom outputs | on event ingestion | **adding** (runtime layer) |
| **`artifact_hash`** | emitted artifact payload | dedupe, provenance, and corruption detection for generated artifacts | on event ingestion and compaction | **adding** (runtime layer) |
| **`projection_hash`** | the KG/index mutation derived from an accepted event | whether the semantic projection changed and can be replayed or rebuilt | on projection into the KG/index | **adding** (runtime layer) |

Two append-only logs sit alongside the gates (they are not hashes, they are ledgers):

| Ledger | Holds | Owner | Status |
|--------|-------|-------|--------|
| `schema_suggestions/` | observer findings | machine | **adding** |
| `schema_reviews/` | human approve/reject decisions | human | **adding** |
| `Events/` | runtime event packets emitted by blossoms/workers | machine | **adding** |
| `Evidence/` | human-readable audit projection of accepted events | substrate / human-reviewed as needed | **adding** |

**What's already built:** `author_hash` and `file_hash` (the two-hash enrichment mechanism) — reference implementation, 153 lines, 9 passing tests including adversarial no-self-retrigger cases.¹

> ¹ The line and test counts describe the reference enricher as recorded in working notes; verify them against the implementation repository before publishing externally.

**Section-scoped refinement:** `machine_hash[]` is required for independently tracked enrichment regions, alongside `author_hash[]`. The original reference proof covered only the two-hash ownership boundary; section-level and materiality behavior require their own tests. The evolution layer retains its separate schema gate and ledgers.

**What v1.6 adds:** an optional runtime event substrate profile. Runtime event packets preserve execution truth before that truth is projected into a KG/index, compiled Wiki, or human-readable audit trail.

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
- **Refresh-on-read currency:** check each file's `file_hash` as a watchdog. Unchanged files stop there; changed files are section-compared. Reindex only changed sections and affected dependencies, preserving unchanged identities, vectors, and enrichment. A changed file does not imply all its knowledge changed.
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
file_hash        = hash(WHOLE file)             # watchdog: was the file touched?
author_hash[id]  = hash(author_section[id])    # independent author sections above sentinel
machine_hash[id] = hash(enrichment_section[id]) # independent machine sections below sentinel
```

```python
def maybe_enrich(note, state):
    if hash_file(note) == state.file_hash:
        return 'unchanged file'
    author_delta = compare_stable_sections(note.author_sections, state.author_hashes)
    machine_delta = compare_stable_sections(note.machine_sections, state.machine_hashes)
    for section in author_delta:
        impact = assess_materiality(section, related_enrichment(note, section))
        if impact == 'material':
            revise_only_affected_enrichment(section, impact)
        elif impact == 'uncertain':
            flag_for_review(section)  # do not silently affirm unsupported claims
        else:
            preserve_existing_enrichment(section)
        # Advance the evaluated author baseline only after successful assessment.
        record_evaluated_baseline(section)
    persist_changed_machine_hashes(machine_delta)
    commit_watchdog_after_success(note)  # persist atomically; never cross ownership boundary
```

**The precise proof (three cases):**

1. **Enricher writes below the sentinel** → `author_hash` is unchanged (it only covers *above*) → the enricher does **not** run again. *No loop.* Note: this write **does** change `file_hash`, so it MAY trigger catalog re-indexing — which is correct and desired. The guarantee is narrow and exact: **machine edits below the sentinel may trigger re-indexing, but never trigger another enrichment run.**
2. **Human edits content above the sentinel** → only affected `author_hash[]` entries change. Each changed section is assessed once; an immaterial formatting or presentation edit leaves the enrichment text and `machine_hash[]` untouched. Material evidence changes revise only the affected enrichment; unresolved validity is flagged for review.
3. **No edits** → `file_hash` remains stable and the watchdog skips section inspection.

The original three no-self-retrigger cases passed in the historical whole-author-region reference implementation. The section-scoped refinement extends the mechanism and requires distinct acceptance tests for stable section identities, insertions/reordering, formatting-only edits, meaningful changes, multi-section enrichment, dependency invalidation, and failed/uncertain evaluations. A file-level hash remains a watchdog, never a signal to regenerate the entire file's knowledge.


**Repository-wide JIT positions:** Each source file has its own stable section identities and section hashes. A single derived repository JSON index can collect those file-local positions and qualified cross-file edges for NetworkX traversal and compatible vector search. Section identities do not rotate when unrelated file content moves. Explicit citations and observed dependencies remain distinct from lexical suggestions; only verified affected dependencies are invalidated. This shared index is a derived navigation artifact, never a replacement for source files or the existing paper-specific JIT index.

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

Level 4 — Runtime-Projected Knowledge Asset
  Level 3 + immutable runtime event packets + event_hash + artifact_hash
  + projection_hash + asynchronous KG/index projection + compaction.
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
   - `file_hash` remains the whole-file watchdog; it does not by itself force re-enrichment.
   - `author_hash[]` independently covers stable author sections above the sentinel, each compared with its last successfully evaluated baseline.
   - `machine_hash[]` independently covers machine enrichment sections below the sentinel and is required for section-scoped enrichment.
   - The enricher writes ONLY below the sentinel and only for materially affected knowledge; mere formatting may require no enrichment change.
   - Prove: machine edits do not self-trigger; changed author sections are assessed once; unaffected enrichments retain identity/hash; uncertain validity is flagged; no edit skips; unsuccessful assessment does not advance the baseline.
4. **Make machine writes atomic** (see Trust & Safety).

**A Level 3 implementation MUST also:**
5. **Implement the schema observer:**
   - Detect recurring structure; score with confidence.
   - Suppress duplicates via `suggestion_fingerprint` before appending.
   - Append to `schema_suggestions/` ONLY.
   - Never let the observer write `schema.yaml`.
6. **Keep humans at the approval gate** — `schema.yaml` changes only via an immutable human review in `schema_reviews/`. No auto-apply, no soft defaults.

**A Level 4 implementation MUST also:**
7. **Capture runtime outputs as immutable event packets:**
   - A blossom/worker writes a complete packet to `Events/tmp/`.
   - The packet is validated against the event packet schema before admission.
   - The packet is atomically renamed into `Events/inbox/` when complete.
   - The packet is never edited in place after admission.
8. **Project accepted packets into a KG/index:**
   - The KG/index is a derived semantic projection, rebuildable from accepted packets.
   - Runtime packets carry causal fields (`event_id`, `parent_event_ids`, `depends_on`, `produces`) so projection is causal, not merely chronological.
   - Duplicate packets are suppressed by `event_hash`, `artifact_hash`, or an implementation-defined idempotency key.
9. **Separate capture from compaction:**
   - Workers emit packets only. They do not directly mutate approved schema, human-owned note regions, or durable Wiki claims.
   - A substrate ingestor validates and projects packets.
   - A compactor may later merge duplicates, mark superseded claims, archive hot packets, and prepare human-readable projections.

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
- For runtime packets, treat every packet as a **proposed state transition** until schema validation, idempotency checks, and required canaries pass.
- Runtime capture SHOULD use a staging directory pattern: write to `Events/tmp/`, validate, then rename into `Events/inbox/`. Failed or partial writes MUST NOT be admitted into the KG/index projection.
- The KG/index MUST remain rebuildable from accepted runtime packets and approved Markdown assets. A KG/index corruption MUST NOT destroy the underlying execution or knowledge history.

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
# author_hashes:  <per-stable-section hashes above ## End Index Hash>
# file_hash:      <whole-file watchdog hash>
# machine_hashes: <per-enrichment-section hashes below sentinel; required>
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


# Part IV — Runtime Event Substrate Profile

*An optional execution layer for high-volume, parallel machine outputs before they become durable knowledge assets.*

This part is additive. It does not replace OKF, wanderloots governance, the two-hash enrichment mechanism, or schema evolution.

The distinction is:

```text
Runtime event packets preserve execution truth.
Markdown knowledge assets preserve durable human-readable knowledge.
The KG/index is a semantic projection that links them.
```

A runtime event packet is not a Wiki note. It is not a Raw source. It is a proposed state transition emitted by a worker/blossom and later admitted, rejected, projected, compacted, or promoted.

## Truth, Meaning, and Learning layers (1.6.3)

Part IV of this profile defines the **Truth layer only**. It must stay boring and notary-like: admitted events, hashes, refs, canaries.

```text
Truth layer (this Part):
  Admitted events, hashes, refs, canaries. The admission journal and
  the Events/ lifecycle below. Nothing here reasons about meaning.

Meaning layer (out of scope for this Part):
  KG/index projection — described below in "Ingest, projection, and
  compaction." Accepted packets become semantic structure there, not
  in the Truth layer itself.

Learning layer (out of scope for this profile):
  Weights, priors, skill/model performance. Owned by the consuming
  system — e.g. Loomyn's core/model_profiler.py and roadmap §14 —
  never by this profile.
```

A runtime event packet's admission is a Truth-layer fact. What that fact means, and what should be learned from it, are separate layers with separate consumers.

## Runtime terminology contract

This section makes the project-native terms operational. These terms are allowed only when they map to the required behavior below.

| Term | Operational meaning in this profile | What it is not |
|---|---|---|
| **Runtime event packet** | An immutable JSON file emitted by a worker into `Events/tmp/` and atomically admitted to `Events/inbox/`. It is the ground-truth record of one proposed execution state transition. | A Wiki note, Raw source, chat message, or direct KG write. |
| **Blossom** | A short-lived worker that receives one prepared register frame, runs one selected skill/lap, emits one runtime event packet, and terminates. | A long-lived agent that carries memory, owns the KG, or chats with other workers. |
| **Bloom** | Earlier conversational shorthand for the same idea as **blossom**. This profile uses **blossom** consistently. | A separate runtime primitive. |
| **RAM-based Nucleus** | A hot, rebuildable working state derived from accepted packets and KG/index projection. It exists to keep the whole knowledgebase out of the LLM context window while still letting the system decide what can run next. | Permanent truth, a giant prompt, or a requirement to use Python `shared_memory`. |
| **Dynamic linker** | The resolver that reads the KG/index projection and RAM-based Nucleus, then builds the next small register frame. | A model prompt asking the blossom to search the whole repo or decide its own mission. |
| **Register frame** | The tiny execution context handed to one blossom. It contains only the current node, local neighbors/input, selected skill/opcode, constraints, commit target, canary contract, and exit policy. | The whole KG, full chat history, or broad Raw context. |
| **Skill opcode** | The selected capability the blossom is allowed to run for this lap. | An entire prompt library or all possible skills. |
| **Pick-and-Purge** | The runtime rule that only the selected skill/context enters the register frame; unneeded capabilities and history stay out. | Deleting durable knowledge or removing evidence from the repository. |
| **Logic-Bearing Canary** | Deterministic proof attached to a packet before admission when available: parse result, test log, hash, diff, file existence check, schema validation, or similar evidence. | A conversational claim that the work is done. |
| **Salmon Return** | The blossom's final write-back: emit the useful result as an immutable runtime event packet, then terminate. | Direct mutation of the KG, Wiki, approved schema, or human-owned note content. |
| **Wheat** | The useful technical payload inside the packet: artifact, claim, proof, dependency, contradiction, or next-state hint. | The full reasoning trace or conversational explanation. |
| **Dependency-Driven Suicide** | The blossom exits without producing an accepted state change when its prerequisites are unmet, its skill is not applicable, or its canary fails. It may emit a failure packet if the implementation wants diagnostic evidence. | A crash, data loss, or unhandled exception. |
| **Pressure Front** | Many blossoms running in parallel and dropping independent packets into the event substrate. | Many workers writing the same KG/table/log through one global lock. |
| **KG/index projection** | A rebuildable semantic view over accepted packets and approved Markdown assets. It supports traversal, dependency checks, linking, and register-frame construction. | The capture layer or permanent truth by itself. |
| **Compaction** | Slower cleanup that merges duplicates, marks superseded claims, flags contradictions, archives hot packets, updates `Evidence/EVIDENCE.md`, and may prepare Wiki/schema proposals. | Immediate capture, direct human approval, or deletion of truth without trace. |

The short version is:

```text
Blossom executes a small register frame.
Blossom emits a packet.
The substrate admits or rejects the packet.
The KG/index projects accepted packets.
The RAM-based Nucleus caches the hot working state.
The dynamic linker builds the next register frame.
```

### Public terminology note

The table above keeps the project-native terms because they name specific runtime behaviors used by this profile. They are explanatory terms for readers, not a requirement that downstream implementations expose internal guardrail class names.

Implementations MAY translate these terms into their own enforcement packs, tests, or guardrails. The public conformance requirement is the behavior: short-lived workers receive small frames, emit immutable packets, avoid direct KG/Wiki/schema mutation, and let the substrate validate, project, compact, and rebuild state.

### Minimal runtime loop

This loop is the concrete implementation meaning of the terms above. The loop is assembly-like in discipline, but it is not assembly language. The point is separation of responsibility: the blossom receives a small frame, not the whole world.

```text
Initial prompt or task
   ↓
root runtime event packet
   ↓
ingest + validate + project into KG/index
   ↓
refresh RAM-based Nucleus from projection
   ↓
dynamic linker selects a runnable node and builds a register frame
   ↓
spawn blossom with that frame
   ↓
blossom executes selected skill/opcode
   ↓
logic-bearing canary attached where possible
   ↓
Salmon Return: emit immutable packet to Events/tmp/ then Events/inbox/
   ↓
blossom terminates
   ↓
repeat from ingestion/projection
```

A blossom does not need to read the KG after every write. That is the substrate's job. The substrate ingests packets, updates the projection, refreshes the hot Nucleus, and links the next frame.

---

## Layer 5: Runtime Events — capture before knowledge

Layer 5 exists for systems that run many short-lived workers in parallel. These workers should not all write the KG, the compiled Wiki, or `EVIDENCE.md` directly. They should emit small, immutable event packets into a known repository location.

The hot path is intentionally simple:

```text
worker/blossom executes
   ↓
writes complete JSON packet to Events/tmp/
   ↓
atomically renames packet into Events/inbox/
   ↓
terminates
```

The substrate then handles the slower work:

```text
Events/inbox/
   ↓
ingest + schema validate + canary validate + idempotency check
   ↓
Events/accepted/ or Events/rejected/
   ↓
KG/index projection
   ↓
compaction + human-readable projection
```

### Repository layout

A private source-controlled `knowledgebase/` may expose the runtime folders as normal folders. They do not need to be hidden.

```text
knowledgebase/
  Events/
    tmp/
    inbox/
    processing/
    accepted/
    rejected/
    archive/

  Raw/
    Sources/
    Files/

  Wiki/
    Topics/
    Concepts/
    Entities/
    Projects/
    Logs/
    catalog.jsonl
    index.md

  Graph/
    world.kuzu              # example projection; implementation MAY use something else
    event-index.jsonl
    projection-offsets.json

  Schema/
    frontmatter-schema.md
    event-packet.schema.json
    projection.schema.json
    source-manifest.jsonl
    schema.yaml
    schema_suggestions/
    schema_reviews/

  Runtime/
    registers/
    task-seeds/
    locks/
    stalled-branches.json

  Evidence/
    EVIDENCE.md

  scripts/
    wiki_tool.py
    audit_public.py
```

The names above are recommended for clarity, not a required storage engine. A conformant implementation may use another graph/index engine as long as the accepted packets and approved Markdown assets remain rebuildable.

---

## Runtime event packet

A runtime event packet carries causal coordinates. Chronological arrival order is not authoritative; causal fields are.

```json
{
  "event_id": "evt_8492",
  "event_type": "blossom.output",
  "run_id": "run_551",
  "parent_event_ids": ["evt_8488"],
  "created_at": "2026-07-07T23:12:44.123456Z",

  "producer": {
    "blossom_id": "blossom_8492",
    "active_pgid": "swarm_run_551",
    "skill_selected": "syntax_validation",
    "skills_purged": 24
  },

  "ledger": {
    "_comment": "1.6.2 tamper rule: stamped by the SPAWNER into the child's frozen frame at spawn time. Depth/budget/repair values self-reported by the producer are IGNORED at admission — the writer does not own the gate (same principle as the sentinel). Precedent: loomyn v3.20.3 already does parent-stamps-child in-process (core/rlm.py:1719).",
    "depth": 1,
    "max_depth": 3,
    "budget_remaining_usd": 0.42,
    "repair_count": 0,
    "stamped_by": "blossom_8488"
  },

  "claims": {
    "depends_on": ["auth_schema_written"],
    "produces": ["auth_schema_validated"],
    "supersedes": [],
    "contradicts": []
  },

  "artifact": {
    "content_type": "application/json",
    "hash": "sha256:bbb451fa...",
    "parts": [
      {
        "content": "Syntax standard for auth_module validated; safe for next runner."
      }
    ]
  },

  "logic_bearing_canary": {
    "proof_of_work": "regex_diff_passed",
    "test_log_output": "0 errors, 4 schemas validated"
  },

  "governance": {
    "_comment": "1.6.2: ADVISORY ONLY. These fields are producer-signed and must never be treated as an acceptance gate. Admission means the ingest gate independently re-derives and validates canaries and hashes (see 'Ingest, projection, and compaction'). A self-attested true is a claim, not a proof.",
    "green_mm_compliance": true,
    "purpose_block_verified": "/** PURPOSE: Validates cryptographic integrity of auth payloads **/"
  }
}
```

The same principle is stated as a standalone rule, with `admitted_read_file` as its first concrete instance, in Loomyn roadmap V12.4 §21.2.4 (evidence_ref minting rule) — one evidence physics, two documents (cross-reference already established by this file's own §0.0-equivalent changelog).

### Runtime hash gates

```text
event_hash      = hash(immutable runtime event packet)
artifact_hash   = hash(emitted artifact payload)
projection_hash = hash(KG/index mutation derived from the accepted event)
```

These gates extend the same boundary idea used by `author_hash`, `file_hash`, and `schema_hash`: each gate controls one boundary and does not wake unrelated loops.

---

## Atomic event capture

Machine writes MUST already be atomic in Level 2+. Runtime packets use the same principle, but optimized for parallel capture: write a complete file in `Events/tmp/`, then rename it into `Events/inbox/`. Each worker owns one unique output path, so workers do not need a global KG write lock.

### Tiered durability policy (1.6.2)

The 1.6-draft recipe (fsync file, then rename) is **atomicity, not durability**: it lacks a directory fsync after the rename, and on macOS a plain `fsync` does not flush to disk at all — that requires `fcntl(F_FULLFSYNC)`, which is far slower, and Apple's own guidance for many small file-like writes is batching or SQLite. Per-event full durability is therefore not viable on a primary dev platform under load (500-blossom pressure fronts).

The fix is a **policy tiered by event class**, exactly like isolation tiers — the trust invariant is mechanism-independent:

```text
Claim-bearing / side-effecting / final events:
  durable admission — barrier-ordered rename (F_BARRIERFSYNC or
  directory fsync on POSIX; F_FULLFSYNC or group-commit where loss
  is unacceptable), OR an SQLite/WAL admission journal with Events/
  as its file projection.

Ephemeral scratch / intermediate lap events:
  batched — collected into one lap-level packet; individual loss
  on crash is acceptable and disclosed.
```

Storage granularity is an implementation policy. The admission boundary (untrusted until admitted) is the architecture and does not vary by tier.

This is a Truth-layer storage-engine choice (see "Truth, Meaning, and Learning layers" above). An SQLite/WAL admission journal, a plain append-only file, or any other durable store are interchangeable implementations of the same admission boundary — none of them becomes the system's Meaning or Learning layer by being chosen here.

```python
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any


def emit_runtime_packet(packet: dict[str, Any], root: Path = Path(".")) -> Path:
    """Emit one immutable runtime packet using tmp -> inbox atomic rename.

    The caller is responsible for building a packet that matches
    Schema/event-packet.schema.json. This function only handles the
    filesystem commit boundary.
    """
    tmp_dir = root / "Events" / "tmp"
    inbox_dir = root / "Events" / "inbox"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    inbox_dir.mkdir(parents=True, exist_ok=True)

    event_id = packet.setdefault("event_id", f"evt_{uuid.uuid4().hex}")
    packet.setdefault("created_at_ns", time.time_ns())

    tmp_path = tmp_dir / f"{event_id}.{uuid.uuid4().hex}.tmp"
    final_path = inbox_dir / f"{packet['created_at_ns']}__{event_id}.json"

    data = json.dumps(packet, indent=2, sort_keys=True).encode("utf-8")
    with tmp_path.open("wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    # os.replace is atomic when source and destination are on the same filesystem.
    os.replace(tmp_path, final_path)
    return final_path
```

---

## Ingest, projection, and compaction

The ingestor is the only component that admits runtime events into the KG/index projection. Workers emit packets. They do not directly mutate approved schema, human-owned note regions, or durable Wiki claims.

```python
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def claim_next_packet(root: Path = Path(".")) -> Path | None:
    """Claim one inbox packet by renaming it into processing/."""
    inbox = root / "Events" / "inbox"
    processing = root / "Events" / "processing"
    processing.mkdir(parents=True, exist_ok=True)

    for path in sorted(inbox.glob("*.json")):
        claimed = processing / path.name
        try:
            os.replace(path, claimed)
            return claimed
        except FileNotFoundError:
            continue
    return None


def ingest_one_packet(root: Path = Path(".")) -> None:
    """Validate, project, and move one packet to accepted/ or rejected/."""
    packet_path = claim_next_packet(root)
    if packet_path is None:
        return

    accepted = root / "Events" / "accepted"
    rejected = root / "Events" / "rejected"
    accepted.mkdir(parents=True, exist_ok=True)
    rejected.mkdir(parents=True, exist_ok=True)

    try:
        packet: dict[str, Any] = json.loads(packet_path.read_text())
        validate_event_packet(packet)      # implementation-specific schema validation
        check_idempotency(packet)          # event_hash / artifact_hash gate
        check_canary(packet)               # deterministic proof gate where available
        project_into_kg(packet)            # updates rebuildable KG/index projection
    except Exception as exc:
        reason_path = rejected / f"{packet_path.stem}.reason.txt"
        reason_path.write_text(str(exc))
        os.replace(packet_path, rejected / packet_path.name)
        return

    os.replace(packet_path, accepted / packet_path.name)
```

The functions `validate_event_packet`, `check_idempotency`, `check_canary`, and `project_into_kg` are intentionally implementation-specific. The profile requires the boundary and lifecycle, not a specific graph database.

### Compaction

Compaction is slower than capture. It may:

- merge duplicate claims;
- mark superseded facts;
- flag contradictions;
- archive accepted packets out of the hot path;
- update `Evidence/EVIDENCE.md`;
- update machine-owned enrichment below the sentinel;
- append schema observations to `schema_suggestions/`.

Compaction MUST NOT directly promote AI enrichment above the sentinel or mutate approved `schema.yaml` without the human review path already defined in Layer 4.

---

## Runtime tool commands

A Level 4 implementation SHOULD extend deterministic tooling in the same style as `build`, `lint`, `doctor`, and `search-catalog`.

```text
event-doctor      validate runtime folder structure and projection availability
event-scan        list pending packets in Events/inbox/
event-lint        validate packet JSON shape and required causal fields
event-ingest      ingest pending packets into accepted/rejected and project accepted packets
event-coverage    show which accepted packets are represented in the KG/index or Wiki
event-delta       show packets not yet projected or promoted
event-compact     merge, supersede, archive, and update human-readable projections
event-rebuild-kg  rebuild the KG/index projection from accepted/archive packets
```

---

## Runtime conformance

A Runtime Profile implementation MUST:

1. Capture worker/blossom outputs as immutable event packets.
2. Use a staging boundary (`Events/tmp/` → `Events/inbox/`) for complete-file admission.
3. Treat packet order as non-authoritative; causal fields govern projection.
4. Keep the KG/index rebuildable from accepted packets and approved Markdown assets.
5. Use idempotency gates so duplicate packets do not double-mutate state.
6. Move invalid packets to `Events/rejected/` with reason metadata.
7. Compact hot directories so `Events/inbox/` does not become the archive.
8. Publish durable human-readable knowledge through the existing sentinel/hash model.
9. Prevent machine proposal loops using `suggestion_fingerprint` and the schema review path.

---

## Runtime safety notes

- **Runtime packets are untrusted until admitted.** Schema validity is not semantic truth.
- **Canaries should prefer deterministic evidence.** Test logs, parse results, hashes, diffs, and file existence checks are stronger than conversational assertions.
- **The KG/index is a projection, not the capture layer.** It may be rebuilt from accepted packets and approved Markdown assets.
- **Human authority still governs durable knowledge.** Runtime events may propose knowledge, but human-owned regions and approved schemas are still protected by the boundaries and gates above.
- **Hot folders must be cleaned.** `Events/inbox/` and `Events/processing/` are active runtime areas, not archives.
- **Project-native terms must stay tied to behavior.** Terms such as blossom, Salmon Return, Pick-and-Purge, Logic-Bearing Canary, RAM-based Nucleus, and dynamic linker are valid only when the implementation satisfies the definitions in the runtime terminology contract.

---

# Part V — Reference

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
| Runtime event packets | ❌ | ❌ core setup focuses on Raw/Wiki/Schema | ✅ optional Level 4 |
| Vendor-neutral exchange | ✅ primary | not primary | ✅ via OKF export |

---

## Architecture

```
Knowledge Asset  (the center — independent of any tool)
├── Format       — OKF: markdown + YAML frontmatter
├── Governance   — markdown truth, derived catalog, build/lint/doctor gates, refresh-on-read
├── Enrichment   — sentinel boundary + author_hash (two-hash) → no self-retrigger  [PROVEN]
├── Evolution    — schema observer proposes; humans approve (schema_hash + ledgers)
├── Runtime      — optional event packets + KG/index projection + compaction
└── Consumers    — any agent, search index, editor, graph viewer, or runtime
```

The asset is the unit of portability. Tools are replaceable. The asset is not.

For Level 4, runtime packets are the unit of execution-history portability. KG/index projections are replaceable and rebuildable.

---

## Out of Scope (future extensions)

- **Relationship typing.** OKF links are intentionally untyped; relationship meaning is conveyed by surrounding prose, and graph consumers treat links as directed untyped edges. This profile keeps links as OKF-compatible markdown links in v1.5. Future versions may propose *optional* relationship metadata (`depends_on`, `contradicts`, `supports`, `refines`, `duplicates`, `derived_from`, `cites`) **without changing the underlying link format**.
- **Mandatory graph database.** This profile does not require Kuzu, Neo4j, Graphiti, NetworkX, SQLite, or any other graph/index engine. Runtime projection is required for Level 4; the storage engine is not.
- **A hidden agent workspace.** A private source-controlled `knowledgebase/` may expose `Events/`, `Graph/`, `Runtime/`, and `Evidence/` as normal folders. Hidden folders are an implementation choice, not a requirement.

---

## Open Questions

1. **Confidence weighting** — equal weights on frequency / approval / downstream / decay? Better formulas?
2. **Schema versioning** — auto-migrate old notes, keep them at their version, or make the new schema optional?
3. **Multi-team governance** — whose approval gate wins when several teams co-own one asset?
4. **Evolution scope** — may the observer propose new *types*, or only new *fields* (and deprecations) within existing types?
5. **Structural vs. semantic observation** — keep the observer purely structural, or allow an LLM pass to read field *meaning*?
6. **Runtime promotion** — when should accepted runtime packets become Raw sources, compiled Wiki notes, or only KG/index edges?
7. **Compaction policy** — how long should accepted packets remain as individual files before archive/merge?
8. **Projection freshness** — how far may the KG/index lag behind `Events/inbox/` before a query must wait for ingestion?
9. **Terminology stability** — which project-native terms should remain in the profile, and which should be treated as explanatory names only?
---

## Sources & Lineage

- **Google OKF v0.1** — the portable format.
  https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
  Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

- **wanderloots LLM-Wiki** — the governance philosophy (standards enforced through tooling). Build on Obsidian
  - git- https://github.com/wanderloots-tutorials/vibe-coding/blob/main/wanderloots-llm-wiki-core-setup-v1.0.0.md
  - local source reviewed for this draft: `wanderloots-llm-wiki-core-setup-v1.0.0.md`
  - youtube explainer - https://www.youtube.com/watch?v=QbjAQFJJyt0&t=737s

- **Karpathy's LLM Wiki** — maintain a compiled wiki instead of re-retrieving; treat ingested sources as untrusted.
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

- **User-provided Lexicon / Lexicon of Integrity** — terminology discipline for mapping human language into enforceable engineering definitions, detection hints, allowed patterns, and guardrail packs.

This profile fills the two gaps those sources intentionally left open: **enrichment without self-triggering**, and **schema that learns its own structure** — both under permanent human authority.

The Level 4 runtime profile is a further optional extension: it preserves high-volume execution truth as immutable event packets, then projects accepted packets into a KG/index and human-readable knowledge assets under the same boundary-and-gate safety model.

---

## License & Attribution

**License: MIT.** The MIT copyright/permission notice must be preserved in copies or substantial portions. The spec is intentionally permissive — use, implement, extend, adapt.

Credit for the ideas and sources this profile builds on is kept in `ATTRIBUTION.md` and summarized in the README's Lineage section. This profile is not affiliated with or endorsed by Google, wanderloots, Andrej Karpathy, or any other cited source.