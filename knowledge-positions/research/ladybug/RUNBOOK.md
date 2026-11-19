# Load and use

Install native CLI if needed: https://docs.ladybugdb.com/installation/ (macOS: brew install ladybug). Copy this folder anywhere. From the folder:

```bash
lbug /path/to/knowledge.lbdb < schema.cypher
```

Choose your actual database path. For a populated database inspect and back up first; IF NOT EXISTS does not migrate incompatible tables. Verify KnowledgeItem, EnrichmentCluster, LocationMethod, Relationship and InEnrichmentCluster exist:

```bash
printf 'CALL show_tables() RETURN *;\n' | lbug /path/to/knowledge.lbdb
```

Use your existing native client or the official Ladybug MCP:

```bash
uvx mcp-server-ladybug --db-path /path/to/knowledge.lbdb
```

Configure your existing agent host with that command and real path, or use the existing shared connection. Do not start competing write processes. Copy the whole skills/knowledge-positions-ladybug directory to the host's skills directory. See ACCESS.md for read-only access.

After admitting nonzero compatible vectors, build the native index once, with other database owners closed:

```bash
lbug /path/to/knowledge.lbdb < vector-index.cypher
```

Load VECTOR in querying connections as needed. Verify index maintenance behavior of the installed version. No LLM extension, fallback database or synthetic records.

Acceptance on a separate database using real evidence: admit and retrieve an item, verify original hash and coordinates, link two items with evidence, verify both directions, search same-space vectors, readmit without duplicates/reset, verify three-touch enforcement, and confirm read-only rejects mutation. Do not claim acceptance before execution.

Official docs: https://docs.ladybugdb.com/client-apis/cli/ ; https://docs.ladybugdb.com/cypher/data-definition/create-table/ ; https://docs.ladybugdb.com/extensions/vector/ ; https://github.com/LadybugDB/mcp-server-ladybug .
