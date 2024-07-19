
import os
import traceback
from flask import current_app, send_file
from werkzeug.utils import secure_filename
from database import execute_query
from encryption import encrypt_file, decrypt_file

def upload_file(user_id, file):
    """
    Handles file upload and storage.

    Args:
        user_id (int): ID of the user uploading the file.
        file (FileStorage): File object to be uploaded.

    Returns:
        dict: Information about the uploaded file, including file_id.
    """
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        # Encrypt the file
        encrypted_file_path = encrypt_file(file_path, current_app.config['ENCRYPTION_KEY'])
        
        # Remove the original unencrypted file
        os.remove(file_path)
        
        # Store file information in the database
        query = """
        INSERT INTO files (user_id, filename, file_path)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        result = execute_query(query, (user_id, filename, encrypted_file_path))
        file_id = result[0]['id']
        
        return {
            'file_id': file_id,
            'filename': filename,
            'message': 'File uploaded successfully'
        }
    except Exception as e:
        current_app.logger.error(f"Error uploading file: {traceback.format_exc()}")
        return {'error': 'File upload failed'}

def share_file(file_id, sender_id, recipient_id):
    """
    Shares a file with another user.

    Args:
        file_id (int): ID of the file to be shared.
        sender_id (int): ID of the user sharing the file.
        recipient_id (int): ID of the user receiving the file.

    Returns:
        dict: Information about the shared file.
    """
    try:
        # Check if the file exists and belongs to the sender
        query = "SELECT * FROM files WHERE id = %s AND user_id = %s"
        result = execute_query(query, (file_id, sender_id))
        
        if not result:
            return {'error': 'File not found or you do not have permission to share it'}
        
        file_info = result[0]
        
        # Share the file
        query = """
        INSERT INTO shared_files (file_id, sender_id, recipient_id)
        VALUES (%s, %s, %s)
        """
        execute_query(query, (file_id, sender_id, recipient_id))
        
        return {
            'message': 'File shared successfully',
            'file_id': file_id,
            'filename': file_info['filename']
        }
    except Exception as e:
        current_app.logger.error(f"Error sharing file: {traceback.format_exc()}")
        return {'error': 'File sharing failed'}

def retrieve_shared_files(user_id):
    """
    Retrieves shared files for a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        list: List of shared files for the user.
    """
    try:
        query = """
        SELECT f.id, f.filename, sf.sender_id, u.username as sender_name
        FROM shared_files sf
        JOIN files f ON sf.file_id = f.id
        JOIN users u ON sf.sender_id = u.id
        WHERE sf.recipient_id = %s
        """
        result = execute_query(query, (user_id,))
        
        shared_files = []
        for row in result:
            shared_files.append({
                'file_id': row['id'],
                'filename': row['filename'],
                'sender_id': row['sender_id'],
                'sender_name': row['sender_name']
            })
        
        return shared_files
    except Exception as e:
        current_app.logger.error(f"Error retrieving shared files: {traceback.format_exc()}")
        return {'error': 'Failed to retrieve shared files'}

def download_file(file_id, user_id):
    """
    Downloads a file for a user.

    Args:
        file_id (int): ID of the file to be downloaded.
        user_id (int): ID of the user downloading the file.

    Returns:
        FileResponse: The file to be downloaded.
    """
    try:
        # Check if the user has access to the file
        query = """
        SELECT f.* FROM files f
        LEFT JOIN shared_files sf ON f.id = sf.file_id
        WHERE f.id = %s AND (f.user_id = %s OR sf.recipient_id = %s)
        """
        result = execute_query(query, (file_id, user_id, user_id))
        
        if not result:
            return {'error': 'File not found or you do not have permission to download it'}
        
        file_info = result[0]
        
        # Decrypt the file
        decrypted_file_path = decrypt_file(file_info['file_path'], current_app.config['ENCRYPTION_KEY'])
        
        # Send the file
        return send_file(decrypted_file_path, as_attachment=True, attachment_filename=file_info['filename'])
    except Exception as e:
        current_app.logger.error(f"Error downloading file: {traceback.format_exc()}")
        return {'error': 'File download failed'}
