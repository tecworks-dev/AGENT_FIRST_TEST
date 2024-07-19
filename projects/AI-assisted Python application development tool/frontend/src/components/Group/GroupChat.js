
// Group chat component
// Handles group chat functionality

import React, { useState, useEffect } from 'react';
import MessageList from '../Chat/MessageList';
import { connectSocket, disconnectSocket, onNewMessage } from '../../utils/socket';
import { get, post } from '../../utils/api';
import { encryptMessage, decryptMessage } from '../../utils/encryption';

const GroupChat = ({ groupId, currentUser }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [groupKey, setGroupKey] = useState('');

  useEffect(() => {
    // Connect to WebSocket when component mounts
    connectSocket();

    // Fetch group messages and encryption key
    fetchGroupMessages();
    fetchGroupKey();

    // Listen for new messages
    onNewMessage((message) => {
      if (message.groupId === groupId) {
        const decryptedMessage = decryptMessage(message.content, groupKey);
        setMessages((prevMessages) => [...prevMessages, { ...message, content: decryptedMessage }]);
      }
    });

    // Disconnect from WebSocket when component unmounts
    return () => {
      disconnectSocket();
    };
  }, [groupId]);

  const fetchGroupMessages = async () => {
    try {
      const response = await get(`/api/groups/${groupId}/messages`);
      const decryptedMessages = response.data.map(message => ({
        ...message,
        content: decryptMessage(message.content, groupKey)
      }));
      setMessages(decryptedMessages);
    } catch (error) {
      console.error('Error fetching group messages:', error);
    }
  };

  const fetchGroupKey = async () => {
    try {
      const response = await get(`/api/groups/${groupId}/key`);
      setGroupKey(response.data.key);
    } catch (error) {
      console.error('Error fetching group key:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;

    const encryptedMessage = encryptMessage(newMessage, groupKey);

    try {
      await post(`/api/groups/${groupId}/messages`, { content: encryptedMessage });
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="group-chat">
      <h2>Group Chat</h2>
      <MessageList messages={messages} currentUser={currentUser} />
      <form onSubmit={handleSendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default GroupChat;
