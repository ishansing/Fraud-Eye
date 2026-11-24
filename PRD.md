# Product Requirements Document

## Image Evidence Scanner

| Field | Value |
| --- | --- |
| Status | Draft for implementation planning |
| Version | 1.1 |
| Last updated | 2026-11-23 |
| Product owner | Project team |
| Product type | Offline-first local CLI |
| Normative requirements | [SPEC.md](SPEC.md) |
| Acceptance criteria | [Acceptance criteria](docs/product/acceptance-criteria.md) |
| Research and bibliography | [Research](docs/product/research.md) · References (not yet available) |

## 1. Executive summary

Image Evidence Scanner analyzes a batch of one to five local images and produces a clear, evidence-backed assessment of whether each image is likely fully AI-generated, likely AI-edited, both, or inconclusive. It gathers parseable metadata, provenance claims, image/file properties, pixel-level signals, and outputs from validated local detectors. It compares the image evidence against documented camera-captured and AI-generated/edited reference populations.

The product is designed for a university project and runs locally without uploading images or reports. It gives a direct result, separate generation and editing scores, the evidence behind the result, and a recommendation for further inspection. It does not determine whether a claim or transaction is fraudulent, whether a depicted event occurred, or whether an image is legally authentic.

## 2. Problem statement

Reviewers need a repeatable way to examine whether an image may have been generated or edited with AI. Metadata may be missing, edited, or fabricated. Pixel and camera traces vary across cameras and processing pipelines. Modern detectors can perform well on familiar test data and fail on newer generators, local edits, or common image transformations.

The scanner must combine these signal classes without treating any one of them as definitive. A useful result must be direct enough to guide a reviewer and careful enough to distinguish a model estimate from cryptographically validated provenance or ordinary file metadata.

## 3. Product goals

1. Accept one to five explicitly selected images in a single scan and return a result for each.
2. Collect all metadata values exposed by the supported, bounded parsers and report parser coverage and failures.
3. Collect reproducible image, file-structure, provenance, and pixel-level evidence relevant to image origin and editing.
4. Distinguish full-image AI generation from AI-assisted editing; provide localized edit estimates when the selected model supports them.
5. Compare model features against a documented, held-out reference population containing known camera-captured, fully synthetic, and AI-edited images.
6. Give users a concise verdict, separate generation/edit scores, reasons, evidence coverage, and next-step advisory.
7. Keep all scans local, preserve originals, and bound resource use for untrusted files.

## 4. Users and primary jobs

### Primary user: image reviewer

**Job:** Given a suspicious or unexplained image, quickly see the best available evidence about AI generation or AI editing and know whether further inspection is warranted.

### Secondary user: student or researcher

**Job:** Run a reproducible local analysis on a small image batch and inspect structured evidence, model scores, metadata, and validation results.

## 5. V1 scope

### Included

- Local CLI accepting one through five image file paths per invocation.
- Single-frame JPEG and PNG input, with unsupported or invalid files reported explicitly.
- Original-byte SHA-256 and basic file/image facts.
- EXIF, XMP, IPTC, format-container metadata, ICC profile information, and embedded C2PA data to the extent supported by bounded local parsers.
- Pixel and file indicators such as channel statistics, JPEG quantization/structure, and validated forensic residual or camera-origin features when available.
- Separate local AI-generation and AI-edit detectors; edit localization when supported.
- Evidence-backed image-origin assessment, direct text summary, and optional versioned JSON report.
- Optional local reference data and model weights; no scan-time downloads.

### Excluded

- More than five images per invocation, directory recursion, remote URLs, web uploads, or hosted inference.
- Fraud/legitimate, true/false, trustworthy/untrustworthy, or event-authenticity decisions.
- A claim that a file is “real” solely because it has camera metadata or did not trigger a detector.
- Universal detection of all generators, edits, or image processing.
- Automatic enforcement or consequential decisions.
- Broad image-format support beyond JPEG and PNG in v1.

## 6. User workflow

1. The user selects one to five local JPEG/PNG files.
2. The CLI validates the count, file type, byte size, and decoded-pixel limit before analysis.
3. For each file, the scanner computes a digest, extracts available metadata and image facts, validates embedded provenance offline, measures pixel/file signals, and runs configured local models.
4. The report separates direct observations, signed provenance validation, detector estimates, comparison coverage, and interpretation.
5. The user sees a plain-language assessment and score summary for each image, followed by evidence and limitations. A detailed JSON report can be written locally.
6. The advisory tells the user whether to inspect further. The user remains responsible for any decision beyond image-origin triage.

## 7. Assessment model

Each image receives separate outputs for:

- **AI-generation assessment:** evidence that the full image was generated synthetically.
- **AI-edit assessment:** evidence that a camera-origin or other source image contains AI-generated changes. A localization map is included only when supported and evaluated.
- **Image-origin verdict:** `likely AI-generated`, `likely AI-edited`, `likely AI-generated and edited`, `no configured AI signal crossed threshold`, or `inconclusive`.
- **Scores:** generation and editing scores remain separate. A score is a calibrated likelihood only when calibration has been measured on a documented validation population. Otherwise it is identified as a raw model score; it is never presented as a universal probability.
- **Further-inspection advisory:** `recommended`, `not indicated by configured models`, or `inconclusive`, with the signals and model coverage that produced it.

