---
status: complete
owner: tech-lead
task: TASK-006
inputs:
  - harness/artifacts/TASK-006/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-006

## 1. Architectural Approach
We design the multi-view topic-invariant `StylegramClassifier` architecture:
- `src/namethellm/features/text_transforms.py`:
  - `shape_text(texts)`: Abstract casing pattern extractor that maps words to 'X' (uppercase) and 'x' (lowercase) while preserving spacing, punctuation, and structural layout.
  - `function_text(texts)`: Closed-class function word filter that strips topic semantics by replacing content words with `"CONTENT"`, leaving exclusively grammatical glue words and punctuation.
- `src/namethellm/models/stylegram.py`:
  - `StylegramClassifier`: Scikit-learn estimator combining 5 weighted feature views:
    1. Punctuation-preserving lexical n-grams (1, 2) [weight: 0.8].
    2. Character boundary n-grams (3, 5) [weight: 1.0].
    3. Casing shape character n-grams (2, 6) [weight: 0.5].
    4. Function syntax n-grams (1, 3) [weight: 0.5].
    5. Standardized 46-dimensional stylometric features [weight: 0.5].
  - Solver: L2-regularized logistic regression with balanced class weights.
- `src/namethellm/models/__init__.py`:
  - Export `StylegramClassifier`.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/features/text_transforms.py` | Create | `shape_text` and `function_text` transformation functions |
| `src/namethellm/models/stylegram.py` | Create | `StylegramClassifier` multi-view pipeline |
| `src/namethellm/models/__init__.py` | Modify | Export `StylegramClassifier` |
| `tests/unit/test_text_transforms.py` | Create | Unit tests validating text transformations |
| `tests/unit/test_stylegram.py` | Create | Unit tests validating StylegramClassifier |

## 3. Lane Decomposition & Exclusive File Ownership
Sequential execution (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/features/text_transforms.py`
  - `src/namethellm/models/stylegram.py`
  - `src/namethellm/models/__init__.py`

- **Test Author owns**:
  - `tests/unit/test_text_transforms.py`
  - `tests/unit/test_stylegram.py`

No overlapping ownership exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-004-a`**: In `tests/unit/test_text_transforms.py`:
  - Verify `shape_text` correctly transforms "Hello World!" -> "X x!" and preserves whitespace/digits.
  - Verify `function_text` preserves words like "in", "the", "and" while replacing "artificial" with "CONTENT".
  - Verify edge cases (empty strings `""`, pure numbers, symbols only).
- **`AC-005-a`**: In `tests/unit/test_stylegram.py`:
  - Fit `StylegramClassifier` on synthetic 18-class texts.
  - Verify `predict` outputs valid labels in `VALID_MODELS`.
  - Verify `predict_proba` outputs probabilities summing to $1.0 \pm 10^{-5}$ per sample.
  - Assert 5-fold CV OOF balanced accuracy exceeds Sprint 2 benchmark (> 0.3304).

## 5. Risk Assessment & Mitigations
- **Multi-view extraction memory & speed**:
  - *Mitigation*: Vectorizers fit on transformed generators and sparse representations are directly combined via `scipy.sparse.hstack` without dense instantiation.
- **Handling of zero-length or edge strings**:
  - *Mitigation*: Fallback checks return `""` safely without throwing regex or split exceptions.

## 6. Rollback Plan
Revert git branch to `1db4b5d` if unresolvable issues occur.
