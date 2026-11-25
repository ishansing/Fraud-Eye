def assess() -> dict:
    reason = "No validated model profile is configured."
    task = {
        "status": "unconfigured",
        "detector": None,
        "model_artifact": None,
        "profile": None,
        "score": None,
        "score_semantics": "not_available",
        "threshold": None,
        "threshold_provenance": None,
        "calibration": None,
        "tested_population": None,
        "decision": "inconclusive",
        "limitations": [reason],
        "reasons": [reason],
    }
    return {
        "generation": task.copy(),
        "editing": task.copy(),
        "verdict": "inconclusive",
        "interpretation": (
            "No validated model profile is configured; no AI-origin conclusion is available."
        ),
        "evidence_references": [],
        "advisory": "inconclusive",
        "advisory_scope": reason,
    }
