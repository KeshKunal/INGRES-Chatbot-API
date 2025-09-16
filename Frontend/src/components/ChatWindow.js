import React, { useRef, useEffect } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import SuggestedQuestions from './SuggestedQuestions';

const ChatWindow = ({ messages, isLoading, onSendMessage }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <main className="chat-window">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {messages.length === 1 && !isLoading && (
        <SuggestedQuestions onQuestionClick={onSendMessage} />
      )}
      {isLoading && <TypingIndicator />}
      <div ref={chatEndRef} />
    </main>
  );
};

export default ChatWindow;