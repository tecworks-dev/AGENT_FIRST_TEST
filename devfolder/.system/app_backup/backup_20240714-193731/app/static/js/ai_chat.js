
// app/static/js/ai_chat.js
// Purpose: Implements the AI chat functionality for real-time communication with the AI assistant.
// Description: This file contains WebSocket connection setup, message sending and receiving functions,
// and UI updates for the chat interface.

let socket;
const messageContainer = document.getElementById('message-container');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');

// Initialize WebSocket connection
function initWebSocket() {
    // Use secure WebSocket if the page is served over HTTPS
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    socket = new WebSocket(`${protocol}//${host}/ws/chat`);

    socket.onopen = function(e) {
        console.log("WebSocket connection established");
        addSystemMessage("Connected to AI assistant. How can I help you today?");
    };

    socket.onmessage = function(event) {
        const message = JSON.parse(event.data);
        if (message.type === 'ai_message') {
            addAIMessage(message.content);
        }
    };

    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`WebSocket connection closed cleanly, code=${event.code}, reason=${event.reason}`);
        } else {
            console.error('WebSocket connection died');
        }
        addSystemMessage("Connection to AI assistant lost. Please refresh the page to reconnect.");
    };

    socket.onerror = function(error) {
        console.error(`WebSocket error: ${error.message}`);
        addSystemMessage("Error connecting to AI assistant. Please try again later.");
    };
}

// Send message to server
function sendMessage(message) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'user_message',
            content: message
        }));
    } else {
        console.error('WebSocket is not open. Message not sent.');
        addSystemMessage("Unable to send message. Please check your connection and try again.");
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'user-message');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Add AI message to chat
function addAIMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'ai-message');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Add system message to chat
function addSystemMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system-message');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Handle form submission
messageForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (message) {
        addUserMessage(message);
        sendMessage(message);
        messageInput.value = '';
    }
});

// Initialize chat when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initWebSocket();

    // Reconnect WebSocket if connection is lost
    setInterval(function() {
        if (socket.readyState === WebSocket.CLOSED) {
            console.log('Attempting to reconnect WebSocket...');
            initWebSocket();
        }
    }, 5000);
});

// Implement typing indicator
let typingTimeout;
messageInput.addEventListener('input', function() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'typing',
            content: 'typing'
        }));

        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            socket.send(JSON.stringify({
                type: 'typing',
                content: 'stopped'
            }));
        }, 1000);
    }
});

// Debug mode
const DEBUG = true;

if (DEBUG) {
    console.log('AI Chat script loaded in debug mode');
    window.addEventListener('error', function(e) {
        console.error('AI Chat Error:', e.error.message);
        addSystemMessage(`An error occurred: ${e.error.message}`);
    });
}
