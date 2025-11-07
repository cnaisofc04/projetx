
import { useState } from 'react';
import Logo from './Logo';

export default function HairColor({ user, onNext }) {
  const [hairColorValue, setHairColorValue] = useState(50);

  const hairColors = [
    { value: 0, color: '#000000', label: 'Noir' },
    { value: 16, color: '#2C1810', label: 'Brun foncé' },
    { value: 33, color: '#5C3A21', label: 'Châtain' },
    { value: 50, color: '#8B6F47', label: 'Châtain clair' },
    { value: 66, color: '#C4A574', label: 'Blond foncé' },
    { value: 83, color: '#E5D3B3', label: 'Blond' },
    { value: 100, color: '#F5E6D3', label: 'Blond platine' }
  ];

  const getHairColorFromValue = (value) => {
    // Interpolation entre les couleurs
    for (let i = 0; i < hairColors.length - 1; i++) {
      if (value >= hairColors[i].value && value <= hairColors[i + 1].value) {
        const ratio = (value - hairColors[i].value) / (hairColors[i + 1].value - hairColors[i].value);
        return {
          color: interpolateColor(hairColors[i].color, hairColors[i + 1].color, ratio),
          label: value < (hairColors[i].value + hairColors[i + 1].value) / 2 
            ? hairColors[i].label 
            : hairColors[i + 1].label
        };
      }
    }
    return hairColors[0];
  };

  const interpolateColor = (color1, color2, ratio) => {
    const hex = (x) => {
      const h = x.toString(16);
      return h.length === 1 ? '0' + h : h;
    };

    const r1 = parseInt(color1.substring(1, 3), 16);
    const g1 = parseInt(color1.substring(3, 5), 16);
    const b1 = parseInt(color1.substring(5, 7), 16);

    const r2 = parseInt(color2.substring(1, 3), 16);
    const g2 = parseInt(color2.substring(3, 5), 16);
    const b2 = parseInt(color2.substring(5, 7), 16);

    const r = Math.round(r1 + (r2 - r1) * ratio);
    const g = Math.round(g1 + (g2 - g1) * ratio);
    const b = Math.round(b1 + (b2 - b1) * ratio);

    return '#' + hex(r) + hex(g) + hex(b);
  };

  const currentHairColor = getHairColorFromValue(hairColorValue);

  const handleSubmit = () => {
    onNext({ hairColor: currentHairColor.label, hairColorValue });
  };

  return (
    <div className="hair-color">
      <div className="form-content">
        <Logo size={60} />
        <h2>Couleur de vos cheveux</h2>
        <p className="step-indicator">Étape 7/12</p>
        <p className="subtitle">Déplacez le slider pour sélectionner votre couleur de cheveux</p>

        <div className="hair-color-preview">
          <div 
            className="hair-color-circle"
            style={{ backgroundColor: currentHairColor.color }}
          ></div>
          <h3 className="hair-color-label">{currentHairColor.label}</h3>
        </div>

        <div className="preference-item">
          <div className="preference-header">
            <label>Couleur des cheveux</label>
            <span className="preference-value">{hairColorValue}%</span>
          </div>
          
          <div className="slider-labels">
            <span>🖤 Noir</span>
            <span>💛 Blond platine</span>
          </div>

          <input
            type="range"
            min="0"
            max="100"
            value={hairColorValue}
            onChange={(e) => setHairColorValue(parseInt(e.target.value))}
            className="hair-color-slider"
            style={{
              background: `linear-gradient(to right, #000000 0%, #2C1810 16%, #5C3A21 33%, #8B6F47 50%, #C4A574 66%, #E5D3B3 83%, #F5E6D3 100%)`
            }}
          />
        </div>

        <button className="primary-button" onClick={handleSubmit}>
          Continuer
        </button>
      </div>
    </div>
  );
}
