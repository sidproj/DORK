import ast
import operator


class CalculatorTool:

    name = "calculator"

    description = (
        "Evaluate mathematical expressions involving numbers, "
        "addition, subtraction, multiplication, division, "
        "powers, modulo, and parentheses."
    )

    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate."
            }
        },
        "required": ["expression"]
    }

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def definition(cls):

        return {
            "type": "function",
            "function": {
                "name": cls.name,
                "description": cls.description,
                "parameters": cls.parameters,
            }
        }

    @classmethod
    def execute(cls, expression: str):

        print("Calculator expression:", expression)

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )

            result = cls._evaluate(tree.body)

            print("Calculator result:", result)

            return result

        except Exception as e:

            print("Calculator error:", e)

            raise ValueError(
                "Invalid mathematical expression"
            )

    @classmethod
    def _evaluate(cls, node):

        # Numbers
        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Invalid constant")

        # Binary operations
        if isinstance(node, ast.BinOp):

            operation = cls._operators.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported operator"
                )

            left = cls._evaluate(node.left)
            right = cls._evaluate(node.right)

            return operation(left, right)

        # Unary operations
        if isinstance(node, ast.UnaryOp):

            operation = cls._operators.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported unary operator"
                )

            operand = cls._evaluate(node.operand)

            return operation(operand)

        raise ValueError(
            f"Unsupported expression: {type(node).__name__}"
        )