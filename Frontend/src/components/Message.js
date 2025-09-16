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
import { FiCopy, FiCheck, FiAlertTriangle } from 'react-icons/fi';
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
    if (message.text) {
      navigator.clipboard.writeText(message.text);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const renderContent = () => {
    if (message.type === 'error') {
      return (
        <div className="error-message">
          <div className="error-icon">
            <FiAlertTriangle />
          </div>
          <div className="error-content">
            <p>{message.text}</p>
            {message.errorDetails && (
              <details>
                <summary>Error details</summary>
                <p>{message.errorDetails}</p>
              </details>
            )}
          </div>
        </div>
      );
    }
    
    if ((message.type === 'visualization' || message.type === 'graph') && message.data) {
      const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          title: {
            display: true,
            text: message.data.title || '',
          },
        },
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
        case 'table':
          return (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    {message.data.headers.map((header, index) => (
                      <th key={index}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {message.data.rows.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {row.map((cell, cellIndex) => (
                        <td key={cellIndex}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        case 'assessment':
          return (
            <div className="assessment-card">
              <h3>{message.data.location}</h3>
              <div className={`status-badge ${message.data.category.toLowerCase()}`}>
                {message.data.category}
              </div>
              <div className="assessment-details">
                <div className="detail-item">
                  <span>Annual Recharge:</span>
                  <span>{message.data.annualRecharge} mcm</span>
                </div>
                <div className="detail-item">
                  <span>Total Extraction:</span>
                  <span>{message.data.totalExtraction} mcm</span>
                </div>
                <div className="detail-item">
                  <span>Stage of Extraction:</span>
                  <span>{message.data.extractionStage}%</span>
                </div>
              </div>
            </div>
          );
        default:
          return <p className="message-text">{message.text}</p>;
      }
    }
    
    return <p className="message-text">{message.text}</p>;
  };

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