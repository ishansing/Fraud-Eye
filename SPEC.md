# Image Evidence Scanner — Product Specification

| Field | Value |
| --- | --- |
| Status | Draft for architecture and implementation |
| Version | 1.1 |
| Updated | 2026-11-23 |
| Product requirements | [PRD](PRD.md) |
| Acceptance criteria | [Acceptance criteria](docs/product/acceptance-criteria.md) |
| Research | [Research](docs/product/research.md) |

## 1. Purpose and authority

This document defines the normative behavior of Image Evidence Scanner v1. The PRD defines user outcomes; this specification defines implementation requirements. Acceptance criteria provide the verification conditions for each requirement. Where model behavior is not validated for the selected evaluation domain, the system must report the result as experimental or inconclusive rather than imply certainty.

## 2. Product boundary

The product is an offline-first local CLI. It accepts one to five explicitly selected image files per invocation, analyzes each supported image, and emits a plain-language result plus optional JSON. It assesses likely AI generation and AI-assisted editing. It does not decide fraud, legitimacy, event truth, or legal authenticity.

Version one supports single-frame JPEG and PNG. Directory recursion, remote URLs, network services, and formats beyond JPEG/PNG are out of scope.

## 3. Terms

- **Camera-captured reference:** A dataset image with independently documented camera-origin ground truth. It can still be conventionally edited or depict a false event.
- **AI-generated:** Most or all visible image content was synthesized by a generative system.
- **AI-edited:** A source image contains one or more changes produced by a generative AI system. Traditional non-generative editing is not automatically AI editing.
- **Detector score:** A versioned model's numeric output. It is a probability only when calibrated and validated for the stated population.
- **Verdict:** The tool's evidence-based AI-origin category. It is not a fraud or truth judgment.
- **Inconclusive:** Available or validated evidence is insufficient, conflicting, unsupported, or outside the detector's tested scope.

## 4. Functional requirements

“MUST” is a release requirement. IDs are stable and acceptance criteria reference them.

### Batch inputs and safe processing

- **REQ-1 — Batch size:** Each CLI invocation MUST accept between one and five explicit image file paths. An invocation with zero or more than five paths MUST fail before analysis and explain the accepted limit. Directory paths and URLs MUST be rejected in v1.
- **REQ-2 — Supported formats:** The scanner MUST analyze single-frame JPEG and PNG. Unsupported, malformed, multi-frame, and unreadable files MUST receive an explicit per-image status and reason. A failure for one selected image MUST NOT suppress other image results.
- **REQ-3 — Local and read-only:** All image analysis and model inference MUST run locally. A scan MUST make no network requests, modify no source bytes, and MUST NOT overwrite an input file with a report.
- **REQ-4 — Bounded parsing:** The scanner MUST reject files larger than 100 MiB and images larger than 50,000,000 decoded pixels before unbounded image processing. It MUST retain decoder safeguards and enforce limits on metadata size, nested structures, and processing time. Limit failures MUST be isolated per file.
- **REQ-5 — Image identity:** For each readable file, the report MUST contain SHA-256 of the original bytes. The digest MUST be computed before analysis. A failure to read or hash MUST be explicit.

### Metadata, provenance, and forensic evidence

- **REQ-6 — Metadata coverage:** The scanner MUST extract all values available from its documented, versioned local parsers for EXIF, XMP, IPTC, JPEG metadata segments, PNG ancillary metadata, ICC profiles, and embedded provenance. Reports MUST identify parser/version coverage and extraction errors. Unknown or unsupported blocks MUST be reported as such, not silently treated as empty metadata. Metadata values MUST be labeled unverified unless covered by validated signed provenance.
- **REQ-7 — Sensitive metadata:** Local JSON MUST include all parseable metadata values by default, including GPS, device identifiers, timestamps, creator fields, and AI-system/prompt fields when present. Default terminal output MUST summarize findings without printing full sensitive values. Documentation MUST warn that reports may contain sensitive data.
- **REQ-8 — Provenance and markings:** The scanner MUST inspect C2PA Content Credentials and any supported recognized AI-watermark/metadata markings. C2PA output MUST distinguish absent, present-but-invalid, valid-but-untrusted, trusted/valid, unsupported, and validator-error states as supported by the validator. Include signer, actions, binding, and validation details when available. With network disabled, report that fresh revocation status was not checked. A signed provenance claim can support attribution of a declared action; it MUST NOT be represented as proof of event truth. Absence of provenance or a watermark MUST NOT be evidence that an image is camera-captured.
- **REQ-9 — Technical image signals:** For each supported image, the scanner MUST report format, byte size, dimensions, aspect ratio, mode/color space, bit depth when available, frame count, and relevant file structure. It MUST provide named reproducible pixel indicators, including per-channel distributions/statistics. JPEG-specific indicators such as quantization tables and chroma/subsampling information MUST be reported when available. Any noise, resampling, demosaicing/CFA, sensor-pattern, compression-history, or similar forensic result MUST identify its method, prerequisites/reference data, result, and limits. These indicators MUST NOT be treated as universal proof of camera origin or editing.
- **REQ-10 — Image-level and local evidence:** The report MUST keep whole-image classification separate from localized editing analysis. If a configured edit model provides a region map or heatmap, the result MUST identify the model/version and be labeled an estimated localization. Global image statistics MUST NOT be presented as localized edit detection. Sensor/camera attribution MUST require an appropriate documented reference fingerprint; it MUST NOT infer a specific camera from generic population statistics alone.

