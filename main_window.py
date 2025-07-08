import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QWidget, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
from quantum.state import Qubit
from quantum.gates import H, X, Z, CNOT, apply_gate
from quantum.protocols import teleport
from quantum.algorithms import grovers_search
from visualization.bloch_qt import BlochSphereWidget

class QuantumGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Simulator")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side - controls
        left_layout = QVBoxLayout()
        
        # Widgets
        self.btn_teleport = QPushButton("Run Teleportation", self)
        self.btn_grover = QPushButton("Run Grover's Search", self)
        self.btn_animate = QPushButton("Show Animation", self)
        self.output_label = QLabel("Results will appear here", self)
        self.output_label.setAlignment(Qt.AlignTop)
        self.output_label.setStyleSheet("font-size: 12px; margin: 10px; padding: 10px; border: 1px solid gray;")
        self.output_label.setWordWrap(True)
        
        # Add widgets to left layout
        left_layout.addWidget(self.btn_teleport)
        left_layout.addWidget(self.btn_grover)
        left_layout.addWidget(self.btn_animate)
        left_layout.addWidget(self.output_label)
        
        # Right side - Bloch sphere
        self.bloch_widget = BlochSphereWidget()
        
        # Create left container
        left_container = QWidget()
        left_container.setLayout(left_layout)
        left_container.setMaximumWidth(400)
        
        # Add to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(self.bloch_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Connect buttons
        self.btn_teleport.clicked.connect(self.run_teleportation)
        self.btn_grover.clicked.connect(self.run_grover)
        self.btn_animate.clicked.connect(self.run_animation)
        
        # Initialize with default qubit
        default_qubit = Qubit()
        self.bloch_widget.plot_qubit(default_qubit.state)

    def run_teleportation(self):
        """Demonstrate quantum teleportation"""
        try:
            original_qubit = Qubit(np.array([1, 1])/np.sqrt(2))  # |+⟩ state
            result = teleport(original_qubit, "Alice", "Bob", verbose=True)
            
            # Display results
            self.output_label.setText(
                f"TELEPORTATION RESULTS:\n"
                f"Original state: {np.round(original_qubit.state, 3)}\n"
                f"Teleported state: {np.round(result.state, 3)}\n"
                f"Fidelity: {np.abs(np.dot(original_qubit.state.conj(), result.state))**2:.3f}\n"
                f"Success: {np.allclose(original_qubit.state, result.state, atol=0.1)}"
            )
            
            # Update Bloch sphere
            self.bloch_widget.plot_qubit(result.state)
            
        except Exception as e:
            self.output_label.setText(f"Error in teleportation: {str(e)}")

    def run_grover(self):
        """Run Grover's search algorithm"""
        try:
            result = grovers_search(n_qubits=2)
            
            # Display results
            self.output_label.setText(
                f"GROVER'S SEARCH RESULTS:\n"
                f"Measurement result: {result}\n"
                f"Found target |11⟩: {result == [1, 1]}\n"
                f"Search completed successfully!"
            )
            
            # Create a qubit representing the found state
            if result == [1, 1]:
                found_state = np.array([0, 1])  # |1⟩ state
            else:
                found_state = np.array([1, 0])  # |0⟩ state
            
            self.bloch_widget.plot_qubit(found_state)
            
        except Exception as e:
            self.output_label.setText(f"Error in Grover's search: {str(e)}")

    def run_animation(self):
        """Show qubit animation"""
        try:
            from visualization.animate import animate_qubit
            animate_qubit()
            self.output_label.setText("Animation window opened!\nClose the matplotlib window to continue.")
        except Exception as e:
            self.output_label.setText(f"Error in animation: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = QuantumGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()