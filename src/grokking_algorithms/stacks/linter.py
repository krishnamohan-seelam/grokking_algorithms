# add header comment
# This module provides a Linter class that uses a Matcher to check text for errors,
# specifically for balanced brackets. It includes a default BracketMatcher and allows
# for custom matchers to be implemented, adhering to the Open/Closed Principle. 

from collections import deque
from abc import ABC, abstractmethod

DEFAULT_BRACKET_PAIRS = {'(': ')', '{': '}', '[': ']'}



class Matcher(ABC):
    """Abstract base class for matchers used by the Linter."""
    @abstractmethod
    def match(self, text):
        """
        Analyze the given text and return a list of error messages.

        Args:
            text (str): The input text to be checked.

        Returns:
            list[str]: A list of error messages.
        """
        pass

class BracketMatcher(Matcher):
    """
    Matcher implementation that checks for balanced brackets in the text.
    """
    def __init__(self, pairs=None):
        """
        Initialize the BracketMatcher.

        Args:
            pairs (dict, optional): A dictionary of opening and closing bracket pairs.
        """
        self.pairs = pairs or DEFAULT_BRACKET_PAIRS
    
    def match(self, text):
        """
        Check the text for balanced brackets.

        Args:
            text (str): The input text to be checked.

        Returns:
            list[str]: A list of error messages. Returns an empty list if no errors are found.
        """
        stack = deque()
        errors = []
        for index, char in enumerate(text):
            if char in self.pairs:
                stack.append((char, index))
            elif char in self.pairs.values():
                if not stack:
                    errors.append(f"Unmatched closing '{char}' at index {index}")
                else:
                    last_open, last_index = stack.pop()
                    if self.pairs[last_open] != char:
                        errors.append(f"Mismatched '{last_open}' at index {last_index} with '{char}' at index {index}")
        while stack:
            last_open, last_index = stack.pop()
            errors.append(f"Unmatched opening '{last_open}' at index {last_index}")
        return errors

class Linter:
    """
    Linter class that uses a Matcher to check text for errors.

    Usage:
        >>> from grokking_algorithms.stacks.linter import Linter, BracketMatcher
        >>> linter = Linter(BracketMatcher())
        >>> errors = linter.lint("if (x > 0) { return [x]; }")
        >>> if not errors:
        ...     print("No errors found")
        ... else:
        ...     for error in errors:
        ...         print(error)
    """
    def __init__(self, matcher: Matcher):
        """
        Initialize the Linter with a matcher.

        Args:
            matcher (Matcher): The matcher to use for linting.
        """
        self.matcher = matcher

    def lint(self, text):
        """
        Lint the given text using the configured matcher.

        Args:
            text (str): The input text to be checked.

        Returns:
            list[str]: A list of error messages.
        """
        return self.matcher.match(text)


