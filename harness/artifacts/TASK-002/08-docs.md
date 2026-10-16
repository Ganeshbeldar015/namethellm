---
status: complete
owner: scribe
task: TASK-002
inputs:
  - harness/artifacts/TASK-002/05-build.md
---
# 08-docs.md — Documentation for TASK-002

## 1. Documentation Updates
- Updated `README.md` with:
  - Baseline execution command: `python -m namethellm.evaluate`.
  - Baseline benchmark metric: OOF Balanced Accuracy of 0.3004.
  - Python usage snippet for `metrics.py` and `BaselineTFIDFClassifier`.
- Authored docstrings for all new modules (`metrics.py`, `models/baseline.py`, `evaluate.py`).

## 2. API Summary
- `namethellm.metrics.compute_balanced_accuracy(y_true, y_pred, labels=None) -> float`
- `namethellm.metrics.compute_per_class_recall(y_true, y_pred, labels=None) -> dict[str, float]`
- `namethellm.models.baseline.BaselineTFIDFClassifier`
- `namethellm.evaluate.run_group_kfold_evaluation(df, model_factory=None, n_splits=5, seed=42) -> dict`
