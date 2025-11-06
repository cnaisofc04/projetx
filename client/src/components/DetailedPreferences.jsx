import { useState } from 'react';
import Logo from './Logo';

export default function DetailedPreferences({ user, onNext }) {
  const [preferences, setPreferences] = useState({
    tattoos: 50,
    smoking: 50,
    diet: 50,
    hairColor: 50,
    height: 50,
    bodyHair: 50,
    bodyType: 50,
    style: 50
  });

  const getPreferenceLabel = (value, labels) => {
    if (value < 25) return labels.strong_left;
    if (value < 45) return labels.slight_left;
    if (value >= 45 && value <= 55) return 'Aucune préférence';
    if (value > 75) return labels.strong_right;
    return labels.slight_right;
  };

  const preferenceConfigs = {
    tattoos: {
      label: 'Tatouages',
      left: 'Sans tatouage',
      right: 'Avec tatouages',
      strong_left: 'Préférence forte : sans tatouage',
      slight_left: 'Préférence légère : sans tatouage',
      strong_right: 'Préférence forte : avec tatouages',
      slight_right: 'Préférence légère : avec tatouages'
    },
    smoking: {
      label: 'Tabac',
      left: 'Non-fumeur',
      right: 'Fumeur',
      strong_left: 'Préférence forte : non-fumeur',
      slight_left: 'Préférence légère : non-fumeur',
      strong_right: 'Préférence forte : fumeur',
      slight_right: 'Préférence légère : fumeur'
    },
    diet: {
      label: 'Régime alimentaire',
      left: 'Végétarien',
      right: 'Omnivore',
      strong_left: 'Préférence forte : végétarien',
      slight_left: 'Préférence légère : végétarien',
      strong_right: 'Préférence forte : omnivore',
      slight_right: 'Préférence légère : omnivore'
    },
    hairColor: {
      label: 'Couleur de cheveux',
      left: 'Blonde',
      right: 'Brune/Rousse',
      strong_left: 'Préférence forte : blonde',
      slight_left: 'Préférence légère : blonde',
      strong_right: 'Préférence forte : brune/rousse',
      slight_right: 'Préférence légère : brune/rousse'
    },
    height: {
      label: 'Taille',
      left: 'Petite',
      right: 'Grande',
      strong_left: 'Préférence forte : petite taille',
      slight_left: 'Préférence légère : petite taille',
      strong_right: 'Préférence forte : grande taille',
      slight_right: 'Préférence légère : grande taille'
    },
    bodyHair: {
      label: user?.gender === 'man' ? 'Pilosité corporelle' : 'Pilosité (partenaire)',
      left: 'Rasé',
      right: 'Poilu',
      strong_left: 'Préférence forte : rasé',
      slight_left: 'Préférence légère : rasé',
      strong_right: 'Préférence forte : poilu',
      slight_right: 'Préférence légère : poilu'
    },
    bodyType: {
      label: 'Morphologie',
      left: 'Mince',
      right: 'Athlétique/Robuste',
      strong_left: 'Préférence forte : mince',
      slight_left: 'Préférence légère : mince',
      strong_right: 'Préférence forte : athlétique/robuste',
      slight_right: 'Préférence légère : athlétique/robuste'
    },
    style: {
      label: 'Style vestimentaire',
      left: 'Casual',
      right: 'Élégant',
      strong_left: 'Préférence forte : casual',
      slight_left: 'Préférence légère : casual',
      strong_right: 'Préférence forte : élégant',
      slight_right: 'Préférence légère : élégant'
    }
  };

  const handleSubmit = () => {
    onNext({ detailedPreferences: preferences });
  };

  return (
    <div className="detailed-preferences">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Vos préférences détaillées</h2>
        <p className="step-indicator">Étape 5/7</p>
        <p className="subtitle">
          Ajustez chaque slider selon vos préférences (50% = aucune préférence)
        </p>

        <div className="preferences-container">
          {Object.entries(preferenceConfigs).map(([key, config]) => (
            <div key={key} className="preference-item">
              <div className="preference-header">
                <label>{config.label}</label>
                <span className="preference-value">{preferences[key]}%</span>
              </div>
              
              <div className="slider-labels">
                <span>{config.left}</span>
                <span>{config.right}</span>
              </div>

              <input
                type="range"
                min="0"
                max="100"
                value={preferences[key]}
                onChange={(e) => setPreferences({...preferences, [key]: parseInt(e.target.value)})}
                className="preference-slider"
              />

              <div className="preference-description">
                {getPreferenceLabel(preferences[key], config)}
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
