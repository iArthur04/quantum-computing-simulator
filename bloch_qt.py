# visualization/bloch_qt.py
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class BlochSphereWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        
        # Add title label
        self.title_label = QLabel("Bloch Sphere Visualization")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        self.setup_sphere()
        
    def setup_sphere(self):
        """Set up the basic Bloch sphere structure"""
        self.ax.clear()
        
        # Create sphere surface
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot sphere with transparency
        self.ax.plot_surface(x, y, z, color='lightblue', alpha=0.2)
        
        # Add coordinate axes
        self.ax.quiver(0, 0, 0, 1.2, 0, 0, color='gray', alpha=0.8, arrow_length_ratio=0.1)
        self.ax.quiver(0, 0, 0, 0, 1.2, 0, color='gray', alpha=0.8, arrow_length_ratio=0.1)
        self.ax.quiver(0, 0, 0, 0, 0, 1.2, color='gray', alpha=0.8, arrow_length_ratio=0.1)
        
        # Add labels
        self.ax.text(1.3, 0, 0, 'X', fontsize=12)
        self.ax.text(0, 1.3, 0, 'Y', fontsize=12)
        self.ax.text(0, 0, 1.3, 'Z', fontsize=12)
        
        # Add |0⟩ and |1⟩ labels
        self.ax.text(0, 0, 1.1, '|0⟩', fontsize=14, ha='center')
        self.ax.text(0, 0, -1.1, '|1⟩', fontsize=14, ha='center')
        
        # Set equal aspect ratio and limits
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        
        # Remove axis ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
    def plot_qubit(self, state):
        """Plot a qubit state on the Bloch sphere"""
        self.setup_sphere()
        
        # Normalize state if needed
        state = state / np.linalg.norm(state)
        
        # Extract amplitudes
        alpha = state[0]  # |0⟩ amplitude
        beta = state[1]   # |1⟩ amplitude
        
        # Calculate Bloch sphere coordinates
        # For a qubit state |ψ⟩ = α|0⟩ + β|1⟩
        # Bloch coordinates are:
        x = 2 * np.real(alpha * np.conj(beta))
        y = 2 * np.imag(alpha * np.conj(beta))
        z = np.abs(alpha)**2 - np.abs(beta)**2
        
        # Plot the state vector
        self.ax.quiver(0, 0, 0, x, y, z, 
                      color='red', linewidth=3, arrow_length_ratio=0.1)
        
        # Add a point at the tip
        self.ax.scatter([x], [y], [z], color='red', s=100, alpha=0.8)
        
        # Add state information as text
        state_info = f"State: {alpha:.3f}|0⟩ + {beta:.3f}|1⟩"
        coord_info = f"Bloch coords: ({x:.3f}, {y:.3f}, {z:.3f})"
        self.ax.text2D(0.02, 0.98, state_info, transform=self.ax.transAxes, 
                       fontsize=10, verticalalignment='top',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
        self.ax.text2D(0.02, 0.90, coord_info, transform=self.ax.transAxes, 
                       fontsize=10, verticalalignment='top',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5))
        
        # Update canvas
        self.canvas.draw()