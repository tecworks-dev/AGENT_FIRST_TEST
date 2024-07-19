
"""
Handles performance monitoring and optimization tasks for the AI Software Factory.

This module provides functionality to analyze the performance of projects and suggest
optimizations based on the collected performance data.
"""

import os
import time
import psutil
import tracemalloc
from typing import Dict, Any, List
from flask import current_app
from app.models import Project, PerformanceMetrics
from app.utils.code_analyzer import CodeAnalyzer
from app.utils.code_complexity_analyzer import CodeComplexityAnalyzer
from app.services.data_persistence_service import DataPersistenceService

class PerformanceMonitoringService:
    def __init__(self):
        self.code_analyzer = CodeAnalyzer()
        self.code_complexity_analyzer = CodeComplexityAnalyzer()
        self.data_persistence_service = DataPersistenceService()

    def analyze_performance(self, project_path: str) -> Dict[str, Any]:
        """
        Analyzes the performance of a project.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            Dict[str, Any]: A dictionary containing performance metrics.
        """
        performance_data = {}

        # Measure execution time
        start_time = time.time()
        self._execute_project(project_path)
        execution_time = time.time() - start_time
        performance_data['execution_time'] = execution_time

        # Measure memory usage
        tracemalloc.start()
        self._execute_project(project_path)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        performance_data['memory_usage'] = {
            'current': current / 10**6,  # Convert to MB
            'peak': peak / 10**6  # Convert to MB
        }

        # Measure CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        performance_data['cpu_usage'] = cpu_usage

        # Analyze code complexity
        complexity_report = self.code_complexity_analyzer.generate_complexity_report(project_path)
        performance_data['code_complexity'] = complexity_report

        # Analyze code quality
        code_quality_report = self.code_analyzer.analyze_code_quality(project_path)
        performance_data['code_quality'] = code_quality_report

        return performance_data

    def suggest_optimizations(self, performance_data: Dict[str, Any]) -> List[str]:
        """
        Suggests optimizations based on the performance data.

        Args:
            performance_data (Dict[str, Any]): The performance data collected from analyze_performance.

        Returns:
            List[str]: A list of optimization suggestions.
        """
        suggestions = []

        # Suggest optimizations based on execution time
        if performance_data['execution_time'] > 5:  # Arbitrary threshold
            suggestions.append("Consider optimizing the main execution flow to reduce overall execution time.")

        # Suggest optimizations based on memory usage
        if performance_data['memory_usage']['peak'] > 500:  # Arbitrary threshold (500 MB)
            suggestions.append("High memory usage detected. Consider implementing memory optimization techniques.")

        # Suggest optimizations based on CPU usage
        if performance_data['cpu_usage'] > 80:  # Arbitrary threshold
            suggestions.append("High CPU usage detected. Consider optimizing CPU-intensive operations.")

        # Suggest optimizations based on code complexity
        if performance_data['code_complexity']['average_complexity'] > 10:  # Arbitrary threshold
            suggestions.append("High code complexity detected. Consider refactoring complex functions.")

        # Suggest optimizations based on code quality
        if performance_data['code_quality']['maintainability_index'] < 65:  # Arbitrary threshold
            suggestions.append("Low code maintainability detected. Consider improving code quality and documentation.")

        return suggestions

    def _execute_project(self, project_path: str) -> None:
        """
        Executes the project for performance measurement purposes.

        Args:
            project_path (str): The path to the project directory.
        """
        # This is a placeholder for actual project execution
        # In a real-world scenario, you would implement logic to run the project
        # and collect performance metrics during execution
        pass

    def record_performance_metrics(self, project_id: int, performance_data: Dict[str, Any]) -> None:
        """
        Records performance metrics in the database.

        Args:
            project_id (int): The ID of the project.
            performance_data (Dict[str, Any]): The performance data to be recorded.
        """
        metrics = [
            PerformanceMetrics(
                project_id=project_id,
                metric_name='execution_time',
                metric_value=performance_data['execution_time']
            ),
            PerformanceMetrics(
                project_id=project_id,
                metric_name='memory_usage_peak',
                metric_value=performance_data['memory_usage']['peak']
            ),
            PerformanceMetrics(
                project_id=project_id,
                metric_name='cpu_usage',
                metric_value=performance_data['cpu_usage']
            ),
            PerformanceMetrics(
                project_id=project_id,
                metric_name='code_complexity',
                metric_value=performance_data['code_complexity']['average_complexity']
            ),
            PerformanceMetrics(
                project_id=project_id,
                metric_name='code_maintainability',
                metric_value=performance_data['code_quality']['maintainability_index']
            )
        ]

        self.data_persistence_service.bulk_save(metrics)

    def get_performance_history(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves the performance history for a project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            List[Dict[str, Any]]: A list of performance metrics over time.
        """
        metrics = PerformanceMetrics.query.filter_by(project_id=project_id).order_by(PerformanceMetrics.recorded_at).all()
        return [metric.to_dict() for metric in metrics]

    def generate_performance_report(self, project_id: int) -> str:
        """
        Generates a comprehensive performance report for a project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            str: A formatted performance report.
        """
        project = Project.query.get(project_id)
        if not project:
            return "Project not found."

        performance_history = self.get_performance_history(project_id)
        latest_performance = performance_history[-1] if performance_history else None

        report = f"Performance Report for Project: {project.name}\n\n"

        if latest_performance:
            report += "Latest Performance Metrics:\n"
            for metric, value in latest_performance.items():
                report += f"- {metric}: {value}\n"
        else:
            report += "No performance data available.\n"

        if len(performance_history) > 1:
            report += "\nPerformance Trend:\n"
            for metric in ['execution_time', 'memory_usage_peak', 'cpu_usage', 'code_complexity', 'code_maintainability']:
                values = [record[metric] for record in performance_history if metric in record]
                if values:
                    avg = sum(values) / len(values)
                    trend = "Improving" if values[-1] < avg else "Degrading"
                    report += f"- {metric}: {trend}\n"

        return report

if __name__ == "__main__":
    # This block is for testing purposes only
    DEBUG = True
    if DEBUG:
        service = PerformanceMonitoringService()
        test_project_path = "/path/to/test/project"
        performance_data = service.analyze_performance(test_project_path)
        print("Performance Data:", performance_data)
        suggestions = service.suggest_optimizations(performance_data)
        print("Optimization Suggestions:", suggestions)
