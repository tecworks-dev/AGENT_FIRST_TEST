
"""
Purpose: Implements end-to-end encryption for messages and files.

This module provides functions for encrypting and decrypting messages,
as well as generating public-private key pairs for secure communication.
"""

import traceback
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from app.utils import config, logger

# Initialize logger
log = logger.setup_logger()

# Set debug mode
DEBUG = True

def encrypt_message(message: str, public_key: str) -> str:
    """
    Encrypts a message using the recipient's public key.

    Args:
    message (str): The message to be encrypted.
    public_key (str): The recipient's public key in PEM format.

    Returns:
    str: The encrypted message as a base64-encoded string.
    """
    try:
        if DEBUG:
            log.debug(f"Encrypting message: {message[:10]}...")

        # Load the public key
        public_key = serialization.load_pem_public_key(
            public_key.encode(),
            backend=default_backend()
        )

        # Encrypt the message
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Return the encrypted message as a base64-encoded string
        return encrypted.hex()
    except Exception as e:
        log.error(f"Error encrypting message: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return None

def decrypt_message(encrypted_message: str, private_key: str) -> str:
    """
    Decrypts a message using the recipient's private key.

    Args:
    encrypted_message (str): The encrypted message as a base64-encoded string.
    private_key (str): The recipient's private key in PEM format.

    Returns:
    str: The decrypted message.
    """
    try:
        if DEBUG:
            log.debug(f"Decrypting message: {encrypted_message[:10]}...")

        # Load the private key
        private_key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )

        # Decrypt the message
        decrypted = private_key.decrypt(
            bytes.fromhex(encrypted_message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Return the decrypted message as a string
        return decrypted.decode()
    except Exception as e:
        log.error(f"Error decrypting message: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return None

def generate_key_pair() -> tuple:
    """
    Generates a public-private key pair.

    Returns:
    tuple: A tuple containing the public key and private key in PEM format.
    """
    try:
        if DEBUG:
            log.debug("Generating new key pair...")

        # Generate a new RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Get the public key
        public_key = private_key.public_key()

        # Serialize the keys to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return (public_pem.decode(), private_pem.decode())
    except Exception as e:
        log.error(f"Error generating key pair: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return None

if DEBUG:
    log.debug("Encryption module loaded successfully.")
