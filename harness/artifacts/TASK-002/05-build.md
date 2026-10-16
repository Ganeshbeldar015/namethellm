---
status: complete
owner: builder
task: TASK-002
inputs:
  - harness/artifacts/TASK-002/03-plan.md
  - harness/artifacts/TASK-002/04-tests.md
---
# 05-build.md — Build Log for TASK-002

## 1. Summary of Changes
Implemented the official Balanced Accuracy metric and a high-performance baseline multi-class classifier using sublinear word and character n-gram TF-IDF representations combined with regularized linear classification.

### Files Created
- `src/namethellm/metrics.py`: `compute_balanced_accuracy()`, `compute_per_class_recall()`.
- `src/namethellm/models/__init__.py`: Package export.
- `src/namethellm/models/baseline.py`: `BaselineTFIDFClassifier`.
- `src/namethellm/evaluate.py`: `run_group_kfold_evaluation()`.

## 2. Benchmark Performance
Executed full 5-fold GroupKFold cross-validation on `dataset/train.csv` (2,699 samples, 150 prompt IDs):
- **Overall OOF Balanced Accuracy**: **0.3004** (vs. random guess 0.0555).
- Per-fold breakdown:
  - Fold 1: 0.2927
  - Fold 2: 0.3204
  - Fold 3: 0.2981
  - Fold 4: 0.2815
  - Fold 5: 0.3093
- Execution time: ~38 seconds for all 5 folds.

## 3. Verification Commands & Outputs
- `python -m pytest tests/unit/test_metrics.py tests/unit/test_baseline.py`
  - Result: 6 passed in 38.49s.
  - Exit code: 0.
- `python -m namethellm.evaluate`
  - Result: OOF Balanced Accuracy 0.3004.
  - Exit code: 0.
