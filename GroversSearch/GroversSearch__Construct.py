import math
from psiqworkbench import Qubits

def task_1_sum_of_bits(x: Qubits | list, y: Qubits, s: int) -> None:
    n = len(x)
    num_ancillae = math.ceil(math.log2(n + 1))
    
    qpu = y.qpu
    count = Qubits(num_ancillae, qpu=qpu)
    
    c_masks = [count[i].mask() for i in range(num_ancillae)]
    x_masks = [bit.mask() for bit in x]
    y_mask = y.mask()
    c_full_mask = count.mask()
    
    # --- 1. COMPUTE SUM (Optimized Bounds) ---
    for b_idx, b_mask in enumerate(x_masks):
        # Calculate the highest counter bit that could possibly flip at this stage
        max_i = min(num_ancillae - 1, (b_idx + 1).bit_length() - 1)
        
        # Carries (descending)
        for i in range(max_i, 0, -1):
            ctrl_mask = b_mask
            for j in range(i):
                ctrl_mask |= c_masks[j]
            qpu.x(c_masks[i], ctrl_mask)
        # LSB
        qpu.x(c_masks[0], b_mask)

    # --- 2. CHECK EQUALITY ---
    for i in range(num_ancillae):
        if not (s & (1 << i)):
            qpu.x(c_masks[i])
    
    qpu.x(y_mask, c_full_mask)

    # --- 3. UNCOMPUTE EQUALITY ---
    for i in range(num_ancillae):
        if not (s & (1 << i)):
            qpu.x(c_masks[i])

    # --- 4. UNCOMPUTE SUM (Exact Mirror) ---
    for b_idx in reversed(range(n)):
        b_mask = x_masks[b_idx]
        # Same dynamic bound calculation
        max_i = min(num_ancillae - 1, (b_idx + 1).bit_length() - 1)
        
        # LSB first
        qpu.x(c_masks[0], b_mask)
        # Carries (ascending)
        for i in range(1, max_i + 1):
            ctrl_mask = b_mask
            for j in range(i):
                ctrl_mask |= c_masks[j]
            qpu.x(c_masks[i], ctrl_mask)
            
    # EXPLICIT RELEASE
    count.release()


# ==========================================
# Task 2: Row Constraints
# ==========================================
def task_2_row_constraints(x: Qubits, y: Qubits, row_constr: list[int]) -> None:
    r = len(row_constr)
    c = len(x) // r
    qpu = y.qpu
    
    row_status = Qubits(r, qpu=qpu)
    
    # Compute: Check each row
    for i in range(r):
        row_qubits = x[i*c : (i+1)*c]
        task_1_sum_of_bits(row_qubits, row_status[i], row_constr[i])
        
    # Check Equality: If all rows are correct, flip y
    qpu.x(y.mask(), row_status.mask())
    
    # Uncompute: Exact reverse order
    for i in reversed(range(r)):
        row_qubits = x[i*c : (i+1)*c]
        task_1_sum_of_bits(row_qubits, row_status[i], row_constr[i])
        
    row_status.release()


# ==========================================
# Task 3: Column Constraints
# ==========================================
def task_3_col_constraints(x: Qubits, y: Qubits, col_constr: list[int]) -> None:
    c = len(col_constr)
    r = len(x) // c
    qpu = y.qpu
    
    col_status = Qubits(c, qpu=qpu)
    
    # Compute: Check each column
    for j in range(c):
        col_qubits = [x[i*c + j] for i in range(r)]
        task_1_sum_of_bits(col_qubits, col_status[j], col_constr[j])
        
    # Check Equality: If all columns are correct, flip y
    qpu.x(y.mask(), col_status.mask())
    
    # Uncompute: Exact reverse order
    for j in reversed(range(c)):
        col_qubits = [x[i*c + j] for i in range(r)]
        task_1_sum_of_bits(col_qubits, col_status[j], col_constr[j])
        
    col_status.release()


# ==========================================
# Task 4: The Full Kakuro Puzzle
# ==========================================
def task_4_kakuro_puzzle(x: Qubits, y: Qubits, row_constr: list[int], col_constr: list[int]) -> None:
    qpu = y.qpu
    
    status = Qubits(2, qpu=qpu)
    rows_ok = status[0]
    cols_ok = status[1]
    
    # Compute
    task_2_row_constraints(x, rows_ok, row_constr)
    task_3_col_constraints(x, cols_ok, col_constr)
    
    # Check Equality: If both are valid, flip y
    qpu.x(y.mask(), status.mask())
    
    # Uncompute: Reverse order of compute steps
    task_3_col_constraints(x, cols_ok, col_constr)
    task_2_row_constraints(x, rows_ok, row_constr)
    
    status.release()