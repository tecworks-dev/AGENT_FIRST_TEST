
/**
 * error_handling.js
 * Purpose: Provides enhanced error handling and user feedback mechanisms for the frontend.
 * Description: This file contains functions for handling JavaScript errors, displaying user-friendly
 * error messages, and reporting errors to the server for logging.
 */

// Global error handler
window.onerror = function(message, source, lineno, colno, error) {
    handleError(error || new Error(message));
    return true; // Prevent default error handling
};

/**
 * Handles and logs JavaScript errors
 * @param {Error} error - The error object to handle
 */
function handleError(error) {
    console.error('Error caught:', error);

    // Log error to the server
    reportErrorToServer(error);

    // Display a user-friendly message
    displayErrorToUser('An unexpected error occurred. Our team has been notified.');

    if (DEBUG) {
        console.debug('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
    }
}

/**
 * Displays user-friendly error messages
 * @param {string} message - The error message to display to the user
 */
function displayErrorToUser(message) {
    // Check if error container exists, if not create it
    let errorContainer = document.getElementById('error-container');
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.id = 'error-container';
        errorContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 9999;
        `;
        document.body.appendChild(errorContainer);
    }

    // Create and add error message
    const errorMessage = document.createElement('div');
    errorMessage.textContent = message;
    errorContainer.appendChild(errorMessage);

    // Remove the message after 5 seconds
    setTimeout(() => {
        errorContainer.removeChild(errorMessage);
        if (errorContainer.childNodes.length === 0) {
            document.body.removeChild(errorContainer);
        }
    }, 5000);
}

/**
 * Reports errors to the server for logging
 * @param {Error} error - The error object to report
 */
function reportErrorToServer(error) {
    const errorData = {
        name: error.name,
        message: error.message,
        stack: error.stack,
        userAgent: navigator.userAgent,
        url: window.location.href,
        timestamp: new Date().toISOString()
    };

    fetch('/api/log-error', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorData)
    }).catch(fetchError => {
        console.error('Failed to report error to server:', fetchError);
    });
}

// Custom error types
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

class NetworkError extends Error {
    constructor(message) {
        super(message);
        this.name = 'NetworkError';
    }
}

// Example usage of custom error types
function validateInput(input) {
    if (typeof input !== 'string' || input.length === 0) {
        throw new ValidationError('Input must be a non-empty string');
    }
}

function fetchData(url) {
    return fetch(url).catch(error => {
        throw new NetworkError(`Failed to fetch data from ${url}: ${error.message}`);
    });
}

// Debug flag (set to false in production)
const DEBUG = true;

if (DEBUG) {
    console.debug('Error handling module loaded');
}
