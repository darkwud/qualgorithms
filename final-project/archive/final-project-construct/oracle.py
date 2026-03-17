from psiqworkbench import Qubits

def get_mask(q):
    """Helper to safely extract the hardware bitmask from a Qubits object."""
    if q is None: 
        return 0
    return q._qubit_mask if hasattr(q, '_qubit_mask') else q

def subset_sum_oracle(search_reg, weights, target, cond=None, sum_reg=None):
    """Marks valid subsets that sum to the target, optionally controlled."""
    n = len(weights)
    qpu = search_reg.qpu
    
    cond_mask = get_mask(cond)
    
    # Track if we need to clean up the heap ourselves
    allocated_here = False
    
    if sum_reg is None:
        max_val = max(sum(weights), target)
        sum_bits = max(1, max_val.bit_length())
        sum_reg = Qubits(sum_bits, "sum_reg", qpu)
        allocated_here = True
        
    sum_bits = len(sum_reg)
    
    # --- 1. FORWARD ARITHMETIC ---
    for i in range(n):
        ctrl_mask = cond_mask | get_mask(search_reg[i])
        sum_reg.add(weights[i], condition_mask=ctrl_mask)
        
    sum_reg.subtract(target, condition_mask=cond_mask)
    
    # --- 2. PHASE FLIP ---
    for q in sum_reg:
        q.x(cond=cond)
        
    flip_mask = cond_mask
    if sum_bits > 1:
        flip_mask |= get_mask(sum_reg[:-1])
            
    sum_reg[-1].z(cond=flip_mask if flip_mask != 0 else None)
    
    # UNCOMPUTE THE X GATES!
    for q in sum_reg:
        q.x(cond=cond)
    
    # --- 3. REVERSE ARITHMETIC (UNCOMPUTATION) ---
    sum_reg.add(target, condition_mask=cond_mask)
    
    for i in range(n - 1, -1, -1):
        ctrl_mask = cond_mask | get_mask(search_reg[i])
        sum_reg.subtract(weights[i], condition_mask=ctrl_mask)
        
    # --- 4. EXPLICIT FREE (SYSTEMS LEVEL) ---
    if allocated_here:
        qpu._get_qubit_heap().allocated_mask &= ~sum_reg._qubit_mask