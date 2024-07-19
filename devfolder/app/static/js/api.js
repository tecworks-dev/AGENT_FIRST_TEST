
/**
 * api.js
 * 
 * This file centralizes API calls to the backend.
 * It provides functions for making AJAX requests to various API endpoints
 * and includes error handling for API calls.
 */

// Base URL for API endpoints
const BASE_URL = '/api/v1';

// Default headers for API requests
const DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
};

/**
 * Handles API errors and throws an error with a meaningful message
 * @param {Response} response - The response object from the fetch call
 * @throws {Error} Throws an error with the status and statusText
 */
const handleApiError = async (response) => {
    if (!response.ok) {
        let errorMessage = `API Error: ${response.status} ${response.statusText}`;
        try {
            const errorData = await response.json();
            if (errorData.message) {
                errorMessage += ` - ${errorData.message}`;
            }
        } catch (e) {
            console.error('Error parsing error response:', e);
        }
        throw new Error(errorMessage);
    }
};

/**
 * Makes a GET request to the specified endpoint
 * @param {string} endpoint - The API endpoint
 * @param {Object} params - Query parameters (optional)
 * @returns {Promise<Object>} The response data
 */
export const apiGet = async (endpoint, params = {}) => {
    const url = new URL(`${BASE_URL}${endpoint}`, window.location.origin);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: DEFAULT_HEADERS,
            credentials: 'same-origin'
        });

        await handleApiError(response);
        return await response.json();
    } catch (error) {
        console.error(`Error in GET request to ${endpoint}:`, error);
        throw error;
    }
};

/**
 * Makes a POST request to the specified endpoint
 * @param {string} endpoint - The API endpoint
 * @param {Object} data - The data to be sent in the request body
 * @returns {Promise<Object>} The response data
 */
export const apiPost = async (endpoint, data = {}) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            credentials: 'same-origin',
            body: JSON.stringify(data)
        });

        await handleApiError(response);
        return await response.json();
    } catch (error) {
        console.error(`Error in POST request to ${endpoint}:`, error);
        throw error;
    }
};

/**
 * Makes a PUT request to the specified endpoint
 * @param {string} endpoint - The API endpoint
 * @param {Object} data - The data to be sent in the request body
 * @returns {Promise<Object>} The response data
 */
export const apiPut = async (endpoint, data = {}) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: DEFAULT_HEADERS,
            credentials: 'same-origin',
            body: JSON.stringify(data)
        });

        await handleApiError(response);
        return await response.json();
    } catch (error) {
        console.error(`Error in PUT request to ${endpoint}:`, error);
        throw error;
    }
};

/**
 * Makes a DELETE request to the specified endpoint
 * @param {string} endpoint - The API endpoint
 * @returns {Promise<Object>} The response data
 */
export const apiDelete = async (endpoint) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: DEFAULT_HEADERS,
            credentials: 'same-origin'
        });

        await handleApiError(response);
        return await response.json();
    } catch (error) {
        console.error(`Error in DELETE request to ${endpoint}:`, error);
        throw error;
    }
};

// Project-related API calls
export const projectApi = {
    getProjects: () => apiGet('/projects'),
    getProject: (id) => apiGet(`/projects/${id}`),
    createProject: (data) => apiPost('/projects', data),
    updateProject: (id, data) => apiPut(`/projects/${id}`, data),
    deleteProject: (id) => apiDelete(`/projects/${id}`)
};

// Task-related API calls
export const taskApi = {
    getTasks: (projectId) => apiGet(`/projects/${projectId}/tasks`),
    getTask: (projectId, taskId) => apiGet(`/projects/${projectId}/tasks/${taskId}`),
    createTask: (projectId, data) => apiPost(`/projects/${projectId}/tasks`, data),
    updateTask: (projectId, taskId, data) => apiPut(`/projects/${projectId}/tasks/${taskId}`, data),
    deleteTask: (projectId, taskId) => apiDelete(`/projects/${projectId}/tasks/${taskId}`)
};

// AI-related API calls
export const aiApi = {
    generateCode: (data) => apiPost('/ai/generate-code', data),
    reviewCode: (data) => apiPost('/ai/review-code', data),
    explainCode: (data) => apiPost('/ai/explain-code', data),
    optimizeCode: (data) => apiPost('/ai/optimize-code', data)
};

// User-related API calls
export const userApi = {
    login: (data) => apiPost('/auth/login', data),
    logout: () => apiPost('/auth/logout'),
    register: (data) => apiPost('/auth/register', data),
    getCurrentUser: () => apiGet('/auth/user'),
    updateProfile: (data) => apiPut('/auth/user', data)
};

// WebSocket connection setup
export const setupWebSocket = (token) => {
    const socket = new WebSocket(`ws://${window.location.host}/ws?token=${token}`);
    
    socket.onopen = () => {
        console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // Handle different types of messages
        switch(data.type) {
            case 'task_update':
                // Handle task update
                break;
            case 'project_update':
                // Handle project update
                break;
            // Add more cases as needed
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed');
    };

    return socket;
};

// Export all API functions
export default {
    get: apiGet,
    post: apiPost,
    put: apiPut,
    delete: apiDelete,
    project: projectApi,
    task: taskApi,
    ai: aiApi,
    user: userApi,
    setupWebSocket
};
