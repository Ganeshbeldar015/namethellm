# ADR-0001: GroupKFold Cross-Validation on prompt_id

## Status
Accepted

## Context
In the training data, 2,699 passages are written for 150 prompt IDs. The test set passages are generated from prompts that do not appear in the training data. If validation splits randomly split passages, passages from the same prompt will be in both train and validation folds, causing models to overfit on prompt topic rather than authoring model stylistic fingerprints.

## Decision
Use `GroupKFold` (or `StratifiedGroupKFold`) strictly grouping by `prompt_id`.

## Consequences
Validation scores will accurately reflect generalization to unseen prompts, mirroring the Kaggle test evaluation setup.
