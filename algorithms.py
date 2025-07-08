import numpy as np
from .gates import H, X, Z, apply_gate
from .state import Qubit

def simple_oracle(qubits, target_state=[1, 1]):
    """Oracle that marks the target state by applying phase flip"""
    # Check if we're in the target state (simplified)
    # In a real implementation, this would be more sophisticated
    if len(qubits) >= 2:
        # Apply conditional phase flip to last qubit if in target state
        # This is a simplified oracle
        qubits[-1].state = apply_gate(qubits[-1].state, Z)
    return qubits

def diffusion_operator(qubits):
    """Apply the diffusion operator (inversion about average)"""
    n = len(qubits)
    
    # Apply H to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, H)
    
    # Apply X to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, X)
    
    # Apply multi-controlled Z (simplified for 2 qubits)
    if n == 2:
        # For 2 qubits, apply Z to second qubit if first is |1⟩
        qubits[1].state = apply_gate(qubits[1].state, Z)
    
    # Apply X to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, X)
    
    # Apply H to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, H)
    
    return qubits

def grovers_search(n_qubits=2, iterations=None, target_state=[1, 1]):
    """Grover's search algorithm implementation"""
    
    # Initialize qubits in |0⟩ state
    qubits = [Qubit() for _ in range(n_qubits)]
    
    # Create superposition by applying Hadamard to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, H)
    
    # Determine optimal number of iterations
    if iterations is None:
        N = 2**n_qubits
        iterations = int(np.pi/4 * np.sqrt(N))
    
    # Grover iterations
    for i in range(iterations):
        # Apply oracle
        qubits = simple_oracle(qubits, target_state)
        
        # Apply diffusion operator
        qubits = diffusion_operator(qubits)
    
    # Measure all qubits
    results = [q.measure() for q in qubits]
    
    return results

def quantum_fourier_transform(qubits):
    """Simplified Quantum Fourier Transform"""
    n = len(qubits)
    
    for i in range(n):
        # Apply Hadamard
        qubits[i].state = apply_gate(qubits[i].state, H)
        
        # Apply controlled phase rotations (simplified)
        for j in range(i + 1, n):
            # This is a simplified version
            # In reality, we'd need proper controlled gates
            angle = np.pi / (2**(j-i))
            rotation_gate = np.array([[1, 0], [0, np.exp(1j * angle)]])
            qubits[j].state = apply_gate(qubits[j].state, rotation_gate)
    
    return qubits

def bernstein_vazirani(secret_string="101"):
    """Bernstein-Vazirani algorithm to find secret string"""
    n = len(secret_string)
    
    # Initialize qubits
    qubits = [Qubit() for _ in range(n)]
    ancilla = Qubit()
    
    # Initialize ancilla in |1⟩ state
    ancilla.state = apply_gate(ancilla.state, X)
    
    # Apply Hadamard to all qubits
    for q in qubits:
        q.state = apply_gate(q.state, H)
    ancilla.state = apply_gate(ancilla.state, H)
    
    # Apply oracle (simplified)
    for i, bit in enumerate(secret_string):
        if bit == '1':
            # Apply CNOT between qubit i and ancilla
            # This is simplified - in reality we'd need proper multi-qubit gates
            qubits[i].state = apply_gate(qubits[i].state, X)
    
    # Apply Hadamard to all qubits again
    for q in qubits:
        q.state = apply_gate(q.state, H)
    
    # Measure qubits
    result = [q.measure() for q in qubits]
    
    return ''.join(map(str, result))

def shors_period_finding(N=15, a=7):
    """Simplified Shor's algorithm for period finding"""
    # This is a highly simplified version for demonstration
    # Real Shor's algorithm is much more complex
    
    # Number of qubits needed
    n = int(np.ceil(np.log2(N)))
    
    # Initialize qubits
    qubits = [Qubit() for _ in range(2 * n)]
    
    # Create superposition in first register
    for i in range(n):
        qubits[i].state = apply_gate(qubits[i].state, H)
    
    # Apply modular exponentiation (simplified)
    # In reality, this would be a complex quantum circuit
    
    # Apply QFT to first register
    first_register = qubits[:n]
    quantum_fourier_transform(first_register)
    
    # Measure first register
    result = [q.measure() for q in first_register]
    
    # Classical post-processing would find the period
    # For demonstration, return a simple result
    return result

if __name__ == "__main__":
    # Test the algorithms
    print("Testing Grover's Search:")
    result = grovers_search(n_qubits=2)
    print(f"Result: {result}")
    
    print("\nTesting Bernstein-Vazirani:")
    secret = bernstein_vazirani("101")
    print(f"Found secret string: {secret}")
    
    print("\nTesting Shor's Period Finding:")
    period_result = shors_period_finding()
    print(f"Period finding result: {period_result}")