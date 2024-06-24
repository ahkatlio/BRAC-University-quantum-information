import random

def generate_hidden_binary_string():
    length = random.randint(1, 10)
    
    binary_string = ''.join(random.choices(['0', '1'], k=length))
    
    return binary_string