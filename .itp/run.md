# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Plan and build the Image Evidence Scanner from PRD.md and SPEC.md"
  scale: standard
  checkpoints: phase
  next_phase: align
  completed: [research, align, spec, architecture, slice]
  active_phase: align
  artifacts:
    research: docs/product/research.md
    decisions: docs/product/decisions.md
    spec: docs/product/spec.md
    acceptance_criteria: docs/product/acceptance-criteria.md
    architecture: docs/architecture/architecture.md
    adrs:
      - docs/architecture/ADR/0001-python-local-cli.md
      - docs/architecture/ADR/0002-bounded-local-processing.md
      - docs/architecture/ADR/0003-task-profile-verdict-gates.md
    threat_model: docs/architecture/epics-threat-model.md
    slices:
      - docs/work/ISSUE-001.md
      - docs/work/ISSUE-002.md
      - docs/work/ISSUE-003.md
      - docs/work/ISSUE-004.md
      - docs/work/ISSUE-005.md
      - docs/work/ISSUE-006.md
  loaded_skills: [idea-to-production, itp-research, research, itp-align, grilling, itp-spec, writing-for-agents, itp-architecture, codebase-design, security-threat-model, itp-slice]
  open_questions:
    - "Select local generation/edit models, runtimes, versions, and licenses."
    - "Select evaluation corpus/release, label provenance, and split design for the consumer-image population."
    - "Confirm release gates after feasibility study."
    - "Set hardware and batch resource/time budget."
  handoff:
    status: needs-human
    reason: "Feasibility research recommends an evaluation spike but establishes no model, dataset, artifact rights, or release-gate pass."
    decision: "Approve next step for ISSUE-006 feasibility"
    options:
      - "Authorize bounded candidate evaluation (recommended; no production model approval)"
      - "Keep v1 evidence-only and defer model work"
    affected_artifacts:
      - docs/product/research.md
      - docs/product/decisions.md
      - docs/work/ISSUE-006.md
      - https://github.com/ishansing/Fraud-Eye/issues/1
    resume_with: itp-align
  notes:
    - "Implementation checkpoints committed as 0a0f8cb, e14156b, and 94f2a0f. Review approved the implementation checkpoint for verification; see docs/work/review.md."
    - "The tracker was configured locally before a remote was available; GitHub Issues are now authoritative. Active ISSUE-006 is GitHub #1; completed slices remain local historical specifications."
    - "Owner selected the consumer-image target population, authorized feasibility research/proposal, and chose this Ryzen 9 5900HS / 16 GB / RTX 3060 6 GB machine as a measurement baseline; feasibility findings are in docs/product/research.md, but no model/profile is approved."
    - "C2PA report-size limit is checked after the SDK materializes its manifest; no OS worker memory ceiling is set pending resource-budget decisions."
    - "Verification is blocked for full product completion; evidence is in docs/work/verification.md. The local scanner checkpoint passed its current checks."
    - "Scale is standard because initial architecture and implementation boundaries must be established."
    - "Research completed; stack options are evidence only, not decisions. See docs/product/research.md."
    - "Alignment decisions recorded in docs/product/decisions.md; ExifTool and c2pa-python are selected runtime dependencies. Dataset, hardware budgets, models, and resource limits remain human decisions."
    - "Normative SPEC.md remains the single source of requirement text; docs/product/spec.md indexes it to avoid duplicating requirements."
    - "The initial architecture and threat model informed implemented local input, parser, output, and offline controls; the latest implementation still needs review and verification."
    - "Slices are ordered bootstrap -> bounded scan/report -> metadata/provenance -> forensic signals -> verdict contract -> evaluated model release. ISSUE-006 is gated on human-approved model/data/license/hardware choices."
