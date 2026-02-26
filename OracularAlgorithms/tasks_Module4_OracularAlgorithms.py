from qiskit import QuantumCircuit, QuantumRegister

# In all tasks in this assignment, use only primitive gates and measurements.
# Don't use libraries such as QuantumCircuit.initialize.

# Task 1. Phase oracles for Deutsch algorithm 
# Inputs:
#      1) A quantum circuit.
#      2) A qubit in an arbitrary state, represented as `QuantumRegister` of length 1.
#      3) An integer F which defines which function to implement:
#         F = 0 : f(x) = 0
#         F = 1 : f(x) = 1
#         F = 2 : f(x) = x
#         F = 3 : f(x) = 1 - x
# Goal: Implement a unitary phase oracle that transforms each basis state |x⟩ into state (-1)^f(x) |x⟩.
def task_1_singlequbit_oracles(circ: QuantumCircuit, q: QuantumRegister, F: int) -> None:

    # f(x) = 0 i.e. identity matrix
    # no gate 
    if F == 0:
        pass

    # f(x) = 1 i.e. -I matrix
    elif F == 1:
        circ.x(q[0])
        circ.z(q[0])
        circ.x(q[0])
        circ.z(q[0])

    # f(x) = x i.e. requires Z matrix [[1,0], [0,1]]
    elif F == 2:
        circ.z(q[0])

    # f(x) = 1 - x
    elif F == 3:
        circ.x(q[0])
        circ.z(q[0])
        circ.x(q[0])

# Task 2. Inequality phase oracle 
# Inputs:
#      1) A quantum circuit.
#      2) Two qubits in an arbitrary state, represented as `QuantumRegister` of length 2.
# Goal: Implement a unitary phase oracle that transforms each basis state |x₀x₁⟩ into state (-1)^f(x₀, x₁) |x₀x₁⟩,
#       where f(x₀, x₁) = 1 if x₀ ≠ x₁ and 0 otherwise.
def task_2_inequality_oracle(circ: QuantumCircuit, qr: QuantumRegister) -> None:
    
    
    circ.cx(qr[0], qr[1])   # q1 = q0 XOR q1
    circ.z(qr[1])           # flip phase if q1 = 1
    circ.cx(qr[0], qr[1])   # revert back

# Task 3. Phase oracle for Bernstein-Vazirani algorithm 
# Inputs:
#      1) A quantum circuit.
#      2) N ≥ 2 qubits in an arbitrary state, represented as `QuantumRegister` of length N.
#      3) A bit vector of length N represented as a list[int], each element being 0 or 1.
# Goal: Implement a unitary that transforms each basis state |x₀x₁...xₙ₋₁⟩ into state (-1)^f(x₀, x₁, ..., xₙ₋₁) |x₀x₁...xₙ₋₁⟩,
#       where f(x₀, x₁, ..., xₙ₋₁) = Σᵢ sᵢ xᵢ modulo 2 
#       (i.e., the function implemented by the oracle used in Bernstein-Vazirani algorithm).
def task_3_bv_oracle(circ: QuantumCircuit, qr: QuantumRegister, s: list[int]) -> None:
    
    for i in range(len(s)):
        if s[i] == 1:
            circ.z(qr[i])
            
# Task 4. "Is number divisible by 4" phase oracle 
# Inputs:
#      1) A quantum circuit.
#      2) N ≥ 3 qubits in an arbitrary state, represented as `QuantumRegister` of length N.
# Goal: Implement a unitary that transforms each basis state |x₀x₁...xₙ₋₁⟩ into state (-1)^f(x₀, x₁, ..., xₙ₋₁) |x₀x₁...xₙ₋₁⟩,
#       where f(x₀, x₁, ..., xₙ₋₁) = 1 if integer x is divisible by 4, and 0 otherwise.
#       Bit string x₀, x₁, ..., xₙ₋₁ can be converted to an integer x using little-endian notation:
#       x = xₙ₋₁ ⋅ 2ⁿ⁻¹ + xₙ₋₂ ⋅ 2ⁿ⁻² + ... + x₁ ⋅ 2 + x₀
def task_4_divisible_by_4_oracle(circ: QuantumCircuit, qr: QuantumRegister) -> None:

   # Convert |00⟩ → |11⟩
   circ.x(qr[0])
   circ.x(qr[1])
   
   # Apply CZ gate when both qubits are |1⟩
   circ.cz(qr[0], qr[1])

   # Restore original state
   circ.x(qr[0])
   circ.x(qr[1])  

