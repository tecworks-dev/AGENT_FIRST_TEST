
"""
Defines various Flask routes for the application.
This module contains route handlers for different endpoints of the AI Software Factory application.
"""

from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import User, Project, Task
from app.services import (
    AIService, ProjectManager, TaskManager, FileManager,
    WebBrowsingService, StateMonitoringService
)
from app.utils.error_handler import handle_error
import traceback

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route('/')
@login_required
def index():
    """Home page route"""
    try:
        projects = ProjectManager().get_user_projects(current_user.id)
        return render_template('index.html', projects=projects)
    except Exception as e:
        return handle_error(e)

@routes.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    """User profile page"""
    try:
        user = User.query.get_or_404(user_id)
        if user != current_user and not current_user.is_admin:
            abort(403)
        return render_template('user_profile.html', user=user)
    except Exception as e:
        return handle_error(e)

@routes.route('/project/create', methods=['POST'])
@login_required
def create_project():
    """Creates a new project"""
    try:
        data = request.json
        project = ProjectManager().create_project(
            name=data['name'],
            description=data['description'],
            user_id=current_user.id
        )
        return jsonify(project.to_dict()), 201
    except Exception as e:
        return handle_error(e)

@routes.route('/task/<int:task_id>/update', methods=['PATCH'])
@login_required
def update_task(task_id):
    """Updates task status"""
    try:
        data = request.json
        task = TaskManager().update_task(task_id, status=data['status'])
        return jsonify(task.to_dict())
    except Exception as e:
        return handle_error(e)

@routes.route('/browse', methods=['POST'])
@login_required
def browse_web():
    """Initiates web browsing for research"""
    try:
        data = request.json
        results = WebBrowsingService().search(data['query'])
        return jsonify(results)
    except Exception as e:
        return handle_error(e)

@routes.route('/project/<int:project_id>/state')
@login_required
def get_project_state(project_id):
    """Gets the current state of a project"""
    try:
        project = Project.query.get_or_404(project_id)
        if project.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        state = StateMonitoringService().get_current_state(project_id)
        return jsonify(state)
    except Exception as e:
        return handle_error(e)

@routes.route('/ai/generate', methods=['POST'])
@login_required
def generate_code():
    """Generates code using AI"""
    try:
        data = request.json
        code = AIService().generate_code(data['prompt'])
        return jsonify({'code': code})
    except Exception as e:
        return handle_error(e)

@routes.route('/project/<int:project_id>/files')
@login_required
def get_project_files(project_id):
    """Gets all files for a project"""
    try:
        project = Project.query.get_or_404(project_id)
        if project.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        files = FileManager().get_project_files(project_id)
        return jsonify([file.to_dict() for file in files])
    except Exception as e:
        return handle_error(e)

@routes.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@routes.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    print("This module should not be run directly. Please run main.py instead.")
