import pytest
from grokking_algorithms.stacks.linter import Linter, BracketMatcher, Matcher

@pytest.fixture
def linter():
    return Linter(BracketMatcher())

def test_balanced_parentheses(linter):
    text = "(a + b) * [c - d] {e / f}"
    result = linter.lint(text)
    assert result == []

def test_unmatched_opening_parenthesis(linter):
    text = "(a + b"
    result = linter.lint(text)
    assert any("Unmatched opening '('" in err for err in result)

def test_unmatched_closing_bracket(linter):
    text = "a + b]"
    result = linter.lint(text)
    assert any("Unmatched closing ']'" in err for err in result)

def test_mismatched_brackets(linter):
    text = "[a + b)"
    result = linter.lint(text)
    assert any("Mismatched '[' at index 0 with ')' at index 6" in err for err in result)

def test_multiple_errors(linter):
    text = "(a + [b - c}"
    result = linter.lint(text)
    assert any("Mismatched '['" in err or "Unmatched opening '('" in err for err in result)

def test_empty_string(linter):
    text = ""
    result = linter.lint(text)
    assert result == []

def test_nested_brackets(linter):
    text = "{[(())]}"
    result = linter.lint(text)
    assert result == []

def test_only_opening_brackets(linter):
    text = "(({{[["
    result = linter.lint(text)
    assert all("Unmatched opening" in err for err in result)

def test_only_closing_brackets(linter):
    text = "))}}]]"
    result = linter.lint(text)
    assert all("Unmatched closing" in err for err in result)

# Additional test for custom matcher (Open/Closed Principle)
class DummyMatcher(Matcher):
    def match(self, text):
        """Always returns a dummy error message."""
        return ["Dummy matcher always returns this"]

def test_custom_matcher():
    linter = Linter(DummyMatcher())
    result = linter.lint("any text")
    assert result == ["Dummy matcher always returns this"]