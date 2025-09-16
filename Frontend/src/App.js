import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ToolsBar from './components/ToolsBar';
import ChatInput from './components/ChatInput';
import { streamMessageFromBackend } from './api/chatService';
import './App.css';

const initialMessage = {
    id: uuidv4(),
    sender: 'bot',
    text: 'Hello! I\'m the INGRES AI Assistant. I can help you access groundwater resource data, historical assessments, and provide insights. What would you like to know?',
    type: 'text'
};

function App() {
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    return savedMessages ? JSON.parse(savedMessages) : [initialMessage];
  });
  
  const [selectedTools, setSelectedTools] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState('light');
  const [isToolsVisible, setIsToolsVisible] = useState(false);

  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    document.body.className = '';
    document.body.classList.add(`theme-${theme}`);
  }, [theme]);

  const handleThemeToggle = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const handleSelectTool = (toolId) => {
    setSelectedTools(prev =>
      prev.includes(toolId)
        ? prev.filter(t => t !== toolId)
        : [...prev, toolId]
    );
  };
  
  const handleNewChat = () => {
    setMessages([initialMessage]);
    localStorage.removeItem('chatMessages');
  };

  const handleSendMessage = async (messageText) => {
    const userMessage = { id: uuidv4(), sender: 'user', text: messageText, type: 'text' };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const botMessageId = uuidv4();
    setMessages(prev => [...prev, { id: botMessageId, sender: 'bot', text: '', type: 'text' }]);

    const handleChunk = (chunk) => {
      if (typeof chunk === 'object') {
        if (chunk.type === 'error') {
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { ...msg, text: chunk.text, type: 'error', errorDetails: chunk.errorDetails }
                : msg
            )
          );
        } else if (chunk.type === 'graph') {
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { 
                    ...msg, 
                    text: chunk.text || 'Here is the requested chart.', 
                    type: 'graph', 
                    data: {
                      visualType: 'bar',
                      chartData: chunk.data
                    } 
                  }
                : msg
            )
          );
        } else {
          // Handle other object types
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { ...msg, ...chunk }
                : msg
            )
          );
        }
      } else {
        // Handle plain text chunks
        setMessages(prev =>
          prev.map(msg =>
            msg.id === botMessageId
              ? { ...msg, text: msg.text + chunk }
              : msg
          )
        );
      }
    };

    await streamMessageFromBackend(messageText, selectedTools, handleChunk);
    
    setIsLoading(false);
  };

  return (
    <div className={`app-container theme-${theme}`}>
      <Header 
        theme={theme} 
        onThemeToggle={handleThemeToggle}
        onNewChat={handleNewChat}
      />
      <ChatWindow 
        messages={messages} 
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
      />

      {/* Wrapped in a footer for better structure */}
      <footer className="bottom-area">
        <ToolsBar 
          selectedTools={selectedTools} 
          onSelectTool={handleSelectTool}
          isVisible={isToolsVisible}
        />
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading}
          onVisibilityToggle={() => setIsToolsVisible(!isToolsVisible)}
          isToolsVisible={isToolsVisible}
        />
      </footer>
    </div>
  );
}

export default App;