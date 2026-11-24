# ADR 0001: Python local CLI

- **Status:** Accepted
- **Date:** 2026-11-24

## Context

V1 is a local command-line tool for image parsing and local model inference. The project is greenfield. Research identifies Python's standard `argparse`, `venv`, and the image/model ecosystem as a low-friction fit.

## Decision

Use Python for a single-user CLI, `argparse` for command parsing, and `pytest` for tests. Provide no daemon, hosted inference, or authentication layer in v1. Use the standard `src/` package layout when bootstrapping the application.

## Consequences

- Keeps the initial interface and install surface small while using the available image/model ecosystem.
- Python packaging and distribution details remain to be decided during bootstrap architecture.
- No runtime downloads; dependencies and model/data artifacts must be present before scanning.

## Evidence

- `PRD.md` §§3, 5 and `SPEC.md` §§2–4 define the local CLI boundary.
- `docs/product/research.md` §CLI/runtime and tests cites the Python and pytest documentation.
