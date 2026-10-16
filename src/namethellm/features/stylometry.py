"""Stylometric and structural feature extraction for LLM authorship attribution."""

import collections
import re
import string
from typing import Any, Iterable, Optional, Sequence
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

_SENTENCE_SPLIT_REGEX = re.compile(r"[.!?]+(?:\s+|$)")
_WORD_SPLIT_REGEX = re.compile(r"\b\w+\b")
_MARKDOWN_BULLET_REGEX = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
_MARKDOWN_HEADER_REGEX = re.compile(r"^\s*#{1,6}\s+", re.MULTILINE)
_MARKDOWN_NUMBERED_REGEX = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)

# Signature LLM discourse markers and lexical preferences
_DISCOURSE_WORDS = [
    "delve",
    "furthermore",
    "moreover",
    "testament",
    "crucial",
    "essential",
    "notably",
    "essentially",
    "consequently",
    "tapestry",
    "comprehensive",
    "overall",
]

_PUNCTUATION_SET = set(string.punctuation)


class StylometricFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract topic-invariant stylometric, punctuation, and structural features.

    Computes 46 quantitative metrics capturing:
      - Length and sentence density metrics
      - Character casing and type distributions
      - Punctuation frequencies per 1,000 characters
      - Lexical diversity (TTR, hapax legomena) and word lengths
      - Markdown and document formatting cues
      - Frontier LLM discourse marker signatures

    Guarantees:
      - Output is a 2D numpy array of float64.
      - Strictly 0 NaNs and 0 infinite values.
      - Safe handling of empty, whitespace, and edge-case inputs.
    """

    def __init__(self) -> None:
        self.feature_names_: list[str] = [
            # 1. Length & Density (8)
            "char_count",
            "word_count",
            "sentence_count",
            "line_count",
            "avg_word_length",
            "avg_sentence_length_words",
            "avg_sentence_length_chars",
            "sentence_length_std",
            # 2. Character Ratios (5)
            "uppercase_ratio",
            "lowercase_ratio",
            "digit_ratio",
            "whitespace_ratio",
            "punctuation_ratio",
            # 3. Punctuation Frequencies per 1k chars (13)
            "comma_freq",
            "period_freq",
            "semicolon_freq",
            "colon_freq",
            "exclamation_freq",
            "question_freq",
            "hyphen_freq",
            "em_dash_freq",
            "quotes_freq",
            "parentheses_freq",
            "brackets_freq",
            "ellipsis_freq",
            "asterisk_freq",
            # 4. Lexical Richness (4)
            "type_token_ratio",
            "hapax_ratio",
            "short_words_ratio",
            "long_words_ratio",
            # 5. Markdown & Structure (4)
            "markdown_header_count",
            "markdown_bullet_count",
            "markdown_numbered_count",
            "backtick_count",
            # 6. Discourse Marker Frequencies per 1k words (12)
            *[f"discourse_{w}" for w in _DISCOURSE_WORDS],
        ]

    def fit(self, X: Any, y: Optional[Any] = None) -> "StylometricFeatureExtractor":
        """No-op fit method for scikit-learn compatibility."""
        return self

    def transform(self, X: Iterable[str]) -> np.ndarray:
        """Extract stylometric feature vectors for an iterable of text passages.

        Args:
          X: Iterable of input text passages.

        Returns:
          2D numpy array of shape (n_samples, n_features) with strictly finite values.
        """
        rows = [self._extract_single(text) for text in X]
        if not rows:
            return np.empty((0, len(self.feature_names_)), dtype=np.float64)

        arr = np.array(rows, dtype=np.float64)
        return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)

    def get_feature_names_out(
        self, input_features: Optional[Sequence[str]] = None
    ) -> list[str]:
        """Return names of all extracted features."""
        return list(self.feature_names_)

    def _extract_single(self, text: str) -> list[float]:
        if not isinstance(text, str) or not text.strip():
            return [0.0] * len(self.feature_names_)

        char_count = float(len(text))
        safe_char_denom = max(char_count, 1.0)

        # Tokens and sentences
        words = _WORD_SPLIT_REGEX.findall(text)
        word_count = float(len(words))
        safe_word_denom = max(word_count, 1.0)

        raw_sentences = [s.strip() for s in _SENTENCE_SPLIT_REGEX.split(text) if s.strip()]
        sentence_count = float(max(len(raw_sentences), 1 if word_count > 0 else 0))
        safe_sent_denom = max(sentence_count, 1.0)

        line_count = float(text.count("\n") + 1)

        # Length & Density
        avg_word_length = (
            sum(len(w) for w in words) / safe_word_denom if word_count > 0 else 0.0
        )
        avg_sentence_length_words = word_count / safe_sent_denom
        avg_sentence_length_chars = char_count / safe_sent_denom

        if raw_sentences:
            words_per_sent = [
                float(len(_WORD_SPLIT_REGEX.findall(s))) for s in raw_sentences
            ]
            sent_std = float(np.std(words_per_sent))
        else:
            sent_std = 0.0

        # Character Ratios
        upper_count = sum(1 for c in text if c.isupper())
        lower_count = sum(1 for c in text if c.islower())
        digit_count = sum(1 for c in text if c.isdigit())
        space_count = sum(1 for c in text if c.isspace())
        punct_count = sum(1 for c in text if c in _PUNCTUATION_SET)

        uppercase_ratio = upper_count / safe_char_denom
        lowercase_ratio = lower_count / safe_char_denom
        digit_ratio = digit_count / safe_char_denom
        whitespace_ratio = space_count / safe_char_denom
        punctuation_ratio = punct_count / safe_char_denom

        # Punctuation Frequencies per 1k chars
        norm_factor = 1000.0 / safe_char_denom
        comma_freq = text.count(",") * norm_factor
        period_freq = text.count(".") * norm_factor
        semicolon_freq = text.count(";") * norm_factor
        colon_freq = text.count(":") * norm_factor
        exclamation_freq = text.count("!") * norm_factor
        question_freq = text.count("?") * norm_factor
        hyphen_freq = text.count("-") * norm_factor
        em_dash_freq = (text.count("—") + text.count("–")) * norm_factor
        quotes_freq = (
            text.count('"')
            + text.count("'")
            + text.count("“")
            + text.count("”")
            + text.count("‘")
            + text.count("’")
        ) * norm_factor
        parentheses_freq = (text.count("(") + text.count(")")) * norm_factor
        brackets_freq = (
            text.count("[") + text.count("]") + text.count("{") + text.count("}")
        ) * norm_factor
        ellipsis_freq = (text.count("...") + text.count("…")) * norm_factor
        asterisk_freq = text.count("*") * norm_factor

        # Lexical Richness
        words_lower = [w.lower() for w in words]
        if words_lower:
            counts = collections.Counter(words_lower)
            ttr = float(len(counts)) / safe_word_denom
            hapax_ratio = sum(1 for c in counts.values() if c == 1) / safe_word_denom
            short_words_ratio = sum(1 for w in words if len(w) <= 3) / safe_word_denom
            long_words_ratio = sum(1 for w in words if len(w) >= 7) / safe_word_denom
        else:
            ttr = 0.0
            hapax_ratio = 0.0
            short_words_ratio = 0.0
            long_words_ratio = 0.0

        # Markdown & Structure
        md_header_count = float(len(_MARKDOWN_HEADER_REGEX.findall(text)))
        md_bullet_count = float(len(_MARKDOWN_BULLET_REGEX.findall(text)))
        md_numbered_count = float(len(_MARKDOWN_NUMBERED_REGEX.findall(text)))
        backtick_count = float(text.count("`"))

        # Discourse markers per 1k words
        word_norm = 1000.0 / safe_word_denom
        words_set_counts = collections.Counter(words_lower)
        discourse_vals = [
            float(words_set_counts.get(w, 0)) * word_norm for w in _DISCOURSE_WORDS
        ]

        return [
            char_count,
            word_count,
            sentence_count,
            line_count,
            avg_word_length,
            avg_sentence_length_words,
            avg_sentence_length_chars,
            sent_std,
            uppercase_ratio,
            lowercase_ratio,
            digit_ratio,
            whitespace_ratio,
            punctuation_ratio,
            comma_freq,
            period_freq,
            semicolon_freq,
            colon_freq,
            exclamation_freq,
            question_freq,
            hyphen_freq,
            em_dash_freq,
            quotes_freq,
            parentheses_freq,
            brackets_freq,
            ellipsis_freq,
            asterisk_freq,
            ttr,
            hapax_ratio,
            short_words_ratio,
            long_words_ratio,
            md_header_count,
            md_bullet_count,
            md_numbered_count,
            backtick_count,
            *discourse_vals,
        ]
