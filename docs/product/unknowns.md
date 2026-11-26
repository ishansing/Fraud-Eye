# Open questions for the SPECv3 target

These questions remain unresolved; research may narrow options but does not approve handling real
documents, persistence, public access, model claims, or consequential use. See the [adoption
decision](decisions.md) and the [normative target and safety gates](../../SPEC.md).

## Privacy and trust

- What does “24-hour retention” mean for raw documents, derivatives, backups, crash dumps, logs,
  and SQLite rows? What deletion evidence is required? This conflicts with the target's
  “Zero-Retention” label.
- What authentication, user roles, credential lifecycle, and access model apply to the API,
  review UI, feedback endpoint, artifacts, and webhooks?
- Is the target strictly single-user/local, or does it include multiple users or tenants? The
  target mentions cross-tenant protections without defining tenants.
- Which explicit owner, privacy, security, legal, and operational approvals must precede any
  real-document handling, persistence, non-loopback exposure, or stronger verdict?

## Data, model, and evaluation

- Kriyam TamperFlow's first-party card states non-commercial terms and a separate agreement for
  commercial training; the viewer's visible row count differed from the card's stated image count.
  Reconcile the files/splits and obtain terms before any use.
- The ICDAR 2023 “Find it again!” receipt dataset is identifiable from the first-party page, but
  license and split/source grouping are unstated there.
- DocTamper's dataset is non-commercial, restricted-access, and does not cover AIGC text tampering;
  model-code/weight terms need direct clarification.
- Are these datasets accessible under terms suitable for the intended evaluation and distribution?
- Which population, document languages, capture conditions, and ground-truth process define the
  target evaluation cohorts? Are training, calibration, and held-out sets source-disjoint?
- Which exact parser/model/scorer versions and artifact licenses are acceptable? Candidate names
  in SPECv3 are not a validated or approved stack.
- What evidence will validate pHash reuse thresholds, small-area localization, score calibration,
  and operating cutoffs against false positives and subgroup performance?

## Runtime and operations

- Which supported OS, Python, CUDA/cuDNN, GPU, and CPU configurations define the target hardware
  and fallback contract?
- What measured limits apply to PDF object depth, image dimensions, timeouts, memory, concurrency,
  model warm-up, worker queueing, and cleanup after process termination?
- What webhook destination policy, signing key handling, retry schedule, and SSRF protections are
  required?

Until resolved, the current service remains a loopback-only synthetic PNG prototype: memory-only
and always `INCONCLUSIVE`.
