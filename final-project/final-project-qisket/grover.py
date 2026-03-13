from qiskit import QuantumCircuit
from Final_Project.diffusion import diffusion_operator

def grover_iteration(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Builds one Grover iteration: G = D * O
    """

    # Size of the search space (n qubits)
    n = oracle.num_qubits
    qc = QuantumCircuit(n, name="GroverIteration")

    # Apply the Phase Oracle (O)
    # The Oracle 'marks' the correct subsets by flipping their phase to negative.
    # .compose() attaches the oracle gates to our main iteration circuit.
    qc.compose(oracle, inplace=True)

    # Apply the Diffusion Operator (D)
    # The Diffusion operator (also called the 'Inversion about the Mean')
    # transforms those negative phases into increased probabilities.
    qc.compose(diffusion_operator(n), inplace=True)

    # Return the combined operator G
    return qc