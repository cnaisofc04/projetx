import { useState } from 'react';
import Logo from './Logo';
import PhotoUploader from './shared/PhotoUploader';
import ChipSelector from './shared/ChipSelector';

export default function ProfileSetup({ user, onComplete }) {
  const [photos, setPhotos] = useState([]);
  const [professions, setProfessions] = useState([]);
  const [customProfession, setCustomProfession] = useState('');
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

  const alphabeticRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;

  const validateAlphabetic = (value) => {
    return alphabeticRegex.test(value);
  };

  const addCustomItem = (value, list, setter, inputSetter, icon = '✨') => {
    const trimmedValue = value.trim();

    if (!trimmedValue) {
      return;
    }

    if (!validateAlphabetic(trimmedValue)) {
      alert('⚠️ Seuls les lettres, espaces, tirets et apostrophes sont autorisés. Pas de chiffres ou caractères spéciaux.');
      return;
    }

    if (list.length >= 10) {
      return;
    }

    const newItem = {
      id: `custom_${Date.now()}_${Math.random()}`,
      label: trimmedValue,
      icon: icon,
      isCustom: true
    };
    setter([...list, newItem]);
    inputSetter('');
  };

  const removeItem = (index, list, setter) => {
    setter(list.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (photos.length > 0 && professions.length > 0 && professionalStatus.length > 0) {
      const completeProfile = {
        photos,
        professions,
        professionalStatus,
        interests,
        favoriteBooks,
        favoriteMovies,
        favoriteMusic
      };

      // Sauvegarder via le backend Flask (évite les problèmes CORS)
      try {
        console.log('📤 Envoi au backend pour:', user.email);
        console.log('📦 Données:', completeProfile);

        const response = await fetch('http://0.0.0.0:5000/api/save-profile', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(completeProfile)
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Erreur serveur');
        }

        const result = await response.json();
        console.log('✅ Profil sauvegardé avec succès:', result);
        onComplete(completeProfile);
      } catch (error) {
        console.error('❌ Erreur sauvegarde profil:', error);
        alert(`Erreur sauvegarde: ${error.message}\nVeuillez réessayer ou contacter le support.`);
      }
    }
  };

  const canSubmit = photos.length > 0 && professions.length > 0 && professionalStatus.length > 0;
  const currentStepNumber = user?.gender === 'woman' ? '10-11/11' : '9-11/11';

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
          <h3>Profession(s) *</h3>
          <div className="tags-list">
            {professions.map((prof, index) => (
              <span key={prof.id || index} className="tag">
                {prof.icon} {prof.label}
                <button type="button" onClick={() => removeItem(index, professions, setProfessions)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customProfession}
              onChange={(e) => setCustomProfession(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customProfession, professions, setProfessions, setCustomProfession, '💼'))}
              placeholder="Ex: Développeur, Professeur, Designer..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customProfession, professions, setProfessions, setCustomProfession, '💼')}
              disabled={professions.length >= 5}
            >
              Ajouter
            </button>
          </div>
        </div>

        <div className="profile-section">
          <h3>Centres d'intérêt</h3>
          <ChipSelector
            options={interestPresets}
            selected={interests.filter(i => !i.isCustom).map(i => i.id || i)}
            onToggle={(selected) => {
              const customInterests = interests.filter(i => i.isCustom);
              const presetInterests = selected.map(id => 
                interestPresets.find(preset => preset.id === id) || id
              );
              setInterests([...presetInterests, ...customInterests]);
            }}
            maxSelection={10}
          />
          <div className="tags-list">
            {interests.map((interest, index) => {
              if (typeof interest === 'object' && interest.label) {
                return (
                  <span key={interest.id || index} className="tag">
                    {interest.icon} {interest.label}
                    <button type="button" onClick={() => removeItem(index, interests, setInterests)}>×</button>
                  </span>
                );
              }
              return null;
            })}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customInterest}
              onChange={(e) => setCustomInterest(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customInterest, interests, setInterests, setCustomInterest, '✨'))}
              placeholder="Ajouter un intérêt personnalisé"
            />
            <button
              type="button"
              onClick={() => addCustomItem(customInterest, interests, setInterests, setCustomInterest, '✨')}
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
              <span key={book.id || index} className="tag">
                {book.icon} {book.label}
                <button type="button" onClick={() => removeItem(index, favoriteBooks, setFavoriteBooks)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customBook}
              onChange={(e) => setCustomBook(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customBook, favoriteBooks, setFavoriteBooks, setCustomBook, '📚'))}
              placeholder="Ex: 1984, Le Petit Prince..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customBook, favoriteBooks, setFavoriteBooks, setCustomBook, '📚')}
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
              <span key={movie.id || index} className="tag">
                {movie.icon} {movie.label}
                <button type="button" onClick={() => removeItem(index, favoriteMovies, setFavoriteMovies)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customMovie}
              onChange={(e) => setCustomMovie(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customMovie, favoriteMovies, setFavoriteMovies, setCustomMovie, '🎬'))}
              placeholder="Ex: Inception, La La Land..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customMovie, favoriteMovies, setFavoriteMovies, setCustomMovie, '🎬')}
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
              <span key={artist.id || index} className="tag">
                {artist.icon} {artist.label}
                <button type="button" onClick={() => removeItem(index, favoriteMusic, setFavoriteMusic)}>×</button>
              </span>
            ))}
          </div>
          <div className="custom-input-section">
            <input
              type="text"
              value={customMusic}
              onChange={(e) => setCustomMusic(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem(customMusic, favoriteMusic, setFavoriteMusic, setCustomMusic, '🎵'))}
              placeholder="Ex: Beyoncé, Daft Punk, Mozart..."
            />
            <button
              type="button"
              onClick={() => addCustomItem(customMusic, favoriteMusic, setFavoriteMusic, setCustomMusic, '🎵')}
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