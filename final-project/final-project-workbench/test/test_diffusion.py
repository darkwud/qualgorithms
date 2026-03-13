import pytest
from pytest import approx
from psiqworkbench import QPU, Qubits
from src.diffusion import diffusion_operator

@pytest.mark.parametrize("n", [1, 2, 3, 5])
def test_diffusion_invariance(n):
    # Initialize QPU
    qpu = QPU(num_qubits=n + 1)
    reg = Qubits(n, "search_reg", qpu)
    
    # Prepare the uniform superposition 
    for i in range(n):
        reg[i].had()
        
    initial_state = qpu.pull_state()
    
    # Apply the Diffusion Operator
    diffusion_operator(reg)
    
    # Verify Invariance
    final_state = qpu.pull_state()
    for i in range(len(initial_state)):
        assert abs(final_state[i]) == approx(abs(initial_state[i]), abs=1e-5), \
            f"State drifted at index {i} for n={n}"
            
    # Verify Memory Cleanup
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    assert active_qubits == n, \
        f"Memory leak in Diffusion! Expected {n} active qubits, got {active_qubits}"