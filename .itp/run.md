# Installation preference, not a completed lifecycle. Root sets goal and scale.
run:
  goal: "Build the Fraud Netra local prototype toward the adopted SPECv3 hybrid-MVP target"
  scale: standard
  checkpoints: phase
  next_phase: align
  completed: [align, spec]
  active_phase: align
  artifacts:
    research: docs/product/research.md
    decisions: docs/product/decisions.md
    spec: docs/product/spec.md
    acceptance_criteria: docs/product/acceptance-criteria.md
    unknowns: docs/product/unknowns.md
    source_spec: SPECv3.md
    architecture: docs/architecture/architecture.md
    adrs:
      - docs/architecture/ADR/0004-loopback-png-prototype.md
    threat_model: docs/architecture/epics-threat-model.md
    slices:
      - docs/work/ISSUE-007.md
      - docs/work/ISSUE-008.md
  loaded_skills: [idea-to-production, itp-align, grilling, domain-modeling, itp-spec, writing-for-agents, itp-research, research]
  open_questions:
    - "Resolve or explicitly defer target retention semantics, authentication, evaluation data provenance, parser/model choices, and supported resource budgets before target architecture or implementation."
    - "Re-scope authoritative GitHub architecture tracking from the completed prototype architecture to the adopted SPECv3 target before implementation slices are created."
  notes:
    - "Image Evidence Scanner implementation, issue slices, architecture, research, review, and verification are historical; see git history and the marked historical artifacts."
    - "SPECv3 is adopted as a long-term target only. The current API remains loopback-only, synthetic PNG-only, memory-only, and INCONCLUSIVE."
    - "Heatmap URLs are deferred for the prototype. Webhooks, review console, Kubernetes/GPU deployment, and real-document handling are later phases."
    - "GitHub Issues are authoritative. Former image-scanner issue #1 is closed as superseded; Fraud Netra architecture is tracked in #2."
    - "SPECv2.md and SPECv3.md are retained source proposals; SPEC.md adapts the current target under the preserved safety gates."
    - "The first loopback API implementation does not verify that caller data is synthetic and must not be exposed publicly."
