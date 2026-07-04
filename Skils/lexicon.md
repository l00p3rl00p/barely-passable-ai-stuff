<!-- EXPLAINER:PROTECT_DOC (do not delete/overwrite; safe to exclude from bulk cleanup/scripts) -->

# Lexicon of Integrity — 

> **Source of Truth**: `USER_OUTCOMES.md` (Constitutional)

This lexicon defines the canonical terminology used to describe system states, failure modes, and governance principles. All agents and automated tools must adhere to these definitions to maintain "Semantic Alignment."

## 🚫 Failure Signals (Lexicon)

### Green Lies
- **Definition**: Technical tests pass but Operational Reality (ORT) fails (Workflow Mismatch).
- **Symptom**: The code runs, but the human cannot use it for the intended outcome.

### Red Lies
- **Definition**: Infrastructure reports `isError: true` for a valid logic verification attempt (Handshake Drift).
- **Symptom**: A tool call fails technically (e.g., V8 isolate crash) even if the logic it was testing would have passed.

### Ghost Code
- **Definition**: Features that exist in source code (L5) but have no corresponding Build Contract (L3) or Evidence (L6).
- **Resolution**: Trigger a retroactive build to generate missing contract + evidence.

### Silent Discards
- **Definition**: Features dropped during refactoring without a "Four-Team Review" decision log.

### Silent Reframing
- **Definition**: Changing task context or narrative without explicit user notification.
- **Severity**: Terminal failure during preservation/verbatim orders.

### Implicit Reinterpretation
- **Definition**: Quietly altering requirement meanings based on machine preference.
- **Severity**: Violation of CORE MISSION.

### Scope Mutation
- **Definition**: Gradual, undocumented expansion/contraction of work boundaries.
- **Severity**: Violation of Rule of One intent.

### Drift via Summary
- **Definition**: Loss of detail or intent during distillation.
- **Severity**: Terminal failure during Word-for-Word requests.

### Path Leakage
- **Definition**: Presence of literal `/Users/name/` strings in shared documentation or logs.
- **Mitigation**: Automated Path Masking (v1.3.0+).

---

## 🏗️ Operational States

### SOFTWARE START
- **Definition**: The minimal shippable foundation including Q1 Front Door and Q2 Doctor.

### OPERATIONAL REALITY (ORT)
- **Definition**: Proving a real user workflow works end-to-end (UI intent -> backend contract -> runtime effect -> evidence usability).
