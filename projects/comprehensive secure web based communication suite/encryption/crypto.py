
"""
Purpose: Handles end-to-end encryption for all communications.
Description: This module provides an EncryptionManager class that handles encryption and decryption
of data using the Fernet symmetric encryption scheme. It also includes functionality for key
generation and management.
"""

import os
import base64
import traceback
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DEBUG = True

class EncryptionManager:
    def __init__(self):
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)

    def _generate_key(self):
        """
        Generate a secure encryption key using PBKDF2.
        """
        try:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
            if DEBUG:
                print(f"DEBUG: Generated encryption key: {key}")
            return key
        except Exception as e:
            print(f"Error generating encryption key: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return None

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt the given data using Fernet symmetric encryption.

        Args:
            data (bytes): The data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        try:
            encrypted_data = self.fernet.encrypt(data)
            if DEBUG:
                print(f"DEBUG: Encrypted data: {encrypted_data[:20]}...")
            return encrypted_data
        except Exception as e:
            print(f"Error encrypting data: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return None

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt the given data using Fernet symmetric encryption.

        Args:
            data (bytes): The data to be decrypted.

        Returns:
            bytes: The decrypted data.
        """
        try:
            decrypted_data = self.fernet.decrypt(data)
            if DEBUG:
                print(f"DEBUG: Decrypted data: {decrypted_data[:20]}...")
            return decrypted_data
        except Exception as e:
            print(f"Error decrypting data: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return None

if __name__ == "__main__":
    # Test the EncryptionManager
    manager = EncryptionManager()
    original_data = b"This is a test message."
    encrypted = manager.encrypt(original_data)
    decrypted = manager.decrypt(encrypted)
    
    print(f"Original: {original_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    assert original_data == decrypted, "Encryption/Decryption test failed!"
    print("Encryption/Decryption test passed successfully!")
