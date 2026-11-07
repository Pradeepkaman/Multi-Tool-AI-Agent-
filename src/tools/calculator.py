"""Math calculator tool for evaluating arithmetic and mathematical expressions safely."""

import math
from typing import Any, Dict
from langchain_core.tools import tool


# Safe math functions and constants allowed in expressions
SAFE_MATH_ENV: Dict[str, Any] = {
    # Constants
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
    # Functions
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "pow": pow,
    "sum": sum,
    "sqrt": math.sqrt,
    "cbrt": getattr(math, "cbrt", lambda x: x ** (1 / 3)),
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "factorial": math.factorial,
    "gcd": math.gcd,
}


def safe_calculate(expression: str) -> str:
    """Safely evaluates a mathematical expression string.

    Args:
        expression: A string representing a math expression (e.g., '25 * 4 + 10', 'sqrt(144)', '(120 - 90) / 90 * 100').

    Returns:
        A string representing the evaluated numerical result or an error message.
    """
    cleaned = expression.strip()
    if not cleaned:
        return "Error: Empty expression provided."

    # Replace common formatting characters
    cleaned = cleaned.replace("^", "**").replace("×", "*").replace("÷", "/")

    # Check for disallowed built-in access or unsafe patterns
    disallowed_terms = [
        "__", "import", "eval", "exec", "open", "os", "sys", "subprocess",
        "lambda", "globals", "locals", "compile", "classmethod", "input"
    ]
    for term in disallowed_terms:
        if term in cleaned:
            return f"Error: Expression contains prohibited keyword '{term}'."

    try:
        # Evaluate with empty globals and restricted safe math locals
        result = eval(cleaned, {"__builtins__": {}}, SAFE_MATH_ENV)

        if isinstance(result, float):
            # Format floating point numbers cleanly
            if result.is_integer():
                return str(int(result))
            return f"{result:.6g}"
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as exc:
        return f"Error evaluating expression '{expression}': {str(exc)}"


@tool("calculator")
def calculator_tool(expression: str) -> str:
    """Useful for performing mathematical calculations and evaluating numerical formulas.
    Input should be a mathematical expression string like '500 * (1 + 0.08) ** 5' or '(450 - 300) / 300 * 100'.
    """
    return safe_calculate(expression)
