# Lessons Learned

- [L-001] Avoid prompt leakage in CV -> Cause: Grouped topics in training set -> Rule: Always use GroupKFold on `prompt_id` to strictly separate prompts between train and validation folds.
- [L-002] Secret detection false positives on operating manual -> Cause: `prompt.md` documents regex and sample keys -> Rule: Linter skips `prompt.md` during secrets scanning.
- [L-003] Stratified group splitting with asymmetric class sizes -> Cause: claude-fable-5 has 149 rows while others have 150 -> Rule: Use StratifiedGroupKFold with fixed random seed to balance class distributions across folds without strict integer equality constraints.
- [L-004] Baseline TF-IDF parameter tuning -> Cause: Setting min_df > 1 causes vectorizer pruning errors on small unit test corpora -> Rule: Use min_df=1 for vectorizers to handle arbitrary batch sizes safely while bounding memory via max_features.
