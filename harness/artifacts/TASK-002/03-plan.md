---
status: complete
owner: tech-lead
task: TASK-002
inputs:
  - harness/artifacts/TASK-002/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-002

## 1. Architectural Approach
We design the evaluation metric and baseline modeling layer:
- `src/namethellm/metrics.py`: Implementation of macro-averaged per-class recall and balanced accuracy metric, fully aligned with Kaggle's evaluation logic.
- `src/namethellm/models/baseline.py`: Multi-class text classification pipeline utilizing sublinear-scaled word and character n-gram TF-IDF representations combined with regularized linear classification.
- `src/namethellm/evaluate.py`: Cross-validation engine providing leak-free Out-Of-Fold (OOF) evaluation, per-fold scores, and metric reporting.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/metrics.py` | Create | Balanced accuracy and per-class recall calculation |
| `src/namethellm/models/__init__.py` | Create | Models package initialization |
| `src/namethellm/models/baseline.py` | Create | Baseline TF-IDF + LogisticRegression pipeline |
| `src/namethellm/evaluate.py` | Create | GroupKFold OOF evaluation runner |
| `tests/unit/test_metrics.py` | Create | Unit tests for AC-003-a and metric edge cases |
| `tests/unit/test_baseline.py` | Create | Unit tests for AC-005-a and OOF evaluation |

## 3. Lane Decomposition & Exclusive File Ownership
Sequential execution (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/metrics.py`
  - `src/namethellm/models/__init__.py`
  - `src/namethellm/models/baseline.py`
  - `src/namethellm/evaluate.py`

Test Author owns:
  - `tests/unit/test_metrics.py`
  - `tests/unit/test_baseline.py`

No overlapping ownership exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-003-a`**: In `test_metrics.py`:
  - Synthesize truth and predicted arrays with 18 classes.
  - Assert `compute_balanced_accuracy(y_true, y_pred)` equals `sklearn.metrics.balanced_accuracy_score(y_true, y_pred)` to within $10^{-6}$.
  - Assert `compute_per_class_recall` accurately computes sensitivity per class with zero division errors when a class has 0 true or predicted instances.
- **`AC-005-a`**: In `test_baseline.py`:
  - Run `run_group_kfold_evaluation()` on a subset or full dataset with 5 folds.
  - Assert that out-of-fold balanced accuracy strictly exceeds $0.15$ (surpassing random guess $0.0555$).
  - Assert that OOF predictions array has length equal to the input dataset (2,699) with no null values.

## 5. Risk Assessment & Mitigations
- **Execution Speed**: High-dimensional n-grams can be slow if `max_features` is unbound.
  - *Mitigation*: Cap vocabulary (`max_features=10000` for word, `15000` for char_wb), use `sublinear_tf=True`, and fast solver `lbfgs` with `max_iter=300`.

## 6. Rollback Plan
Revert git branch to `0864ab2` if unresolvable regressions occur.
