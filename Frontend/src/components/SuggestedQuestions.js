import React from 'react';
import './SuggestedQuestions.css';

const SuggestedQuestions = ({ onQuestionClick }) => {
  const questions = [
    "What is the groundwater level in Karnataka?",
    "Show me groundwater extraction trends in Punjab",
    "Which districts are in the 'Over-Exploited' category?",
    "What is the annual groundwater recharge in Gujarat?",
    "Compare groundwater levels between 2020 and 2023"
  ];

  return (
    <div className="suggested-questions">
      <h4>Try asking about groundwater data:</h4>
      <div className="question-buttons">
        {questions.map((question, index) => (
          <button
            key={index}
            className="question-btn"
            onClick={() => onQuestionClick(question)}
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SuggestedQuestions;