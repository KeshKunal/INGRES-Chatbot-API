import React, { useRef, useEffect } from 'react'; 
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import SuggestedQuestions from './SuggestedQuestions';

const ChatWindow = ({ messages, isLoading, loadingStatus, onSendMessage }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading, loadingStatus]);

  const getStatusIcon = (status) => {
    const statusLower = status.toLowerCase();
    
    if (statusLower.includes('analyzing') || statusLower.includes('query') || statusLower.includes('intelligence')) {
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

  const statusInfo = loadingStatus ? getStatusIcon(loadingStatus) : null;

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
          {statusInfo ? (
            <div className="message bot loading-message"> 
              <img src="/images/bot-avatar.png" alt="Bot Avatar" className="message-avatar bot-avatar" />
              <div className={`message-content loading-container ${statusInfo.className}`}>
                <div className={`loading-icon ${statusInfo.animation}`}>
                  {statusInfo.icon}
                </div>
                <div className="loading-text">{loadingStatus}</div>
              </div>
            </div>
          ) : (
            <div className="message bot loading-message"> {/* Also wrap TypingIndicator like a bot message */}
              <img src="/path/to/bot-avatar.png" alt="Bot Avatar" className="message-avatar bot-avatar" />
              <div className="message-content"> {/* Use message-content for consistent padding/width */}
                <TypingIndicator />
              </div>
            </div>
          )}
        </>
      )}
      <div ref={chatEndRef} />
    </main>
  );
};

export default ChatWindow;