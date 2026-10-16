---
status: complete
owner: tech-lead
task: TASK-004
inputs:
  - harness/artifacts/TASK-004/01-spec.md
---
# 03-plan.md — Implementation Plan for TASK-004

## 1. Architectural Approach
We design a modular, high-throughput, scikit-learn compatible stylometric feature engineering component:
- `src/namethellm/features/__init__.py`: Package init exporting `StylometricFeatureExtractor`.
- `src/namethellm/features/stylometry.py`:
  - `StylometricFeatureExtractor(BaseEstimator, TransformerMixin)`:
    - Implements standard `fit(X, y=None)` and `transform(X)`.
    - Computes ~36 topic-invariant quantitative features across 5 distinct linguistic categories:
      1. Length & sentence density (char count, word count, sentence count, line count, avg word length, avg sentence length in words and chars, sentence length standard deviation).
      2. Casing & character density ratios (uppercase ratio, lowercase ratio, digit ratio, whitespace ratio, punctuation ratio).
      3. Punctuation frequency profiles per 1,000 chars (comma, period, semicolon, colon, exclamation, question mark, hyphen, em/en-dash, quotes, parentheses, brackets, ellipses, asterisks).
      4. Lexical diversity & richness (Type-Token Ratio, hapax legomena ratio, short words ratio <= 3 chars, long words ratio >= 7 chars).
      5. Structural formatting & markdown patterns (header lines, bullet lines, numbered list lines, backtick counts).
      6. LLM discourse signature frequencies per 1,000 words (delve, furthermore, moreover, testament, crucial, essential, notably, essentially, consequently, tapestry, comprehensive, in conclusion).
    - Guarantees zero division handling: all denominators use safe safeguards (`max(denom, 1)` or explicit conditionals) and final output is sanitized with `np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)`.
    - Implements `get_feature_names_out(input_features=None)`.

## 2. File-Level Change List
| File Path | Action | Purpose |
|---|---|---|
| `src/namethellm/features/__init__.py` | Create | Package initialization and public symbol export |
| `src/namethellm/features/stylometry.py` | Create | `StylometricFeatureExtractor` implementation |
| `tests/unit/test_stylometry.py` | Create | Unit tests validating AC-004-a and edge cases |

## 3. Lane Decomposition & Exclusive File Ownership
Sequential execution (solo builder lane `main`):
- **Lane `main` owns**:
  - `src/namethellm/features/__init__.py`
  - `src/namethellm/features/stylometry.py`

- **Test Author owns**:
  - `tests/unit/test_stylometry.py`

No overlapping ownership exists.

## 4. Test Strategy per Acceptance Criteria
- **`AC-004-a`**: In `tests/unit/test_stylometry.py`:
  - **Output Dimensions**: Verify output is 2D numpy array with shape `(len(texts), n_features)` and `n_features >= 30`.
  - **Finite Numbers Guarantee**: Assert `np.isnan(X_feat).sum() == 0` and `np.isinf(X_feat).sum() == 0` across varied sample corpora.
  - **Pipeline Compatibility**: Verify integration inside `sklearn.pipeline.Pipeline` and `sklearn.pipeline.FeatureUnion`.
  - **Feature Names**: Verify `get_feature_names_out()` returns exact list of string names matching output columns.
  - **Edge Cases**:
    - Empty text string `""` -> finite zeros, no crash or division by zero.
    - Single character string `"A"` -> finite output.
    - String with zero punctuation -> finite output.
    - String with zero words (e.g. whitespace or punctuation only `"!?!?"`) -> finite output.
    - Multilingual / unicode text (e.g. Chinese characters, emojis) -> finite output.
    - Determinism: Repeated calls produce identical arrays.

## 5. Risk Assessment & Mitigations
- **Feature Extraction Latency**: Regex tokenization over thousands of texts can be slow if unoptimized.
  - *Mitigation*: Compile regular expressions at module level and rely on vectorized Python string methods (`count()`, `isupper()`) where possible.
- **Division by Zero**: Empty strings or texts with 0 words could cause ZeroDivisionError.
  - *Mitigation*: Defensive normalization and `np.nan_to_num`.

## 6. Rollback Plan
Revert git branch to `036a213` if unresolvable issues occur.
