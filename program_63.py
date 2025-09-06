import numpy as np

def ket(n, size=2):
    state = np.zeros(size, dtype=np.complex128)
    state[n] = 1
    return state

def tensor_product(state1, state2):
    return np.kron(state1, state2)

def hadamard():
    return np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]], dtype=np.complex128)

def pauli_x():
    return np.array([[0, 1], [1, 0]], dtype=np.complex128)

def cnot():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ], dtype=np.complex128)

def apply_gate(gate, state_vector):
    return gate @ state_vector

if __name__ == "__main__":
    q0 = ket(0)
    q1 = ket(1)

    print("Initial state of a single qubit (q0):")
    print(q0)
    
    h_gate = hadamard()
    superposition = apply_gate(h_gate, q0)
    print("\nState after applying Hadamard gate to q0:")
    print(superposition)
    
    two_qubit_state = tensor_product(q0, q0)
    print("\nInitial state of two qubits (q0, q0):")
    print(two_qubit_state)
    
    cnot_gate = cnot()
    entangled_state = apply_gate(cnot_gate, apply_gate(tensor_product(h_gate, np.identity(2)), two_qubit_state))
    print("\nState after applying Hadamard to first qubit and then CNOT gate:")
    print(entangled_state)