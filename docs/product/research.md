# Implementation-planning research

Research for the open technical choices in `PRD.md` and `SPEC.md`; evidence is not a product decision. Sources checked 2026-11-24. “Recommendation” denotes an implementation-planning option, not an adopted choice.

## Findings

### CLI/runtime and tests

- **Evidence:** Python provides built-in `argparse` for CLI parsing and `venv` for isolated environments. `pytest` documents a conventional `src/` layout and test execution with `python -m pytest`. [Python argparse](https://docs.python.org/3/library/argparse.html), [Python venv](https://docs.python.org/3/library/venv.html), [pytest good practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- **Recommendation:** Python is a low-friction CLI/runtime candidate for image/model ecosystem integration; use stdlib `argparse` and `pytest`, avoiding a new CLI framework until needs justify it. This is not an evaluation of packaging/install UX or native distribution.

### Bounded JPEG/PNG decode

- **Evidence:** Pillow supports JPEG and PNG, opens lazily (header identification before pixel loading), and has `MAX_IMAGE_PIXELS` decompression-bomb warning/error behavior. Its documented pixel default is a library safeguard, not this product’s 50-million-pixel contract. [Pillow image API](https://pillow.readthedocs.io/en/stable/reference/Image.html), [Pillow formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
- **Recommendation:** Pillow is a plausible decoder if the implementation restricts format explicitly to JPEG/PNG, checks dimensions before `load()`, sets the configured bound to the SPEC policy, treats the warning as an error, checks frame count, and retains built-in safeguards. Enforce byte-size and wall-clock/resource bounds separately; pixel count alone does not bound parser time or all memory use.

### Broad metadata

- **Evidence:** ExifTool’s first-party format tables list read support across EXIF, GPS, IPTC, XMP, ICC profiles, JPEG and PNG; its JPEG documentation covers APP segments including EXIF/XMP. [ExifTool supported formats](https://exiftool.org/#supported), [ExifTool application docs](https://exiftool.org/exiftool_pod.html)
- **Evidence:** C2PA is a distinct signed provenance format; ExifTool’s support for recognizing C2PA/JUMBF metadata does not by itself perform C2PA signature/trust validation. The C2PA SDK advertises parsing and validating embedded manifests. [ExifTool supported formats](https://exiftool.org/#supported), [C2PA Rust SDK](https://github.com/contentauth/c2pa-rs)
- **Recommendation:** Evaluate ExifTool as a broad read-only metadata backend, with versioned output and an explicit allowlisted invocation; independently bound subprocess time/output and capture errors. Verify fields/coverage on representative JPEG and PNG fixtures. Parser support does not guarantee every unknown block/value is exposed, so SPEC’s coverage contract still needs a defined inventory.

### Offline C2PA validation

- **Evidence:** The official C2PA Rust SDK supports parsing and validating manifests, with configurable settings/context and trust anchors. C2PA guidance explains that signer trust depends on configured trust lists and revocation services/status. [c2pa-rs](https://github.com/contentauth/c2pa-rs), [SDK settings guide](https://opensource.contentauthenticity.org/docs/sdk-repos/c2pa-cpp/docs/context-settings), [C2PA guidance](https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html)
- **Recommendation:** Prototype the SDK’s local-file API with an explicit locally stored trust list and no network configuration. Report signature/manifest validity separately from trust and freshness of revocation status. The reviewed sources establish configurability and local trust-anchor input, but do **not** establish a universal “network disabled” switch or guarantee all validator code paths are network-free; prove this with network-denial tests or process-level isolation before claiming REQ-3/8.

### Local model runtime and weight safety

- **Evidence:** ONNX Runtime is designed to load and run a local model path; it exposes `disable_telemetry_events()`, which only documents disabling telemetry—not all possible networking. [ONNX Runtime Python API](https://onnxruntime.ai/docs/api/python/api_summary.html), [ONNX Runtime privacy](https://github.com/microsoft/onnxruntime/blob/main/docs/Privacy.md)
- **Evidence:** PyTorch’s serialization documentation describes `weights_only=True` loading to restrict unpickling behavior. That is a risk reduction, not proof that an arbitrary artifact is safe or that the model cannot consume excessive resources. [PyTorch serialization notes](https://docs.pytorch.org/docs/stable/notes/serialization.html)
- **Recommendation:** Prefer a fixed, locally supplied ONNX artifact and ONNX Runtime for inference if selected candidate models export correctly; it separates inference from training dependencies. Do not download weights/code at scan time. Verify artifact hashes against a locally supplied manifest, pin model/runtime versions, and test with network denied. Avoid accepting arbitrary pickle/model code. Evaluate task accuracy, licenses, hardware support, and ONNX conversion on actual candidate detectors before selection.

### Network-free execution

- **Evidence:** A runtime’s offline/local-model API or telemetry opt-out is not a system-wide network prohibition; the reviewed ONNX Runtime API only promises telemetry-event disablement. C2PA validation may depend on configured revocation/trust behavior.
- **Recommendation:** Treat “no network” as a process execution invariant: deny outbound networking in integration tests (OS/network namespace or equivalent), exercise scan paths including C2PA and model initialization, and fail tests if any connection is attempted. Require models, trust lists, and reference data to be explicit local paths. Build/install dependencies before scan time; no runtime fetch/update path.

## Unresolved / evidence limits

- No concrete generation/edit detector was selected or validated; neither model quality, licensing, hardware feasibility, nor release targets can be established from runtime documentation.
- The exact parser behavior for malformed/oversized EXIF, XMP, IPTC, ICC, and nested container blocks needs adversarial fixture testing; documentation feature lists are not resource-bound guarantees.
- Confirm the C2PA SDK version, supported JPEG/PNG bindings, trust-list provenance/update process, revocation behavior, and network attempts empirically.
- Define operational memory/time bounds and supported reference hardware; SPEC gives input-size/pixel ceilings but not a scan-time budget.

## Sources

All links above are first-party project documentation, official specifications, or official project repositories. External research was limited to the claims cited inline; recommendations are explicitly separated from documented facts.
