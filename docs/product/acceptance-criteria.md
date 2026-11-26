# Acceptance criteria

These criteria verify [`SPEC.md`](../../SPEC.md). The current delivery is the local
synthetic-data prototype. SPECv3's hybrid-MVP requirements are future-target gates, not claims
that the features exist or are authorized today.

## Prototype acceptance criteria

- **Prototype boundary:** The service binds only to loopback. Tests and fixtures use synthetic documents; no real customer, financial, or identity records are accepted as project test data.
- **First slice:** One generated PNG per request; body ≤ 1 MiB; decoded content ≤ 4,000,000 pixels; one frame; nested parser depth 0; request-read timeout 2 seconds. The server cannot verify that caller-provided data is synthetic.
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

## Future-target acceptance gates (SPECv3)

- **REQ-1–4:** Each enabled format has malformed/locked-file error tests. Multi-page and bundle tests prove per-page/per-file failure isolation. The 25 MiB / 20-page defaults, image pixel bound, nested-PDF depth, and per-page timeout are enforced before expensive processing. `document_id`, original-byte SHA-256, and pHash are tested independently; pHash similarity is never itself presented as proof of fraud.
- **REQ-5–8.1:** Synthetic fixtures cover parser failures, stripped metadata for applicable document types, the versioned producer blacklist, profile-specific timestamp deltas, PDF raster-over-text overlays, and font-subset/glyph-width inconsistencies.
- **REQ-9–11:** FFT, JPEG ELA at calibrated Q 90–95, and the selected segmentation model have method/coverage tests. Pages over 1500 px use overlapping 512 px tiles; area thresholds and localization are evaluated on a held-out mask set before heatmaps are described as validated.
- **REQ-12–14:** The pinned OCR model/runtime returns word and character geometry, text, and confidence. Geometry checks are fixture-tested; the `<0.65` rule is applied only to sections meeting the documented `≥150 DPI` condition.
- **REQ-15–16:** Decimal-based ledger arithmetic has exact rounding tests; synthetic ledger heuristics cover duplicate references, round-number clustering, and invalid dates. Identity checksum and format validators have known-valid and known-invalid fixtures and report structured findings.
- **REQ-17–18:** Scorer inputs, artifact version, calibration, cutoff, and circuit-breaker precedence are reproducible and tested. `PASS`/`FLAGGED` remain disabled until separate release approval and held-out gates; no output may trigger credit, lending, onboarding, identity, or KYC decisions.
- **REQ-19–20.1:** HMAC verification/retry limits, authenticated UI/API access, artifact path safety, heatmap expiry, and analyst feedback validation/storage have separate security, privacy, and integration tests. Feedback is not automatically treated as verified ground truth.
- **NFR-1–2, NFR-6:** The three proposed evaluation tiers use licensed, source-disjoint data and establish precision, recall, localization, degradation curves, and ablation results before any performance claim.
- **NFR-3–4:** Profiling on an explicitly supported 4–8 GB laptop GPU and CPU fallback measures p95 GPU latency, five-page PDF latency, CPU latency, peak VRAM/RAM, and bounded worker/queue behavior. Targets are not claimed until measured.
- **NFR-5:** The 24-hour file TTL, encryption, deletion guarantees, crash/backup behavior, and SQLite data fields are explicitly approved and tested before storage is implemented. This is not “zero retention.”
- **NFR-7:** Parser, model, data, profile, and cutoff versions are reproducible and recorded alongside every target analysis before non-inconclusive output.
- **NFR-8:** Before any non-loopback access, tests prove authentication, authorization, TLS, artifact path safety, and tenant isolation if tenancy is in scope; complete security/privacy/legal review.
- Dataset access, rights, label provenance, and any use of non-synthetic evaluation material are approved before acquisition or processing. Research findings alone do not grant those permissions.
- Any transition to real-document handling, persistence, non-inconclusive outcomes, or external access requires separate owner approval and documented privacy/security/legal review.
