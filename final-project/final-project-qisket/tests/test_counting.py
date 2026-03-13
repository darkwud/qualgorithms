from qiskit_aer import AerSimulator
from qiskit import transpile
from Final_Project.oracle import subset_sum_oracle
from Final_Project.counting import quantum_counting_circuit, estimate_solutions
import pytest


# These represent four distinct "scenarios" to prove our algorithm works.
# (weights, target, expected_M, label)
FINAL_TEST_SUITE = [
    ([1, 2, 3], 3, 2, "Standard M=2"), # Standard Search. Subsets {1,2} and {3} both sum to 3.
    ([1, 1, 1, 1], 2, 6, "High Density M=6"), # High Density. Many ways to get the target (6 combinations).
    ([2, 2, 2], 1, 0, "Zero Solution M=0"), # Edge Case (Zero). No possible combination sums to 1.
    ([1], 1, 1, "Minimal n=1 Case") # Minimal Case. Only one qubit, one possible solution.
]

# Runs the test function 4 separate times, once for each case above.
@pytest.mark.parametrize("weights, target, expected_M, label", FINAL_TEST_SUITE)

def test_system_accuracy(weights, target, expected_M, label):
    """
    Automated Accuracy Test:
    Ensures the 'Most Probable' measurement from the quantum circuit 
    maps back to the correct classical solution count.
    """
    n = len(weights)
    t = 6 # Using 6 qubits for higher resolution
    
    # Circuit Assmembly
    oracle = subset_sum_oracle(weights, target)
    qc = quantum_counting_circuit(n, oracle, counting_qubits=t)
    
    # Simulation
    backend = AerSimulator()
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=1024).result()
    counts = result.get_counts()
    
    # Pick the most likely outcome
    measured_str = max(counts, key=counts.get)
    # Qiskit bitstrings are LSB (rightmost) to MSB (leftmost)
    measured_int = int(measured_str, 2)
    
    # Calculation
    # Use the sin^2 formula to convert the measured integer into a solution count M.
    actual_M = estimate_solutions(measured_int, n, t)
    
    # Assert with a small tolerance (Quantum Counting is an estimate)
    # For these small N, it should be exactly correct when rounded.
    assert actual_M == expected_M, f"Failed {label}: Expected {expected_M}, got {actual_M} (Measured: {measured_str})"