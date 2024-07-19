
import asyncio
import logging
from flask import Flask
from flask_socketio import SocketIO
from app import create_app

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
def main():
    app = create_app()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    socketio = SocketIO(app, async_mode='asyncio')

    async def run_app():
        try:
            logger.info("Starting the application...")
            await socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            logger.error(f"An error occurred while running the application: {str(e)}")
        finally:
            logger.info("Application stopped.")

    async def user_input():
        while True:
            user_in = await asyncio.to_thread(input, "Enter 'q' to quit: ")
            if user_in.strip().lower() == 'q':
                logger.info("User requested to quit.")
                socketio.stop()
                break

    async def main_async():
        await asyncio.gather(run_app(), user_input())

    asyncio.run(main_async())

if __name__ == '__main__':
    main()
