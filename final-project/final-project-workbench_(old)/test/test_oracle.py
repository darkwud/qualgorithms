import math
import pytest
from itertools import product
from pytest import approx
from psiqworkbench import QPU, Qubits
from src.oracle import subset_sum_oracle 

TEST_CASES = [
    ([1, 2, 3], 3, [(0,0,1), (1,1,0)], "Standard Case"),
    ([1], 1, [(1,)], "Minimal n=1 Case"),
    ([1, 1], 2, [(1,1)], "Duplicate Weights"),
    ([2, 4], 0, [(0,0)], "Target Zero (Empty Set) Case")
]

def get_amplitude_index(bits):
    return sum(b << i for i, b in enumerate(bits))

@pytest.mark.parametrize("weights, target, valid_bits, label", TEST_CASES)
def test_subset_sum_oracle_state(weights, target, valid_bits, label):
    n = len(weights)
    
    # Memory Calculation
    max_sum = sum(weights)
    sum_bits = max(1, max_sum.bit_length()) 

    total_qpu_qubits = n + (sum_bits * 2) + 1 + 5
    
    # Initialize QPU Environment
    qpu = QPU(num_qubits=total_qpu_qubits)
    search_reg = Qubits(n, "search", qpu)
    
    # Uniform Superposition
    qpu.label("Superposition Prep")
    for i in range(n):
        search_reg[i].had()
        
    # Apply the Oracle
    qpu.label("Subset Sum Oracle")
    subset_sum_oracle(search_reg, weights, target)
    
    # Extract and Verify the State
    state = qpu.pull_state()
    
    expected_magnitude = 1.0 / math.sqrt(2 ** n)
    
    for bits in product([0, 1], repeat=n):
        index = get_amplitude_index(bits)
        amplitude = state[index]
        
        if bits in valid_bits:
            expected_amp = -expected_magnitude
            assert amplitude.real == approx(expected_amp, abs=1e-5), \
                f"Failed {label}: Bitstring {bits} should be flipped to {expected_amp}, got {amplitude.real}"
        else:
            expected_amp = expected_magnitude
            assert amplitude.real == approx(expected_amp, abs=1e-5), \
                f"Failed {label}: Bitstring {bits} should remain positive at {expected_amp}, got {amplitude.real}"

    # Memory Leak Check
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    assert active_qubits == n, \
        f"Memory leak detected! Oracle did not cleanly uncompute. Expected {n} active qubits, got {active_qubits}"