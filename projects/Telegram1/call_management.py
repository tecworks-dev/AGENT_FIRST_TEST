
# call_management.py
"""
This module handles voice and video calling capabilities for the Telegram clone application.
It provides functionality to initiate calls, end calls, and check call status.
"""

import traceback
from flask import current_app
import webrtc
from config import DEBUG

def initiate_call(caller_id, callee_id, call_type):
    """
    Initiates a voice or video call between two users.
    
    Args:
    caller_id (str): The ID of the user initiating the call.
    callee_id (str): The ID of the user receiving the call.
    call_type (str): The type of call ('voice' or 'video').
    
    Returns:
    str: The unique ID of the initiated call, or None if the call failed to initiate.
    """
    try:
        if DEBUG:
            print(f"Initiating {call_type} call from {caller_id} to {callee_id}")
        
        # Initialize WebRTC connection
        connection = webrtc.create_connection()
        
        # Generate a unique call ID
        call_id = webrtc.generate_call_id()
        
        # Set up call parameters based on call type
        if call_type == 'voice':
            connection.enable_audio()
        elif call_type == 'video':
            connection.enable_audio()
            connection.enable_video()
        else:
            raise ValueError("Invalid call type. Must be 'voice' or 'video'.")
        
        # Establish the connection between caller and callee
        success = connection.connect(caller_id, callee_id)
        
        if success:
            if DEBUG:
                print(f"Call initiated successfully. Call ID: {call_id}")
            return call_id
        else:
            if DEBUG:
                print("Failed to initiate call.")
            return None
    
    except Exception as e:
        current_app.logger.error(f"Error in initiate_call: {str(e)}")
        if DEBUG:
            print(f"Error in initiate_call: {str(e)}")
            traceback.print_exc()
        return None

def end_call(call_id):
    """
    Ends an ongoing call.
    
    Args:
    call_id (str): The unique ID of the call to be ended.
    
    Returns:
    bool: True if the call was successfully ended, False otherwise.
    """
    try:
        if DEBUG:
            print(f"Ending call with ID: {call_id}")
        
        # Retrieve the WebRTC connection for the given call ID
        connection = webrtc.get_connection(call_id)
        
        if connection:
            # Terminate the WebRTC connection
            success = connection.terminate()
            
            if success:
                if DEBUG:
                    print(f"Call {call_id} ended successfully.")
                return True
            else:
                if DEBUG:
                    print(f"Failed to end call {call_id}.")
                return False
        else:
            if DEBUG:
                print(f"No active call found with ID: {call_id}")
            return False
    
    except Exception as e:
        current_app.logger.error(f"Error in end_call: {str(e)}")
        if DEBUG:
            print(f"Error in end_call: {str(e)}")
            traceback.print_exc()
        return False

def get_call_status(call_id):
    """
    Retrieves the current status of a call.
    
    Args:
    call_id (str): The unique ID of the call.
    
    Returns:
    str: The status of the call ('active', 'ended', or 'not_found').
    """
    try:
        if DEBUG:
            print(f"Getting status for call ID: {call_id}")
        
        # Retrieve the WebRTC connection for the given call ID
        connection = webrtc.get_connection(call_id)
        
        if connection:
            # Check the connection status
            if connection.is_active():
                status = 'active'
            else:
                status = 'ended'
        else:
            status = 'not_found'
        
        if DEBUG:
            print(f"Call {call_id} status: {status}")
        
        return status
    
    except Exception as e:
        current_app.logger.error(f"Error in get_call_status: {str(e)}")
        if DEBUG:
            print(f"Error in get_call_status: {str(e)}")
            traceback.print_exc()
        return 'error'
