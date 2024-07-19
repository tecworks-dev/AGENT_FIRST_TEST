
"""
Manages AI models with versioning and rollback capabilities.

This module provides functionality for loading, updating, and rolling back AI models,
as well as managing model versions and metadata.
"""

import os
import json
from typing import Any, Dict, List, Optional
import traceback
from app.utils.custom_exceptions import AIModelException

class AIModelManager:
    def __init__(self, models_directory: str = "app/models"):
        self.models_directory = models_directory
        self.models = {}
        self._load_models()

    def _load_models(self):
        """Initialize the models dictionary with available models and versions."""
        try:
            for model_name in os.listdir(self.models_directory):
                model_path = os.path.join(self.models_directory, model_name)
                if os.path.isdir(model_path):
                    self.models[model_name] = self._get_model_versions(model_path)
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            traceback.print_exc()

    def _get_model_versions(self, model_path: str) -> Dict[str, str]:
        """Get all versions of a specific model."""
        versions = {}
        for version in os.listdir(model_path):
            version_path = os.path.join(model_path, version)
            if os.path.isdir(version_path):
                versions[version] = version_path
        return versions

    def load_model(self, model_name: str, version: str = 'latest') -> Any:
        """
        Load a specific version of an AI model.

        Args:
            model_name (str): Name of the model to load.
            version (str): Version of the model to load. Defaults to 'latest'.

        Returns:
            Any: The loaded model object.

        Raises:
            AIModelException: If the model or version is not found.
        """
        if model_name not in self.models:
            raise AIModelException(f"Model '{model_name}' not found.")

        if version == 'latest':
            version = max(self.models[model_name].keys())

        if version not in self.models[model_name]:
            raise AIModelException(f"Version '{version}' of model '{model_name}' not found.")

        model_path = self.models[model_name][version]
        try:
            # Here you would typically use a library like tensorflow or pytorch to load the model
            # For this example, we'll just return the path
            return model_path
        except Exception as e:
            print(f"Error loading model {model_name} version {version}: {str(e)}")
            traceback.print_exc()
            raise AIModelException(f"Failed to load model '{model_name}' version '{version}'.")

    def update_model(self, model_name: str, new_version: str) -> bool:
        """
        Update a model to a new version.

        Args:
            model_name (str): Name of the model to update.
            new_version (str): New version of the model.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            AIModelException: If the model is not found or the version already exists.
        """
        if model_name not in self.models:
            raise AIModelException(f"Model '{model_name}' not found.")

        if new_version in self.models[model_name]:
            raise AIModelException(f"Version '{new_version}' of model '{model_name}' already exists.")

        try:
            new_model_path = os.path.join(self.models_directory, model_name, new_version)
            os.makedirs(new_model_path, exist_ok=True)
            self.models[model_name][new_version] = new_model_path
            return True
        except Exception as e:
            print(f"Error updating model {model_name} to version {new_version}: {str(e)}")
            traceback.print_exc()
            return False

    def rollback_model(self, model_name: str, target_version: str) -> bool:
        """
        Roll back a model to a previous version.

        Args:
            model_name (str): Name of the model to roll back.
            target_version (str): Target version to roll back to.

        Returns:
            bool: True if the rollback was successful, False otherwise.

        Raises:
            AIModelException: If the model or target version is not found.
        """
        if model_name not in self.models:
            raise AIModelException(f"Model '{model_name}' not found.")

        if target_version not in self.models[model_name]:
            raise AIModelException(f"Target version '{target_version}' of model '{model_name}' not found.")

        try:
            # Here you would typically implement the rollback logic
            # For this example, we'll just print a message
            print(f"Rolling back model '{model_name}' to version '{target_version}'")
            return True
        except Exception as e:
            print(f"Error rolling back model {model_name} to version {target_version}: {str(e)}")
            traceback.print_exc()
            return False

    def list_model_versions(self, model_name: str) -> List[str]:
        """
        List all available versions of a model.

        Args:
            model_name (str): Name of the model.

        Returns:
            List[str]: List of available versions.

        Raises:
            AIModelException: If the model is not found.
        """
        if model_name not in self.models:
            raise AIModelException(f"Model '{model_name}' not found.")

        return list(self.models[model_name].keys())

    def get_model_metadata(self, model_name: str, version: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a specific model version.

        Args:
            model_name (str): Name of the model.
            version (str): Version of the model.

        Returns:
            Dict[str, Any]: Metadata of the model.

        Raises:
            AIModelException: If the model or version is not found.
        """
        if model_name not in self.models:
            raise AIModelException(f"Model '{model_name}' not found.")

        if version not in self.models[model_name]:
            raise AIModelException(f"Version '{version}' of model '{model_name}' not found.")

        model_path = self.models[model_name][version]
        metadata_file = os.path.join(model_path, 'metadata.json')

        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            return metadata
        except FileNotFoundError:
            return {"error": "Metadata file not found"}
        except json.JSONDecodeError:
            return {"error": "Invalid metadata file format"}
        except Exception as e:
            print(f"Error reading metadata for model {model_name} version {version}: {str(e)}")
            traceback.print_exc()
            return {"error": "Failed to read metadata"}

if __name__ == "__main__":
    # Example usage
    model_manager = AIModelManager()
    
    try:
        model = model_manager.load_model("example_model", "latest")
        print(f"Loaded model: {model}")

        versions = model_manager.list_model_versions("example_model")
        print(f"Available versions: {versions}")

        metadata = model_manager.get_model_metadata("example_model", versions[0])
        print(f"Model metadata: {metadata}")

        update_success = model_manager.update_model("example_model", "new_version")
        print(f"Model update success: {update_success}")

        rollback_success = model_manager.rollback_model("example_model", versions[0])
        print(f"Model rollback success: {rollback_success}")
    except AIModelException as e:
        print(f"AIModelException: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
