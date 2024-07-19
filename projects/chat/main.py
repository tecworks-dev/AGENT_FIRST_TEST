import asyncio
import traceback
import logging
from server import ChatServer
from config import SERVER_HOST, SERVER_PORT

def print_access_information():
    """
    Prints access information to the terminal at startup.
    """
    print("=" * 50)
    print("Chat Server Access Information")
    print("=" * 50)
    print(f"Server Host: {SERVER_HOST}")
    print(f"Server Port: {SERVER_PORT}")
    print("=" * 50)
    print("To connect to the server, use a compatible chat client")
    print("and connect to the above host and port.")
    print("=" * 50)

async def run_server():
    """
    Coroutine to run the chat server.
    """
    chat_server = ChatServer()
    await chat_server.start(SERVER_HOST, SERVER_PORT)

def main():
    """
    Main function to start the chat server and run the application.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        print_access_information()
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logging.info("\nShutting down the chat server...")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error("Traceback:")
        logging.error(traceback.format_exc())
    finally:
        logging.info("Chat server has been shut down.")

if __name__ == "__main__":
    main()