"""Baseline TF-IDF and regularized linear multi-class classifier."""

from typing import Sequence, Union
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class BaselineTFIDFClassifier:
    """Baseline classifier combining word and subword char TF-IDF n-grams with LogisticRegression."""

    def __init__(
        self,
        c: float = 1.0,
        max_iter: int = 400,
        random_state: int = 42,
    ):
        self.c = c
        self.max_iter = max_iter
        self.random_state = random_state

        word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            max_features=12000,
            sublinear_tf=True,
        )

        char_vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            max_features=18000,
            sublinear_tf=True,
        )

        features = FeatureUnion([
            ("word_tfidf", word_vectorizer),
            ("char_tfidf", char_vectorizer),
        ])

        classifier = LogisticRegression(
            C=self.c,
            max_iter=self.max_iter,
            random_state=self.random_state,
            solver="lbfgs",
        )

        self.pipeline = Pipeline([
            ("features", features),
            ("clf", classifier),
        ])
        self.classes_: np.ndarray = np.array([])

    def fit(
        self,
        texts: Union[Sequence[str], pd.Series, np.ndarray],
        y: Union[Sequence[str], pd.Series, np.ndarray],
    ) -> "BaselineTFIDFClassifier":
        """Fits the vectorizer and classifier on text training passages."""
        self.pipeline.fit(texts, y)
        self.classes_ = self.pipeline.named_steps["clf"].classes_
        return self

    def predict(
        self,
        texts: Union[Sequence[str], pd.Series, np.ndarray],
    ) -> np.ndarray:
        """Predicts class labels for text passages."""
        return self.pipeline.predict(texts)

    def predict_proba(
        self,
        texts: Union[Sequence[str], pd.Series, np.ndarray],
    ) -> np.ndarray:
        """Predicts calibrated class probability distributions."""
        return self.pipeline.predict_proba(texts)
