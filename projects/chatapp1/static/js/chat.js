// static/js/chat.js

let socket;

// Function to establish WebSocket connection
function connectSocket() {
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('WebSocket connected');
    });

    socket.on('new_message', function(data) {
        receiveMessage(data);
    });

    socket.on('disconnect', function() {
        console.log('WebSocket disconnected');
    });
}

// Function to send a message to the server
function sendMessage(message) {
    if (socket && socket.connected) {
        socket.emit('message', {
            content: message,
            sender_id: currentUserId,  // Assuming currentUserId is set somewhere
            timestamp: new Date().toISOString()
        });
    } else {
        console.error('WebSocket is not connected');
    }
}

// Function to handle incoming messages
function receiveMessage(data) {
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    
    // Create sender element
    const senderElement = document.createElement('span');
    senderElement.className = 'sender';
    senderElement.textContent = data.sender_id + ': ';
    
    // Create content element
    const contentElement = document.createElement('span');
    contentElement.className = 'content';
    contentElement.textContent = data.content;
    
    // Create timestamp element
    const timestampElement = document.createElement('span');
    timestampElement.className = 'timestamp';
    timestampElement.textContent = new Date(data.timestamp).toLocaleTimeString();
    
    // Append elements to message
    messageElement.appendChild(senderElement);
    messageElement.appendChild(contentElement);
    messageElement.appendChild(timestampElement);
    
    // Append message to chat container
    const chatContainer = document.getElementById('chatMessages');
    chatContainer.appendChild(messageElement);
    
    // Scroll to bottom of chat
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to initialize chat functionality
function initChat() {
    connectSocket();
    
    // Add event listener for send button
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');
    
    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = '';
        }
    });
}

// Initialize chat when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initChat);