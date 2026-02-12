# Debugging BB84 Key Distribution Protocol
# In the class, you have learned about the BB84 protocol for securely generating random bitstrings, which can then be used to encrypt information to securely share it between parties.
# In this assignment you are going to look at the Qiskit implementation of this protocol and find 2 bugs in it.

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from random import randint

def sender_quantum(circ: QuantumCircuit, qr: QuantumRegister) -> tuple[list[int], list[int]]:
    '''The sender side of BB84 protocol.
    
    This function prepares each of the qubits in the input array in one of the |0⟩, |1⟩, |+⟩, or |-⟩ states randomly.
    Additionally, it returns a tuple of two arrays, an array of the chosen bases (X or Z) and an array of the encoded bits (0 or 1).
    Remember that |0⟩ and |1⟩ are the basis vectors in the Z basis and |+⟩ and |-⟩ are the basis vectors in the X basis.
    
    Returns:
        A tuple of two integer arrays. Each element of the first array indicates the basis chosen for preparation, 0 for Z, 1 for X.
        The corresponding element of the second array indicates whether the qubit was prepared as 0 or 1 in that basis.
    '''
    chosen_bases = []
    chosen_bits = []
    for ind in range(qr.size):
        # 0 - 0 in chosen basis, 1 - 1 in chosen basis
        chosen_bits.append(randint(0, 1))
        if chosen_bits[ind]:
            circ.x(qr[ind])

        # 0 - Z basis, 1 - X basis
        chosen_bases.append(randint(0, 1))
        if chosen_bases[ind]:
            circ.h(qr[ind])     # buggy 1

    # In the BB84 protocol, the sender will only communicate the bases to the receiver. 
    # In our implementation we're also returning the bits encoded to allow for protocol visualization.
    return chosen_bases, chosen_bits

def receiver_quantum(circ: QuantumCircuit, qr: QuantumRegister, cr: ClassicalRegister) -> tuple[list[int], list[int]]:
    '''The receiver side of BB84 protocol.

    This function measures each qubit in a randomly chosen basis, X or Z, and returns the chosen bases and the measurement results.

    Returns:
        A tuple of two integer arrays. Each element of the first array indicates the basis chosen for measurement, 0 for Z, 1 for X.
        The corresponding element of the second array indicates whether the qubit was measured as 0 or 1 in that basis.
    '''
    chosen_bases = []
    for ind in range(qr.size):
        chosen_bases.append(randint(0, 1))
        if chosen_bases[ind]:
            circ.h(qr[ind])
    circ.measure(qr, cr)
    
    # Perform the measurement
    simulator = AerSimulator(method='statevector')
    res = simulator.run(circ, shots=1).result().get_counts().keys()
    res_str = list(res)[0]

    measured_bits = [1 if m == '1' else 0 for m in reversed(res_str)] # buggy 2
    return chosen_bases, measured_bits

n = 20
qr = QuantumRegister(n)
cr = ClassicalRegister(n)
circ = QuantumCircuit(qr, cr)

bases_sender, bits_sender = sender_quantum(circ, qr)
bases_receiver, bits_receiver = receiver_quantum(circ, qr, cr)
# Now the sender and the receiver can both reconstruct the key!

# Print results
same = "|" 
basisSentChar = "|"
basisRecChar = "|"
bitSent = "|"
bitRec = "|"
key_sender = "|"
key_receiver = "|"
stateSent = "|"
for i in range(n):
    bitSent += f' {bits_sender[i]} |'
    bitRec += f' {bits_receiver[i]} |'
    same += f' {"y" if bases_receiver[i] == bases_sender[i] else "n"} |'
    key_sender += f' {bits_sender[i]} |' if bases_receiver[i] == bases_sender[i] else '   |'
    key_receiver += f' {bits_receiver[i]} |' if bases_receiver[i] == bases_sender[i] else '   |'
    basisRecChar += ' Z |' if bases_receiver[i] == 0 else ' X |'
    if bases_sender[i] == 0:
        stateSent += f'|{bits_sender[i]}>|'
        basisSentChar += ' Z |'
    else:
        stateSent += '|+>|' if bits_sender[i] == 0 else '|->|'
        basisSentChar += ' X |'

print("Let's compare this to the selected bases, and the transmitted qubit states")
print(f"The sender bases were:      {basisSentChar}")
print(f"The receiver bases were:    {basisRecChar}")
print(f"Both bases match (yes/no):  {same}")
print(f"The sender encoded bit:     {bitSent}")
print(f"The states sent were:       {stateSent}")
print(f"The receiver measured:      {bitRec}")
print("Notice how the key is formed by the bits where bases are equal")
print(f"Generated sender key:       {key_sender}")
print(f"Generated receiver key:     {key_receiver}")
