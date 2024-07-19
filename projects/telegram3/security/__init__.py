"""
Security measures initialization.

This module initializes security-related components for the messaging platform.
It sets up various security measures to ensure secure communication and protect user data.
"""

import traceback
import logging
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

# Initialize security components
csrf = CSRFProtect()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)

def init_security(app):
    """
    Initializes security-related components for the Flask application.

    This function sets up various security measures such as CSRF protection,
    secure headers, and content security policy.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    try:
        # Implement CSRF protection
        csrf.init_app(app)

        # Set secure headers
        Talisman(app, content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",
            'style-src': "'self' 'unsafe-inline'",
        })

        # Implement rate limiting
        limiter.init_app(app)

        # Set up SSL/TLS configuration
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['REMEMBER_COOKIE_SECURE'] = True

        # Implement proper password hashing
        bcrypt.init_app(app)

        if DEBUG:
            logger.debug("Security components initialized successfully.")

        logger.info("Security measures have been initialized.")
    except Exception as e:
        logger.error(f"Error initializing security components: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())

# Additional security-related functions
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)