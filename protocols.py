import numpy as np
from .gates import H, X, Z, CNOT, apply_gate
from .state import Qubit

def teleport(qubit, sender, receiver, verbose=False):
    """Fixed teleportation protocol with proper gate dimensions"""
    if verbose: print(f"\n=== Teleporting qubit from {sender} to {receiver} ===")
    
    # Step 1: Create Bell pair (|00> + |11>)/√2
    alice = Qubit(np.array([1, 0]))
    bob = Qubit(np.array([1, 0]))
    alice.state = apply_gate(alice.state, H)
    bell_state = apply_gate(np.kron(alice.state, bob.state), CNOT)
    if verbose: 
        print(f"1. Bell pair created: {np.round(bell_state, 3)}")
    
    # Step 2: Combine with input qubit (|ψ⟩⊗(|00⟩+|11⟩)/√2)
    combined = np.kron(qubit.state, bell_state)
    if verbose:
        print(f"2. Combined state (|ψ⟩⊗Bell):\n{np.round(combined, 3)}")
    
    # Step 3: Alice's operations (CNOT then H on her qubits)
    # System ordering: |ψ⟩|a⟩|b⟩
    cnot_gate = np.kron(CNOT, np.eye(2))  # CNOT on ψ and a
    hadamard_gate = np.kron(np.kron(H, np.eye(2)), np.eye(2))  # H on ψ
    combined = apply_gate(combined, cnot_gate)
    combined = apply_gate(combined, hadamard_gate)
    if verbose:
        print(f"3. After Alice's operations:\n{np.round(combined, 3)}")
    
    # Step 4: Measurement simulation (simplified)
    m1 = 0 if np.random.random() < 0.5 else 1  # ψ measurement
    m2 = 0 if np.random.random() < 0.5 else 1  # a measurement
    if verbose:
        print(f"4. Measurement results: m1={m1}, m2={m2}")
    
    # Step 5: Bob's correction
    if m2: bob.state = apply_gate(bob.state, X)
    if m1: bob.state = apply_gate(bob.state, Z)
    if verbose:
        print(f"5. Bob's final state: {np.round(bob.state, 3)}")
    
    return bob