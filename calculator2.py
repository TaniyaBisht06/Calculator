import sympy as sp
from fractions import Fraction

# ---------------- BASIC CALCULATOR ---------------- #

def basic_calculator():
    print("\n--- Basic Calculator ---")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = int(input("Enter choice (1-4): "))
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))

    if choice == 1:
        print("Result =", a + b)

    elif choice == 2:
        print("Result =", a - b)

    elif choice == 3:
        print("Result =", a * b)

    elif choice == 4:
        if b == 0:
            print("Division by zero not allowed!")
        else:
            frac = Fraction(a, b)
            print("Fraction form =", frac)
            print("Decimal form =", round(a / b, 2))

# ---------------- MATRIX INPUT ---------------- #

def input_matrix(augmented=False):
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))

    if augmented:
        print("⚠ If augmented, include constant column as last column.")

    print("Enter matrix elements row-wise (space separated):")

    matrix = []
    for i in range(rows):
        row = list(map(int, input().split()))
        matrix.append(row)

    return sp.Matrix(matrix)

# ---------------- MATRIX CALCULATOR ---------------- #

def matrix_calculator():
    print("\n--- Matrix Calculator ---")
    print("1. Matrix Inverse")
    print("2. REF")
    print("3. RREF")

    choice = int(input("Enter your choice: "))

    # -------- INVERSE -------- #
    if choice == 1:
        M = input_matrix()

        print("\nInput Matrix:")
        sp.pprint(M)

        if M.rows != M.cols:
            print("Inverse only exists for square matrices.")
            return

        if M.det() == 0:
            print("Matrix is singular. Inverse does not exist.")
            return

        print("\nCofactor Matrix:")
        sp.pprint(M.cofactor_matrix())

        print("\nInverse Matrix:")
        sp.pprint(M.inv())

    # -------- REF or RREF -------- #
    elif choice == 2 or choice == 3:

        print("\n1. Normal Matrix")
        print("2. Augmented Matrix")

        matrix_type = int(input("Enter your choice: "))

        if matrix_type == 1:
            M = input_matrix(augmented=False)

        elif matrix_type == 2:
            M = input_matrix(augmented=True)

        else:
            print("Invalid choice!")
            return

        print("\nInput Matrix:")
        sp.pprint(M)

        if choice == 2:
            print("\nRow Echelon Form (REF):")
            sp.pprint(M.echelon_form())

        elif choice == 3:
            print("\nReduced Row Echelon Form (RREF):")
            rref_matrix, _ = M.rref()
            sp.pprint(rref_matrix)

    else:
        print("Invalid choice!")

# ---------------- MAIN MENU ---------------- #

def main():
    while True:
        print("\n====== ADVANCED CALCULATOR ======")
        print("1. Basic Calculator")
        print("2. Matrix Calculator")
        print("3. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            basic_calculator()

        elif choice == 2:
            matrix_calculator()

        elif choice == 3:
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

main()