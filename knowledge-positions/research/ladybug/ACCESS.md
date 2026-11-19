# Native access

LadybugDB is embedded. Do not manufacture equivalents to OmniGraph policy YAML, identities or branches. Use native opening modes and OS permissions.

Read-only human or agent CLI:

```bash
lbug --read_only /path/to/knowledge.lbdb
```

Authorized contributor/maintenance: lbug /path/to/knowledge.lbdb (read-write). Raw write access also permits schema changes; no separate schema privilege is implied. The official MCP exposes general Cypher and its documented CLI options have no read-only switch. Do not grant unrestricted MCP or writable file access to a read-only actor. Use existing host/service authorization where needed or native read-only clients. No new authorization service is required by this representation.

Respect native concurrency: one owning read-write database process; multiple connections in it as supported. Separate processes may be blocked by locks, including readers. Do not bypass locks. Agents sharing live knowledge should use the existing common connection/service rather than competing write-mode MCP instances. Host coordination is optional; no native coordination or protected branch equivalent is assumed.

References: https://docs.ladybugdb.com/client-apis/cli/ ; https://docs.ladybugdb.com/concurrency/ ; https://github.com/LadybugDB/mcp-server-ladybug .
