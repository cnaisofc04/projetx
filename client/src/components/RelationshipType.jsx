import { useState } from 'react';
import Logo from './Logo';

export default function RelationshipType({ user, onNext }) {
  const [preferences, setPreferences] = useState({
    serious: 50,
    casual: 50,
    marriage: 50,
    nothing_serious: 50,
    fun: 50
  });

  const relationshipTypes = [
    { id: 'serious', label: 'Relation sérieuse', icon: '💕' },
    { id: 'casual', label: 'Plan d\'un soir', icon: '🌙' },
    { id: 'marriage', label: 'Je veux me marier', icon: '💍' },
    { id: 'nothing_serious', label: 'Rien de sérieux', icon: '😊' },
    { id: 'fun', label: 'Me divertir', icon: '🎉' }
  ];

  const getPreferenceLabel = (value) => {
    if (value < 25) return 'Pas intéressé(e)';
    if (value < 45) return 'Peu intéressé(e)';
    if (value >= 45 && value <= 55) return 'Neutre';
    if (value > 75) return 'Très intéressé(e)';
    return 'Intéressé(e)';
  };

  const handleSubmit = () => {
    onNext({ relationshipPreferences: preferences });
  };

  return (
    <div className="relationship-type">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Que recherchez-vous ?</h2>
        <p className="step-indicator">Étape 3/9</p>
        <p className="subtitle">Ajustez votre intérêt pour chaque type de relation (50% = neutre)</p>

        <div className="preferences-container">
          {relationshipTypes.map(type => (
            <div key={type.id} className="preference-item">
              <div className="preference-header">
                <label>
                  <span className="type-icon-small">{type.icon}</span> {type.label}
                </label>
                <span className="preference-value">{preferences[type.id]}%</span>
              </div>
              
              <div className="slider-labels">
                <span>Pas intéressé</span>
                <span>Très intéressé</span>
              </div>

              <input
                type="range"
                min="0"
                max="100"
                value={preferences[type.id]}
                onChange={(e) => setPreferences({...preferences, [type.id]: parseInt(e.target.value)})}
                className="preference-slider"
              />

              <div className="preference-description">
                {getPreferenceLabel(preferences[type.id])}
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
