from functools import partial
from os import makedirs
from random import randint
from psiqworkbench import QPU, Qubits
from psiqworkbench.filter_presets import BIT_DEFAULT
from psiqworkbench.ops.qpu_ops import *
from pytest import approx
from .tasks_Module5_ReversibleComputing import *


def get_filtered_instructions(n_inputs: int, n_qubits: int, quantum_op):
    '''Runs solution on a QPU and fetches the list of gate instructions produced for later replay.'''
    qpu = QPU(num_qubits=n_qubits, filters=BIT_DEFAULT)
    x = Qubits(n_inputs, "x", qpu)
    y = Qubits(1, "y", qpu)
    quantum_op(x, y)

    # Check that there are no leftover auxiliary qubits - only x and y
    num_qubits = qpu._get_qubit_heap().allocated_mask.bit_count()
    if num_qubits != n_inputs + 1:
        raise Exception("Your solution should release all auxiliary qubits it allocates")

    instructions = qpu.get_instructions()
    # The first three instructions
    # are going to be reset and qubit allocations - skip them
    return instructions[3:]


def check_op_types(instructions):
    for instr in instructions:
        if type(instr) is QPU_op_read:
            raise Exception("Your solution should not use measurements")
        if type(instr) is QPU_op_write:
            raise Exception("Your solution should not use write operation")
        if type(instr) is QPU_op and instr.opcode not in (OP_qc_x, OP_qc_lelbow, OP_qc_relbow):
            raise Exception("Your solution should not use gates other than X, controlled X, and Gidney elbows")


def run_test_reversible(n_inputs: int, n_qubits: int, quantum_op, f, filename = None):
    # The solution is a sequence of reversible gates that doesn't depend on the inputs - can run it just once and replay later
    filtered_instructions = get_filtered_instructions(n_inputs, n_qubits, quantum_op)

    # Check that the solution doesn't use prohibited op types
    check_op_types(filtered_instructions)

    qpu = QPU(filters=BIT_DEFAULT)
    qpu.enable_qubit_allocation_debugging()
    for input in range(2 ** n_inputs):
        qpu.reset(n_qubits)
        x = Qubits(n_inputs, "x", qpu)
        y = Qubits(1, "y", qpu)

        # Prepare quantum input
        x.write(input)
        # Run the reversible computation as filtered instructions
        qpu.label("Solution")
        qpu.put_instructions(filtered_instructions)

        # Convert integer input to a Boolean array
        input_str = (f"{{:0>{n_inputs}b}}").format(input)
        input_le = [input_str[i] == '1' for i in range(n_inputs)][::-1]

        # Evaluate classical function on the classical input
        res_expected = int(f(input_le))

        # Compare the results of classical and quantum computations
        qpu.label("Read")
        res_x = x.read()
        res_y = y.read()

        # Draw the circuit - only on the first run (won't change between runs)
        # Modify this logic or file name in the function call if you want to keep multiple circuits per test
        if input == 0 and filename is not None:
            makedirs("out", exist_ok=True)
            qpu.draw(f"./out/{filename}.svg")

        # Show bit string input in little endian (LSB first) to match qubit state
        if res_x != input:
            raise Exception(f"Error for x={input} ({input_str[::-1]}): the state of the input qubits changed")
        if res_y != res_expected:
            raise Exception(f"Error for x={input} ({input_str[::-1]}): expected {res_expected}, got {res_y}")


############################################################
def f_nand(args: list[bool]):
    return not (args[0] and args[1])


def test_1_nand_gate():
    run_test_reversible(2, 3, task_1_nand_gate, f_nand, "task_1_nand_gate")


############################################################
def test_2_peres_gate():
    qpu = QPU(num_qubits=3, filters=['>>buffer>>', '>>unitary>>'])
    x = Qubits(3, "reg", qpu)
    # Explicitly apply an identity gate to each qubit
    # to make Workbench return a matrix of the right size even when the solution is empty.
    x.identity()
    task_2_peres_gate(x)

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    actual = ufilter.get()
    print("Unitary implemented by your solution:")
    print(actual)

    expected = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0]
    ]

    for a, e in zip(actual, expected):
        assert a == approx(e)


############################################################
def f_fixed_pattern(args: list[bool]):
    for ind in range(len(args)):
        if args[ind] != (ind % 3 > 0):
            return False
    return True


def test_3_fixed_pattern():
    for n in range(2, 7):
        run_test_reversible(n, n + 1, task_3_fixed_pattern, f_fixed_pattern, f"task_3_fixed_pattern")


############################################################
def f_flipped_halves(args: list[bool]):
    K = len(args) // 2
    for ind in range(K):
        if args[ind] == args[ind + K]:
            return False
    return True


def test_4_flipped_halves():
    for k in range(1, 5):
        run_test_reversible(2 * k, 2 * k + 1, task_4_flipped_halves, f_flipped_halves, f"task_4_flipped_halves")


############################################################
def f_no_three_bits(args: list[bool]):
    for ind in range(len(args) - 2):
        if args[ind] == args[ind + 1] and args[ind] == args[ind + 2]:
            return False
    return True


def test_5_no_three_bits():
    for n in range(3, 8):
        run_test_reversible(n, 2 * n - 1, task_5_no_three_bits, f_no_three_bits, f"task_5_no_three_bits")


############################################################
def f_regexp_match(args: list[bool], pattern: list[int]):
    for ind in range(len(pattern)):
        if pattern[ind] != -1 and args[ind] != (pattern[ind] == 1):
            return False
    return True


def test_6_regexp_match():
    tests = [
        [0], 
        [1], 
        [-1], 
        [0, 1], 
        [0, -1, 1], 
        [-1, -1, -1, -1], 
        [0, 1, -1, 0], 
        [-1, 1, -1, 0, -1], 
        [1, 1, 1, 0, 0, 0]
    ]
    # Add random tests
    for _ in range(10):
        n = randint(4, 6)
        pattern = [randint(-1, 1) for _ in range(n)]
        tests.append(pattern)

    for pattern in tests:
        print(f"Testing {pattern=}")
        n = len(pattern)
        f = partial(f_regexp_match, pattern=pattern)
        quantum_op = partial(task_6_regexp_match, pattern=pattern)
        run_test_reversible(n, n + 1, quantum_op, f, f"task_6_regexp_match")
