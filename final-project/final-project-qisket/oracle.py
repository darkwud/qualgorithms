from qiskit import QuantumCircuit
from itertools import product

def subset_sum_oracle(weights, target):
    """
    Builds a phase oracle for the subset sum problem.

    Marks (applies a -1 phase) to all bitstrings whose selected
    weights sum to the target value.

    Args:
        weights (list[int]): The set of numbers (e.g., [1,2,3])
        target (int): Target subset sum

    Returns:
        QuantumCircuit: Oracle circuit that flips phase of valid states
    """

     # Number of qubits = number of elements in the set
    n = len(weights)
    # Create quantum circuit with n qubits
    qc = QuantumCircuit(n, name="SubsetSumOracle")

    # Find all bitstrings that satisfy subset sum
    valid_states = []

    # Generate all possible bitstrings of length n
    for bits in product([0, 1], repeat=n):
        # Compute subset sum for this bitstring
        subset_sum = sum(w for b, w in zip(bits, weights) if b)

        # If it matches the target, mark as valid
        if subset_sum == target:
            valid_states.append(bits)

    # Mark each valid state with a phase flip
    for state in valid_states:
        for i, bit in enumerate(state):
            if bit == 0:
                qc.x(i)

        # --- PHASE FLIP LOGIC ---
        if n == 1:
            # If there's only 1 qubit, we can't use MCX (which needs >= 2).
            # A Z gate flips the phase of the |1> state.
            qc.z(0)
        else:
            # Standard logic for n > 1, Apply multi-controlled Z gate
            qc.h(n-1)
            qc.mcx(list(range(n-1)), n-1)
            qc.h(n-1)
        # ------------------------

        # Undo the X gates to restore original basis
        for i, bit in enumerate(state):
            if bit == 0:
                qc.x(i)

    return qc