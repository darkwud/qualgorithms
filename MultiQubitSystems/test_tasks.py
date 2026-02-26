from math import sqrt
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
from pytest import approx
from .tasks_Module2_MultiQubitSystems import *

# Create the simulator instance to add save_statevector method to QuantumCircuit
simulator = AerSimulator(method='statevector')

def check_state_vector(
    solution,        # Callable that is being tested
    n_qubits,        # Number of qubits in the register
    expected_vector  # State vector it should prepare
) -> None:
    # Construct the circuit that has the callable as a part of it
    qr = QuantumRegister(n_qubits)
    circ = QuantumCircuit(qr)
    solution(circ, qr)

    # Save the state vector
    circ.save_statevector()

    # Run the simulation and get the results
    circ = transpile(circ, backend=simulator)
    res = simulator.run(circ).result()
    # Extract the saved state vector
    actual_vector = res.get_statevector().data

    if actual_vector != approx(expected_vector):
        print("Expected state vector:")
        print(expected_vector)
        print("Actual state vector:")
        print(actual_vector)
        raise ValueError("State vectors should be equal")


def test_1_prepare_state():
    expected_vector = [0.5, -0.5, -0.5, 0.5]
    check_state_vector(task_1_prepare_state, 2, expected_vector)


def test_2_prepare_state():
    expected_vector = [0.5, -0.5, 0.5, 0.5]
    check_state_vector(task_2_prepare_state, 2, expected_vector)


def test_3_prepare_state():
    for n in range(2, 11):
        expected_vector = [0] * (2 ** n)
        ind1 = int(('0011' * 4)[:n][::-1], 2)
        ind2 = int(('1100' * 4)[:n][::-1], 2)
        expected_vector[ind1] = expected_vector[ind2] = 1 / sqrt(2)
        check_state_vector(task_3_prepare_state, n, expected_vector)


def test_4_prepare_state():
    for n in range(2, 11, 2):
        expected_vector = [0] * (2 ** n)
        for ind in range(0, 2 ** (n // 2)):
            strind = ''
            for _ in range(n // 2):
                strind += str(ind % 2) * 2
                ind //= 2
            expected_vector[int(strind, 2)] = 1 / (sqrt(2) ** (n // 2))    
        check_state_vector(task_4_prepare_state, n, expected_vector)


def print_matrix(matrix):
    for row in matrix:
        print(row)


def test_5_signed_swap():
    # Construct the circuit that has the callable as a part of it
    q = QuantumRegister(2)
    circ = QuantumCircuit(q)
    task_5_signed_swap(circ, q)
    # Convert the circuit to a matrix
    op = Operator(circ)
    actual_matrix = op.data

    expected_matrix = [[1, 0, 0, 0],
                       [0, 0, -1, 0],
                       [0, -1, 0, 0],
                       [0, 0, 0, 1]]

    # Check that the actual matrix matches the expected one
    for actual, expected in zip(actual_matrix, expected_matrix):
        if actual != approx(expected):
            print("Expected matrix:")
            print_matrix(expected_matrix)
            print("Actual matrix:")
            print_matrix(actual_matrix)
            raise ValueError("Operation matrices should be equal")


def check_distinguish_states(
    n_qubits,    # Number of qubits in the register
    n_states,    # Number of different states
    state_names, # Readable names of the states
    state_amps,  # Amplitudes of each state
    sol_circuit, # Measurement circuit
    sol_decoder  # Classical logic of decoding measurement results
):
    for ind in range(n_states):
        # print(f"Running experiments on state {state_names[ind]}...")
        qr = QuantumRegister(n_qubits)
        cr = ClassicalRegister(n_qubits)
        circ = QuantumCircuit(qr, cr)

        # Prepare the state number ind
        circ.initialize(state_amps[ind], qr, normalize=True)

        try:
            # Apply the solution circuit
            sol_circuit(circ, qr, cr)

            # Run the simulation
            circ = transpile(circ, backend=simulator)
            res_counts = simulator.run(circ).result().get_counts()

            # Interpret the results
            # Use decoder for each of the measurement outcomes - all must give correct result
            for res_bitstring in res_counts.keys():
                res_ind = sol_decoder(res_bitstring)
                if res_ind != ind:
                    raise ValueError(f"Unexpected measurement decoding: raw measurement {res_bitstring}, expected {ind}, got {res_ind}")
        except Exception as e:
            raise Exception(f"Testing on state {state_names[ind]}: {e}")


def test_6_two_threequbit_states():
    amps = [[0, 0.5, 0, 0.5, 0.5, 0, 0.5, 0],
            [0.5, 0, 0.5, 0, 0, 0.5, 0, 0.5]]
    check_distinguish_states(3, 2, ["(|000⟩ + |001⟩ + |010⟩ + |100⟩) / 2", 
                                    "(|110⟩ + |101⟩ + |011⟩ + |111⟩) / 2"], 
                             amps, task_6_measure_two_threequbit_states_circuit, task_6_measure_two_threequbit_states_decoder)


def test_7_four_threequbit_states():
    amps = [[1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, -1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, -1, 0, 0, 0, 0, 1, 0]]
    check_distinguish_states(3, 4, ["(|000⟩ + |111⟩) / sqrt(2)", 
                                    "(|000⟩ - |111⟩) / sqrt(2)", 
                                    "(|011⟩ + |100⟩) / sqrt(2)", 
                                    "(|011⟩ - |100⟩) / sqrt(2)"], 
                             amps, task_7_measure_four_threequbit_states_circuit, task_7_measure_four_threequbit_states_decoder)


def test_8_four_twoqubit_states():
    amps = [[1,  3,  2,  6], 
            [3, -1,  6, -2],
            [2,  6, -1, -3],
            [6, -2, -3,  1]]
    check_distinguish_states(2, 4, ["1|00⟩ + 3|10⟩ + 2|01⟩ + 6|11⟩", 
                                    "3|00⟩ - 1|10⟩ + 6|01⟩ - 2|11⟩", 
                                    "2|00⟩ + 6|10⟩ - 1|01⟩ - 3|11⟩", 
                                    "6|00⟩ - 2|10⟩ - 3|01⟩ + 1|11⟩"], 
                             amps, task_8_measure_four_twoqubit_states_circuit, task_8_measure_four_twoqubit_states_decoder)
