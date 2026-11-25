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
    - "Implementation checkpoint committed as 0a0f8cb. Review is blocked because required docs/agents/issue-tracker.md is missing; resume review after tracker setup."
    - "ISSUE-006 remains gated on human model/profile/resource decisions."
    - "Scale is standard because initial architecture and implementation boundaries must be established."
    - "Research completed; stack options are evidence only, not decisions. See docs/product/research.md."
    - "Alignment decisions recorded in docs/product/decisions.md; ExifTool and c2pa-python are selected runtime dependencies. Dataset, hardware budgets, models, and resource limits remain human decisions."
    - "Normative SPEC.md remains the single source of requirement text; docs/product/spec.md indexes it to avoid duplicating requirements."
    - "Initial architecture and threat model are design-only; no runtime code or security control is implemented. Local Markdown links resolve and git diff --check is clean."
    - "Slices are ordered bootstrap -> bounded scan/report -> metadata/provenance -> forensic signals -> verdict contract -> evaluated model release. ISSUE-006 is gated on human-approved model/data/license/hardware choices."
