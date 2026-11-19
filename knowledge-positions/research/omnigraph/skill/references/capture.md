# Capture and contribution

Invoke the installed bundle's adapter.py using its virtual-environment Python. Specify your configured native target and graph/branch. Use --help for exact arguments if needed. Standalone graph: --target ./graph.omni; server: --target NAME --graph ID.

- capture PATH --domain DOMAIN --reviewed: admit actual UTF-8 evidence; --start/--end select inclusive lines; --kind/--heading describe the unit.
- item ID, read ID, by-source SOURCE: direct access. A changed source is not current evidence.
- neighbors ID: immediate incoming and outgoing associations.
- search SUBJECT: deterministic lexical proximity plus full text, bounded results. Only after earlier gates are insufficient.
- link SRC DST RELATION EVIDENCE --reviewed: preserve qualified evidence, both endpoints already admitted.
- enrich ID MEANING --reviewed: retain a finding; duplicate finding is a no-op, two refinements after admission.

Retain human/agent-authored findings as durable reviewed sources (prefer OKF Markdown with type, title and source references). Capture those files; do not confuse a note with original evidence. Preserve contributions outside disposable projections. Domain does not grant access. Stop reading once sufficient.
