import random
def generate_reset_password_token():
    return str(random.randint(100000, 999999))
