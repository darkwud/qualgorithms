import math
import pytest
from itertools import product
from pytest import approx
from psiqworkbench import QPU, Qubits
# Adjust import based on your exact folder structure
from oracle import subset_sum_oracle 

# Define our Test Library (Weights, Target, Expected Solutions)
TEST_CASES = [
    ([1, 2, 3], 3, [(0,0,1), (1,1,0)], "Standard Case"),
    ([1], 1, [(1,)], "Minimal n=1 Case"),
    ([1, 1], 2, [(1,1)], "Duplicate Weights"),
    ([2, 4], 0, [(0,0)], "Target Zero (Empty Set) Case")
]

def get_amplitude_index(bits):
    """
    Helper function to calculate the state vector index.
    Assumes the search register is allocated at the lowest indices of the QPU.
    """
    return sum(b << i for i, b in enumerate(bits))

@pytest.mark.parametrize("weights, target, valid_bits, label", TEST_CASES)
def test_subset_sum_oracle_state(weights, target, valid_bits, label):
    """
    Tests the FTQC Oracle by putting the search register into a uniform 
    superposition, applying the oracle, and pulling the exact state vector 
    to verify phase flips.
    """
    n = len(weights)
    
    # 1. Calculate Peak Memory Requirements
    max_sum = sum(weights)
    sum_bits = max(1, max_sum.bit_length())  # Ensure at least 1 bit even if sum is 0
        
    # We need: Search Reg (n) + Sum Reg (sum_bits) + Addend (sum_bits) + Ancilla (1)
    # We also add a modest 5-qubit safety buffer for internal addition carry-bits.
    total_qpu_qubits = n + (sum_bits * 2) + 1 + 5
    
    # 2. Initialize QPU Environment
    qpu = QPU(num_qubits=total_qpu_qubits)
    search_reg = Qubits(n, "search", qpu)
    
    # 3. State Preparation: Uniform Superposition
    qpu.label("Superposition Prep")
    for i in range(n):
        search_reg[i].had()
        
    # 4. Apply the Oracle
    qpu.label("Subset Sum Oracle")
    subset_sum_oracle(search_reg, weights, target)
    
    # 5. Extract and Verify the State
    # Because our oracle strictly uncomputes the sum_reg and ancilla, 
    # they are guaranteed to be in the |0> state. Therefore, the search_reg 
    # amplitudes will map cleanly to the lowest indices of the state vector.
    state = qpu.pull_state()
    
    expected_magnitude = 1.0 / math.sqrt(2 ** n)
    
    for bits in product([0, 1], repeat=n):
        index = get_amplitude_index(bits)
        amplitude = state[index]
        
        if bits in valid_bits:
            # Solution states MUST have a negative amplitude (phase flip)
            expected_amp = -expected_magnitude
            assert amplitude.real == approx(expected_amp, abs=1e-5), \
                f"Failed {label}: Bitstring {bits} should be flipped to {expected_amp}, got {amplitude.real}"
        else:
            # Non-solution states MUST remain positive
            expected_amp = expected_magnitude
            assert amplitude.real == approx(expected_amp, abs=1e-5), \
                f"Failed {label}: Bitstring {bits} should remain positive at {expected_amp}, got {amplitude.real}"

    # 6. Verify Memory Cleanup (Strict Uncomputation)
    # Check that there are no leftover auxiliary qubits. The only active 
    # allocations at the end should be our search register.
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    assert active_qubits == n, \
        f"Memory leak detected! Oracle did not cleanly uncompute. Expected {n} active qubits, got {active_qubits}"