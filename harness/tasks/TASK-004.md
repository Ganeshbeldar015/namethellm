# TASK-004 — Stylometric & Structural Feature Extraction

Backlog ref: TASK-004 · Sprint: 2 · Priority: Must · Status: Complete

## Intent
Implement a robust, scikit-learn compatible stylometric and structural feature extractor (`StylometricFeatureExtractor`) that captures topic-invariant authorship signals across the 18 frontier LLMs.

## Scope / Out of scope
**In Scope**:
- `src/namethellm/features/__init__.py`: Package init.
- `src/namethellm/features/stylometry.py`:
  - `StylometricFeatureExtractor(BaseEstimator, TransformerMixin)`:
    - Text length & density: character count, word count, line count, sentence count, avg word length, avg sentence length, sentence length std dev.
    - Punctuation & symbol frequency profiles: commas, semicolons, colons, dashes (hyphen, en-dash, em-dash), quotes, parentheses, brackets, ellipses, asterisks, markdown bullets, exclamation/question marks.
    - Casing & character distributions: uppercase ratio, lowercase ratio, digit ratio, whitespace ratio, punctuation ratio.
    - Lexical diversity & richness: Type-Token Ratio (TTR), hapax legomena ratio, short word ratio, long word ratio.
    - Markdown & structure indicators: header markers, bullet lists, numbered lists, backtick/code frequency.
    - Distinctive discourse markers / LLM function word frequencies.
  - Safe numerical guarantees: 0 division protections (`np.nan_to_num`, zero fill), output guaranteed to have shape `(n_samples, n_features)` with zero NaNs or Infs.
- `tests/unit/test_stylometry.py`: Comprehensive unit tests verifying `AC-004-a` and edge cases (empty strings, single characters, purely numeric, extreme length variations).

**Out of Scope**:
- Tree model training (handled in `TASK-005`).
- Dense neural embeddings (deferred to Sprint 3).

## Requirements
- `REQ-004`: Extract topic-invariant stylistic, punctuation, lexical, and structural features.

## Acceptance
- `AC-004-a`: Given raw text passages, when passed to the feature extractor, then numerical feature vectors are produced without NaNs or infinite values.

## Risks / Notes
- Features must be topic-invariant to generalize across unseen prompt IDs (aligning with ADR-0001).
- Extractor must be compatible with scikit-learn `Pipeline` and `FeatureUnion`.
