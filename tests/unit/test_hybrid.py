"""Unit tests for HybridStyloClassifier and BalancedAccuracyCalibrator (AC-005-a, AC-006-a)."""

import numpy as np
import pytest
from sklearn.metrics import balanced_accuracy_score

from namethellm.constants import VALID_MODELS
from namethellm.models.hybrid import HybridStyloClassifier
from namethellm.postprocess import BalancedAccuracyCalibrator


@pytest.fixture
def synthetic_data() -> tuple[list[str], list[str]]:
    """Synthesize text samples across all 18 classes with distinct stylometric markers."""
    texts = []
    labels = []
    for i, model in enumerate(VALID_MODELS):
        # 3 samples per class with distinctive patterns
        texts.append(f"Standard passage {i} by {model} with some sentences. Furthermore, crucial details.")
        texts.append(f"# Heading {i}\n- Bullet point one\n- Bullet point two\n`code snippet`")
        texts.append(f"Short dialogue: 'Indeed,' delve into the tapestry; moreover... {i}")
        labels.extend([model, model, model])
    return texts, labels


def test_hybrid_stylo_classifier_fit_predict(synthetic_data: tuple[list[str], list[str]]):
    """AC-005-a: HybridStyloClassifier fits, predicts valid labels, and outputs valid probabilities."""
    texts, labels = synthetic_data
    clf = HybridStyloClassifier(random_state=42)
    clf.fit(texts, labels)

    assert hasattr(clf, "classes_")
    assert len(clf.classes_) == 18

    # Predict
    preds = clf.predict(texts[:5])
    assert len(preds) == 5
    assert all(p in VALID_MODELS for p in preds)

    # Predict proba
    probs = clf.predict_proba(texts[:5])
    assert probs.shape == (5, 18)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)
    row_sums = probs.sum(axis=1)
    np.testing.assert_allclose(row_sums, 1.0, atol=1e-5)


def test_calibrator_properties():
    """AC-006-a: BalancedAccuracyCalibrator preserves probability axioms and does not decrease metric."""
    np.random.seed(42)
    n_samples = 200
    n_classes = 18

    # Create synthetic true labels (uniform across classes)
    y_true = np.random.choice(n_classes, size=n_samples)

    # Create synthetic predictions that are biased towards class 0
    logits = np.random.randn(n_samples, n_classes)
    logits[:, 0] += 1.5  # overpredict class 0
    exp_logits = np.exp(logits)
    probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)

    raw_preds = np.argmax(probs, axis=1)
    raw_score = balanced_accuracy_score(y_true, raw_preds)

    calibrator = BalancedAccuracyCalibrator(gamma=0.2)
    calibrator.fit(probs)
    calibrated_probs = calibrator.calibrate(probs)

    # Probability axioms
    assert calibrated_probs.shape == probs.shape
    assert np.all(calibrated_probs >= 0.0)
    np.testing.assert_allclose(calibrated_probs.sum(axis=1), 1.0, atol=1e-5)

    calibrated_preds = calibrator.predict(probs)
    calibrated_score = balanced_accuracy_score(y_true, calibrated_preds)

    # AC-006-a: Balanced accuracy must not decrease
    assert calibrated_score >= raw_score


def test_calibrator_neutral_on_balanced():
    """AC-006-a: Calibrator with gamma=0 leaves probabilities unchanged."""
    probs = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]])
    calibrator = BalancedAccuracyCalibrator(gamma=0.0)
    calibrator.fit(probs)
    calibrated = calibrator.calibrate(probs)
    np.testing.assert_allclose(calibrated, probs, atol=1e-6)
