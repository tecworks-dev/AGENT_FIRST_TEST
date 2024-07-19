
/**
 * Main JavaScript file for the frontend.
 * This file handles Flask components for the UI, WebSocket connection setup,
 * API calls to the backend, and state management.
 */

// Debug mode
const DEBUG = true;

// State management
let appState = {
    currentUser: null,
    currentProject: null,
    tasks: [],
    aiChatHistory: []
};

// WebSocket connection setup
let socket;

document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    setupEventListeners();
    initializeUI();
});

function initializeWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws`);

    socket.onopen = (event) => {
        if (DEBUG) console.log('WebSocket connection established');
        socket.send(JSON.stringify({ type: 'authenticate', token: getAuthToken() }));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    socket.onclose = (event) => {
        if (DEBUG) console.log('WebSocket connection closed');
        // Attempt to reconnect after a delay
        setTimeout(initializeWebSocket, 5000);
    };
}

function setupEventListeners() {
    document.getElementById('createProjectBtn').addEventListener('click', createProject);
    document.getElementById('createTaskBtn').addEventListener('click', createTask);
    document.getElementById('aiChatInput').addEventListener('keypress', handleAIChatInput);
}

function initializeUI() {
    fetchCurrentUser();
    fetchProjects();
    updateTaskList();
}

// API calls to the backend

async function fetchCurrentUser() {
    try {
        const response = await fetch('/api/user');
        if (response.ok) {
            appState.currentUser = await response.json();
            updateUserInfo();
        } else {
            throw new Error('Failed to fetch user info');
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
    }
}

async function fetchProjects() {
    try {
        const response = await fetch('/api/projects');
        if (response.ok) {
            const projects = await response.json();
            updateProjectList(projects);
        } else {
            throw new Error('Failed to fetch projects');
        }
    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}

async function createProject() {
    const projectName = document.getElementById('projectName').value;
    const projectDescription = document.getElementById('projectDescription').value;

    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: projectName, description: projectDescription }),
        });

        if (response.ok) {
            const newProject = await response.json();
            appState.currentProject = newProject;
            updateProjectList([...appState.projects, newProject]);
        } else {
            throw new Error('Failed to create project');
        }
    } catch (error) {
        console.error('Error creating project:', error);
    }
}

async function createTask() {
    const taskTitle = document.getElementById('taskTitle').value;
    const taskDescription = document.getElementById('taskDescription').value;

    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: taskTitle,
                description: taskDescription,
                project_id: appState.currentProject.id
            }),
        });

        if (response.ok) {
            const newTask = await response.json();
            appState.tasks.push(newTask);
            updateTaskList();
        } else {
            throw new Error('Failed to create task');
        }
    } catch (error) {
        console.error('Error creating task:', error);
    }
}

// UI update functions

function updateUserInfo() {
    const userInfoElement = document.getElementById('userInfo');
    userInfoElement.textContent = `Welcome, ${appState.currentUser.username}!`;
}

function updateProjectList(projects) {
    const projectListElement = document.getElementById('projectList');
    projectListElement.innerHTML = '';

    projects.forEach(project => {
        const projectElement = document.createElement('div');
        projectElement.className = 'project-item';
        projectElement.textContent = project.name;
        projectElement.addEventListener('click', () => selectProject(project));
        projectListElement.appendChild(projectElement);
    });
}

function selectProject(project) {
    appState.currentProject = project;
    updateTaskList();
}

function updateTaskList() {
    const taskListElement = document.getElementById('taskList');
    taskListElement.innerHTML = '';

    appState.tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item';
        taskElement.textContent = task.title;
        taskListElement.appendChild(taskElement);
    });
}

// WebSocket message handling

function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'task_update':
            updateTask(data.task);
            break;
        case 'project_update':
            updateProject(data.project);
            break;
        case 'ai_response':
            handleAIResponse(data.message);
            break;
        default:
            if (DEBUG) console.log('Unknown message type:', data.type);
    }
}

function updateTask(task) {
    const index = appState.tasks.findIndex(t => t.id === task.id);
    if (index !== -1) {
        appState.tasks[index] = task;
    } else {
        appState.tasks.push(task);
    }
    updateTaskList();
}

function updateProject(project) {
    if (appState.currentProject && appState.currentProject.id === project.id) {
        appState.currentProject = project;
    }
    updateProjectList(appState.projects.map(p => p.id === project.id ? project : p));
}

// AI chat functionality

function handleAIChatInput(event) {
    if (event.key === 'Enter') {
        const input = event.target;
        const message = input.value.trim();
        if (message) {
            sendAIChatMessage(message);
            input.value = '';
        }
    }
}

function sendAIChatMessage(message) {
    socket.send(JSON.stringify({
        type: 'ai_chat',
        message: message,
        project_id: appState.currentProject ? appState.currentProject.id : null
    }));
    appendAIChatMessage('User', message);
}

function handleAIResponse(message) {
    appendAIChatMessage('AI', message);
}

function appendAIChatMessage(sender, message) {
    const chatHistoryElement = document.getElementById('aiChatHistory');
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${sender.toLowerCase()}-message`;
    messageElement.textContent = `${sender}: ${message}`;
    chatHistoryElement.appendChild(messageElement);
    chatHistoryElement.scrollTop = chatHistoryElement.scrollHeight;

    appState.aiChatHistory.push({ sender, message });
}

// Helper functions

function getAuthToken() {
    // Implement this function to retrieve the authentication token
    // (e.g., from localStorage or a cookie)
    return localStorage.getItem('authToken');
}

// Error handling
window.onerror = function(message, source, lineno, colno, error) {
    console.error('Unhandled error:', error);
    // You could send this error to your server for logging
    // sendErrorToServer(message, source, lineno, colno, error);
};

// Add any additional functions or logic as needed

if (DEBUG) {
    console.log('main.js loaded and initialized');
}
