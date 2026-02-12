from psiqworkbench import Qubits

# In all tasks
#  - you should not use measurements or the write operation. These will be rejected by the testing harness.
#  - you should not use gates other than X and controlled X. These will be rejected by the testing harness.
#  - you should not use push_state and pull_state. These will be ignored by the testing harness.
#  - you should uncompute and release any auxiliary qubits you allocate, if the task allows you that. The testing harness will check that.

# For tasks 4-6, your solutions should focus on the conditions the oracles check rather than on the classical states they mark.
# For example, in task 4, for N = 4 you should not use four five-qubit gates to mark the states |0011⟩, |0110⟩, |1001⟩, and |1100⟩ directly.
# Instead, consider how you can check the condition described in the task and use one-, two-, and three-qubit gates to flip the state conditionally.


# Task 1. NAND gate (1 point).
# Inputs:
#      1) A Qubits register of length 2 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x₀, x₁) = NAND(x₀, x₁) = NOT (x₀ AND x₁).
#       Leave the input register in the same state it started in.
def task_1_nand_gate(x: Qubits, y: Qubits) -> None:
    # Write your code here
    ...


# Task 2. Peres gate (1 point).
# Input: A Qubits register of length 3 in an arbitrary superposition state (the input register |x⟩).
# Goal: Implement a three-qubit gate defined by its effect on the basis states
#       (the qubits are given in order |x[0], x[1], x[2]⟩):
#        |0 0 0⟩ → |0 0 0⟩
#        |0 0 1⟩ → |0 0 1⟩
#        |0 1 0⟩ → |0 1 0⟩
#        |0 1 1⟩ → |0 1 1⟩
#        |1 0 0⟩ → |1 1 0⟩
#        |1 0 1⟩ → |1 1 1⟩
#        |1 1 0⟩ → |1 0 1⟩
#        |1 1 1⟩ → |1 0 0⟩
def task_2_peres_gate(x: Qubits) -> None:
    # Write your code here
    ...


# Task 3. |011011...⟩ marking oracle (1 point).
# Inputs:
#      1) A Qubits register of length 2 ≤ N ≤ 6 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the bit pattern of x is 011011... (extend or shorten the pattern to appropriate length)
#                  and 0 otherwise.
#       Leave the input register in the same state it started in.
# For example, for N = 4 the basis state that should be marked is |0110⟩.
def task_3_fixed_pattern(x: Qubits, y: Qubits) -> None:
    # Write your code here
    ...


# Task 4. Check that the first half of the bit string equals the second half flipped (2 points).
# Inputs:
#      1) A Qubits register of length N = 2K in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the first K bits of the string x are equal the last K bits, flipped, and 0 otherwise.
#       That is, bit x[j] should equal the negation of bit x[j + K] for all j from 0 to K-1, inclusive.
#       Leave the input register in the same state it started in.
# For example, for N = 4 the basis states that should be marked are |0011⟩, |0110⟩, |1001⟩, and |1100⟩.
def task_4_flipped_halves(x: Qubits, y: Qubits) -> None:
    # Write your code here
    ...


# Task 5. Check that the bit string doesn't have three identical bits in a row (2 points).
# Inputs:
#      1) A Qubits register of length N ≥ 3 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the bit string x doesn't have three identical bits in a row, and 0 if it does.
#       Leave the input register in the same state it started in.
# For example, for N = 4 the basis states that should NOT be marked are |0000⟩, |0001⟩, |0111⟩, |1000⟩, |1110⟩, and |1111⟩.
#       All other basis states should be marked.
# For this task, you can allocate n-2 auxiliary qubits.
def task_5_no_three_bits(x: Qubits, y: Qubits) -> None:
    # Write your code here
    ...


# Task 6. Regexp matching marking oracle (3 points).
# Inputs:
#      1) A Qubits register of length N ≥ 1 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
#      3) A bit pattern of length N represented as a list of integers.
#         k-th element of the pattern encodes the allowed states of the qubit x[k]:
#         values 0 and 1 represent states |0⟩ and |1⟩, respectively, value -1 represents "any state".
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the bit string x matches the given pattern, and 0 if it does not.
#       Leave the input register in the same state it started in.
# For example, for N = 3 the bit pattern [0, -1, 1] matches two basis states that should be marked: |001⟩ and |011⟩;
# the bit pattern [1, -1, -1] matches four basis states: |100⟩, |101⟩, |110⟩, and |111⟩.
def task_6_regexp_match(x: Qubits, y: Qubits, pattern: list[int]) -> None:
    # Write your code here
    ...
