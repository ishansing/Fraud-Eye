# ISSUE-004: Add reproducible image and forensic signals

## Objective

Report measured image/file signals with reproducible methods, prerequisites, and limitations; keep global measurements separate from localized-edit evidence.

## Requirements

- `REQ-9`, `REQ-10`, `REQ-18`, `REQ-20`, `NFR-8`

## Acceptance criteria

- Report per-channel distributions/statistics and available JPEG quantization/subsampling/file-structure indicators.
- Every forensic result names its method, prerequisites/reference data, result, and limitations.
- No sensor/camera attribution is emitted without an appropriate documented fingerprint; generic population statistics cannot identify a specific camera.
- Whole-image statistics are never presented as localized-edit detection.
- Any region map is labeled estimated localization and includes model/version; absent unsupported capability cleanly.

## Relevant files/modules

- `src/image_evidence_scanner/image_input.py`
- `src/image_evidence_scanner/report.py`
- `tests/test_scan_cli.py`
- `README.md`

## Dependencies

- `ISSUE-001`, `ISSUE-002`
- `ISSUE-003` for metadata context when signals depend on parser output.

## Out of scope

- Claiming universal camera origin, editing history, or authenticity; adding sensor attribution without a documented reference fingerprint.

## Validation

Run:

```sh
python -m pytest -q tests/test_scan_cli.py
ruff check .
```

**Pass bar:** all tests pass; fixed fixtures produce deterministic named values; missing prerequisites produce explicit unavailable/limited results rather than inferred origin; no global-only signal produces a localization field.

## Documentation impact

- `README.md`: describe emitted measurements and why none independently proves image origin or editing.

## Conditional specialist triggers

- `differential-review`: considered; trigger if new native parsers, untrusted references, or security-sensitive file handling is added.

## Merge gate

Integrate when checks pass and `itp-review` approves requirement coverage and score/evidence wording.
