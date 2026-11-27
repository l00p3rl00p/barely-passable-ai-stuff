## 4. Identity, exact source positions and deterministic equality

[SDF guide](../SDF/README.md) · Return to [capture reference](../contracts/common-record.md)

For new source-backed UKC/1 records, define a deterministic ID from **(schema, authority, source_key, observed_source_version, native_kind, native_unit_key)**. Exact same normalized inputs must produce exact same identity bytes in every language; no random UUID, database auto-ID or machine-specific temporary checkout path is allowed as a canonical identity.

**Canonical ID bytes profile UKC-ID-1:**
1. Construct the ordered six-element array of UTF-8 strings: **["ukc/1", authority, source_key, source_version, native_kind, unit_key]**.
2. Encode as compact UTF-8 JSON with no spaces, using literal non-ASCII Unicode (rather than optional ASCII escapes), escaping JSON quotes, backslashes and control characters. Adapter normalization of authority/path/unit is an explicitly versioned producer contract; input to ID hashing must be identical across languages.
3. SHA-256 the exact encoded bytes; output **ukc:v1:** followed by 64 lowercase hexadecimal characters.

For already existing historical identities, retain a stable **legacy_id** alias mapping to an unambiguous canonical record. Never silently claim a historical hash was computed by this new scheme. A new source version may produce a new source-versioned ID; retain stable logical-unit aliases and supersession links when available. Do not change unrelated IDs because another file changed.

**Coordinates:** exact UTF-8 byte ranges are zero-based, end-exclusive; all other coordinate systems declare their unit, basis and version. Prefer source-native hierarchy/anchor over guessed line numbers; preserve complementary verified spans. Model-described positions are candidate leads until deterministic reader/source evidence confirms them.

**Resolution:** to read exact original evidence, check access for the present principal, source authority and version, span bounds and content hash. Changed or inaccessible sources return typed failure/lead status, never substitute a new source and claim exact evidence. A locator is not an access grant.

**Hashes:** SHA-256 of original bytes and specific spans is an integrity identity, not semantic understanding. Reuse unchanged work. Source and accepted enrichment hashes must have distinct ownership and update rules when optional lifecycle governance is enabled.

