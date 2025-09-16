import React from 'react';
import { FaChartBar, FaDatabase, FaMapMarkedAlt, FaFileAlt } from 'react-icons/fa';

const ToolButton = ({ icon, label, isSelected, onClick }) => {
  return (
    <button
      className={`tool-button ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      {icon}
      {label}
    </button>
  );
};

// REFACTORED: Now receives 'onSelectTool' prop for clarity
const ToolsBar = ({ selectedTools, onSelectTool, isVisible }) => {
  const tools = [
    { id: 'research', label: 'Research Data', icon: <FaFileAlt /> },
    { id: 'graph', label: 'Generate Graphs', icon: <FaChartBar /> },
    { id: 'trend', label: 'Trend Analysis', icon: <FaDatabase /> },
    { id: 'local', label: 'Check your local area', icon: <FaMapMarkedAlt /> },
  ];

  return (
    <div className={`tools-bar ${!isVisible ? 'hidden' : ''}`}>
      <div className="tools-container">
        {tools.map((tool) => (
          <ToolButton
            key={tool.id}
            icon={tool.icon}
            label={tool.label}
            isSelected={selectedTools.includes(tool.id)}
            onClick={() => onSelectTool(tool.id)} // REFACTORED: Using clearer prop name
          />
        ))}
      </div>
    </div>
  );
};

export default ToolsBar;