import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Bar, Line, Pie } from 'react-chartjs-2';
import './Message.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { FiCopy, FiCheck } from 'react-icons/fi';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Message = ({ message, isProcessing }) => {
  const isUser = message.sender === 'user';
  const messageClass = isUser ? 'user' : 'bot';
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const formatGroundwaterData = (text) => {
    // Heuristic to determine if this is a groundwater data response.
    // Check for common keywords and the expected Markdown heading format.
    if (!text.includes('#### **') || (!text.includes('RainfallTotal') && !text.includes('AnnualGroundwaterRechargeTotal'))) {
      return null; // Fallback to default markdown rendering
    }

    // Split the text into an introductory part and district entries
    const parts = text.split(/(#### \*\*)/);
    let introText = '';
    let districtEntriesRaw = [];

    if (parts.length > 1) {
      introText = parts[0].trim();
      // Reconstruct district entries, ensuring each starts with '#### **'
      for (let i = 1; i < parts.length; i += 2) {
        if (parts[i] === '#### **') {
          districtEntriesRaw.push(parts[i] + parts[i + 1]);
        }
      }
    } else {
      return null;
    }

    if (districtEntriesRaw.length === 0) {
      return null;
    }

    return (
      <div className="groundwater-response">
        {introText && <ReactMarkdown className="intro-text">{introText}</ReactMarkdown>}
        
        <div className="districts-container">
          {districtEntriesRaw.map((entry, index) => {
            const lines = entry.split('\n').filter(line => line.trim());
            if (lines.length === 0) return null;

            const districtNameMatch = lines[0].match(/#### \*\*([^*]+)\*\*/);
            const districtName = districtNameMatch ? districtNameMatch[1].trim() : `District ${index + 1}`;
            
            const dataPoints = [];
            lines.slice(1).forEach(line => {
              // Generic regex to match: "- **FieldName**: Value Unit"
              const match = line.match(/^- \*\*([A-Za-z0-9_]+)\*\*:\s*([0-9,.]+)\s*(.*)$/);
              if (match) {
                const label = match[1].replace(/([A-Z])/g, ' $1').trim(); // Add space before capital letters
                const rawValue = match[2];
                const unit = match[3].trim();
                
                // Remove commas before parsing to float for robustness
                const cleanedValue = rawValue.replace(/,/g, ''); 
                dataPoints.push({ label: label, value: cleanedValue, unit: unit });
              }
            });

            return (
              <div key={index} className="district-card">
                <h3 className="district-name">{districtName}</h3>
                <div className="data-grid">
                  {dataPoints.map((point, idx) => (
                    <div key={idx} className="data-item">
                      <span className="data-label">{point.label}</span>
                      <span className="data-value">
                        {parseFloat(point.value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} <span className="unit">{point.unit}</span>
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    if (message.type === 'error') {
      return (
        <div className="error-message">
          <p className="error-text">{message.text}</p>
          {message.errorDetails && (
            <details className="error-details">
              <summary>Technical Details</summary>
              <p>{message.errorDetails}</p>
            </details>
          )}
        </div>
      );
    }

    if (message.sender === 'user') {
      return <p className="message-text">{message.text}</p>;
    }
    
    if (message.sender === 'bot') {
      if (message.type === 'visualization' && message.data) {
        // ... (visualization logic remains the same)
      } else {
        // For regular bot text, try to format as structured data first.
        const formattedData = formatGroundwaterData(message.text);
        if (formattedData) {
          return formattedData; // Render the structured cards
        }
        // If it's not structured data, render as plain markdown.
        return <ReactMarkdown>{message.text}</ReactMarkdown>;
      }
    }
    
    return <p className="message-text">{message.text}</p>;
  };

  const showCopyButton = message.sender === 'bot' && 
                        message.text && 
                        message.text.trim().length > 0 && 
                        !message.text.endsWith('...');

  if (isProcessing) {
    // This is now handled by ChatWindow.js, but kept as a fallback.
    return (
      <div className="message bot-message">
        <img src="/images/bot-avatar.png" alt="Bot Avatar" className="message-avatar" />
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    );
  }

  return (
    <div className={`message ${messageClass}`}>
      <img 
        src={isUser ? "/images/user-avatar.png" : "/images/bot-avatar.png"} 
        alt={`${isUser ? 'User' : 'Bot'} Avatar`} 
        className="message-avatar"
      />
      <div className="message-content">
        {renderContent()}
        {!isUser && showCopyButton && (
          <button 
            className="copy-btn" 
            onClick={handleCopy}
            title="Copy message"
          >
            {isCopied ? <FiCheck /> : <FiCopy />}
          </button>
        )}
      </div>
    </div>
  );
};

export default Message;