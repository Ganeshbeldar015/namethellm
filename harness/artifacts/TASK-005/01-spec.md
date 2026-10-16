---
status: complete
owner: po-spec
task: TASK-005
inputs:
  - docs/harness.md
  - harness/tasks/TASK-005.md
---
# 01-spec.md — Specification for TASK-005

## 1. Problem
While the baseline TF-IDF model establishes a functional benchmark (0.3004 OOF Balanced Accuracy), it lacks topic-invariant stylometric signals and suffers from uncalibrated marginal class prediction skew. We require a hybrid classifier that integrates word/character n-grams with 46 stylometric features, paired with a decision-threshold calibrator designed to maximize Balanced Accuracy across all 18 classes.

## 2. Scope
- Module `src/namethellm/models/hybrid.py`:
  - `HybridStyloClassifier`: Scikit-learn estimator combining:
    1. Word TF-IDF n-grams (1, 2) with sublinear TF.
    2. Character TF-IDF n-grams (3, 5) with sublinear TF.
    3. Scaled 46 stylometric features from `StylometricFeatureExtractor`.
    4. Regularized multi-class classifier with balanced class weighting.
  - Exposes `.fit(X, y)`, `.predict(X)`, `.predict_proba(X)`, and `.classes_`.
- Module `src/namethellm/postprocess.py`:
  - `BalancedAccuracyCalibrator`: Marginal power prior adjustment calibrating class prediction distributions to optimize Balanced Accuracy without decreasing validation scores.
- Metric Exit Gate:
  - 5-fold CV Out-of-Fold Balanced Accuracy strictly exceeds the Sprint 1 baseline score of 0.3004.

## 3. Out of Scope
- Neural transformer hidden state extraction (Sprint 3).
- Automated submission to Kaggle platform.

## 4. User Stories
- As an ML engineer, when I train `HybridStyloClassifier`, I want an Out-of-Fold Balanced Accuracy significantly higher than 0.3004.
- As an ML engineer, when I apply `BalancedAccuracyCalibrator` to predicted probability distributions, the balanced accuracy metric remains monotonic or improves without distorting probability calibration.

## 5. Requirements to Acceptance Criteria Mapping

### REQ-005: Advanced Attribution Models
- **`AC-005-a`**: Given the training folds, when model is trained, then out-of-fold balanced accuracy strictly exceeds random guess (0.0555) and surpasses the baseline (0.3004).

### REQ-006: Balanced Accuracy Probability Calibration
- **`AC-006-a`**: Given out-of-fold probability distributions, when balanced accuracy optimization or prior adjustment is applied, then validation balanced accuracy does not decrease.

## 6. Edge Cases & Constraints
- Class alignment: `predict_proba()` output columns must strictly align with `classes_` and `VALID_MODELS`.
- Probabilities must sum to 1.0 per row within numerical tolerance ($10^{-5}$).
- Zero division protection during marginal frequency calibration.

## 7. Non-Functional Requirements
- 5-fold CV execution runtime < 60 seconds on CPU.
- Offline, deterministic execution.

## 8. Open Questions
- None.
