# Knowledge Graph Relationships: The Useful 80%

*A practical description of a knowledge graph that connects software, human understanding, evidence, and evolving decisions.*

## The central idea

A graph does not become useful because it has more edges. Sixty thousand relationships can create sixty thousand ways to get lost. The value comes from **a small, understandable vocabulary of relationships**, clear direction, reliable source evidence, and the ability to answer a real question.

The starting point is simple:

> **Entity → relationship → entity**
>
> A relationship should explain something worth knowing: what exists, what depends on what, what causes or produces what, what supports a claim, or what has changed.

An *entity* may be a function, document, system, person, observation, requirement, decision, or idea. An *edge* describes how two entities relate. Some statements are directly observed; others are interpretations, proposals, or unresolved questions. These are not interchangeable.

## 1. The foundation: relationships that answer most questions

These are the core relationship families worth recognizing first. Their names are descriptive labels, not a mandatory universal ontology.

| Basic relationship | Direction | Why it exists |
|---|---|---|
| **CONTAINS / DEFINES** | Container → component | Locate what exists and where it belongs. |
| **IS_A / INHERITS** | Specific type → broader type | Understand classification and specialization. |
| **PART_OF** | Component → whole | Follow composition and ownership of structure. |
| **CALLS / USES** | Consumer → function or service | Trace how components interact. |
| **DEPENDS_ON / REQUIRES** | Dependent → prerequisite | Assess impact and prerequisites. |
| **PRODUCES** | Activity → output | Connect work to results. |
| **READS / WRITES** | Actor → information or artifact | Understand information flow and side effects. |
| **IMPLEMENTS** | Implementation → requirement | Connect the actual system to its intended behavior. |
| **TESTS / VERIFIES** | Test or evidence → subject | Find what has been checked and by what means. |
| **DOCUMENTS / DESCRIBES** | Knowledge asset → subject | Link human explanation to its subject. |
| **REFERENCES / RELATED_TO** | Entity → another entity | Provide navigation when a more precise relationship is not yet warranted. |
| **DERIVED_FROM / SUPPORTED_BY** | Assertion → originating source | Make claims traceable rather than merely plausible. |

These relationships provide a practical starting set, **not a statistically measured 80% coverage claim**. Their purpose is to answer everyday questions such as:

- Where is it, and what does it do?
- What uses it, and what would change if it changed?
- Which requirement is it intended to satisfy?
- What proves the result, and where did that knowledge come from?

**The discipline:** Use the most specific relationship that improves an actual query. Do not create three synonyms for the same edge unless they have materially different meanings.

## 2. The enrichment: relationships added for deeper understanding

Once the foundation works, additional edges are useful for particular domains. These enrich the graph; they are not prerequisites for every graph.

### Software structure, routing, and dependencies

| Enriched relationship | Meaning | Why it is useful |
|---|---|---|
| `OVERRIDES` | Child method → inherited method | Understand changes to inherited behavior. |
| `DECORATES` | Decorator → decorated function | Understand wrapping and interception. |
| `DEPENDS_ON` | Manifest/component → package/service | Trace dependencies and impact. |
| `reads_config` | Code → configuration | Explain where behavior is configured. |
| `writes_artifact` | Code → produced artifact | Identify externally visible effects. |
| `launches_script` | Launcher → script | Trace execution across process boundaries. |
| `dispatches_to` | Command/flag → execution target | Determine what a user command actually invokes. |
| `wraps_module` | Wrapper → underlying module | See indirection instead of confusing wrapper with implementation. |
| `registers_command` | Program → exposed command | Connect interface to available actions. |
| `planned_in` | Feature/configuration → planning document | Connect planned intent with implementation. |
| `TESTS` | Test → code under test | Identify verification coverage. |

### Gaps and unresolved relationships

These are **findings about the graph**, not necessarily normal connections to invented target nodes.

| Finding | What it means | Why retain it |
|---|---|---|
| `unrouted_flag` | A command flag lacks a discovered route. | Expose possible broken command wiring. |
| `dead_space_candidate` | A symbol has no discovered inbound caller. | Surface potentially unused code without calling it dead. |
| `calls_unresolved` | A call target could not be resolved. | Avoid claiming certainty from incomplete parsing. |
| `missing_receiver` | A call receiver could not be identified. | Preserve the exact missing link for later investigation. |

