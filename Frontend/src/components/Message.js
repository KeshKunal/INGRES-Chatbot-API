import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { FiCopy, FiCheck } from 'react-icons/fi';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  const messageClass = isUser ? 'user' : 'bot';
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    if (message.text) {
      navigator.clipboard.writeText(message.text);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const renderContent = () => {
    if (message.type === 'graph' && message.data) {
        // ... graph logic
    }
    return <p className="message-text">{message.text}</p>;
  };

  return (
    <div className={`message ${messageClass}`}>
      <img
        src={isUser ? '/images/user-avatar.png' : '/images/bot-avatar.png'}
        alt={`${messageClass} avatar`}
        className="message-avatar"
      />
      <div className="message-content">
        {renderContent()}
      </div>
      {!isUser && message.text && (
        <button className="copy-btn" onClick={handleCopy} title="Copy text">
          {isCopied ? <FiCheck color="green" /> : <FiCopy />}
        </button>
      )}
    </div>
  );
};

export default Message;