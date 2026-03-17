def diffusion_operator(search_reg, cond=None):
    """Applies the Grover diffusion operator, optionally controlled."""
    n = len(search_reg)
    
    # 1. Apply H and X
    for q in search_reg:
        q.had(cond=cond)
        q.x(cond=cond)
        
    # 2. Multi-controlled Z (Using Hardware Bitmasks)
    z_mask = 0
    if cond is not None:
        z_mask |= cond._qubit_mask
        
    if n > 1:
        # Add the rest of the search register to the control mask
        z_mask |= search_reg[:-1]._qubit_mask
        
    # Apply Z using the combined integer mask
    final_cond = z_mask if z_mask != 0 else None
    search_reg[-1].z(cond=final_cond)
    
    # 3. Uncompute
    for q in search_reg:
        q.x(cond=cond)
        q.had(cond=cond)