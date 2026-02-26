from psiqworkbench import Qubits

# In the first three tasks, you have to prepare the given state using quantum Fourier transform.
# You do not need to implement QFT yourself or to apply it as part of your solution; 
# you need to put the given qubits into such a state that applying QFT to them converts them into the required state.
# Check out the code of the testing harness in test_tasks.py to see how exactly the testing is done.

# Task 1. Prepare periodic state using QFT (1 point).
# Input: a Qubits register of length n ≥ 2 in the |0...0⟩ state.
# Goal: create the state such that applying QFT to it prepares the following state:
#       1/sqrt(N) Σₖ exp(2πik/N) |k⟩, where N = 2ⁿ.
# For example, for n = 2 N = 4, and the goal state is 
#       1/2 (|0⟩ + i|1⟩ - |2⟩ - i|3⟩).
def task_1_periodic_state_prep(reg: Qubits) -> None:
    # Write your code here
    ...


# Task 2. Prepare equal superposition of odd states using QFT (1 point).
# Input: a Qubits register of length n ≥ 2 in the |0...0⟩ state.
# Goal: create the state such that applying QFT to it prepares the following state:
#       1/sqrt(2ⁿ⁻¹) (|1⟩ + |3⟩ + ... + |2ⁿ-1⟩).
# For example, for n = 2 the goal state is 
#       1/sqrt(2) (|1⟩ + |3⟩).
def task_2_odd_superposition_prep(reg: Qubits) -> None:
    # Write your code here
    ...


# Task 3. Prepare superposition of cosines using QFT (3 points).
# Input: a Qubits register of length n ≥ 2 in the |0...0⟩ state.
# Goal: create the state such that applying QFT to it prepares the following state:
#       1/sqrt(2ⁿ⁻¹) Σₖ cos(2πk/N) |k⟩, where N = 2ⁿ.
# For example, for n = 2 N = 4, and the goal state is 
#       1/sqrt(2) (cos(0)|0⟩ + cos(π/2)|1⟩ + cos(π)|2⟩ + cos(3π/2)|3⟩) = 1/sqrt(2) (|0⟩ - |2⟩).
def task_3_cosines_prep(reg: Qubits) -> None:
    # Write your code here
    ...


# Task 4. Eigenstates of the single-qubit gate (1 point).
# Inputs:
#      1) a Qubits register of length 1 in the |0⟩ state.
#      2) a real eigenvalue (+1 or -1).
# Goal: prepare the corresponding eigenstate |ψ₊₁⟩ or |ψ₋₁⟩ of the gate that has the following matrix:
#       / 0.6  0.8 \
#       \ 0.8 -0.6 /
# You can prepare these eigenstates up to a global phase.
def task_4_single_qubit_eigenstate(reg: Qubits, eigenvalue: float) -> None:
    # Write your code here
    ...


# Task 5. Eigenstates of the two-qubit gate (2 points).
# Inputs:
#      1) a Qubits register of length 2 in the |00⟩ state.
#      2) a complex eigenvalue (+1, -1, i, or -i).
# Goal: prepare the corresponding eigenstate of the gate that has the following matrix:
#       / 1  0  0  0 \
#       | 0  0  i  0 |
#       | 0  i  0  0 |
#       \ 0  0  0 -1 /
# You can prepare these eigenstates up to a global phase.
def task_5_two_qubit_eigenstate(reg: Qubits, eigenvalue: complex) -> None:
    # Write your code here
    ...


# Task 6. 3-bit adaptive phase estimation (2 points).
# In this task, we'll consider 3-bit adaptive phase estimation algorithm
# that runs for a unitary/eigenvector pair with eigenphase θ = 0.θ₁θ₂θ₃.
# The eigenphase is guaranteed to have three binary digits of precision.
# Your goal is to implement part of the logic for estimating the _most_ significant digit θ₁
# based on the two least significant digits θ₂ and θ₃ that were already estimated.
#
# Inputs:
#      1) a Qubits register "phase" of length 1 used in the adaptive phase estimation algorithm.
#      2) the two least significant bits of the eigenphase θ₂ and θ₃.
#         Each bit is represented as an integer, 0 or 1.
# Your code will be called _after_ the application of the controlled unitary, 
# but _before_ the final measurement.
#                  ┌───┐       ┌───────────┐  ┌───┐
# phase:      |0>──┤ H ├───┬───┤ Your code ├──┤ M ╞══
#                  └───┘┌──┴──┐└───────────┘  └───┘
# eigenstate: |ψ>───────┤  U  ├──────────────────────
#                       └─────┘
# Goal: Apply the sequence of gates to the phase qubit so that the final measurement 
# always returns the correct _most_ significant bit θ₁.
def task_6_adaptive_phase_estimation(phase: Qubits, theta2: int, theta3: int) -> None:
    # Write your code here
    ...


# Task 7 (extra credit). Reverse-engineer QPE (2 points).
# Input: a real number φ in [0, 1) interval.
# Output: a tuple of two function (U, P) which describe a single-qubit unitary and a eigenstate preparation function
#         that together have an eigenphase φ (within given error).
#         In other words, find a unitary and its eigenstate which have the eigenvalue exp(2iπ φ).
#
# For example, if phase = 0.0, you can return (Z, I): the Z gate and its eigenstate |0⟩ with eigenvalue 1 = exp(2πi · 0.0);
#              if phase = 0.5, you can return (Z, X): the Z gate and its eigenstate |1⟩ with eigenvalue -1 = exp(2πi · 0.5).
#
# To evaluate your return, the unitary and the eigenstate preparation will be passed
# to the quantum phase estimation implementation in the testing harness.
# This implementation will be invoked with exactly 8 bits of precision (phase bits).
# The returned value has to be accurate within the absolute error of 0.01.
# To check this, the test will use the state vector of the system instead of individual measurement outcomes;
# for each value of φ, any basis states that have amplitude with absolute value over 1E-6 must be within 0.01 of the φ.
# (See the testing harness for the complete implementation.)
def task_7_reverse_engineer_qpe(phase: float):
    # This code defines the signatures of two functions that you need to implement
    # and then returns these two functions.

    def unitary(reg: Qubits, cond: Qubits) -> None:
        # Write your code here
        # Remember that your unitary has to have a controlled variant defined!
        # For example, to implement a unitary Z, uncomment the following line:
        # reg.z(cond=cond)
        ...

    def stateprep(reg: Qubits) -> None:
        # Write your code here
        # State preparation unitary doesn't have to have a controlled variant defined.
        # For example, to implement a unitary X that prepares the state |1⟩, uncomment the following line:
        # reg.x()
        ...

    return unitary, stateprep
