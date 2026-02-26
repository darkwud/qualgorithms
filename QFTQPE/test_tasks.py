from cmath import exp, pi, sqrt, cos
from functools import partial
from random import random
from psiqworkbench import QPU, Qubits, Units
from psiqworkbench.qubricks import QFT
from pytest import approx
from .tasks_Module7_QFTQPE import *


def get_filtered_instructions(n_qubits: int, quantum_op):
    '''Runs solution on a QPU and fetches the list of gate instructions produced for later replay.'''
    qpu = QPU(num_qubits=n_qubits)
    reg = Qubits(n_qubits, "reg", qpu)
    quantum_op(reg)

    # Check that there are no leftover auxiliary qubits - only x and y
    num_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    if num_qubits != n_qubits:
        raise Exception("Your solution should release all auxiliary qubits it allocates")

    instructions = qpu.get_instructions()
    # The first two instructions
    # are going to be reset and qubit allocation - skip them
    return instructions[2:]


def run_qft_stateprep_test(solution, n, expected_state):
    qpu = QPU(num_qubits=n)
    reg = Qubits(n, "reg", qpu)
    # Prepare the state asked for by the task
    qpu.label("Solution")
    filtered_instructions = get_filtered_instructions(n, solution)
    qpu.put_instructions(filtered_instructions)
    # Apply QFT to transform it into the final state
    qpu.label("QFT")
    qft = QFT()
    qft.compute(reg)

    # Uncomment this line to draw the circuit
    # qpu.draw("qft_stateprep.svg")
    
    state = qpu.pull_state()
    print("Actual state:")
    print(state)
    print("Expected state:")
    print(expected_state)
    assert state == approx(expected_state)


############################################################
def test_1_periodic_state_prep():
    for n in range(2, 10):
        N = 2 ** n
        expected_state = [exp(2 * pi * 1j * k / N) / sqrt(N) for k in range(N)]
        run_qft_stateprep_test(task_1_periodic_state_prep, n, expected_state)


############################################################
def test_2_odd_superposition_prep():
    for n in range(2, 10):
        expected_state = [1 / sqrt(2 ** (n - 1)) if k % 2 == 1 else 0 for k in range(2 ** n)]
        run_qft_stateprep_test(task_2_odd_superposition_prep, n, expected_state)


############################################################
def test_3_cosines_prep():
    for n in range(2, 10):
        N = 2 ** n
        expected_state = [cos(2 * pi * k / N) / sqrt(2 ** (n - 1)) for k in range(N)]
        run_qft_stateprep_test(task_3_cosines_prep, n, expected_state)


############################################################
def run_eigenstate_prep_test(solution, n, matrix, eigenvalue):
    qpu = QPU(num_qubits=n)
    reg = Qubits(n, "reg", qpu)
    # Prepare the eigenstate
    filtered_instructions = get_filtered_instructions(n, partial(solution, eigenvalue=eigenvalue))
    qpu.put_instructions(filtered_instructions)

    # Get the resulting state
    state = qpu.pull_state()
    # Multiply it by the matrix of the gate
    applied_state = [sum(matrix[i][j] * state[j] for j in range(len(state))) for i in range(len(matrix))]
    # Multiply it by the eigenvalue
    expected_state = [state[j] * eigenvalue for j in range(len(state))]
    print(f"State prepared for eigenvalue {eigenvalue}:")
    print(state)
    print("Result of applying the gate to the prepared state:")
    print(applied_state)
    print("Expected result:")
    print(expected_state)
    # The resulting states should be the same (by definition of eigenstate)
    assert applied_state == approx(expected_state)


############################################################
def test_4_single_qubit_eigenstate():
    matrix = [[0.6, 0.8], 
              [0.8, -0.6]]
    for eigenvalue in [+1, -1]:
        run_eigenstate_prep_test(task_4_single_qubit_eigenstate, 1, matrix, eigenvalue)


