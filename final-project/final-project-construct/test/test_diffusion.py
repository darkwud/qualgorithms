import pytest
from pytest import approx
from psiqworkbench import QPU, Qubits
from diffusion import diffusion_operator

# We test the same edge cases:
# n=1 (special logic), n=2 (minimal multi-control), n=3 (odd), n=5 (scale up)
@pytest.mark.parametrize("n", [1, 2, 3, 5])
def test_diffusion_invariance(n):
    """
    Tests that the Diffusion operator preserves the uniform superposition state 
    and perfectly cleans up its temporary ancilla memory.
    """
    # 1. Initialize QPU (Needs 'n' qubits + 1 for the diffusion ancilla)
    qpu = QPU(num_qubits=n + 1)
    reg = Qubits(n, "search_reg", qpu)
    
    # 2. Prepare the uniform superposition |s>
    for i in range(n):
        reg[i].had()
        
    initial_state = qpu.pull_state()
    
    # 3. Apply the Diffusion Operator
    diffusion_operator(reg)
    
    # 4. Verify Invariance
    # Diffusion on the uniform superposition should result in the exact same state 
    # (though sometimes with a global -1 phase depending on the exact math). 
    # We check absolute values to safely ignore global phase.
    final_state = qpu.pull_state()
    for i in range(len(initial_state)):
        assert abs(final_state[i]) == approx(abs(initial_state[i]), abs=1e-5), \
            f"State drifted at index {i} for n={n}"
            
    # 5. Verify Memory Cleanup
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    assert active_qubits == n, \
        f"Memory leak in Diffusion! Expected {n} active qubits, got {active_qubits}"