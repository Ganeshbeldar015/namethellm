---
status: complete
owner: po-spec
task: TASK-002
inputs:
  - docs/harness.md
  - harness/tasks/TASK-002.md
---
# 01-spec.md — Specification for TASK-002

## 1. Problem
To benchmark LLM authorship attribution algorithms and guide feature iteration, we require:
1. An exact, standalone implementation of the competition's Balanced Accuracy metric.
2. A fast, leak-free baseline classifier (TF-IDF + calibrated linear modeling) evaluated via GroupKFold cross-validation on `prompt_id`.

## 2. Scope
- Implementation of `compute_balanced_accuracy(y_true, y_pred)` and `compute_per_class_recall(y_true, y_pred)`.
- Implementation of `BaselineTFIDFClassifier` combining character/word n-gram TF-IDF vectorization with regularized linear classification (Ridge / LogisticRegression / LinearSVC).
- Implementation of cross-validation runner in `src/namethellm/evaluate.py` calculating out-of-fold predictions and scores across the 5 GroupKFold splits.

## 3. Out of Scope
- Tree-based boosting (LightGBM) and deep transformer models (Sprint 2 & 3).
- Test submission generation (TASK-003).

## 4. User Stories
- As an ML engineer, I want to compute balanced accuracy locally and obtain results identical to `sklearn.metrics.balanced_accuracy_score`, so my local validation exactly mirrors Kaggle's leaderboard metric.
- As an ML engineer, I want to inspect per-class recall across all 18 models to identify which model pairs are confusing each other.
- As an ML engineer, I want a fast (< 30s) baseline model with verified out-of-fold accuracy significantly above random guessing (1/18 ≈ 0.0555).

## 5. Requirements to Acceptance Criteria Mapping

### REQ-003: Balanced Accuracy Metric
- **`AC-003-a`**: Given true labels `y_true` and predicted labels `y_pred` for the 18 classes:
  1. `compute_balanced_accuracy(y_true, y_pred)` produces a float matching `sklearn.metrics.balanced_accuracy_score(y_true, y_pred)` to within $10^{-6}$.
  2. `compute_per_class_recall(y_true, y_pred)` returns a dictionary mapping all 18 model names to their individual recall scores $[0.0, 1.0]$.
  3. The mean of `compute_per_class_recall` equals `compute_balanced_accuracy`.

### REQ-005: Baseline Model & OOF Evaluation
- **`AC-005-a`**: Given `dataset/train.csv` split into 5 folds via `get_group_kfold_splits()`:
  1. The baseline model is trained sequentially on 5 folds with zero prompt leakage.
  2. Out-of-fold balanced accuracy strictly exceeds random guess: $\text{OOF Balanced Accuracy} > 0.15$ (well above $0.0555$).
  3. The evaluation script returns an out-of-fold prediction series matching the full training dataset length (2,699).

## 6. Edge Cases & Constraints
- Handling missing classes in predictions: If a model is never predicted, its recall must be 0.0 without division-by-zero errors.
- String label handling: Both raw strings (e.g. `'gpt-5.5'`) and integer-encoded labels must be supported.

## 7. Non-Functional Requirements
- Evaluation of full 5-fold CV must complete within 45 seconds on standard CPU.
- Complete reproducibility with fixed random seed (`seed=42`).

## 8. Open Questions
- None.
