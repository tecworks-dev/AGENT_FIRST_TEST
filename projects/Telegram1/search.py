
# search.py
# Purpose: Implements inline search functionality across messages and contacts.
# Description: This module provides functions to search through messages and contacts
# for a given user, as well as a global search function that combines both.

import traceback
from flask import current_app
from database import get_user_messages, get_user_contacts

DEBUG = True  # Set to False in production

def search_messages(user_id, query):
    """
    Search through user's messages for a given query.

    Args:
    user_id (int): The ID of the user performing the search.
    query (str): The search query string.

    Returns:
    list: A list of message dictionaries that match the query.
    """
    try:
        messages = get_user_messages(user_id)
        results = [msg for msg in messages if query.lower() in msg['content'].lower()]
        
        if DEBUG:
            print(f"Search messages results for user {user_id}: {len(results)} matches")
        
        return results
    except Exception as e:
        current_app.logger.error(f"Error in search_messages: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return []

def search_contacts(user_id, query):
    """
    Search through user's contacts for a given query.

    Args:
    user_id (int): The ID of the user performing the search.
    query (str): The search query string.

    Returns:
    list: A list of contact dictionaries that match the query.
    """
    try:
        contacts = get_user_contacts(user_id)
        results = [contact for contact in contacts if query.lower() in contact['name'].lower() or query.lower() in contact['username'].lower()]
        
        if DEBUG:
            print(f"Search contacts results for user {user_id}: {len(results)} matches")
        
        return results
    except Exception as e:
        current_app.logger.error(f"Error in search_contacts: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return []

def search_global(user_id, query):
    """
    Perform a global search across messages and contacts for a given query.

    Args:
    user_id (int): The ID of the user performing the search.
    query (str): The search query string.

    Returns:
    dict: A dictionary containing lists of matching messages and contacts.
    """
    try:
        message_results = search_messages(user_id, query)
        contact_results = search_contacts(user_id, query)
        
        results = {
            'messages': message_results,
            'contacts': contact_results
        }
        
        if DEBUG:
            print(f"Global search results for user {user_id}: {len(message_results)} messages, {len(contact_results)} contacts")
        
        return results
    except Exception as e:
        current_app.logger.error(f"Error in search_global: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return {'messages': [], 'contacts': []}

# Additional helper functions can be added here if needed

if DEBUG:
    print("search.py module loaded successfully")
