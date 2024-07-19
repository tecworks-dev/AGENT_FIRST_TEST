import asyncio

class User:
    """
    Represents a chat user in the application.

    Attributes:
        username (str): The user's chosen username.
        reader (asyncio.StreamReader): The StreamReader for receiving messages.
        writer (asyncio.StreamWriter): The StreamWriter for sending messages.
    """

    def __init__(self, username: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Initializes a User instance.

        Args:
            username (str): The user's chosen username.
            reader (asyncio.StreamReader): The StreamReader for receiving messages.
            writer (asyncio.StreamWriter): The StreamWriter for sending messages.
        """
        self.username = username
        self.reader = reader
        self.writer = writer

    async def send_message(self, message: str):
        """
        Sends a message to the user through their StreamWriter.

        Args:
            message (str): The message to be sent to the user.
        """
        try:
            self.writer.write(message.encode() + b'\n')
            await self.writer.drain()
        except Exception as e:
            # Log the error to the console
            print(f"Error sending message to {self.username}: {str(e)}")
            # You might want to handle this error further, e.g., by notifying the server
            # that this user's connection might be broken