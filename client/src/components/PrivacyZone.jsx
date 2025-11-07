import { useState } from 'react';
import Logo from './Logo';

export default function PrivacyZone({ user, onNext }) {
  const [privacyData, setPrivacyData] = useState({
    enablePrivacyZone: false,
    addresses: [],
    radius: 5
  });
  const [currentAddress, setCurrentAddress] = useState('');

  const addAddress = () => {
    if (currentAddress.trim() && privacyData.addresses.length < 5) {
      setPrivacyData({
        ...privacyData,
        addresses: [...privacyData.addresses, currentAddress.trim()]
      });
      setCurrentAddress('');
    }
  };

  const removeAddress = (index) => {
    setPrivacyData({
      ...privacyData,
      addresses: privacyData.addresses.filter((_, i) => i !== index)
    });
  };

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
                <label>Adresse(s) ou lieu(x) *</label>
                <div className="tags-list">
                  {privacyData.addresses.map((addr, index) => (
                    <span key={index} className="tag">
                      📍 {addr}
                      <button type="button" onClick={() => removeAddress(index)}>×</button>
                    </span>
                  ))}
                </div>
                <div className="custom-input-section">
                  <input
                    type="text"
                    value={currentAddress}
                    onChange={(e) => setCurrentAddress(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addAddress())}
                    placeholder="Ex: 123 rue de la Paix, Paris"
                  />
                  <button
                    type="button"
                    onClick={addAddress}
                    disabled={privacyData.addresses.length >= 5 || !currentAddress.trim()}
                  >
                    Ajouter
                  </button>
                </div>
                <p className="helper-text">Vos adresses ne seront jamais partagées (max 5)</p>
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
          disabled={privacyData.enablePrivacyZone && privacyData.addresses.length === 0}
        >
          Continuer
        </button>
      </div>
    </div>
  );
}