### AI scores and verdict

- **REQ-11 — Separate task outputs:** The scanner MUST produce separate AI-generation and AI-edit assessment records. Each record MUST include status, detector name/version, model artifact identifier, raw score and score semantics, threshold and threshold provenance, calibration profile, tested population, limitations, and reasons. A calibrated 0–100 likelihood MAY be reported only when calibration on independent data supports that interpretation. Otherwise show the model's raw score with units and label it uncalibrated. Scores MUST NOT be averaged across task types into one universal authenticity score.
- **REQ-12 — Reference comparison:** The classification pipeline MUST compare evidence against a versioned reference/training profile whose documented labeled data includes camera-captured images, fully AI-generated images, and AI-edited images. Metadata and pixel indicators may contribute only when their use has been evaluated under missing, modified, and stripped-metadata conditions. Runtime inference MUST use the exact local profile/model versions named in the report; it MUST NOT download data, models, or code.
- **REQ-13 — Per-task decision:** Each task MUST produce one of `likely`, `not_flagged`, or `inconclusive` using its validated, task-specific threshold. The report MUST state the threshold and validation domain. `not_flagged` MUST mean only that this detector did not cross its threshold.
- **REQ-14 — Overall verdict:** Each image MUST receive exactly one overall verdict:
  - `likely_ai_generated` when the validated generation task crosses its threshold and the result is not materially contradicted by other required evidence;
  - `likely_ai_edited` when the validated edit task crosses its threshold and the generation task does not establish full-image synthesis;
  - `likely_ai_generated_and_edited` when both validated tasks cross their thresholds;
  - `no_configured_ai_signal_crossed_threshold` only when all tasks required by the active profile ran successfully below their thresholds;
  - `inconclusive` when required task output is absent, invalid, out of scope, materially conflicting, or not supported by a validated profile.
  The verdict MUST include a concise plain-language explanation and evidence references. It MUST NOT claim certainty, authenticity, fraud, or event truth.
- **REQ-15 — Further-inspection advisory:** Each image MUST include `recommended`, `not_indicated_by_configured_models`, or `inconclusive`. A likely classification, conflicting indicators, provenance inconsistency, low evidence coverage, or out-of-domain status MUST recommend further inspection. The no-trigger advisory is permitted only when all active-profile tasks completed and the profile's validation gate passed. The report MUST describe the scope of any `not_indicated` result.
- **REQ-16 — Clear user response:** Text output MUST present the verdict first, followed by generation/edit scores, the most relevant evidence, model/data profile, advisory, and a short limitation statement. Detailed metadata remains in JSON. Output MUST distinguish direct file observations, verified provenance, detector estimates, and final interpretation.
- **REQ-17 — No fraud decision:** The scanner MUST NOT label an image or its associated claim fraudulent/legitimate, true/false, or authentic/inauthentic, and MUST NOT trigger any external or consequential action.

### Reporting and operation

- **REQ-18 — Batch report:** The CLI MUST provide a concise human-readable summary for each selected image and a batch summary. When requested, it MUST write a valid versioned JSON report with one result per input and batch-level status. It MUST preserve all available metadata values and include evidence, parser coverage, model/data versions, scores, thresholds, verdict, advisory, limitations, and failures.
- **REQ-19 — Output safety and exit status:** JSON writes MUST be atomic and MUST refuse symlink destinations or destinations that resolve to an input. The command MUST return nonzero for invalid batch size, unreadable/unsupported images, analysis failures, or report-write failures while preserving available per-image results when the report destination is writable.
- **REQ-20 — Documentation:** User documentation MUST cover CLI usage, the one-to-five limit, supported formats, privacy and metadata sensitivity, parser coverage, verdict semantics, detector setup, reference/evaluation profile, limits, and the meaning of every score/advisory.

## 5. JSON report contract

The top-level report MUST include `schema_version`, scan timestamp, tool version, batch status, and per-image results. Each result MUST contain:

