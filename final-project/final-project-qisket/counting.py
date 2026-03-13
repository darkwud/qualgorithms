from qiskit import QuantumCircuit
import numpy as np
from Final_Project.grover import grover_iteration


def inverse_qft(circuit, qubits):
    """
    Performs the Inverse Quantum Fourier Transform (IQFT).
    Purpose: To convert phase information stored in the counting qubits 
    into a measurable binary integer (m) which we then use to calculate the phase fraction (phi).
    """
    n = len(qubits)
    # Reverse the order of qubits to match QFT mathematical convention
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - i - 1])

    # Apply controlled phase rotations
    for j in range(n):
        for m in range(j):
            # Apply negative rotations to 'undo' the QFT phase
            angle = -np.pi / (2 ** (j - m))
            circuit.cp(angle, qubits[j], qubits[m])
        circuit.h(qubits[j])


def controlled_grover(oracle, power):
    """
    Builds a Grover operator (G) raised to a power (2^i) and makes it 'Controlled'.
    
    Purpose: In Quantum Phase Estimation, we must apply the operator 
    periodically to create interference patterns in the counting register.
    """

    # Construct the base Grover iteration: G = D * O
    single_g = grover_iteration(oracle)
    
    # 2. Convert to a gate and raise to the required power
    # This repeats the [Oracle + Diffusion] sequence 2^i times
    g_gate = single_g.to_gate(label=f"G^{power}").power(power)

    # Return controlled gate (1 control qubit)
    return g_gate.control(1)


def quantum_counting_circuit(n, oracle, counting_qubits=4):
    """
    The main architectural assembly for the Quantum Counting system.
    n: number of qubits in search register (where the subsets are, the length of weights)
    counting_qubits (t): qubits in the 'precision' register (the ruler)
    """
    # Total qubits: counting + search
    qc = QuantumCircuit(counting_qubits + n, counting_qubits)
    counting = list(range(counting_qubits))
    search = list(range(counting_qubits, counting_qubits + n))

    # Initialize counting and search qubits
    qc.h(counting)
    qc.h(search)

    # Apply controlled Grover iterations
    # Each counting qubit 'i' controls the application of Grover 2^i times.
    for i in range(counting_qubits):
        power = 2 ** i
        controlled_G = controlled_grover(oracle, power)
        qc.append(controlled_G, [counting[i]] + search)

    # Apply inverse QFT on counting qubits
    # Extract the rotation frequency from the counting qubits
    inverse_qft(qc, counting)

    # Measure
    # Collapse the counting register into a binary string
    qc.measure(counting, counting)
    return qc


def estimate_solutions(measured_value, n, counting_qubits):
    N = 2 ** n
    # phi is the value in [0, 1]
    phi = measured_value / (2 ** counting_qubits)
    
    # Standard Quantum Counting formula:
    # The phase measured (theta) relates to M/N via sin^2(theta/2) = M/N
    # Here, theta = 2 * pi * phi. So theta/2 = pi * phi.
    
    # IMPORTANT: We need the angle relative to the rotation.
    # For Grover, M = N * sin^2(phi * pi) is the standard.
    
    M = N * (np.sin(np.pi * phi) ** 2)
    
    # If M > N/2, you are likely measuring the "null" space.
    # In Grover search, M is usually small.
    if M > N / 2:
        M = N - M
        
    return int(round(M))