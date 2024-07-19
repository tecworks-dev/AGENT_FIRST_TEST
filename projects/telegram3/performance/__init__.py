# performance/__init__.py
"""
Performance optimization initialization.
This module initializes performance-related components for the application.
"""

import traceback
import logging
from flask_caching import Cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

# Initialize cache
cache = Cache()

def init_performance(app):
    """
    Initializes performance-related components.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    try:
        if DEBUG:
            logger.info("Initializing performance components...")

        # Set up caching mechanisms
        cache.init_app(app, config={'CACHE_TYPE': 'simple'})

        # Configure database query optimizations
        app.config['SQLALCHEMY_ECHO'] = DEBUG  # Log SQL queries in debug mode

        # Implement request rate limiting
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        limiter = Limiter(app, key_func=get_remote_address)

        # Set up asynchronous task processing
        from celery import Celery
        app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
        app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
        celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)

        if DEBUG:
            logger.info("Performance components initialized successfully.")

    except Exception as e:
        logger.error(f"Error initializing performance components: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())

    if DEBUG:
        logger.info("Performance initialization complete.")