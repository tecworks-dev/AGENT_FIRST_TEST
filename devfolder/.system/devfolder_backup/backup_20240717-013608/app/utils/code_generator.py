
# app/utils/code_generator.py
"""
Utility for generating code snippets and boilerplate.

This module provides a CodeGenerator class with methods to generate class and function templates.
It uses Jinja2 for template rendering, allowing for flexible and customizable code generation.
"""

import jinja2
from typing import List

class CodeGenerator:
    def __init__(self):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('app/templates/code_templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate_class_template(self, class_name: str, attributes: List[str], methods: List[str]) -> str:
        """
        Generate a class template with the given name, attributes, and methods.

        Args:
            class_name (str): The name of the class.
            attributes (List[str]): List of attribute names for the class.
            methods (List[str]): List of method names for the class.

        Returns:
            str: The generated class template as a string.
        """
        template = self.env.get_template('class_template.py.jinja')
        return template.render(class_name=class_name, attributes=attributes, methods=methods)

    def generate_function_template(self, func_name: str, params: List[str], return_type: str) -> str:
        """
        Generate a function template with the given name, parameters, and return type.

        Args:
            func_name (str): The name of the function.
            params (List[str]): List of parameter names for the function.
            return_type (str): The return type of the function.

        Returns:
            str: The generated function template as a string.
        """
        template = self.env.get_template('function_template.py.jinja')
        return template.render(func_name=func_name, params=params, return_type=return_type)

    def _sanitize_input(self, input_str: str) -> str:
        """
        Sanitize input strings to prevent template injection.

        Args:
            input_str (str): The input string to sanitize.

        Returns:
            str: The sanitized input string.
        """
        return jinja2.escape(input_str)

if __name__ == "__main__":
    # Example usage
    generator = CodeGenerator()
    
    # Generate a class template
    class_template = generator.generate_class_template(
        "ExampleClass",
        ["attribute1", "attribute2"],
        ["method1", "method2"]
    )
    print("Generated Class Template:")
    print(class_template)
    
    # Generate a function template
    function_template = generator.generate_function_template(
        "example_function",
        ["param1", "param2"],
        "str"
    )
    print("\nGenerated Function Template:")
    print(function_template)
