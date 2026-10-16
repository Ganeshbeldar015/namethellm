import pytest
import numpy as np
from sklearn.metrics import balanced_accuracy_score

from namethellm.metrics import compute_balanced_accuracy, compute_per_class_recall
from namethellm.constants import VALID_MODELS


def test_balanced_accuracy_matches_sklearn():
    """AC-003-a: Balanced accuracy matches sklearn implementation."""
    np.random.seed(42)
    y_true = np.random.choice(VALID_MODELS, size=500)
    y_pred = np.random.choice(VALID_MODELS, size=500)

    score = compute_balanced_accuracy(y_true, y_pred)
    expected_score = balanced_accuracy_score(y_true, y_pred)

    assert pytest.approx(score, abs=1e-6) == expected_score


def test_per_class_recall_matches_mean_balanced_accuracy():
    """AC-003-a: Arithmetic mean of per-class recall equals balanced accuracy."""
    np.random.seed(42)
    y_true = np.random.choice(VALID_MODELS, size=500)
    y_pred = np.random.choice(VALID_MODELS, size=500)

    per_class = compute_per_class_recall(y_true, y_pred, labels=VALID_MODELS)
    assert len(per_class) == len(VALID_MODELS)
    assert set(per_class.keys()) == set(VALID_MODELS)

    mean_recall = np.mean(list(per_class.values()))
    score = compute_balanced_accuracy(y_true, y_pred, labels=VALID_MODELS)

    assert pytest.approx(mean_recall, abs=1e-6) == score


def test_perfect_accuracy():
    """Perfect prediction yields 1.0 balanced accuracy."""
    y_true = VALID_MODELS * 10
    y_pred = list(y_true)

    score = compute_balanced_accuracy(y_true, y_pred)
    assert pytest.approx(score, abs=1e-6) == 1.0


def test_zero_recall_no_division_error():
    """Class with zero correct predictions yields 0.0 recall without error."""
    y_true = ["gpt-5.5"] * 10 + ["gemini-3.8-flash"] * 10
    # Predict everything as gpt-5.5
    y_pred = ["gpt-5.5"] * 20

    per_class = compute_per_class_recall(y_true, y_pred, labels=["gpt-5.5", "gemini-3.8-flash"])
    assert per_class["gpt-5.5"] == 1.0
    assert per_class["gemini-3.8-flash"] == 0.0
    assert compute_balanced_accuracy(y_true, y_pred, labels=["gpt-5.5", "gemini-3.8-flash"]) == 0.5