An unresolved edge is **not proof of a missing dependency**. It may reflect dynamic dispatch, incomplete analysis, unsupported syntax, or a genuinely absent connection. Record which one is known.

### Execution, evidence, and intent

| Enriched relationship | Meaning | Why it is useful |
|---|---|---|
| `GOVERNS` | Intent or rule → activity | Keep the purpose visible. |
| `PROPOSES` | Actor → proposed action | Separate suggestion from authorization. |
| `AUTHORIZES` | Decision → permitted action | Record who or what admitted the action. |
| `EXECUTES` | Action → execution | Distinguish a plan from something that ran. |
| `EMITS` | Execution → event | Connect runtime activity to observable evidence. |
| `OBSERVES` | Sensor or source → event | Identify independent observations. |
| `CORROBORATES` | Evidence → consistent evidence | Establish support across sources. |
| `CONTRADICTS` | Assertion/evidence → conflicting assertion/evidence | Preserve disagreement instead of hiding it. |
| `EXPECTED_BY` | Expected event → requirement | Make missing expected events investigable. |
| `ALIGNS_WITH / DEVIATES_FROM` | Observed behavior → intended behavior | Explain whether results served the purpose. |
| `EVALUATES` | Assessment → evidence or predicate | Make a conclusion inspectable. |
| `INTERVENES_IN` | Corrective action → execution | Preserve what was done to redirect behavior. |
| `STOPS / CONTINUES` | Decision → execution | Record control outcomes. |

These do not make the graph itself a judge. **An evaluation is a separate operation** that consumes relationships and evidence, then records its result with provenance. A code path that *could* write a file is not proof that a file *was* written.

### Human knowledge, decisions, and learning

| Enriched relationship | Meaning | Why it is useful |
|---|---|---|
| `SUPPORTS / REFUTES` | Evidence → claim | Distinguish substantiated claims from assertions. |
| `ASSUMES` | Conclusion → assumption | Reveal what an answer depends upon. |
| `REFINES` | New understanding → previous understanding | Preserve improvement without erasing history. |
| `SUPERSEDES` | Current decision → earlier decision | Retrieve the current position while retaining why it changed. |
| `INVALIDATES` | Evidence → previous conclusion | Expose knowledge that no longer holds. |
| `AFFECTS` | Change → impacted entity | Support impact analysis across technical and human domains. |
| `DERIVED_FROM` | Knowledge record → source passage/event | Return to the original rather than reinterpreting a summary indefinitely. |

## 3. How intersections become knowledge

A single edge tells you one fact. A **small, well-grounded path** tells you something actionable.

For example:

```text
Requirement
    ↑ IMPLEMENTS
Function ── reads_config ──> Configuration
    │
    ├── writes_artifact ─────> Output
    │
    └── TESTED_BY <────────── Test

Runtime execution ── EMITS ──> Observation
Observation ── SUPPORTS or CONTRADICTS ──> Claim about the result
```

This answers different questions without confusing them:

1. **Structure:** What can the function do?
2. **Intent:** What is it supposed to accomplish?
3. **Execution:** What actually happened?
4. **Evidence:** What independent source confirms the result?
5. **History:** Was that conclusion refined, rejected, or superseded later?

A relationship's **direction**, scope, and evidence matter more than adding a large number of loosely defined edges.

## 4. How the knowledge center operates

The knowledge center joins **human knowledge** and **computer-derived knowledge** without making either silently overwrite the other.

```text
Human-authored knowledge ──┐
                           ├──> Portable knowledge assets
Code / docs / configs ─────┤       (Markdown + metadata + links)
Runtime observations ──────┘                  │
                                             ▼
                                Parse / index / enrich
                                             │
                              ┌──────────────┴─────────────┐
                              ▼                            ▼
                       Knowledge index               Graph relationships
                              └──────────────┬─────────────┘
                                             ▼
                              Query relevant connected facts
                                             ▼
                              Return answer + source evidence
```

