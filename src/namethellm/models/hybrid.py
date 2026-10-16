"""Hybrid multi-class classifier combining TF-IDF n-grams with stylometric features."""

from typing import Any, Iterable, Optional, Sequence
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from namethellm.features.stylometry import StylometricFeatureExtractor


class HybridStyloClassifier(BaseEstimator, ClassifierMixin):
    """Hybrid classifier integrating lexical/character n-grams and 46 stylometric features.

    Architecture:
      - FeatureUnion:
        1. Sublinear word n-grams (1, 2) capped at 12,000 features.
        2. Sublinear char_wb n-grams (3, 5) capped at 18,000 features.
        3. Standardized stylometric metrics (46 features).
      - Estimator:
        L2-regularized LogisticRegression with balanced class weights.
    """

    def __init__(
        self,
        C: float = 1.2,
        max_iter: int = 400,
        random_state: int = 42,
    ) -> None:
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state

        self.pipeline = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            (
                                "word_tfidf",
                                TfidfVectorizer(
                                    ngram_range=(1, 2),
                                    max_features=12000,
                                    sublinear_tf=True,
                                    min_df=1,
                                ),
                            ),
                            (
                                "char_tfidf",
                                TfidfVectorizer(
                                    analyzer="char_wb",
                                    ngram_range=(3, 5),
                                    max_features=18000,
                                    sublinear_tf=True,
                                    min_df=1,
                                ),
                            ),
                            (
                                "stylo",
                                Pipeline(
                                    [
                                        ("extractor", StylometricFeatureExtractor()),
                                        ("scaler", StandardScaler()),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                (
                    "clf",
                    LogisticRegression(
                        C=self.C,
                        max_iter=self.max_iter,
                        solver="lbfgs",
                        class_weight="balanced",
                        random_state=self.random_state,
                    ),
                ),
            ]
        )

    def fit(
        self,
        X: Iterable[str],
        y: Sequence[str],
    ) -> "HybridStyloClassifier":
        """Fit the hybrid pipeline on text passages and target labels."""
        self.pipeline.fit(X, y)
        self.classes_ = self.pipeline.named_steps["clf"].classes_
        return self

    def predict(self, X: Iterable[str]) -> np.ndarray:
        """Predict model labels for given text passages."""
        return self.pipeline.predict(X)

    def predict_proba(self, X: Iterable[str]) -> np.ndarray:
        """Predict class probability distributions."""
        return self.pipeline.predict_proba(X)
