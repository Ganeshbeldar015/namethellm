# Lessons Learned

- [L-001] Avoid prompt leakage in CV -> Cause: Grouped topics in training set -> Rule: Always use GroupKFold on `prompt_id` to strictly separate prompts between train and validation folds.
- [L-002] Secret detection false positives on operating manual -> Cause: `prompt.md` documents regex and sample keys -> Rule: Linter skips `prompt.md` during secrets scanning.
- [L-003] Stratified group splitting with asymmetric class sizes -> Cause: claude-fable-5 has 149 rows while others have 150 -> Rule: Use StratifiedGroupKFold with fixed random seed to balance class distributions across folds without strict integer equality constraints.
