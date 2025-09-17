import React, { useRef, useEffect } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import SuggestedQuestions from './SuggestedQuestions';

const ChatWindow = ({ messages, isLoading, loadingStatus, onSendMessage }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading, loadingStatus]);

  // Helper function to get appropriate icon and animation for different statuses
  const getStatusIcon = (status) => {
    const statusLower = status.toLowerCase();
    
    if (statusLower.includes('analyzing') || statusLower.includes('processing query')) {
      return { icon: '🔍', animation: 'animate-pulse', className: 'analyzing' };
    } else if (statusLower.includes('fetching') || statusLower.includes('retrieving') || statusLower.includes('database')) {
      return { icon: '📊', animation: 'animate-bounce', className: 'processing' };
    } else if (statusLower.includes('generating') || statusLower.includes('preparing') || statusLower.includes('response')) {
      return { icon: '⚡', animation: 'animate-spin', className: 'generating' };
    } else if (statusLower.includes('connecting') || statusLower.includes('initializing')) {
      return { icon: '🔗', animation: 'animate-pulse', className: 'analyzing' };
    } else {
      return { icon: '🤖', animation: 'animate-pulse', className: '' };
    }
  };

  return (
    <main className="chat-window">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {messages.length === 1 && !isLoading && (
        <SuggestedQuestions onQuestionClick={onSendMessage} />
      )}
      {(isLoading || loadingStatus) && (
        <>
          {loadingStatus ? (
            <div className={`loading-container ${getStatusIcon(loadingStatus).className}`}>
              <div className={`loading-icon ${getStatusIcon(loadingStatus).animation}`}>
                {getStatusIcon(loadingStatus).icon}
              </div>
              <div className="loading-text">{loadingStatus}</div>
            </div>
          ) : (
            <div className="loading-container">
              <TypingIndicator />
            </div>
          )}
        </>
      )}
      <div ref={chatEndRef} />
    </main>
  );
};

export default ChatWindow;