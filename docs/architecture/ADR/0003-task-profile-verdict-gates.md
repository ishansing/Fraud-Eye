# ADR 0003: Task profiles and gated verdicts

- **Status:** Accepted
- **Date:** 2026-11-24

## Context

Generation and editing are distinct tasks with separate thresholds and validation domains. No concrete models or reference dataset have been selected or validated.

## Decision

Represent generation and editing as separate task assessments. The report composition layer combines only task decisions from the active, versioned local profile and applies the SPEC verdict rules. No model plugin framework or cross-model universal score is introduced. Until a task/domain profile passes its held-out gate, its result remains experimental or inconclusive.

Exact model formats, inference runtime, calibration data, thresholds, and reference corpus are deferred to feasibility and architecture follow-up.

## Consequences

- The task-result contract and verdict rules can be tested independently of model accuracy.
- A model adapter or ONNX Runtime dependency is not selected until candidate models pass license, safety, hardware, and evaluation checks.
- Reports must retain raw score semantics and profile/version provenance.

## Evidence

- `SPEC.md` REQ-11–REQ-15 and NFR-1–NFR-5.
- `docs/product/decisions.md` records the release-gating decision and unresolved model/data choices.
