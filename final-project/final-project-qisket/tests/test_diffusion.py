from qiskit.quantum_info import Statevector
from Final_Project.diffusion import diffusion_operator
import numpy as np
import pytest

# We select these specific 'n' values to stress-test every branch of our logic:
# n=1: Tests the special 'if n == 1' logic (Z-gate fix for MCX error).
# n=2: Tests the smallest multi-qubit case (often uses a simple CZ gate).
# n=3: Tests a standard 'odd' number of qubits for symmetry.
# n=5: Tests that the Multi-Controlled X (MCX) scales to larger registers.
@pytest.mark.parametrize("n", [1, 2, 3, 5])

def test_diffusion_properties(n):
    """
    Tests two core properties of the Diffusion operator:
    1. Invariance: The uniform superposition |s> should stay |s> (up to a sign).
    2. Reflection: It should reflect amplitudes about the mean.
    """
    diff = diffusion_operator(n)
    N = 2**n
    
    # --- Test 1: Invariance of Uniform Superposition ---
    s_vector = Statevector.from_label('+' * n)
    evolved_s = s_vector.evolve(diff)
    
    # We check absolute values because of potential global phase (-1)
    assert np.allclose(np.abs(evolved_s.data), np.abs(s_vector.data)), \
        f"Uniform state not preserved for n={n}"

    # --- Test 2: Reflection about the Mean ---
    # Prepare a state where only the first amplitude is 1.0, others are 0.0
    # The mean (average) is 1/N.
    # Formula for reflection: New_Amp = 2*(Mean) - Old_Amp
    initial_data = np.zeros(N)
    initial_data[0] = 1.0
    psi = Statevector(initial_data)
    
    evolved_psi = psi.evolve(diff)
    
    mean = 1.0 / N
    expected_amp_0 = 2 * mean - 1.0
    expected_amp_others = 2 * mean - 0.0
    
    # Again, check absolute values or account for the global phase
    actual_data = evolved_psi.data
    
    # If the first amplitude was 1 and the rest 0, 
    # the new amplitudes should all be the same (except possibly the first)
    # or follow the 2*mean - amp rule perfectly.
    assert np.allclose(np.abs(actual_data[0]), np.abs(expected_amp_0)), \
        f"Reflection failed for index 0 at n={n}"
    if n > 1:
        assert np.allclose(np.abs(actual_data[1]), np.abs(expected_amp_others)), \
            f"Reflection failed for other indices at n={n}"