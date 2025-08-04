import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class Operator(str, Enum):
    """Enumeration of supported mathematical operators.
    
    This enum defines the basic arithmetic operators and their precedence levels.
    Higher precedence operators are evaluated before lower precedence operators.
    """
    ADD = "+"
    SUBTRACT = "-" 
    MULTIPLY = "*"
    DIVIDE = "/"

    @property
    def precedence(self) -> int:
        """Get the precedence level of the operator.
        
        Returns:
            int: 1 for addition and subtraction (lower precedence)
                 2 for multiplication and division (higher precedence)
        """
        if self in (Operator.ADD, Operator.SUBTRACT):
            return 1
        return 2


@dataclass
class ExpressionNode:
    """A node in the expression parse tree.
    
    Each node represents either an operand (variable or number) or an operator.
    Operator nodes have left and right children representing the operands.
    """
    value: str
    left: Optional['ExpressionNode'] = None
    right: Optional['ExpressionNode'] = None

    @property
    def is_operator(self) -> bool:
        """Check if this node represents an operator.
        
        Returns:
            bool: True if the node is an operator, False if it's an operand
        """
        return self.value in {op.value for op in Operator}

    @property
    def precedence(self) -> int:
        """Get the precedence level of this node.
        
        Returns:
            int: 3 for operands (highest precedence)
                 1 or 2 for operators based on their type
        """
        if not self.is_operator:
            return 3  # Operand has highest precedence
        return Operator(self.value).precedence


class ExpressionParser:
    """Parser that converts a string expression into a parse tree.
    
    This class implements a recursive descent parser with precedence climbing
    to handle operator precedence correctly. It builds a tree structure where
    each node is an ExpressionNode representing either an operand or an operator.
    """
    def __init__(self, expression: str):
        """Initialize the parser with an expression string.
        
        Args:
            expression: The mathematical expression to parse
        """
        self._tokens: List[str] = self._tokenize(expression)
        self._position: int = 0

    @staticmethod
    def _tokenize(expr: str) -> List[str]:
        """Convert an expression string into a list of tokens.
        
        Args:
            expr: The expression string to tokenize
            
        Returns:
            List of tokens (operators, variables, numbers, parentheses)
        """
        token_pattern = r'[A-Za-z_][A-Za-z0-9_]*|\d+|[()+\-*/]'
        return re.findall(token_pattern, expr.replace(" ", ""))

    def parse(self) -> ExpressionNode:
        """Parse the expression and return the root node of the parse tree.
        
        Returns:
            The root ExpressionNode of the parsed expression tree
        """
        return self._parse_expression()

    def _parse_expression(self, min_precedence: int = 0) -> ExpressionNode:
        """Parse an expression with precedence climbing.
        
        This method implements the precedence climbing algorithm to ensure
        operators are associated with the correct operands based on precedence.
        
        Args:
            min_precedence: The minimum precedence level to consider
            
        Returns:
            An ExpressionNode representing the parsed expression
        """
        node = self._parse_term()

        while (self._has_remaining_tokens and 
               self._current_token in {op.value for op in Operator}):
            operator = self._current_token
            precedence = ExpressionNode(operator).precedence
            if precedence < min_precedence:
                break
            self._advance_position()
            right = self._parse_expression(precedence + 1)
            node = ExpressionNode(operator, node, right)

        return node

    def _parse_term(self) -> ExpressionNode:
        """Parse a term (operand or parenthesized expression).
        
        A term is either a variable/number or a parenthesized expression.
        
        Returns:
            An ExpressionNode representing the parsed term
        
        Raises:
            ValueError: If parentheses are mismatched
        """
        token = self._current_token
        self._advance_position()

        if token == "(":
            node = self._parse_expression()
            if not self._has_remaining_tokens or self._current_token != ")":
                raise ValueError("Mismatched parentheses")
            self._advance_position()
            return node
        
        return ExpressionNode(token)

    @property
    def _current_token(self) -> str:
        """Get the current token being processed.
        
        Returns:
            The current token string
        """
        return self._tokens[self._position]

    @property
    def _has_remaining_tokens(self) -> bool:
        """Check if there are more tokens to process.
        
        Returns:
            True if there are more tokens, False otherwise
        """
        return self._position < len(self._tokens)

    def _advance_position(self) -> None:
        """Move to the next token in the token list."""
        self._position += 1


class ExpressionFormatter:
    """Formatter that converts a parse tree into a formatted expression string.
    
    This class traverses the parse tree and adds parentheses according to
    operator precedence rules to ensure the expression is unambiguous.
    """
    def format(self, node: ExpressionNode, parent_precedence: int = 0) -> str:
        """Format an expression tree into a string with appropriate parentheses.
        
        This method recursively formats the expression tree, adding parentheses
        where needed to maintain the correct operator precedence and association.
        
        Args:
            node: The root node of the expression tree to format
            parent_precedence: The precedence of the parent node
            
        Returns:
            A formatted string representation of the expression
        """
        if not node.is_operator:
            return node.value

        left_formatted = self.format(node.left, node.precedence)
        right_formatted = self.format(node.right, node.precedence)
        
        # For addition and subtraction, we need special handling of parentheses
        if node.value in (Operator.ADD.value, Operator.SUBTRACT.value):
            # Add parentheses to left operand if it's a multiplication or division
            left_formatted = self._add_parentheses_if_needed(
                node.left, left_formatted, "*/")
            # Add parentheses to right operand if it's any operator
            right_formatted = self._add_parentheses_if_needed(
                node.right, right_formatted)
                
        expr = f"{left_formatted}{node.value}{right_formatted}"
        # Add parentheses around the entire expression if needed based on parent precedence
        return f"({expr})" if node.precedence < parent_precedence else expr

    @staticmethod
    def _add_parentheses_if_needed(node: ExpressionNode, 
                                 formatted: str, 
                                 specific_ops: str = "") -> str:
        """Add parentheses to a formatted expression if needed.
        
        Args:
            node: The node being formatted
            formatted: The already formatted string for this node
            specific_ops: If provided, only add parentheses if the node's operator
                         is in this string
                         
        Returns:
            The formatted string with parentheses added if needed
        """
        needs_parentheses = (node.is_operator and 
                           (not specific_ops or node.value in specific_ops))
        return f"({formatted})" if needs_parentheses else formatted


# 🧪 Example usage
if __name__ == "__main__":
    expr = input("Enter expression (e.g., a+b-c*d/e): ")
    parser = ExpressionParser(expr)
    tree = parser.parse()

    formatter = ExpressionFormatter()
    result = formatter.format(tree)

    print("Bracketed expression:", result)
