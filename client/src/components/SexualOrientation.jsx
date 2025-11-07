import { useState } from 'react';
import Logo from './Logo';

export default function SexualOrientation({ user, onNext }) {
  const [preferences, setPreferences] = useState({
    hetero: 50,
    homo: 50,
    bi: 50,
    trans: 50
  });

  const orientations = [
    { id: 'hetero', label: 'Hétérosexuel(le)', icon: '👫' },
    { id: 'homo', label: 'Homosexuel(le)', icon: '👭' },
    { id: 'bi', label: 'Bisexuel(le)', icon: '💗' },
    { id: 'trans', label: 'Transgenre', icon: '🏳️‍⚧️' }
  ];

  const getPreferenceLabel = (value) => {
    if (value < 25) return 'Pas ouvert(e)';
    if (value < 45) return 'Peu ouvert(e)';
    if (value >= 45 && value <= 55) return 'Neutre';
    if (value > 75) return 'Très ouvert(e)';
    return 'Ouvert(e)';
  };

  const handleSubmit = () => {
    onNext({ sexualOrientationPreferences: preferences });
  };

  return (
    <div className="sexual-orientation">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Vos préférences d'orientation</h2>
        <p className="step-indicator">Étape 4/11</p>
        <p className="subtitle">Indiquez votre ouverture pour chaque orientation (50% = neutre)</p>

        <div className="preferences-container">
          {orientations.map(orientation => (
            <div key={orientation.id} className="preference-item">
              <div className="preference-header">
                <label>
                  <span className="type-icon-small">{orientation.icon}</span> {orientation.label}
                </label>
                <span className="preference-value">{preferences[orientation.id]}%</span>
              </div>
              
              <div className="slider-labels">
                <span>Pas ouvert</span>
                <span>Très ouvert</span>
              </div>

              <input
                type="range"
                min="0"
                max="100"
                value={preferences[orientation.id]}
                onChange={(e) => setPreferences({...preferences, [orientation.id]: parseInt(e.target.value)})}
                className="preference-slider"
              />

              <div className="preference-description">
                {getPreferenceLabel(preferences[orientation.id])}
              </div>
            </div>
          ))}
        </div>

        <button className="primary-button" onClick={handleSubmit}>
          Continuer
        </button>
      </div>
    </div>
  );
}
