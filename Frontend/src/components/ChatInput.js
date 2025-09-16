import React, { useState, useRef } from 'react';
import { FiMic, FiSend, FiChevronUp, FiSquare } from 'react-icons/fi';

// REFACTORED: Now receives 'onVisibilityToggle' prop for clarity
const ChatInput = ({ onSendMessage, isLoading, onVisibilityToggle, isToolsVisible }) => {
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  
  const handleSend = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleVoiceInput = async () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        mediaRecorderRef.current.start();
        const audioChunks = [];
        mediaRecorderRef.current.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });
        mediaRecorderRef.current.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          console.log("Audio Blob ready to be sent:", audioBlob);
        });
        setIsRecording(true);
      } catch (err) {
        console.error("Error accessing microphone:", err);
        alert("Could not access the microphone. Please check your browser permissions.");
      }
    }
  };

  return (
    <div className="chat-input-container">
      <button 
        className={`tools-toggle-btn ${isToolsVisible ? 'toggled' : ''}`} 
        onClick={onVisibilityToggle} // REFACTORED: Using clearer prop name
        title="Toggle Tools"
      >
        <FiChevronUp />
      </button>
      <textarea
        className="chat-input"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask about groundwater resources..."
        rows="1"
        disabled={isLoading || isRecording}
      />
      <button 
        className={`icon-button ${isRecording ? 'recording' : ''}`} 
        disabled={isLoading} 
        onClick={handleVoiceInput}
        title={isRecording ? "Stop Recording" : "Record Voice"}
      >
        {isRecording ? <FiSquare /> : <FiMic />}
      </button>
      <button className="icon-button send-button" onClick={handleSend} disabled={isLoading || isRecording}>
        <FiSend />
      </button>
    </div>
  );
};

export default ChatInput;