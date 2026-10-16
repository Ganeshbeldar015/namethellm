"""Multi-view Stylegram classifier combining lexical, character, casing shape, and function syntax."""

from typing import Iterable, Sequence
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from namethellm.features.stylometry import StylometricFeatureExtractor
from namethellm.features.text_transforms import function_text, shape_text


class StylegramClassifier(BaseEstimator, ClassifierMixin):
    """Multi-view topic-invariant text attribution classifier.

    Extracts 5 complementary views:
      1. Word-level n-grams with punctuation tokens (weight 0.8)
      2. Character boundary n-grams (weight 1.0)
      3. Casing shape character n-grams (weight 0.5)
      4. Topic-stripped function word syntax n-grams (weight 0.5)
      5. Standardized 46-dimensional stylometric features (weight 0.5)

    Solves with balanced-class regularized logistic regression.
    """

    def __init__(
        self,
        C: float = 1.2,
        max_iter: int = 500,
        random_state: int = 42,
    ) -> None:
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state

        self.word_vec = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=12000,
            sublinear_tf=True,
            min_df=1,
            token_pattern=r"(?u)\b\w+\b|[^\w\s]",
        )
        self.char_vec = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            max_features=18000,
            sublinear_tf=True,
            min_df=1,
        )
        self.shape_vec = TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 6),
            max_features=10000,
            sublinear_tf=True,
            min_df=1,
        )
        self.func_vec = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=10000,
            sublinear_tf=True,
            min_df=1,
            token_pattern=r"(?u)\b\w+\b|[^\w\s]",
        )
        self.stylo_pipe = Pipeline(
            [
                ("extractor", StylometricFeatureExtractor()),
                ("scaler", StandardScaler()),
            ]
        )
        self.clf = LogisticRegression(
            C=self.C,
            max_iter=self.max_iter,
            solver="lbfgs",
            class_weight="balanced",
            random_state=self.random_state,
        )

    def fit(
        self,
        X: Iterable[str],
        y: Sequence[str],
    ) -> "StylegramClassifier":
        """Fit all 5 feature views and the multi-class linear classifier."""
        X_list = list(X)
        w_feat = self.word_vec.fit_transform(X_list) * 0.8
        c_feat = self.char_vec.fit_transform(X_list) * 1.0
        s_feat = self.shape_vec.fit_transform(shape_text(X_list)) * 0.5
        f_feat = self.func_vec.fit_transform(function_text(X_list)) * 0.5
        stylo_feat = self.stylo_pipe.fit_transform(X_list) * 0.5

        X_all = hstack([w_feat, c_feat, s_feat, f_feat, stylo_feat], format="csr")
        self.clf.fit(X_all, y)
        self.classes_ = self.clf.classes_
        return self

    def predict(self, X: Iterable[str]) -> np.ndarray:
        """Predict model labels for input passages."""
        X_all = self._transform_all(X)
        return self.clf.predict(X_all)

    def predict_proba(self, X: Iterable[str]) -> np.ndarray:
        """Predict class probability distributions."""
        X_all = self._transform_all(X)
        return self.clf.predict_proba(X_all)

    def _transform_all(self, X: Iterable[str]) -> csr_matrix:
        X_list = list(X)
        w_feat = self.word_vec.transform(X_list) * 0.8
        c_feat = self.char_vec.transform(X_list) * 1.0
        s_feat = self.shape_vec.transform(shape_text(X_list)) * 0.5
        f_feat = self.func_vec.transform(function_text(X_list)) * 0.5
        stylo_feat = self.stylo_pipe.transform(X_list) * 0.5
        return hstack([w_feat, c_feat, s_feat, f_feat, stylo_feat], format="csr")
