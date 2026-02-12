from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# In all tasks in this assignment, use only primitive gates and measurements.
# Don't use libraries such as QuantumCircuit.initialize.

# Task 1. Clone |+⟩ and |-⟩ states.
# Inputs:
#      1) A quantum circuit.
#      2) A data qubit that is guaranteed to be in |+⟩ or |-⟩ state, represented as `QuantumRegister` of length 1.
#      3) A scratch qubit that is guaranteed to be in the |0⟩ state, represented as `QuantumRegister` of length 1.
# Goal: Implement a unitary transformation that will clone the data qubit state onto the scratch qubit,
#       i.e., will transform |+, 0⟩ into |+, +⟩ and |-, 0⟩ into |-, -⟩.
# Do not use measurements.
def task_1_clone_plus_minus(circ: QuantumCircuit, data: QuantumRegister, scratch: QuantumRegister) -> None:

    # convert to Hadarmard
    circ.h(data[0]) 

    # clone using CNOT
    circ.cx(data[0], scratch[0])
    
    # convert both qubits to |+⟩ |-⟩ basis
    circ.h(data[0])
    circ.h(scratch[0])

# Task 2. Delete |+⟩ and |-⟩ states.
# Inputs:
#      1) A quantum circuit.
#      2) Two qubits that are guaranteed to be in |++⟩ or |--⟩ state, represented as `QuantumRegister` of length 2.
# Goal: Implement a unitary transformation that will delete the data from the second qubit while leaving the first qubit in its state,
#       i.e., will transform |+, +⟩ into |+, 0⟩ and |-, -⟩ into |-, 0⟩.
# Do not use measurements.
def task_2_delete_plus_minus(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    
    # Convert both qubits from |+⟩ and |-⟩ to |0⟩ and |1⟩ 
    circ.h(qr[0])
    circ.h(qr[1])

    # Unclone CNOT
    circ.cx(qr[0], qr[1])

    # Convert back to |+⟩ and |-⟩
    circ.h(qr[0])

# Task 3. Superdense coding using |Ψ⁺⟩ = (|01⟩ + |10⟩) / sqrt(2)
# This task considers a modification of the superdense coding protocol 
# in which the pair of qubits shared by sender and receiver are entangled in a state |Ψ⁺⟩ = (|01⟩ + |10⟩) / sqrt(2).
# 
# The sender performs the standard message encoding operation on their qubit (see the testing harness for details).
# After this they send their qubit to the receiver.
#
# Inputs:
#      1) A quantum circuit.
#      2) Sender's and receiver's qubits (in that order), represented as `QuantumRegister` of length 2.
# Goal: Implement the receiver's part of the protocol (the message decoding) before the final measurement so that it produces the sender's message.
# The measurements will be done by the testing harness; you need to apply the gates to the qubits 
# so that measurement result is the same message the sender encoded in their qubit (in little-endian).
def task_3_superdense_coding(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    
    # Standard Bell measurement
    circ.cx(qr[0], qr[1])
    circ.h(qr[0])

    # Flip second bit
    circ.x(qr[1])

# Task 4. Teleportation using |Ψ⁻⟩ = (|10⟩ - |01⟩) / sqrt(2).
# This task considers a modification of the teleportation protocol
# in which the pair of qubits shared by the sender and the receiver are entangled in a state (|10⟩ - |01⟩) / sqrt(2),
# where the first qubit in ket notation denotes the sender's qubit and the second one - the receiver's qubit.
#
# The sender has a message qubit in the state |ψ⟩ = α|0⟩ + β|1⟩.
# They perform the standard message sending operation on the message qubit and their part of the entangled pair (see the testing harness for details).
# After this they send the two measured bits to the receiver.
#
# Inputs:
#      1) A quantum circuit.
#      2) The receiver's qubit, represented as `QuantumRegister` of length 1.
#      3) Two measured bits, the bit produced by measuring the message qubit and the bit produced by measuring the sender's qubit, represented as `ClassicalRegister` of length 2.
# Goal: Implement the receiver's part of the protocol (fixup of the received state) so that the receiver's qubit ends up in the state |ψ⟩.
# You are allowed to introduce a global phase to the teleported state; for example, ending up with a qubit in state -|ψ⟩ is fine.
def task_4_teleportation(circ: QuantumCircuit, receiver: QuantumRegister, bits: ClassicalRegister) -> None:

    # Apply Z gate when measurement (bits[0]) = 0
    with circ.if_test((bits[0], 0)):
        circ.z(receiver[0])

    # Apply X gate when measurement (bits[1]) = 0
    with circ.if_test((bits[1], 0)):
        circ.x(receiver[0])

# Task 5. H gate teleportation.
# The sender and the receiver share a qubit in the state (I ⊗ H)(|00⟩ + |11⟩) / sqrt(2) = 1/2 (|00⟩ + |01⟩ + |10⟩ - |11⟩)
# (the Hadamard gate is applied to the receiver's qubit).
# The sender has a qubit in the state |ψ⟩ = α|0⟩ + β|1⟩.
# They want to send to the receiver the state H|ψ⟩ without the receiver applying an H gate to their qubit (this is called gate teleportation).
# 
# The sender performs the standard message sending operation on the message qubit and their part of the entangled pair (see the testing harness for details).
# After this they send the two measured bits to the receiver.
#
# Goal: Implement the receiver's part of the protocol (fixup of the received state) so that the receiver's qubit ends up in the state H|ψ⟩.
# You can only use the Pauli gates; you can not use H or arbitrary rotation gates.
# You are allowed to introduce a global phase to the teleported state; for example, ending up with a qubit in state -H|ψ⟩ is fine.
def task_5_gate_teleportation(circ: QuantumCircuit, receiver: QuantumRegister, bits: ClassicalRegister) -> None:
    
    # Apply Z gate on bit[1] = 1 -> X
    with circ.if_test((bits[1], 1)):
        circ.z(receiver[0])

    # Apply X gate on bit[0] = 1 -> Z
    with circ.if_test((bits[0], 1)):
        circ.x(receiver[0])