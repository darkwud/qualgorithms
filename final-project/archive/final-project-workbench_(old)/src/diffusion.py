def diffusion_operator(search_reg, cond=None):
    """Applies the Grover diffusion operator"""
    n = len(search_reg)
    
    # Apply H and X
    for q in search_reg:
        q.had(cond=cond)
        q.x(cond=cond)
        
    # Multi-controlled Z
    z_mask = 0
    if cond is not None:
        z_mask |= cond._qubit_mask
        
    if n > 1:
        z_mask |= search_reg[:-1]._qubit_mask
        
    # Apply Z 
    final_cond = z_mask if z_mask != 0 else None
    search_reg[-1].z(cond=final_cond)
    
    # Uncompute
    for q in search_reg:
        q.x(cond=cond)
        q.had(cond=cond)