############################################################
def test_5_two_qubit_eigenstate():
    matrix = [[1,  0,  0,  0],
              [0,  0, 1j,  0],
              [0, 1j,  0,  0],
              [0,  0,  0,  -1]]
    for eigenvalue in [+1, -1, +1j, -1j]:
        run_eigenstate_prep_test(task_5_two_qubit_eigenstate, 2, matrix, eigenvalue)


############################################################
def three_bit_adaptive_phase_estimation(eigenphase):
    qpu = QPU(num_qubits=2)
    phase = Qubits(1, "phase", qpu)
    eigenstate = Qubits(1, "eigenstate", qpu)

    # Use a fixed unitary-eigenstate pair: eigenstate = |0⟩, 
    # unitary = Rz with the specific rotation angle
    angle = -4 * pi * eigenphase * Units.rad

    res = ""

    # Estimate the least significant bit θ₃
    qpu.label("Estimate least significant bit")
    phase.had()
    for _ in range(4):
        eigenstate.rz(angle, cond=phase)
    phase.had()

    if phase.read() == 1:
        res = "1" + res
        phase.x()
    else:
        res = "0" + res

    # Estimate the middle bit θ₂
    qpu.label("Estimate middle bit")
    phase.had()
    for _ in range(2):
        eigenstate.rz(angle, cond=phase)
    # Adjust phase for the value of θ₃
    if res[-1] == "1":
        phase.s_inv()
    phase.had()

    if phase.read() == 1:
        res = "1" + res
        phase.x()
    else:
        res = "0" + res

    # Estimate the most significant bit θ₁
    qpu.label("Start estimating MSB")
    phase.had()
    eigenstate.rz(angle, cond=phase)
    # Adjust phase for the values of θ₂ and θ₃
    solution = partial(task_6_adaptive_phase_estimation, theta2=int(res[0]), theta3=int(res[1]))
    filtered_instructions = get_filtered_instructions(1, solution)
    qpu.label("Solution")
    qpu.put_instructions(filtered_instructions)

    qpu.label("Read")
    if phase.read() == 1:
        res = "1" + res
    else:
        res = "0" + res

    # Uncomment this line to draw the circuit
    # qpu.draw("adaptive_phase_estimation.svg")

    return int(res, base=2)


############################################################
def test_6_adaptive_phase_estimation():
    shots = 100
    for theta_int in range(8):
        theta = theta_int / 8
        estimates = [0] * 8
        for _ in range(shots):
            est = three_bit_adaptive_phase_estimation(theta)
            estimates[est] += 1
        assert estimates[theta_int] == shots, f"Actual phase {theta_int} / 8, estimated phases distribution: {estimates}"


############################################################
def eight_bit_quantum_phase_estimation_state(unitary, stateprep):
    phase_bits = 8

    qpu = QPU(num_qubits=9)
    phase = Qubits(phase_bits, "phase", qpu)
    eigenstate = Qubits(1, "eigenstate", qpu)

    phase.had()
    stateprep(eigenstate)

    # phase uses little endian encoding
    for k in range(phase_bits):
        for _ in range(2 ** k):
            unitary(eigenstate, cond=phase[k])

    qft = QFT()
    qft.compute(phase, dagger=True)

    # Don't measure, instead return the entire state vector for analysis
    return phase.pull_state()


############################################################
def test_7_reverse_engineer_qpe():
    for _ in range(10):
        phase = random()
        unitary, stateprep = task_7_reverse_engineer_qpe(phase)
        phase_est_state = eight_bit_quantum_phase_estimation_state(unitary, stateprep)
        # At this point, we want to have all possible readouts be within 0.01 from the correct answer.
        # So any basis states outside of the range should have near-0 amplitude (and probability).
        for ind in range(len(phase_est_state)):
            if abs(phase_est_state[ind]) > 1e-6:
                phase_est = ind / 2 ** 8
                assert phase_est == approx(phase, abs=0.01), f"Actual phase {phase}, possible estimated phase {phase_est}"
