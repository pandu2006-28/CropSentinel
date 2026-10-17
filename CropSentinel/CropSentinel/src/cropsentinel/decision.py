"""Trust-aware decision policy scaffold for CropSentinel.

Predictions passed to this module must come from an actual classifier. The
project's demo values are synthetic. Thresholds must be selected using
representative, labelled field data before any deployment.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .quality import ImageQuality


class DecisionAction(str, Enum):
    RECAPTURE = "recapture"
    HUMAN_REVIEW = "human_review"
    POSSIBLE_DISEASE_ALERT = "possible_disease_alert"
    HEALTHY_CLASS_PREDICTED = "healthy_class_predicted"
    INVALID_INPUT = "invalid_input"


@dataclass(frozen=True)
class DecisionResult:
    action: DecisionAction
    predicted_class: str | None
    top_confidence: float | None
    confidence_margin: float | None
    reasons: tuple[str, ...]
    disclaimer: str = (
        "Model output is not a definitive diagnosis; inspect the plant and use "
        "authoritative crop-specific guidance."
    )


def decide(
    predictions: Mapping[str, float],
    image_quality: ImageQuality,
    *,
    min_confidence: float = 0.80,
    min_margin: float = 0.20,
    healthy_label: str = "healthy",
) -> DecisionResult:
    """Choose whether to recapture, defer, or issue a possible-disease alert.

    This reference policy:
    - recaptures if the image quality gate failed;
    - rejects empty, non-finite, negative, or out-of-range probabilities;
    - defers uncertain/ambiguous predictions for human review;
    - uses 'possible disease' for high-confidence non-healthy classes;
    - describes a healthy-class result only as a model prediction, not proof
      that the crop is free of disease.
    """
    if not image_quality.usable:
        return DecisionResult(
            action=DecisionAction.RECAPTURE,
            predicted_class=None,
            top_confidence=None,
            confidence_margin=None,
            reasons=("image_quality_failed", *image_quality.reasons),
        )

    if not predictions:
        return DecisionResult(
            action=DecisionAction.INVALID_INPUT,
            predicted_class=None,
            top_confidence=None,
            confidence_margin=None,
            reasons=("no_model_predictions",),
        )

    cleaned: list[tuple[str, float]] = []
    for label, value in predictions.items():
        if not isinstance(label, str) or not label.strip():
            return DecisionResult(
                DecisionAction.INVALID_INPUT, None, None, None, ("invalid_class_label",)
            )
        if not isinstance(value, (int, float)) or not 0.0 <= float(value) <= 1.0:
            return DecisionResult(
                DecisionAction.INVALID_INPUT, None, None, None, ("invalid_probability",)
            )
        cleaned.append((label, float(value)))

    ranked = sorted(cleaned, key=lambda item: item[1], reverse=True)
    top_label, top_conf = ranked[0]
    second_conf = ranked[1][1] if len(ranked) > 1 else 0.0
    margin = top_conf - second_conf

    if top_conf < min_confidence or margin < min_margin:
        return DecisionResult(
            action=DecisionAction.HUMAN_REVIEW,
            predicted_class=top_label,
            top_confidence=top_conf,
            confidence_margin=margin,
            reasons=("confidence_or_class_margin_below_threshold",),
        )

    if top_label.strip().lower() == healthy_label.strip().lower():
        return DecisionResult(
            action=DecisionAction.HEALTHY_CLASS_PREDICTED,
            predicted_class=top_label,
            top_confidence=top_conf,
            confidence_margin=margin,
            reasons=("classifier_predicted_healthy_class_only",),
        )

    return DecisionResult(
        action=DecisionAction.POSSIBLE_DISEASE_ALERT,
        predicted_class=top_label,
        top_confidence=top_conf,
        confidence_margin=margin,
        reasons=("high_confidence_non_healthy_class_requires_confirmation",),
    )
