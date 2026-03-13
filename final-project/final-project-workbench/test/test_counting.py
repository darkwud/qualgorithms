import pytest
from src.counting import quantum_counting

COUNTING_TEST_CASES = [
    ([1, 2, 3], 3, 3, "Standard 3-qubit search, 3-bit precision"),
    ([1], 1, 2, "Minimal 1-qubit search, 2-bit precision"),
    ([2, 2, 2], 10, 4, "Zero Solutions Case, 4-bit precision")
]

@pytest.mark.parametrize("weights, target, precision, label", COUNTING_TEST_CASES)
def test_quantum_counting_execution(weights, target, precision, label):
    # Execute the full algorithm
    measurement = quantum_counting(weights, target, precision_qubits=precision)
    
    #  Validate the Output
    assert isinstance(measurement, int), \
        f"Failed {label}: Expected integer measurement, got {type(measurement)}"
        
    max_possible_val = (2 ** precision) - 1
    assert 0 <= measurement <= max_possible_val, \
        f"Failed {label}: Measurement {measurement} out of bounds for {precision} precision qubits."