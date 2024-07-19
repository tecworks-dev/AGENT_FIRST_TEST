
/**
 * project.js
 * This file contains JavaScript functionality specific to project management and interactions.
 */

// Debug mode flag
const DEBUG = true;

// Function to log debug messages
function debugLog(message) {
    if (DEBUG) {
        console.log(`[DEBUG] ${message}`);
    }
}

// Project class to manage project-related operations
class Project {
    constructor(id, name, description) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.tasks = [];
    }

    addTask(task) {
        this.tasks.push(task);
        debugLog(`Task added to project ${this.name}: ${task.title}`);
    }

    removeTask(taskId) {
        const index = this.tasks.findIndex(task => task.id === taskId);
        if (index !== -1) {
            this.tasks.splice(index, 1);
            debugLog(`Task removed from project ${this.name}: ${taskId}`);
        }
    }

    updateTask(taskId, updates) {
        const task = this.tasks.find(task => task.id === taskId);
        if (task) {
            Object.assign(task, updates);
            debugLog(`Task updated in project ${this.name}: ${taskId}`);
        }
    }
}

// Function to create a new project
async function createProject(name, description) {
    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, description }),
        });

        if (!response.ok) {
            throw new Error('Failed to create project');
        }

        const data = await response.json();
        debugLog(`Project created: ${data.name}`);
        return new Project(data.id, data.name, data.description);
    } catch (error) {
        console.error('Error creating project:', error);
        throw error;
    }
}

// Function to load project details
async function loadProject(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}`);
        if (!response.ok) {
            throw new Error('Failed to load project');
        }

        const data = await response.json();
        debugLog(`Project loaded: ${data.name}`);
        return new Project(data.id, data.name, data.description);
    } catch (error) {
        console.error('Error loading project:', error);
        throw error;
    }
}

// Function to update project details
async function updateProject(projectId, updates) {
    try {
        const response = await fetch(`/api/projects/${projectId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates),
        });

        if (!response.ok) {
            throw new Error('Failed to update project');
        }

        const data = await response.json();
        debugLog(`Project updated: ${data.name}`);
        return new Project(data.id, data.name, data.description);
    } catch (error) {
        console.error('Error updating project:', error);
        throw error;
    }
}

// Function to delete a project
async function deleteProject(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete project');
        }

        debugLog(`Project deleted: ${projectId}`);
        return true;
    } catch (error) {
        console.error('Error deleting project:', error);
        throw error;
    }
}

// Function to load project tasks
async function loadProjectTasks(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}/tasks`);
        if (!response.ok) {
            throw new Error('Failed to load project tasks');
        }

        const data = await response.json();
        debugLog(`Project tasks loaded: ${data.length} tasks`);
        return data;
    } catch (error) {
        console.error('Error loading project tasks:', error);
        throw error;
    }
}

// Function to update the project dashboard
function updateProjectDashboard(project) {
    const dashboardElement = document.getElementById('project-dashboard');
    if (dashboardElement) {
        dashboardElement.innerHTML = `
            <h2>${project.name}</h2>
            <p>${project.description}</p>
            <div id="task-list"></div>
        `;
        updateTaskList(project.tasks);
    }
}

// Function to update the task list
function updateTaskList(tasks) {
    const taskListElement = document.getElementById('task-list');
    if (taskListElement) {
        taskListElement.innerHTML = tasks.map(task => `
            <div class="task-item" data-task-id="${task.id}">
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <span class="task-status">${task.status}</span>
            </div>
        `).join('');
    }
}

// Event listener for project creation form
document.addEventListener('DOMContentLoaded', () => {
    const projectForm = document.getElementById('project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const name = document.getElementById('project-name').value;
            const description = document.getElementById('project-description').value;
            try {
                const project = await createProject(name, description);
                updateProjectDashboard(project);
            } catch (error) {
                console.error('Failed to create project:', error);
                alert('Failed to create project. Please try again.');
            }
        });
    }
});

// Export functions and classes for use in other modules
export {
    Project,
    createProject,
    loadProject,
    updateProject,
    deleteProject,
    loadProjectTasks,
    updateProjectDashboard,
    updateTaskList
};
