# Differential security review

**Range:** `a22a883...e14156b`  
**Scope:** Local image input, ExifTool/C2PA process boundaries, report output, and scan egress.
The runtime is greenfield in this range; there is no pre-existing application behavior to
regress.

## Threat model and controls

- Attacker supplies a malformed or adversarial local JPEG/PNG that an operator chooses to scan.
- Installed ExifTool and `c2pa-python` artifacts are operator-controlled.
- Inputs are limited to 100 MiB and 50 million decoded pixels. ExifTool has fixed argv, a
  5-second timeout, and a 16 MiB output cap. C2PA runs in a separate worker with a 10-second
  timeout, explicit remote-manifest/OCSP disablement, and an 8 MiB report cap.
- The worker context is exercised with an active-manifest-shaped fixture and asserts both
  network settings are false. CI rejects and counts IPv4 and IPv6 OUTPUT traffic.
- JSON output is written atomically and rejects symlink and input-file destinations.

## Findings

### MEDIUM — C2PA report cap is not a peak-memory ceiling

`src/image_evidence_scanner/c2pa_worker.py:18–30` obtains the entire manifest JSON string
through `Reader.json()` before checking its 8 MiB size. The 100 MiB input bound and timeout
limit the exposure, but do not enforce an operating-system memory limit for the child. A
crafted large manifest may therefore consume substantially more memory than the report cap
before it is rejected. The current risk is bounded by input size and process lifetime; no
reproducible exhaustion was demonstrated. README and `.itp/run.md` disclose that no worker
memory ceiling is set; select a supported platform budget before claiming that protection.

## Coverage and blast radius

- No removed security code or baseline regression was found; application code is newly added
  after the design-only baseline.
- Critical-path callers are narrow: `scan_batch` invokes metadata and C2PA once per supported
  image; CLI accepts at most five images.
- Tests cover image bounds, ExifTool timeout/output/nesting bounds, offline context settings,
  C2PA absence, report destination safety, and pixel/file-structure summaries.
- Local test suite passed. The GitHub Actions firewall workflow was not executed locally, and
  no real signed C2PA asset was tested under denied networking.

## Recommendation

No demonstrated compromise or network bypass. Keep the C2PA memory-ceiling limitation visible;
do not treat the 8 MiB report cap as a process-memory bound.
