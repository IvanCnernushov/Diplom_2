import random
import string


def generate_unique_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}@example.com"


def generate_invalid_ingredient_hash():
    return "invalid_ingredient_hash_12345"