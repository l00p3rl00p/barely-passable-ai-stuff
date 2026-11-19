# Rust build prerequisites (separate from the OmniGraph representation)

Install once on a machine that builds the Rust ingester. The running OmniGraph engine does not need Rust or Cargo installed just to read/write the graph.

1. Install the current stable Rust toolchain using the official instructions at https://www.rust-lang.org/tools/install (or use an existing stable toolchain). On macOS, install Apple's command-line tools if they are missing: `xcode-select --install`. On Linux use the distribution's native C/C++ build tools, linker and pkg-config as needed. Tree-sitter grammars build native C code. No Python model runtime, Ollama or embedding service is required.
2. Verify prerequisites: `rustc --version`, `cargo --version`, `omnigraph version`.
3. Obtain the Rust ingestion source checkout. Current development workspace: https://github.com/l00p3rl00p/quatrus-scratchpad/tree/feature/omnigraph-schema-init-9d2d6b/experiments/evolving-knowledge-context/GPT/jitk-omnigraph . Use your actual checkout location; it is not required at a fixed path.
4. From that workspace (the directory containing the Rust workspace Cargo.toml), run:

```sh
cargo fetch
cargo build --release --workspace
cargo test --workspace
```

Cargo fetch resolves/downloads the declared dependencies before ingestion. Keep the Cargo-generated lockfile; do not fabricate it or manually pin versions. If resolution or compilation fails, fix the actual manifest/build failure rather than skipping readers. The previous scanner manifest contains declared reader dependencies, not proof of integration or a successful build.

Once the final Rust method is built and accepted, distribute its release executable for the target platform; operators need not repeatedly download dependencies or build it. A build is not ingestion acceptance. Run the real-format and native OmniGraph integration tests before using it for production data.

No installer script and no changes to your shell profile, graph permissions or OmniGraph installation are made by these instructions.
