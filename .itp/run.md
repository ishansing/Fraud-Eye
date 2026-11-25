# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Plan and build the Image Evidence Scanner from PRD.md and SPEC.md"
  scale: standard
  checkpoints: phase
  next_phase: review
  completed: [research, align, spec, architecture, slice]
  active_phase: review
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
    - "Define evaluation dataset/profile and target population."
    - "Confirm release gates after feasibility study."
    - "Set hardware and batch resource/time budget."
  notes:
    - "Implementation checkpoints committed as 0a0f8cb and e14156b. Review findings for depth bounds, PNG/JPEG structure reporting, dual-stack CI blocking, verdict documentation, output profile/limitations, color-space metadata, and signal prerequisites were addressed; re-review the latest commit."
    - "Local issue tracker configuration recorded in docs/agents/issue-tracker.md; no remote was available, so no external tracker was inferred."
    - "ISSUE-006 remains gated on human model/profile/resource decisions."
    - "C2PA report-size limit is checked after the SDK materializes its manifest; no OS worker memory ceiling is set pending resource-budget decisions."
    - "Scale is standard because initial architecture and implementation boundaries must be established."
    - "Research completed; stack options are evidence only, not decisions. See docs/product/research.md."
    - "Alignment decisions recorded in docs/product/decisions.md; ExifTool and c2pa-python are selected runtime dependencies. Dataset, hardware budgets, models, and resource limits remain human decisions."
    - "Normative SPEC.md remains the single source of requirement text; docs/product/spec.md indexes it to avoid duplicating requirements."
    - "The initial architecture and threat model informed implemented local input, parser, output, and offline controls; the latest implementation still needs review and verification."
    - "Slices are ordered bootstrap -> bounded scan/report -> metadata/provenance -> forensic signals -> verdict contract -> evaluated model release. ISSUE-006 is gated on human-approved model/data/license/hardware choices."
