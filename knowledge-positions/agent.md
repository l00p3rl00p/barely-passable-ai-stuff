# Agent reference — Knowledge Positions library

This is a capability reference, not a project assignment. Read the [Quick Start](README.md#quick-start--capture-working-conversations), [Core Vocabulary](CORE_VOCABULARY.md) and [Runbook](RUNBOOK.md). Use the actual library and [capture.py](capture.py).

The API accepts caller-selected source-backed knowledge, creates location/relation/proximity slots, links qualified relationships, saves/loads and verifies records, and supports ten native graph views plus arbitrary named derivation. Unknown vectors are null. Semantic payload mutation has a hard three-touch budget; after touch 3 grow outward through relationships/new nodes. `chat_context` uses graph-theoretic attenuation by default with a conservative/balanced/aggressive dial; explicit ego radius is available when requested. Full graph analysis and dependency invalidation remain unrestricted.

An agent's human/application instructions determine which conversations to read, what to retain, where to store it, how often to capture and whether to commit/push. Do not assume a particular provider, private repository or workflow. Do not invent source identifiers, relationships or vectors; preserve evidence and authorization boundaries. If given a project-specific instruction file, follow that file's scope and policy while using the library's documented operations.
