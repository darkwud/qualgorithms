from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate

def draw_ascii_counting():
    print("\n" + "="*50)
    print(" SLIDE 2: QUANTUM COUNTING ARCHITECTURE ")
    print("="*50)
    
    t_reg = QuantumRegister(3, 't_count')
    n_reg = QuantumRegister(2, 'n_search')
    c_reg = ClassicalRegister(3, 'meas')
    qc = QuantumCircuit(t_reg, n_reg, c_reg)
    
    # Initialization
    qc.h(t_reg)
    qc.h(n_reg)
    qc.barrier()
    
    # Controlled Grover Iterations
    cg1 = Gate(name="G^1", num_qubits=3, params=[])
    cg2 = Gate(name="G^2", num_qubits=3, params=[])
    cg4 = Gate(name="G^4", num_qubits=3, params=[])
    
    qc.append(cg1, [t_reg[0], n_reg[0], n_reg[1]])
    qc.append(cg2, [t_reg[1], n_reg[0], n_reg[1]])
    qc.append(cg4, [t_reg[2], n_reg[0], n_reg[1]])
    qc.barrier()
    
    # Inverse QFT
    iqft = Gate(name="IQFT", num_qubits=3, params=[])
    qc.append(iqft, [t_reg[0], t_reg[1], t_reg[2]])
    qc.barrier()
    
    # Measurement
    qc.measure(t_reg, c_reg)
    
    # Print ASCII Circuit with |0> kets
    print(qc.draw(output='text', initial_state=True))


def draw_ascii_decoherence():
    print("\n" + "="*50)
    print(" SLIDE 4: THE UNCOMPUTATION BOTTLENECK ")
    print("="*50)
    
    search = QuantumRegister(2, 'Search')
    scratch = QuantumRegister(2, 'Scratch')
    qc = QuantumCircuit(search, scratch)
    
    qc.h(search)
    qc.barrier()
    
    # Compute
    compute = Gate(name="Compute", num_qubits=4, params=[])
    qc.append(compute, [0, 1, 2, 3])
    
    # Mark
    mark = Gate(name="Mark(-1)", num_qubits=2, params=[])
    qc.append(mark, [2, 3])
    qc.barrier()
    
    # The Mistake (Garbage leftover)
    garbage = Gate(name="Garbage Leftover", num_qubits=2, params=[])
    qc.append(garbage, [2, 3])
    
    # Print ASCII Circuit with |0> kets
    print(qc.draw(output='text', initial_state=True))

if __name__ == "__main__":
    draw_ascii_counting()
    draw_ascii_decoherence()
    print("\n")