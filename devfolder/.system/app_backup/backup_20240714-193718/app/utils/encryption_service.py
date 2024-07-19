
# Purpose: Provides encryption and decryption utilities for sensitive data.
# Description: This module implements an EncryptionService class that uses the Fernet
# symmetric encryption scheme to securely encrypt and decrypt sensitive information.

import os
from cryptography.fernet import Fernet
import base64
import logging
import traceback

DEBUG = True

class EncryptionService:
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self):
        key_file = 'encryption_key.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
        return key

    def encrypt(self, data: str) -> str:
        """
        Encrypts the given string data.

        Args:
            data (str): The string to be encrypted.

        Returns:
            str: The encrypted data as a base64-encoded string.
        """
        try:
            if DEBUG:
                print(f"Encrypting data: {data[:10]}...")
            
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logging.error(f"Error during encryption: {str(e)}")
            if DEBUG:
                print(f"Encryption error: {traceback.format_exc()}")
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts the given encrypted data.

        Args:
            encrypted_data (str): The encrypted data as a base64-encoded string.

        Returns:
            str: The decrypted string.
        """
        try:
            if DEBUG:
                print(f"Decrypting data: {encrypted_data[:10]}...")
            
            decoded_data = base64.urlsafe_b64decode(encrypted_data)
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logging.error(f"Error during decryption: {str(e)}")
            if DEBUG:
                print(f"Decryption error: {traceback.format_exc()}")
            raise

# Example usage
if __name__ == "__main__":
    encryption_service = EncryptionService()
    
    # Test encryption and decryption
    original_data = "This is a secret message!"
    encrypted = encryption_service.encrypt(original_data)
    decrypted = encryption_service.decrypt(encrypted)
    
    print(f"Original: {original_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Decryption successful: {original_data == decrypted}")
