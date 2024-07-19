"""
Purpose: Handles encrypted file sharing functionality.
Description: This module provides a FileSharingManager class that manages the upload and download
of encrypted files. It uses the EncryptionManager for end-to-end encryption of files.
"""

import os
import uuid
import traceback
from typing import Optional
from encryption.crypto import EncryptionManager

DEBUG = True

class FileSharingManager:
    def __init__(self, encryption_manager: EncryptionManager):
        self.encryption_manager = encryption_manager
        self.file_storage_path = "shared_files"  # Directory to store encrypted files
        
        # Ensure the file storage directory exists
        if not os.path.exists(self.file_storage_path):
            os.makedirs(self.file_storage_path)
        
        if DEBUG:
            print(f"FileSharingManager initialized. Storage path: {self.file_storage_path}")

    def upload_file(self, user: str, file_path: str) -> Optional[str]:
        """
        Encrypts and uploads a file to the shared storage.
        
        Args:
            user (str): The username of the uploader.
            file_path (str): The path to the file to be uploaded.
        
        Returns:
            str: A unique file ID for the uploaded file, or None if upload fails.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read the file content
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Encrypt the file content
            encrypted_content = self.encryption_manager.encrypt(file_content)

            # Generate a unique file ID
            file_id = str(uuid.uuid4())

            # Save the encrypted file
            encrypted_file_path = os.path.join(self.file_storage_path, file_id)
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_content)

            if DEBUG:
                print(f"File uploaded successfully. User: {user}, File ID: {file_id}")

            return file_id

        except Exception as e:
            if DEBUG:
                print(f"Error uploading file: {str(e)}")
                traceback.print_exc()
            return None

    def download_file(self, user: str, file_id: str) -> Optional[bytes]:
        """
        Downloads and decrypts a file from the shared storage.
        
        Args:
            user (str): The username of the downloader.
            file_id (str): The unique ID of the file to be downloaded.
        
        Returns:
            bytes: The decrypted file content, or None if download fails.
        """
        try:
            encrypted_file_path = os.path.join(self.file_storage_path, file_id)
            
            if not os.path.exists(encrypted_file_path):
                raise FileNotFoundError(f"File not found: {file_id}")

            # Read the encrypted file content
            with open(encrypted_file_path, 'rb') as encrypted_file:
                encrypted_content = encrypted_file.read()

            # Decrypt the file content
            decrypted_content = self.encryption_manager.decrypt(encrypted_content)

            if DEBUG:
                print(f"File downloaded successfully. User: {user}, File ID: {file_id}")

            return decrypted_content

        except Exception as e:
            if DEBUG:
                print(f"Error downloading file: {str(e)}")
                traceback.print_exc()
            return None

# Example usage (for demonstration purposes)
if __name__ == "__main__":
    encryption_manager = EncryptionManager()
    file_sharing = FileSharingManager(encryption_manager)
    
    # Upload a file
    uploaded_file_id = file_sharing.upload_file("alice", "example.txt")
    if uploaded_file_id:
        print(f"File uploaded with ID: {uploaded_file_id}")
        
        # Download the file
        downloaded_content = file_sharing.download_file("bob", uploaded_file_id)
        if downloaded_content:
            print(f"Downloaded file content: {downloaded_content.decode('utf-8')}")
        else:
            print("File download failed")
    else:
        print("File upload failed")