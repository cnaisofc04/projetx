import { useState } from 'react';
import Logo from './Logo';

export default function PsychologyQuestions({ user, onNext }) {
  const [answers, setAnswers] = useState({
    shy: 50,
    introverted: 50
  });

  const getLabel = (value) => {
    if (value < 25) return 'Pas du tout';
    if (value < 45) return 'Un peu';
    if (value >= 45 && value <= 55) return 'Moyennement';
    if (value > 75) return 'Beaucoup';
    return 'Assez';
  };

  const handleSubmit = () => {
    onNext(answers);
  };

  return (
    <div className="psychology-questions">
      <div className="form-content">
        <Logo size={60} />
        <h2>Apprenons à vous connaître</h2>
        <p className="step-indicator">Étape 2/11</p>

        <div className="questions-container">
          <div className="question-card">
            <div className="preference-header">
              <h3>Vous êtes timide ?</h3>
              <span className="preference-value">{answers.shy}%</span>
            </div>
            <div className="slider-labels">
              <span>Pas du tout</span>
              <span>Très timide</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={answers.shy}
              onChange={(e) => setAnswers({...answers, shy: parseInt(e.target.value)})}
              className="preference-slider"
            />
            <div className="preference-description">
              {getLabel(answers.shy)}
            </div>
          </div>

          <div className="question-card">
            <div className="preference-header">
              <h3>Vous êtes introverti ?</h3>
              <span className="preference-value">{answers.introverted}%</span>
            </div>
            <div className="slider-labels">
              <span>Pas du tout</span>
              <span>Très introverti</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={answers.introverted}
              onChange={(e) => setAnswers({...answers, introverted: parseInt(e.target.value)})}
              className="preference-slider"
            />
            <div className="preference-description">
              {getLabel(answers.introverted)}
            </div>
          </div>
        </div>

        <button
          className="primary-button"
          onClick={handleSubmit}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}