"""Constants, valid labels, and schema column definitions."""

from typing import Final

VALID_MODELS: Final[list[str]] = [
    "gpt-5.5",
    "gpt-5.6-luna",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-6-astra",
    "gemini-3.1-pro-preview",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "claude-fable-5",
    "claude-opus-4-6",
    "claude-opus-4-8",
    "claude-opus-5",
    "claude-sonnet-5",
    "qwen3.8-max",
    "glm-5.3",
    "glm-5.3-flash",
    "kimi-k3",
]

VALID_MODELS_SET: Final[set[str]] = set(VALID_MODELS)

TRAIN_COLUMNS: Final[list[str]] = ["id", "prompt_id", "text", "model"]
TEST_COLUMNS: Final[list[str]] = ["id", "text"]
SUBMISSION_COLUMNS: Final[list[str]] = ["id", "model"]
