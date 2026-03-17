from functools import partial
from src.counting import quantum_counting

# Calculare expected number of solutions
def f_count_subset_sum(weights: list[int], target: int) -> int:
    count = 0
    n = len(weights)
    # Iterate over all 2^n possible subsets
    for i in range(1 << n):
        subset_sum = sum(weights[j] for j in range(n) if (i & (1 << j)))
        if subset_sum == target:
            count += 1
    return count

# Validate bounds
def run_test_counting(precision: int, quantum_op, f, label: str):
    # Run the quantum computation
    measurement = quantum_op()
    
    expected_count = f()

    # Validate the Output Types and Bounds
    if not isinstance(measurement, int):
        raise Exception(f"Failed {label}: Expected integer measurement, got {type(measurement)}")
        
    max_possible_val = (2 ** precision) - 1
    if measurement < 0 or measurement > max_possible_val:
        raise Exception(f"Failed {label}: Measurement {measurement} out of bounds for {precision} precision qubits.")

def test_1_quantum_counting_execution():
    test_cases = [
        ([1, 2, 3], 3, 3, "Standard 3-qubit search, 3-bit precision"),
        ([1], 1, 2, "Minimal 1-qubit search, 2-bit precision"),
        ([2, 2, 2], 10, 4, "Zero Solutions Case, 4-bit precision")
    ]

    for weights, target, precision, label in test_cases:
        print(f"Testing {label}: {weights=}, {target=}, {precision=}")
        
        # Use partial to bind the arguments
        f = partial(f_count_subset_sum, weights=weights, target=target)
        quantum_op = partial(quantum_counting, weights, target, precision_qubits=precision)
        
        # Pass to the runner
        run_test_counting(precision, quantum_op, f, label)