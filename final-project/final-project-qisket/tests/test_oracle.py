import pytest
from itertools import product 
from qiskit.quantum_info import Statevector
from Final_Project.oracle import subset_sum_oracle


# Define our Test Library (Weights, Target, Expected Solutions)
TEST_CASES = [
    ([1, 2, 3], 3, [(0,0,1), (1,1,0)], "Standard Case"),
    ([1], 1, [(1,)], "Minimal n=1 Case"),
    ([1, 1], 2, [(1,1)], "Duplicate Weights"),
    ([5, 5, 5], 20, [], "Zero Solutions Case"),
    ([2, 4], 0, [(0,0)], "Target Zero (Empty Set) Case")
]

def get_amplitude_index(bits):
    """Qiskit uses little-endian: (1,0,0) is index 1, (0,1,0) is index 2."""
    return sum(b << i for i, b in enumerate(bits))

# Runs the test function 5 separate times, once for each case above.
@pytest.mark.parametrize("weights, target, valid_bits, label", TEST_CASES)

def test_oracle_scenarios(weights, target, valid_bits, label):
    """
    Encompassing test suite that verifies the phase-flip logic for the Oracle.
    
    A Phase Oracle should:
    1. Multiply the amplitude of 'Solution' states by -1 (Phase flip).
    2. Leave 'Non-solution' states exactly as they were (Positive phase).
    """
    n = len(weights)

    # Generate the Oracle circuit based on the current test case
    oracle = subset_sum_oracle(weights, target)
    
    # Iterate through every possible state in the 2^n search space
    for bits in product([0, 1], repeat=n):
        # Prepare a pure computational basis state |bits> 
        # We reverse the bits because Statevector.from_label reads left-to-right (MSB to LSB),
        # but our 'bits' tuple is indexed 0 to n-1 (LSB to MSB).
        sv = Statevector.from_label(''.join(map(str, bits[::-1]))) # Little-endian flip
        evolved_sv = sv.evolve(oracle)
        
        index = get_amplitude_index(bits)
        amplitude = evolved_sv.data[index]
        
        if bits in valid_bits:
            # Solution states MUST have a negative amplitude (phase flip)
            assert amplitude < 0, f"Failed {label}: Bitstring {bits} should be flipped"
        else:
            # Non-solution states MUST stay positive
            assert amplitude > 0, f"Failed {label}: Bitstring {bits} should NOT be flipped"