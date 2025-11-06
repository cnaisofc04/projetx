import { useState } from 'react';
import Logo from './Logo';

export default function ProfileSetup({ user, onComplete }) {
  const [photos, setPhotos] = useState([]);
  const [bio, setBio] = useState('');
  const [profession, setProfession] = useState('');
  const [interests, setInterests] = useState([]);
  const [interestInput, setInterestInput] = useState('');

  const handlePhotoAdd = () => {
    if (photos.length < 6) {
      setPhotos([...photos, `https://via.placeholder.com/300?text=Photo+${photos.length + 1}`]);
    }
  };

  const handleInterestAdd = () => {
    if (interestInput.trim() && interests.length < 10) {
      setInterests([...interests, interestInput.trim()]);
      setInterestInput('');
    }
  };

  const removeInterest = (index) => {
    setInterests(interests.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    if (photos.length > 0 && bio.length >= 50 && profession) {
      onComplete({
        photos,
        bio,
        profession,
        interests
      });
    }
  };

  const canSubmit = photos.length > 0 && bio.length >= 50 && profession;

  return (
    <div className="profile-setup">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Complétez votre profil</h2>
        <p className="step-indicator">Étape 6/7</p>

        <div className="profile-section">
          <h3>Photos ({photos.length}/6)</h3>
          <div className="photo-grid">
            {photos.map((photo, index) => (
              <div key={index} className="photo-placeholder">
                <img src={photo} alt={`Photo ${index + 1}`} />
              </div>
            ))}
            {photos.length < 6 && (
              <button className="add-photo-btn" onClick={handlePhotoAdd}>
                + Ajouter une photo
              </button>
            )}
          </div>
        </div>

        <div className="profile-section">
          <h3>Bio (minimum 50 caractères) *</h3>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            placeholder="Parlez de vous, de vos passions, de ce que vous recherchez..."
            rows="5"
            maxLength="500"
          />
          <div className="char-count">{bio.length}/500 caractères</div>
        </div>

        <div className="profile-section">
          <h3>Profession *</h3>
          <input
            type="text"
            value={profession}
            onChange={(e) => setProfession(e.target.value)}
            placeholder="Votre métier"
          />
        </div>

        <div className="profile-section">
          <h3>Centres d'intérêt (max 10)</h3>
          <div className="interest-input">
            <input
              type="text"
              value={interestInput}
              onChange={(e) => setInterestInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleInterestAdd())}
              placeholder="Sport, musique, cuisine..."
            />
            <button onClick={handleInterestAdd} disabled={interests.length >= 10}>
              Ajouter
            </button>
          </div>
          <div className="interests-tags">
            {interests.map((interest, index) => (
              <span key={index} className="interest-tag">
                {interest}
                <button onClick={() => removeInterest(index)}>×</button>
              </span>
            ))}
          </div>
        </div>

        <button 
          className="primary-button" 
          onClick={handleSubmit}
          disabled={!canSubmit}
        >
          {canSubmit ? 'Créer mon profil' : 'Complétez les champs requis'}
        </button>
      </div>
    </div>
  );
}
