import math
from psiqworkbench import QPU, Qubits
from psiqworkbench.resource_estimation.qre import SymbolicQPU
from .grover import grover_iteration

def apply_iqft(reg):
    """
    Inverse Quantum Fourier Transform.
    """
    n = len(reg)
    
    # Native IQFT
    if hasattr(reg, 'iqft'):
        reg.iqft()
        return

    # Swaps
    if hasattr(reg[0], 'swap'):
        for i in range(n // 2):
            reg[i].swap(reg[n - 1 - i])
            
    # Controlled Phases and Hadamards
    for j in range(n):
        for m in range(j):
            angle = -math.pi / (2 ** (j - m))
            if hasattr(reg[j], 'rz'):
                reg[j].rz(angle, cond=reg[m])
            elif hasattr(reg[j], 'p'):
                reg[j].p(angle, cond=reg[m])
        reg[j].had()


def quantum_counting(weights: list[int], target: int, precision_qubits: int = 4, return_qpu: bool = False):
    """
    Executes Quantum Counting to determine the number of valid subsets.
    """
    n = len(weights)
    
    # Memory allocation
    max_val = max(sum(weights), target)
    sum_bits = max(1, max_val.bit_length())
    
    total_qpu_qubits = precision_qubits + n + (sum_bits * 2) + 2 + 5 
    
    total_qpu_qubits = precision_qubits + n + (sum_bits * 2) + 2 + 5 
    qpu = QPU(num_qubits=total_qpu_qubits)
    
    count_reg = Qubits(precision_qubits, "count_reg", qpu)
    search_reg = Qubits(n, "search_reg", qpu)
    
    sum_reg = Qubits(sum_bits, "sum_reg", qpu)
    
    # Superposition
    for i in range(precision_qubits):
        count_reg[i].had()
    for i in range(n):
        search_reg[i].had()
        
    # Controlled Grover Iterations
    for j in range(precision_qubits):
        iterations = 2 ** j
        for _ in range(iterations):

            grover_iteration(search_reg, weights, target, cond=count_reg[j], sum_reg=sum_reg)
            
    # Inverse QFT
    apply_iqft(count_reg)
    
    if return_qpu:
        return qpu
    
    # Measure
    measurement = count_reg.read()

    N = 2 ** n 
    phi = measurement / (2 ** precision_qubits)
    M = N * (math.sin(math.pi * phi) ** 2)
    
    if M > N / 2:
        M = N - M
        
    return int(round(M))