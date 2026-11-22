#!/usr/bin/env bash
# Append existing JITK instructions to any installed skill; optionally add Quatrus OmniGraph specifics.
# Does not rewrite, upgrade, or reformat the original file. Idempotent by section marker.
set -euo pipefail

usage() {
  echo "Usage: bash append-to-skill.sh /path/to/SKILL.md [--quatrus]" >&2
  echo "Use --quatrus only for an OmniGraph skill in the configured Quatrus environment." >&2
}
if [[ $# -lt 1 || $# -gt 2 ]]; then usage; exit 2; fi
target=$1
if [[ ! -f "$target" ]]; then
  echo "Skill file does not exist: $target" >&2
  exit 2
fi
if [[ $# -eq 2 && "$2" != "--quatrus" ]]; then usage; exit 2; fi

if [[ $# -eq 2 ]] && ! grep -Eq '^name:[[:space:]]*omnigraph[[:space:]]*
generic="$here/jitk.md"
quatrus="$here/../../research/omnigraph/skills/omnigraph-upstream-plus-quatrus/quatrus-ingestion.appendix.md"

append_once() {
  local file=$1 marker=$2 label=$3
  if ! grep -Fq "$marker" "$file"; then
    echo "Invalid appendix: $file" >&2
    exit 2
  fi
  if grep -Fq "$marker" "$target"; then
    echo "Already present: $label (unchanged)"
    return
  fi
  # Add only at EOF; leave the original contents byte-for-byte untouched.
  printf '\n\n' >> "$target"
  cat "$file" >> "$target"
  echo "Appended: $label"
}

append_once "$generic" '<!-- knowledge-positions-jitk:start -->' 'generic JITK'
if [[ $# -eq 2 ]]; then
  append_once "$quatrus" '<!-- quatrus-ingestion:start -->' 'Quatrus OmniGraph'
fi
 "$target"; then
  echo "Refusing Quatrus-specific appendix: skill name is not omnigraph" >&2
  exit 2
fi

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
generic="$here/jitk.md"
quatrus="$here/../../research/omnigraph/skills/omnigraph-upstream-plus-quatrus/quatrus-ingestion.appendix.md"

append_once() {
  local file=$1 marker=$2 label=$3
  if ! grep -Fq "$marker" "$file"; then
    echo "Invalid appendix: $file" >&2
    exit 2
  fi
  if grep -Fq "$marker" "$target"; then
    echo "Already present: $label (unchanged)"
    return
  fi
  # Add only at EOF; leave the original contents byte-for-byte untouched.
  printf '\n\n' >> "$target"
  cat "$file" >> "$target"
  echo "Appended: $label"
}

append_once "$generic" '<!-- knowledge-positions-jitk:start -->' 'generic JITK'
if [[ $# -eq 2 ]]; then
  if ! grep -Eq '^name:[[:space:]]*omnigraph[[:space:]]*$' "$target"; then
    echo "Refusing Quatrus-specific appendix: skill name is not omnigraph" >&2
    exit 2
  fi
  append_once "$quatrus" '<!-- quatrus-ingestion:start -->' 'Quatrus OmniGraph'
fi
