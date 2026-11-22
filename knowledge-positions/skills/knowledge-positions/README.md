# JITK — Just-in-Time Knowledge skill

**One self-contained skill.** Use [`SKILL.md`](SKILL.md) when a task benefits from finding, connecting, verifying or evolving knowledge. The agent can navigate Location, Relation and Proximity by any available method without reading the full SDK or invoking an additional skill.

## Files in this folder

| File | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | The active skill: YAML `intent` and `trigger`, JITK method guidance, **and** the appendix already at the bottom |
| [`jitk.md`](jitk.md) | The same marker-delimited appendix as a reusable, standalone piece for appending to **another** skill |
| [`append-to-skill.sh`](append-to-skill.sh) | Bash helper that appends `jitk.md` to an existing `SKILL.md`; repeated calls skip the existing marker |
| [`README.md`](README.md) | This file |

The appendix describes available methods, with **OmniGraph** (native graph access via the installed OmniGraph skill, CLI or MCP) and **Codebase MCP / Codebase Memory** (code navigation, structural positions and codebase graph traversal) as *two known examples*, not required dependencies. It does **not** invent a slash command or tool name: use the actual installed interface and permissions. Additional readers, parsers or stores are equally valid.

## Install or use this skill

Copy or reference this folder through your agent host's usual skill-discovery mechanism. The host determines when and how skills load; copying the folder does not install a database, MCP server, prompt hook or background job.

The active `SKILL.md` **already contains the appendix**. Do **not** run the append helper against it for installation.

## Append JITK to another skill

From the root of this GitHub repository, run:

```bash
bash knowledge-positions/skills/knowledge-positions/append-to-skill.sh /path/to/other-skill/SKILL.md
```

Or, from within this skill's folder:

```bash
bash append-to-skill.sh /path/to/other-skill/SKILL.md
```

The helper requires Bash and a writable, existing target file. It appends to EOF, retains all preceding bytes, refuses a missing target, and skips adding the appendix again if the start marker is present. It does not run JITK, query a graph, scan files or modify source knowledge.

For the existing **Quatrus-specific OmniGraph** deployment only, an additional optional flag is supported when using the complete repository checkout:

```bash
bash knowledge-positions/skills/knowledge-positions/append-to-skill.sh /path/to/omnigraph/SKILL.md --quatrus
```

That adds the generic appendix and the separate existing Quatrus ingestion instructions, while rejecting a non-OmniGraph target. This is *not* a generic JITK configuration. For OmniGraph engine operations, retain its version-matched native skill and companion references.

## Verification and previous material

Check that the target's original contents are unchanged up to the first `<!-- knowledge-positions-jitk:start -->` marker, and that the appendix occurs only once. To check shell syntax, run `bash -n knowledge-positions/skills/knowledge-positions/append-to-skill.sh` from the repository root.

The previous longer Knowledge Positions skill and its helper are preserved in [the archive](../../archive/knowledge-positions-skill-2026-11-21/); that archive is not the active JITK skill. The [Knowledge Positions SDK](../../README.md) is optional technical reference material, never a prerequisite for using this skill.
