# Project decisions

Source: owner alignment on 2026-11-26, based on `SPECv2.md`.

## Facts

- `SPECv2.md` proposes the document-screening product now named Fraud Netra for Lending, Underwriting, and KYC operations via API, webhooks, and a review console.
- The supplied specification used the working title DocShield Forensics; the canonical project name is Fraud Netra.
- The prior project was an offline image CLI. Its PRD, implementation, acceptance criteria, threat model, and architecture do not describe Fraud Netra.
- The provided specification includes support for PDF/JPEG/PNG/TIFF, multi-page processing, financial/identity signals, a numeric score, binary verdicts, and visual overlays.

## Decisions

- **Product direction:** Replace Image Evidence Scanner with Fraud Netra. `SPECv2.md` is the new product input; canonical documents use the owner-selected name and prototype scope.
- **Prototype data:** Use synthetic documents only. Do not upload or process real identity, financial, or customer documents in this prototype.
- **Prototype deployment:** Begin with a local-only REST API vertical slice and bounded in-memory processing. No public endpoint or production tenant.
- **Retention:** Do not persist uploaded documents or generated artifacts in the prototype; process them in memory for the request lifetime.
- **Screening boundary:** Results are screening signals only. Do not make or trigger credit, lending, onboarding, or KYC decisions.
- **Verdict gate:** Until the applicable evaluation gates pass, return `INCONCLUSIVE`; enable `PASS`/`FLAGGED` only for an approved profile that meets the gates.
- **Heatmaps:** Defer heatmap generation and URLs in the first prototype. Revisit access and lifetime when designing the review-console flow for memory-only processing.
- **Phasing:** The first slice is a local API using synthetic fixtures. Defer webhook delivery, review console, Kubernetes/GPU deployment, and real-document handling until the core flow and privacy/security design are validated.
- **First format:** Begin with one PNG fixture per request; do not enable PDF, JPEG, or TIFF parsing yet.
- **Local API:** Use the Python standard library HTTP server, bound to `127.0.0.1` only. No authentication is added for this loopback-only prototype.
- **Prototype bounds:** Request body ≤ 1 MiB, one PNG page, ≤ 4,000,000 decoded pixels, no nested-document parser (depth 0), and a 2-second socket/request-read timeout. Processing is limited to bounded PNG decoding and metadata-free response generation.
- **Release evidence:** Treat the provided precision, recall, latency, and throughput numbers as release gates to measure, not established performance claims.

## Open questions

- Which local API framework and PDF/image parsing libraries fit the bounded prototype?
- Which first document type and synthetic fixture format will provide the smallest useful end-to-end slice?
- What byte, page, pixel, and timeout limits should the prototype enforce?
- What scoring/evidence can be emitted without implying model validation, and how will the eventual profile be evaluated against the stated release gates?
- What security, privacy, hosting, tenant, retention, and legal review is required before any real-document or externally reachable deployment?
- How should later webhook and review-console access work without persistent document or heatmap storage?

These decisions authorize a synthetic-data prototype only. They do not authorize production hosting, real customer data, model claims, or consequential decisions.
