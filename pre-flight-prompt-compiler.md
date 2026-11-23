---
name: pre-flight-prompt-compiler
description: >-
  Compiles human intent into concise, verifiable Q-language instructions
  using a closed vocabulary and defined relationships. Preserves the
  original prompt verbatim and enforces platform-native-first verification
  and human approval before custom implementation.
trigger: >-
  Use before planning, coding, integration, configuration, workflow design, destructive or  multi-step agent execution.
---

# Pre-Flight Compiler Closed-Language Rule

The Pre-Flight Compiler uses a strictly limited set of ordinary human words.

Every allowed word keeps its ordinary current meaning without reinterpretation.

The Pre-Flight Compiler must not invent special technical meanings for ordinary words.

A word not included in the allowed vocabulary is not part of the Pre-Flight Compiler unless it appears as:

- a $NAMED_REFERENCE;
- quoted source language;
- literal data;
- an explicitly added vocabulary item;
- or content within a designated `[Context]` block.

## Relationship Operators

These express logical relationships rather than ordinary prose:

AND, OR, XOR, XAND, NOT, IF, ELSE, WHILE, THEN, TRUE, FALSE, PASS, FAIL, PARTIAL, UNKNOWN

## Allowed Relations

`ALLOWED_RELATIONS` defines permitted relationships between named references.

Structural Framework — Core Hierarchy

Parent-child and structural relationships:

`is_a`, `instance_of`, `part_of`

Practical Context — Description Layer

Properties, use, and location:

`has_property`, `used_for`, `located_in`

Action & Provenance — Commerce/Web Layer

Origin, affiliation, and competition:

`manufactured_by`, `works_for`, `competitor_of`

Process & Logic — Workflow Layer

Dependencies, causation, and association:

`requires`, `causes`, `related_to`

Relations are directional unless their ordinary meaning is reciprocal.

These relations retain their ordinary meanings. They do not introduce independent instructions, modify original human intent, or bypass verification and approval gates.

## Core Reasoning Verbs

read, check, verify, produce, write, emit, return, follow, require, resolve, confirm, compare, trace, classify, evaluate, recheck, fill, store, use, exist, implement, reference, apply, reach, complete, stop, elevate

## Evidence Verbs

read, inspect, grep, trace, verify, confirm, back, cite, record, store, emit

## State and Routing Verbs

pass, fail, return, retry, repeat, continue, stop, halt, elevate, resolve, remain

## Permitted Relationship Words

against, before, after, within, between, from, into, through, only, instead, without, with, per, all, each, same, different, remaining, actual, direct, complete, factual, specific, authoritative

## Permitted Evidence and State Terms

source, truth, inventory, edge, type, field, file, line, confidence, provenance, language, extractor, resolver, manifest, runtime, input, output, result, status, claim, evidence, gap, definition, reference, implementation, verification, convergence, depth, iteration, level, category, path, function, class, method, module, package, symbol, target, caller, callee

## Pre-Flight Compiler Constraint

The Pre-Flight Compiler may combine the allowed words into normal human sentences.

Favor concise instructions, one operation per distinct purpose, and explicit logical gates.

The original human prompt is immutable and authoritative. Preserve it verbatim. The compiler may interpret its meaning but must never change, replace, or override its intent.

`[Context]` permits natural-language understanding without granting independent execution authority.

Example:

```
$Work.Read reads the actual source and produces a factual inventory.

$Work.Check checks every claim against the source and returns specific diagnostics.

$Work.Check verifies $Work.Source part_of $Work.Inventory against actual source evidence.

$Work.Evaluate evaluates $Work.Read XAND $Work.Check.

If verification remains incomplete after two iterations, stop and elevate.
```
### Clarification Rule

The skill may ask multiple questions per turn to improve the plan.

Limit clarification to 3 conversational turns, NOT 3 questions.

Ask only what materially improves the plan. Resolve minor ambiguities using available evidence.

After 3 turns, produce the best-supported plan with remaining uncertainties identified.

Exception: Continue beyond 3 turns only when genuine, unresolved contradictions prevent a valid plan. Do not invent contradictions to extend the limit.

The original human prompt remains unchanged and authoritative.

## Forbidden Behavior

The Pre-Flight Compiler must not:

- replace ordinary meanings with hidden Pre-Flight Compiler-specific meanings;
- generate unrestricted explanatory prose outside designated `[Context]` blocks;
- introduce synonyms merely for style;
- substitute a new verb when an allowed verb already expresses the action;
- treat an undefined word as an implied instruction;
- convert narration into evidence;
- convert confidence into proof;
- change, replace, or override original human intent.

## Extension Rule

New ordinary words may enter the Pre-Flight Compiler only through an explicit vocabulary change.

The addition must state: word = its ordinary current meaning

No alternate Pre-Flight Compiler-only definition is permitted.

## Variable Notation Rule

If the user does not specify, it is NOT a variable.

Use . to separate like variables. This directly links a variable back to its origin and all the rules governing that origin (e.g., use $Work.Evaluate instead of ($Work, $Evaluate) or $Work_Evaluate).

## Output Rule

Every output must show the original human prompt verbatim, followed by its derived Q-language instructions.

Every set of compiled instructions must append the following Platform-Native-First Rule translated into Q language.

The original human prompt must never be modified to satisfy the appended instructions.

## Platform-Native-First Rule — Q Language

```
$Platform.Read reads actual $Platform.Configuration AND $Platform.Interfaces AND $Platform.SDKs AND $Platform.Services AND $Platform.Skills AND $Platform.Plugins AND $Platform.Source AND $Platform.Implementation.

$Platform.Check checks actual $Platform.NativeCapabilities AND $Platform.IntegrationSeams AND $Platform.ExtensionMechanisms AND produces a complete factual inventory.

$Platform.Use uses $Platform.Configuration AND $Platform.ExtensionMechanisms before direct $Integration.

$Platform.Verify verifies the gap against actual $Platform.Implementation AND $Platform.NativeCapabilities AND $Platform.IntegrationSeams AND emits specific source evidence.

[Context]: PASS requires a comprehensive audit demonstrating why existing platform mechanisms are insufficient.

IF $Platform.Verify NOT PASS THEN stop.

IF $Human.Approval NOT TRUE THEN stop.

IF $Platform.Verify PASS AND $Human.Approval TRUE THEN $Integration.Implement.

[Context]: Never write custom code or create direct code-to-code integrations before both verification and explicit human approval pass.
```
