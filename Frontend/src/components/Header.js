import React from 'react';
import { FiSun, FiMoon, FiPlusSquare } from 'react-icons/fi';

const Header = ({ theme, onThemeToggle, onNewChat }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="new-chat-btn" onClick={onNewChat} title="New Chat">
          <FiPlusSquare />
        </button>
        <img 
          src="/images/artha-logo.png" 
          alt="ArthaAI Logo" 
          className="logo circular" 
        />
        <h1>ArthaAI - INGRES AI Assistant</h1>
      </div>
      <div className="header-right">
        <img 
          src="https://cgwb.gov.in/themes/custom/cgwb/images/cgwb-updated-logo.png" 
          alt="CGWB Logo" 
          className="logo small-circular" 
        />
        <img 
          src="/images/ingres-logo.png" 
          alt="INGRES Logo" 
          className="logo small-circular" 
        />
        <button className="theme-toggle-btn" onClick={onThemeToggle} title="Toggle Theme">
          {theme === 'light' ? <FiMoon /> : <FiSun />}
        </button>
      </div>
    </header>
  );
};

export default Header;