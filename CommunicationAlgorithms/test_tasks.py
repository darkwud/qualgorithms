from math import pi, sqrt, cos, sin, atan2
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from pytest import approx
from .tasks_Module31_CommunicationAlgorithms import *

# Create the simulator instance to add save_statevector method to QuantumCircuit
simulator = AerSimulator(method='statevector')

def test_1_clone_plus_minus():
    for state_ind in [0, 1]:
        # Construct the circuit
        data = QuantumRegister(1)
        scratch = QuantumRegister(1)
        circ = QuantumCircuit(data, scratch)
        circ.initialize([1, 1] if state_ind == 0 else [1, -1], data, normalize=True)
        task_1_clone_plus_minus(circ, data, scratch)
        circ.save_statevector()

        circ = transpile(circ, backend=simulator)
        res = simulator.run(circ).result()
        actual_vector = res.get_statevector().data

        expected_vector = [0.5, 0.5, 0.5, 0.5] if state_ind == 0 else [0.5, -0.5, -0.5, 0.5]

        if actual_vector != approx(expected_vector):
            print("Expected state vector:")
            print(expected_vector)
            print("Actual state vector:")
            print(actual_vector)
            raise ValueError("State vectors should be equal")


def test_2_delete_plus_minus():
    for state_ind in [0, 1]:
        # Construct the circuit
        qr = QuantumRegister(2)
        circ = QuantumCircuit(qr)
        circ.initialize([0.5, 0.5, 0.5, 0.5] if state_ind == 0 else [0.5, -0.5, -0.5, 0.5], qr, normalize=True)
        task_2_delete_plus_minus(circ, qr)
        circ.save_statevector()

        circ = transpile(circ, backend=simulator)
        res = simulator.run(circ).result()
        actual_vector = res.get_statevector().data

        expected_vector = [1/sqrt(2), 1/sqrt(2), 0, 0] if state_ind == 0 else [1/sqrt(2), -1/sqrt(2), 0, 0]

        if actual_vector != approx(expected_vector):
            print("Expected state vector:")
            print(expected_vector)
            print("Actual state vector:")
            print(actual_vector)
            raise ValueError("State vectors should be equal")


def test_3_superdense_coding():
    # Loop over the 4 possible messages
    for message in range(4):
        # Construct the circuit
        qr = QuantumRegister(2)
        cr = ClassicalRegister(2)
        circ = QuantumCircuit(qr, cr)

        # Initialize the entangled pair
        circ.initialize([0, 1/sqrt(2), 1/sqrt(2), 0], qr)

        # Run the senders's part of the protocol
        # Encode the least significant bit in the relative phase
        if message % 2:
            circ.z(qr[0])
        # Encode the most significant bit in the basis state
        if message // 2:
            circ.x(qr[0])

        # Run the receiver's part of the protocol
        task_3_superdense_coding(circ, qr)

        # Measure
        circ.measure(qr, cr)

        circ = transpile(circ, backend=simulator)
        res_map = simulator.run(circ).result().get_counts()

        assert len(res_map) == 1, f"The protocol should produce deterministic results, and it produced {res_map}"
        res_int = int(list(res_map.keys())[0], 2)
        assert res_int == message, f"Expected message {message}, actual message {res_int}"
        


def test_4_teleportation():
    from random import uniform

    # Repeat the protocol on multiple test cases
    for _ in range(10):
        # Construct the circuit
        sender, receiver, message = QuantumRegister(1), QuantumRegister(1), QuantumRegister(1)
        sender_bits, receiver_bits = ClassicalRegister(2), ClassicalRegister(1)
        circ = QuantumCircuit(sender, receiver, message, sender_bits, receiver_bits)

        # Entangle sender and receiver in state |Ψ⁻⟩
        circ.h(sender)
        circ.cx(sender, receiver)
        circ.z(sender)
        circ.x(sender)

        # Prepare the message qubit in a random state
        angle = uniform(0.1, pi / 2 - 0.1)
        alpha, beta = cos(angle), sin(angle)
        circ.ry(2 * atan2(beta, alpha), message)

        # Perform sender's part of the protocol
        circ.cx(message, sender)
        circ.h(message)
        circ.measure(message, sender_bits[0])
        circ.measure(sender, sender_bits[1])

        # Call receiver's part of the protocol
        task_4_teleportation(circ, receiver, sender_bits)

        # "Unprepare" the receiver's qubit
        circ.ry(-2 * atan2(beta, alpha), receiver)

        # Measure the receiver's qubit - it should end up in the |0⟩ state
        circ.measure(receiver, receiver_bits)

        # Run the simulation
        res_counts = simulator.run(circ).result().get_counts()
        print(res_counts)
        for key, _ in res_counts.items():
            if key[0] != '0':
                raise ValueError(f"Unexpected measurement outcome: after unpreparation receiver's qubit should always end up in the |0⟩ state")


def test_5_gate_teleportation():
    from random import uniform

    # Repeat the protocol on multiple test cases
    for _ in range(10):
        # Construct the circuit
        sender, receiver, message = QuantumRegister(1), QuantumRegister(1), QuantumRegister(1)
        sender_bits, receiver_bits = ClassicalRegister(2), ClassicalRegister(1)
        circ = QuantumCircuit(sender, receiver, message, sender_bits, receiver_bits)

        # Entangle sender and receiver in state (H⊗I)|Φ⁺⟩
        circ.h(sender)
        circ.cx(sender, receiver)
        circ.h(receiver)

        # Prepare the message qubit in a random state
        angle = uniform(0.1, pi / 2 - 0.1)
        alpha, beta = cos(angle), sin(angle)
        circ.ry(2 * atan2(beta, alpha), message)

        # Perform sender's part of the protocol
        circ.cx(message, sender)
        circ.h(message)
        circ.measure(message, sender_bits[0])
        circ.measure(sender, sender_bits[1])

        # Call receiver's part of the protocol
        task_5_gate_teleportation(circ, receiver, sender_bits)

        # "Unprepare" the receiver's qubit
        circ.h(receiver)
        circ.ry(-2 * atan2(beta, alpha), receiver)

        # Measure the receiver's qubit - it should end up in the |0⟩ state
        circ.measure(receiver, receiver_bits)

        # Run the simulation
        res_counts = simulator.run(circ).result().get_counts()
        print(res_counts)
        for key, _ in res_counts.items():
            if key[0] != '0':
                raise ValueError(f"Unexpected measurement outcome: after unpreparation receiver's qubit should always end up in the |0⟩ state")

