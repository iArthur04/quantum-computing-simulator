import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from quantum.state import Qubit
from quantum.gates import H, apply_gate

def animate_qubit():
    """Animate qubit state evolution on Bloch sphere"""
    fig = plt.figure(figsize=(10, 5))
    
    # Create two subplots
    ax1 = fig.add_subplot(121)  # 2D probability plot
    ax2 = fig.add_subplot(122, projection='3d')  # 3D Bloch sphere
    
    # Initialize qubit
    qubit = Qubit()
    
    # Data storage for animation
    probs_0 = []
    probs_1 = []
    frames_data = []
    
    def init():
        ax1.clear()
        ax2.clear()
        
        # Setup 2D plot
        ax1.set_xlim(0, 20)
        ax1.set_ylim(0, 1)
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Probability')
        ax1.set_title('Qubit Measurement Probabilities')
        ax1.legend(['|0⟩', '|1⟩'])
        
        # Setup 3D Bloch sphere
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        ax2.plot_surface(x, y, z, color='lightblue', alpha=0.3)
        
        ax2.set_xlim([-1.5, 1.5])
        ax2.set_ylim([-1.5, 1.5])
        ax2.set_zlim([-1.5, 1.5])
        ax2.set_title('Bloch Sphere Evolution')
        
        return []
    
    def update(frame):
        # Apply Hadamard gate to evolve the state
        qubit.state = apply_gate(qubit.state, H)
        
        # Calculate probabilities
        prob_0 = np.abs(qubit.state[0])**2
        prob_1 = np.abs(qubit.state[1])**2
        
        probs_0.append(prob_0)
        probs_1.append(prob_1)
        
        # Update 2D plot
        ax1.clear()
        ax1.plot(range(len(probs_0)), probs_0, 'b-', label='|0⟩')
        ax1.plot(range(len(probs_1)), probs_1, 'r-', label='|1⟩')
        ax1.set_xlim(0, 20)
        ax1.set_ylim(0, 1)
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Probability')
        ax1.set_title('Qubit Measurement Probabilities')
        ax1.legend()
        ax1.grid(True)
        
        # Update 3D Bloch sphere
        ax2.clear()
        
        # Redraw sphere
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        ax2.plot_surface(x_sphere, y_sphere, z_sphere, color='lightblue', alpha=0.3)
        
        # Calculate Bloch coordinates
        alpha = qubit.state[0]
        beta = qubit.state[1]
        
        x = 2 * np.real(alpha * np.conj(beta))
        y = 2 * np.imag(alpha * np.conj(beta))
        z = np.abs(alpha)**2 - np.abs(beta)**2
        
        # Draw state vector
        ax2.quiver(0, 0, 0, x, y, z, color='red', linewidth=3, arrow_length_ratio=0.1)
        ax2.scatter([x], [y], [z], color='red', s=100)
        
        # Add axes
        ax2.quiver(0, 0, 0, 1.2, 0, 0, color='gray', alpha=0.6, arrow_length_ratio=0.1)
        ax2.quiver(0, 0, 0, 0, 1.2, 0, color='gray', alpha=0.6, arrow_length_ratio=0.1)
        ax2.quiver(0, 0, 0, 0, 0, 1.2, color='gray', alpha=0.6, arrow_length_ratio=0.1)
        
        ax2.text(0, 0, 1.3, '|0⟩', fontsize=12)
        ax2.text(0, 0, -1.3, '|1⟩', fontsize=12)
        
        ax2.set_xlim([-1.5, 1.5])
        ax2.set_ylim([-1.5, 1.5])
        ax2.set_zlim([-1.5, 1.5])
        ax2.set_title(f'Bloch Sphere (Frame {frame})')
        
        return []
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=20, init_func=init, 
                       blit=False, interval=500, repeat=True)
    
    plt.tight_layout()
    plt.show()
    
    return ani

def plot_quantum_circuit():
    """Plot a simple quantum circuit diagram"""
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Draw circuit lines
    ax.plot([0, 6], [2, 2], 'k-', linewidth=2)  # Qubit line
    ax.plot([0, 6], [1, 1], 'k-', linewidth=2)  # Ancilla line
    
    # Add gates
    # Hadamard gate
    rect_h = plt.Rectangle((1, 1.8), 0.4, 0.4, facecolor='lightblue', edgecolor='black')
    ax.add_patch(rect_h)
    ax.text(1.2, 2, 'H', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # CNOT gate
    ax.plot([3, 3], [1, 2], 'k-', linewidth=2)
    ax.scatter([3], [2], s=100, c='black')
    ax.scatter([3], [1], s=200, c='white', edgecolors='black', linewidth=2)
    ax.plot([2.9, 3.1], [1, 1], 'k-', linewidth=2)
    ax.plot([3, 3], [0.9, 1.1], 'k-', linewidth=2)
    
    # Measurement
    rect_m = plt.Rectangle((4.8, 1.8), 0.4, 0.4, facecolor='lightgreen', edgecolor='black')
    ax.add_patch(rect_m)
    ax.text(5, 2, 'M', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Labels
    ax.text(-0.3, 2, '|ψ⟩', ha='center', va='center', fontsize=14)
    ax.text(-0.3, 1, '|0⟩', ha='center', va='center', fontsize=14)
    
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(0.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Quantum Teleportation Circuit', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    animate_qubit()