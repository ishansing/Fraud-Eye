# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Plan and build the Fraud Netra synthetic-data prototype from SPECv2.md"
  scale: standard
  checkpoints: phase
  next_phase: implement
  completed: [align, spec, architecture, slice]
  active_phase: implement
  artifacts:
    research: docs/product/research.md
    decisions: docs/product/decisions.md
    spec: docs/product/spec.md
    acceptance_criteria: docs/product/acceptance-criteria.md
    architecture: docs/architecture/architecture.md
    adrs:
      - docs/architecture/ADR/0004-loopback-png-prototype.md
    threat_model: docs/architecture/epics-threat-model.md
    slices:
      - docs/work/ISSUE-007.md
      - docs/work/ISSUE-008.md
  loaded_skills: [idea-to-production, itp-align, grilling, domain-modeling, itp-spec, writing-for-agents, itp-architecture, codebase-design, security-threat-model, itp-slice, itp-implement, tdd]
  open_questions:
    - "Define later security/privacy/legal gates before real documents or external deployment."
  notes:
    - "Image Evidence Scanner implementation, issue slices, architecture, research, review, and verification are historical; see git history and the marked historical artifacts."
    - "Owner approved Fraud Netra direction with a local-only, synthetic-data, in-memory prototype; screening only; inconclusive until evaluation gates pass."
    - "Heatmap URLs are deferred for the prototype. Webhooks, review console, Kubernetes/GPU deployment, and real-document handling are later phases."
    - "GitHub Issues are authoritative. Former image-scanner issue #1 is closed as superseded; Fraud Netra architecture is tracked in #2."
    - "SPECv2.md remains the supplied source proposal; canonical docs reflect owner-approved prototype limits."
    - "Fraud Netra-specific external research was not needed to settle scope; technical library/runtime choices remain open for architecture."
    - "Old scanner ADRs are not architecture decisions for Fraud Netra; new ADRs will be recorded during ISSUE-007."
    - "The first implementation is a loopback-only PNG endpoint; it does not verify that caller data is synthetic and cannot be exposed publicly."
