
import traceback
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def encrypt_message(message, public_key):
    """
    Encrypts a message using the recipient's public key.

    Args:
    message (str): The message to encrypt.
    public_key (bytes): The recipient's public key.

    Returns:
    bytes: The encrypted message.
    """
    try:
        # Deserialize the public key
        public_key = serialization.load_pem_public_key(
            public_key,
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
        return encrypted
    except Exception as e:
        print(f"Error encrypting message: {str(e)}")
        traceback.print_exc()
        return None

def decrypt_message(encrypted_message, private_key):
    """
    Decrypts a message using the recipient's private key.

    Args:
    encrypted_message (bytes): The encrypted message.
    private_key (bytes): The recipient's private key.

    Returns:
    str: The decrypted message.
    """
    try:
        # Deserialize the private key
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )

        # Decrypt the message
        decrypted = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()
    except Exception as e:
        print(f"Error decrypting message: {str(e)}")
        traceback.print_exc()
        return None

def generate_key_pair():
    """
    Generates a new public-private key pair.

    Returns:
    tuple: (public_key, private_key) as PEM-encoded bytes.
    """
    try:
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

        return (public_pem, private_pem)
    except Exception as e:
        print(f"Error generating key pair: {str(e)}")
        traceback.print_exc()
        return None

def encrypt_file(file_data, key):
    """
    Encrypts a file using Fernet symmetric encryption.

    Args:
    file_data (bytes): The file data to encrypt.
    key (bytes): The encryption key.

    Returns:
    bytes: The encrypted file data.
    """
    try:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        return encrypted_data
    except Exception as e:
        print(f"Error encrypting file: {str(e)}")
        traceback.print_exc()
        return None

def decrypt_file(encrypted_data, key):
    """
    Decrypts a file using Fernet symmetric encryption.

    Args:
    encrypted_data (bytes): The encrypted file data.
    key (bytes): The decryption key.

    Returns:
    bytes: The decrypted file data.
    """
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        print(f"Error decrypting file: {str(e)}")
        traceback.print_exc()
        return None

def generate_symmetric_key():
    """
    Generates a new symmetric key for file encryption.

    Returns:
    bytes: The generated symmetric key.
    """
    try:
        return Fernet.generate_key()
    except Exception as e:
        print(f"Error generating symmetric key: {str(e)}")
        traceback.print_exc()
        return None
