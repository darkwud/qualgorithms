# The tasks in this module are inspired by Kakuro puzzles (https://en.wikipedia.org/wiki/Kakuro).
# We will consider solving puzzles that are represented with a rectangular grid of empty squares.
# The goal of the puzzle is to fill each empty square in the grid with digits 0 or 1
# in such a way that the digits in each row add up to the given integers,
# and the digits in each column add up to the given integers.

# For example, consider the following 2×2 puzzle:
#     1   2
# 1 |   |   |
# 2 |   |   |
# 
# The sum of two bits in the bottom row must be 2, so each bit has to be 1.
# Similarly, the sum of two bits in the right column must be 2, so each bit has to be 1.
# The remaining bit in the top left square must be 0.
# The complete solution to this puzzle is unique:
#
#     1   2
# 1 | 0 | 1 |
# 2 | 1 | 1 |

from psiqworkbench import Qubits

# In all tasks
#  - you should not use measurements or the write operation. These will be rejected by the testing harness.
#  - you should not use gates other than X and controlled X (possibly with multiple control qubits). These will be rejected by the testing harness.
#  - you should not use push_state and pull_state. These will be ignored by the testing harness.
#  - you should uncompute and release any auxiliary qubits you allocate. The testing harness will check that.

# Your solutions should focus on the conditions the oracles check rather than on the classical states they mark.
# You should not use multi-qubit gates to mark the basis states that satisfy the oracle conditions directly.
# Instead, consider how you can check the condition described in each task and use smaller gates to perform the evaluation.


# Task 1. Check that the sum of quantum bits is S 
# Inputs:
#      1) A Qubits register of length N ≥ 2 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
#      3) An integer S.
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the sum of bits in the bit string x equals S, and 0 if it doesn't.
#       Leave the input register in the same state it started in.
# For example, for N = 3 and S = 2 the basis states that should be marked are |011⟩, |101⟩, and |110⟩.
def task_1_sum_of_bits(x: Qubits, y: Qubits, s: int) -> None:
    ...





# Task 2. Check that the row constraints of a Kakuro puzzle are satisfied 
# Inputs:
#      1) A Qubits register of length R * C in an arbitrary superposition state (the input register |x⟩).
#         The qubits in the register correspond to the empty squares in the puzzle grid with R rows and C columns.
#         The square in row r and column c has index r * C + c in the Qubits register.
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
#      3) An array of R integers row_constr that specify the row constraints on the Kakuro puzzle.
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the sum of bits in each row r equals the corresponding integer row_constr[r], 
#                and 0 if for at least one row it doesn't.
#       Leave the input register in the same state it started in.
# For the example puzzle from the beginning of the file, R = C = 2, row_constr = [1, 2].
# The basis states that should be marked are |0111⟩ and |1011⟩: 
# the first two bits (row 0) should add up to 1 and the last two bits (row 1) should add up to 2.
def task_2_row_constraints(x: Qubits, y: Qubits, row_constr: list[int]) -> None:
    ...





# Task 3. Check that the column constraints of a Kakuro puzzle are satisfied 
# Inputs:
#      1) A Qubits register of length R * C in an arbitrary superposition state (the input register |x⟩).
#         The qubits in the register correspond to the empty squares in the puzzle grid with R rows and C columns.
#         The square in row r and column c has index r * C + c in the Qubits register.
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
#      3) An array of C integers col_constr that specify the column constraints on the Kakuro puzzle.
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the sum of bits in each column c equals the corresponding integer col_constr[c], 
#                and 0 if for at least one row it doesn't.
#       Leave the input register in the same state it started in.
# For the example puzzle from the beginning of the file, R = C = 2, col_constr = [1, 2].
# The basis states that should be marked are |0111⟩ and |1101⟩: 
# the first and the third bits (column 0) should add up to 1 and the second and fourth bits (column 1) should add up to 2.
def task_3_col_constraints(x: Qubits, y: Qubits, col_constr: list[int]) -> None:
    ...




# Task 4. Check that the Kakuro puzzle is solved correctly 
# Inputs:
#      1) A Qubits register of length R * C in an arbitrary superposition state (the input register |x⟩).
#         The qubits in the register correspond to the empty squares in the puzzle grid with R rows and C columns.
#         The square in row r and column c has index r * C + c in the Qubits register.
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
#      3) An array of R integers row_constr that specify the row constraints on the Kakuro puzzle.
#      4) An array of C integers col_constr that specify the column constraints on the Kakuro puzzle.
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the input x describes a valid solution to the given Kakuro puzzle, and 0 otherwise.
#       Leave the input register in the same state it started in.
# For the example puzzle from the beginning of the file, R = C = 2, row_constr = col_constr = [1, 2].
# The only basis states that should be marked is |0111⟩.
def task_4_kakuro_puzzle(x: Qubits, y: Qubits, row_constr: list[int], col_constr: list[int]) -> None:
    # Write your code here
    ...


# Task 7. Optimize your solution 
# This task does not have a separate operation associated with it!
# The tests for task 7 run on the oracle you've implemented in task 4.
# For this task to be graded, the oracle has to be correct (that is, to pass the test for task 4).
#
# Task 7 is scored based on the resource estimates for this oracle acting on the 8×8 Kakuro puzzle
# with row_constr = col_constr = [1, 2, 1, 2, 1, 2, 1, 2]
# The scoring is based on the active volume of one oracle call.
# Your goal is to reduce the active volume to _under 150k_:
#  - if AV < 150k, you get 2 points.
#  - if 150k ≤ AV < 220k, you get 1 point.
#  - if 220k ≤ AV, you get 0 points.
