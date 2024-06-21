import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import base64

def _obscure_logic(a, b):
    return np.dot(a, np.linalg.inv(np.linalg.inv(b)))

def _encode_message(msg):
    return base64.b64encode(msg.encode()).decode()

def _decode_message(encoded_msg):
    return base64.b64decode(encoded_msg).decode()

def check_homework_1(user_final_state):
    a = np.array([0, 1])
    
    b = np.array(list(map(lambda x: [x[1], x[0]], [[0, 1], [1, 0]])))
    expected_final_state = _obscure_logic(a, b)

    correct_msg = _encode_message("Correct! Your final state is the expected state |0⟩. 🔥❤️👍")
    incorrect_msg = _encode_message("Incorrect. Please try again. ⚠️")
    
    if np.array_equal(user_final_state, expected_final_state):
        return _decode_message(correct_msg)
    else:
        return _decode_message(incorrect_msg)

def check_homework_2(student_circuit):
    init_circuit = QuantumCircuit(1)
    init_circuit.h(0)
    backend = Aer.get_backend('statevector_simulator')
    init_circuit = transpile(init_circuit, backend)
    job = backend.run(init_circuit, shots=1000)
    plus_state = job.result().get_statevector()
    
    expected_circuit = QuantumCircuit(1)
    expected_circuit.h(0)  
    expected_circuit.x(0) 

    expected_circuit = transpile(expected_circuit, backend)
    job = backend.run(expected_circuit, shots=1000)
    expected_final_state = job.result().get_statevector()
    
    student_circuit = transpile(student_circuit, backend)
    job = backend.run(student_circuit, shots=1000)
    student_final_state = job.result().get_statevector()
    
    if np.allclose(student_final_state, expected_final_state):
        return "Correct! Your final state matches the expected state."
    else:
        return "Incorrect. Please try again."