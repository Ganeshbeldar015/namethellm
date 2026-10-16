"""Unit tests for text transformation functions (AC-004-a)."""

from namethellm.features.text_transforms import function_text, shape_text


def test_shape_text_casing_abstraction():
    """AC-004-a: shape_text correctly abstracts words into casing symbols."""
    inputs = [
        "Hello world!",
        "ALL CAPS",
        "lower case only.",
        "Mixed123 Numbers",
    ]
    outputs = shape_text(inputs)

    assert outputs[0] == "X x!"
    assert outputs[1] == "X X"
    assert outputs[2] == "x x x."
    assert "X" in outputs[3] or "x" in outputs[3]


def test_shape_text_edge_cases():
    """AC-004-a: shape_text safely handles empty strings and punctuation."""
    inputs = ["", "   ", "12345", "!@#$%^&*()"]
    outputs = shape_text(inputs)

    assert len(outputs) == 4
    assert outputs[0] == ""
    assert outputs[1] == "   "
    assert outputs[2] == "12345"
    assert outputs[3] == "!@#$%^&*()"


def test_function_text_syntax_isolation():
    """AC-004-a: function_text preserves function words and replaces content words."""
    inputs = [
        "This is a crucial test of the attribution pipeline.",
        "In fact, although it seemed complicated, it was simple.",
    ]
    outputs = function_text(inputs)

    # Function words: 'this', 'is', 'a', 'of', 'the' should be preserved (lowercased)
    assert "this is a CONTENT CONTENT of the CONTENT CONTENT ." in outputs[0]
    # Function words: 'in', 'although', 'it', 'it', 'was' preserved
    assert "in" in outputs[1] and "although" in outputs[1] and "was" in outputs[1]


def test_function_text_edge_cases():
    """AC-004-a: function_text safely handles empty strings and punctuation-only inputs."""
    inputs = ["", "   ", ".,;:!?"]
    outputs = function_text(inputs)

    assert outputs[0] == ""
    assert outputs[1] == ""
    assert outputs[2] == ". , ; : ! ?"
