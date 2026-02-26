from psiqworkbench import Qubits

# In all tasks
#  - you should not use measurements or the write operation.
#  - you should not use gates other than X and controlled X.
#  - you should not use push_state and pull_state. 
#  - you should uncompute and release any auxiliary qubits you allocate, if the task allows you that. The testing harness will check that.

# For tasks 4-6, your solutions should focus on the conditions the oracles check rather than on the classical states they mark.
# For example, in task 4, for N = 4 you should not use four five-qubit gates to mark the states |0011⟩, |0110⟩, |1001⟩, and |1100⟩ directly.
# Instead, consider how you can check the condition described in the task and use one-, two-, and three-qubit gates to flip the state conditionally.


######################################################
# Task 1. NAND gate 
# Inputs:
#      1) A Qubits register of length 2 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x₀, x₁) = NAND(x₀, x₁) = NOT (x₀ AND x₁).
#       Leave the input register in the same state it started in.
def task_1_nand_gate(x: Qubits, y: Qubits) -> None:

    # Flip y unconditionally
    # y becomes |y ⊕ 1⟩
    y.x()

    # Flip y if both x qubits are |1⟩
    y.x(x)


######################################################
# Task 2. Peres gate 
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

    # Flip x[2] if both x[0] and x[1] = 1 (Tofolli)
    x[2].x(x[0:2])

    # Flip x[1] if x[0] = 1 (CNOT)
    x[1].x(x[0])


######################################################
# Task 3. |011011...⟩ marking oracle 
# Inputs:
#      1) A Qubits register of length 2 ≤ N ≤ 6 in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the bit pattern of x is 011011... (extend or shorten the pattern to appropriate length)
#                  and 0 otherwise.
#       Leave the input register in the same state it started in.
# For example, for N = 4 the basis state that should be marked is |0110⟩.
def task_3_fixed_pattern(x: Qubits, y: Qubits) -> None:
    n = len(x)

    # Apply X gate to every qubit expecting a 0
    for i in range(n):
        if i % 3 == 0:
            x[i].x() 

    # Flip y based on x register
    # Applied when input matches pattern (011011...), x qubits transform to |1⟩ 
    y.x(x)

    # Uncompute to return x register it original state
    # Apply X gate to reverse to normalization 
    for i in range(n):
        if i % 3 == 0:
            x[i].x()  


 ######################################################           
# Task 4. Check that the first half of the bit string equals the second half flipped 
# Inputs:
#      1) A Qubits register of length N = 2K in an arbitrary superposition state (the input register |x⟩).
#      2) A Qubits register of length 1 in an arbitrary superposition state (the output register |y⟩).
# Goal: Transform the state |x⟩|y⟩ into the state |x⟩|y ⊕ f(x)⟩ (⊕ is addition modulo 2),
#       where f(x) = 1 if the first K bits of the string x are equal the last K bits, flipped, and 0 otherwise.
#       That is, bit x[j] should equal the negation of bit x[j + K] for all j from 0 to K-1, inclusive.
#       Leave the input register in the same state it started in.
# For example, for N = 4 the basis states that should be marked are |0011⟩, |0110⟩, |1001⟩, and |1100⟩.

def task_4_flipped_halves(x: Qubits, y: Qubits) -> None:

    n = len(x)
    k = n // 2

    # Compare x[j] with x[j + k]
    # Apply CNOT flip if control = '1'
    # x[j + k] = '1' iff two bits are different
    for j in range(k):
        x[j + k].x(x[j])

    # Successful flip should have second half of wires sitting at '1'
    # Flip qubit y
    y.x(x[k:n])

    # Uncompute by running comparison to flip bits back to original state
    for j in range(k):
        x[j + k].x(x[j])


######################################################
# Task 5. Check that the bit string doesn't have three identical bits in a row 
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
    n = len(x)
    # Allocate n - 2 for temporary status checks
    aux = Qubits(n - 2, "aux", x.qpu)

    # Assume bit is 1 for starters
    for i in range(n - 2):
        # Flip bit = 1
        aux[i].x()

        # Check for '111'
        # If 1s, flip to 0s
        aux[i].x(x[i:i+3])

        # Check for '000' 
        # Flip 0s to 1s and check
        # Flip them back once check is complete
        x[i:i+3].x()
        aux[i].x(x[i:i+3]) # If it was '0s', light flips 'OFF'.
        x[i:i+3].x()

    # If all status bits stayed 'ON', no triplets were found
    y.x(aux)

    # Repeat logic in order to revers logic to 0s
    for i in range(n - 2):
        x[i:i+3].x()
        aux[i].x(x[i:i+3])
        x[i:i+3].x()
        aux[i].x(x[i:i+3])
        aux[i].x() # aux wire returned to 0

    aux.release()


######################################################
# Task 6. Regexp matching marking oracle 
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

    # Filter -1 for cleaner pattern recognition
    constrained_pos = [i for i in range(len(x)) if pattern[i] != -1]

    # If outputs = -1, job complete
    if not constrained_pos:
        y.x()
        return

    # Flip gate = 1 if pattern expects 0
    for i in constrained_pos:
        if pattern[i] == 0:
            x[i].x()

    # Check important wires and flip y if pattern matches expectation
    y.x(x[constrained_pos])

    # Uncompute 0 bits
    for i in constrained_pos:
        if pattern[i] == 0:
            x[i].x()