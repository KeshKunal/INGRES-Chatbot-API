import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="message bot">
      <img src="/images/bot-avatar.png" alt="bot avatar" className="message-avatar" />
      <div className="message-content">
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;