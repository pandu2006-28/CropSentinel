"""Image-quality gate using externally calculated metrics.

This module deliberately does not calculate blur/exposure/occlusion from an image.
Those metrics must be computed by a camera pipeline and calibrated with real data.
The thresholds below are illustrative defaults, not validated field thresholds.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageQuality:
    usable: bool
    reasons: tuple[str, ...]
    blur_score: float
    exposure_fraction: float
    occlusion_fraction: float


def assess_image_quality(
    *,
    blur_score: float,
    exposure_fraction: float,
    occlusion_fraction: float,
    min_blur_score: float = 0.35,
    min_exposure_fraction: float = 0.80,
    max_exposure_fraction: float = 0.995,
    max_occlusion_fraction: float = 0.20,
) -> ImageQuality:
    """Apply simple range checks to metrics supplied by another component.

    Expected normalized ranges:
      - blur_score: 0.0 (very blurry) through 1.0 (sharp)
      - exposure_fraction: proportion of pixels in a usable exposure band
      - occlusion_fraction: estimated share of the leaf region that is obscured
    """
    vals = {
        "blur_score": blur_score,
        "exposure_fraction": exposure_fraction,
        "occlusion_fraction": occlusion_fraction,
    }
    for name, value in vals.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0.0 and 1.0")

    reasons: list[str] = []
    if blur_score < min_blur_score:
        reasons.append("blur_below_threshold")
    if exposure_fraction < min_exposure_fraction:
        reasons.append("underexposed_or_low_contrast")
    if exposure_fraction > max_exposure_fraction:
        reasons.append("overexposed")
    if occlusion_fraction > max_occlusion_fraction:
        reasons.append("leaf_region_obstructed")

    return ImageQuality(
        usable=not reasons,
        reasons=tuple(reasons),
        blur_score=blur_score,
        exposure_fraction=exposure_fraction,
        occlusion_fraction=occlusion_fraction,
    )
