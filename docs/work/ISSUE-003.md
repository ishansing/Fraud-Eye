# ISSUE-003: Extract metadata and validate provenance

## Objective

Extend the scan with versioned metadata coverage, explicit parser failures, sensitive-value handling, and offline provenance status.

## Requirements

- `REQ-6`–`REQ-8`, `REQ-18`, `REQ-20`, `NFR-6`, `NFR-7`, `NFR-8`

## Acceptance criteria

- Extract all values exposed by the adopted documented local parsers for EXIF, XMP, IPTC, JPEG/PNG metadata, ICC, and supported embedded provenance.
- Report parser name/version/coverage, errors, unsupported blocks, and unverified metadata labels; do not silently map parse failures to empty metadata.
- Include parseable sensitive metadata in local JSON, while terminal output summarizes without printing full values.
- C2PA states distinguish absent, invalid, valid-but-untrusted, trusted/valid, unsupported, and validator error where the selected SDK supports them; include signer/action/binding details when available.
- Offline validation states that fresh revocation status was not checked. No provenance/watermark remains neutral evidence.
- Enforce metadata byte/nesting/time/output bounds and isolate failures per image.
- Integration tests deny outbound networking across metadata and provenance paths.

## Relevant files/modules

- `src/image_evidence_scanner/{metadata,provenance,scan,report}.py`
- `tests/{test_metadata,test_provenance,test_offline_scan}.py`
- Bounded local test fixtures and `README.md`

## Dependencies

- `ISSUE-001`, `ISSUE-002`
- ExifTool adoption requires representative and adversarial fixture results.
- C2PA SDK/binding adoption requires proof of local-file support and no network activity; otherwise preserve explicit unsupported status and keep this slice blocked from claiming validation coverage.

## Out of scope

- Trust-list update service, online revocation, signing, metadata editing, and remote parser/model services.

## Validation

Run:

```sh
python -m pytest -q tests/test_metadata.py tests/test_provenance.py tests/test_offline_scan.py
ruff check .
```

**Pass bar:** all tests pass; fixtures demonstrate each supported parser's coverage/errors; network-denied tests observe zero attempted connections; malformed and oversized blocks remain within configured limits and do not suppress sibling image results.

## Documentation impact

- `README.md`: explain parser coverage/version reporting, provenance trust states, sensitive JSON contents, and offline revocation limits.

## Conditional specialist triggers

- `differential-review`: triggered; this slice invokes parsers on hostile content and handles provenance claims.
- `security-threat-model`: architecture threat model exists; revisit only if implementation adds a new trust boundary or external exposure.

## Merge gate

Integrate only with green checks, approved `itp-review`, and documented parser/C2PA versions and fixture results. Any unresolved network attempt or unbounded parser behavior blocks integration.
