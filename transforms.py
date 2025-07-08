import numpy as np
from .gates import H, apply_gate 

def qft(qubits):
    """Quantum Fourier Transform on a list of qubits."""
    n = len(qubits)
    for i in range(n):
        for j in range(i):
            # Apply controlled rotations
            angle = np.pi/(2**(i-j))
            qubits[i].state = apply_gate(qubits[i].state, 
                np.array([[1, 0], [0, np.exp(1j*angle)]]))
        qubits[i].state = apply_gate(qubits[i].state, H)
    return qubits