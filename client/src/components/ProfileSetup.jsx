import { useState } from 'react';
import Logo from './Logo';
import PhotoUploader from './shared/PhotoUploader';
import ChipSelector from './shared/ChipSelector';

export default function ProfileSetup({ user, onComplete }) {
  const [photos, setPhotos] = useState([]);
  const [profession, setProfession] = useState('');
  const [professionalStatus, setProfessionalStatus] = useState([]);
  const [interests, setInterests] = useState([]);
  const [customInterest, setCustomInterest] = useState('');
  const [favoriteBooks, setFavoriteBooks] = useState([]);
  const [customBook, setCustomBook] = useState('');
  const [favoriteMovies, setFavoriteMovies] = useState([]);
  const [customMovie, setCustomMovie] = useState('');
  const [favoriteMusic, setFavoriteMusic] = useState([]);
  const [customMusic, setCustomMusic] = useState('');

  const professionalStatusOptions = [
    { id: 'student', label: 'Étudiant(e)', icon: '🎓' },
    { id: 'employed', label: 'En activité', icon: '💼' },
    { id: 'unemployed', label: 'En recherche', icon: '🔍' },
    { id: 'retired', label: 'Retraité(e)', icon: '🏖️' },
    { id: 'entrepreneur', label: 'Entrepreneur', icon: '🚀' },
    { id: 'freelance', label: 'Freelance', icon: '💻' }
  ];

  const interestPresets = [
    { id: 'sport', label: 'Sport', icon: '⚽' },
    { id: 'travel', label: 'Voyages', icon: '✈️' },
    { id: 'music', label: 'Musique', icon: '🎵' },
    { id: 'cinema', label: 'Cinéma', icon: '🎬' },
    { id: 'reading', label: 'Lecture', icon: '📚' },
    { id: 'cooking', label: 'Cuisine', icon: '👨‍🍳' },
    { id: 'art', label: 'Art', icon: '🎨' },
    { id: 'nature', label: 'Nature', icon: '🌳' },
    { id: 'gaming', label: 'Jeux vidéo', icon: '🎮' },
    { id: 'photography', label: 'Photo', icon: '📸' }
  ];

  const addCustomItem = (value, list, setter, inputSetter) => {
    if (value.trim() && list.length < 10) {
      setter([...list, value.trim()]);
      inputSetter('');
    }
  };

  const removeItem = (index, list, setter) => {
    setter(list.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    if (photos.length > 0 && profession && professionalStatus.length > 0) {
      onComplete({
        photos,
        profession,
        professionalStatus,
        interests,
        favoriteBooks,
        favoriteMovies,
        favoriteMusic
      });
    }
  };

  const canSubmit = photos.length > 0 && profession && professionalStatus.length > 0;
  const currentStepNumber = user?.gender === 'woman' ? '8/9' : '7/9';

  return (
    <div className="profile-setup">
      <div className="form-content wide">
        <Logo size={60} />
        <h2>Complétez votre profil</h2>
        <p className="step-indicator">Étape {currentStepNumber}</p>

        <PhotoUploader photos={photos} onPhotosChange={setPhotos} maxPhotos={6} />

        <div className="profile-section">
          <h3>Situation professionnelle *</h3>
          <ChipSelector
            options={professionalStatusOptions}
            selected={professionalStatus}
            onToggle={setProfessionalStatus}
            maxSelection={2}
          />
        </div>

        <div className="profile-section">
          <h3>Profession *</h3>
          <input
            type="text"
            value={profession}
            onChange={(e) => setProfession(e.target.value)}
            placeholder="Ex: Développeur, Professeur, Designer..."
          />
        </div>

        <div className="profile-section">
          <h3>Centres d'intérêt</h3>
          <ChipSelector
            options={interestPresets}
            selected={interests}
            onToggle={setInterests}
            maxSelection={10}
          />
          <div className="custom-input-section">
            <input
              type="text"
              value={customInterest}
              onChange={(e) => setCustomInterest(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customInterest, interests, setInterests, setCustomInterest))}
              placeholder="Ajouter un intérêt personnalisé"
            />
            <button
              type="button"
              onClick={() => addCustomItem(customInterest, interests, setInterests, setCustomInterest)}
              disabled={interests.length >= 10}
            >
              Ajouter
            </button>
          </div>
        </div>

        <div className="profile-section">
          <h3>Livres préférés</h3>
          <div className="tags-list">
            {favoriteBooks.map((book, index) => (
              <span key={index} className="tag">
                📚 {book}
                <button type="button" onClick={() => removeItem(index, favoriteBooks, setFavoriteBooks)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customBook}
              onChange={(e) => setCustomBook(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customBook, favoriteBooks, setFavoriteBooks, setCustomBook))}
              placeholder="Ex: 1984, Le Petit Prince..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customBook, favoriteBooks, setFavoriteBooks, setCustomBook)}
              disabled={favoriteBooks.length >= 10}
            >
              Ajouter
            </button>
          </div>
        </div>

        <div className="profile-section">
          <h3>Films préférés</h3>
          <div className="tags-list">
            {favoriteMovies.map((movie, index) => (
              <span key={index} className="tag">
                🎬 {movie}
                <button type="button" onClick={() => removeItem(index, favoriteMovies, setFavoriteMovies)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customMovie}
              onChange={(e) => setCustomMovie(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customMovie, favoriteMovies, setFavoriteMovies, setCustomMovie))}
              placeholder="Ex: Inception, La La Land..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customMovie, favoriteMovies, setFavoriteMovies, setCustomMovie)}
              disabled={favoriteMovies.length >= 10}
            >
              Ajouter
            </button>
          </div>
        </div>

        <div className="profile-section">
          <h3>Musique / Artistes préférés</h3>
          <div className="tags-list">
            {favoriteMusic.map((artist, index) => (
              <span key={index} className="tag">
                🎵 {artist}
                <button type="button" onClick={() => removeItem(index, favoriteMusic, setFavoriteMusic)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customMusic}
              onChange={(e) => setCustomMusic(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customMusic, favoriteMusic, setFavoriteMusic, setCustomMusic))}
              placeholder="Ex: Beyoncé, Daft Punk, Mozart..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customMusic, favoriteMusic, setFavoriteMusic, setCustomMusic)}
              disabled={favoriteMusic.length >= 10}
            >
              Ajouter
            </button>
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
