
// Message.js
// Purpose: Individual message component for displaying a single message in the chat interface.
// Description: This component renders a single message with sender information, content, and timestamp.

import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const MessageContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  max-width: 70%;
  ${props => props.isSender ? 'align-self: flex-end;' : 'align-self: flex-start;'}
  background-color: ${props => props.isSender ? '#DCF8C6' : '#FFFFFF'};
`;

const SenderName = styled.span`
  font-weight: bold;
  font-size: 0.9em;
  margin-bottom: 5px;
`;

const MessageContent = styled.p`
  margin: 0;
  word-wrap: break-word;
`;

const Timestamp = styled.span`
  font-size: 0.8em;
  color: #999;
  align-self: flex-end;
  margin-top: 5px;
`;

const Message = ({ content, sender, timestamp, currentUser }) => {
  const isSender = sender === currentUser;

  return (
    <MessageContainer isSender={isSender}>
      {!isSender && <SenderName>{sender}</SenderName>}
      <MessageContent>{content}</MessageContent>
      <Timestamp>{new Date(timestamp).toLocaleString()}</Timestamp>
    </MessageContainer>
  );
};

Message.propTypes = {
  content: PropTypes.string.isRequired,
  sender: PropTypes.string.isRequired,
  timestamp: PropTypes.string.isRequired,
  currentUser: PropTypes.string.isRequired,
};

export default Message;

// Debug logging
if (process.env.NODE_ENV === 'development') {
  console.log('Message component loaded');
}
