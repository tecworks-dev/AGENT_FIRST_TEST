
# Purpose: Handle media sharing routes for the messaging platform
# Description: This file contains route definitions for media uploading, retrieval, and deletion

from flask import Blueprint, request, jsonify
from app.services.media import MediaService
import traceback

media_bp = Blueprint('media', __name__)

@media_bp.route('/media', methods=['POST'])
def upload_media():
    """
    Handle media upload
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400

        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        result = MediaService.upload_media(int(user_id), file)
        return jsonify(result), 201

    except Exception as e:
        if __debug__:
            print(f"Error in upload_media: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while uploading the media'}), 500

@media_bp.route('/media/<int:media_id>', methods=['GET'])
def get_media(media_id):
    """
    Retrieve media by ID
    """
    try:
        result = MediaService.get_media(media_id)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Media not found'}), 404

    except Exception as e:
        if __debug__:
            print(f"Error in get_media: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while retrieving the media'}), 500

@media_bp.route('/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    """
    Delete media by ID
    """
    try:
        result = MediaService.delete_media(media_id)
        if result:
            return jsonify({'message': 'Media deleted successfully'}), 200
        else:
            return jsonify({'error': 'Media not found or could not be deleted'}), 404

    except Exception as e:
        if __debug__:
            print(f"Error in delete_media: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while deleting the media'}), 500

if __debug__:
    print("Media routes loaded")
