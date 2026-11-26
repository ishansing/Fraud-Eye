# ISSUE-008: Local synthetic PNG screening endpoint

**GitHub issue:** [#2](https://github.com/ishansing/Fraud-Eye/issues/2)  
**Normative scope:** [`SPEC.md`](../../SPEC.md), [`architecture.md`](../architecture/architecture.md), and [ADR 0004](../architecture/ADR/0004-loopback-png-prototype.md)

## Objective

Implement the first runnable, loopback-only, memory-only API slice for one generated synthetic PNG.

## Requirements

- `SPEC.md` REQ-1–REQ-4, REQ-17–REQ-18, NFR-5, NFR-8

## Acceptance criteria

- `python -m fraud_netra` binds only to `127.0.0.1`.
- `POST /v1/documents/analyze` accepts multipart fields `file` (one PNG) and `document_type`.
- `GET /healthz` returns a minimal health status.
- Requests over 1 MiB, malformed multipart, unsupported/corrupt PNG, multi-frame content, and images over 4,000,000 pixels fail with bounded structured errors.
- Request reads have a 2-second timeout; no PDF/archive/nested parser is enabled (depth 0).
- Successful responses include a unique `document_id`, SHA-256 of original bytes, duration, `INCONCLUSIVE`, reason, null unvalidated scores, empty anomalies, and null heatmap.
- No source bytes or extracted content are persisted, logged, or sent to an external service.
- Tests call the HTTP endpoint with generated fixtures and verify success, errors, bounds, and loopback-only startup configuration.

## Relevant files

- `src/fraud_netra/`
- `tests/test_api.py`
- `README.md`, `SPEC.md`, and `docs/product/acceptance-criteria.md`

## Dependencies

- [ISSUE-007 architecture](../architecture/architecture.md)
- Existing Python and Pillow dependencies

## Out of scope

Real documents, other formats, metadata/forensic analysis, OCR, scoring, `PASS`/`FLAGGED`, webhooks, UI, persistence, authentication, or public deployment.

## Validation

- `./.venv/bin/python -m pytest -q`
- `./.venv/bin/ruff check src/fraud_netra tests/test_api.py`
- Pass when both commands exit 0 and the tests exercise the public HTTP seam.

## Documentation impact

- `README.md`: startup command, supported fixture, and synthetic-only warning.
- `SPEC.md` and `docs/product/acceptance-criteria.md`: mark the first supported format and limits.

## Merge gate

Tests and lint pass; review confirms fixed loopback binding, strict byte/pixel limits, and no input persistence.
