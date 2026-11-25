from image_evidence_scanner.assessment import assess


def test_unconfigured_profile_produces_separate_inconclusive_task_records():
    result = assess()

    assert result["verdict"] == "inconclusive"
    assert result["advisory"] == "inconclusive"
    assert result["generation"]["decision"] == "inconclusive"
    assert result["editing"]["decision"] == "inconclusive"
    assert result["generation"]["score_semantics"] == "not_available"
    assert result["editing"]["score_semantics"] == "not_available"
    assert "profile is configured" in result["generation"]["reasons"][0]
    assert "profile is configured" in result["editing"]["reasons"][0]


def test_unconfigured_profile_does_not_claim_no_trigger_advisory():
    result = assess()

    assert result["advisory"] != "not_indicated_by_configured_models"
    assert result["interpretation"] == (
        "No validated model profile is configured; no AI-origin conclusion is available."
    )
