# Acceptance criteria

These criteria verify the normative requirements in [`../../SPEC.md`](../../SPEC.md).
Model verdicts remain experimental or inconclusive until the applicable release gates pass.

## Batch input and safe processing

- **REQ-1:** Zero and six input paths fail before analysis with the one-to-five limit; one and five explicit paths are accepted for processing. Directories and URLs are rejected.
- **REQ-2:** JPEG and PNG single-frame inputs are analyzed. Unsupported, malformed, multi-frame, and unreadable inputs receive per-image status and reason; other batch results remain present.
- **REQ-3:** A scan makes no network request, leaves input bytes unchanged, and never writes a report over an input.
- **REQ-4:** Inputs over 100 MiB and decoded images over 50,000,000 pixels fail before expensive processing. Oversized/nested metadata and time-bound failures are bounded and isolated; decoder safeguards remain active.
- **REQ-5:** Each readable input has the SHA-256 of its original bytes computed before analysis. Read/hash failures are explicit.

## Metadata, provenance, and evidence

- **REQ-6:** Report all values exposed by documented local parsers for EXIF, XMP, IPTC, JPEG/PNG metadata, ICC, and embedded provenance. Include parser/version coverage, errors, unknown/unsupported blocks, and unverified labeling.
- **REQ-7:** JSON includes all parseable metadata, including sensitive fields. Default terminal output does not print full sensitive metadata.
- **REQ-8:** Provenance output distinguishes absent, invalid, valid-but-untrusted, trusted/valid, unsupported, and validator-error states where supported. Include signer/action/binding/validation details when available; disclose that fresh revocation status was not checked offline. Absence of provenance is neutral.
- **REQ-9:** Report format, byte size, dimensions, aspect ratio, mode/color space, available bit depth/frame count, relevant file structure, and named reproducible pixel indicators. JPEG quantization/subsampling are included when available. Forensic methods state prerequisites, references, results, and limits; none is presented as proof of origin/editing.
- **REQ-10:** Whole-image and localized-edit assessments are separate. A localization map is estimated, model/version identified, and only present when supported. Global statistics are not localized detection; specific camera attribution requires a documented fingerprint.

## Scores and verdicts

- **REQ-11:** Generation and editing each have separate task records with status, detector/model/profile versions, raw score semantics, threshold/provenance, calibration, tested population, limits, and reasons. Probability language is used only for independently calibrated scores on a named population.
- **REQ-12:** Every active classification profile identifies a versioned, documented reference population containing camera-captured, fully synthetic, and AI-edited examples. Evidence use is evaluated with metadata missing/modified/stripped. Inference uses exact local versions and performs no download.
- **REQ-13:** Each task decision is `likely`, `not_flagged`, or `inconclusive`, using its validated task threshold and naming that threshold/domain. `not_flagged` is not an authenticity claim.
- **REQ-14:** Each image has exactly one allowed overall verdict. The verdict follows the task/profile conditions in SPEC REQ-14; missing, invalid, conflicting, unsupported, or out-of-domain required evidence produces `inconclusive`. Explanation names evidence and avoids certainty, authenticity, fraud, and event-truth claims.
- **REQ-15:** Each image has exactly one allowed advisory. Likely, conflicting, inconsistent, low-coverage, or out-of-domain evidence recommends inspection. A no-inspection advisory is emitted only when all active tasks complete and the profile passes its validation gate.
- **REQ-16:** Text output presents verdict first, then separate scores, relevant evidence, model/data profile, advisory, and limitations. Detailed sensitive metadata stays in JSON; evidence categories remain distinguishable.
- **REQ-17:** No output labels an image/claim fraudulent, legitimate, true, false, authentic, or inauthentic; no consequential or external action occurs.

## Reporting, operation, and release

- **REQ-18:** Requested JSON is valid and versioned, with timestamp, tool version, batch status, one result per input, identity/facts/metadata/provenance/forensics/model tasks/interpretation, and failures. Available metadata and evidence are preserved.
- **REQ-19:** JSON writes are atomic and refuse symlink destinations and any destination resolving to an input. Invalid batch size, unreadable/unsupported input, analysis failure, or report-write failure returns nonzero while preserving available results whenever possible.
- **REQ-20:** User documentation covers CLI usage and limits, supported formats, privacy/sensitive metadata, parser coverage, verdict/score/advisory meanings, detector setup, evaluation profile, and limitations.
- **NFR-1–NFR-5:** Before non-experimental verdicts, document disjoint source/generator/camera/editing partitions, transformation stress tests, required task metrics, frozen thresholds, sample counts/confidence intervals, and held-out release-gate results. Localization remains experimental until its mask-quality gate passes.
- **NFR-6–NFR-9:** Verification demonstrates bounded parsing/resources, offline behavior, reproducible version/digest reporting, and correct score semantics. Runtime tests deny outbound networking across decode, provenance, and inference paths.
