
/**
 * websocket.js
 * 
 * This file handles WebSocket connections with enhanced authentication and message validation.
 * It provides functions for initializing WebSocket connections, sending and handling messages,
 * and authenticating the connection.
 */

// Debug flag for logging
const DEBUG = true;

/**
 * Initializes a new WebSocket connection with authentication
 * @param {string} token - The authentication token
 * @returns {WebSocket} The initialized WebSocket connection
 */
function initWebSocket(token) {
    if (DEBUG) console.log('Initializing WebSocket connection...');

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const socket = new WebSocket(`${protocol}//${host}/ws`);

    socket.onopen = function(event) {
        if (DEBUG) console.log('WebSocket connection opened:', event);
        authenticate(socket, token);
    };

    socket.onclose = function(event) {
        if (DEBUG) console.log('WebSocket connection closed:', event);
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    socket.onmessage = handleMessage;

    return socket;
}

/**
 * Sends a validated message through the WebSocket
 * @param {WebSocket} socket - The WebSocket connection
 * @param {object} message - The message to send
 */
function sendMessage(socket, message) {
    if (DEBUG) console.log('Sending message:', message);

    if (typeof message !== 'object') {
        console.error('Invalid message format. Expected an object.');
        return;
    }

    try {
        const validatedMessage = JSON.stringify(message);
        socket.send(validatedMessage);
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

/**
 * Handles incoming messages with proper validation
 * @param {MessageEvent} event - The message event
 */
function handleMessage(event) {
    if (DEBUG) console.log('Received message:', event.data);

    try {
        const message = JSON.parse(event.data);
        
        // Validate message structure
        if (!message.type || !message.content) {
            throw new Error('Invalid message structure');
        }

        // Handle different message types
        switch (message.type) {
            case 'update':
                handleUpdateMessage(message.content);
                break;
            case 'error':
                handleErrorMessage(message.content);
                break;
            case 'notification':
                handleNotificationMessage(message.content);
                break;
            default:
                console.warn('Unknown message type:', message.type);
        }
    } catch (error) {
        console.error('Error handling message:', error);
    }
}

/**
 * Authenticates the WebSocket connection
 * @param {WebSocket} socket - The WebSocket connection
 * @param {string} token - The authentication token
 */
function authenticate(socket, token) {
    if (DEBUG) console.log('Authenticating WebSocket connection...');

    const authMessage = {
        type: 'authentication',
        token: token
    };

    sendMessage(socket, authMessage);
}

/**
 * Handles update messages
 * @param {object} content - The content of the update message
 */
function handleUpdateMessage(content) {
    if (DEBUG) console.log('Handling update message:', content);
    // Implement update logic here
}

/**
 * Handles error messages
 * @param {object} content - The content of the error message
 */
function handleErrorMessage(content) {
    console.error('Received error message:', content);
    // Implement error handling logic here
}

/**
 * Handles notification messages
 * @param {object} content - The content of the notification message
 */
function handleNotificationMessage(content) {
    if (DEBUG) console.log('Received notification:', content);
    // Implement notification display logic here
}

// Export functions for use in other modules
export { initWebSocket, sendMessage };
