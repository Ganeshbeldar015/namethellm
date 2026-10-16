# Lessons Learned

- [L-001] Avoid prompt leakage in CV -> Cause: Grouped topics in training set -> Rule: Always use GroupKFold on `prompt_id` to strictly separate prompts between train and validation folds.
- [L-002] Secret detection false positives on operating manual -> Cause: `prompt.md` documents regex and sample keys -> Rule: Linter skips `prompt.md` during secrets scanning.
