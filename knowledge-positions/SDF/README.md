# Knowledge Positions — Software Development Framework (SDF)

This is the **developer-facing navigation to the existing Knowledge Positions method**. It organizes the material; it does not replace the research, define a new method, or require a particular implementation.

Knowledge Positions has two entry points: [the paper](../paper/README.md) and this **Software Development Framework**. For the relationship between JITK and Knowledge Positions, read [the canonical paper](../research/paper.md), especially [§1.2: JITK, Knowledge Positions, and practical use](../research/paper.md#12-the-larger-endeavor-jitk-knowledge-positions-and-practical-use).

**JITK is the broader research and engineering endeavor.** Knowledge Positions is a contribution within it: one source-backed knowledge identity and one logical record, with available values usable by multiple methods. A method may use existing recorded values without creating a competing knowledge object or a mandatory AST-to-graph-to-vector conversion chain. An implementation must not invent values that are absent. The original evidence remains authoritative.

## Read the framework in this order

| Start here | Existing material | What it establishes |
| --- | --- | --- |
| **1. Understand** | [Mission](../MISSION.md), [Architecture](../ARCHITECTURE.md), [Core vocabulary](../CORE_VOCABULARY.md) | Why the method exists, its logical model, and its terminology |
| **2. Specify** | [Common record](../contracts/common-record.md), [Positions](../contracts/positions.md), [Public operations](../contracts/public-operations.md), [First law](../contracts/first-law.md) | Language-independent records, invariants, operations, and boundaries |
| **3. Apply the method** | [Methods](../methods/), [Core](../core/), [Location/access](../LOCATION_ACCESS.md) | Retrieval, relations, proximity, source access, lifecycle, and enrichment |
| **4. See examples** | [Examples](../examples/), [Developer guidance](../docs/implementer-guide.md) | Concrete demonstrations, not mandatory algorithms or technologies |
| **5. Choose tools/language** | [Languages](../languages/), [Adapters](../adapters/), [Python library guide](../docs/python-library-guide.md) | Optional implementations and integration guidance; language is not the method |
| **6. Verify behavior** | [Conformance](../conformance/), [reference-library smoke-check tooling](../tools/) | Whether an implementation maintains the stated requirements; a smoke check is not certification |

### Existing higher-order specifications

These existing specifications extend the practical guidance beyond the introductory paper and core method; neither is rewritten or treated as a new foundational identity:

- [Knowledge Asset Evolution — OKF-compatible extension profile](../Knowledge-Asset-Evolution-Spec-v1.6.3.md): independent source/author/machine/schema hash gates, controlled enrichment, and lifecycle/event boundaries (proposal status in the existing document).
- [Knowledge Graph Relationships and Enrichment](../Knowledge_Graph_Relationships_and_Enrichment.md): useful directional relationship families, evidence distinctions, and qualified enrichment. Its vocabulary is descriptive, not a compulsory universal ontology.

The framework points to the specifications as authored; it does not collapse their separate rules into a rewritten summary or claim that all proposals are implemented.

The stages above are **a reading path**, not a required runtime pipeline. Location, relation, and proximity are addressable values of the **same record**; no sequential conversion between separate knowledge objects is prescribed.

## Paper and framework

- **The paper:** [Just-in-Time Knowledge: Beyond the Context Window](../research/paper.md). Its hypotheses, experiments, limitations, and evolving findings remain at their existing location; the [paper entry point](../paper/README.md) identifies it.
- **Framework reference:** Existing [conceptual](../core/), [contract](../contracts/), and [method](../methods/) documents. These define and explain the shared-identity method without prescribing a programming language.
- **Reference code and practical experiments:** The repository includes an installable [Python implementation](../knowledge_positions.py), [examples](../examples/), and [research experiments](../research/). Other language guides describe their actual status; they are not promises of completed implementations.
- **Generic skill:** The [JITK skill](../skills/knowledge-positions/SKILL.md) belongs conceptually with this framework: it describes how an agent uses available knowledge capabilities, independent of any one agent host. Provider-specific skill packaging and integration are practical examples rather than framework requirements.

The folder layout is intentionally **not** a new set of copied concepts, contracts, or examples. Links point to their existing authoritative files so that organizational cleanup does not fork the framework or disturb the working package.

## Existing outlier to review

The existing `research/` directory contains more than the manuscript: it also holds runnable connector and storage integration experiments (including OmniGraph and LadybugDB work). Those are practical demonstrations, not part of the paper's prose. They are **left where they are for now** rather than moved speculatively or treated as a third conceptual pillar.

## What this does not change

This navigation does **not** rename the Python package, rewrite or relocate the paper, alter the UKC/1 candidate contract, declare additional conformance, or change source files, packaging, tests, or runtime behavior. Any future physical moves should preserve links and test entry points and be made only when the move itself adds value.

## Reconstructible knowledge: an observed cross-language example

[Read the reconstruction account and run the JavaScript example](examples/README.md). While maintaining the living paper, the derived section index was found stale. We reconstructed it from the authoritative manuscript using JavaScript—even though the reference tool was written in Python. The method, stable identities, verified source positions, and resulting navigational data survived the change in language. This is a concrete demonstration of source durability and disposable derived navigation, **not** a claim that any language or unverified transformation is automatically conformant.
