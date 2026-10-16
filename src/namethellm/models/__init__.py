"""Models package for Name That LLM."""

from namethellm.models.baseline import BaselineTFIDFClassifier
from namethellm.models.hybrid import HybridStyloClassifier

__all__ = ["BaselineTFIDFClassifier", "HybridStyloClassifier"]

