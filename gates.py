import numpy as np

# Single-qubit gates
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])

# Two-qubit gates
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])

def apply_gate(state, gate):
    """Safe gate application with dimension check"""
    if gate.shape[1] != state.shape[0]:
        raise ValueError(f"Gate dimension {gate.shape} incompatible with state {state.shape}")
    return np.dot(gate, state)