# ADR 0004: Loopback PNG prototype

- **Status:** Accepted
- **Date:** 2026-11-26

## Context

The first runnable Fraud Netra slice must accept a generated fixture, stay local and in-memory,
and always return `INCONCLUSIVE`. A broad document parser or web framework would add dependencies
and attack surface before the prototype has a validated screening profile.

## Decision

Use Python's standard library HTTP server bound directly to `127.0.0.1`, with a multipart
`POST /v1/documents/analyze` endpoint accepting one PNG and a `document_type`. Use the existing
Pillow dependency to validate/decode PNG bytes. Cap the request at 1 MiB, the image at one frame
and 4,000,000 pixels, nested parser depth at 0 (no nested-document parser), and request reads at
2 seconds. Return the original-byte SHA-256 and an `INCONCLUSIVE` result with null unvalidated
scores. Do not persist bytes, log submitted content, spawn subprocesses, or access the network.

## Consequences

- The first slice has a small dependency and runtime surface, with a real HTTP test seam.
- Only synthetic PNG fixtures are supported; PDF, JPEG, TIFF, metadata analysis, and forensic
  conclusions remain unsupported.
- The service is not safe for public exposure, multi-user operation, or real documents.
- The socket timeout bounds slow request reads, not a hard CPU-processing deadline.
