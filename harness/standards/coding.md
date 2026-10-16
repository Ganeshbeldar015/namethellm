# Coding Standards

1. **Python 3.10+ Compatibility**: Code must run seamlessly in both Python 3.10+ and standard Kaggle notebook environments.
2. **Type Annotations**: All public module functions and class methods must have explicit PEP 484 type annotations.
3. **No Wildcard Imports**: Always import explicit classes and functions (e.g. `from sklearn.metrics import balanced_accuracy_score`).
4. **Formatting & Linting**: Follow PEP 8 guidelines. Lines <= 100 characters where practical.
5. **Deterministic Randomness**: Any function using stochastic components or model training must accept a `seed: int = 42` parameter and set numpy/torch random states.
6. **Leakage Prevention**: Transformations (scalers, encoders, TF-IDF vectorizers) must be fitted strictly on training fold splits and never on out-of-fold validation or test data.
