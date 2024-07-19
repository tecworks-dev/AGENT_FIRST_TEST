
# group_management.py
# Purpose: Handles creation and management of group chats and channels.
# Description: This module provides functions to create groups, add members, and remove members from groups.

import traceback
from flask import current_app
from database import get_db_connection
from utils import generate_unique_id
from config import DEBUG

def create_group(creator_id, group_name, members):
    """
    Create a new group chat or channel.
    
    Args:
    - creator_id (int): The ID of the user creating the group
    - group_name (str): The name of the group
    - members (list): List of user IDs to be added to the group
    
    Returns:
    - int: The ID of the newly created group, or None if creation fails
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        group_id = generate_unique_id()
        
        # Insert the new group into the database
        cursor.execute("""
            INSERT INTO groups (id, name, creator_id)
            VALUES (?, ?, ?)
        """, (group_id, group_name, creator_id))
        
        # Add members to the group
        for member_id in members:
            cursor.execute("""
                INSERT INTO group_members (group_id, user_id)
                VALUES (?, ?)
            """, (group_id, member_id))
        
        db.commit()
        
        if DEBUG:
            print(f"Group '{group_name}' created with ID: {group_id}")
        
        return group_id
    except Exception as e:
        db.rollback()
        if DEBUG:
            print(f"Error creating group: {str(e)}")
            traceback.print_exc()
        return None
    finally:
        cursor.close()
        db.close()

def add_member(group_id, user_id):
    """
    Add a member to an existing group.
    
    Args:
    - group_id (int): The ID of the group
    - user_id (int): The ID of the user to be added
    
    Returns:
    - bool: True if the member was added successfully, False otherwise
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Check if the user is already a member of the group
        cursor.execute("""
            SELECT COUNT(*) FROM group_members
            WHERE group_id = ? AND user_id = ?
        """, (group_id, user_id))
        
        if cursor.fetchone()[0] > 0:
            if DEBUG:
                print(f"User {user_id} is already a member of group {group_id}")
            return False
        
        # Add the user to the group
        cursor.execute("""
            INSERT INTO group_members (group_id, user_id)
            VALUES (?, ?)
        """, (group_id, user_id))
        
        db.commit()
        
        if DEBUG:
            print(f"User {user_id} added to group {group_id}")
        
        return True
    except Exception as e:
        db.rollback()
        if DEBUG:
            print(f"Error adding member to group: {str(e)}")
            traceback.print_exc()
        return False
    finally:
        cursor.close()
        db.close()

def remove_member(group_id, user_id):
    """
    Remove a member from an existing group.
    
    Args:
    - group_id (int): The ID of the group
    - user_id (int): The ID of the user to be removed
    
    Returns:
    - bool: True if the member was removed successfully, False otherwise
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Check if the user is a member of the group
        cursor.execute("""
            SELECT COUNT(*) FROM group_members
            WHERE group_id = ? AND user_id = ?
        """, (group_id, user_id))
        
        if cursor.fetchone()[0] == 0:
            if DEBUG:
                print(f"User {user_id} is not a member of group {group_id}")
            return False
        
        # Remove the user from the group
        cursor.execute("""
            DELETE FROM group_members
            WHERE group_id = ? AND user_id = ?
        """, (group_id, user_id))
        
        db.commit()
        
        if DEBUG:
            print(f"User {user_id} removed from group {group_id}")
        
        return True
    except Exception as e:
        db.rollback()
        if DEBUG:
            print(f"Error removing member from group: {str(e)}")
            traceback.print_exc()
        return False
    finally:
        cursor.close()
        db.close()

if DEBUG:
    print("group_management.py loaded")
