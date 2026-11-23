---
type: Research Section
title: '15. Execution-boundary capture: persistence cannot be an optional thought
  [EKC:28]'
description: Records that the agent bypassed optional persistence and proposes capturing
  source events at the host execution boundary.
tags:
- runtime-hooks
- durable-capture
- optional-tool-bypass
status: draft
sources:
- id: manuscript
  resource: ../../fixture/paper.md
  title: Original research manuscript
source_ref: paper.md#EKC:28
source_span:
  start_byte: 783
  end_byte: 2248
  unit: utf8_byte
source_content_sha256: f7549a4645915a2e6333d01c3360e05bf4fb40fcbdc1c3a83a228919f4b90f6a
knowledge_annotation_sha256: e53ad77af994b58515e99a25d15e1d4b3e3edf70b7213321c68dbda15097bc48
ast_ref: ../ast/EKC-28.json
x_jit_location:
  owner_namespace: null
  realm: local_file
  source_id: paper.md#EKC:28
  source_version_sha256: f7549a4645915a2e6333d01c3360e05bf4fb40fcbdc1c3a83a228919f4b90f6a
  version_scope: section
  position:
    start_byte: 783
    end_byte: 2248
    unit: utf8_byte
    span_sha256: f7549a4645915a2e6333d01c3360e05bf4fb40fcbdc1c3a83a228919f4b90f6a
    precision: verified_utf8_span
  possible_routes:
  - environment: python_process
    via: filesystem
  last_resolution: observed_read
---

# Summary

Records that the agent bypassed optional persistence and proposes capturing source events at the host execution boundary.

## Annotated paragraphs

- **paper.md#EKC:28/ast/paragraph_open/19285d1e331cea577687/1**: Documentation cannot alone guarantee the capture path will run. (tags: enforcement, prompt-limitations; source hash: `19285d1e331cea57`)

  - `related_to` → [EKC:27](./EKC-27.md): The paragraph contrasts optional instructions with the persistent starting procedure.
## Relationships

- `related_to` → [EKC:27](./EKC-27.md): The operational capture boundary elaborates the separate runtime responsibilities described in Section 14.
