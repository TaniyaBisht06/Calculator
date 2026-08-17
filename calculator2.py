import sympy as sp
from fractions import Fraction


# ============================================================
# BASIC CALCULATOR
# ============================================================

def basic_calculator(choice, a, b):
    """
    Performs basic arithmetic operations.

    choice:
        1 = Addition
        2 = Subtraction
        3 = Multiplication
        4 = Division
    """

    try:
        choice = int(choice)
        a = int(a)
        b = int(b)
    except (TypeError, ValueError):
        return {
            "success": False,
            "error": "Choice and numbers must be valid integers."
        }

    if choice == 1:
        return {
            "success": True,
            "operation": "Addition",
            "result": a + b
        }

    elif choice == 2:
        return {
            "success": True,
            "operation": "Subtraction",
            "result": a - b
        }

    elif choice == 3:
        return {
            "success": True,
            "operation": "Multiplication",
            "result": a * b
        }

    elif choice == 4:

        if b == 0:
            return {
                "success": False,
                "error": "Division by zero not allowed!"
            }

        fraction = Fraction(a, b)

        return {
            "success": True,
            "operation": "Division",
            "fraction": str(fraction),
            "decimal": round(a / b, 2)
        }

    else:
        return {
            "success": False,
            "error": "Invalid choice! Please select 1-4."
        }


# ============================================================
# MATRIX INPUT
# ============================================================

def input_matrix(matrix_data):
    """
    Converts incoming matrix data into a SymPy Matrix.

    matrix_data should contain rows of numerical values.
    """

    if not isinstance(matrix_data, (list, tuple)):
        raise ValueError("Matrix data must be a list of rows.")

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
    """
    Converts a SymPy Matrix into a JSON-friendly list.

    SymPy values such as Rational(1, 2) are converted
    to strings so that they can be returned safely.
    """

    return [
        [str(value) for value in row]
        for row in matrix.tolist()
    ]


# ============================================================
# MATRIX CALCULATOR
# ============================================================

def matrix_calculator(operation, matrix_data):
    """
    Performs matrix operations.

    operation:
        inverse = Matrix Inverse
        ref     = Row Echelon Form
        rref    = Reduced Row Echelon Form
    """

    if not isinstance(operation, str):
        return {
            "success": False,
            "error": "Operation must be a string."
        }

    operation = operation.lower().strip()

    # Convert incoming matrix data into SymPy Matrix
    try:
        matrix = input_matrix(matrix_data)

    except ValueError as error:
        return {
            "success": False,
            "error": str(error)
        }

    # ========================================================
    # MATRIX INVERSE
    # ========================================================

    if operation == "inverse":

        # Inverse only exists for square matrices
        if matrix.rows != matrix.cols:
            return {
                "success": False,
                "error": "Inverse only exists for square matrices."
            }

        # Check for singular matrix
        if matrix.det() == 0:
            return {
                "success": False,
                "error": "Matrix is singular. Inverse does not exist."
            }

        try:
            cofactor = matrix.cofactor_matrix()
            inverse = matrix.inv()

        except (ValueError, ZeroDivisionError) as error:
            return {
                "success": False,
                "error": str(error)
            }

        return {
            "success": True,
            "operation": "Matrix Inverse",
            "input_matrix": matrix_to_list(matrix),
            "cofactor_matrix": matrix_to_list(cofactor),
            "result_matrix": matrix_to_list(inverse)
        }

    # ========================================================
    # ROW ECHELON FORM
    # ========================================================

    elif operation == "ref":

        try:
            ref_matrix = matrix.echelon_form()

        except (ValueError, TypeError) as error:
            return {
                "success": False,
                "error": str(error)
            }

        return {
            "success": True,
            "operation": "Row Echelon Form (REF)",
            "input_matrix": matrix_to_list(matrix),
            "result_matrix": matrix_to_list(ref_matrix)
        }

    # ========================================================
    # REDUCED ROW ECHELON FORM
    # ========================================================

    elif operation == "rref":

        try:
            rref_matrix, pivot_columns = matrix.rref()

        except (ValueError, TypeError) as error:
            return {
                "success": False,
                "error": str(error)
            }

        return {
            "success": True,
            "operation": "Reduced Row Echelon Form (RREF)",
            "input_matrix": matrix_to_list(matrix),
            "result_matrix": matrix_to_list(rref_matrix),
            "pivot_columns": list(pivot_columns)
        }

    # ========================================================
    # INVALID OPERATION
    # ========================================================

    else:
        return {
            "success": False,
            "error": (
                "Invalid matrix operation. "
                "Use 'inverse', 'ref', or 'rref'."
            )
        }