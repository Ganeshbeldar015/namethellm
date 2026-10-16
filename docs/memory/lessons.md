# Lessons Learned

- [L-001] Avoid prompt leakage in CV -> Cause: Grouped topics in training set -> Rule: Always use GroupKFold on `prompt_id` to strictly separate prompts between train and validation folds.
- [L-002] Secret detection false positives on operating manual -> Cause: `prompt.md` documents regex and sample keys -> Rule: Linter skips `prompt.md` during secrets scanning.
- [L-003] Stratified group splitting with asymmetric class sizes -> Cause: claude-fable-5 has 149 rows while others have 150 -> Rule: Use StratifiedGroupKFold with fixed random seed to balance class distributions across folds without strict integer equality constraints.
- [L-004] Baseline TF-IDF parameter tuning -> Cause: Setting min_df > 1 causes vectorizer pruning errors on small unit test corpora -> Rule: Use min_df=1 for vectorizers to handle arbitrary batch sizes safely while bounding memory via max_features.
- [L-005] Defensive submission validation ordering -> Cause: Checking value equality or array comparisons before checking null/NaN triggers assertion errors or index mismatches -> Rule: Always validate null/NaN values across all columns before performing element-wise comparisons or set inclusion.
- [L-006] Fast stylometric feature extraction -> Cause: Calling heavy regex or NLP parsers across thousands of rows can exceed inference time budgets -> Rule: Precompile lightweight regexes, use Python native string counters, and vectorize ratios with NumPy zero-safe denominators to achieve sub-second extraction.
- [L-007] Stylometric feature synergy with linear classifiers vs trees -> Cause: High-dimensional word/character n-grams (30,000 features) preserve granular authorship tokens that tree ensembles compress or discard in SVD projection -> Rule: Combining sparse TF-IDF with standardized dense stylometric features in an L2-regularized linear model with balanced class weights yields superior performance over tree ensembles on text authorship attribution.
- [L-008] Topic-invariant syntax and casing representations -> Cause: Models overfit to topical themes across prompts when relying strictly on standard lexical n-grams -> Rule: Encoding structural casing morphology ('shape_text') and stripping content words to preserve closed-class function word syntax ('function_text') significantly boosts cross-prompt generalization (+0.0426 balanced accuracy).




