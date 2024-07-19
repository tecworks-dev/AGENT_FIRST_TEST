
# Purpose: Initializes utils package.
# Description: This file imports and makes available utility modules for encryption, authentication, and WebSocket operations.

import logging
from .encryption import *
from .auth import *
from .websocket import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug mode
DEBUG = True

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode is enabled in utils/__init__.py")

try:
    logger.info("Utils package initialized successfully")
except Exception as e:
    logger.error(f"Error initializing utils package: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

# Test imports
def test_imports():
    try:
        # Test encryption module
        assert 'encrypt_message' in globals(), "encrypt_message not imported from encryption module"
        assert 'decrypt_message' in globals(), "decrypt_message not imported from encryption module"
        assert 'generate_key' in globals(), "generate_key not imported from encryption module"
        
        # Test auth module
        assert 'generate_2fa_secret' in globals(), "generate_2fa_secret not imported from auth module"
        assert 'verify_2fa' in globals(), "verify_2fa not imported from auth module"
        
        # Test websocket module
        assert 'emit_message' in globals(), "emit_message not imported from websocket module"
        assert 'emit_group_message' in globals(), "emit_group_message not imported from websocket module"
        
        logger.debug("All expected functions are imported correctly")
    except AssertionError as e:
        logger.error(f"Import test failed: {str(e)}")
        raise

if DEBUG:
    test_imports()

# Unittest
import unittest

class TestUtils(unittest.TestCase):
    def test_encryption_imports(self):
        self.assertTrue('encrypt_message' in globals())
        self.assertTrue('decrypt_message' in globals())
        self.assertTrue('generate_key' in globals())

    def test_auth_imports(self):
        self.assertTrue('generate_2fa_secret' in globals())
        self.assertTrue('verify_2fa' in globals())

    def test_websocket_imports(self):
        self.assertTrue('emit_message' in globals())
        self.assertTrue('emit_group_message' in globals())

if __name__ == '__main__':
    unittest.main()
