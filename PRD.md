# Product Requirements Document

## Fraud Netra

| Field | Value |
| --- | --- |
| Status | Long-term target adopted; current implementation remains safety-gated |
| Version | 1.1.0-Hybrid-MVP target |
| Updated | 2026-11-26 |
| Normative requirements | [SPEC.md](SPEC.md), adapted from [SPECv3.md](SPECv3.md) |
| Acceptance criteria | [Acceptance criteria](docs/product/acceptance-criteria.md) |
| Decisions | [Project decisions](docs/product/decisions.md) |

## 1. Product outcome

Fraud Netra's long-term target is a single-node document-screening system for Lending, Underwriting, and KYC review. The adopted target proposes four forensic layers, a calibrated score, profile-gated screening signals, analyst review, and a local modular-monolith deployment. These are target capabilities, not implemented or validated results.

The current deliverable remains deliberately narrower: a loopback-only REST API prototype exercised with generated synthetic PNG fixtures. It validates a bounded image, returns its digest, and reports `INCONCLUSIVE`; it does not perform forensics or claim validated detection performance.

## 2. Users and goals

### Target users

- **Risk analyst:** Reviews document findings and decides whether more investigation is needed.
- **KYC/compliance officer:** Uses screening signals as one input to a human-controlled review process.
- **Platform engineer:** Integrates the future analysis API.

### Product goals

1. Accept supported document formats through a clear, bounded API.
2. Preserve source identity with a SHA-256 digest computed before transformations.
3. Extract explainable metadata, visual, OCR/layout, and deterministic logic findings as those layers are validated.
4. Keep synthetic/test inputs and derived content in memory for the current prototype request lifetime.
5. Return `INCONCLUSIVE` until a task/profile has passed its evaluation and release gates.
6. Make findings useful for human review; never make or trigger credit, lending, onboarding, identity, or KYC decisions.

## 3. Current prototype scope

- Local-only REST API bound to loopback.
- Synthetic document fixtures only; no real identity, financial, or customer records.
- One synchronous document-analysis request at a time for the first vertical slice.
- Bounded, in-memory request handling; no persisted source documents, extracted content, or derived artifacts.
- Structured response with document ID, source digest, processing time, typed findings, and `INCONCLUSIVE` verdict.
- Score fields remain null unless a validated profile gives them defined, evaluated meaning.
- Unsupported, malformed, or over-limit inputs return structured errors.

## 4. Product vision beyond the prototype

The adopted v1.1 target (see `SPECv3.md`) proposes PDF/JPEG/PNG/TIFF ingestion, multi-page processing, metadata/font and vision forensics, ONNX OCR, deterministic/statistical checks, model-based scoring, analyst feedback, webhooks, a review UI, and local persistence. None is part of the current runtime. Real-document handling, persistence, authenticated remote access, and any non-`INCONCLUSIVE` profile require separate owner approval, architecture, privacy/security/legal review, and representative evaluation evidence.

SPECv3 proposes at least 96% precision with Doc-AUC/Region-F1 tracking, at least 93% recall, GPU latency at or below 1 second per page, CPU fallback latency at or below 3.5 seconds per page, at or below 4.5 seconds for a 5-page PDF, peak VRAM at or below 3.5 GB, and peak RAM at or below 4.5 GB. These are unverified targets, not current performance claims; the target does not retain the earlier 50/300 RPS objective.

## 5. Boundaries and safeguards

- The prototype does not accept real customer documents and is not reachable from external networks.
- Findings are screening evidence, not proof that a document is authentic, fraudulent, or false.
- The system does not approve or reject credit, lending, onboarding, identity, or KYC applications.
- The prototype does not persist documents or expose heatmap URLs.
- Webhooks, review console, multi-tenant service, Kubernetes, GPU inference, and production deployment are deferred.
- Any use with real documents, external access, persistent storage, or consequential workflows requires owner approval plus privacy, security, and legal review.

## 6. Success measures

The prototype succeeds when the local API accepts its documented synthetic fixtures, rejects invalid or over-limit input cleanly, preserves the original digest, emits a valid structured `INCONCLUSIVE` response, and demonstrably avoids persistence and external access.

Production readiness is a separate milestone requiring held-out evaluation, the specified KPI gates, load tests, security/privacy verification, and approval of the deployment and data-handling design.

## 7. Trajectory

1. Keep the current synthetic-only API as the safe development baseline.
2. Break the v1.1 target into independently testable slices; resolve the retention, authentication, evaluation-data, and resource-budget gaps first.
3. Build metadata/container and deterministic logic layers using synthetic fixtures only.
4. Evaluate OCR/vision candidates, dataset licenses, and model validity before emitting model-based signals.
5. Design the target modular monolith, local auth, SQLite audit data, and ephemeral storage only after architecture and threat-model review.
6. Enable real documents or stronger screening signals only after separate approval and the applicable security, privacy, legal, and evaluation gates.
