import { useState } from 'react';
import Logo from './Logo';

export default function PrivacyZone({ user, onNext }) {
  const [privacyData, setPrivacyData] = useState({
    enablePrivacyZone: false,
    address: '',
    radius: 5
  });

  const handleSubmit = () => {
    onNext({ privacyShadowZone: privacyData });
  };

  return (
    <div className="privacy-zone">
      <div className="form-content">
        <Logo size={60} />
        <h2>Zone d'ombre</h2>
        <p className="step-indicator">Étape {user?.gender === 'woman' ? '7/9' : '6/9'}</p>
        <p className="subtitle">
          Définissez une zone où vous ne souhaitez pas être visible
        </p>

        <div className="privacy-section">
          <div className="toggle-section">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={privacyData.enablePrivacyZone}
                onChange={(e) => setPrivacyData({...privacyData, enablePrivacyZone: e.target.checked})}
              />
              <span>Activer la zone d'ombre</span>
            </label>
            <p className="helper-text">
              Si activé, vous ne serez pas visible et ne verrez pas les personnes dans cette zone
            </p>
          </div>

          {privacyData.enablePrivacyZone && (
            <>
              <div className="form-group">
                <label>Adresse ou lieu *</label>
                <input
                  type="text"
                  value={privacyData.address}
                  onChange={(e) => setPrivacyData({...privacyData, address: e.target.value})}
                  placeholder="Ex: 123 rue de la Paix, Paris"
                />
                <p className="helper-text">Votre adresse ne sera jamais partagée</p>
              </div>

              <div className="form-group">
                <label>Rayon de la zone : {privacyData.radius} km</label>
                <input
                  type="range"
                  min="1"
                  max="50"
                  value={privacyData.radius}
                  onChange={(e) => setPrivacyData({...privacyData, radius: parseInt(e.target.value)})}
                  className="preference-slider"
                />
                <div className="slider-labels">
                  <span>1 km</span>
                  <span>50 km</span>
                </div>
              </div>
            </>
          )}
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={privacyData.enablePrivacyZone && !privacyData.address}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
