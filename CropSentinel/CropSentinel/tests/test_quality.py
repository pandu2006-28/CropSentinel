import pytest

from cropsentinel.quality import assess_image_quality


def test_good_quality_passes():
    result = assess_image_quality(
        blur_score=0.8,
        exposure_fraction=0.9,
        occlusion_fraction=0.05,
    )
    assert result.usable is True
    assert result.reasons == ()


def test_blurry_image_fails():
    result = assess_image_quality(
        blur_score=0.1,
        exposure_fraction=0.9,
        occlusion_fraction=0.05,
    )
    assert result.usable is False
    assert "blur_below_threshold" in result.reasons


def test_metric_outside_normalized_range_raises():
    with pytest.raises(ValueError):
        assess_image_quality(
            blur_score=1.2,
            exposure_fraction=0.9,
            occlusion_fraction=0.05,
        )
