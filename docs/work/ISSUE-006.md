# ISSUE-006: Integrate evaluated local models and pass release gates

## Objective

Connect selected local generation/edit models and a documented reference profile only after feasibility, license, hardware, and held-out evaluation evidence exists.

## Requirements

- `REQ-11`–`REQ-15`, `REQ-18`, `NFR-1`–`NFR-5`, `NFR-8`, `NFR-9`

## Acceptance criteria

- Human-approved model/runtime versions, artifact formats, license review, target population, reference corpus, and hardware/time/memory budget are recorded before implementation.
- Model and profile artifacts are explicit local inputs; no scan-time download or arbitrary executable/pickle loading occurs.
- Generation and edit tasks are evaluated independently with source/generator/tool-disjoint splits and required transformation slices.
- The evaluation records class-specific precision/recall, false-positive/false-negative rates, balanced accuracy, calibration, confidence intervals, coverage/inconclusive rate, sample counts, and localization metrics where applicable.
- Thresholds are selected on calibration data, frozen before held-out evaluation, and named/versioned in reports.
- Only a task/domain meeting ≥80% sensitivity at ≤5% false-positive rate on each required held-out slice may produce non-experimental `likely`; calibrated likelihood additionally requires ECE ≤0.05 on a named independent population.
- Failed/unavailable profiles remain experimental or inconclusive; localization remains experimental until its mask-quality gate passes.

## Relevant files/modules

- `src/image_evidence_scanner/` task adapters, profile loading, assessment, and report modules
- `scripts/evaluate_profile.py`
- `tests/` model/profile contract and network-denial tests
- `data/` or user-supplied external local reference-data location (decide before implementation; do not commit sensitive or unlicensed corpora)
- `docs/product/decisions.md`, `docs/product/research.md`, `README.md`

## Dependencies

- `ISSUE-001`–`ISSUE-005`
- **Blocked pending human-approved model/data/runtime/license/hardware decisions and feasibility evidence.** No model choice is implied by this issue.

## Out of scope

- Hosted inference, runtime downloads, claims beyond the named evaluation population, and automatic consequential decisions.

## Validation

Run:

```sh
python -m pytest -q tests/test_model_profile.py tests/test_offline_scan.py
```

Run the project’s versioned held-out evaluation command:

```sh
python scripts/evaluate_profile.py --profile PATH --dataset PATH --split held-out --output PATH
```

**Pass bar:** contract/offline tests pass; the command exits 0 and emits a reproducible report with dataset/model/profile/threshold versions, sample counts, confidence intervals, and required metrics. The named profile passes all applicable release gates before non-experimental verdicts are enabled. If no profile passes, the no-profile/inconclusive path remains green and enabled.

## Documentation impact

- `README.md`: document only selected models, licenses, artifact setup, target population, evaluation profile, limits, and release status.

## Conditional specialist triggers

- `differential-review`: triggered; local model loading, release gating, and report interpretation are security/quality-sensitive.
- `security-threat-model`: revisit if model loading introduces a new trust boundary or artifacts become remotely supplied.

## Merge gate

No integration of a non-experimental profile without human approval of the named model/data/license and review of held-out evidence. Integrate experimental profiles only with green tests, explicit experimental status, and approved `itp-review`.