| Group | Required content |
| --- | --- |
| Identity | Input path, processing status, SHA-256 when readable, detected format, file size. |
| Image facts | Dimensions, aspect ratio, mode/color space, bit depth/frame count when available. |
| Metadata | Parseable values, parser/version coverage, parse errors, explicit unverified label. |
| Provenance | C2PA/recognized-marking status, validation details, signer/action/binding fields when available, revocation limitation. |
| Forensics | Named measurements, results, prerequisites/reference data, limitations, optional edit localization. |
| Model tasks | Separate generation and editing status, model/profile versions, score type/value, calibration, threshold, validation scope, limitations. |
| Interpretation | Task decisions, one overall verdict, rationale, advisory, evidence coverage, and unresolved/contradicting signals. |

JSON field names are draft until the first stable release. Any incompatible change after that release requires a schema-version increment.

## 6. Quality, validation, and robustness requirements

- **NFR-1 — Representative data:** Training/reference, calibration, and final test partitions MUST be separate by source image and disjoint by generator family/version, camera model where possible, editing tool, and acquisition pipeline. Dataset provenance, label method, licensing, class balance, and known gaps MUST be recorded.
- **NFR-2 — Stress testing:** Evaluation MUST include common recompression qualities, resizing, cropping, screenshots/re-digitization, metadata removal and modification, and camera computational-photography pipelines. Evaluate model behavior for generation and editing separately.
- **NFR-3 — Metrics:** Report per-class precision, recall/sensitivity, specificity, false-positive rate, false-negative rate, balanced accuracy, calibration (e.g. Brier score and expected calibration error), confidence intervals, coverage/inconclusive rate, and edit-localization metrics (e.g. F1/IoU) where applicable. Aggregate accuracy alone is insufficient.
- **NFR-4 — Threshold governance:** Select task thresholds on calibration data against a documented false-positive constraint. Freeze thresholds before final held-out evaluation. Reports and release notes MUST identify threshold version and operating population. Scores outside the validated population MUST be downgraded to experimental or inconclusive.
- **NFR-5 — Robustness release gate:** To issue non-experimental `likely` verdicts for a task/domain, the frozen threshold MUST achieve at least 80% sensitivity at no more than 5% false-positive rate on that task's held-out target population and each required core transformation slice. A score MUST NOT be called a calibrated likelihood unless the independent calibration profile has ECE ≤ 0.05 and its population is named. Publish confidence intervals and sample counts. Heatmaps MUST remain experimental until pixel-localization evaluation passes a documented mask-quality threshold. These are initial project release targets, not research findings or claims about any current model. If a target is missed, results for that domain MUST remain experimental or inconclusive.
- **NFR-6 — Resource and parser safety:** Enforce the file, pixel, metadata, and time bounds before expensive analysis; retain library decoder limits; isolate malformed metadata and per-image failures.
- **NFR-7 — Privacy and offline behavior:** No network requests during scan. Full local JSON may contain sensitive data. Default text output must not expose those values.
- **NFR-8 — Reproducibility:** Record software, parser, model, calibration profile, reference dataset/profile, and threshold versions with each result. Preserve the original input digest.
- **NFR-9 — Score semantics:** Detector scores from different tasks or models are not directly comparable. Use probability language only for independently calibrated scores and name the population to which that calibration applies.

## 7. Acceptance and release readiness

See [docs/product/acceptance-criteria.md](docs/product/acceptance-criteria.md). Functional completion does not satisfy the model release gate by itself. AI verdicts remain marked experimental until the NFR-1 through NFR-5 evidence is documented and the selected profile passes its approved gate.

## 8. Decisions and open questions

### Confirmed

- One to five explicit local image files per scan; no folder or URL inputs in v1.
- Extract all available supported metadata, keep it local, and include it in JSON by default.
- Compare against documented, held-out camera-captured and synthetic/edit reference populations, not fixed universal EXIF rules.
- Provide a clear AI-generation/AI-edit verdict with separate task scores and a further-inspection advisory.
- Keep fraud, legitimacy, and event-truth decisions out of scope.

### Open for architecture and implementation planning

1. Which generation and edit models, versions, licenses, and local runtimes meet this project's deployment and evaluation constraints?
2. Which dataset release/profile and target users define the evaluation population?
3. Should the initial task gate of ≥80% sensitivity at ≤5% false-positive rate and ECE ≤0.05 be retained after a feasibility study?
4. What resource/time budget and hardware define support for batches of five?
5. Which metadata parser stack offers safe and sufficiently broad format coverage?

## 9. Change control

Product goals belong in the PRD. Normative behavior belongs here under stable `REQ-*` IDs. Verification conditions belong in acceptance criteria and reference those IDs. Changes to verdict categories, score semantics, limits, supported formats, metadata exposure, reference profile, or network behavior require updating this spec, acceptance criteria, decisions, architecture, and user documentation.
