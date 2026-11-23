### 3.6 On-touch enrichment and cold reconstruction — essential operational example

**Question: “What's wrong with SOUP?”** A cold intelligence need not be handed the answer, and ingestion need not have extracted every entity. It can locate a likely source using any available value; follow recorded source, containment or conversation references; and read the exact relevant section. An imperfect first hit can be sufficient if it supplies a useful place to look.

**A later question:** The intelligence searches again, retrieves a different source, and combines that evidence with the relevant source passage already present in its *current* working context. The newly seen relationship may be useful enough to record. **Ordinary in-context reasoning is not itself a mandatory persistent graph write.**

**Enrichment admission:** When evidence supports a reusable new relationship, add a qualified event/delta with subject, predicate, object, source spans, actor and admission status under the *same knowledge identity*. Do not pretend a model's proposal was directly parsed source metadata. Do not revisit or enrich unrelated files merely because one item was touched. The original sources remain authoritative.

**Cold-start proof:** Delete disposable graph/lexical/vector indexes; keep the original source snapshot, sessions and accepted evidence-backed discoveries that were preserved durably. Rebuild by cheap, deterministic re-ingestion. Ask the identical SOUP question in two isolated runs from the same durable snapshot. Compare supported findings, retrieved locations, cited original passages and unsupported claims. Separately compare against a genuinely unindexed/no-source-access baseline if useful. **A reproducible answer need not use identical words or exact-ranked first hits.** If an accepted discovery existed only in the erased derived database, a failed rebuild reveals a durability defect—not a mandate to enrich the entire corpus.

**The lifecycle is intentionally small:** record available values once → use any suitable retrieval method → follow source evidence → reason in context → optionally admit a qualified useful delta → discard and reconstruct indexes whenever convenient. No initial whole-corpus intelligence job, mandatory positional filling or method-to-method conversion.

