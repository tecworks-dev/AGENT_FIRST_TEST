
from datetime import datetime

class Message:
    """
    Represents a chat message in the application.

    Attributes:
        content (str): The content of the message.
        sender (str): The username of the message sender.
        timestamp (datetime): The time when the message was created.
    """

    def __init__(self, content: str, sender: str):
        """
        Initializes a new Message instance.

        Args:
            content (str): The content of the message.
            sender (str): The username of the message sender.
        """
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now()

    def to_dict(self):
        """
        Converts the Message instance to a dictionary for easy serialization.

        Returns:
            dict: A dictionary representation of the Message.
        """
        return {
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self):
        """
        Returns a string representation of the Message.

        Returns:
            str: A formatted string containing message details.
        """
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.sender}: {self.content}"

    def __repr__(self):
        """
        Returns a string representation of the Message for debugging purposes.

        Returns:
            str: A string representation of the Message instance.
        """
        return f"Message(content='{self.content}', sender='{self.sender}', timestamp='{self.timestamp}')"
