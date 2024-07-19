
/**
 * task.js
 * 
 * This file contains JavaScript functionality specific to task management
 * in the AI Software Factory application.
 */

// Ensure strict mode is enabled
'use strict';

// Task management module
const TaskManager = (function() {
    // Private variables
    let currentTask = null;

    // Private methods
    function updateTaskStatus(taskId, newStatus) {
        return fetch(`/api/tasks/${taskId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        }).then(response => response.json());
    }

    function createSubtask(parentTaskId, subtaskData) {
        return fetch(`/api/tasks/${parentTaskId}/subtasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subtaskData),
        }).then(response => response.json());
    }

    // Public methods
    return {
        initializeTask: function(taskId) {
            fetch(`/api/tasks/${taskId}`)
                .then(response => response.json())
                .then(taskData => {
                    currentTask = taskData;
                    this.renderTaskDetails();
                })
                .catch(error => console.error('Error initializing task:', error));
        },

        renderTaskDetails: function() {
            if (!currentTask) return;

            const taskDetailsElement = document.getElementById('task-details');
            if (taskDetailsElement) {
                taskDetailsElement.innerHTML = `
                    <h2>${currentTask.title}</h2>
                    <p>${currentTask.description}</p>
                    <p>Status: <span id="task-status">${currentTask.status}</span></p>
                    <button onclick="TaskManager.changeStatus('in_progress')">Start Task</button>
                    <button onclick="TaskManager.changeStatus('completed')">Complete Task</button>
                `;
            }
        },

        changeStatus: function(newStatus) {
            if (!currentTask) return;

            updateTaskStatus(currentTask.id, newStatus)
                .then(updatedTask => {
                    currentTask = updatedTask;
                    const statusElement = document.getElementById('task-status');
                    if (statusElement) {
                        statusElement.textContent = updatedTask.status;
                    }
                    console.log(`Task status updated to: ${updatedTask.status}`);
                })
                .catch(error => console.error('Error updating task status:', error));
        },

        addSubtask: function() {
            if (!currentTask) return;

            const subtaskTitle = prompt('Enter subtask title:');
            if (subtaskTitle) {
                createSubtask(currentTask.id, { title: subtaskTitle })
                    .then(newSubtask => {
                        console.log('New subtask created:', newSubtask);
                        // TODO: Update UI to show new subtask
                    })
                    .catch(error => console.error('Error creating subtask:', error));
            }
        },

        requestAIAssistance: function() {
            if (!currentTask) return;

            fetch(`/api/ai-assist/task/${currentTask.id}`)
                .then(response => response.json())
                .then(aiSuggestion => {
                    console.log('AI Suggestion:', aiSuggestion);
                    // TODO: Display AI suggestion in UI
                })
                .catch(error => console.error('Error getting AI assistance:', error));
        }
    };
})();

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const taskId = document.body.dataset.taskId;
    if (taskId) {
        TaskManager.initializeTask(taskId);
    }

    const aiAssistButton = document.getElementById('ai-assist-button');
    if (aiAssistButton) {
        aiAssistButton.addEventListener('click', TaskManager.requestAIAssistance);
    }

    const addSubtaskButton = document.getElementById('add-subtask-button');
    if (addSubtaskButton) {
        addSubtaskButton.addEventListener('click', TaskManager.addSubtask);
    }
});

// Debugging
if (DEBUG) {
    console.log('task.js loaded');
    window.TaskManager = TaskManager; // Expose TaskManager to window for debugging
}
