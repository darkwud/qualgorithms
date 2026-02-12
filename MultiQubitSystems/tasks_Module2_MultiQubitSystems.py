from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

# In all tasks in this assignment, use only primitive gates and measurements.
# Don't use libraries such as QuantumCircuit.initialize.

# Task 1. Prepare state (|00⟩ - |01⟩ - |10⟩ + |11⟩) / 2 ().
# Inputs:
#      1) A quantum circuit.
#      2) Two qubits in the |00⟩ state, represented as `QuantumRegister` of length 2.
# Goal: Change the state of the qubits to (|00⟩ - |01⟩ - |10⟩ + |11⟩) / 2.
# You need to prepare this state exactly (not up to a global phase).
def task_1_prepare_state(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    # For qubit 0: |0⟩ -> |1⟩ -> (|0⟩ - |1⟩)/√2
    circ.x(qr[0])
    circ.h(qr[0])
    
    # For qubit 1: |0⟩ -> |1⟩ -> (|0⟩ - |1⟩)/√2
    circ.x(qr[1])
    circ.h(qr[1])

# Task 2. Prepare state (|00⟩ + |01⟩ - |10⟩ + |11⟩) / 2 ().
# Inputs:
#      1) A quantum circuit.
#      2) Two qubits in the |00⟩ state, represented as `QuantumRegister` of length 2.
# Goal: Change the state of the qubits to (|00⟩ + |01⟩ - |10⟩ + |11⟩) / 2.
# You need to prepare this state exactly (not up to a global phase).
def task_2_prepare_state(circ: QuantumCircuit, qr: QuantumRegister) -> None:
   # Apply H to both qubits to create superposition
    circ.h(qr[0])
    circ.h(qr[1])
    
    # Apply Z to qubit 1 to flip sign of |01⟩ and |11⟩
    circ.z(qr[0])
    
    # Apply CZ to flip sign of |11⟩ back to positive
    circ.cz(qr[0], qr[1])
    
# Task 3. Prepare state (|00110011...⟩ + |11001100...⟩) / sqrt(2) ().
# Inputs:
#      1) A quantum circuit.
#      2) N qubits in the |0...0⟩ state, represented as `QuantumRegister` of length N.
# Goal: Change the state of the qubits to (|00110011...⟩ + |11001100...⟩) / sqrt(2).
#       Trim the bit strings to the length of the given quantum register.
#       For example, for N = 3 the required state is (|001⟩ + |110⟩) / sqrt(2).
# You need to prepare this state exactly (not up to a global phase).
def task_3_prepare_state(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    n = len(qr)
    
    # Create superposition on qr[0]
    circ.h(qr[0])
    
    # Set each other qubit
    for i in range(1, n):
        # Check if bit at position i matches bit at position 0
        same_as_first = ((i % 4) < 2) 
        
        if same_as_first:
            circ.cx(qr[0], qr[i])
        else:
            circ.x(qr[i])
            circ.cx(qr[0], qr[i])
    
# Task 4. Prepare state |0000...⟩ + |0011...⟩ + ... + |1100...⟩ + |1111...⟩ ().
# Inputs:
#      1) A quantum circuit.
#      2) N qubits in the |0...0⟩ state, represented as `QuantumRegister` of length N.
#         You are guaranteed that N will be even.
# Goal: Change the state of the qubits to an equal superposition of all the basis states for which
#        - qubits with indices 0 and 1 are in the same state,
#        - qubits with indices 2 and 3 are in the same state,
#        - and so on, qubits with indices 2k and 2k+1 are in the same state.
#       In other words, create an equal superposition of all the basis states
#       of the form |aabbccdd...⟩, where each letter denotes one bit.
#       Trim the bit strings to the length of the given quantum register.
#       For example, for N = 4 the required state is (|0000⟩ + |0011⟩ + |1100⟩ + |1111⟩) / 2.
# You need to prepare this state exactly (not up to a global phase).
def task_4_prepare_state(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    n = len(qr)
    
    # Apply H to even-indexed qubits
    for i in range(0, n, 2):
        circ.h(qr[i])
    
    # Copy each even qubit to its odd partner using CNOT
    for i in range(0, n, 2):
        circ.cx(qr[i], qr[i + 1])
    
# Task 5. Implement the signed SWAP gate ().
# Inputs:
#      1) A quantum circuit.
#      2) Two qubits in an arbitrary state, represented as `QuantumRegister` of length 2.
# Goal: Apply the sSWAP gate described with the following matrix to the qubits:
#     /  1  0  0  0  \
#    |   0  0 -1  0   |
#    |   0 -1  0  0   |
#     \  0  0  0  1  /
def task_5_signed_swap(circ: QuantumCircuit, qr: QuantumRegister) -> None:

    # Apply SWAP gate
    circ.swap(qr[0], qr[1])
    
    # Step 2: Apply Z to both qubits
    circ.z(qr[0])
    circ.z(qr[1])

# The multi-qubit measurement tasks are implemented as two functions each.
# 1. The "circuit" function should construct the measurement circuit; it should apply the necessary gates and end in a measurement.
# 2. The "decoder" function should take the bit string of measurement outcomes (0s and 1s), exactly as returned by Qiskit, and return an integer - the index of the state.
# You need to implement both functions for the task to pass the test.
# For convenience, the default decoder that converts the bit string to an integer is already implemented for you; 
# if it suits you, you don't need to reimplement it.
# (Remember that Qiskit reverts the order of qubits when producing measurement result; that's why decoder uses big-endian to convert bit string to integer.)

# Task 6. Distinguish two three-qubit states .
# You are given three qubits which are guaranteed to be in one of the two orthogonal states.
# Goal: Figure out which state the qubits are in:
#        - 0 if they are in the state (|001⟩ + |011⟩ + |100⟩ + |110⟩) / 2
#        - 1 if they are in the state (|000⟩ + |010⟩ + |101⟩ + |111⟩) / 2

# Task 6.1. The circuit function.
# Inputs:
#      1) A quantum circuit.
#      2) A `QuantumRegister` of length 3.
#      3) A classical register of length 3.
def task_6_measure_two_threequbit_states_circuit(circ: QuantumCircuit, qr: QuantumRegister, cr: ClassicalRegister) -> None:
    # Compute parity of qr[0] and qr[2] by XORing into qr[0]
    circ.cx(qr[2], qr[0])
    
    # Measure all qubits
    circ.measure(qr, cr)

# Task 6.2. The decoder function.
# Input: The bit string of measurement results produced by the circuit function.
# Return: The state the circuit function was given.
def task_6_measure_two_threequbit_states_decoder(meas: str) -> int:
    parity = int(meas[2])  # This is qr[0] after the CNOT
    
    # flip: parity 1 → return 0, parity 0 → return 1
    return 1 - parity

# Task 7. Distinguish four three-qubit states .
# You are given three qubits which are guaranteed to be in one of the four orthogonal states.
# Goal: Figure out which state the qubits are in:
#        - 0 if they are in the state |S0⟩ = (|000⟩ + |111⟩) / sqrt(2)
#        - 1 if they are in the state |S1⟩ = (|000⟩ - |111⟩) / sqrt(2)
#        - 2 if they are in the state |S2⟩ = (|011⟩ + |100⟩) / sqrt(2)
#        - 3 if they are in the state |S3⟩ = (|011⟩ - |100⟩) / sqrt(2)

# Task 7.1. The circuit function.
# Inputs:
#      1) A quantum circuit.
#      2) A `QuantumRegister` of length 3.
#      3) A classical register of length 3.
def task_7_measure_four_threequbit_states_circuit(circ: QuantumCircuit, qr: QuantumRegister, cr: ClassicalRegister) -> None:
    # CNOT from qr[0] to qr[1]
    circ.cx(qr[0], qr[1])
    
    # CNOT from qr[0] to qr[2]
    circ.cx(qr[0], qr[2])
    
    # Hadamard on qr[0] to detect phase
    circ.h(qr[0])
    
    # Measure
    circ.measure(qr, cr)

# Task 7.2. The decoder function.
# Input: The bit string of measurement results produced by the circuit function.
# Return: The state the circuit function was given.
def task_7_measure_four_threequbit_states_decoder(meas: str) -> int:
    # Index states by binary integer 
    q2 = int(meas[0])  
    q0 = int(meas[2]) 
    
    #q2 is the most significant bit
    return q2 * 2 + q0

# Task 8. Distinguish four two-qubit states .
# You are given two qubits which are guaranteed to be in one of the four orthogonal states.
# Goal: Figure out which state the qubits are in:
#        - 0 if they are in the state |S0⟩ = (1|00⟩ + 3|10⟩ + 2|01⟩ + 6|11⟩) / sqrt(50)
#        - 1 if they are in the state |S1⟩ = (3|00⟩ - 1|10⟩ + 6|01⟩ - 2|11⟩) / sqrt(50)
#        - 2 if they are in the state |S2⟩ = (2|00⟩ + 6|10⟩ - 1|01⟩ - 3|11⟩) / sqrt(50)
#        - 3 if they are in the state |S3⟩ = (6|00⟩ - 2|10⟩ - 3|01⟩ + 1|11⟩) / sqrt(50)

# Task 8.1. The circuit function.
# Inputs:
#      1) A quantum circuit.
#      2) A `QuantumRegister` of length 2.
#      3) A classical register of length 2.
def task_8_measure_four_twoqubit_states_circuit(circ: QuantumCircuit, qr: QuantumRegister, cr: ClassicalRegister) -> None:  
    # U_q1 transforms q1 basis to computational basis |0⟩, |1⟩
    U_q1 = (1/np.sqrt(5)) * np.array([[1, 2],[2, -1]])
    
    # U_q0 transforms q0 basis to computational basis |0⟩, |1⟩
    U_q0 = (1/np.sqrt(10)) * np.array([[1, 3],[3, -1]])
    
    # Apply U_q0 to qr[0] and U_q1 to qr[1]
    circ.unitary(U_q0, [qr[0]], label='U_q0')
    circ.unitary(U_q1, [qr[1]], label='U_q1')
    
    # Measure
    circ.measure(qr, cr)

# Task 8.2. The decoder function.
# Input: The bit string of measurement results produced by the circuit function.
# Return: The state the circuit function was given.
def task_8_measure_four_twoqubit_states_decoder(meas: str) -> int:
    # Index states by binary integer
    q1 = int(meas[0])
    q0 = int(meas[1])
    
    # q1 is the most significant bit
    return q1 * 2 + q0