
import { useState } from 'react';
import Logo from './Logo';

export default function Religion({ user, onNext }) {
  const [selectedReligion, setSelectedReligion] = useState('');

  const religions = [
    { id: 'christianisme', label: 'Christianisme', icon: '✝️' },
    { id: 'islam', label: 'Islam', icon: '☪️' },
    { id: 'judaisme', label: 'Judaïsme', icon: '✡️' },
    { id: 'bouddhisme', label: 'Bouddhisme', icon: '☸️' },
    { id: 'hindouisme', label: 'Hindouisme', icon: '🕉️' },
    { id: 'athee', label: 'Athée', icon: '🔬' },
    { id: 'agnostique', label: 'Agnostique', icon: '❓' },
    { id: 'autre', label: 'Autre', icon: '🌟' }
  ];

  const handleSubmit = () => {
    if (selectedReligion) {
      onNext({ religion: selectedReligion });
    }
  };

  return (
    <div className="religion">
      <div className="form-content">
        <Logo size={60} />
        <h2>Votre religion</h2>
        <p className="step-indicator">Étape 5/11</p>
        <p className="subtitle">Sélectionnez votre religion ou conviction</p>

        <div className="orientation-grid">
          {religions.map((religion) => (
            <div
              key={religion.id}
              className={selectedReligion === religion.id ? 'orientation-card active' : 'orientation-card'}
              onClick={() => setSelectedReligion(religion.id)}
            >
              <span className="orientation-icon">{religion.icon}</span>
              <span className="orientation-label">{religion.label}</span>
            </div>
          ))}
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={!selectedReligion}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
