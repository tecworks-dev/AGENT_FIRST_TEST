
# Purpose: Generates visualizations for project data and metrics.
# Description: This service provides methods to create various charts and graphs
# for visualizing project progress, code quality, and performance trends.

from typing import Dict, Any
import matplotlib.pyplot as plt
import io
import base64
from app.models import Project, Task, File, PerformanceMetrics
from app.utils.code_analyzer import CodeAnalyzer
from sqlalchemy import func
from datetime import datetime, timedelta

class DataVisualizationService:
    def __init__(self):
        self.code_analyzer = CodeAnalyzer()

    def generate_project_progress_chart(self, project_id: int) -> bytes:
        """
        Generates a line chart showing project progress over time.
        
        :param project_id: The ID of the project
        :return: PNG image data as bytes
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        tasks = Task.query.filter_by(project_id=project_id).all()
        dates = [task.created_at.date() for task in tasks]
        completed_tasks = [task.status == 'completed' for task in tasks]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, completed_tasks, marker='o')
        plt.title(f"Project Progress: {project.name}")
        plt.xlabel("Date")
        plt.ylabel("Completed Tasks")
        plt.ylim(0, max(completed_tasks) + 1)

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        return img_buffer.getvalue()

    def generate_code_quality_heatmap(self, project_id: int) -> bytes:
        """
        Generates a heatmap visualizing code quality across project files.
        
        :param project_id: The ID of the project
        :return: PNG image data as bytes
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        files = File.query.filter_by(project_id=project_id).all()
        file_names = [file.name for file in files]
        complexity_scores = []

        for file in files:
            analysis = self.code_analyzer.analyze_complexity(file.content)
            complexity_scores.append(analysis['cyclomatic_complexity'])

        plt.figure(figsize=(12, 8))
        plt.imshow([complexity_scores], cmap='YlOrRd', aspect='auto')
        plt.colorbar(label='Cyclomatic Complexity')
        plt.title(f"Code Quality Heatmap: {project.name}")
        plt.yticks([])
        plt.xticks(range(len(file_names)), file_names, rotation=45, ha='right')

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        
        return img_buffer.getvalue()

    def generate_performance_trend_graph(self, project_id: int) -> bytes:
        """
        Generates a line graph showing performance trends over time.
        
        :param project_id: The ID of the project
        :return: PNG image data as bytes
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        metrics = PerformanceMetrics.query.filter_by(project_id=project_id).order_by(PerformanceMetrics.recorded_at).all()
        
        dates = [metric.recorded_at for metric in metrics]
        response_times = [metric.metric_value for metric in metrics if metric.metric_name == 'response_time']
        cpu_usage = [metric.metric_value for metric in metrics if metric.metric_name == 'cpu_usage']
        memory_usage = [metric.metric_value for metric in metrics if metric.metric_name == 'memory_usage']

        plt.figure(figsize=(12, 6))
        plt.plot(dates, response_times, label='Response Time (ms)', marker='o')
        plt.plot(dates, cpu_usage, label='CPU Usage (%)', marker='s')
        plt.plot(dates, memory_usage, label='Memory Usage (MB)', marker='^')
        
        plt.title(f"Performance Trends: {project.name}")
        plt.xlabel("Date")
        plt.ylabel("Metric Value")
        plt.legend()
        plt.grid(True)

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        
        return img_buffer.getvalue()

    def _convert_to_base64(self, image_bytes: bytes) -> str:
        """
        Converts image bytes to base64 string for embedding in HTML.
        
        :param image_bytes: The image data as bytes
        :return: Base64 encoded string
        """
        return base64.b64encode(image_bytes).decode('utf-8')

if __name__ == "__main__":
    # This block is for testing purposes only
    from app import create_app, db
    app = create_app()
    with app.app_context():
        vis_service = DataVisualizationService()
        
        # Example usage
        project_id = 1  # Assume a project with ID 1 exists
        progress_chart = vis_service.generate_project_progress_chart(project_id)
        quality_heatmap = vis_service.generate_code_quality_heatmap(project_id)
        performance_graph = vis_service.generate_performance_trend_graph(project_id)
        
        # Convert to base64 for embedding in HTML
        progress_chart_b64 = vis_service._convert_to_base64(progress_chart)
        quality_heatmap_b64 = vis_service._convert_to_base64(quality_heatmap)
        performance_graph_b64 = vis_service._convert_to_base64(performance_graph)
        
        print("Charts generated successfully.")
        print(f"Progress Chart: <img src='data:image/png;base64,{progress_chart_b64}' />")
        print(f"Quality Heatmap: <img src='data:image/png;base64,{quality_heatmap_b64}' />")
        print(f"Performance Graph: <img src='data:image/png;base64,{performance_graph_b64}' />")