# Task 5. "Does the bit string start with given prefix" phase oracle 
# Inputs:
#      1) A quantum circuit.
#      2) N ≥ 3 qubits in an arbitrary state, represented as `QuantumRegister` of length N.
#      3) A bit vector of length K represented as a list[int], each element being 0 or 1 (2 ≤ K < N).
# Goal: Implement a unitary that transforms each basis state |x₀x₁...xₙ₋₁⟩ into state (-1)^f(x₀, x₁, ..., xₙ₋₁) |x₀x₁...xₙ₋₁⟩,
#       where f(x₀, x₁, ..., xₙ₋₁) = 1 if the prefix of x (the substring starting at position 0) of length K equals the given bit vector, 
#       and 0 otherwise.
# For example, for N = 4, K = 2, and bit vector s = [0, 1] the oracle should flip the phases of four basis states of the form |01**⟩.
def task_5_has_prefix(circ: QuantumCircuit, qr: QuantumRegister, s: list[int]) -> None:
    
    K = len(s)

    # Apply X when s[i] = 0
    for i in range(K):
        if s[i] == 0:
            circ.x(qr[i])
    
    # Apply multi-controlled Z on qubits 0 to K-1
    if K == 2:
        # Special case for cz
        circ.cz(qr[0], qr[1])
    else:
        # Case for MCZ
        controls = [qr[i] for i in range (K - 1)]
        target = qr[K - 1]

        # Target qr[K - 1]
        circ.h(target)
        circ.mcx(controls, target)
        circ.h(target)

    for i in range(K):
        if s[i] == 0:
            circ.x(qr[i])

# Task 6. "Is the bit string a palindrome" phase oracle 
# Inputs:
#      1) A quantum circuit.
#      2) N ≥ 2 qubits in an arbitrary state, represented as `QuantumRegister` of length N.
# Goal: Implement a unitary that transforms each basis state |x₀x₁...xₙ₋₁⟩ into state (-1)^f(x₀, x₁, ..., xₙ₋₁) |x₀x₁...xₙ₋₁⟩,
#       where f(x₀, x₁, ..., xₙ₋₁) = 1 if the bit string x is a palindrome, and 0 otherwise.
#       A bit string is a palindrome if it equals its reverse, or, in other words, its first bit equals its last bit, 
#       its second bit equals its second-to-last bit, and so on.
# For example, for N = 2 the oracle should flip the phases of states |00⟩ and |11⟩.
# For N = 3, the oracle should flip the phases of states |000⟩, |010⟩, |101⟩, and |111⟩.
# Hint: you might find reversible computing techniques from the next module helpful in this task.
def task_6_palindrome(circ: QuantumCircuit, qr: QuantumRegister) -> None:
  
    N = len(qr)
    num_pairs = N // 2

    # Compute XOR on each right side register pair
    for i in range(num_pairs):
        circ.cx(qr[i], qr[N - 1 - i])

    # Compute Phase -1 when XOR == 0
    xor_qubits = [qr[N - 1 - i] for i in range(num_pairs)]

    # Compute zeros to ones
    for q in xor_qubits:
        circ.x(q)

    # Multi-controlled Z
    if num_pairs == 1:
        circ.z(xor_qubits[0])
    elif num_pairs == 2:
        circ.cz(xor_qubits[0], xor_qubits[1])
    else:
        # MCZ = H on target
        controls = xor_qubits[:-1]
        target = xor_qubits[-1]
        circ.h(target)
        circ.mcx(controls, target)
        circ.h(target)

    # Uncompute X gate
    for q in xor_qubits:
        circ.x(q)

    # Uncompute XORs
    for i in range(num_pairs - 1, -1, -1):
        circ.cx(qr[i], qr[N - 1 - i])
