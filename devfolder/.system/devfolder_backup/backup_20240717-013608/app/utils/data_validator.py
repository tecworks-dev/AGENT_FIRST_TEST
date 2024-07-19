
# Purpose: Provide data validation utilities for the AI Software Factory application.
# Description: This module contains a DataValidator class that offers methods for
#              validating and sanitizing user input to ensure data integrity and security.

import re
from typing import Dict, Any, Tuple, List
from marshmallow import Schema, fields, validate

class DataValidator:
    """
    A utility class for validating and sanitizing input data.
    """

    def validate_user_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate user input against a given schema.

        Args:
            data (Dict[str, Any]): The input data to validate.
            schema (Dict[str, Any]): The schema to validate against.

        Returns:
            Tuple[bool, List[str]]: A tuple containing a boolean indicating whether the validation
            passed and a list of error messages if any.
        """
        class DynamicSchema(Schema):
            pass

        for field_name, field_type in schema.items():
            setattr(DynamicSchema, field_name, field_type)

        schema_instance = DynamicSchema()
        errors = schema_instance.validate(data)

        if errors:
            return False, [f"{field}: {', '.join(error_msgs)}" for field, error_msgs in errors.items()]
        return True, []

    def sanitize_input(self, input_string: str) -> str:
        """
        Sanitize input string to prevent XSS attacks.

        Args:
            input_string (str): The input string to sanitize.

        Returns:
            str: The sanitized input string.
        """
        # Remove HTML tags
        sanitized = re.sub(r'<[^>]*?>', '', input_string)
        
        # Escape special characters
        sanitized = sanitized.replace('&', '&amp;')
        sanitized = sanitized.replace('<', '&lt;')
        sanitized = sanitized.replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;')
        sanitized = sanitized.replace("'", '&#x27;')
        
        return sanitized

if __name__ == "__main__":
    # Example usage and testing
    validator = DataValidator()

    # Test validate_user_input
    schema = {
        'username': fields.Str(required=True, validate=validate.Length(min=3, max=50)),
        'email': fields.Email(required=True),
        'age': fields.Int(validate=validate.Range(min=18, max=100))
    }

    valid_data = {
        'username': 'johndoe',
        'email': 'john@example.com',
        'age': 30
    }

    invalid_data = {
        'username': 'a',
        'email': 'invalid_email',
        'age': 15
    }

    is_valid, errors = validator.validate_user_input(valid_data, schema)
    print(f"Valid data test - Is valid: {is_valid}, Errors: {errors}")

    is_valid, errors = validator.validate_user_input(invalid_data, schema)
    print(f"Invalid data test - Is valid: {is_valid}, Errors: {errors}")

    # Test sanitize_input
    malicious_input = "<script>alert('XSS');</script>Hello & welcome"
    sanitized = validator.sanitize_input(malicious_input)
    print(f"Sanitized input: {sanitized}")
