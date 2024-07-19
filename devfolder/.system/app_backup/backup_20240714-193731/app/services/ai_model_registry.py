
"""
Manages different AI models used in the application.

This module provides a registry for AI models, allowing for easy management
and retrieval of various models used throughout the application.
"""

from typing import Any, List, Dict
import os
import json
import logging

class AIModelRegistry:
    """
    A registry for managing AI models used in the application.
    """

    def __init__(self):
        self.models: Dict[str, str] = {}
        self.registry_file = 'ai_model_registry.json'
        self.load_registry()

    def load_registry(self) -> None:
        """Load the model registry from a file if it exists."""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    self.models = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Error decoding {self.registry_file}. Starting with an empty registry.")
        else:
            logging.info(f"{self.registry_file} not found. Starting with an empty registry.")

    def save_registry(self) -> None:
        """Save the current state of the model registry to a file."""
        with open(self.registry_file, 'w') as f:
            json.dump(self.models, f)

    def register_model(self, model_name: str, model_path: str) -> bool:
        """
        Register a new AI model or update an existing one.

        Args:
            model_name (str): The name of the model.
            model_path (str): The path to the model file or directory.

        Returns:
            bool: True if the model was successfully registered, False otherwise.
        """
        if not os.path.exists(model_path):
            logging.error(f"Model path does not exist: {model_path}")
            return False

        self.models[model_name] = model_path
        self.save_registry()
        logging.info(f"Model '{model_name}' registered successfully.")
        return True

    def get_model(self, model_name: str) -> Any:
        """
        Retrieve a registered AI model.

        Args:
            model_name (str): The name of the model to retrieve.

        Returns:
            Any: The loaded model object, or None if the model is not found.
        """
        if model_name not in self.models:
            logging.warning(f"Model '{model_name}' not found in registry.")
            return None

        model_path = self.models[model_name]
        try:
            # Here you would typically load the model using the appropriate method
            # For example, if using TensorFlow:
            # import tensorflow as tf
            # return tf.keras.models.load_model(model_path)
            
            # For demonstration, we'll just return the path
            return model_path
        except Exception as e:
            logging.error(f"Error loading model '{model_name}': {str(e)}")
            return None

    def list_models(self) -> List[str]:
        """
        List all registered models.

        Returns:
            List[str]: A list of names of all registered models.
        """
        return list(self.models.keys())

    def remove_model(self, model_name: str) -> bool:
        """
        Remove a model from the registry.

        Args:
            model_name (str): The name of the model to remove.

        Returns:
            bool: True if the model was successfully removed, False otherwise.
        """
        if model_name not in self.models:
            logging.warning(f"Model '{model_name}' not found in registry.")
            return False

        del self.models[model_name]
        self.save_registry()
        logging.info(f"Model '{model_name}' removed from registry.")
        return True

if __name__ == "__main__":
    # Example usage
    registry = AIModelRegistry()
    
    # Register a model
    registry.register_model("text_classification", "/path/to/text_classification_model")
    
    # List all models
    print("Registered models:", registry.list_models())
    
    # Get a model
    model = registry.get_model("text_classification")
    if model:
        print("Model path:", model)
    
    # Remove a model
    registry.remove_model("text_classification")
    
    print("Updated registered models:", registry.list_models())
