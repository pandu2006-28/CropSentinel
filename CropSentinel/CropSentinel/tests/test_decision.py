from cropsentinel import assess_image_quality, decide
from cropsentinel.decision import DecisionAction


def good_quality():
    return assess_image_quality(
        blur_score=0.85,
        exposure_fraction=0.92,
        occlusion_fraction=0.02,
    )


def test_bad_image_requests_recapture():
    poor = assess_image_quality(
        blur_score=0.1,
        exposure_fraction=0.5,
        occlusion_fraction=0.4,
    )
    result = decide({"early_blight": 0.99, "healthy": 0.01}, poor)
    assert result.action == DecisionAction.RECAPTURE


def test_uncertain_prediction_defers_to_human():
    result = decide({"healthy": 0.48, "early_blight": 0.45, "late_blight": 0.07}, good_quality())
    assert result.action == DecisionAction.HUMAN_REVIEW


def test_confident_nonhealthy_prediction_is_possible_disease_alert():
    result = decide({"healthy": 0.05, "early_blight": 0.88, "late_blight": 0.07}, good_quality())
    assert result.action == DecisionAction.POSSIBLE_DISEASE_ALERT
    assert result.predicted_class == "early_blight"


def test_healthy_class_is_not_described_as_proof_of_health():
    result = decide({"healthy": 0.92, "early_blight": 0.05, "late_blight": 0.03}, good_quality())
    assert result.action == DecisionAction.HEALTHY_CLASS_PREDICTED
    assert "not a definitive diagnosis" in result.disclaimer


def test_missing_predictions_is_invalid():
    result = decide({}, good_quality())
    assert result.action == DecisionAction.INVALID_INPUT
