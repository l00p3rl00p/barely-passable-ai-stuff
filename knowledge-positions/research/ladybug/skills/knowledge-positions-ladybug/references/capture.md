# Capture and contribution

Canonical research/library govern admission. No second implementation included; do not claim library validation unless it ran. Position, Relation, Proximity, Resonance (research only). Source remains authoritative.

New records include id, kind, source_id, source_precision, status, enrichment_touches=1, enrichment_touch_limit=3, enrichment_frozen=false plus verified source/version/span/position and available metadata. Canonical identity/hash rules apply. Unverified locator-only fields stay null rather than fabricated; container coordinates must not pretend to be UTF-8 offsets. Use scanner-compatible lexical-hash-512, not the incompatible capture.py variant. Unknown vectors remain unknown. No LLM extension.

Within a native write transaction, look up id, verify existing identity/source/version/lifecycle, CREATE only if absent. Never overwrite reviewed enrichment on reread. For relationships verify both endpoints and evidence, MERGE by source, target, relation and canonical evidence_key; preserve independent evidence and existing reviewed lifecycle. Record qualification and origin. Node primary key ensures node identity; edge uniqueness requires writer transaction. Enrichment follows admission plus two changes then grow outward. Verify source before updates, preserve history and propagate lifecycle by canonical contract. Never implicitly revive historical items. Native schema alone does not enforce all these rules.

Use native parameterized Cypher or bulk load of already admitted records with equivalent transactional checks. The skill does not replace the writer.
