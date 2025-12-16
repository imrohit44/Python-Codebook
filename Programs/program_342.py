import numpy as np

class QuantumSimulator:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        # Initialize state to |0...0>
        self.state_vector = np.zeros(2**num_qubits, dtype=complex)
        self.state_vector[0] = 1.0

        # Define gates
        self.H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        self.X = np.array([[0, 1], [1, 0]], dtype=complex)

    def _get_identity(self):
        return np.eye(2, dtype=complex)

    def apply_gate(self, gate_matrix, target_qubit):
        # Build the full tensor product matrix for the operation
        op_matrix = 1
        for i in range(self.num_qubits):
            if i == target_qubit:
                op_matrix = np.kron(op_matrix, gate_matrix)
            else:
                op_matrix = np.kron(op_matrix, self._get_identity())
        
        # Apply the transformation
        self.state_vector = op_matrix.dot(self.state_vector)

    def measure(self):
        # Return probability distribution (magnitudes squared)
        probabilities = np.abs(self.state_vector)**2
        return probabilities

    def run_circuit(self):
        # Example Circuit: H on qubit 0, X on qubit 1
        self.apply_gate(self.H, target_qubit=0)
        self.apply_gate(self.X, target_qubit=1)
        
        return self.measure()

if __name__ == '__main__':
    simulator = QuantumSimulator(num_qubits=2)
    probabilities = simulator.run_circuit()
    
    print("State |00> probability:", probabilities[0])
    print("State |01> probability:", probabilities[1])
    print("State |10> probability:", probabilities[2])
    print("State |11> probability:", probabilities[3])