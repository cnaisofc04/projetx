import { useState } from 'react';
import Logo from './Logo';

export default function PsychologyQuestions({ user, onNext }) {
  const [answers, setAnswers] = useState({
    shy: null,
    introverted: null
  });

  const handleSubmit = () => {
    if (answers.shy !== null && answers.introverted !== null) {
      onNext(answers);
    }
  };

  return (
    <div className="psychology-questions">
      <div className="form-content">
        <Logo size={60} />
        <h2>Apprenons à vous connaître</h2>
        <p className="step-indicator">Étape 2/7</p>

        <div className="questions-container">
          <div className="question-card">
            <h3>Vous êtes timide ?</h3>
            <div className="answer-buttons">
              <button
                className={answers.shy === true ? 'answer-btn active' : 'answer-btn'}
                onClick={() => setAnswers({...answers, shy: true})}
              >
                Oui
              </button>
              <button
                className={answers.shy === false ? 'answer-btn active' : 'answer-btn'}
                onClick={() => setAnswers({...answers, shy: false})}
              >
                Non
              </button>
            </div>
          </div>

          <div className="question-card">
            <h3>Vous êtes introverti ?</h3>
            <div className="answer-buttons">
              <button
                className={answers.introverted === true ? 'answer-btn active' : 'answer-btn'}
                onClick={() => setAnswers({...answers, introverted: true})}
              >
                Oui
              </button>
              <button
                className={answers.introverted === false ? 'answer-btn active' : 'answer-btn'}
                onClick={() => setAnswers({...answers, introverted: false})}
              >
                Non
              </button>
            </div>
          </div>
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={answers.shy === null || answers.introverted === null}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
