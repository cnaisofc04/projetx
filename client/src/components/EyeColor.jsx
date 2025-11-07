
import { useState } from 'react';
import Logo from './Logo';

export default function EyeColor({ user, onNext }) {
  const [selectedColor, setSelectedColor] = useState('');

  const eyeColors = [
    { id: 'marron', label: 'Marron', icon: '🟤' },
    { id: 'bleu', label: 'Bleu', icon: '🔵' },
    { id: 'vert', label: 'Vert', icon: '🟢' },
    { id: 'noisette', label: 'Noisette', icon: '🟡' },
    { id: 'gris', label: 'Gris', icon: '⚪' },
    { id: 'noir', label: 'Noir', icon: '⚫' },
    { id: 'autre', label: 'Autre', icon: '🌈' }
  ];

  const handleSubmit = () => {
    if (selectedColor) {
      onNext({ eyeColor: selectedColor });
    }
  };

  return (
    <div className="eye-color">
      <div className="form-content">
        <Logo size={60} />
        <h2>Couleur de vos yeux</h2>
        <p className="step-indicator">Étape 6/11</p>
        <p className="subtitle">Sélectionnez la couleur de vos yeux</p>

        <div className="orientation-grid">
          {eyeColors.map((color) => (
            <div
              key={color.id}
              className={selectedColor === color.id ? 'orientation-card active' : 'orientation-card'}
              onClick={() => setSelectedColor(color.id)}
            >
              <span className="orientation-icon">{color.icon}</span>
              <span className="orientation-label">{color.label}</span>
            </div>
          ))}
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={!selectedColor}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
