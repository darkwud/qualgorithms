from .oracle import subset_sum_oracle
from .diffusion import diffusion_operator

def grover_iteration(search_reg, weights, target, cond=None, sum_reg=None):

    # Apply full grover
    subset_sum_oracle(search_reg, weights, target, cond=cond, sum_reg=sum_reg)
    diffusion_operator(search_reg, cond=cond)