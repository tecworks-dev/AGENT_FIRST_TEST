from flask import Blueprint, request, jsonify
from app.services.search import SearchService
from flask_login import current_user, login_required

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    """
    Handle GET requests for search functionality
    """
    try:
        query = request.args.get('query', '')
        user_id = current_user.id

        if not query:
            return jsonify({'error': 'Missing query parameter'}), 400

        search_service = SearchService()
        
        # Search for messages
        messages = search_service.search_messages(user_id, query)
        
        # Search for media
        media = search_service.search_media(user_id, query)

        results = {
            'messages': messages,
            'media': media
        }

        return jsonify(results), 200

    except Exception as e:
        error_message = f"An error occurred during search: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500