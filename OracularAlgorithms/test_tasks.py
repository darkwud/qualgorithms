from functools import partial
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
from pytest import approx
from .tasks_Module4_OracularAlgorithms import *

# Create the simulator instance to add save_statevector method to QuantumCircuit
simulator = AerSimulator(method='statevector')

def print_matrix(matrix):
    for row in matrix:
        print(row)


def check_operation_matrix(
    n,              # Number of qubits
    solution,       # Callable that is being tested
    expected_matrix # Matrix it should have
) -> None:
    # Construct the circuit that has the callable as a part of it
    q = QuantumRegister(n)
    circ = QuantumCircuit(q)
    solution(circ, q)
    # Convert the circuit to a matrix
    op = Operator(circ)
    actual_matrix = op.data

    # Check that the actual matrix matches the expected one
    for actual, expected in zip(actual_matrix, expected_matrix):
        if actual != approx(expected):
            print("Expected matrix:")
            print_matrix(expected_matrix)
            print("Actual matrix:")
            print_matrix(actual_matrix)
            raise ValueError("Operation matrices should be equal")


def test_1_singlequbit_oracles():
    expected_matrices = [[[1, 0], [0, 1]],
                         [[-1, 0], [0, -1]],
                         [[1, 0], [0, -1]],
                         [[-1, 0], [0, 1]]]
    for F in range(4):
        fun = partial(task_1_singlequbit_oracles, F=F)
        check_operation_matrix(1, fun, expected_matrices[F])


def test_2_inequality_oracle():
    expected_matrix = [[0] * 4 for _ in range(4)]
    for ind in range(4):
        expected_matrix[ind][ind] = -1 if ind % 2 != ind // 2 else 1
    check_operation_matrix(2, task_2_inequality_oracle, expected_matrix)


def int_as_bits(num: int, n_bits: int) -> list[int]:
    return [1 if num & (1 << i) > 0 else 0 for i in range(n_bits)]


def test_3_bv_oracle():
    for n in range(2, 5):
        expected_matrix = [[0] * 2 ** n for _ in range(2 ** n)]
        for s_int in range(2 ** n):
            # Use little-endian for s_bits and later for ind
            s_bits = int_as_bits(s_int, n)
            for ind in range(2 ** n):
                # Do bitwise AND of bits in ind and s and then count bits set to 1
                expected_matrix[ind][ind] = 1 if (s_int & ind).bit_count() % 2 == 0 else -1
            fun = partial(task_3_bv_oracle, s=s_bits)
            check_operation_matrix(n, fun, expected_matrix)


def test_4_divisible_by_4_oracle():
    for n in range(3, 6):
        expected_matrix = [[0] * 2 ** n for _ in range(2 ** n)]
        for ind in range(2 ** n):
            expected_matrix[ind][ind] = -1 if ind % 4 == 0 else 1
        check_operation_matrix(n, task_4_divisible_by_4_oracle, expected_matrix)


def test_5_has_prefix():
    for n in range(3, 6):
        expected_matrix = [[0] * 2 ** n for _ in range(2 ** n)]
        for k in range(2, n):
            for s_int in range(2 ** k):
                s_bits = int_as_bits(s_int, k)
                print(f"Testing {n=} s={s_bits}")
                # Construct the matrix
                for ind in range(2 ** n):
                    # Take k least-significant ones
                    ind_substr = ind % (2 ** k)
                    expected_matrix[ind][ind] = -1 if ind_substr == s_int else 1
                fun = partial(task_5_has_prefix, s=s_bits)
                check_operation_matrix(n, fun, expected_matrix)


def test_6_palindrome():
    for n in range(2, 7):
        expected_matrix = [[0] * 2 ** n for _ in range(2 ** n)]
        for ind in range(2 ** n):
            ind_bits = int_as_bits(ind, n)
            expected_matrix[ind][ind] = -1 if ind_bits == ind_bits[::-1] else 1
        check_operation_matrix(n, task_6_palindrome, expected_matrix)

