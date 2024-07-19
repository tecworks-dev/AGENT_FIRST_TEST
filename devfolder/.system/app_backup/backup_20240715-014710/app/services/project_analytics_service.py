
# Purpose: Provides analytics and insights for projects.
# Description: This service calculates various metrics, generates reports, and predicts project completion dates.

from typing import Dict, Any
from datetime import datetime, timedelta
from app.models import Project, Task
from app.utils.data_validator import DataValidator
from sqlalchemy import func
import logging
import traceback

class ProjectAnalyticsService:
    def __init__(self):
        self.data_validator = DataValidator()

    def calculate_project_metrics(self, project_id: int) -> Dict[str, Any]:
        """
        Calculate various metrics for a given project.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            total_tasks = Task.query.filter_by(project_id=project_id).count()
            completed_tasks = Task.query.filter_by(project_id=project_id, status='completed').count()
            open_tasks = total_tasks - completed_tasks
            
            if total_tasks > 0:
                completion_percentage = (completed_tasks / total_tasks) * 100
            else:
                completion_percentage = 0

            avg_task_duration = (
                Task.query.filter_by(project_id=project_id, status='completed')
                .with_entities(func.avg(Task.updated_at - Task.created_at))
                .scalar()
            )

            if avg_task_duration:
                avg_task_duration = avg_task_duration.total_seconds() / 3600  # Convert to hours

            return {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "open_tasks": open_tasks,
                "completion_percentage": round(completion_percentage, 2),
                "avg_task_duration": round(avg_task_duration, 2) if avg_task_duration else None
            }
        except Exception as e:
            logging.error(f"Error calculating project metrics: {str(e)}")
            logging.error(traceback.format_exc())
            return {}

    def generate_project_report(self, project_id: int) -> str:
        """
        Generate a comprehensive report for a given project.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            metrics = self.calculate_project_metrics(project_id)
            
            report = f"Project Report for: {project.name}\n"
            report += f"Description: {project.description}\n\n"
            report += f"Total Tasks: {metrics['total_tasks']}\n"
            report += f"Completed Tasks: {metrics['completed_tasks']}\n"
            report += f"Open Tasks: {metrics['open_tasks']}\n"
            report += f"Completion Percentage: {metrics['completion_percentage']}%\n"
            
            if metrics['avg_task_duration']:
                report += f"Average Task Duration: {metrics['avg_task_duration']} hours\n"
            
            report += f"\nProject Started: {project.created_at}\n"
            report += f"Last Updated: {project.updated_at}\n"
            
            predicted_completion = self.predict_project_completion(project_id)
            report += f"\nPredicted Completion Date: {predicted_completion}\n"

            return report
        except Exception as e:
            logging.error(f"Error generating project report: {str(e)}")
            logging.error(traceback.format_exc())
            return "Error generating project report"

    def predict_project_completion(self, project_id: int) -> datetime:
        """
        Predict the completion date for a given project based on current progress and task durations.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            metrics = self.calculate_project_metrics(project_id)
            
            if metrics['total_tasks'] == 0 or metrics['completed_tasks'] == 0:
                return datetime.now() + timedelta(days=30)  # Default prediction if no data

            avg_task_duration = metrics['avg_task_duration'] or 24  # Default to 24 hours if None
            remaining_tasks = metrics['open_tasks']
            
            total_remaining_hours = avg_task_duration * remaining_tasks
            days_to_completion = total_remaining_hours / 24  # Assuming 8-hour workdays
            
            predicted_completion = datetime.now() + timedelta(days=days_to_completion)
            
            return predicted_completion
        except Exception as e:
            logging.error(f"Error predicting project completion: {str(e)}")
            logging.error(traceback.format_exc())
            return datetime.now() + timedelta(days=30)  # Return a default date in case of error

if __name__ == "__main__":
    # This block is for testing purposes only
    pass
