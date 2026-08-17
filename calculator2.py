
import sympy as sp
from fractions import Fraction


# ---------------- BASIC CALCULATOR ---------------- #

def basic_calculator(choice, a, b):
    """
    Performs basic arithmetic operations.

    choice:
        1 = Addition
        2 = Subtraction
        3 = Multiplication
        4 = Division
    """

    # Convert incoming values to integers
    choice = int(choice)
    a = int(a)
    b = int(b)

    # Addition
    if choice == 1:
        return {
            "success": True,
            "operation": "Addition",
            "result": a + b
        }

    # Subtraction
    elif choice == 2:
        return {
            "success": True,
            "operation": "Subtraction",
            "result": a - b
        }

    # Multiplication
    elif choice == 3:
        return {
            "success": True,
            "operation": "Multiplication",
            "result": a * b
        }

    # Division
    elif choice == 4:

        # Division by zero
        if b == 0:
            return {
                "success": False,
                "error": "Division by zero not allowed!"
            }

        else:
            frac = Fraction(a, b)

            return {
                "success": True,
                "operation": "Division",
                "fraction": str(frac),
                "decimal": round(a / b, 2)
            }

    # Invalid operation
    else:
        return {
            "success": False,
            "error": "Invalid choice! Please select 1-4."
        }


# ---------------- MATRIX INPUT ---------------- #

def input_matrix(matrix_data, augmented=False):
    """
    Converts the matrix received from the frontend
    into a SymPy Matrix.
    """

    try:
        matrix = []

        for row in matrix_data:
            matrix.append([int(value) for value in row])

        M = sp.Matrix(matrix)

        return M

    except (ValueError, TypeError):
        raise ValueError("Invalid matrix values.")


# ---------------- MATRIX HELPER ---------------- #

def matrix_to_list(matrix):
    """
    Converts a SymPy Matrix into a JSON-friendly list.

    SymPy values such as Rational(1, 2) cannot be directly
    returned through JSON, so they are converted to strings.
    """

    return [
        [str(value) for value in row]
        for row in matrix.tolist()
    ]


# ---------------- MATRIX CALCULATOR ---------------- #

def matrix_calculator(operation, matrix_data):
    """
    Performs matrix operations.

    operation:
        inverse = Matrix Inverse
        ref     = Row Echelon Form
        rref    = Reduced Row Echelon Form
    """

    operation = str(operation).lower()

    # Convert frontend matrix data to SymPy Matrix
    try:
        M = input_matrix(matrix_data)

    except ValueError as error:
        return {
            "success": False,
            "error": str(error)
        }

    # Make sure matrix is not empty
    if M.rows == 0 or M.cols == 0:
        return {
            "success": False,
            "error": "Matrix cannot be empty."
        }

    # ==================================================
    # MATRIX INVERSE
    # ==================================================

    if operation == "inverse":

        # Inverse only exists for square matrices
        if M.rows != M.cols:
            return {
                "success": False,
                "error": "Inverse only exists for square matrices."
            }

        # Check whether matrix is singular
        if M.det() == 0:
            return {
                "success": False,
                "error": "Matrix is singular. Inverse does not exist."
            }

        # Cofactor Matrix
        cofactor = M.cofactor_matrix()

        # Inverse Matrix
        inverse = M.inv()

        return {
            "success": True,
            "operation": "Matrix Inverse",
            "input_matrix": matrix_to_list(M),
            "cofactor_matrix": matrix_to_list(cofactor),
            "result_matrix": matrix_to_list(inverse)
        }

    # ==================================================
    # ROW ECHELON FORM (REF)
    # ==================================================

    elif operation == "ref":

        ref_matrix = M.echelon_form()

        return {
            "success": True,
            "operation": "Row Echelon Form (REF)",
            "input_matrix": matrix_to_list(M),
            "result_matrix": matrix_to_list(ref_matrix)
        }

    # ==================================================
    # REDUCED ROW ECHELON FORM (RREF)
    # ==================================================

    elif operation == "rref":

        rref_matrix, pivot_columns = M.rref()

        return {
            "success": True,
            "operation": "Reduced Row Echelon Form (RREF)",
            "input_matrix": matrix_to_list(M),
            "result_matrix": matrix_to_list(rref_matrix),
            "pivot_columns": list(pivot_columns)
        }

    # ==================================================
    # INVALID OPERATION
    # ==================================================

    else:
        return {
            "success": False,
            "error": "Invalid matrix operation."
        }