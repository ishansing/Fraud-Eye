# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Plan and build the Fraud Netra synthetic-data prototype from SPECv2.md"
  scale: standard
  checkpoints: phase
  next_phase: architecture
  completed: [align, spec]
  active_phase: architecture
  artifacts:
    research: docs/product/research.md
    decisions: docs/product/decisions.md
    spec: docs/product/spec.md
    acceptance_criteria: docs/product/acceptance-criteria.md
    architecture: docs/architecture/architecture.md
    adrs: []
    threat_model: docs/architecture/epics-threat-model.md
    slices:
      - docs/work/ISSUE-007.md
  loaded_skills: [idea-to-production, itp-align, grilling, domain-modeling, itp-spec, writing-for-agents, itp-architecture, codebase-design, security-threat-model]
  open_questions:
    - "Choose the local API framework and bounded parsers for the prototype."
    - "Select the first document type, synthetic fixture format, and parser limits for the vertical slice."
    - "Define later security/privacy/legal gates before real documents or external deployment."
  notes:
    - "Image Evidence Scanner implementation, issue slices, architecture, research, review, and verification are historical; see git history and the marked historical artifacts."
    - "Owner approved Fraud Netra direction with a local-only, synthetic-data, in-memory prototype; screening only; inconclusive until evaluation gates pass."
    - "Heatmap URLs are deferred for the prototype. Webhooks, review console, Kubernetes/GPU deployment, and real-document handling are later phases."
    - "GitHub Issues are authoritative. Former image-scanner issue #1 is closed as superseded; Fraud Netra architecture is tracked in #2."
    - "The supplied SPECv2.md is retained unchanged as source input; PRD.md, SPEC.md, and acceptance criteria now reflect owner-approved prototype limits."
    - "Fraud Netra-specific external research was not needed to settle scope; technical library/runtime choices remain open for architecture."
    - "Old scanner ADRs are not architecture decisions for Fraud Netra; new ADRs will be recorded during ISSUE-007."
