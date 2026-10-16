"""Cross-validation split module grouped by prompt_id."""

from typing import Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold, GroupKFold


def get_group_kfold_splits(
    df: pd.DataFrame,
    group_col: str = "prompt_id",
    target_col: Optional[str] = "model",
    n_splits: int = 5,
    seed: int = 42,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates cross-validation splits strictly grouped by prompt_id.

    Ensures zero prompt leakage between training and validation splits.
    Uses StratifiedGroupKFold when target_col is present to maintain balanced
    model representations across folds.

    Args:
        df: DataFrame containing the dataset.
        group_col: Column name to group splits on (default: 'prompt_id').
        target_col: Target column for stratification if present (default: 'model').
        n_splits: Number of cross-validation folds (default: 5).
        seed: Random seed for reproducible shuffling (default: 42).

    Returns:
        List of (train_indices, val_indices) numpy array tuples.

    Raises:
        ValueError: If group_col is missing from DataFrame.
    """
    if group_col not in df.columns:
        raise ValueError(f"Group column '{group_col}' not found in DataFrame.")

    groups = df[group_col].to_numpy()
    X = np.zeros(len(df))  # Dummy features for index generation

    if target_col and target_col in df.columns:
        y = df[target_col].to_numpy()
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        splits = list(splitter.split(X, y, groups=groups))
    else:
        splitter = GroupKFold(n_splits=n_splits)
        splits = list(splitter.split(X, groups=groups))

    return splits
