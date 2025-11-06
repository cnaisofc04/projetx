import { useState } from 'react';
import Logo from './Logo';

export default function SexualOrientation({ user, onNext }) {
  const [selected, setSelected] = useState(null);

  const orientations = [
    { id: 'hetero', label: 'Hétérosexuel(le)', icon: '👫' },
    { id: 'homo', label: 'Homosexuel(le)', icon: '👭' },
    { id: 'bi', label: 'Bisexuel(le)', icon: '💗' },
    { id: 'trans', label: 'Transgenre', icon: '🏳️‍⚧️' }
  ];

  const handleSubmit = () => {
    if (selected) {
      onNext({ sexualOrientation: selected });
    }
  };

  return (
    <div className="sexual-orientation">
      <div className="form-content">
        <Logo size={60} />
        <h2>Votre orientation sexuelle</h2>
        <p className="step-indicator">Étape 4/7</p>

        <div className="orientation-grid">
          {orientations.map(orientation => (
            <button
              key={orientation.id}
              className={selected === orientation.id ? 'orientation-card active' : 'orientation-card'}
              onClick={() => setSelected(orientation.id)}
            >
              <span className="orientation-icon">{orientation.icon}</span>
              <span className="orientation-label">{orientation.label}</span>
            </button>
          ))}
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={!selected}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
