# TASK-005 — Hybrid Stylometric Modeling & Balanced Accuracy Calibration

Backlog ref: TASK-005 · Sprint: 2 · Priority: Must · Status: Complete

## Intent
Build the hybrid multi-class classification architecture combining high-dimensional lexical/character n-grams with topic-invariant stylometric features, and implement a postprocessing probability calibrator optimized for Balanced Accuracy.

## Scope / Out of scope
**In Scope**:
- `src/namethellm/models/hybrid.py`:
  - `HybridStyloClassifier`: Scikit-learn estimator combining:
    1. Sublinear word-level TF-IDF (1-2 ngrams, 12k features).
    2. Sublinear char-level TF-IDF (3-5 ngrams, 18k features).
    3. 46 standardized stylometric features (`StylometricFeatureExtractor` + `StandardScaler`).
    4. Regularized classifier with balanced class weights.
- `src/namethellm/postprocess.py`:
  - `BalancedAccuracyCalibrator`: Marginal power prior adjustment calibrating class prediction distributions to optimize Balanced Accuracy.
- `tests/unit/test_hybrid.py`:
  - Tests covering estimator interface, probability output validity, and calibration guarantees.
- Metric exit gate: Full 5-fold CV OOF Balanced Accuracy strictly improves over Sprint 1 baseline (0.3004 -> target > 0.3200).

**Out of Scope**:
- Neural transformer hidden state extraction (Sprint 3).

## Requirements
- `REQ-005`: Develop baseline and advanced attribution models.
- `REQ-006`: Calibrate probability predictions and apply decision thresholds optimized for balanced accuracy.

## Acceptance
- `AC-005-a`: Given the training folds, when model is trained, then out-of-fold balanced accuracy strictly exceeds random guess and beats the baseline (target > 0.3004).
- `AC-006-a`: Given out-of-fold probability distributions, when balanced accuracy optimization or prior adjustment is applied, then validation balanced accuracy does not decrease.

## Risks / Notes
- Features must maintain zero prompt leakage via `StratifiedGroupKFold` on `prompt_id` (ADR-0001).
