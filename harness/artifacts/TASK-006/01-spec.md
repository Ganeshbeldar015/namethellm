---
status: complete
owner: po-spec
task: TASK-006
inputs:
  - docs/harness.md
  - harness/tasks/TASK-006.md
---
# 01-spec.md — Specification for TASK-006

## 1. Problem
Traditional n-gram features conflate semantic topic vocabulary with author-specific stylistic syntax. When evaluated across unseen prompts (ADR-0001), standard n-grams suffer from topic leakage and false correlations. To achieve frontier attribution performance, we must isolate topic-invariant syntactic structures (function-word patterns) and typographical layout rhythms (casing shape patterns) alongside lexical and stylometric features.

## 2. Scope
- Module `src/namethellm/features/text_transforms.py`:
  - `shape_text(texts)`: Replaces uppercase words with 'X' and lowercase words with 'x', capturing capitalization frequency, casing rhythm, and title-casing style.
  - `function_text(texts)`: Replaces all content words with `"CONTENT"`, leaving only closed-class function words and punctuation marks, isolating pure grammatical syntax.
- Module `src/namethellm/models/stylegram.py`:
  - `StylegramClassifier`: Multi-view ensemble combining:
    1. Word n-grams with punctuation preserved (`(1, 2)`, 12,000 features).
    2. Character n-grams (`char_wb`, `(3, 5)`, 18,000 features).
    3. Casing shape n-grams (`char`, `(2, 6)`, 10,000 features).
    4. Function syntax n-grams (`word`, `(1, 3)`, 10,000 features).
    5. Scaled 46 stylometric features.
  - Estimator: L2-regularized logistic regression with balanced class weights.
- Metric Exit Gate:
  - 5-fold CV Out-of-Fold Balanced Accuracy strictly improves over the Sprint 2 benchmark of 0.3304 (target $\ge 0.3400$).

## 3. Out of Scope
- GPU-only deep neural transformer inference (handled in standalone Kaggle packaging in Sprint 4).

## 4. User Stories
- As a competitor, when I run `StylegramClassifier`, the model captures syntax and casing patterns that generalize across unseen prompts, increasing cross-validation balanced accuracy.
- As an engineer, passing edge cases (empty strings, single characters, punctuation-only) to `shape_text` or `function_text` produces clean, valid text representations without errors.

## 5. Requirements to Acceptance Criteria Mapping

### REQ-004: Topic-Invariant Stylistic Features
- **`AC-004-a`**: Given raw text passages, when transformed and passed to feature extractors, numerical vectors are strictly finite without NaNs or infinite values.

### REQ-005: Advanced Attribution Models
- **`AC-005-a`**: Given the training folds, when model is trained, then out-of-fold balanced accuracy strictly exceeds Sprint 2 benchmark (> 0.3304).

## 6. Edge Cases & Constraints
- Empty string: `shape_text([""])` returns `[""]`; `function_text([""])` returns `[""]`.
- Text with only punctuation or symbols: correctly preserved without IndexError.
- Unicode / foreign characters: correctly handled.

## 7. Non-Functional Requirements
- Total 5-fold CV runtime < 60 seconds on standard CPU.
- Fully offline and deterministic.

## 8. Open Questions
- None.
