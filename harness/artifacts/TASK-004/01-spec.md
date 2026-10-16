---
status: complete
owner: po-spec
task: TASK-004
inputs:
  - docs/harness.md
  - harness/tasks/TASK-004.md
---
# 01-spec.md — Specification for TASK-004

## 1. Problem
Different frontier LLMs exhibit subtle, consistent stylistic fingerprints — such as sentence length variation, punctuation frequencies (e.g. em-dashes, semicolons, ellipses), lexical richness, markdown header usage, bullet points, and specific discourse marker words. Because the competition evaluates models on unseen prompts (ADR-0001), lexical n-grams alone risk overfitting to topics. We need topic-invariant stylometric and structural feature extraction that generalizes across any prompt.

## 2. Scope
- Package: `src/namethellm/features/`
- Module: `src/namethellm/features/stylometry.py`
  - `StylometricFeatureExtractor`: Scikit-learn compatible transformer implementing `fit(X, y=None)` and `transform(X)`.
  - Feature categories:
    1. Length & sentence structure (char count, word count, sentence count, avg word length, avg sentence length, sentence length std dev).
    2. Punctuation frequencies (commas, periods, semicolons, colons, exclamation marks, question marks, hyphens, en-dashes, em-dashes, quotes, parentheses, brackets, ellipses).
    3. Casing & character ratios (uppercase ratio, lowercase ratio, digit ratio, whitespace ratio, punctuation ratio).
    4. Lexical diversity & vocabulary richness (Type-Token Ratio, hapax legomena ratio, short words ratio, long words ratio).
    5. Formatting & structural indicators (markdown headers, bullet points, numbered lists, code backticks).
    6. LLM discourse marker / signature word counts (e.g., "delve", "furthermore", "moreover", "testament", "crucial", "essential", "notably", "essentially", "in conclusion").
  - Output guarantees: 2D numpy array of shape `(n_samples, n_features)` of type `float64` with strictly 0 NaNs and 0 infinite values.
  - Method `get_feature_names_out()` returning list of all computed feature names.

## 3. Out of Scope
- Training GBDT or tree models (handled in `TASK-005`).
- Pretrained neural transformer embeddings (deferred to Sprint 3).

## 4. User Stories
- As an ML engineer, when I include `StylometricFeatureExtractor()` in a scikit-learn `Pipeline` or `FeatureUnion`, it transforms text passages into clean, finite numerical features without producing NaN or inf.
- As an ML engineer, when an input text is empty, single-character, or contains atypical unicode, the extractor safely handles division by zero and returns finite zeros rather than raising runtime errors.

## 5. Requirements to Acceptance Criteria Mapping

### REQ-004: Topic-Invariant Stylometric Feature Extraction
- **`AC-004-a`**: Given raw text passages, when passed to the feature extractor, then numerical feature vectors are produced without NaNs or infinite values.
  - Verification:
    1. Shape is `(len(texts), n_features)` where `n_features >= 30`.
    2. `np.isnan(features).sum() == 0`.
    3. `np.isinf(features).sum() == 0`.
    4. Deterministic output for identical inputs.
    5. Safe zero-handling on empty string `""` or single word inputs.

## 6. Edge Cases & Constraints
- Empty text string `""`: outputs finite zeros across all features without crashing or dividing by zero.
- Text without punctuation or without whitespace: handles gracefully.
- Multilingual / non-ASCII unicode: safely processed.
- Memory: vectorization must execute in < 2 seconds for 3,000 samples.

## 7. Non-Functional Requirements
- Strictly offline, hermetic computation.
- Pure Python and NumPy/SciPy without heavyweight external NLP runtime dependencies like spacy or java-based tokenizers.

## 8. Open Questions
- None.
