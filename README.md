# Fraud Netra

Fraud Netra is a document-screening project for Lending, Underwriting, and KYC review
workflows. The approved current target is a **local-only prototype using synthetic documents**.

## Current status

The prototype scope from `SPECv2.md` has been reconciled into `PRD.md`, `SPEC.md`, and the
acceptance criteria. Architecture and implementation have not yet started for Fraud Netra. The
code currently in `src/` is the earlier Image Evidence Scanner CLI;
it is not a Fraud Netra API and must not be used to process real customer documents.

## Local prototype

The first prototype endpoint accepts only one project-generated synthetic PNG per request.
It binds to `127.0.0.1:8000`, keeps request data in memory, and always returns `INCONCLUSIVE`;
it does not determine whether an input is synthetic or make a lending, identity, or KYC decision.
Never submit real or sensitive documents.

Run with `python -m fraud_netra` after installing the project dependencies. The
`POST /v1/documents/analyze` endpoint expects multipart fields `file` (PNG) and `document_type`.
Requests are limited to 1 MiB and decoded images to 4,000,000 pixels.

## Prototype boundary

- Local REST API bound to loopback only.
- Synthetic fixtures only; no real identity, financial, or customer records.
- In-memory request processing; no document or artifact persistence.
- Successful prototype analyses return `INCONCLUSIVE`; unvalidated scores remain null.
- Screening evidence is not a credit, lending, onboarding, identity, or KYC decision.
- Webhooks, review console, heatmap URLs, public hosting, and GPU deployment are deferred.

See [`PRD.md`](PRD.md), [`SPEC.md`](SPEC.md), and
[`docs/product/acceptance-criteria.md`](docs/product/acceptance-criteria.md) for the current
scope and project trajectory. Work status is tracked in
[GitHub Issues](https://github.com/ishansing/Fraud-Eye/issues).
