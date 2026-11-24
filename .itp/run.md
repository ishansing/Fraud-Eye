# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Plan and build the Image Evidence Scanner from PRD.md and SPEC.md"
  scale: standard
  checkpoints: phase
  next_phase: architecture
  completed: [research, align, spec]
  artifacts:
    research: docs/product/research.md
    decisions: docs/product/decisions.md
    spec: docs/product/spec.md
    acceptance_criteria: docs/product/acceptance-criteria.md
  loaded_skills: [idea-to-production, itp-research, research, itp-align, grilling, itp-spec, writing-for-agents]
  open_questions:
    - "Select local generation/edit models, runtimes, versions, and licenses."
    - "Define evaluation dataset/profile and target population."
    - "Confirm release gates after feasibility study."
    - "Set hardware and batch resource/time budget."
    - "Select bounded metadata parser stack."
  notes:
    - "Greenfield project; no implementation or architecture artifact is present."
    - "Scale is standard because initial architecture and implementation boundaries must be established."
    - "Research completed; stack options are evidence only, not decisions. See docs/product/research.md."
    - "Alignment decisions recorded in docs/product/decisions.md; specific dataset, hardware budgets, models, and final parser/runtime choices remain for feasibility/architecture."
    - "Normative SPEC.md remains the single source of requirement text; docs/product/spec.md indexes it to avoid duplicating requirements."
