
// WebSocket utility functions for real-time communication

import io from 'socket.io-client';

let socket;

// Connect to the WebSocket server
export const connectSocket = () => {
  if (process.env.NODE_ENV === 'development') {
    console.log('Connecting to WebSocket server...');
  }
  
  socket = io(process.env.REACT_APP_WEBSOCKET_URL, {
    transports: ['websocket'],
    upgrade: false,
  });

  socket.on('connect', () => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Connected to WebSocket server');
    }
  });

  socket.on('connect_error', (error) => {
    console.error('WebSocket connection error:', error);
  });

  return socket;
};

// Disconnect from the WebSocket server
export const disconnectSocket = () => {
  if (process.env.NODE_ENV === 'development') {
    console.log('Disconnecting from WebSocket server...');
  }

  if (socket) {
    socket.disconnect();
  }
};

// Listen for new messages
export const onNewMessage = (callback) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.on('new_message', (message) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('New message received:', message);
    }
    callback(message);
  });
};

// Join a chat room
export const joinRoom = (roomId) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.emit('join_room', { room_id: roomId });
  if (process.env.NODE_ENV === 'development') {
    console.log(`Joined room: ${roomId}`);
  }
};

// Leave a chat room
export const leaveRoom = (roomId) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.emit('leave_room', { room_id: roomId });
  if (process.env.NODE_ENV === 'development') {
    console.log(`Left room: ${roomId}`);
  }
};

// Send a message through WebSocket
export const sendMessage = (message) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.emit('new_message', message);
  if (process.env.NODE_ENV === 'development') {
    console.log('Message sent:', message);
  }
};

// Listen for typing events
export const onTyping = (callback) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.on('typing', (data) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Typing event received:', data);
    }
    callback(data);
  });
};

// Emit typing event
export const emitTyping = (roomId, userId) => {
  if (!socket) {
    console.error('Socket is not connected. Call connectSocket() first.');
    return;
  }

  socket.emit('typing', { room_id: roomId, user_id: userId });
  if (process.env.NODE_ENV === 'development') {
    console.log(`Emitted typing event for user ${userId} in room ${roomId}`);
  }
};

// Error handler
const handleError = (error) => {
  console.error('WebSocket error:', error);
  // Implement retry logic or show user-friendly error message
};

// Add error listener
if (socket) {
  socket.on('error', handleError);
}
