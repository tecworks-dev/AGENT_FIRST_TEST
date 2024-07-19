from flask import Flask
from app import create_app
import logging

def main():
    app = create_app()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting the application...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"An error occurred while running the application: {str(e)}")
    finally:
        logger.info("Application stopped.")

if __name__ == '__main__':
    main()