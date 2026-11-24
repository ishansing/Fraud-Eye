# ISSUE-002: Scan bounded local image batches

## Objective

Implement one useful end-to-end scan path for explicit JPEG/PNG inputs: validate, hash, measure basic image facts, isolate failures, and render text plus optional JSON.

## Requirements

- `REQ-1`–`REQ-5`, `REQ-9` (basic facts), `REQ-16`, `REQ-18`, `REQ-19`

## Acceptance criteria

- Reject zero or more than five paths before analysis; reject directories and URLs.
- Analyze valid single-frame JPEG/PNG; report unsupported, malformed, multi-frame, unreadable, and per-file size/pixel-limit failures explicitly without suppressing other results.
- Enforce 100 MiB input and 50,000,000 decoded-pixel limits before full decode; preserve decoder safeguards.
- Hash original bytes before analysis and report SHA-256, format, size, dimensions, aspect ratio, mode, and frame count when available.
- Do not make network requests or modify inputs.
- Before model assessments exist, each image's assessment is explicitly inconclusive. Text output leads with verdict/status and does not dump sensitive metadata. JSON is valid/versioned, one result per input, and batch status is present.
- JSON output is atomic and refuses symlink destinations and destinations resolving to inputs. Batch processing preserves successful results when another input fails.

## Relevant files/modules

- `src/image_evidence_scanner/{cli,scan,image_input,report,output}.py`
- `tests/{test_cli,test_scan,test_image_input,test_report,test_output}.py`
- `README.md`

## Dependencies

- `ISSUE-001`

## Out of scope

- EXIF/XMP/IPTC extraction, C2PA validation, advanced forensic signals, and AI models.

## Validation

Run:

```sh
python -m pytest -q tests/test_cli.py tests/test_scan.py tests/test_image_input.py tests/test_report.py tests/test_output.py
ruff check .
```

**Pass bar:** all tests pass; tests cover 0/1/5/6 inputs, malformed/unsupported/multi-frame files, byte/pixel bounds, hash-before-analysis, mixed batch outcomes, no input mutation, symlink/input output refusal, and atomic-write failure.

## Documentation impact

- `README.md`: document supported formats, batch limits, file/pixel limits, invocation, output behavior, and local-only/privacy warning.

## Conditional specialist triggers

- `differential-review`: triggered; this slice parses untrusted files and writes user-selected paths.

## Merge gate

Integrate only with green checks, approved `itp-review`, and no unresolved high-severity security findings.
