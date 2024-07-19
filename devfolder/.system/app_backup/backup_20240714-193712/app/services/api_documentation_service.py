
# Purpose: Generates API documentation for the project.
# Description: This service provides methods to generate and update API documentation
# based on the project structure and code.

from typing import List, Dict, Any
import os
import ast
import re
from app.models import Project
from app.utils.code_parser import CodeParser
from app.utils.api_utils import AsyncAnthropic
from app import db

class APIDocumentationService:
    def __init__(self):
        self.code_parser = CodeParser()
        self.ai_client = AsyncAnthropic()

    async def generate_api_docs(self, project_id: int) -> str:
        """
        Generates API documentation for the specified project.

        Args:
            project_id (int): The ID of the project to generate documentation for.

        Returns:
            str: The generated API documentation in Markdown format.
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")

        api_routes = self._extract_api_routes(project)
        models = self._extract_models(project)

        documentation = "# API Documentation\n\n"
        documentation += self._generate_routes_documentation(api_routes)
        documentation += "\n\n"
        documentation += self._generate_models_documentation(models)

        return documentation

    async def update_api_docs(self, project_id: int, changes: List[Dict[str, Any]]) -> bool:
        """
        Updates the API documentation for the specified project based on the provided changes.

        Args:
            project_id (int): The ID of the project to update documentation for.
            changes (List[Dict[str, Any]]): A list of changes to apply to the documentation.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")

        current_docs = await self.generate_api_docs(project_id)
        updated_docs = self._apply_changes_to_docs(current_docs, changes)

        # Save the updated documentation to the project
        project.api_documentation = updated_docs
        db.session.commit()

        return True

    def _extract_api_routes(self, project: Project) -> List[Dict[str, Any]]:
        """
        Extracts API routes from the project's route files.

        Args:
            project (Project): The project to extract routes from.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing route information.
        """
        routes = []
        for file in project.files:
            if file.name.endswith('.py') and 'routes' in file.name:
                tree = ast.parse(file.content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        route_info = self._extract_route_info(node)
                        if route_info:
                            routes.append(route_info)
        return routes

    def _extract_route_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extracts route information from an AST node.

        Args:
            node (ast.FunctionDef): The AST node representing a route function.

        Returns:
            Dict[str, Any]: A dictionary containing route information.
        """
        route_info = {
            'name': node.name,
            'methods': [],
            'path': '',
            'description': ast.get_docstring(node) or ''
        }

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and decorator.func.attr == 'route':
                route_info['path'] = decorator.args[0].s
                if len(decorator.args) > 1:
                    route_info['methods'] = [m.s for m in decorator.args[1].elts]

        return route_info

    def _extract_models(self, project: Project) -> List[Dict[str, Any]]:
        """
        Extracts model information from the project's model files.

        Args:
            project (Project): The project to extract models from.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing model information.
        """
        models = []
        for file in project.files:
            if file.name.endswith('.py') and 'models' in file.name:
                tree = ast.parse(file.content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        model_info = self._extract_model_info(node)
                        if model_info:
                            models.append(model_info)
        return models

    def _extract_model_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extracts model information from an AST node.

        Args:
            node (ast.ClassDef): The AST node representing a model class.

        Returns:
            Dict[str, Any]: A dictionary containing model information.
        """
        model_info = {
            'name': node.name,
            'attributes': [],
            'description': ast.get_docstring(node) or ''
        }

        for child in node.body:
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                attr_name = child.target.id
                attr_type = self._get_type_hint(child.annotation)
                model_info['attributes'].append({'name': attr_name, 'type': attr_type})

        return model_info

    def _get_type_hint(self, annotation: ast.AST) -> str:
        """
        Extracts the type hint from an AST annotation.

        Args:
            annotation (ast.AST): The AST node representing a type annotation.

        Returns:
            str: A string representation of the type hint.
        """
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            return f"{annotation.value.id}[{self._get_type_hint(annotation.slice.value)}]"
        return "Any"

    def _generate_routes_documentation(self, routes: List[Dict[str, Any]]) -> str:
        """
        Generates documentation for API routes.

        Args:
            routes (List[Dict[str, Any]]): A list of dictionaries containing route information.

        Returns:
            str: The generated route documentation in Markdown format.
        """
        docs = "## API Routes\n\n"
        for route in routes:
            docs += f"### {route['name']}\n\n"
            docs += f"**Path:** `{route['path']}`\n\n"
            docs += f"**Methods:** {', '.join(route['methods'])}\n\n"
            docs += f"**Description:** {route['description']}\n\n"
        return docs

    def _generate_models_documentation(self, models: List[Dict[str, Any]]) -> str:
        """
        Generates documentation for data models.

        Args:
            models (List[Dict[str, Any]]): A list of dictionaries containing model information.

        Returns:
            str: The generated model documentation in Markdown format.
        """
        docs = "## Data Models\n\n"
        for model in models:
            docs += f"### {model['name']}\n\n"
            docs += f"{model['description']}\n\n"
            docs += "**Attributes:**\n\n"
            for attr in model['attributes']:
                docs += f"- `{attr['name']}`: {attr['type']}\n"
            docs += "\n"
        return docs

    def _apply_changes_to_docs(self, current_docs: str, changes: List[Dict[str, Any]]) -> str:
        """
        Applies changes to the current API documentation.

        Args:
            current_docs (str): The current API documentation.
            changes (List[Dict[str, Any]]): A list of changes to apply.

        Returns:
            str: The updated API documentation.
        """
        for change in changes:
            if change['type'] == 'add':
                current_docs = self._add_section(current_docs, change['section'], change['content'])
            elif change['type'] == 'update':
                current_docs = self._update_section(current_docs, change['section'], change['content'])
            elif change['type'] == 'delete':
                current_docs = self._delete_section(current_docs, change['section'])

        return current_docs

    def _add_section(self, docs: str, section: str, content: str) -> str:
        """
        Adds a new section to the documentation.

        Args:
            docs (str): The current documentation.
            section (str): The section to add.
            content (str): The content of the new section.

        Returns:
            str: The updated documentation.
        """
        return f"{docs}\n\n## {section}\n\n{content}"

    def _update_section(self, docs: str, section: str, content: str) -> str:
        """
        Updates an existing section in the documentation.

        Args:
            docs (str): The current documentation.
            section (str): The section to update.
            content (str): The new content for the section.

        Returns:
            str: The updated documentation.
        """
        pattern = re.compile(f"## {re.escape(section)}.*?(?=\n\n## |$)", re.DOTALL)
        return pattern.sub(f"## {section}\n\n{content}", docs)

    def _delete_section(self, docs: str, section: str) -> str:
        """
        Deletes a section from the documentation.

        Args:
            docs (str): The current documentation.
            section (str): The section to delete.

        Returns:
            str: The updated documentation.
        """
        pattern = re.compile(f"## {re.escape(section)}.*?(?=\n\n## |$)", re.DOTALL)
        return pattern.sub("", docs)

# Debug statements
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("APIDocumentationService loaded successfully")
