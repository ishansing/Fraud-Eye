# ISSUE-007: Design the Fraud Netra local prototype architecture

**GitHub issue:** [#2](https://github.com/ishansing/Fraud-Eye/issues/2)  
**Normative scope:** [`SPEC.md`](../../SPEC.md) and [`docs/product/decisions.md`](../product/decisions.md)

## Objective

Replace the historical image-scanner architecture with a testable design for the owner-approved
local, synthetic-data, in-memory REST API prototype.

## Requirements

- `SPEC.md` REQ-1–REQ-5, REQ-17–REQ-20, NFR-5, NFR-8

## Acceptance criteria

- The architecture defines the local API entrypoint, request/response contract, module interfaces,
  and test seam for one synthetic document per request.
- The service is loopback-only and documents the operator constraint that only generated
  synthetic fixtures may be submitted; it does not claim to detect whether arbitrary uploads
  contain real data.
- Request byte, page, pixel, parser-depth, and processing-time limits have explicit prototype
  values before implementation.
- Request bytes, extracted content, and derived artifacts remain in memory; tests are planned to
  detect any disk or network use in the request path.
- Successful analyses return `INCONCLUSIVE`, a reason, and null unvalidated scores. No model,
  webhook, heatmap URL, UI, or consequential decision is enabled.
- A new threat model covers hostile uploads, local callers, parser resource exhaustion, and
  accidental retention/exposure. The old CLI threat model is labeled historical.
- The design distinguishes prototype scope from future external hosting, real-document
  processing, tenant isolation, retention, webhooks, and review-console decisions.

## Dependencies

- Owner-aligned decisions in `docs/product/decisions.md`
- Normative prototype scope in `SPEC.md`

## Status

Architecture decisions are recorded in [`architecture.md`](../architecture/architecture.md)
and [ADR 0004](../architecture/ADR/0004-loopback-png-prototype.md). Implementation is tracked
separately in [ISSUE-008](ISSUE-008.md).

## Out of scope

- Selecting forensic models or processing real customer documents.
- Public deployment, webhooks, review UI, GPU/Kubernetes infrastructure, and 24-hour retention.

## Validation

Review architecture and threat-model artifacts against every acceptance criterion and the cited
requirement IDs before creating the implementation slice.
