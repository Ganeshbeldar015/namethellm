"""Topic-invariant text transformations for isolating syntax and casing morphology."""

import re
from typing import Final, Sequence

_WORD_OR_PUNCT_REGEX: Final = re.compile(r"\w+|[^\w\s]")
_LETTERS_REGEX: Final = re.compile(r"[^\W\d_]+")

FUNCTION_WORDS: Final[set[str]] = set(
    "a an the and or but if while although because as so than that which who whom whose "
    "this these those it its they them their theirs he him his she her hers we us our ours "
    "you your yours i me my mine in on at to from with without for of by over under between "
    "through into about is are was were be been being have has had do does did can could will "
    "would shall should may might must not no nor all any some each every both either neither "
    "other another such only also just very too more most less least here there when where why "
    "how what whether then now still yet even much many few little".split()
)


def shape_text(texts: Sequence[str]) -> list[str]:
    """Abstract words to their casing pattern while preserving whitespace, digits, and punctuation.

    Uppercase-initial words become 'X'; lowercase words become 'x'.
    For example: 'Hello World!' -> 'X x!'
    """
    return [
        _LETTERS_REGEX.sub(lambda m: "X" if m.group(0)[0].isupper() else "x", text)
        for text in texts
    ]


def function_text(texts: Sequence[str]) -> list[str]:
    """Filter text to isolate closed-class function words and punctuation from topic semantics.

    Replaces open-class content words with the literal token 'CONTENT'.
    For example: 'This is a crucial test.' -> 'this is a CONTENT CONTENT .'
    """
    results: list[str] = []
    for text in texts:
        if not text or not text.strip():
            results.append("")
            continue
        tokens = _WORD_OR_PUNCT_REGEX.findall(text)
        transformed = [
            t.lower() if t.lower() in FUNCTION_WORDS or not t.isalnum() else "CONTENT"
            for t in tokens
        ]
        results.append(" ".join(transformed))
    return results
