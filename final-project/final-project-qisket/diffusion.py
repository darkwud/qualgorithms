from qiskit import QuantumCircuit

def diffusion_operator(n: int) -> QuantumCircuit:
    """
    Builds the Grover diffusion operator for n qubits.
    Reflects amplitudes about the average/mean.
    """
    qc = QuantumCircuit(n, name="Diffusion")

    # H on all qubits (go to superposition basis)
    qc.h(range(n))

    # X on all qubits
    qc.x(range(n))

    # The Phase Flip (|11...1>)
    if n == 1:
        # For 1 qubit, we just need a Z gate to flip the phase of |1>
        qc.z(0)
    else:
        # For n > 1, use the Multi-Controlled Z logic
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)

    # Undo X
    qc.x(range(n))

    # Undo H
    qc.h(range(n))

    return qc