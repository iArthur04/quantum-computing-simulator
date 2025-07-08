import numpy as np

class Qubit:
    def __init__(self, state=None):
        # Fixed the missing space in the comment
        self.state = state if state is not None else np.array([1, 0])  # |0⟩ by default

    def measure(self):
        """Collapse the state to |0⟩ or |1⟩ probabilistically."""
        prob_0 = np.abs(self.state[0])**2
        return 0 if np.random.random() < prob_0 else 1

    def tensor_product(self, other):
        """Combine two qubits (for multi-qubit systems)."""
        return np.kron(self.state, other.state)
    
    def __str__(self):
        """String representation of the qubit state."""
        return f"Qubit state: {self.state}"