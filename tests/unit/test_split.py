import pytest
import pandas as pd
import numpy as np

from namethellm import data
from namethellm import split


def test_group_kfold_no_prompt_leakage():
    """AC-002-a: Train and validation prompt_ids must be strictly disjoint for every fold."""
    df = data.load_train_data()
    splits = split.get_group_kfold_splits(df, group_col="prompt_id", n_splits=5, seed=42)
    assert len(splits) == 5

    for fold_idx, (train_idx, val_idx) in enumerate(splits):
        train_prompts = set(df.iloc[train_idx]["prompt_id"])
        val_prompts = set(df.iloc[val_idx]["prompt_id"])

        intersection = train_prompts.intersection(val_prompts)
        assert len(intersection) == 0, f"Fold {fold_idx} has prompt leakage: {intersection}"


def test_group_kfold_covers_all_samples():
    """AC-002-a: Union of all validation splits covers exactly all dataset rows with no duplicates."""
    df = data.load_train_data()
    splits = split.get_group_kfold_splits(df, group_col="prompt_id", n_splits=5, seed=42)

    val_indices = []
    for _, val_idx in splits:
        val_indices.extend(val_idx)

    assert len(val_indices) == len(df)
    assert len(set(val_indices)) == len(df)


def test_group_kfold_all_classes_present():
    """AC-002-b: Every validation fold contains samples from all 18 models."""
    df = data.load_train_data()
    splits = split.get_group_kfold_splits(df, group_col="prompt_id", n_splits=5, seed=42)

    for fold_idx, (_, val_idx) in enumerate(splits):
        val_models = set(df.iloc[val_idx]["model"])
        assert len(val_models) == 18, f"Fold {fold_idx} has only {len(val_models)}/18 models"


def test_split_deterministic_with_seed():
    """Splits are identical when executed with the same random seed."""
    df = data.load_train_data()
    splits_1 = split.get_group_kfold_splits(df, seed=42)
    splits_2 = split.get_group_kfold_splits(df, seed=42)

    for (t1, v1), (t2, v2) in zip(splits_1, splits_2):
        np.testing.assert_array_equal(t1, t2)
        np.testing.assert_array_equal(v1, v2)
