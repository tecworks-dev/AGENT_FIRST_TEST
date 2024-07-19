# Purpose: Manages individual and group messaging capabilities
# Description: This module provides functionality for sending messages and creating group chats

import traceback
from typing import List
from encryption.crypto import EncryptionManager

DEBUG = True

class MessagingManager:
    def __init__(self, encryption_manager: EncryptionManager):
        self.encryption_manager = encryption_manager
        self.groups = {}  # Dictionary to store group information

    def send_message(self, sender: str, recipient: str, content: str) -> bool:
        """
        Send an encrypted message from sender to recipient.

        Args:
            sender (str): The username of the message sender
            recipient (str): The username of the message recipient
            content (str): The content of the message

        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        try:
            # Encrypt the message content
            encrypted_content = self.encryption_manager.encrypt(content.encode())

            # TODO: Implement actual message sending logic (e.g., through a network layer)
            # For now, we'll just simulate sending by printing to console
            if DEBUG:
                print(f"Sending encrypted message from {sender} to {recipient}")
                print(f"Encrypted content: {encrypted_content}")

            # In a real implementation, you would send the encrypted_content to the recipient
            # and return True only if the sending was successful

            return True
        except Exception as e:
            if DEBUG:
                print(f"Error in send_message: {str(e)}")
                traceback.print_exc()
            return False

    def create_group(self, name: str, members: List[str]) -> str:
        """
        Create a new group chat.

        Args:
            name (str): The name of the group
            members (List[str]): List of usernames to be added to the group

        Returns:
            str: The unique identifier for the created group, or an empty string if creation failed
        """
        try:
            # Generate a unique group ID (in a real implementation, this should be more robust)
            group_id = f"group_{len(self.groups) + 1}"

            # Store group information
            self.groups[group_id] = {
                "name": name,
                "members": members
            }

            if DEBUG:
                print(f"Created group '{name}' with ID {group_id}")
                print(f"Group members: {', '.join(members)}")

            return group_id
        except Exception as e:
            if DEBUG:
                print(f"Error in create_group: {str(e)}")
                traceback.print_exc()
            return ""

    def send_group_message(self, sender: str, group_id: str, content: str) -> bool:
        """
        Send a message to a group.

        Args:
            sender (str): The username of the message sender
            group_id (str): The unique identifier of the group
            content (str): The content of the message

        Returns:
            bool: True if the message was sent successfully to all group members, False otherwise
        """
        try:
            if group_id not in self.groups:
                if DEBUG:
                    print(f"Group with ID {group_id} does not exist")
                return False

            group = self.groups[group_id]
            success = True

            for member in group["members"]:
                if member != sender:
                    if not self.send_message(sender, member, content):
                        success = False

            if DEBUG:
                print(f"Group message sent to '{group['name']}' (ID: {group_id}) by {sender}")

            return success
        except Exception as e:
            if DEBUG:
                print(f"Error in send_group_message: {str(e)}")
                traceback.print_exc()
            return False

# Example usage and testing (if this module is run directly)
if __name__ == "__main__":
    encryption_manager = EncryptionManager()
    messaging_manager = MessagingManager(encryption_manager)

    # Test sending a direct message
    result = messaging_manager.send_message("alice", "bob", "Hello, Bob!")
    print(f"Direct message sent: {result}")

    # Test creating a group
    group_id = messaging_manager.create_group("Friends", ["alice", "bob", "charlie"])
    print(f"Group created with ID: {group_id}")

    # Test sending a group message
    if group_id:
        result = messaging_manager.send_group_message("alice", group_id, "Hello, friends!")
        print(f"Group message sent: {result}")