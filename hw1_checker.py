import numpy as np

def check_homework_1(user_final_state):
    # Define the initial state |1⟩
    initial_state = np.array([0, 1])
    
    # Define the X gate
    X_gate = np.array([[0, 1],
                       [1, 0]])
    
    # Apply the X gate to the initial state
    expected_final_state = np.dot(X_gate, initial_state)
    
    # Check if the user's final state matches the expected final state
    if np.array_equal(user_final_state, expected_final_state):
        return "Correct! Your final state is the expected state |0⟩."
    else:
        return "Incorrect. Please try again."