
"""
Purpose: Handles message encryption and decryption for the Secure Messaging Platform.

This module provides functions for generating encryption keys, encrypting messages,
and decrypting messages using the Fernet symmetric encryption scheme from the
cryptography library.
"""

import traceback
from cryptography.fernet import Fernet
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

def generate_key():
    """
    Generate a new encryption key.

    Returns:
        bytes: A new encryption key.
    """
    try:
        key = Fernet.generate_key()
        if DEBUG:
            logger.debug(f"Generated new encryption key: {key}")
        return key
    except Exception as e:
        logger.error(f"Error generating encryption key: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
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
        encrypted_message = f.encrypt(message.encode())
        if DEBUG:
            logger.debug(f"Message encrypted: {message} -> {encrypted_message}")
        return encrypted_message
    except Exception as e:
        logger.error(f"Error encrypting message: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        raise

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypt an encrypted message using the provided key.

    Args:
        encrypted_message (bytes): The encrypted message to decrypt.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted message.
    """
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        if DEBUG:
            logger.debug(f"Message decrypted: {encrypted_message} -> {decrypted_message}")
        return decrypted_message
    except Exception as e:
        logger.error(f"Error decrypting message: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        raise

# Unit tests
import unittest

class TestEncryption(unittest.TestCase):
    def test_encryption_decryption(self):
        key = generate_key()
        original_message = "Hello, World!"
        encrypted = encrypt_message(original_message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(original_message, decrypted)

    def test_different_keys(self):
        key1 = generate_key()
        key2 = generate_key()
        message = "Test message"
        encrypted = encrypt_message(message, key1)
        with self.assertRaises(Exception):
            decrypt_message(encrypted, key2)

if __name__ == "__main__":
    unittest.main()
