## 3. One logical record: the representation contract

Every successfully admitted knowledge item has **one common logical knowledge record** under a stable identity. Record the naturally occurring values once and preserve them alongside the original information. The fields provide the data on which structural, relational, lexical and vector methods operate; the SDK MUST NOT require three separately filled position objects. If a value needed by a particular method is unavailable, that method reports the missing value rather than blocking admission, constructing an alternate representation or launching a conversion chain. A single source can contain many items. The natural grain is source-adapter-defined: file, symbol, AST/DOM node, document section, message, event, paragraph, observed relation or qualified finding.

**Minimum UKC/1 logical fields** (not a mandated programming-language struct or physical DB schema):

| Name | Meaning |
|---|---|
| **schema** | Literal version label **ukc/1**. |
| **id** | Version-scoped deterministic knowledge identity (§4), shared by all methods. |
| **source** | Authority/owner namespace, source key, observed version/digest, original route/realm and current-access requirements. |
| **kind** | Honest native item kind. Never force HTML or prose to pretend to be Python AST. |
| **location** | Known source/structural coordinates and verification method, or explicit unknown. Keep all independently verified alternate coordinates. |
| **relations** | Zero or more native observed links/edges and qualified discovered relations (§5). |
| **proximity** | Zero or more space-ID-tagged vectors, with explicit status; lexical/fuzzy candidate access may use source text directly. |
| **values** | All supplied names, titles, typed fields, text, order, attributes, flags and literal facts; do not silently drop fields. |
| **native** | Complete supplied native parse/structure and/or immutable hash-addressed payload, sufficient for exact reconstruction of admitted inputs. |
| **evidence** | Source version, coordinates, original byte/span digests and separately accepted finding/event provenance. |

Use **one shared logical record**, even if runtime performance calls for multiple physical indexes. A graph table row and a vector-index entry referencing the same ID are not independent bodies of knowledge. They are materializations over the record. A consumer can read all known positions without another AI inference or a second import.

### 3.1 What “complete” means

**Entry-point invariance (mandatory):** Given identical source-backed observations, whether an adapter first encounters a node through a title, an AST node, a relationship, or a vector result, it MUST resolve the same canonical knowledge identity and expose the same known common-record values. No entry route may generate a distinct knowledge record or require rebuilding fields through its own retrieval engine. The source-native name, relation, path and numeric value remain individually labeled, with original precision and provenance preserved. **Record once; label deterministically; read through any applicable method.**

Record all values actually available at the input boundary. Never add a title, causal edge, actor, location or meaning not supplied. Missing fields stay unknown. Preserve native path, child order, UTF-8 offsets, explicit attributes and any source-specific field, even if no current search method needs them. An implementation may retain a large native payload in a content-addressed sidecar, but the record must have a verified pointer and portable export must include or resolve that payload. A dangling external payload is not a lossless record.

The SDK does not impose a universal AST schema. A deterministic adapter describes source-native structure; UKC records it.

### 3.2 OKF-compatible interchange

UKC records MUST have a **valid OKF-compatible representation** on export and import. Use upstream-recognized OKF fields correctly, plus a producer-defined **x_ukc** extension for identity, positions, original native values, evidence and optional sidecar references. The source body and its exact bytes must be preserved where available. Unknown YAML keys, native fields and unrelated OKF content must round-trip without being silently discarded.

**OKF is the common translation vocabulary and portable packaging, not a semantic extraction service.** Translating observed parser values to an equivalent OKF field/extension is a copy or deterministic mapping; it does not make an LLM think about their meaning. If a destination representation cannot express a native source value, preserve it losslessly in a native extension or sidecar and report limited direct query support. Do not manufacture equivalent meaning.

An illustrative asset (not a normative upstream OKF schema, and digest placeholders are intentionally not executable fixtures):

~~~yaml
---
type: SourceUnit
title: Example
x_ukc:
  schema: ukc/1
  id: "ukc:v1:<computed-digest>"
  source:
    authority: repo:example
    key: docs/example.md
    version: "sha256:<source-bytes-digest>"
  location:
    status: known
    basis: parser
    path: ["document", "heading[0]"]
    spans: [{unit: utf8-byte, start: 0, end: 10}]
  relations: []
  proximity: [{space: "lexical-hash-512/rust-scanner-v1", status: unknown, vector: null}]
  native: {storage: inline}
  evidence: {source_sha256: "<source-bytes-digest>"}
---
# Example
~~~

A “knowledge graph” with an OKF note containing only a generated summary but not the original supplied structure does not meet this contract.

