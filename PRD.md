# Product Requirements Document

## DocShield Forensics

| Field | Value |
| --- | --- |
| Status | Approved local synthetic-data prototype scope; not yet implemented |
| Version | 1.0.0-MVP |
| Updated | 2026-11-26 |
| Normative requirements | [SPEC.md](SPEC.md), based on [SPECv2.md](SPECv2.md) |
| Acceptance criteria | [Acceptance criteria](docs/product/acceptance-criteria.md) |
| Decisions | [Project decisions](docs/product/decisions.md) |

## 1. Product outcome

DocShield Forensics is a document-screening system for Lending, Underwriting, and KYC operations. Its long-term target accepts financial and identity documents, collects metadata, image, OCR/layout, and deterministic financial/identity signals, and presents findings for human review.

The current project deliverable is deliberately narrower: a local-only REST API prototype exercised with synthetic documents. It demonstrates safe ingestion, document identity, bounded parsing, and a structured screening response without handling real customer data or claiming validated detection performance.

## 2. Users and goals

### Target users

- **Risk analyst:** Reviews document findings and decides whether more investigation is needed.
- **KYC/compliance officer:** Uses screening signals as one input to a human-controlled review process.
- **Platform engineer:** Integrates the future analysis API.

### Product goals

1. Accept supported document formats through a clear, bounded API.
2. Preserve source identity with a SHA-256 digest computed before transformations.
3. Extract explainable metadata, visual, OCR/layout, and deterministic logic findings as those layers are validated.
4. Keep synthetic/test inputs and derived content in memory for the prototype request lifetime.
5. Return `INCONCLUSIVE` until a task/profile has evidence to support a stronger screening signal.
6. Make findings useful for human review without deciding credit, lending, identity, or KYC outcomes.

## 3. Current prototype scope

- Local-only REST API bound to loopback.
- Synthetic document fixtures only; no real identity, financial, or customer records.
- One synchronous document-analysis request at a time for the first vertical slice.
- Bounded, in-memory request handling; no persisted source documents, extracted content, or derived artifacts.
- Structured response with document ID, source digest, processing time, typed findings, and `INCONCLUSIVE` verdict.
- Score fields remain null unless a validated profile gives them defined, evaluated meaning.
- Unsupported, malformed, or over-limit inputs return structured errors.

## 4. Product vision beyond the prototype

The broader product target includes multi-page PDF/TIFF and image inputs, four forensic layers, per-document screening scores, gated `PASS`/`FLAGGED` signals, authenticated integrations, and a human review console. These features require separate architecture, privacy/security decisions, representative evaluation data, and release evidence. They are not implied by the prototype’s completion.

The initial product proposal names target KPIs of at least 96% precision on tampered documents, at least 93% recall on synthetic/AI documents, at most 2 seconds per page, and 50 base / 300 peak requests per second. These are unverified release targets, not current performance claims.

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

1. Reconcile this PRD, `SPEC.md`, and acceptance criteria with the owner-approved prototype scope.
2. Redesign architecture and threat model for a local in-memory API handling synthetic fixtures.
3. Implement the smallest end-to-end ingestion and response slice.
4. Add deterministic metadata and document-logic findings with synthetic tests.
5. Evaluate OCR/vision candidates and data rights before model-backed results.
6. Revisit webhooks, review UI, external hosting, retention, and real-document handling only after security/privacy review and owner approval.
