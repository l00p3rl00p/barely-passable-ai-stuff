#!/usr/bin/env bash
# Append Knowledge Positions JITK to an existing skill without rewriting its content.
# Optional --quatrus applies only to an OmniGraph skill in a configured Quatrus environment.
set -euo pipefail

usage() {
  printf 'Usage: bash append-to-skill.sh /path/to/SKILL.md [--quatrus]\n' >&2
}
if [[ $# -lt 1 || $# -gt 2 ]]; then usage; exit 2; fi
target=$1
if [[ ! -f "$target" ]]; then
  printf 'Skill file does not exist: %s\n' "$target" >&2
  exit 2
fi
if [[ $# -eq 2 && "$2" != "--quatrus" ]]; then usage; exit 2; fi

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
generic="$here/jitk.md"
# For a standalone generic skill install, only the generic appendix is needed.
# Quatrus remains an optional, repository-local integration.
quatrus=""
for candidate in \
  "$here/../../research/omnigraph/skills/omnigraph-upstream-plus-quatrus/quatrus-ingestion.appendix.md" \
  "$here/../../../research/omnigraph/skills/omnigraph-upstream-plus-quatrus/quatrus-ingestion.appendix.md"; do
  if [[ -f "$candidate" ]]; then quatrus="$candidate"; break; fi
done

append_once() {
  local file=$1 marker=$2 label=$3
  if [[ ! -f "$file" ]] || ! grep -Fq "$marker" "$file"; then
    printf 'Invalid or missing appendix: %s\n' "$file" >&2
    exit 2
  fi
  if grep -Fq "$marker" "$target"; then
    printf 'Already present: %s (unchanged)\n' "$label"
    return
  fi
  # Preserve every pre-existing byte. Add new instructions at EOF only.
  printf '\n\n' >> "$target"
  cat "$file" >> "$target"
  printf 'Appended: %s\n' "$label"
}

# Preflight optional Quatrus mode before writing anything.
if [[ $# -eq 2 ]]; then
  if ! grep -Eq '^name:[[:space:]]*omnigraph[[:space:]]*$' "$target"; then
    printf 'Refusing Quatrus appendix: target is not an OmniGraph skill\n' >&2
    exit 2
  fi
  if [[ -z "$quatrus" ]] || ! grep -Fq '<!-- quatrus-ingestion:start -->' "$quatrus"; then
    printf 'Quatrus appendix unavailable; use a complete repository checkout\n' >&2
    exit 2
  fi
fi
append_once "$generic" '<!-- knowledge-positions-jitk:start -->' 'generic JITK'
if [[ $# -eq 2 ]]; then
  append_once "$quatrus" '<!-- quatrus-ingestion:start -->' 'Quatrus OmniGraph'
fi
