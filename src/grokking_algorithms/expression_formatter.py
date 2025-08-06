import re
from abc import ABC, abstractmethod

# --- Expression Base Classes ---


class Expression(ABC):
    """
    Abstract base class for all expression nodes in the expression tree.
    All subclasses must implement the format method, which returns a string representation of the expression.
    """

    @abstractmethod
    def format(self, parent_prec=0):
        """
        Format the expression as a string, adding parentheses as needed based on operator precedence.
        Args:
            parent_prec (int): The precedence of the parent operator.
        Returns:
            str: The formatted string representation of the expression.
        """
        pass


class Value(Expression):
    """
    Represents a literal value (number) in the expression.
    """

    def __init__(self, val):
        """
        Args:
            val (str): The value as a string (e.g., '42', '3.14').
        """
        self.val = val

    def format(self, parent_prec=0):
        """
        Returns the string representation of the value.
        """
        return str(self.val)


class Variable(Expression):
    """
    Represents a variable (identifier) in the expression.
    """

    def __init__(self, name):
        """
        Args:
            name (str): The variable name.
        """
        self.name = name

    def format(self, parent_prec=0):
        """
        Returns the variable name as a string.
        """
        return self.name


class UnaryOp(Expression):
    """
    Represents a unary operation (e.g., -a, abs(a)) in the expression.
    """

    def __init__(self, op, operand):
        """
        Args:
            op (str): The unary operator or function name.
            operand (Expression): The operand expression.
        """
        self.op = op
        self.operand = operand

    def format(self, parent_prec=0):
        """
        Formats the unary operation as a string, e.g., '-(a)' or 'abs(a)'.
        """
        # Unary operators like - and functions like abs(), round()
        # Always format as op(expr), with parentheses after operator for clarity
        return f"{self.op}({self.operand.format()})"


class BinaryOp(Expression):
    """
    Represents a binary operation (e.g., a + b, a * b) in the expression.
    Handles operator precedence and associativity for correct parenthesization.
    """

    def __init__(self, left, op, right):
        """
        Args:
            left (Expression): The left operand.
            op (str): The binary operator.
            right (Expression): The right operand.
        """
        self.left = left
        self.op = op
        self.right = right

    def format(self, parent_prec=0):
        """
        Formats the binary operation as a string, adding parentheses as needed based on precedence.
        """
        op_prec, assoc = OperatorMeta.get(self.op)

        # Helper function to decide if child should be parenthesized
        def must_parenthesize(child, child_side):
            if isinstance(child, BinaryOp):
                child_prec, _ = OperatorMeta.get(child.op)
                # Parenthesize if child's precedence is greater than current op
                if child_prec > op_prec:
                    return True
                # If same precedence and it conflicts with associativity, parenthesize
                if child_prec == op_prec:
                    if (assoc == "L" and child_side == "right") or (
                        assoc == "R" and child_side == "left"
                    ):
                        return True
            # Parenthesize for UnaryOp if appropriate (usually not necessary)
            return False

        # Format left and right sub-expressions with adjusted precedence context
        # +1 or same precedence depending on associativity, to manage chains properly
        left_fmt = self.left.format(op_prec if assoc == "L" else op_prec + 1)
        right_fmt = self.right.format(op_prec + 1 if assoc == "L" else op_prec)

        if must_parenthesize(self.left, "left"):
            left_fmt = f"({left_fmt})"
        if must_parenthesize(self.right, "right"):
            right_fmt = f"({right_fmt})"

        expr_str = f"{left_fmt} {self.op} {right_fmt}"

        # Parenthesize if current op precedence is less than parent precedence
        if op_prec < parent_prec:
            return f"({expr_str})"
        return expr_str


# --- Operator Metadata ---


class OperatorMeta:
    """
    Stores metadata about supported operators, including their precedence and associativity.
    Provides methods to query operator properties.
    """

    # Map operator -> (precedence, associativity)
    OPERATORS = {
        "or": (1, "L"),
        "and": (2, "L"),
        "not": (3, "R"),  # if you support unary not
        "==": (4, "L"),
        "!=": (4, "L"),
        "<": (5, "L"),
        ">": (5, "L"),
        "<=": (5, "L"),
        ">=": (5, "L"),
        "+": (5, "L"),
        "-": (5, "L"),
        "*": (6, "L"),
        "/": (6, "L"),
        "%": (6, "L"),
        "**": (7, "R"),  # exponentiation is right-associative
    }

    @classmethod
    def get(cls, op):
        """
        Returns the precedence and associativity for the given operator.
        Args:
            op (str): The operator.
        Returns:
            tuple: (precedence, associativity)
        Raises:
            ValueError: If the operator is not supported.
        """
        if op not in cls.OPERATORS:
            raise ValueError(f"Unknown operator: {op}")
        return cls.OPERATORS[op]

    @classmethod
    def contains(cls, op):
        """
        Checks if the operator is supported.
        Args:
            op (str): The operator.
        Returns:
            bool: True if supported, False otherwise.
        """
        return op in cls.OPERATORS


# --- Tokenizer ---


