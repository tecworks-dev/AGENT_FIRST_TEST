import asyncio
import traceback
from server import ChatServer
from config import SERVER_HOST, SERVER_PORT

async def main():
    """
    Main function to start the chat server and run the application.
    """
    try:
        # Create a new ChatServer instance
        chat_server = ChatServer()

        # Start the server
        await chat_server.start(SERVER_HOST, SERVER_PORT)

    except KeyboardInterrupt:
        # Handle graceful shutdown on keyboard interrupt
        print("\nShutting down the chat server...")
    except Exception as e:
        # Log any errors that occur during execution
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
    finally:
        # Perform any necessary cleanup
        print("Chat server has been shut down.")

if __name__ == "__main__":
    asyncio.run(main())