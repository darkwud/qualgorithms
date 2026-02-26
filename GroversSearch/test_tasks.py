from functools import partial
from os import makedirs
from random import randint
from psiqworkbench import QPU, Qubits
from psiqworkbench.filter_presets import BIT_DEFAULT
from psiqworkbench.ops.qpu_ops import *
from .tasks_Module6_GroversSearch import *


def get_filtered_instructions_cpp(n_inputs: int, n_qubits: int, quantum_op, filename = None):
    '''Runs solution on a QPU and fetches the list of gate instructions produced for later replay.'''
    qpu = QPU(num_qubits=n_qubits, filters=BIT_DEFAULT)
    x = Qubits(n_inputs, "x", qpu)
    y = Qubits(1, "y", qpu)
    quantum_op(x, y)

    # Draw the circuit - only the logic applied by the solution itself (won't change between runs)
    if filename is not None:
        makedirs("out", exist_ok=True)
        qpu.draw(f"./out/{filename}.svg", show_qubricks=True)

    # Check that there are no leftover auxiliary qubits - only x and y
    num_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    if num_qubits != n_inputs + 1:
        raise Exception("Your solution should release all auxiliary qubits it allocates")

    instructions = qpu.get_instructions(format="cpp")
    # The first three instructions
    # are going to be reset and qubit allocations - skip them
    return instructions[3:]


def check_op_types(instructions):
    for instr in instructions:
        if type(instr) is QPU_op_read:
            raise Exception("Your solution should not use measurements")
        if type(instr) is QPU_op_write:
            raise Exception("Your solution should not use write operation")
        if type(instr) is QPU_op and instr.opcode != OP_qc_x:
            raise Exception("Your solution should not use gates other than X and controlled X")


def run_test_reversible(n_inputs: int, n_qubits: int, quantum_op, f, filename = None):
    # The solution is a sequence of reversible gates that doesn't depend on the inputs - can run it just once and replay later
    filtered_instructions = get_filtered_instructions_cpp(n_inputs, n_qubits, quantum_op, filename)

    # Check that the solution doesn't use prohibited op types
    check_op_types(filtered_instructions)

    qpu = QPU(filters=BIT_DEFAULT)
    # Turn on checking that released qubits are uncomputed
    qpu.enable_qubit_allocation_debugging()
    bit_sim = qpu.get_filter_by_name('>>bit-sim>>')
    for input in range(2 ** n_inputs):
        qpu.reset(n_qubits)
        x = Qubits(n_inputs, "x", qpu)
        y = Qubits(1, "y", qpu)

        # Prepare quantum input
        x.write(input)
        # Run the reversible computation as filtered instructions
        qpu.flush()
        bit_sim._put_native(filtered_instructions)

        # Convert integer input to a Boolean array
        input_str = (f"{{:0>{n_inputs}b}}").format(input)
        input_le = [input_str[i] == '1' for i in range(n_inputs)][::-1]

        # Evaluate classical function on the classical input
        res_expected = int(f(input_le))

        # Compare the results of classical and quantum computations
        qpu.label("Read")
        res_x = x.read()
        res_y = y.read()

        # Show bit string input in little endian (LSB first) to match qubit state
        if res_x != input:
            raise Exception(f"Error for x={input} ({input_str[::-1]}): the state of the input qubits changed")
        if res_y != res_expected:
            raise Exception(f"Error for x={input} ({input_str[::-1]}): expected {res_expected}, got {res_y}")


############################################################
def f_sum_of_bits(args: list[bool], s: int):
    return args.count(True) == s


def test_1_sum_of_bits():
    for n in range(2, 7):
        for s in range(n):
            print(f"Testing {n=}, {s=}")
            f = partial(f_sum_of_bits, s=s)
            quantum_op = partial(task_1_sum_of_bits, s=s)
            run_test_reversible(n, 3 * n + 1, quantum_op, f, "task_1_sum_of_bits")


############################################################
def f_row_constraints(args: list[bool], row_constr: list[int]):
    R = len(row_constr)
    C = len(args) // R
    for row in range(R):
        sum = 0
        for col in range(C):
            sum += args[row * C + col]
        if sum != row_constr[row]:
            return False
    return True


def test_2_row_constraints():
    for R in range(1, 4):
        for C in range(2, 4):
            for _ in range(3):
                row_constr = [randint(0, C) for _ in range(R)]
                print(f"Testing {R=}, {C=}, {row_constr=}")
                f = partial(f_row_constraints, row_constr=row_constr)
                quantum_op = partial(task_2_row_constraints, row_constr=row_constr)
                run_test_reversible(R * C, 2 * R * C + 2 * (R + C) + 1, quantum_op, f, "task_2_row_constraints")


############################################################
def f_col_constraints(args: list[bool], col_constr: list[int]):
    C = len(col_constr)
    R = len(args) // C
    for col in range(C):
        sum = 0
        for row in range(R):
            sum += args[row * C + col]
        if sum != col_constr[col]:
            return False
    return True


def test_3_col_constraints():
    for R in range(1, 4):
        for C in range(2, 4):
            for _ in range(3):
                col_constr = [randint(0, R) for _ in range(C)]
                print(f"Testing {R=}, {C=}, {col_constr=}")
                f = partial(f_col_constraints, col_constr=col_constr)
                quantum_op = partial(task_3_col_constraints, col_constr=col_constr)
                run_test_reversible(R * C, 2 * R * C + 2 * (R + C) + 1, quantum_op, f, "task_3_col_constraints")


############################################################
def f_kakuro_puzzle(args: list[bool], row_constr: list[int], col_constr: list[int]):
    return f_row_constraints(args, row_constr) and f_col_constraints(args, col_constr)


def test_4_kakuro_puzzle():
    for R in range(2, 4):
        for C in range(2, 4):
            for _ in range(3):
                # Generate a random puzzle and get constraints from it rather than generate constraints randomly
                puzzle = [[randint(0, 1) for _ in range(C)] for _ in range(R)]
                row_constr = [puzzle[r].count(1) for r in range(R)]
                col_constr = [sum([puzzle[r][c] for r in range(R)]) for c in range(C)]
                print(f"Testing {R=}, {C=}, {row_constr=}, {col_constr=}")
                f = partial(f_kakuro_puzzle, row_constr=row_constr, col_constr=col_constr)
                quantum_op = partial(task_4_kakuro_puzzle, row_constr=row_constr, col_constr=col_constr)
                run_test_reversible(R * C, R * C + R + C + max(R, C) + 3, quantum_op, f, "task_4_kakuro_puzzle")


############################################################
def get_task_7_av():
    # Run resource estimation on one particular test case
    qpu = QPU(num_qubits=100, filters=BIT_DEFAULT)
    R = C = 8
    row_constr = col_constr = [1, 2] * 4
    x = Qubits(R * C, "x", qpu)
    y = Qubits(1, "y", qpu)
    task_4_kakuro_puzzle(x, y, row_constr, col_constr)

    # Get active volume
    return qpu.metrics()["active_volume"]


def test_7_1pt():
    av = get_task_7_av()
    assert av >= 150000 and av < 220000


def test_7_2pt():
    av = get_task_7_av()
    assert av < 150000