**Human knowledge** includes intent, decisions, rationale, requirements, lessons, context, and corrections. **Computer knowledge** includes syntax, code structure, dependencies, file and process behavior, tests, telemetry, and observed results. **Links** join these without demanding that every source be stored in one database.

The operating rules are deliberately modest:

- **Source remains source.** Keep original text, code, event, and human decisions available. An index or semantic projection is not a substitute for them.
- **Separate ownership.** Human-authored material and machine-generated enrichment have distinguishable regions or records. Automation may suggest or annotate without silently rewriting a human decision.
- **Enrich only when relevant content changes.** Keep a whole-file `file_hash` as the freshness/watchdog check, then independently compare stable author-section `author_hash[]` and machine-enrichment `machine_hash[]` values only for touched files. The sentinel distinguishes ownership, not a single document-wide author unit. A changed author section initiates a materiality assessment, not automatic regeneration: formatting-only changes may leave tags, claims, and relationship hashes unchanged. Uncertain claims require review, not silent acceptance; only qualified affected dependencies need revalidation. The machine's own writes must not retrigger author enrichment.
- **Navigate across files, not only within one document.** File-local section positions contribute to a single derived repository JSON index: stable section identity, source coordinates and hash, optional vector position, and qualified cross-document edges. NetworkX can traverse the same evidence-linked graph that vector retrieval helps discover. Mere lexical overlap is a candidate relationship, not a verified semantic edge; preserve unaffected section identity and vectors when files elsewhere change.
- **Preserve qualification.** Store relationship type, direction, origin, evidence, confidence when meaningful, and lifecycle status (`observed`, `proposed`, `reviewed`, `rejected`, `superseded`, or `unresolved`).
- **Keep history.** Correct a mistaken claim by recording the correction and its source, not by pretending the earlier claim never existed.
- **Retrieve just in time.** Find the smallest connected set that answers the question; expand to the original source only when needed.
- **Treat missing evidence carefully.** An absent event is meaningful only if the source was expected to capture it and coverage is known.

The two key distinctions are **knowledge versus index** (original knowledge persists even if an index is rebuilt) and **evidence versus interpretation** (an inference never silently becomes an observation).

## 5. How OKF fits

[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) is a portable way to exchange knowledge using Markdown with YAML frontmatter, concepts, and links. It is not itself a mandatory graph database or a prescribed list of edge types.

A simple portable knowledge note might look like:

```markdown
---
type: decision
title: Use a shared configuration service
tags: [architecture, configuration]
---

# Use a shared configuration service

The service centralizes settings for the application.

## Relationships
- REQUIRES: [Configuration schema](../schemas/configuration.md)
- IMPLEMENTED_BY: [Configuration client](../components/config-client.md)
- DERIVED_FROM: [Architecture discussion](../sessions/architecture-discussion.md)
```

**Typed labels above are an application convention in the Markdown body**, not required OKF relationship syntax. A graph indexer can read them and build navigable relationships while the underlying notes remain ordinary, portable Markdown. If a system uses machine-readable typed edges in additional YAML fields, those fields should be documented as an extension rather than attributed to the base specification.

An extended **Knowledge Asset Evolution** profile (version **1.6.3**) describes additions for living knowledge: human/machine ownership boundaries, a whole-file freshness watchdog plus independently hashed author sections and required machine enrichment sections, materiality-sensitive updates, human-reviewed schema evolution, and the separation of durable execution truth from derived meaning. The historical two-hash reference tests establish its original ownership boundary, not yet the generalized section-scoped refinement. Its version number belongs to that extension profile, **not to Google's OKF specification**.

**References**

- [Google — Open Knowledge Format specification (upstream v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- [Google — Knowledge Catalog OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- Companion document: [Knowledge Asset Evolution: An OKF-Compatible Extension Profile](Knowledge-Asset-Evolution-Spec-v1.6.3.md), version 1.6.3.

---

**The point:** Build the relationships that let someone locate something, explain its purpose, trace its dependencies, test its behavior, inspect the evidence, and recover how the understanding changed. Everything else is an enrichment justified by a real question—not a competition to create the most edges.