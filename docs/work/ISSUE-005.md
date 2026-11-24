# ISSUE-005: Implement task assessments and conservative verdicts

## Objective

Implement the generation/edit task-result contract and overall verdict/advisory rules independently of any unvalidated model.

## Requirements

- `REQ-10`–`REQ-17`, `REQ-18`, `NFR-4`, `NFR-8`, `NFR-9`

## Acceptance criteria

- Generation and editing remain separate task records; there is no averaged authenticity score.
- Each task result carries status, detector/model/profile identity, score semantics, threshold provenance, calibration/population, limitations, and reasons.
- Raw scores are explicitly uncalibrated; probability language is available only for a named independent calibration profile meeting its gate.
- All task and overall verdict combinations follow `SPEC.md` REQ-13/REQ-14.
- Missing, invalid, out-of-domain, conflicting, or unvalidated task/profile results yield experimental or inconclusive outcomes as specified.
- `not_flagged` and no-trigger advisory text are explicitly limited to configured, successfully run tasks/profile scope.
- Likely/conflicting/inconsistent/low-coverage/out-of-domain cases recommend further inspection.
- With no configured validated profile, every image remains inconclusive/experimental and never receives a non-experimental likely verdict.

## Relevant files/modules

- `src/image_evidence_scanner/assessment.py`
- `src/image_evidence_scanner/report.py`
- `tests/test_assessment.py`
- `README.md`

## Dependencies

- `ISSUE-001`, `ISSUE-002`
- `ISSUE-003` and `ISSUE-004` for evidence context.

## Out of scope

- Selecting or claiming a model, calibration population, or validated threshold.

## Validation

Run:

```sh
python -m pytest -q tests/test_assessment.py tests/test_report.py
ruff check .
```

**Pass bar:** all task/verdict/advisory decision-table tests pass, including missing/invalid/conflicting/out-of-domain profile cases and raw-vs-calibrated score semantics.

## Documentation impact

- `README.md`: document verdict categories, score semantics, advisory meanings, and experimental/unvalidated behavior.

## Conditional specialist triggers

- `differential-review`: triggered if assessment rules or profile gating change; this is the core trust/interpretation surface.
- `agentic-eval`: not triggered; scanner model evaluation is covered by SPEC NFR-1–NFR-5, not agent behavior evaluation.

## Merge gate

Integrate with green checks, approved `itp-review`, and no unsupported certainty or authenticity language.
