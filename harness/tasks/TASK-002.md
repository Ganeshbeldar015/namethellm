# TASK-002 — Balanced Accuracy Metric and Baseline TF-IDF Classifier

Backlog ref: TASK-002 · Sprint: 1 · Priority: Must

## Intent
Implement the competition evaluation metric (Balanced Accuracy) and build a fast, deterministic baseline classifier using TF-IDF and calibrated linear modeling with GroupKFold out-of-fold evaluation.

## Scope / Out of scope
**In Scope**:
- `src/namethellm/metrics.py`: Official balanced accuracy metric ($\frac{1}{K} \sum_{i=1}^K \text{recall}_i$), per-model recall breakdown, and evaluation helper.
- `src/namethellm/models/baseline.py`: TF-IDF text feature extraction pipeline coupled with linear classifiers (Ridge / LogisticRegression / LinearSVC).
- `src/namethellm/evaluate.py`: Full Out-Of-Fold (OOF) cross-validation runner using `get_group_kfold_splits`.

**Out of Scope**:
- Non-linear tree models (LightGBM) or deep neural nets (deferred to Sprint 2 & 3).
- Submission file creation (handled in TASK-003).

## Guidance
- Metric must strictly replicate Kaggle's evaluation formula: macro-averaged per-class recall across the 18 candidate models.
- All vectorizers and scalers must be fitted strictly inside training folds to prevent any data leakage.
- Provide full out-of-fold score reporting and ensure reproducible results with `seed=42`.

## Requirements
- `REQ-003`: Implement balanced accuracy evaluation metric matching Kaggle's official specification.
- `REQ-005`: Develop baseline and advanced attribution models (linear classifiers, GBDTs, embeddings/neural).

## Acceptance
- `AC-003-a`: Given predicted class labels and ground truth labels for 18 classes, when evaluated, then the score matches `sklearn.metrics.balanced_accuracy_score(y_true, y_pred)`.
- `AC-005-a`: Given the training folds, when baseline model (TF-IDF + Ridge/LogisticRegression) is trained, then out-of-fold balanced accuracy strictly exceeds random guess (1/18 ≈ 0.0555).

## Risks / Notes
- The baseline must execute quickly (< 60s for full 5-fold CV) so that rapid iteration is possible.
