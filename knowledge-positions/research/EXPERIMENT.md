# Original GPS experiment: evidence and replay

## Source and artifact identity

The November 10, 2026 pilot used a 28-passage curated fixture. The original source file is the fixture, not a full chat export. The source owner withheld it from the second model and relayed four requested passages.

| Artifact | SHA-256 / observation |
|---|---|
| Original navigation ZIP | 0b89a64820b4b2b716c6e0d13d0cb3b43f2a2e8ba5c979b1a3fcbd15947cc8a1 |
| Source fixture | c8011e71a141e68d87b740ab138df63e5fe0c8a20f27d1b6100913dde9fb4e02 |
| Original index.json | 152addbf6e3064a70f4497a8650e2b5a8a36e02c6f202a24576a5ffba2b7231b |
| Original index.sqlite | 392bbc32ee8aed7515a51b4922b9e2f591d875e0cf41f6d89acae10338800a81 |
| Original knowledge_positions.py | 392b4fc971c78aee1d792b8af209173d4b816a5e7a6d94878abb3581d7918d53 |
| Original gps.py | e56b8258094e533352e104a642861ea31a27cbf8f1f70059d1690c3cc72d70b9 |

## Historical IDs and verified replay

| Tag | Node ID | Source byte span |
|---|---|---|
| First result | 7fca407d89dd7f1b78e0edf99cacd00f6ffe24f25912dec971c72500f150ee22 | 1951–2014 |
| Second result | 0d9ff06f1c71716a10ffa3ea6888eec1b46a68f297bb10bd3de37e7763a7684e | 2015–2114 |
| Upstream | 55f87710006b396c3dfecf3ca17a2bebaa258b2316295354035217a86f599f98 | 1874–1950 |
| Downstream | c185a2dd7dbb148264024c9de16bf4de66eda126d90bd5af099972efafcf0130 | 2115–2165 |

Offsets are zero-based, end-exclusive. During manuscript preparation the original ZIP was extracted, its source digest checked, the original search rerun, and each of these four IDs resolved using its original gps.py. Results: 28 nodes, 42 edges (27 next_passage, 15 shared_terms); 2,270 source bytes; 288 retrieved span bytes. All four requested passages matched the recorded trial. The original graph and FTS indexes occupied 218,640 and 24,576 bytes respectively. This replay verifies retrieval mechanics, not the reported independent model session or its token use.

## Reproduce the current public example

See [GPS example](../examples/gps/README.md). The example was subsequently maintained, so rebuilt IDs depend on the exact source version and identity algorithm. Use the current search output. The exact original navigation archive is retained with the originating experiment; the published example is not represented as that exact archive.

The original test was human-mediated and the second model's identifier, inference settings, full trace and token counts were not recorded. No comparative baseline or large-corpus test was performed. See paper Sections 6–8 for limits and proposed measurements.
