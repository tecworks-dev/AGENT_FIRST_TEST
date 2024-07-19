import base64
import os

def generate_key():
    """
    Generates a new encryption key.

    Returns:
    bytes: A new encryption key.
    """
    return os.urandom(32)

def encrypt(message: str, key: bytes):
    """
    Encrypts a message using the provided key.

    Args:
    message (str): The message to encrypt.
    key (bytes): The encryption key.

    Returns:
    str: The encrypted message.
    """
    encoded = message.encode()
    encrypted = bytes(a ^ b for a, b in zip(encoded, key))
    return base64.b64encode(encrypted).decode()

def decrypt(encrypted_message: str, key: bytes):
    """
    Decrypts an encrypted message using the provided key.

    Args:
    encrypted_message (str): The encrypted message to decrypt.
    key (bytes): The encryption key.

    Returns:
    str: The decrypted message.
    """
    encrypted = base64.b64decode(encrypted_message)
    decrypted = bytes(a ^ b for a, b in zip(encrypted, key))
    return decrypted.decode()

# Example usage
if __name__ == "__main__":
    # Generate a new encryption key
    key = generate_key()
    if key:
        print("Generated key:", key)

        # Encrypt a message
        original_message = "Hello, World!"
        encrypted = encrypt(original_message, key)
        if encrypted:
            print("Encrypted message:", encrypted)

            # Decrypt the message
            decrypted = decrypt(encrypted, key)
            if decrypted:
                print("Decrypted message:", decrypted)
                
                # Verify the decryption
                assert original_message == decrypted, "Decryption failed"
                print("Encryption and decryption successful!")
    else:
        print("Failed to generate encryption key.")