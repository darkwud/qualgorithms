import pytest
import math
from pytest import approx
from psiqworkbench import QPU, Qubits
from grover import grover_iteration

# Test Scenarios: (Weights, Target, Expected Solution Bitstrings, Label)
GROVER_TEST_CASES = [
    ([1, 2, 3], 3, [(0, 0, 1), (1, 1, 0)], "Standard 3-qubit"),
    ([1], 1, [(1,)], "Minimal 1-qubit"),
    ([2, 2, 2], 10, [], "Zero Solutions Case")
]

def get_amplitude_index(bits):
    """Calculates the state vector index for a given bitstring."""
    return sum(b << i for i, b in enumerate(bits))

@pytest.mark.parametrize("weights, target, valid_bits, label", GROVER_TEST_CASES)
def test_grover_amplification(weights, target, valid_bits, label):
    """
    Core Test: Verifies that one Grover iteration correctly 'boosts' 
    the probability of the solution states and cleans up all memory.
    """
    n = len(weights)
    N = 2 ** n
    
    # 1. Calculate Memory Requirements safely
    max_val = max(sum(weights), target)
    sum_bits = max(1, max_val.bit_length())
    
    # Search Reg + Sum Reg + Addend + Ancillas + 5 buffer qubits for arithmetic
    total_qpu_qubits = n + (sum_bits * 2) + 2 + 5 
    
    qpu = QPU(num_qubits=total_qpu_qubits)
    search_reg = Qubits(n, "search_reg", qpu)
    
    # 2. Create a uniform superposition |s>
    qpu.label("Superposition Prep")
    for i in range(n):
        search_reg[i].had()
        
    initial_prob = 1.0 / N
    
    # 3. Apply exactly one Grover iteration
    qpu.label("Grover Iteration")
    grover_iteration(search_reg, weights, target)
    
    # 4. Validation Logic
    state = qpu.pull_state()
    
    if not valid_bits:
        # CASE: NO SOLUTIONS
        # If the Oracle marks nothing, Grover should not amplify anything.
        for i in range(N):
            prob = abs(state[i])**2
            assert prob == approx(initial_prob, abs=1e-5), \
                f"Failed {label}: Prob changed from {initial_prob} to {prob} without solutions."
    else:
        # CASE: SOLUTIONS EXIST
        # Check that solutions are strictly amplified
        for bits in valid_bits:
            index = get_amplitude_index(bits)
            final_prob = abs(state[index])**2
            
            if n == 1:
                assert final_prob == approx(initial_prob, abs=1e-5), "n=1 should preserve prob."
            else:
                assert final_prob > initial_prob + 0.01, \
                    f"Failed {label}: Grover did not amplify solution {bits}. Prob went from {initial_prob} to {final_prob}"
                    
    # 5. Verify Memory Cleanup across the entire G block
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    assert active_qubits == n, \
        f"Memory leak in Grover! Expected {n} active qubits, got {active_qubits}"