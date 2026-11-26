# Verification

**Historical:** This verification covers the superseded Image Evidence Scanner implementation
only; it is not evidence for Fraud Netra.

**Status:** Blocked for full product completion; the committed local-scanner checkpoint is
verified.

## Fresh evidence

| Command | Result |
| --- | --- |
| `PATH=/tmp/opencode/Image-ExifTool-13.64:$PATH ./.venv/bin/python -m pytest -q` | 28 passed in 21.91s |
| `./.venv/bin/ruff check .` | All checks passed |
| `./.venv/bin/ruff format --check .` | 56 files already formatted |
| `git diff --check` | Passed |
| `./.venv/bin/python -m image_evidence_scanner --help` | Passed; CLI help rendered |

ExifTool is not installed system-wide in this environment; tests used the temporary ExifTool
13.64 distribution. The GitHub Actions IPv4/IPv6 firewall job was not executed locally.

## Acceptance review

- **REQ-1–5:** CLI tests cover one-to-five inputs, local-only path checks, source-byte
  preservation, SHA-256, size/pixel limits, and isolated input failures.
- **REQ-6–8:** Tests cover EXIF/XMP/IPTC values, sensitive-value terminal privacy, parser
  unavailable/timeout/output/nesting failures, C2PA absence, and disabled remote/OCSP settings.
  A real signed C2PA asset and live denied-network validation were not exercised.
- **REQ-9–10:** Tests cover image facts, ICC description where available, channel distributions,
  JPEG quantization/subsampling, bounded PNG chunk summaries, and no localization claim.
- **REQ-11–17:** Separate generation/edit records remain unconfigured and inconclusive; no
  unsupported model verdict is emitted. Model-backed task combinations and evaluation gates
  are not implemented.
- **REQ-18–20:** Tests cover versioned JSON output, per-input results, atomic destination
  protections, terminal summaries, and documentation.
- **NFR-1–5 / ISSUE-006:** Not verified; model, evaluation population, license, hardware, and
  release-profile decisions remain open.
- **NFR-6–9:** Input, parser time/output/nesting, and offline settings have local checks.
  The C2PA worker has no operating-system memory ceiling; CI firewall behavior is not locally
  observed.

## Blockers and handoff

Full product completion requires human-approved generation/edit models, evaluation dataset and
target population, licenses, hardware/resource budget, and release profile. `Reader.json()` also
materializes the C2PA manifest before the 8 MiB report check; this limit is not a peak-memory
ceiling. Keep that limitation explicit until a supported worker memory budget is selected.

No production model is selected or claimed, and the product goal is not complete.
