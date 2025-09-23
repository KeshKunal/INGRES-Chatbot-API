import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatWindow from './components/ChatWindow'; 
import Header from './components/Header';
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
  const [loadingStatus, setLoadingStatus] = useState('');

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
    setLoadingStatus('');
    localStorage.removeItem('chatMessages');
  };

  const handleSendMessage = async (messageText) => {
    const userMessage = { id: uuidv4(), sender: 'user', text: messageText, type: 'text' };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setLoadingStatus('Initializing...'); // Initial status

    const botMessageId = uuidv4();
    // Add a placeholder message for the bot's response
    setMessages(prev => [...prev, { id: botMessageId, sender: 'bot', text: '', type: 'text' }]);

    const handleChunk = (chunk) => {
      // All chunks from the new backend are objects
      if (typeof chunk !== 'object' || chunk === null) return;

      switch (chunk.type) {
        case 'status':
          setLoadingStatus(chunk.message);
          break;
        
        case 'error':
          setLoadingStatus('');
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { ...msg, text: chunk.text, type: 'error', errorDetails: chunk.errorDetails }
                : msg
            )
          );
          break;
        
        case 'final_text':
          setLoadingStatus('');
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { ...msg, text: chunk.content, type: 'text' }
                : msg
            )
          );
          break;

        case 'visualization':
          setLoadingStatus('');
          setMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { 
                    ...msg, 
                    text: chunk.data.title || 'Here is the requested chart.', 
                    type: 'visualization', // Set the correct type
                    data: chunk.data // Pass the whole data object
                  }
                : msg
            )
          );
          break;

        default:
          break; // Ignore unknown chunk types
      }
    };

    await streamMessageFromBackend(messageText, selectedTools, handleChunk);
    
    setIsLoading(false);
    setLoadingStatus(''); // Clear status when done
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
        loadingStatus={loadingStatus}
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