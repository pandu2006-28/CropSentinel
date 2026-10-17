#!/usr/bin/env python3
"""Run a synthetic demonstration of CropSentinel reference decision logic."""

from cropsentinel import assess_image_quality, decide


def main() -> None:
    quality = assess_image_quality(
        blur_score=0.82,
        exposure_fraction=0.91,
        occlusion_fraction=0.04,
    )
    # Synthetic scores only; these are not predictions from a trained model.
    simulated_scores = {
        "healthy": 0.08,
        "early_blight": 0.86,
        "late_blight": 0.06,
    }
    result = decide(simulated_scores, quality)
    print("CropSentinel synthetic demo — NOT a field test")
    print(f"Image-quality gate passed: {quality.usable}")
    print(f"Decision: {result.action.value}")
    print(f"Simulated predicted class: {result.predicted_class}")
    print(f"Simulated top confidence: {result.top_confidence}")
    print(f"Reasons: {', '.join(result.reasons)}")
    print(f"Disclaimer: {result.disclaimer}")


if __name__ == "__main__":
    main()
