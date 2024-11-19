### Encryption of SQL queries for privacy purposes ###

from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


# Generate key for SQL encryption
def generate_key():
    return Fernet.generate_key().decode()


# Load key from .env and return cipher object
def load_cipher():
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY").encode()
    # !!!Provide key for testing purposes!!!
    cipher = Fernet(key)

    return cipher


def encrypt_value(value):
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    return cipher.encrypt(value.encode()).decode()


def decrypt_value(value):
    if value is None:
        return None
    return cipher.decrypt(value.encode()).decode()


cipher = load_cipher()
