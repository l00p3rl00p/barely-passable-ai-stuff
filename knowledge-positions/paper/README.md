# The paper

> **Paper lock — research baseline.** The manuscript is the completed research artifact, not the running log for new specifications, implementation discoveries, or framework additions.
>
> Before proposing any change, ask: **(1) Is the point already clear in the paper?** If yes, leave the manuscript unchanged and continue in the [SDF](../SDF/README.md). **(2) If it is not clear, why not?** Inspect whether the material is absent, contradictory, or simply distributed across sections. That finding is grounds for review, **not automatic permission to edit the paper**. Preserve the manuscript unless a specific, justified correction is explicitly agreed.

The canonical manuscript is **[Just-in-Time Knowledge: Beyond the Context Window](../research/paper.md)**.

It is the paper: the original inquiry, arguments, experiments, limitations, and subsequent findings. It is not the Software Development Framework.

The paper currently lives in `research/paper.md` alongside its section index, companion artifacts, and reproducible experiments. This entry point keeps the manuscript at its existing authoritative path; it does **not** copy or move the paper, which would invalidate source coordinates and existing references.

To apply the Knowledge Positions method, see the separate [Software Development Framework (SDF)](../SDF/README.md).

## Verify the paper's living Knowledge Positions

The manuscript's section-scoped navigation is derived from the authoritative source. After any approved paper change, its positions, hashes, and index must be maintained without changing the source to fit the index.

From `knowledge-positions/research/` (with the existing Python dependencies installed):

```sh
python jit_index.py verify
```

If verification fails, inspect the source change and then regenerate the **derived index only** with `python jit_index.py build`; run `python jit_index.py verify` again. The verifier checks the complete paper hash, all tagged sections and ordered coordinates, section digests, and relationship endpoints. The historical whole-paper companion is not the current maintenance authority.

## Reconstruction demonstration: Python method, JavaScript execution

During a later integrity check, the existing paper's derived JIT index was stale. The assistant worked from the **unchanged authoritative paper** and the existing Python method, reconstructed the same section-scoped navigation in JavaScript, and restored the index without running Python. This was later maintenance evidence, not a new result of the original manuscript experiment.

The complete account, runnable [JavaScript source](../SDF/examples/rebuild-paper-index.mjs), and [try-it-yourself instructions](../SDF/examples/README.md) live in the SDF, so the paper remains locked while its living navigation can still be reconstructed.
