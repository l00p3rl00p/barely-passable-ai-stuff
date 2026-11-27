# SDK validation tools

The current installable library is the existing Python `knowledge_positions` package. This directory contains a **portable smoke test** for that package and a reference to the separate, language-neutral UKC/1 conformance contract.

## Smoke check: existing Python implementation

From `knowledge-positions/`, after `python -m pip install .`:

```sh
bash tools/check-sdk.sh
```

[`check-sdk.sh`](check-sdk.sh) checks Python syntax and executes [the first-use example](../examples/sdk_first_use.py), which asserts its expected output. It requires no configured OmniGraph target, LLM provider, original private source corpus, or local machine-specific path.

## Full conformance is distinct

See [UKC/1 conformance requirements](../conformance/requirements.md). The shared test contract covers canonical identities, complete native records, lossless OKF exchange, source authorization, vector compatibility, and cross-language parity. The smoke check above **does not** certify any of those unimplemented or untested conditions.

The historical characterization documents currently record missing standalone probes on `main`; do not claim a successful run of unavailable tests.

## Regenerate the documentation knowledge graph

The [documentation graph](../index.md) is a deterministic view of the existing Markdown, not a new UKC or OKF record store. The scanner uses the same CommonMark parser family as the existing alpha reader and preserves source bytes. It lists native Markdown links and backlinks without semantic inference. Existing malformed YAML is reported, not silently fixed.

From `knowledge-positions/`:

```sh
python -m pip install markdown-it-py ruamel.yaml
python tools/graph-docs.py --write
python tools/graph-docs.py
```

The second command checks that regeneration is stable. For a graph consumer, pass `--graph-json /tmp/kp-docs-graph.json` to export a disposable derived graph; the documents remain authoritative. The graph is document-level and does not claim typed semantic relationships or UKC/OKF conformance.
