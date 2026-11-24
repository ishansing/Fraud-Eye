# Project decisions

Source: alignment of `PRD.md`, `SPEC.md`, and `docs/product/research.md` on 2026-11-24.

## Facts

- V1 is a local CLI for one to five explicit JPEG/PNG inputs; it must not make fraud, event-truth, legitimacy, or legal-authenticity judgments (`PRD.md` §§3, 5; `SPEC.md` §§2, 4).
- Non-experimental `likely` outputs require the specified held-out performance gates; unsupported results must remain experimental or inconclusive (`SPEC.md` NFR-5).
- Research identifies Python, Pillow, ExifTool, C2PA SDK, and ONNX Runtime as candidates only; none has been adopted (`docs/product/research.md`).

## Decisions

- **Runtime/deployment:** Use Python for a single-user local CLI. V1 has no daemon, network service, or authentication layer.
- **Verdict gating:** Generation/edit verdicts are non-experimental only for task/domain profiles that pass the applicable documented release gates. Until then, report experimental or inconclusive outcomes; do not promise model-backed classifications without evidence.
- **Evaluation scope:** Define a narrow, explicit target population and documented reference corpus for v1. Report cases outside the validated scope as experimental or inconclusive rather than implying broad generality.
- **Performance gates:** Retain the initial targets provisionally: at least 80% sensitivity at no more than 5% false-positive rate on the required held-out slices; require ECE ≤0.05 on an independent named population before using calibrated-likelihood language. Revisit only with feasibility evidence.
- **Metadata parser evaluation:** Evaluate ExifTool first for broad metadata extraction using an allowlisted invocation with bounded time/output and representative plus adversarial fixtures. This is an evaluation direction, not a final dependency selection.
- **Untrusted input processing:** Treat selected images and embedded metadata as hostile. Apply byte/pixel/time bounds, isolate per-image failures, and test execution with outbound networking denied. Use a bounded subprocess for ExifTool if it passes evaluation; subprocess separation is not itself a sandbox.
- **Threat-model context:** V1 is manually operated by one local user; inputs may be hostile. No remote service, shared multi-user processing, or attacker control of installed software/model artifacts is in scope.
- **Resource planning:** Specify a modest reference machine and measurable time/memory budgets for single-image and five-image scans before selecting detector models.

## Open questions

- Which concrete population, corpus release, label provenance, and split design will define the v1 evaluation domain?
- Which reference hardware and numerical per-image/batch time and memory limits are supportable?
- Which generation/edit models, runtimes, versions, and licenses pass feasibility and evaluation?
- Does ExifTool meet parser coverage, safety, and packaging needs on representative/adversarial JPEG and PNG fixtures?
- Which parser, decoder, and C2PA SDK versions and configurations meet offline and resource-bound requirements?

These open implementation choices are deferred to research/architecture and feasibility work; they do not authorize broad claims or bypass the release gates.
