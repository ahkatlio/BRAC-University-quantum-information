#_____________________________Import Libraries______________________#
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import base64
from sympy import Matrix
from sympy.physics.quantum import TensorProduct as tensor_product

#_____________________________Functions_____________________________#

def _obscure_logic(a, b):
    return np.dot(a, np.linalg.inv(np.linalg.inv(b)))

def _encode_message(msg):
    return base64.b64encode(msg.encode()).decode()

def _decode_message(encoded_msg):
    return base64.b64decode(encoded_msg).decode()

#_____________________________Homework Grader________________________#

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
    
def check_homework_3(student_circuit):
    backend = Aer.get_backend('statevector_simulator')
    
    expected_final_state = Statevector.from_label('1')
    
    transpiled_student_circuit = transpile(student_circuit, backend)
    
    job = backend.run(transpiled_student_circuit)
    student_final_state = job.result().get_statevector()
    if np.allclose(student_final_state, expected_final_state):
        return "Correct! Your final state is |1⟩."
    else:
        return "Incorrect. The final state is not |1⟩. Please try again."

def grade_homework_5(student_responses):
    CX = Matrix([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]])

    qubit_0 = Matrix([1, 0])  
    qubit_1 = Matrix([0, 1])  
    
    initial_states = {
        '|11⟩': tensor_product(qubit_1, qubit_1),
        '|01⟩': tensor_product(qubit_0, qubit_1),
        '|00⟩': tensor_product(qubit_0, qubit_0)
    }
    
    expected_results = {
        '|11⟩': '10',
        '|01⟩': '01',
        '|00⟩': '00'
    }
    
    grades = {}
    for state_label, initial_state in initial_states.items():
        result_state = CX * initial_state
        index = result_state.tolist().index([1])
        binary_state = format(index, '02b')
        grades[state_label] = ('Correct' if binary_state == expected_results[state_label] else 'Incorrect')
    
    for state_label, student_answer in student_responses.items():
        if grades[state_label] == 'Correct' and student_answer == expected_results[state_label]:
            grades[state_label] = 'Correct'
        else:
            grades[state_label] = 'Incorrect'
    
    return grades

def grade_homework_6(student_circuit):
    simulator = Aer.get_backend('statevector_simulator')
    transpiled_circuit = transpile(student_circuit, simulator)
    result = simulator.run(transpiled_circuit).result()
    statevector = result.get_statevector()
    expected_state = Statevector.from_label('01')
    if statevector == expected_state:
        return "Correct! Your circuit correctly implements the CX gate for the |11⟩ state."
    else:
        return "Incorrect. The expected output is |10⟩. Please review your circuit."
    
def grade_homework_7_qc(student_circuit):
    simulator = Aer.get_backend('statevector_simulator')
    transpiled_circuit = transpile(student_circuit, simulator)
    result =  simulator.run(transpiled_circuit).result()
    statevector = result.get_statevector()
    
    expected_state = Statevector.from_label('01')
    if statevector == expected_state:
        return "Quantum Circuit Part: Correct!"
    else:
        return "Quantum Circuit Part: Incorrect. The expected output is |01⟩."

def grade_homework_7_matrix(final_state):
    expected_final_state = Matrix([[0], [1], [0], [0]])
    if final_state == expected_final_state:
        return "Matrix Calculation Part: Correct!"
    else:
        return "Matrix Calculation Part: Incorrect. The expected output is |01⟩."

def grade_homework_8(student_circuit):
    simulator = Aer.get_backend('statevector_simulator')
    transpiled_circuit = transpile(student_circuit, simulator)
    result = simulator.run(transpiled_circuit).result()
    student_statevector = result.get_statevector()
    
    expected_statevector = Statevector([0.88145203-0.10567166j, 0.35765803-0.28975256j])
    
    if np.allclose(student_statevector, expected_statevector.data):
        return "Correct! Your circuit correctly implements the specified rotations."
    else:
        return "Incorrect. Please check your rotations and try again."