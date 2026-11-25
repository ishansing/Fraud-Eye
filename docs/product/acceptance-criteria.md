# Acceptance criteria

These criteria verify [`SPEC.md`](../../SPEC.md). The current delivery is the local
synthetic-data prototype. Later-phase criteria are release gates, not claims that the features
exist today.

## Prototype acceptance criteria

- **Prototype boundary:** The service binds only to loopback. Tests and fixtures use synthetic documents; no real customer, financial, or identity records are accepted as project test data.
- **REQ-1:** Each implemented format is documented. Supported synthetic fixtures are accepted; malformed, unsupported, password-locked, and unreadable files return structured error codes.
- **REQ-2:** A request failure is isolated and does not corrupt another request. Multi-page and bundle behavior is deferred and not claimed.
- **REQ-3:** Byte, page, pixel, parser-depth, and time limits are configured and checked before expensive work. Limit failures return bounded, structured errors.
- **REQ-4:** Each accepted synthetic document gets a unique `document_id` and SHA-256 of the original bytes before rasterization or transformation. Source bytes remain unchanged.
- **REQ-5:** Implemented metadata parsers identify their versions and coverage; malformed or unavailable parser results are explicit.
- **REQ-6–8:** Blacklist/timestamp/vector-overlay checks are not claimed until implemented and covered with synthetic fixtures.
- **REQ-9–11:** FFT, ELA, and pixel segmentation/heatmaps are deferred; the prototype does not claim those signals.
- **REQ-12–16:** OCR/layout, font checks, ledger invariants, and identity checksum rules are added only with corresponding synthetic fixtures and explicit supported document types.
- **REQ-17:** Unvalidated score fields are `null`; no numeric score is invented.
- **REQ-18:** Every successful prototype analysis returns `INCONCLUSIVE`. It never returns `PASS` or `FLAGGED` before an approved profile passes its release gates.
- **REQ-19–20:** Webhooks, review console, and heatmap retrieval are deferred from the prototype.
- **API response:** Includes a unique ID, original-byte digest, processing duration, typed findings, `INCONCLUSIVE`, and null unvalidated scores/heatmap fields. Errors have a stable machine-readable reason.
- **NFR-5:** Source bytes, extracted document content, and derived artifacts are not written to disk or external services; in-memory data is released at request completion.
- **NFR-8:** The API binds to loopback only. No public listener, webhook, or heatmap download route exists.

## Later-phase requirements

- **NFR-1–2:** Held-out evaluation measures precision and recall on the named target population; the proposed 96% precision and 93% recall targets pass before production claims.
- **NFR-3–4:** Load tests on the approved deployment verify the proposed ≤2 seconds/page and 50/300 RPS targets.
- **NFR-6:** Training, calibration, and held-out data are source-disjoint and cover the target documents and transformations.
- **NFR-7:** Model, parser, policy, profile, and threshold versions are reproducible and recorded.
- **NFR-8:** Before external access, TLS, authentication, authorization, tenant isolation, privacy review, and security review are verified.
- **REQ-19–20:** Webhook signing/retry behavior and analyst review/heatmap behavior have their own integration and access-control tests.
- `PASS`/`FLAGGED` remain screening signals only; they do not approve or reject credit, lending, onboarding, identity, or KYC applications.
- Any transition to real-document handling or persistence requires owner approval and documented privacy/security/legal review.
