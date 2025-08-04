# Grokking Algorithms

Grokking Algorithms is a project designed to provide a comprehensive understanding of algorithms through practical examples and implementations in Python. This project aims to simplify complex algorithmic concepts and make them accessible to everyone.

## Installation

To install the necessary dependencies for this project, you can use the following command:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the dependencies listed in `pyproject.toml` using:

```bash
pip install .
```

## Usage

To run the main application, execute the following command:

```bash
python src/grokking_algorithms/main.py
```

## Testing

To run the tests for this project, you can use the following command:

```bash
pytest tests/test_main.py
```
## Formulex 

FormulEx (Formula Expression) is a module for parsing, formatting, and manipulating mathematical expressions. It provides a clean way to handle expressions with proper operator precedence and parentheses placement.

### Purpose and Need

FormulEx addresses several common needs when working with mathematical expressions:

1. **Parsing expressions**: Converting string expressions like `a+b*c` into structured representations
2. **Formatting with proper precedence**: Ensuring expressions are unambiguous by adding parentheses where needed
3. **Expression manipulation**: Providing a tree structure that can be traversed and modified

This is particularly useful for:
- Educational tools that teach algebraic concepts
- Code that generates or manipulates mathematical formulas
- Applications that need to parse user-provided expressions

### Design and Architecture

FormulEx uses a three-part design:

1. **Expression Model**: `ExpressionNode` class represents nodes in an expression tree, with each node being either an operand or an operator with left and right child nodes.

2. **Parser**: `ExpressionParser` implements a recursive descent parser with precedence climbing to convert string expressions into expression trees.

3. **Formatter**: `ExpressionFormatter` traverses the expression tree and formats it with appropriate parentheses based on operator precedence rules.

The module also includes an `Operator` enum that defines supported operators and their precedence levels.

### How It Works

1. **Parsing Process**:
   - The input expression is tokenized into individual components (variables, numbers, operators, parentheses)
   - The parser builds a tree structure where operators are nodes and operands are leaves
   - Operator precedence is handled during parsing to ensure the tree structure reflects the correct evaluation order

2. **Formatting Process**:
   - The formatter traverses the expression tree recursively
   - It adds parentheses based on operator precedence rules
   - For addition and subtraction, it adds parentheses to the right operand if it's an operator
   - For multiplication and division in the context of addition/subtraction, it adds parentheses to ensure proper precedence

### Usage Examples

#### Basic Usage

```python
from grokking_algorithms.formulex import ExpressionParser, ExpressionFormatter

# Parse an expression
expr = "a+b*c"
parser = ExpressionParser(expr)
tree = parser.parse()

# Format with appropriate parentheses
formatter = ExpressionFormatter()
result = formatter.format(tree)
print(result)  # Outputs: a+(b*c)
```

#### More Complex Examples

```python
# Format expressions with mixed operators
expressions = [
    "a*b+c/d",           # Becomes: (a*b)+(c/d)
    "a+(b-c)*d",         # Becomes: a+((b-c)*d)
    "x1*y2+(a-b/c)"      # Becomes: (x1*y2)+(a-(b/c))
]

for expr in expressions:
    parser = ExpressionParser(expr)
    tree = parser.parse()
    result = formatter.format(tree)
    print(f"{expr} → {result}")
```

### Benefits

- **Clarity**: Expressions are formatted with parentheses that make the intended order of operations clear
- **Correctness**: The parser handles operator precedence correctly, avoiding common mistakes
- **Flexibility**: The expression tree can be manipulated programmatically before formatting

FormulEx provides a solid foundation for working with mathematical expressions in a structured and reliable way.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.