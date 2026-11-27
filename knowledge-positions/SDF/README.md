# Knowledge Positions — Software Development Framework (SDF)

[Knowledge Positions home](../README.md)

## Start here

You do not need to read every Markdown file. Pick the task you want to complete and follow only that path.

| I want to… | Start with one document |
|---|---|
| Understand the method | [First Law](../contracts/first-law.md) |
| Build or improve a kit | [Implementation cookbook](../docs/implementer-guide.md) |
| Know what data to capture | [Complete capture reference](../contracts/common-record.md) |
| Check a kit or its implementation status | [Conformance](../conformance/requirements.md) |
| Find the existing Rust components | [Rust component guide](../languages/rust/README.md) |
| Run an existing example | [Examples](../examples/README.md) |
| Use JITK as an agent | [JITK skill](../skills/knowledge-positions/README.md) |
| Read the research | [The paper](../paper/README.md) |

JITK is an approach to making knowledge available when needed. KP represents knowledge through Location, Relation, Proximity and Resonance (currently a reserved UKC extension). UKC is the common record contract; OKF is the external interoperability format; the SDF is the development framework; kits implement it against native targets. The paper is an independent research perspective.

## Build a kit: read in this order

Each step has one primary document. Follow its supporting links only when needed. Stop when the question you are answering is resolved; do not read research to discover mandatory requirements.

| Step | Open | Done when |
|---|---|---|
| 1. Understand | [First Law](../contracts/first-law.md) | You understand one identity, one logical record and independent access methods. |
| 2. Capture | [Common record](../contracts/common-record.md) | You can list required/conditional fields and unknown-value behavior. |
| 3. Process | [Lifecycle](../core/lifecycle.md) | You can distinguish touch 0–3 and block grouping; native ingestion is independently defined in the [native ingestion contract](../contracts/native-ingestion.md). |
| 4. Assemble | [SIPOC cookbook](../docs/implementer-guide.md) | You know the supplier, input, process, output, customer, native capabilities and checks for each selected component. |
| 5. Verify | [Conformance requirements](../conformance/requirements.md) | You can report actual pass, fail, blocked and unsupported results. |

## Reference map — open only as needed

| Folder | First document | Purpose |
|---|---|---|
| Contracts | [Contracts guide](../contracts/README.md) | Normative record, ingestion and operations. |
| Core | [Core guide](../core/README.md) | Identity, lifecycle, relationships and recovery. |
| Methods | [Methods guide](../methods/README.md) | Applicable retrieval, graph and proximity methods. |
| Readers | [Reader guide](../readers/README.md) | Native parser fidelity and field mappings. |
| Implementation guidance | [Docs guide](../docs/README.md) | Cookbook, authority and component inventory. |
| Conformance | [Conformance guide](../conformance/README.md) | Requirements, evidence and review checklists. |

For the complete section-by-section normative index, see [UKC specification](../unified-knowledge-context.md). For what is actually implemented, see the [capability map](../docs/component-and-capability-map.md). Normative requirements are distinct from implementation guidance, optional host profiles, historical experiments and research.

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
