import pytest
from counting import quantum_counting

# Test Scenarios: (Weights, Target, Precision Qubits, Label)
COUNTING_TEST_CASES = [
    ([1, 2, 3], 3, 3, "Standard 3-qubit search, 3-bit precision"),
    ([1], 1, 2, "Minimal 1-qubit search, 2-bit precision"),
    ([2, 2, 2], 10, 4, "Zero Solutions Case, 4-bit precision")
]

@pytest.mark.parametrize("weights, target, precision, label", COUNTING_TEST_CASES)
def test_quantum_counting_execution(weights, target, precision, label):
    """
    Tests that the complete Quantum Counting algorithm compiles, 
    dynamically sizes its QPU environment, executes the IQFT, 
    and successfully collapses the state into a classical measurement.
    """
    # 1. Execute the full algorithm
    measurement = quantum_counting(weights, target, precision_qubits=precision)
    
    # 2. Validate the Output
    assert isinstance(measurement, int), \
        f"Failed {label}: Expected integer measurement, got {type(measurement)}"
        
    max_possible_val = (2 ** precision) - 1
    assert 0 <= measurement <= max_possible_val, \
        f"Failed {label}: Measurement {measurement} out of bounds for {precision} precision qubits."
