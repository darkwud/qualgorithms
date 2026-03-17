from functools import partial
import math
from psiqworkbench import QPU, Qubits

# Import your specific implementation
from src.grover import grover_iteration

############################################################
# Classical Reference Functions
############################################################
def f_subset_sum_match(subset_bits: list[bool], weights: list[int], target: int) -> bool:
    """Classically checks if a specific boolean subset selection matches the target sum."""
    subset_sum = sum(w for b, w in zip(subset_bits, weights) if b)
    return subset_sum == target

def f_count_solutions(weights: list[int], target: int) -> int:
    """Classically counts how many valid solutions exist in the dataset."""
    count = 0
    n = len(weights)
    for i in range(1 << n):
        subset_bits = [bool((i >> j) & 1) for j in range(n)]
        if f_subset_sum_match(subset_bits, weights, target):
            count += 1
    return count

def f_optimal_iterations(N: int, M: int) -> int:
    """Classically calculates the optimal number of Grover iterations."""
    if M == 0:
        return 0
    return math.floor((math.pi / 4) * math.sqrt(N / M))

############################################################
# Generic Runner
############################################################
def run_test_grover(n_items: int, total_qubits: int, quantum_op, f_iters, f_match, label: str):
    """Executes full Grover's algorithm and verifies it collapses to a valid answer."""
    optimal_iters = f_iters()
    
    # 1. Initialize the QPU with enough heap space (no BIT_DEFAULT, use statevector)
    qpu = QPU(num_qubits=total_qubits)
    search_reg = Qubits(n_items, "search", qpu)
    
    # 2. Put the search register into an equal superposition using the correct syntax!
    for i in range(n_items):
        search_reg[i].had()
        
    # 3. Apply the Grover iterations dynamically
    for _ in range(optimal_iters):
        quantum_op(search_reg=search_reg, cond=None)
        
    # 4. Measure the circuit
    meas_val = search_reg.read()
    
    # 5. Verify the measured integer maps to a correct subset
    subset_bits = [bool((meas_val >> j) & 1) for j in range(n_items)]
    is_solution = f_match(subset_bits=subset_bits)
    
    if not is_solution:
         raise Exception(f"Failed {label}: Grover diffusion failed to amplify target. "
                         f"Measured state {subset_bits} is not a valid solution.")

############################################################
# Test Cases
############################################################
def test_1_grover_amplification():
    test_cases = [
        ([1, 2, 3], 3, "Standard 3-item oracle"), 
        ([1, 1, 1], 2, "Multi-solution Grover search")   
    ]

    for weights, target, label in test_cases:
        n_items = len(weights)
        N_space = 1 << n_items
        M_solutions = f_count_solutions(weights, target)
        
        # Calculate bits for the summary
        max_val = max(sum(weights), target)
        sum_bits = max(1, max_val.bit_length())
        total_qubits = n_items + sum_bits + 1

        # This print will show up in the terminal when running pytest -s
        print(f"\n--- Grover Test: {label} ---")
        print(f"  Configuration: Space={N_space}, Solutions={M_solutions}")
        print(f"  Hardware Footprint: {total_qubits} Qubits ({n_items} search + {sum_bits} sum + 1 buffer)")
        
        if M_solutions == 0:
            print(f"  Skipping: 0 solutions found.")
            continue
        
        # ... (rest of your binding and execution code) ...
        
        # Bind functions
        f_iters = partial(f_optimal_iterations, N=N_space, M=M_solutions)
        f_match = partial(f_subset_sum_match, weights=weights, target=target)
        quantum_op = partial(grover_iteration, weights=weights, target=target)
        
        # Execute the runner
        run_test_grover(n_items, total_qubits, quantum_op, f_iters, f_match, label)