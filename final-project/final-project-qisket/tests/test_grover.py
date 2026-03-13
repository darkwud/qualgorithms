from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from Final_Project.oracle import subset_sum_oracle
from Final_Project.grover import grover_iteration
import numpy as np
import pytest


# Test Scenarios: (Weights, Target, Expected Solution Bitstrings)
# (weights, target, expected_M, label)
GROVER_TEST_CASES = [
    ([1, 2, 3], 3, [(0, 0, 1), (1, 1, 0)], "Standard 3-qubit"),
    ([1], 1, [(1,)], "Minimal 1-qubit"),
    ([2, 2, 2], 10, [], "Zero Solutions Case")
]

def get_bit_probability(bits, statevector):
    """
    Helper function to extract the probability of a specific bitstring.
    Qiskit uses Little-Endian: (1,0,0) is index 1 (2^0).
    """
    index = sum(b << i for i, b in enumerate(bits))
    # Probability = |Amplitude|^2
    return np.abs(statevector[index])**2

# Runs the test function 3 separate times, once for each case above.
@pytest.mark.parametrize("weights, target, valid_bits, label", GROVER_TEST_CASES)

def test_grover_amplification(weights, target, valid_bits, label):
    """
    Core Test: Verifies that one Grover iteration correctly 'boosts' 
    the probability of the solution states.
    """
    n = len(weights)
    N = 2**n

    # Build the Oracle and the Grover Iteration (G = D * O)
    oracle = subset_sum_oracle(weights, target)
    grover = grover_iteration(oracle)

    # Create a uniform superposition |s>
    # In this state, every item has an equal probability of 1/N.
    qc = QuantumCircuit(n)
    qc.h(range(n))
    initial_prob = 1.0 / N
    
    # Apply exactly one Grover iteration
    # This should rotate the state vector toward the 'marked' solutions.
    qc.compose(grover, inplace=True)
    state = Statevector.from_instruction(qc).data

    # Validation Logic
    if not valid_bits:
        # CASE: NO SOLUTIONS
        # If the Oracle marks nothing, Grover should not amplify anything.
        # All probabilities should remain roughly 1/N.
        for i in range(N):
            prob = np.abs(state[i])**2
            assert np.isclose(prob, initial_prob, atol=1e-5), \
                f"Failed {label}: Prob changed from {initial_prob} to {prob} without solutions."
    else:
        # Check that solutions are amplified
        for bits in valid_bits:
            final_prob = get_bit_probability(bits, state)
            
            # Special case for n=1: Prob starts at 0.5 and stays at 0.5 (swapped)
            if n == 1:
                assert np.isclose(final_prob, initial_prob, atol=1e-5), "n=1 should preserve prob."
            else:
                # For n > 1, Grover MUST strictly increase the probability
                assert final_prob > initial_prob, \
                    f"Failed {label}: {bits} not amplified ({final_prob} <= {initial_prob})"