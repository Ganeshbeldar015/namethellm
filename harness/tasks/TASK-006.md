# TASK-006 — Multi-View Stylegram Architecture & Ensembling

Backlog ref: TASK-006 · Sprint: 3 · Priority: Must · Status: Complete

## Intent
Build the multi-view topic-invariant `StylegramClassifier` architecture that combines structural casing patterns (`shape_text`), topic-stripped function-word syntax (`function_text`), word/character n-grams, and standardized stylometry, establishing a new cross-validation benchmark (> 0.3400).

## Scope / Out of scope
**In Scope**:
- `src/namethellm/features/text_transforms.py`:
  - `shape_text(texts)`: Encodes capitalization and casing morphology by abstracting alphabetic words to casing representations ('X' for uppercase, 'x' for lowercase).
  - `function_text(texts)`: Replaces all content words with a generic token (`"CONTENT"`), preserving purely function words and punctuation to completely isolate syntax from topic semantics.
- `src/namethellm/models/stylegram.py`:
  - `StylegramClassifier`: Multi-view ensemble combining:
    1. Word n-grams with punctuation tokens.
    2. Character n-grams (`char_wb`).
    3. Casing shape n-grams.
    4. Function syntax n-grams.
    5. Standardized 46-dimensional stylometric features.
  - Multi-class probability predictions and calibration support.
- `tests/unit/test_text_transforms.py`:
  - Unit tests for `shape_text` and `function_text` verifying correct transformations, determinism, and empty/edge string handling.
- `tests/unit/test_stylegram.py`:
  - Unit tests for `StylegramClassifier` verifying estimator methods and probability calibration.
- Exit Gate: 5-fold CV Out-of-Fold Balanced Accuracy strictly improves over Sprint 2 (0.3304 -> target > 0.3400).

**Out of Scope**:
- GPU-dependent deep model inference (deferred to Kaggle notebook packaging in Sprint 4).

## Requirements
- `REQ-004`: Extract topic-invariant stylistic, punctuation, lexical, and structural features.
- `REQ-005`: Develop baseline and advanced attribution models.

## Acceptance
- `AC-004-a`: Given raw text passages, when passed to the feature extractor, numerical feature vectors are produced without NaNs or infinite values.
- `AC-005-a`: Given the training folds, when model is trained, then out-of-fold balanced accuracy strictly exceeds Sprint 2 benchmark (> 0.3304).

## Risks / Notes
- Feature extraction across 4 views must be efficient and memory bounded.
- Strict compliance with `StratifiedGroupKFold` on `prompt_id` (ADR-0001).
