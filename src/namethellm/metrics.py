"""Competition evaluation metrics and per-class recall analysis."""

from typing import Optional, Sequence, Union
import numpy as np
import pandas as pd
from sklearn.metrics import recall_score, balanced_accuracy_score


def compute_per_class_recall(
    y_true: Union[Sequence, np.ndarray, pd.Series],
    y_pred: Union[Sequence, np.ndarray, pd.Series],
    labels: Optional[Sequence[str]] = None,
) -> dict[str, float]:
    """Calculates per-class recall (sensitivity) for each candidate class.

    Args:
        y_true: Ground truth target labels.
        y_pred: Predicted class labels.
        labels: Optional ordered sequence of target labels. If None, unique sorted
                labels from y_true are used.

    Returns:
        Dictionary mapping class label to its sensitivity in [0.0, 1.0].
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)

    if labels is None:
        target_labels = np.unique(y_true_arr)
    else:
        target_labels = np.asarray(labels)

    recalls = recall_score(
        y_true_arr,
        y_pred_arr,
        labels=target_labels,
        average=None,
        zero_division=0.0,
    )

    return {str(label): float(recall) for label, recall in zip(target_labels, recalls)}


def compute_balanced_accuracy(
    y_true: Union[Sequence, np.ndarray, pd.Series],
    y_pred: Union[Sequence, np.ndarray, pd.Series],
    labels: Optional[Sequence[str]] = None,
) -> float:
    """Calculates macro-averaged balanced accuracy.

    Formula: (1 / K) * sum(recall_i for i in 1..K)

    Args:
        y_true: Ground truth target labels.
        y_pred: Predicted class labels.
        labels: Optional sequence of target labels to include in the macro average.

    Returns:
        Balanced accuracy score in [0.0, 1.0].
    """
    if labels is not None:
        per_class = compute_per_class_recall(y_true, y_pred, labels=labels)
        return float(np.mean(list(per_class.values())))

    return float(balanced_accuracy_score(y_true, y_pred))
