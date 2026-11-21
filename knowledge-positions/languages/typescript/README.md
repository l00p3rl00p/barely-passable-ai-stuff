# TypeScript SDK — contract entry point

No existing UKC TypeScript SDK library was verified in the inspected Knowledge Positions repository. This folder is the **designated language location**, not an installable NPM package or a claim of implemented bindings.

A TypeScript consumer should follow the same [common UKC record](../../contracts/common-record.md), [public operations](../../contracts/public-operations.md), [canonical identity profile](../../core/identity.md), and [shared conformance tests](../../conformance/requirements.md), using language-idiomatic types and errors.

There is no mandatory server, protocol, transpiler, runtime or secondary database. A future TypeScript binding must connect to an **existing, explicitly supported execution boundary** and advertise only real capabilities; it must not synthesize successful replies or silently implement a competing interpretation of knowledge.

See the [capability map](../../docs/component-and-capability-map.md). Nothing in this directory installs a runtime.
