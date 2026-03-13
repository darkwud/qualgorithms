from psiqworkbench import Qubits
import math
from grover import grover_iteration

def apply_iqft(reg: Qubits) -> None:
    """Applies the Inverse Quantum Fourier Transform (IQFT)."""
    n = len(reg)
    for j in range(n - 1, -1, -1):
        for m in range(n - 1, j, -1):
            angle = -math.pi / (2 ** (m - j))
            reg[j].rz(angle, cond=reg[m])
        reg[j].had()
        
    for i in range(n // 2):
        mirror_idx = n - i - 1
        reg[i].swap(reg[mirror_idx])

def quantum_counting(weights: list[int], target: int, precision_qubits: int = 4) -> int:
    """
    Executes Quantum Counting to determine the number of valid subsets.
    Returns the raw integer measurement of the counting register.
    """
    n = len(weights)
    
    # 1. Memory Calculation
    max_val = max(sum(weights), target)
    sum_bits = max(1, max_val.bit_length())
    
    total_qpu_qubits = precision_qubits + n + (sum_bits * 2) + 2 + 5 
    
    from psiqworkbench import QPU
    qpu = QPU(num_qubits=total_qpu_qubits)
    
    count_reg = Qubits(precision_qubits, "count_reg", qpu)
    search_reg = Qubits(n, "search_reg", qpu)
    
    # --- PRE-ALLOCATE THE SCRATCHPAD HERE ---
    # This prevents the QPU from crashing during the QPE loops!
    sum_reg = Qubits(sum_bits, "sum_reg", qpu)
    
    # 2. Superposition
    for i in range(precision_qubits):
        count_reg[i].had()
    for i in range(n):
        search_reg[i].had()
        
    # 3. Controlled Grover Iterations
    for j in range(precision_qubits):
        iterations = 2 ** j
        for _ in range(iterations):
            # Pass the shared sum_reg into every iteration
            grover_iteration(search_reg, weights, target, cond=count_reg[j], sum_reg=sum_reg)
            
    # 4. Inverse QFT
    apply_iqft(count_reg)
    
    # 5. Measure
    measurement = count_reg.read()

    # 6. Classical Post-Processing (The Translation)
    N = 2 ** n  # Total number of possible subsets
    phi = measurement / (2 ** precision_qubits)
    M = N * (math.sin(math.pi * phi) ** 2)
    
    if M > N / 2:
        M = N - M
        
    return int(round(M))