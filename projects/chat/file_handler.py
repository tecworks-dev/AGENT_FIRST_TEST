
import base64
import os
import traceback

def encode_file(file_path: str) -> str:
    """
    Encodes the contents of a file to base64.

    Args:
        file_path (str): The path to the file to be encoded.

    Returns:
        str: The base64 encoded content of the file.

    Raises:
        FileNotFoundError: If the specified file is not found.
        IOError: If there's an error reading the file.
    """
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        return encoded_content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        traceback.print_exc()
    except IOError as e:
        print(f"Error reading file: {e}")
        traceback.print_exc()
    return ""

def decode_file(encoded_content: str, file_name: str) -> bool:
    """
    Decodes base64 encoded content and saves it as a file.

    Args:
        encoded_content (str): The base64 encoded content to be decoded.
        file_name (str): The name of the file to save the decoded content.

    Returns:
        bool: True if the file was successfully saved, False otherwise.

    Raises:
        IOError: If there's an error writing the file.
    """
    try:
        decoded_content = base64.b64decode(encoded_content)
        with open(file_name, "wb") as file:
            file.write(decoded_content)
        print(f"File saved successfully: {file_name}")
        return True
    except IOError as e:
        print(f"Error writing file: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    return False

# Example usage (can be removed in production)
if __name__ == "__main__":
    # Test encoding
    test_file_path = "test_file.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test file for encoding and decoding.")
    
    encoded = encode_file(test_file_path)
    print(f"Encoded content: {encoded[:50]}...")  # Print first 50 characters
    
    # Test decoding
    decoded_file_name = "decoded_test_file.txt"
    success = decode_file(encoded, decoded_file_name)
    
    if success:
        print(f"Original file content:")
        with open(test_file_path, "r") as f:
            print(f.read())
        
        print(f"Decoded file content:")
        with open(decoded_file_name, "r") as f:
            print(f.read())
    
    # Clean up test files
    os.remove(test_file_path)
    os.remove(decoded_file_name)
