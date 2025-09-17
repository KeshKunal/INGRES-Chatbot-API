import React from 'react';
import './SuggestedQuestions.css';

const SuggestedQuestions = ({ onQuestionClick }) => {
  const questions = [
    "What is the groundwater level in Bengaluru South, Karnataka?",
    "Show me groundwater extraction trends in Kolar",
    "Which districts are in the 'Over-Exploited' category in goa?",
    "What is the annual groundwater recharge in Chennai?",
    "Can you give me the ground water data of delhi highlighiting the critical parameters"
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