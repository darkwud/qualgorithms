# analyze.py
# IMPORTANT: Check your Construct 'Learning' docs or sample projects for the 
# exact Bartiq import paths if these specific method names throw an ImportError.

import bartiq 
from counting import quantum_counting

def run_scaling_analysis():
    # 1. Define a problem size that would instantly crash a local simulator.
    # A state vector simulator would need millions of Terabytes of RAM for n=30.
    # The Resource Analyzer won't simulate the math, so it will process this instantly.
    weights = [i for i in range(1, 31)]  # [1, 2, 3... 30]
    target = 150
    precision = 5
    
    n = len(weights)
    print(f"Compiling Quantum Counting for n={n} weights...")

    # 2. Trace the Routine
    # This intercepts all your QPU calls (like .add() and .had()) and compiles 
    # them into a hardware-agnostic symbolic graph rather than simulating them.
    compiled_routine = bartiq.trace(
        quantum_counting, 
        weights=weights, 
        target=target, 
        precision_qubits=precision
    )

    # 3. Run the Resource Estimator
    # This applies FTQC fault-tolerant routing and magic-state distillation 
    # logic to your compiled graph to estimate the true hardware cost.
    report = bartiq.estimate_resources(compiled_routine)

    # 4. Print the Scaling Data
    print("\n" + "="*40)
    print(f" FTQC SCALING DATA: SUBSET SUM (n={n})")
    print("="*40)
    # Note: Property names (like .logical_qubits) might be nested under different 
    # keys in the report dictionary depending on your QDE version.
    print(f"Peak Logical Qubits: {report.logical_qubits}")
    print(f"Total T-Gate Count:  {report.t_count}")
    print(f"Algorithmic Depth:   {report.logical_depth}")
    print("="*40)

if __name__ == "__main__":
    run_scaling_analysis()