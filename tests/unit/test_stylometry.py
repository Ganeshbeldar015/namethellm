"""Unit tests for StylometricFeatureExtractor (AC-004-a)."""

import numpy as np
import pytest
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from namethellm.features.stylometry import StylometricFeatureExtractor


@pytest.fixture
def sample_texts() -> list[str]:
    return [
        "This is a standard English paragraph. It has two sentences! Furthermore, it is brief.",
        "# Markdown Heading\n- Bullet item one\n- Bullet item two\n\n```python\nprint('hello')\n```",
        "A passage with dialogue: 'Indeed,' she said—delving into the mysterious tapestry; moreover, crucial details followed...",
        "SHORT.",
        "1. First point.\n2. Second point.\n3. Third point with 100% precision and $50 budget.",
    ]


def test_stylometric_extractor_shape_and_features(sample_texts: list[str]):
    """AC-004-a: Extractor produces 2D array with >= 30 features matching get_feature_names_out."""
    extractor = StylometricFeatureExtractor()
    features = extractor.fit_transform(sample_texts)

    assert isinstance(features, np.ndarray)
    assert features.ndim == 2
    assert features.shape[0] == len(sample_texts)
    assert features.shape[1] >= 30

    feature_names = extractor.get_feature_names_out()
    assert len(feature_names) == features.shape[1]
    assert all(isinstance(name, str) for name in feature_names)


def test_stylometric_extractor_no_nans_or_infs(sample_texts: list[str]):
    """AC-004-a: Numerical feature vectors are strictly finite with zero NaNs or infs."""
    extractor = StylometricFeatureExtractor()
    features = extractor.fit_transform(sample_texts)

    assert not np.isnan(features).any(), "NaN values found in extracted features"
    assert not np.isinf(features).any(), "Infinite values found in extracted features"


def test_stylometric_extractor_edge_cases():
    """AC-004-a: Handles empty strings, whitespace, single characters, and pure punctuation."""
    edge_cases = [
        "",  # completely empty string
        "   \t\n   ",  # whitespace only
        "A",  # single character
        "!@#$%^&*()_+-=[]{}|;':\",./<>?",  # punctuation only
        "1234567890",  # numbers only
        "测试中文文本。这是一个测试句子！",  # non-ASCII unicode
        "word " * 500,  # repeated words
    ]

    extractor = StylometricFeatureExtractor()
    features = extractor.fit_transform(edge_cases)

    assert features.shape == (len(edge_cases), len(extractor.get_feature_names_out()))
    assert not np.isnan(features).any()
    assert not np.isinf(features).any()
    # Empty string should yield non-negative finite features (mostly 0.0)
    assert (features[0] >= 0.0).all()


def test_stylometric_extractor_pipeline_compatibility(sample_texts: list[str]):
    """AC-004-a: Compatible with scikit-learn FeatureUnion and Pipeline."""
    union = FeatureUnion(
        [
            ("tfidf", TfidfVectorizer(max_features=50)),
            ("stylo", StylometricFeatureExtractor()),
        ]
    )

    pipe = Pipeline([("features", union)])
    X = pipe.fit_transform(sample_texts)

    assert X.shape[0] == len(sample_texts)
    assert X.shape[1] > 50  # 50 TF-IDF features + stylometric features


def test_stylometric_extractor_discriminative_signals():
    """AC-004-a: Extracted features accurately distinguish specific stylistic signals."""
    markdown_text = ["# Header\n- Bullet 1\n- Bullet 2\n`code`"]
    plain_text = ["Just a simple continuous paragraph of regular text without markdown."]

    extractor = StylometricFeatureExtractor()
    md_feat = extractor.fit_transform(markdown_text)
    plain_feat = extractor.transform(plain_text)

    names = list(extractor.get_feature_names_out())
    bullet_idx = names.index("markdown_bullet_count")
    header_idx = names.index("markdown_header_count")

    assert md_feat[0, bullet_idx] > plain_feat[0, bullet_idx]
    assert md_feat[0, header_idx] > plain_feat[0, header_idx]
