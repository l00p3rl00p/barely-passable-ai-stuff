# Knowledge Positions — Software Development Framework (SDF)

This is the **developer-facing navigation to the existing Knowledge Positions method**. It organizes the material; it does not replace the research, define a new method, or require a particular implementation.

Knowledge Positions has two entry points: [the paper](../paper/README.md) and this **Software Development Framework**. For the relationship between JITK and Knowledge Positions, read [the canonical paper](../research/paper.md), especially [§1.2: JITK, Knowledge Positions, and practical use](../research/paper.md#12-the-larger-endeavor-jitk-knowledge-positions-and-practical-use).

**JITK is the broader research and engineering endeavor.** Knowledge Positions is a contribution within it: one source-backed knowledge identity and one logical record, with available values usable by multiple methods. A method may use existing recorded values without creating a competing knowledge object or a mandatory AST-to-graph-to-vector conversion chain. An implementation must not invent values that are absent. The original evidence remains authoritative.

## Developer guide and table of contents

JITK is an approach to making knowledge available when needed. KP represents knowledge through Location, Relation, Proximity and Resonance (currently a reserved UKC extension). UKC is the common record contract. OKF is the external interoperability format. This SDF is the development framework; kits implement it against their native targets. The paper is an independent research perspective.

| Step / goal | Read in order | Check your work |
|---|---|---|
| 1. Understand the framework | [First Law](../contracts/first-law.md), [positions](../contracts/positions.md), [scope and authority](../docs/authority-and-evidence.md) | Identify common identity and separate JITK, KP, UKC, OKF, SDF and kits. |
| 2. Know what to capture | [Complete capture reference](../contracts/common-record.md), [identity algorithm](../core/identity.md), [relationship vocabulary](../CORE_VOCABULARY.md) | Every required/conditional field, provenance and missing-value behavior accounted for. |
| 3. Know how it operates | [Native ingestion](../contracts/native-ingestion.md), [lifecycle and block grouping](../core/lifecycle.md), [relationships](../core/relations-and-enrichment.md), [public operations](../contracts/public-operations.md) | Check processing boundaries, touch budget, supported groupings and retrieval. |
| 4. Build a kit | [SIPOC assembly cookbook](../docs/implementer-guide.md), [reader crosswalks](../readers/native-to-common.md), [native adapters](../adapters/README.md) | Assess native capabilities, implement only gaps, execute recipe checks. |
| 5. Check and certify | [UKC conformance](../conformance/requirements.md), [independent review checklist](../conformance/sdf-independent-review.md), [scanner/emitter checks](../conformance/scanner-emitter-checklist.md) | Record actual inputs, expected and observed outputs, pass/fail/blocked. |
| 6. Use existing components | [Rust](../languages/rust/README.md), [Python reference](../languages/python/README.md), [TypeScript status](../languages/typescript/README.md), [examples](../examples/README.md) | Verify actual capabilities and limitations before installation/use. |
| 7. Explore research | [Paper](../paper/README.md), [research](../research/README.md), [reconstruction examples](examples/README.md) | Distinguish existing experiments from normative requirements and current verification. |

For a complete section-by-section normative index, see [UKC specification](../unified-knowledge-context.md). For existing component coverage, see the [capability map](../docs/component-and-capability-map.md). No implementation must read historical experiments to discover hidden requirements.

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

This navigation does **not** rename the Python package, rewrite or relocate the paper, declare additional conformance, or change runtime code, packaging, tests or configuration. Approved contract clarifications are owned by their linked normative sections. Any future physical moves should preserve links and test entry points and be made only when the move itself adds value.

## Reconstructed Knowledge Positions — executed, cross-language paper proof

[Run the complete current-paper reconstruction](examples/README.md) in Python or JavaScript. Both implementations read the existing public paper and archived companion without modifying them. In the latest verified execution, they produced **29 current `ukc/1` common records**, found **15 unchanged historical sections**, reproduced **15 matching lexical vectors**, and reconstructed **38 source-observed structural relations plus eight hash-qualified historical editorial navigation relations**. Another 22 historical editorial links remain inactive because the underlying source version changed.

This is the language-neutral shared-record method in actual use: one canonical source-backed identity per section, available Location/Relation/Proximity values, honest native structural metadata, verified original-byte resolution, and portable records using the historical `x_ukc` spelling (the current interchange contract uses `x-ukc`). The [shared regression test](../tests/test_paper_reconstruction.py) is executed by [GitHub Actions](../../.github/workflows/paper-reconstruction.yml). Existing [three-touch tests](../tests/test_enrichment_budget.py) separately establish that semantic payload mutation freezes after the third touch while qualified outward relationships remain possible. No historical per-edge touch attribution is claimed.

The public example is intentionally **EKC-anchored Markdown only**; it does not claim full CommonMark AST fidelity or complete source-agnostic SDK certification. The original manuscript and historical index remain intact. This is a technical reproduction of the current paper, not a retroactive amendment to its original research.
