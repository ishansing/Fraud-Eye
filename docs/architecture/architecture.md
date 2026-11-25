# Image Evidence Scanner architecture

**Historical:** This architecture describes the superseded offline image CLI. It does not apply
to DocShield; a new local API architecture is the next lifecycle phase.

**Status:** The initial architecture has been implemented through ISSUE-005; model-backed
classification remains gated on the decisions recorded in `.itp/run.md`.

## System shape

An offline Python CLI accepts explicit paths, processes each image sequentially, and renders a concise terminal result plus an optional versioned JSON report. ExifTool and C2PA validation run in bounded child processes. No server, upload surface, database, cloud inference, or scan-time download exists in v1.

```text
src/image_evidence_scanner/
  cli.py                 argument parsing, exit status, top-level orchestration
  scan.py                per-file lifecycle and failure isolation
  image_input.py         bounded read, digest, decode, image facts, pixel signals, file structure
  metadata.py            bounded ExifTool invocation, JSON size/depth checks, parser coverage
  provenance.py          bounded C2PA worker orchestration
  c2pa_worker.py         offline C2PA validation in a killable child process
  assessment.py          task result validation and verdict/advisory rules
  report.py              text and versioned JSON rendering
  output.py              safe atomic report writing
tests/
  unit and integration tests, with adversarial fixtures kept small and local
```

Keep modules private to the package until callers require otherwise. Avoid a generic plugin system: the selected model and parser stack have not been validated. Define only the small internal records needed to pass observations, task outcomes, and failures between modules; preserve unknown values and parser errors rather than collapsing them to empty data.

## Module responsibilities and seams

| Module | Interface responsibility | Requirements |
|---|---|---|
| CLI / scan orchestration | Validate 1–5 explicit arguments, process each independently, preserve results, return specified exit status | REQ-1, REQ-2, REQ-18, REQ-19 |
| Image input | Bounded bytes and original digest; facts and global measurements from the same input bytes; explicit format/frame/error status | REQ-2–REQ-5, REQ-9–REQ-10 |
| Metadata / provenance | Return values, parser/version coverage, errors, unverified labels, and distinct signature/trust/revocation states | REQ-6–REQ-8 |
| Assessment | Independent generation/edit task records; apply profile gates and exact verdict/advisory rules | REQ-10–REQ-15 |
| Report / output | Safe concise terminal text, complete versioned JSON, atomic protected destination | REQ-7, REQ-16–REQ-19 |

## Processing flow

1. Parse explicit paths; reject invalid batch size, directories, and URLs before opening files.
2. For each input in order, enforce byte limit, obtain bytes through a single per-image path, hash those original bytes, and validate format/frame/dimensions before full decode.
3. Run bounded metadata/provenance parsers, image measurements, and only locally configured model tasks. Isolate failures into the per-image result.
4. Assess each task independently. Apply the overall verdict and advisory rules only from task/profile status and evidence; unsupported or out-of-domain profiles yield experimental/inconclusive results.
5. Render a terminal summary without full sensitive values. If requested, serialize all parseable metadata to JSON and atomically write only to a safe destination.
6. Return nonzero when any specified batch/input/analysis/report failure occurred, without discarding other results.

## Dependencies and controls

- **Python / argparse / pytest:** selected runtime and minimal CLI/test tooling (ADR 0001).
- **Pillow:** selected decoder for explicit JPEG/PNG/frame checks, dimension checks before loading, configured pixel limits, and retained decoder safeguards.
- **ExifTool:** separately installed metadata subprocess; invoke with fixed arguments and no shell. Missing executable or parse errors are explicit; they must not silently become empty metadata.
- **C2PA:** use the official `c2pa-python` binding for local byte streams. Set both remote-manifest and OCSP fetching false; run in a worker with a timeout. Preserve the unchecked-fresh-revocation limitation.
- **Models:** no model/runtime is selected. Require explicit local artifacts/profile versions; no remote code or weight loading. Do not load arbitrary pickle artifacts.
- **Reference data:** local, versioned profile only; dataset/license/provenance and held-out gates required before non-experimental verdicts.

All user inputs and embedded metadata are untrusted. Per-image processing remains bounded and sequential. No scan-time network path is permitted; tests must deny outbound networking across parsing, provenance, and inference. JSON may contain sensitive metadata, so output destinations are operator-selected and terminal output is redacted by default.

## Testing strategy

- Unit tests for batch/path validation, bounds, requirement-specific verdict/advisory tables, JSON schema/version, metadata labels, and destination safety.
- Fixture integration tests for JPEG/PNG format/frame/dimension handling, parser coverage and failures, provenance states, and failure isolation.
- Adversarial parser fixtures test malformed, oversized, deeply nested, and time-consuming metadata.
- Security integration test runs scan paths with outbound network denied and verifies input bytes remain unchanged.
- Output tests exercise symlinks, aliases/resolved input destinations, atomic failure behavior, and batch result preservation.
- Held-out model evaluation is a separate release gate; ordinary functional tests cannot establish model validity.

## Deferred decisions and risks

- Exact Python packaging/install UX, supported Python version, and CI/linter choices.
- ExifTool version support, C2PA trust-list update process, and empirical network-denial evidence.
- Generation/edit models, artifact formats, licenses, calibration/profile data, and threshold values.
- Dataset population and splits, reference hardware, and numerical time/memory budgets.
- Whether a sandbox or OS-level resource isolation is necessary after parser/runtime feasibility tests.

## Architecture decisions

- [ADR 0001: Python local CLI](ADR/0001-python-local-cli.md)
- [ADR 0002: Bounded local processing](ADR/0002-bounded-local-processing.md)
- [ADR 0003: Task profiles and verdict gates](ADR/0003-task-profile-verdict-gates.md)
- Security risks and required mitigations: [epics threat model](epics-threat-model.md)
