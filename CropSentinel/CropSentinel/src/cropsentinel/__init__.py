"""CropSentinel reference decision logic.

This package contains a small testable reference implementation. It is not an
embedded firmware build or a trained crop-disease classifier.
"""

from .decision import DecisionAction, DecisionResult, decide
from .quality import ImageQuality, assess_image_quality

__all__ = [
    "DecisionAction",
    "DecisionResult",
    "ImageQuality",
    "assess_image_quality",
    "decide",
]
