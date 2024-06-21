import numpy as np
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