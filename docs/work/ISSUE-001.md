# ISSUE-001: Bootstrap the Python CLI

## Objective

Create the smallest runnable project foundation: Python package, test runner, linter/formatter, CI, and a CLI smoke test.

## Requirements

- `REQ-1`, `REQ-3`, `REQ-20`

## Acceptance criteria

- The project installs locally using the documented development command and declares a supported Python version.
- `python -m image_evidence_scanner --help` succeeds and explains that input paths are required.
- `python -m pytest -q` passes the CLI smoke test.
- `ruff check .` and `ruff format --check .` pass.
- CI runs those same checks on a clean checkout. CI performs no image scan and has no secrets.

## Relevant files/modules

- `pyproject.toml`
- `src/image_evidence_scanner/cli.py`
- `tests/test_cli.py`
- `.github/workflows/ci.yml`
- `README.md`

## Dependencies

- None; this is the bootstrap slice.

## Out of scope

- Image decoding, metadata extraction, model dependencies, release packaging, or publishing.

## Validation

Run:

```sh
python -m image_evidence_scanner --help
python -m pytest -q
ruff check .
ruff format --check .
```

**Pass bar:** all commands exit 0; CLI help exits 0 and includes usage and an input-path argument; the same checks pass in CI.

## Documentation impact

- `README.md`: add development setup and CLI smoke-test usage.

## Conditional specialist triggers

- `differential-review`: not triggered for bootstrap-only tooling/configuration unless a security-sensitive workflow or dependency behavior changes.

## Merge gate

Integrate when all listed commands and CI pass and `itp-review` returns approved.