The phrase `no configured AI signal crossed threshold` means only that the configured and successfully run detectors did not trigger. It is not equivalent to “camera photo,” “authentic,” or “unedited.” Missing, unsupported, conflicting, or out-of-validation evidence must lead to `inconclusive` where it prevents a supported classification.

## 8. Reference and evaluation strategy

“Real image” is operationally defined for model development as an image with known camera-captured provenance in the reference dataset. It does not mean the depicted event is true, and it does not mean the pixels have never been conventionally edited.

The system must use a versioned, documented reference corpus with verified labels and disjoint training, calibration, and held-out test partitions. The corpus must include multiple camera makers/models and computational photography pipelines; full-image outputs from multiple modern generators; AI-edited images with original-image pairs and masks when available; and common transformations such as resizing, cropping, JPEG compression, screenshots/re-digitization, and metadata removal or modification.

Evaluation must split by camera source, generator family/version, editing tool, and source image to reduce leakage. It must report class-specific precision/recall, false-positive and false-negative rates, balanced accuracy, calibration quality, coverage/inconclusive rate, and localization metrics where applicable. Results must be broken out by transformation and relevant content groups. Thresholds are selected on calibration data under an explicit false-positive constraint and then frozen before held-out evaluation. Initial v1 targets are at least 80% sensitivity at no more than 5% false-positive rate for each supported task/domain, and expected calibration error (ECE) no greater than 0.05 before a score is called a calibrated likelihood. These are product release targets, not claims about current models. If a target is missed, keep the affected profile experimental and use `inconclusive` when a supported classification cannot be made.

No detector may be called robust based only on random train/test splits from one dataset or aggregate accuracy. If a model does not meet its documented release gate for a relevant test domain, that domain's verdict is `inconclusive` or explicitly experimental.

## 9. Success measures

- Every invocation processes between one and five selected inputs, with clear rejection outside that range.
- Every supported file receives a parseable report with digest, facts, available metadata, provenance result, diagnostics, model statuses, verdict, and advisory.
- The CLI preserves successful results when another selected file fails.
- The verdict names the evidence and model versions used; it never claims proof of authenticity or fraud.
- Independent held-out testing documents per-class and per-transformation performance, calibration, false-positive behavior, and localization quality before any robustness claim.
- Scanning performs no network access and leaves original file bytes unchanged.

## 10. Privacy, security, and trust

- Image files and reports stay on the local machine; the scanner has no network scan path.
- JSON includes all available metadata by default, including GPS and device identifiers. Users must choose a private output location.
- Terminal output shows a concise summary and escapes control characters; it does not print full sensitive metadata by default.
- Files and metadata are untrusted inputs. Parsers are bounded, decoder safeguards remain enabled, and per-file failures are isolated.
- C2PA validation runs offline. The report states that fresh online certificate revocation status was not checked.
- Model weights, model code, and reference datasets are explicit local inputs. The scanner never downloads or executes remote code at scan time.

## 11. Release gates

1. Functional criteria in [SPEC.md](SPEC.md) and [acceptance-criteria.md](docs/product/acceptance-criteria.md) pass.
2. Generation and editing tasks are evaluated independently on documented held-out sets against the initial release targets above.
3. Calibration and threshold selection are documented; raw scores are not mislabeled as probabilities.
4. The report distinguishes positive provenance, absent provenance, detector hits, detector misses, unavailable models, and inconclusive cases.
5. All user-facing materials explain the limits of AI detection, metadata, and sensor/camera signals.

## 12. Risks and mitigations

| Risk | Product mitigation |
| --- | --- |
| A model learns dataset artifacts rather than origin | Paired and source-disjoint datasets; held-out generator/camera families; post-processing stress tests. |
| Real image is called AI-generated | Threshold against a documented false-positive budget; class-specific reporting; `inconclusive` outcome. |
| AI-edited image is missed by whole-image detector | Separate edit/localization task and benchmark; never infer edit status from the generation model alone. |
| Camera-like noise falsely suggests camera origin | Treat sensor features as supporting signals; use known-source references; never use them as a standalone authenticity rule. |
| Metadata is false, stripped, or sensitive | Label it unverified, report completeness, preserve all values only in local JSON, and avoid text leakage. |
| Provenance is absent or a signed claim is misleading | Report validation and signer separately; absence is neutral; signed claims do not establish event truth. |
| Detector distribution becomes stale | Version model/data/thresholds and rerun drift and held-out evaluation before updating a verdict profile. |

## 13. Decisions and open items

### Confirmed decisions

- V1 is local and processes one to five explicit image files per invocation.
- The product returns an image-origin classification verdict, separate generation/edit scores, evidence, and a further-inspection advisory.
- The verdict is not a fraud or event-truth judgment.
- “Real” comparison means comparison to labeled camera-captured references, not universal metadata rules.
- JSON includes all available metadata by default and may contain sensitive data.

### Deferred decisions

- Exact model architectures, versions, runtime dependencies, licenses, and safe weight formats.
- The validation corpus, whether to retain or revise the initial release targets, threshold policy, and recalibration process.
- Whether RAW/TIFF/WebP/HEIC support is valuable after JPEG/PNG v1.
- Performance targets and reference hardware for single-image and five-image batches.

## 14. Traceability

The implementation contract is [SPEC.md](SPEC.md). Testable behavior is in [acceptance-criteria.md](docs/product/acceptance-criteria.md). Research findings are in [research.md](docs/product/research.md); a separate bibliography has not yet been created. Architecture must be revised to reflect this PRD before model integration begins.
