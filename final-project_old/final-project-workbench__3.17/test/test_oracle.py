from functools import partial
from psiqworkbench import QPU, Qubits
from src.oracle import subset_sum_oracle

# Memory Leak test
def run_test_oracle_memory(n_items: int, total_qubits: int, quantum_op, label: str):
    """Executes the oracle to ensure perfect uncomputation and memory management."""
    
    # Iterate through every possible subset input
    for i in range(1 << n_items):

        qpu = QPU(num_qubits=total_qubits) 
        search_reg = Qubits(n_items, "search", qpu)
        search_reg.write(i)
        
        quantum_op(search_reg=search_reg, cond=None)
        qpu.flush()
        
        # Verify we have correct inpyt
        res_x = search_reg.read()
        if res_x != i:
            raise Exception(f"Failed {label}: Oracle altered the input register! Expected {i}, got {res_x}")

        active_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
        if active_qubits != n_items:
            raise Exception(f"Failed {label} on input {i}: Memory leak detected! "
                            f"Oracle failed to uncompute and release auxiliary qubits.")

# Perform on couple of test cases
def test_1_oracle_memory_integrity():
    test_cases = [
        ([1, 2, 3], 3, "Standard 3-item oracle"),
        ([5, 10], 15, "2-item exact match"),
        ([2, 2, 2], 10, "Zero solutions oracle")
    ]

    for weights, target, label in test_cases:
        print(f"Testing Oracle Memory Integrity {label}: {weights=}, {target=}")
        n_items = len(weights)
        
        # Allocate memory
        max_val = max(sum(weights), target)
        sum_bits = max(1, max_val.bit_length())
        total_qubits = n_items + sum_bits + 1 
        
        quantum_op = partial(subset_sum_oracle, weights=weights, target=target)
        
        # Check Memory Leak
        run_test_oracle_memory(n_items, total_qubits, quantum_op, label)