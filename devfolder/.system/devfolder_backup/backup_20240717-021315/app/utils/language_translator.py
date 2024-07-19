
"""
Implements code translation between programming languages.

This module provides functionality to translate code from one programming language to another
and detect the language of a given code snippet.
"""

import re
from typing import Dict, Any
from pygments.lexers import guess_lexer
from app.utils.api_utils import AsyncAnthropic
import os

class LanguageTranslator:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def translate_code(self, code: str, from_language: str, to_language: str) -> str:
        """
        Translates code from one programming language to another.

        Args:
            code (str): The source code to translate.
            from_language (str): The source programming language.
            to_language (str): The target programming language.

        Returns:
            str: The translated code in the target language.
        """
        prompt = f"""
        Translate the following {from_language} code to {to_language}:

        {code}

        Translated {to_language} code:
        """

        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            translated_code = response.content[0].text.strip()
            return translated_code
        except Exception as e:
            print(f"Error in translate_code: {str(e)}")
            return ""

    def detect_language(self, code: str) -> str:
        """
        Detects the programming language of a given code snippet.

        Args:
            code (str): The code snippet to analyze.

        Returns:
            str: The detected programming language.
        """
        try:
            lexer = guess_lexer(code)
            return lexer.name
        except Exception as e:
            print(f"Error in detect_language: {str(e)}")
            return "Unknown"

import unittest

class TestLanguageTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = LanguageTranslator()

    def test_detect_language(self):
        python_code = "def hello_world():\n    print('Hello, World!')"
        java_code = "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"

        self.assertEqual(self.translator.detect_language(python_code), "Python")
        self.assertEqual(self.translator.detect_language(java_code), "Java")

    async def test_translate_code(self):
        python_code = "def factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)"
        expected_java_code = """
public class Factorial {
    public static int factorial(int n) {
        return n == 0 ? 1 : n * factorial(n - 1);
    }
}
"""
        translated_code = await self.translator.translate_code(python_code, "Python", "Java")
        self.assertIn("public class", translated_code)
        self.assertIn("public static int factorial", translated_code)

if __name__ == "__main__":
    unittest.main()
