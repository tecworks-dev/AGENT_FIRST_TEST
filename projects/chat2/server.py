import asyncio
import traceback
from chat_room import ChatRoom
from user import User
from message import Message
from encryption import encrypt, decrypt, generate_key

class ChatServer:
    def __init__(self):
        """
        Initializes server attributes
        """
        self.clients = set()
        self.chat_rooms = {}
        self.encryption_key = None  # We'll generate this when starting the server

    async def start(self, host, port):
        """
        Starts the TCP server
        """
        try:
            self.encryption_key = generate_key()
            server = await asyncio.start_server(self.handle_connection, host, port)
            print(f"Server started on {host}:{port}")
            async with server:
                await server.serve_forever()
        except Exception as e:
            print(f"Error starting server: {str(e)}")
            traceback.print_exc()

    async def handle_connection(self, reader, writer):
        """
        Handles new TCP connections
        """
        try:
            # Add the new client to our set of clients
            self.clients.add(writer)
            
            # Wait for the client to send their username
            username = (await reader.readline()).decode().strip()
            user = User(username, reader, writer)
            
            print(f"New connection from {username}")
            
            # Add the user to a default chat room (you might want to implement room selection later)
            if 'default' not in self.chat_rooms:
                self.chat_rooms['default'] = ChatRoom('default')
            self.chat_rooms['default'].add_user(user)
            
            try:
                while True:
                    message = await reader.readline()
                    if not message:
                        break
                    
                    # Decrypt the incoming message
                    decrypted_message = decrypt(message.decode().strip(), self.encryption_key)
                    
                    # Create a Message object
                    msg = Message(decrypted_message, username)
                    
                    # Broadcast the message to all clients in the room
                    await self.broadcast(msg.to_dict(), username)
            finally:
                # When the connection is closed, remove the client
                self.clients.remove(writer)
                self.chat_rooms['default'].remove_user(user)
                writer.close()
                await writer.wait_closed()
                print(f"Connection closed for {username}")
        except Exception as e:
            print(f"Error handling connection: {str(e)}")
            traceback.print_exc()

    async def broadcast(self, message: dict, sender: str):
        """
        Broadcasts messages to all connected clients
        """
        try:
            if self.clients:
                # Encrypt the message before broadcasting
                encrypted_message = encrypt(str(message), self.encryption_key)
                for writer in self.clients:
                    if not writer.is_closing():
                        writer.write(encrypted_message.encode() + b'\n')
                        await writer.drain()
        except Exception as e:
            print(f"Error broadcasting message: {str(e)}")
            traceback.print_exc()

# Note: This file doesn't need a main function as it will be imported and used by main.py