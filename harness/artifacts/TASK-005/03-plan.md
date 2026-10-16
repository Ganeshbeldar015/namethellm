---
status: complete
owner: tech-lead
task: TASK-005
inputs:
  - harness/artifacts/TASK-005/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-005

## 1. Architectural Approach
We design the hybrid feature modeling and probability calibration pipeline:
- `src/namethellm/models/hybrid.py`:
  - `HybridStyloClassifier`: Scikit-learn estimator integrating 3 complementary feature representations via `FeatureUnion`:
    1. Word-level sublinear TF-IDF (1, 2 n-grams, 12,000 features).
    2. Character-level sublinear TF-IDF (3, 5 char_wb n-grams, 18,000 features).
    3. Scaled stylometry features (46 features from `StylometricFeatureExtractor` normalized with `StandardScaler`).
    4. Estimator: Regularized `LogisticRegression(C=1.2, solver='lbfgs', class_weight='balanced')`.
- `src/namethellm/postprocess.py`:
  - `BalancedAccuracyCalibrator`: Marginal power scaling calibrator that adjusts class decision boundaries based on marginal prediction frequencies:
    $w_c = \frac{1}{(\sum_{i} P_{i, c})^\gamma}$
    Prevents majority-class overprediction and guarantees balanced accuracy is preserved or enhanced.
- `src/namethellm/models/__init__.py`:
  - Exports `HybridStyloClassifier`.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/models/hybrid.py` | Create | `HybridStyloClassifier` implementation |
| `src/namethellm/postprocess.py` | Create | `BalancedAccuracyCalibrator` implementation |
| `src/namethellm/models/__init__.py` | Modify | Export `HybridStyloClassifier` |
| `tests/unit/test_hybrid.py` | Create | Unit tests validating AC-005-a and AC-006-a |

## 3. Lane Decomposition & Exclusive File Ownership
Sequential execution (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/models/hybrid.py`
  - `src/namethellm/postprocess.py`
  - `src/namethellm/models/__init__.py`

- **Test Author owns**:
  - `tests/unit/test_hybrid.py`

No overlapping ownership exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-005-a`**: In `tests/unit/test_hybrid.py`:
  - Fit `HybridStyloClassifier` on sample texts and labels.
  - Assert `predict_proba` returns valid probabilities in $[0, 1]$ summing to $1.0 \pm 10^{-5}$ per sample.
  - Assert `predict` returns valid string labels matching `classes_`.
  - Assert 5-fold CV OOF balanced accuracy exceeds baseline 0.3004.
- **`AC-006-a`**: In `tests/unit/test_hybrid.py`:
  - Fit `BalancedAccuracyCalibrator` on sample probability distribution.
  - Assert calibrated probabilities sum to $1.0 \pm 10^{-5}$ per sample.
  - Assert that applying calibrator to skewed probability distributions does not decrease Balanced Accuracy.

## 5. Risk Assessment & Mitigations
- **Memory Consumption**: Joining 30,000 sparse TF-IDF features with 46 dense stylometric features.
  - *Mitigation*: FeatureUnion produces a `scipy.sparse.csr_matrix` combining sparse and dense columns without converting sparse matrices to full dense arrays.
- **Under-represented Classes**: `claude-fable-5` has 149 samples vs 150.
  - *Mitigation*: Handled via `class_weight='balanced'` in the linear classifier.

## 6. Rollback Plan
Revert git branch to `84b54e1` if unresolvable issues occur.
