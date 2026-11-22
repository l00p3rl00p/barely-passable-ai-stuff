# Knowledge Positions — generic JITK skill package

Install **this directory** as one skill. It is independent of OmniGraph, any specific graph engine, an LLM provider, and the original development environment.

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Generic Knowledge Positions skill, including the JITK appendix at its end |
| [`jitk.md`](jitk.md) | Same standalone, marker-delimited JITK appendix to reuse with other skills |
| [`append-to-skill.sh`](append-to-skill.sh) | Bash-only append helper: does not rewrite or replace a target skill |

The generic skill explains **Reuse → Direct access → Explore → Discover**, how to select actually available Position / Relation / Proximity capabilities, source verification, bounded results and qualified contribution. It delegates implementation commands and access controls to whichever storage, parser, library, or service is actually selected.

## Append JITK to another installed skill

From a directory containing this package, run:

```bash
bash knowledge-positions/skills/knowledge-positions/append-to-skill.sh /path/to/other-skill/SKILL.md
```

Substitute the actual destination. The helper appends only the [JITK appendix](jitk.md), skips an existing marker, and never replaces upstream instructions. **Do not run it against this packaged `SKILL.md` to install JITK: the appendix is already included.**

For an optional, **Quatrus-specific** OmniGraph installation in the complete repository checkout, the same helper accepts `--quatrus`. That adds the existing Quatrus appendix from its separate location and is neither an OmniGraph requirement nor a generic JITK default. See the [OmniGraph integration README](../../research/omnigraph/skills/omnigraph-upstream-plus-quatrus/README.md) for the one-command invocation.

No install, scan, ingestion, or database connection occurs when reading or packaging these files. The helper modifies a destination only when explicitly invoked.
