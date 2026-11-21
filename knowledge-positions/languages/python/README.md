# Python SDK — existing library

The existing installable **experimental** Knowledge Positions Python distribution is at [`../../pyproject.toml`](../../pyproject.toml). Its implementation is [`knowledge_positions.py`](../../knowledge_positions.py); **this directory does not contain a second Python implementation**.

Install from the existing `knowledge-positions/` directory:

```sh
python -m pip install .
```

Import the existing API:

```python
from knowledge_positions import KnowledgePositions

k = KnowledgePositions(encoder=my_existing_encoder, model_name="my-declared-vector-space")
# Use k.add(...), k.link(...), k.neighbors(...), k.search(...) as implemented.
```

Pass a real compatible encoder if vector computation is needed; `defer_embedding=True` on admission avoids compulsory embedding. The existing [capture workflow](../../capture.py), [graph/vector analysis](../../core_operations.py), and [OmniGraph adapter](../../research/omnigraph/adapter.py) remain separate consumers, not required parts of the SDK contract.

**UKC/1 status:** An existing Python API is available, but its historic identity and record format are not the same as the [UKC-ID-1](../../core/identity.md) and [common record](../../contracts/common-record.md) contract. Do not claim full UKC/1 parity or lossless OKF interchange without executing the [shared conformance suite](../../conformance/requirements.md). See the [capability map](../../docs/component-and-capability-map.md) for exact coverage and gaps.
