import { useState } from 'react';
import Logo from './Logo';
import SliderPreference from './shared/SliderPreference';

export default function DetailedPreferences({ user, onNext }) {
  const [preferences, setPreferences] = useState({
    tattoos: 50,
    smoking: 50,
    diet: 50,
    hairBlonde: 50,
    hairBrunette: 50,
    hairRedhead: 50,
    height: 50,
    bodyHair: 50,
    bodyType: 50,
    style: 50
  });

  const handleSubmit = () => {
    onNext({ detailedPreferences: preferences });
  };

  return (
    <div className="detailed-preferences">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Vos préférences détaillées</h2>
        <p className="step-indicator">Étape 8/12</p>
        <p className="subtitle">
          Ajustez chaque slider selon vos préférences (50% = aucune préférence)
        </p>

        <div className="preferences-container">
          <SliderPreference
            label="Tatouages"
            value={preferences.tattoos}
            onChange={(val) => setPreferences({...preferences, tattoos: val})}
            leftLabel="Sans tatouage"
            rightLabel="Avec tatouages"
          />

          <SliderPreference
            label="Tabac"
            value={preferences.smoking}
            onChange={(val) => setPreferences({...preferences, smoking: val})}
            leftLabel="Non-fumeur"
            rightLabel="Fumeur"
          />

          <SliderPreference
            label="Régime alimentaire"
            value={preferences.diet}
            onChange={(val) => setPreferences({...preferences, diet: val})}
            leftLabel="Végétarien"
            rightLabel="Omnivore"
          />

          <div className="hair-section">
            <h3 className="section-title">Couleur de cheveux</h3>

            <SliderPreference
              label="Cheveux blonds"
              value={preferences.hairBlonde}
              onChange={(val) => setPreferences({...preferences, hairBlonde: val})}
              leftLabel="Pas intéressé(e)"
              rightLabel="Très intéressé(e)"
            />

            <SliderPreference
              label="Cheveux bruns"
              value={preferences.hairBrunette}
              onChange={(val) => setPreferences({...preferences, hairBrunette: val})}
              leftLabel="Pas intéressé(e)"
              rightLabel="Très intéressé(e)"
            />

            <SliderPreference
              label="Cheveux roux"
              value={preferences.hairRedhead}
              onChange={(val) => setPreferences({...preferences, hairRedhead: val})}
              leftLabel="Pas intéressé(e)"
              rightLabel="Très intéressé(e)"
            />
          </div>

          <SliderPreference
            label="Taille"
            value={preferences.height}
            onChange={(val) => setPreferences({...preferences, height: val})}
            leftLabel="Petite"
            rightLabel="Grande"
          />

          <SliderPreference
            label={user?.gender === 'man' ? 'Pilosité corporelle' : 'Pilosité (partenaire)'}
            value={preferences.bodyHair}
            onChange={(val) => setPreferences({...preferences, bodyHair: val})}
            leftLabel="Rasé(e)"
            rightLabel="Poilu(e)"
          />

          <SliderPreference
            label="Morphologie"
            value={preferences.bodyType}
            onChange={(val) => setPreferences({...preferences, bodyType: val})}
            leftLabel="Mince"
            rightLabel="Athlétique/Robuste"
          />

          <SliderPreference
            label="Style vestimentaire"
            value={preferences.style}
            onChange={(val) => setPreferences({...preferences, style: val})}
            leftLabel="Casual"
            rightLabel="Élégant"
          />
        </div>

        <button className="primary-button" onClick={handleSubmit}>
          Continuer
        </button>
      </div>
    </div>
  );
}