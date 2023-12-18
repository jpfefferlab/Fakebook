import uuid

def get_random_string():
    random_string = str(uuid.uuid4())[:8].replace('-', '').lower()
    return random_string

