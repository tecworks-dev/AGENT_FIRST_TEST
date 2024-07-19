
"""
Purpose: Implements code obfuscation functionality for security purposes.
Description: This module provides a CodeObfuscator class that can obfuscate and deobfuscate
             code in various programming languages to enhance security and protect intellectual property.
"""

import ast
import random
import string
import traceback

DEBUG = True

class CodeObfuscator:
    def __init__(self):
        self.obfuscation_map = {}
        self.deobfuscation_map = {}

    def obfuscate_code(self, code: str, language: str) -> str:
        """
        Obfuscates the given code based on the specified programming language.

        Args:
            code (str): The original code to be obfuscated.
            language (str): The programming language of the code.

        Returns:
            str: The obfuscated code.
        """
        try:
            if language.lower() == 'python':
                return self._obfuscate_python(code)
            else:
                raise NotImplementedError(f"Obfuscation for {language} is not implemented yet.")
        except Exception as e:
            if DEBUG:
                print(f"Error in obfuscate_code: {str(e)}")
                print(traceback.format_exc())
            return code  # Return original code if obfuscation fails

    def deobfuscate_code(self, obfuscated_code: str, language: str) -> str:
        """
        Deobfuscates the given code based on the specified programming language.

        Args:
            obfuscated_code (str): The obfuscated code to be deobfuscated.
            language (str): The programming language of the code.

        Returns:
            str: The deobfuscated code.
        """
        try:
            if language.lower() == 'python':
                return self._deobfuscate_python(obfuscated_code)
            else:
                raise NotImplementedError(f"Deobfuscation for {language} is not implemented yet.")
        except Exception as e:
            if DEBUG:
                print(f"Error in deobfuscate_code: {str(e)}")
                print(traceback.format_exc())
            return obfuscated_code  # Return obfuscated code if deobfuscation fails

    def _obfuscate_python(self, code: str) -> str:
        tree = ast.parse(code)
        obfuscator = self._PythonObfuscator()
        obfuscated_tree = obfuscator.visit(tree)
        self.obfuscation_map = obfuscator.obfuscation_map
        self.deobfuscation_map = {v: k for k, v in self.obfuscation_map.items()}
        return ast.unparse(obfuscated_tree)

    def _deobfuscate_python(self, obfuscated_code: str) -> str:
        tree = ast.parse(obfuscated_code)
        deobfuscator = self._PythonDeobfuscator(self.deobfuscation_map)
        deobfuscated_tree = deobfuscator.visit(tree)
        return ast.unparse(deobfuscated_tree)

    class _PythonObfuscator(ast.NodeTransformer):
        def __init__(self):
            self.obfuscation_map = {}

        def visit_Name(self, node):
            if node.id not in self.obfuscation_map:
                obfuscated_name = self._generate_obfuscated_name()
                self.obfuscation_map[node.id] = obfuscated_name
            node.id = self.obfuscation_map[node.id]
            return node

        def _generate_obfuscated_name(self):
            return ''.join(random.choices(string.ascii_letters, k=10))

    class _PythonDeobfuscator(ast.NodeTransformer):
        def __init__(self, deobfuscation_map):
            self.deobfuscation_map = deobfuscation_map

        def visit_Name(self, node):
            if node.id in self.deobfuscation_map:
                node.id = self.deobfuscation_map[node.id]
            return node

if DEBUG:
    # Example usage and debugging
    obfuscator = CodeObfuscator()
    original_code = """
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
"""
    print("Original code:")
    print(original_code)

    obfuscated_code = obfuscator.obfuscate_code(original_code, 'python')
    print("\nObfuscated code:")
    print(obfuscated_code)

    deobfuscated_code = obfuscator.deobfuscate_code(obfuscated_code, 'python')
    print("\nDeobfuscated code:")
    print(deobfuscated_code)

    assert original_code.strip() == deobfuscated_code.strip(), "Deobfuscation failed to recover the original code"
    print("\nAssertion passed: Original code matches deobfuscated code")
