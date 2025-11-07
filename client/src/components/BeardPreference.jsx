import { useState } from 'react';
import Logo from './Logo';
import SliderPreference from './shared/SliderPreference';

export default function BeardPreference({ user, onNext }) {
  const [beardPreference, setBeardPreference] = useState(50);

  const handleSubmit = () => {
    onNext({ beardPreference });
  };

  return (
    <div className="beard-preference">
      <div className="form-content">
        <Logo size={60} />
        <h2>Préférence de barbe</h2>
        <p className="step-indicator">Étape 6/9</p>
        <p className="subtitle">
          Indiquez votre préférence pour les hommes barbus (50% = aucune préférence)
        </p>

        <div className="preferences-container">
          <SliderPreference
            label="Hommes avec barbe"
            value={beardPreference}
            onChange={setBeardPreference}
            leftLabel="Sans barbe"
            rightLabel="Avec barbe"
          />
        </div>

        <button className="primary-button" onClick={handleSubmit}>
          Continuer
        </button>
      </div>
    </div>
  );
}
