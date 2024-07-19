
# app/utils/encryption.py

"""
This module implements encryption and decryption functions for secure messaging.
It provides functions for generating encryption keys, encrypting and decrypting messages,
as well as hashing and verifying passwords.
"""

import traceback
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

# Set DEBUG to True for development, False for production
DEBUG = True

def generate_key() -> bytes:
    """
    Generate a new encryption key.

    Returns:
        bytes: A new encryption key.
    """
    try:
        return Fernet.generate_key()
    except Exception as e:
        if DEBUG:
            print(f"Error generating key: {str(e)}")
            print(traceback.format_exc())
        raise

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypt a message using the provided key.

    Args:
        message (str): The message to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted message.
    """
    try:
        f = Fernet(key)
        return f.encrypt(message.encode())
    except Exception as e:
        if DEBUG:
            print(f"Error encrypting message: {str(e)}")
            print(traceback.format_exc())
        raise

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypt an encrypted message using the provided key.

    Args:
        encrypted_message (bytes): The encrypted message.
        key (bytes): The decryption key.

    Returns:
        str: The decrypted message.
    """
    try:
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()
    except Exception as e:
        if DEBUG:
            print(f"Error decrypting message: {str(e)}")
            print(traceback.format_exc())
        raise

def hash_password(password: str) -> str:
    """
    Hash a password for secure storage.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    try:
        return generate_password_hash(password)
    except Exception as e:
        if DEBUG:
            print(f"Error hashing password: {str(e)}")
            print(traceback.format_exc())
        raise

def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Verify a provided password against a stored hashed password.

    Args:
        stored_password (str): The stored hashed password.
        provided_password (str): The password to verify.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    try:
        return check_password_hash(stored_password, provided_password)
    except Exception as e:
        if DEBUG:
            print(f"Error verifying password: {str(e)}")
            print(traceback.format_exc())
        raise

if DEBUG:
    print("Encryption module loaded successfully.")
