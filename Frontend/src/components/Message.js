import React, { useState } from 'react';
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
import botAvatar from '../assets/bot-avatar.png';
import userAvatar from '../assets/user-avatar.png';

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
    // Check if this is a groundwater data response
    if (!text.includes('Total Rainfall') && !text.includes('Annual Groundwater')) {
      return <p className="message-text">{text}</p>;
    }

    // Split the text by district entries
    const districtEntries = text.split('**For ').filter(entry => entry.trim());
    
    if (districtEntries.length === 0) {
      return <p className="message-text">{text}</p>;
    }

    const introText = districtEntries[0].split('**')[0];
    
    return (
      <div className="groundwater-response">
        {introText && <p className="intro-text">{introText.trim()}</p>}
        
        <div className="districts-container">
          {districtEntries.map((entry, index) => {
            if (!entry.includes('district')) return null;
            
            const lines = entry.split(' - ');
            const districtName = lines[0].replace(/\*+/g, '').trim();
            
            // Extract data points
            const dataPoints = [];
            lines.forEach(line => {
              if (line.includes('Total Rainfall:')) {
                const rainfall = line.match(/Total Rainfall:\s*([0-9.]+)\s*mm/);
                if (rainfall) dataPoints.push({ label: 'Total Rainfall', value: rainfall[1], unit: 'mm' });
              }
              if (line.includes('Annual Groundwater Recharge:')) {
                const recharge = line.match(/Annual Groundwater Recharge:\s*([0-9.]+)\s*ham/);
                if (recharge) dataPoints.push({ label: 'Annual Groundwater Recharge', value: recharge[1], unit: 'ham' });
              }
              if (line.includes('Annual Extractable Groundwater Resource:')) {
                const extractable = line.match(/Annual Extractable Groundwater Resource:\s*([0-9.]+)\s*ham/);
                if (extractable) dataPoints.push({ label: 'Annual Extractable Resource', value: extractable[1], unit: 'ham' });
              }
              if (line.includes('Total Groundwater Extraction:')) {
                const extraction = line.match(/Total Groundwater Extraction:\s*([0-9.]+)\s*ham/);
                if (extraction) dataPoints.push({ label: 'Total Groundwater Extraction', value: extraction[1], unit: 'ham' });
              }
              if (line.includes('Stage of Groundwater Extraction:')) {
                const stage = line.match(/Stage of Groundwater Extraction:\s*([0-9.]+)%/);
                if (stage) dataPoints.push({ label: 'Stage of Extraction', value: stage[1], unit: '%' });
              }
              if (line.includes('Net Annual Groundwater Available for Future Use:')) {
                const future = line.match(/Net Annual Groundwater Available for Future Use:\s*([0-9.]+)\s*ham/);
                if (future) dataPoints.push({ label: 'Available for Future Use', value: future[1], unit: 'ham' });
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
                        {parseFloat(point.value).toLocaleString()} <span className="unit">{point.unit}</span>
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

    if (message.type === 'visualization' && message.data) {
      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: message.data.title || 'Data Visualization'
          }
        }
      };

      switch (message.data.visualType) {
        case 'bar':
          return (
            <div className="chart-container">
              <Bar data={message.data.chartData} options={options} />
            </div>
          );
        case 'line':
          return (
            <div className="chart-container">
              <Line data={message.data.chartData} options={options} />
            </div>
          );
        case 'pie':
          return (
            <div className="chart-container">
              <Pie data={message.data.chartData} options={options} />
            </div>
          );
        default:
          return formatGroundwaterData(message.text);
      }
    }
    
    return formatGroundwaterData(message.text);
  };

  const showCopyButton = message.sender === 'bot' && 
                        message.text && 
                        message.text.trim().length > 0 && 
                        !message.text.endsWith('...');

  if (isProcessing) {
    return (
      <div className="message bot-message">
        <img src={botAvatar} alt="Bot Avatar" className="message-avatar" />
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
        src={isUser ? userAvatar : botAvatar} 
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