
# Purpose: Detects the programming language of a given code snippet.
# Description: This module provides a LanguageDetector class that uses the pygments library
# to guess the programming language of a given code snippet.

import traceback
from pygments.lexers import guess_lexer

class LanguageDetector:
    def __init__(self):
        pass

    def detect_language(self, code: str) -> str:
        """
        Detects the programming language of a given code snippet.

        Args:
            code (str): The code snippet to analyze.

        Returns:
            str: The detected programming language.

        Raises:
            Exception: If there's an error during language detection.
        """
        try:
            lexer = guess_lexer(code)
            return lexer.name
        except Exception as e:
            error_msg = f"Error detecting language: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return "Unknown"

# Debugging statements
if __name__ == "__main__":
    DEBUG = True
    
    if DEBUG:
        print("Debug mode: Testing LanguageDetector")
        
        detector = LanguageDetector()
        
        # Test cases
        python_code = """
def hello_world():
    print("Hello, World!")
"""
        
        javascript_code = """
function helloWorld() {
    console.log("Hello, World!");
}
"""
        
        unknown_code = """
This is not a programming language.
"""
        
        print("Detecting Python:", detector.detect_language(python_code))
        print("Detecting JavaScript:", detector.detect_language(javascript_code))
        print("Detecting Unknown:", detector.detect_language(unknown_code))
