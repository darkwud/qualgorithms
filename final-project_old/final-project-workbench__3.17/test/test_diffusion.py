from functools import partial
from psiqworkbench import QPU, Qubits

# Import your specific implementation
from src.diffusion import diffusion_operator

############################################################
# Generic Runner
############################################################
def run_test_diffusion(n_qubits: int, quantum_op, label: str):
    """Executes the diffusion operator and checks invariance and memory limits."""
    # 1. Initialize QPU (Using the full statevector simulator)
    qpu = QPU(num_qubits=n_qubits + 1)
    reg = Qubits(n_qubits, "search_reg", qpu)
    
    # 2. Prepare the uniform superposition using the correct .had() syntax
    for i in range(n_qubits):
        reg[i].had()
        
    # Flush ops and get the baseline state vector
    qpu.flush()
    initial_state = qpu.pull_state()
    
    # 3. Apply the Diffusion Operator
    quantum_op(search_reg=reg, cond=None)
    
    # Flush again to ensure the diffusion gates are applied
    qpu.flush()
    
    # 4. Verify Invariance (The amplitude magnitudes should remain unchanged)
    final_state = qpu.pull_state()
    for i in range(len(initial_state)):
        diff = abs(abs(final_state[i]) - abs(initial_state[i]))
        if diff > 1e-5:
            raise Exception(f"Failed {label}: State drifted at index {i}. "
                            f"Expected ~{abs(initial_state[i])}, got {abs(final_state[i])}")
            
    # 5. Verify Memory Cleanup
    active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    if active_qubits != n_qubits:
        raise Exception(f"Failed {label}: Memory leak in Diffusion! "
                        f"Expected {n_qubits} active qubits, got {active_qubits}")

############################################################
# Test Cases
############################################################
def test_1_diffusion_invariance():
    test_cases = [
        (1, "1-qubit diffusion"),
        (2, "2-qubit diffusion"),
        (3, "3-qubit diffusion"),
        (5, "5-qubit diffusion")
    ]

    for n, label in test_cases:
        print(f"Testing Diffusion {label}: n={n}")
        
        # Bind the diffusion operator
        quantum_op = partial(diffusion_operator)
        
        # Execute the runner
        run_test_diffusion(n, quantum_op, label)