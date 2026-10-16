"""Cross-validation evaluation engine using GroupKFold splits."""

from typing import Any, Callable, Optional
import numpy as np
import pandas as pd

from namethellm import data
from namethellm import split
from namethellm import metrics
from namethellm.models.baseline import BaselineTFIDFClassifier
from namethellm.constants import VALID_MODELS


def run_group_kfold_evaluation(
    df: pd.DataFrame,
    model_factory: Optional[Callable[[], Any]] = None,
    n_splits: int = 5,
    seed: int = 42,
    verbose: bool = False,
) -> dict[str, Any]:
    """Runs full out-of-fold cross-validation strictly grouped on prompt_id.

    Args:
        df: Training DataFrame containing 'text', 'model', and 'prompt_id'.
        model_factory: Optional factory function returning a classifier instance.
                       Defaults to BaselineTFIDFClassifier.
        n_splits: Number of cross-validation folds.
        seed: Random seed for group-stratified splitting.
        verbose: If True, prints per-fold scores.

    Returns:
        Dictionary containing:
        - 'oof_balanced_accuracy': Overall OOF balanced accuracy.
        - 'oof_predictions': Array of OOF predictions matching df index.
        - 'per_class_recall': Dict mapping each of 18 models to its recall score.
        - 'fold_scores': List of balanced accuracy scores per fold.
    """
    if model_factory is None:
        def model_factory():
            return BaselineTFIDFClassifier(random_state=seed)

    splits = split.get_group_kfold_splits(
        df,
        group_col="prompt_id",
        target_col="model",
        n_splits=n_splits,
        seed=seed,
    )

    oof_preds = np.empty(len(df), dtype=object)
    fold_scores: list[float] = []

    for fold_idx, (train_idx, val_idx) in enumerate(splits):
        train_texts = df.iloc[train_idx]["text"].to_numpy()
        train_y = df.iloc[train_idx]["model"].to_numpy()

        val_texts = df.iloc[val_idx]["text"].to_numpy()
        val_y = df.iloc[val_idx]["model"].to_numpy()

        model = model_factory()
        model.fit(train_texts, train_y)

        preds = model.predict(val_texts)
        oof_preds[val_idx] = preds

        fold_score = metrics.compute_balanced_accuracy(val_y, preds, labels=VALID_MODELS)
        fold_scores.append(fold_score)

        if verbose:
            print(f"Fold {fold_idx + 1}/{n_splits} Balanced Accuracy: {fold_score:.4f}")

    overall_score = metrics.compute_balanced_accuracy(
        df["model"].to_numpy(),
        oof_preds,
        labels=VALID_MODELS,
    )
    per_class = metrics.compute_per_class_recall(
        df["model"].to_numpy(),
        oof_preds,
        labels=VALID_MODELS,
    )

    return {
        "oof_balanced_accuracy": float(overall_score),
        "oof_predictions": oof_preds,
        "per_class_recall": per_class,
        "fold_scores": fold_scores,
    }


def main():
    print("Loading training dataset...")
    df = data.load_train_data()
    print(f"Loaded {len(df)} samples across {df['prompt_id'].nunique()} prompts.")

    print("\nRunning 5-fold GroupKFold baseline evaluation...")
    results = run_group_kfold_evaluation(df, n_splits=5, seed=42, verbose=True)

    print("\n" + "=" * 50)
    print(f"Overall OOF Balanced Accuracy: {results['oof_balanced_accuracy']:.4f}")
    print("=" * 50)
    print("\nPer-Model Recall:")
    for model_name, rec in sorted(results["per_class_recall"].items()):
        print(f"  {model_name:24s}: {rec:.4f}")


if __name__ == "__main__":
    main()
