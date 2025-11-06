import { useState } from 'react';
import Logo from './Logo';

export default function RelationshipType({ user, onNext }) {
  const [selected, setSelected] = useState(null);

  const relationshipTypes = [
    { id: 'serious', label: 'Relation sérieuse', icon: '💕' },
    { id: 'casual', label: 'Plan d\'un soir', icon: '🌙' },
    { id: 'marriage', label: 'Je veux me marier', icon: '💍' },
    { id: 'nothing_serious', label: 'Rien de sérieux', icon: '😊' },
    { id: 'fun', label: 'Me divertir', icon: '🎉' }
  ];

  const handleSubmit = () => {
    if (selected) {
      onNext({ relationshipType: selected });
    }
  };

  return (
    <div className="relationship-type">
      <div className="form-content">
        <Logo size={60} />
        <h2>Que recherchez-vous ?</h2>
        <p className="step-indicator">Étape 3/7</p>

        <div className="type-grid">
          {relationshipTypes.map(type => (
            <button
              key={type.id}
              className={selected === type.id ? 'type-card active' : 'type-card'}
              onClick={() => setSelected(type.id)}
            >
              <span className="type-icon">{type.icon}</span>
              <span className="type-label">{type.label}</span>
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
