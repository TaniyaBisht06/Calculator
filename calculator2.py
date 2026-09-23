from fractions import Fraction

import sympy as sp
from flask import Flask, jsonify, request


app = Flask(__name__)


def error_response(message):
    """Create a consistent error response."""
    return {
        "success": False,
        "error": message
    }


# ============================================================
# BASIC CALCULATOR
# ============================================================

def basic_calculator(choice, a, b):
    """Perform a basic arithmetic operation."""

    try:
        choice = int(choice)
        a = int(a)
        b = int(b)
    except (TypeError, ValueError):
        return error_response(
            "Choice and numbers must be valid integers."
        )

    operations = {
        1: ("Addition", lambda: a + b),
        2: ("Subtraction", lambda: a - b),
        3: ("Multiplication", lambda: a * b),
    }

    if choice in operations:
        operation_name, calculation = operations[choice]

        return {
            "success": True,
            "operation": operation_name,
            "result": calculation()
        }

    if choice == 4:
        if b == 0:
            return error_response(
                "Division by zero not allowed!"
            )

        fraction = Fraction(a, b)

        return {
            "success": True,
            "operation": "Division",
            "fraction": str(fraction),
            "decimal": round(a / b, 2)
        }

    return error_response(
        "Invalid choice! Please select 1-4."
    )


# ============================================================
# MATRIX INPUT
# ============================================================

def input_matrix(matrix_data):
    """Convert incoming matrix data into a SymPy Matrix."""

    if not isinstance(matrix_data, (list, tuple)):
        raise ValueError(
            "Matrix data must be a list of rows."
        )

    if not matrix_data:
        raise ValueError("Matrix cannot be empty.")

    try:
        matrix = sp.Matrix(matrix_data)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid matrix data.") from error

    if matrix.rows == 0 or matrix.cols == 0:
        raise ValueError("Matrix cannot be empty.")

    return matrix


# ============================================================
# MATRIX CONVERSION
# ============================================================

def matrix_to_list(matrix):
    """Convert a SymPy Matrix into a JSON-friendly list."""

    return [
        [str(value) for value in row]
        for row in matrix.tolist()
    ]


# ============================================================
# MATRIX OPERATIONS
# ============================================================

def calculate_inverse(matrix):
    """Calculate the inverse and cofactor matrix."""

    if matrix.rows != matrix.cols:
        return error_response(
            "Inverse only exists for square matrices."
        )

    if matrix.det() == 0:
        return error_response(
            "Matrix is singular. Inverse does not exist."
        )

    cofactor = matrix.cofactor_matrix()
    inverse = matrix.inv()

    return {
        "success": True,
        "operation": "Matrix Inverse",
        "input_matrix": matrix_to_list(matrix),
        "cofactor_matrix": matrix_to_list(cofactor),
        "result_matrix": matrix_to_list(inverse)
    }


def calculate_ref(matrix):
    """Calculate row echelon form."""

    ref_matrix = matrix.echelon_form()

    return {
        "success": True,
        "operation": "Row Echelon Form (REF)",
        "input_matrix": matrix_to_list(matrix),
        "result_matrix": matrix_to_list(ref_matrix)
    }


def calculate_rref(matrix):
    """Calculate reduced row echelon form."""

    rref_matrix, pivot_columns = matrix.rref()

    return {
        "success": True,
        "operation": "Reduced Row Echelon Form (RREF)",
        "input_matrix": matrix_to_list(matrix),
        "result_matrix": matrix_to_list(rref_matrix),
        "pivot_columns": list(pivot_columns)
    }


MATRIX_OPERATIONS = {
    "inverse": calculate_inverse,
    "ref": calculate_ref,
    "rref": calculate_rref
}


# ============================================================
# MATRIX CALCULATOR
# ============================================================

def matrix_calculator(operation, matrix_data):
    """Validate input and perform a matrix operation."""

    if not isinstance(operation, str):
        return error_response(
            "Operation must be a string."
        )

    operation = operation.lower().strip()
    operation_handler = MATRIX_OPERATIONS.get(operation)

    if operation_handler is None:
        return error_response(
            "Invalid matrix operation. "
            "Use 'inverse', 'ref', or 'rref'."
        )

    try:
        matrix = input_matrix(matrix_data)
        return operation_handler(matrix)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        return error_response(str(error))


# ============================================================
# FLASK WEB APPLICATION
# ============================================================

@app.route("/")
def home():
    return """
    <h1>Calculator API</h1>
    <p>Calculator application is running.</p>

    <h2>Available Endpoints</h2>

    <ul>
        <li>
            <a href="/calculate?choice=1&a=10&b=5">
                Basic Calculator
            </a>
        </li>

        <li>
            <a href="/search?q=test">
                Search
            </a>
        </li>
    </ul>
    """


@app.route("/calculate", methods=["GET"])
def calculate():
    choice = request.args.get("choice")
    a = request.args.get("a")
    b = request.args.get("b")

    result = basic_calculator(choice, a, b)

    return jsonify(result)


@app.route("/matrix", methods=["POST"])
def matrix():
    data = request.get_json()

    if not data:
        return jsonify(
            error_response("JSON data is required.")
        ), 400

    operation = data.get("operation")
    matrix_data = data.get("matrix")

    result = matrix_calculator(
        operation,
        matrix_data
    )

    return jsonify(result)


# ============================================================
# DELIBERATELY VULNERABLE ENDPOINT FOR DAST LAB
# ============================================================

@app.route("/search")
def search():
    query = request.args.get("q", "")

    # INTENTIONALLY VULNERABLE:
    # User input is reflected directly into HTML.
    # This endpoint is used only for the OWASP ZAP lab.
    return f"<h2>Search Result: {query}</h2>"


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",  # nosec B104
        port=5000
    )
