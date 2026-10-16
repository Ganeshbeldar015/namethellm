import pytest
import numpy as np
import pandas as pd

from namethellm import data
from namethellm.models.baseline import BaselineTFIDFClassifier
from namethellm.evaluate import run_group_kfold_evaluation


def test_baseline_classifier_fit_predict():
    """BaselineTFIDFClassifier fits on text and outputs valid predictions."""
    train_texts = [
        "This is an analytical explanation of quantum entanglement.",
        "A lyrical prose discussing the metaphysical horizons of being.",
        "Here is a Python function implementing quicksort efficiently.",
    ]
    train_labels = ["gpt-5.5", "claude-opus-5", "gemini-3.8-flash"]

    clf = BaselineTFIDFClassifier(random_state=42)
    clf.fit(train_texts, train_labels)

    test_texts = ["A short paragraph discussing quantum mechanics."]
    preds = clf.predict(test_texts)
    assert len(preds) == 1
    assert preds[0] in train_labels

    probas = clf.predict_proba(test_texts)
    assert probas.shape == (1, 3)
    assert pytest.approx(np.sum(probas[0]), abs=1e-5) == 1.0


def test_group_kfold_evaluation_exceeds_random_guess():
    """AC-005-a: Out-of-fold balanced accuracy strictly exceeds random guess (0.0555)."""
    df = data.load_train_data()

    # Fast 5-fold evaluation with baseline model
    results = run_group_kfold_evaluation(df, n_splits=5, seed=42)

    oof_score = results["oof_balanced_accuracy"]
    oof_preds = results["oof_predictions"]

    assert len(oof_preds) == len(df)
    assert pd.Series(oof_preds).isnull().sum() == 0

    # Strict check: must exceed random guess (0.0555) by at least 2.5x (> 0.15)
    assert oof_score > 0.15, f"OOF score {oof_score} does not exceed threshold 0.15"
    assert "per_class_recall" in results
    assert len(results["per_class_recall"]) == 18
