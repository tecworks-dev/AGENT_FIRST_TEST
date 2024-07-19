
"""
app/utils/dependency_graph.py

This file implements dependency graph functionality for the AI Software Factory project.
It provides a DependencyGraph class that can generate a graph representation of project dependencies.

The graph is created using the networkx library, which allows for easy manipulation and analysis of graph structures.
"""

import networkx as nx
from typing import Dict, Any
from app.models import Project, File
from app import db

class DependencyGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def generate_graph(self, project_id: int) -> nx.Graph:
        """
        Generates a dependency graph for a given project.

        Args:
            project_id (int): The ID of the project to generate the graph for.

        Returns:
            nx.Graph: A networkx Graph object representing the project's dependency structure.
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")

        files = File.query.filter_by(project_id=project_id).all()

        for file in files:
            self.graph.add_node(file.name, type='file')
            self._analyze_file_dependencies(file)

        return self.graph

    def _analyze_file_dependencies(self, file: File):
        """
        Analyzes a file's content to determine its dependencies and adds them to the graph.

        Args:
            file (File): The file object to analyze.
        """
        # This is a simple implementation. In a real-world scenario, you'd want to use
        # language-specific parsers to accurately determine dependencies.
        import_lines = [line.strip() for line in file.content.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]

        for line in import_lines:
            if line.startswith('import'):
                module = line.split('import')[1].strip()
            else:  # line.startswith('from')
                module = line.split('import')[0].split('from')[1].strip()

            # Add the dependency to the graph
            self.graph.add_node(module, type='module')
            self.graph.add_edge(file.name, module)

    def get_dependencies(self, file_name: str) -> Dict[str, Any]:
        """
        Returns the dependencies for a given file.

        Args:
            file_name (str): The name of the file to get dependencies for.

        Returns:
            Dict[str, Any]: A dictionary containing the file's dependencies.
        """
        if file_name not in self.graph:
            return {}

        dependencies = list(self.graph.neighbors(file_name))
        return {
            'file': file_name,
            'dependencies': dependencies
        }

    def get_dependent_files(self, module_name: str) -> Dict[str, Any]:
        """
        Returns the files that depend on a given module.

        Args:
            module_name (str): The name of the module to get dependent files for.

        Returns:
            Dict[str, Any]: A dictionary containing the files that depend on the module.
        """
        if module_name not in self.graph:
            return {}

        dependent_files = [node for node in self.graph.neighbors(module_name) if self.graph.nodes[node]['type'] == 'file']
        return {
            'module': module_name,
            'dependent_files': dependent_files
        }

    def export_graph(self, format: str = 'adjacency') -> Any:
        """
        Exports the graph in the specified format.

        Args:
            format (str): The format to export the graph in. Default is 'adjacency'.

        Returns:
            Any: The graph representation in the specified format.
        """
        if format == 'adjacency':
            return nx.to_dict_of_dicts(self.graph)
        elif format == 'edge_list':
            return list(self.graph.edges())
        else:
            raise ValueError(f"Unsupported export format: {format}")

if __name__ == "__main__":
    # This block is for testing purposes and will only run if the script is executed directly
    import unittest

    class TestDependencyGraph(unittest.TestCase):
        def setUp(self):
            self.graph = DependencyGraph()

        def test_generate_graph(self):
            # Mock a project and files
            project = type('Project', (), {'id': 1})
            file1 = type('File', (), {'name': 'file1.py', 'content': 'import module1\nfrom module2 import function', 'project_id': 1})
            file2 = type('File', (), {'name': 'file2.py', 'content': 'import module3', 'project_id': 1})

            # Mock the database queries
            Project.query.get = lambda x: project if x == 1 else None
            File.query.filter_by = lambda project_id: [file1, file2] if project_id == 1 else []

            self.graph.generate_graph(1)

            self.assertIn('file1.py', self.graph.graph)
            self.assertIn('file2.py', self.graph.graph)
            self.assertIn('module1', self.graph.graph)
            self.assertIn('module2', self.graph.graph)
            self.assertIn('module3', self.graph.graph)

        def test_get_dependencies(self):
            self.graph.graph.add_edge('file1.py', 'module1')
            self.graph.graph.add_edge('file1.py', 'module2')

            deps = self.graph.get_dependencies('file1.py')
            self.assertEqual(deps['file'], 'file1.py')
            self.assertIn('module1', deps['dependencies'])
            self.assertIn('module2', deps['dependencies'])

        def test_get_dependent_files(self):
            self.graph.graph.add_node('file1.py', type='file')
            self.graph.graph.add_node('file2.py', type='file')
            self.graph.graph.add_node('module1', type='module')
            self.graph.graph.add_edge('file1.py', 'module1')
            self.graph.graph.add_edge('file2.py', 'module1')

            deps = self.graph.get_dependent_files('module1')
            self.assertEqual(deps['module'], 'module1')
            self.assertIn('file1.py', deps['dependent_files'])
            self.assertIn('file2.py', deps['dependent_files'])

    unittest.main()
