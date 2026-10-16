---
status: complete
owner: builder
task: TASK-005
inputs:
  - harness/artifacts/TASK-005/03-plan.md
  - harness/artifacts/TASK-005/04-tests.md
---
# 05-build.md — Build Log for TASK-005

## 1. Summary of Changes
Implemented the `HybridStyloClassifier` model and the `BalancedAccuracyCalibrator` postprocessor:
- `src/namethellm/models/hybrid.py`:
  - `HybridStyloClassifier`: Integrates 12,000 word TF-IDF features, 18,000 char_wb TF-IDF features, and 46 standardized stylometric features into an L2-regularized logistic regression classifier with balanced class weights.
- `src/namethellm/postprocess.py`:
  - `BalancedAccuracyCalibrator`: Implements marginal frequency power prior scaling to optimize multi-class balanced accuracy without degrading calibrated probability outputs.
- `src/namethellm/models/__init__.py`:
  - Exported `HybridStyloClassifier`.

## 2. Benchmark Performance
Executed full 5-fold GroupKFold cross-validation on `dataset/train.csv` (2,699 samples, 150 prompt IDs):
- **Sprint 1 Baseline OOF Balanced Accuracy**: **0.3004**
- **HybridStyloClassifier OOF Balanced Accuracy**: **0.3289** (+0.0285 absolute improvement)
- **Calibrated Hybrid OOF Balanced Accuracy ($\gamma=0.05$)**: **0.3304** (+0.0300 absolute improvement over baseline)
- Per-fold breakdown:
  - Fold 1: 0.3225
  - Fold 2: 0.3463
  - Fold 3: 0.3352
  - Fold 4: 0.2889
  - Fold 5: 0.3519

## 3. Verification Commands & Outputs
- `python -m pytest tests/unit/test_hybrid.py`
  - Result: 3 passed in 8.98s.
  - Exit code: 0.
- `python -m pytest tests/unit`
  - Result: 38 passed in 134.30s (all unit tests green).
  - Exit code: 0.
