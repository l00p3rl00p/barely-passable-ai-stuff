#!/usr/bin/env bash
# Portable smoke check of the *existing Python library*, not UKC/1 certification.
# Run after installing from knowledge-positions/: bash tools/check-sdk.sh
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

python -m compileall -q knowledge_positions.py examples/sdk_first_use.py
python examples/sdk_first_use.py
echo "Python SDK first-use smoke check passed (not full UKC/1 conformance)."