TOKEN_SPEC = [
    ("SKIP", r"[ \t]+"),
    ("OP", r"\b(?:and|or|not|is|in)\b|==|!=|<=|>=|\*\*|[+\-*/%<>=()]"),
    ("NUMBER", r"\d+(\.\d*)?"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("COMMA", r","),
    ("UNKNOWN", r"."),
]


def tokenize(expression):
    """
    Tokenizes the input expression string into a sequence of (kind, value) pairs.
    Args:
        expression (str): The input expression string.
    Yields:
        tuple: (token kind, token value)
    Raises:
        SyntaxError: If an unknown character is encountered.
    """
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    for match in re.finditer(regex, expression):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        elif kind == "UNKNOWN":
            raise SyntaxError(f"Unexpected character: {value}")
        yield (kind, value)


# --- Parser ---


class Parser:
    """
    Parses a tokenized expression string into an expression tree (AST).
    Supports operator precedence, associativity, parentheses, and function calls.
    """

    def __init__(self, expression):
        """
        Args:
            expression (str): The input expression string.
        """
        self.tokens = list(tokenize(expression))
        self.pos = 0

    def current(self):
        """
        Returns the current token as a (kind, value) tuple.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def advance(self):
        """
        Advances to the next token.
        """
        self.pos += 1

    def expect(self, kind, value=None):
        """
        Consumes the current token if it matches the expected kind (and value, if provided).
        Raises SyntaxError if not matched.
        """
        tok_kind, tok_val = self.current()
        if tok_kind != kind or (value is not None and tok_val != value):
            raise SyntaxError(f"Expected {kind} {value}, got {tok_kind} {tok_val}")
        self.advance()

    def parse(self):
        """
        Parses the entire expression and returns the root Expression node.
        Raises SyntaxError if extra tokens remain.
        """
        result = self.parse_expression()
        if self.current()[0] != "EOF":
            raise SyntaxError("Unexpected token after end of expression")
        return result

    def parse_expression(self, min_prec=1):
        """
        Parses an expression with respect to operator precedence.
        Args:
            min_prec (int): The minimum precedence to consider.
        Returns:
            Expression: The parsed expression node.
        """
        node = self.parse_primary()

        while True:
            tok_kind, tok_val = self.current()

            # Only parse operators defined in OperatorMeta
            if tok_kind == "OP" and OperatorMeta.contains(tok_val):
                prec, assoc = OperatorMeta.get(tok_val)
                if prec < min_prec:
                    break
                self.advance()
                next_min_prec = prec + 1 if assoc == "L" else prec
                right = self.parse_expression(next_min_prec)
                node = BinaryOp(node, tok_val, right)
            else:
                break
        return node

    def parse_primary(self):
        """
        Parses a primary expression: number, variable, parenthesized expression, or function call.
        Returns:
            Expression: The parsed primary expression node.
        Raises:
            SyntaxError: If an unexpected token is encountered.
        """
        tok_kind, tok_val = self.current()

        if tok_kind == "NUMBER":
            self.advance()
            return Value(tok_val)
        elif tok_kind == "ID":
            self.advance()
            # Check for function call
            if self.current()[1] == "(":
                self.advance()  # skip '('
                args = []
                if self.current()[1] != ")":
                    args.append(self.parse_expression())
                    while self.current()[1] == ",":
                        self.advance()
                        args.append(self.parse_expression())
                self.expect("OP", ")")
                # For this formatter, we use UnaryOp for single-arg functions or custom class for multiple args
                # We'll format multi-arg functions with commas
                if len(args) == 1:
                    return UnaryOp(tok_val, args[0])
                else:
                    # Create a FuncCall with multiple arguments
                    return FuncCall(tok_val, args)
            else:
                return Variable(tok_val)
        elif tok_kind == "OP":
            if tok_val == "(":
                self.advance()
                node = self.parse_expression()
                self.expect("OP", ")")
                return node
            elif tok_val == "-":
                self.advance()
                operand = self.parse_primary()
                return UnaryOp("-", operand)
            else:
                raise SyntaxError(f"Unexpected operator {tok_val} in primary")
        else:
            raise SyntaxError(f"Unexpected token {tok_kind} {tok_val}")


# --- Function call with multiple arguments support ---


class FuncCall(Expression):
    """
    Represents a function call with multiple arguments (e.g., round(a + b, 2)).
    """

    def __init__(self, name, args):
        """
        Args:
            name (str): The function name.
            args (list[Expression]): List of argument expressions.
        """
        self.name = name
        self.args = args

    def format(self, parent_prec=0):
        """
        Formats the function call as a string, e.g., 'round(a + b, 2)'.
        """
        args_str = ", ".join(arg.format() for arg in self.args)
        return f"{self.name}({args_str})"


# --- Main Formatter Class ---


class ExpressionFormatter:
    """
    Main class for formatting expressions.
    Parses the input string and provides a formatted string representation with correct parentheses.
    """

    def __init__(self, expr_string):
        """
        Args:
            expr_string (str): The input expression string.
        """
        self.expr_string = expr_string
        self.expression = Parser(expr_string).parse()

    def format(self):
        """
        Returns the formatted string representation of the parsed expression.
        """
        return self.expression.format(parent_prec=0)


# --- For Manual Testing ---

if __name__ == "__main__":
    tests = [
        ("a + b * c", "a + (b * c)"),
        ("a * b + c", "(a * b) + c"),
        ("a ** b * c", "(a ** b) * c"),
        ("a ** b ** c", "a ** (b ** c)"),
        ("abs(a + b * c)", "abs(a + (b * c))"),
        ("-a + b", "(-a) + b"),
        ("round(a + b, 2)", "round(a + b, 2)"),
        ("a and b or c", "(a and b) or c"),
        ("a == b and c", "(a == b) and c"),
        ("(a + b) * c", "(a + b) * c"),
        ("(a + b) ** c", "(a + b) ** c"),
        ("a + b + c", "a + b + c"),
        ("a * (b + c)", "a * (b + c)"),
        ("-abs(a - b)", "-(abs(a - b))"),
    ]

    for expr, expected in tests:
        fmt = ExpressionFormatter(expr)
        output = fmt.format()
        print(f"Expression: {expr}")
        print(f"Formatted : {output}")
        print(f"Expected  : {expected}")
        print(f"Match     : {output == expected}")
        print("-" * 40)
