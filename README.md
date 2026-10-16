# Name That LLM

Authorship attribution pipeline across 18 frontier LLMs using stylometry, NLP, and machine learning for the Kaggle Code Competition.

## Quickstart

### Installation
```bash
pip install -e .
```

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit

# Harness integrity self-test
python scripts/check_harness.py && python -m pytest tests/harness
```

### Baseline Model Evaluation
```bash
# Run 5-fold GroupKFold baseline evaluation
python -m namethellm.evaluate
```

### Model Performance
- **Sprint 1 Baseline (TF-IDF)**: OOF Balanced Accuracy = **0.3004**
- **Sprint 2 Hybrid (TF-IDF + Stylometry + Calibration)**: OOF Balanced Accuracy = **0.3304**
- **Sprint 3 Stylegram (Multi-View Casing, Syntax, Char/Word & Stylometry)**: OOF Balanced Accuracy = **0.3430** (+0.0426 gain)

### Submission Generation
```bash
# Generate validated submission.parquet for test data
python -m namethellm.submission
```

### API Usage
```python
from namethellm import data, split, metrics, submission
from namethellm.models.stylegram import StylegramClassifier

# Load dataset
train_df = data.load_train_data()
test_df = data.load_test_data()

# Fit multi-view stylegram classifier
clf = StylegramClassifier()
clf.fit(train_df["text"], train_df["model"])

# Generate verified Kaggle submission
sub_df = submission.generate_submission(clf, test_df, output_path="submission.parquet")
```

