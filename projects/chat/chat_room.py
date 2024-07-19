
import traceback
from user import User
from message import Message

class ChatRoom:
    def __init__(self, name: str):
        """
        Initializes a chat room.

        Args:
            name (str): The name of the chat room.
        """
        self.name = name
        self.users = set()

    def add_user(self, user: User):
        """
        Adds a user to the room.

        Args:
            user (User): The user to add to the room.
        """
        try:
            self.users.add(user)
            print(f"User {user.username} added to room {self.name}")
        except Exception as e:
            print(f"Error adding user to room: {str(e)}")
            traceback.print_exc()

    def remove_user(self, user: User):
        """
        Removes a user from the room.

        Args:
            user (User): The user to remove from the room.
        """
        try:
            self.users.remove(user)
            print(f"User {user.username} removed from room {self.name}")
        except KeyError:
            print(f"User {user.username} not found in room {self.name}")
        except Exception as e:
            print(f"Error removing user from room: {str(e)}")
            traceback.print_exc()

    def broadcast_message(self, message: Message):
        """
        Broadcasts a message to all users in the room.

        Args:
            message (Message): The message to broadcast.
        """
        try:
            for user in self.users:
                user.send_message(message.to_dict())
            print(f"Message broadcasted in room {self.name}")
        except Exception as e:
            print(f"Error broadcasting message: {str(e)}")
            traceback.print_exc()

    def get_user_list(self):
        """
        Returns a list of usernames in the room.

        Returns:
            list: A list of usernames.
        """
        return [user.username for user in self.users]

    def __str__(self):
        """
        Returns a string representation of the chat room.

        Returns:
            str: A string representation of the chat room.
        """
        return f"ChatRoom: {self.name} (Users: {len(self.users)})"
