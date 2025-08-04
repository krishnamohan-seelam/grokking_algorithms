import pytest
from grokking_algorithms.formulex import ExpressionParser, ExpressionFormatter  # Replace with actual module name

formatter = ExpressionFormatter()

def parse_and_format(expr):
    parser = ExpressionParser(expr)
    tree = parser.parse()
    return formatter.format(tree)

@pytest.mark.parametrize("expr, expected", [
    ("a+b", "a+b"),
    ("a+b*c", "a+(b*c)"),
    ("a*b+c/d", "(a*b)+(c/d)"),
    ("a+(b-c)*d", "a+((b-c)*d)"),
    ("(a+b)*(c-d)", "(a+b)*(c-d)"),
    ("var1+var2*count", "var1+(var2*count)"),
    ("x", "x"),
    ("x1*y2+(a-b/c)", "(x1*y2)+(a-(b/c))"),
    ("  a + b * c - d / e ", "a+(b*c)-(d/e)")
])
def test_expression_formatting(expr, expected):
    assert parse_and_format(expr) == expected