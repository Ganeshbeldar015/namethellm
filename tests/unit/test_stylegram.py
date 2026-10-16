"""Unit tests for StylegramClassifier (AC-005-a)."""

import numpy as np
import pytest

from namethellm.constants import VALID_MODELS
from namethellm.models.stylegram import StylegramClassifier


@pytest.fixture
def synthetic_corpus() -> tuple[list[str], list[str]]:
    """Synthesize text samples across all 18 classes."""
    texts = []
    labels = []
    for i, model in enumerate(VALID_MODELS):
        texts.append(f"Passage {i} by {model}. In the beginning, however, it unfolded.")
        texts.append(f"# Section {i}\n- Detail 1\n- Detail 2\n`code block`")
        texts.append(f"Short narrative {i}: 'Indeed,' delve into the mysterious tapestry; moreover...")
        labels.extend([model, model, model])
    return texts, labels


def test_stylegram_classifier_fit_predict(synthetic_corpus: tuple[list[str], list[str]]):
    """AC-005-a: StylegramClassifier fits, predicts valid labels, and outputs valid probabilities."""
    texts, labels = synthetic_corpus
    clf = StylegramClassifier(random_state=42)
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
