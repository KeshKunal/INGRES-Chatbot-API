import React, { useState } from 'react';
import { FiSun, FiMoon, FiPlusSquare, FiGlobe } from 'react-icons/fi';
import './Header.css';

const Header = ({ theme, onThemeToggle, onNewChat, onLanguageChange }) => {
  const [showLanguages, setShowLanguages] = useState(false);
  
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'te', name: 'తెలుగు' },
    { code: 'ta', name: 'தமிழ்' },
    { code: 'bn', name: 'বাংলা' },
    { code: 'mr', name: 'मराठी' },
    { code: 'gu', name: 'ગુજરાતી' },
    { code: 'kn', name: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'മലയാളം' },
  ];
  return (
    <header className="header">
      <div className="header-left">
        <button className="new-chat-btn" onClick={onNewChat} title="New Chat">
          <FiPlusSquare />
        </button>
        <img 
          src="/images/Artha AI Circular.png" 
          alt="ArthaAI Logo" 
          className="logo circular" 
        />
        <h1>ArthaAI - INGRES AI Assistant</h1>
      </div>
      <div className="header-right">
        <div className="language-selector">
          <button
            className="language-btn"
            onClick={() => setShowLanguages(!showLanguages)}
            title="Change Language"
          >
            <FiGlobe />
          </button>
          {showLanguages && (
            <div className="language-dropdown">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  className="language-option"
                  onClick={() => {
                    onLanguageChange(lang.code);
                    setShowLanguages(false);
                  }}
                >
                  {lang.name}
                </button>
              ))}
            </div>
          )}
        </div>
        <img 
          src="/images/cgwb-logo.png" 
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