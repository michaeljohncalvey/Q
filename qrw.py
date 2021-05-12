import numpy as np
from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.tools.visualization import plot_histogram, plot_state_city

n = 3

qsubnodes = QuantumRegister(1, 'qanc')
print(qsubnodes)
print(qsubnodes[0])

# An n-qubit variant of the CX (Control Not) gate
def cnx(qc, *qubits):
    if len(qubits) >= 3:
        last = qubits[-1]

        # A matrix
        qc.crz(np.pi/2, qubits[-2], qubits[-1])
        qc.cu3(np.pi/2, 0, 0, qubits[-2], qubits[-1])

        # CNOT gate
        cnx(qc, *qubits[:-2], qubits[-1])

        # B matrix
        qc.cu3(-np.pi/2, 0, 0, qubits[-2], qubits[-1])

        # Control
        cnx(qc,*qubits[:-2],qubits[-1])

        # C Matrix
        qc.crz(-np.pi/2,qubits[-2],qubits[-1])
    elif len(qubits)==3:
        qc.ccx(*qubits)
    elif len(qubits)==2:
        qc.cx(*qubits)


# Increment Gate - shift position forward
def increment_gate(qwc, q, subnode):
    print(type(subnode))
    cnx(qwc, subnode, q[2], q[1], q[0])
    cnx(qwc, subnode, q[2], q[1])
    cnx(qwc, subnode, q[2])
    qwc.barrier()
    return qwc


# Decrement Gate - shift position backward
def decrement_gate(qwc, q, subnode):
    qwc.x(subnode)
    qwc.x(q[2])
    qwc.x(q[1])
    cnx(qwc, subnode, q[2], q[1], q[0])
    qwc.x(q[1])
    cnx(qwc, subnode, q[2], q[1])
    qwc.x(q[2])
    cnx(qwc, subnode, q[2])
    qwc.x(subnode)
    return qwc

from qiskit.providers.aer import AerSimulator

# Get simulation result and run iteratively
def ibmsim(circ):
    sim = AerSimulator()

    
    return sim.run(circ, ibmq_backend, shots=1000).result().get_counts(circ)


qnodes = QuantumRegister(n, 'qc')
qsubnodes = QuantumRegister(1, 'qanc')
cnodes = ClassicalRegister(n, 'cr')
csubnodes = ClassicalRegister(1, 'canc')

qwc = QuantumCircuit(qnodes, qsubnodes, cnodes, csubnodes)


# Run circuit
def runQWC(qwc, times):
    for i in range(times):
        qwc.h(qsubnodes[0])
        increment_gate(qwc, qnodes, qsubnodes[0])
        decrement_gate(qwc,qnodes,qsubnodes[0])
        qwc.measure(qnodes, cnodes)

    return qwc


import matplotlib as mpl
step = 1
qwc = runQWC(qwc, step)
qwc.draw(output="mpl")
result = ibmsim(qwc)

print(result)