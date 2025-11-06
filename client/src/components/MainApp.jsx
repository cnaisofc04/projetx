import { useState } from 'react';
import Logo from './Logo';

export default function MainApp({ user, onLogout }) {
  const [currentTab, setCurrentTab] = useState('discover');
  const [currentProfileIndex, setCurrentProfileIndex] = useState(0);
  const [showPremium, setShowPremium] = useState(false);

  const mockProfiles = [
    {
      id: 1,
      name: 'Sophie',
      age: 26,
      city: 'Paris',
      profession: 'Designer graphique',
      bio: 'Passionnée de voyage et de photographie. Je cherche quelqu\'un avec qui partager de belles aventures.',
      photos: ['https://via.placeholder.com/400x500?text=Sophie'],
      interests: ['Photographie', 'Voyage', 'Yoga']
    },
    {
      id: 2,
      name: 'Marc',
      age: 29,
      city: 'Lyon',
      profession: 'Développeur',
      bio: 'Fan de jeux vidéo et de cuisine. Toujours partant pour découvrir de nouveaux restaurants.',
      photos: ['https://via.placeholder.com/400x500?text=Marc'],
      interests: ['Gaming', 'Cuisine', 'Cinéma']
    },
    {
      id: 3,
      name: 'Emma',
      age: 24,
      city: 'Marseille',
      profession: 'Professeure',
      bio: 'Amoureuse des livres et de la nature. Je recherche des moments authentiques.',
      photos: ['https://via.placeholder.com/400x500?text=Emma'],
      interests: ['Lecture', 'Randonnée', 'Musique']
    }
  ];

  const currentProfile = mockProfiles[currentProfileIndex];

  const handleSwipe = (direction) => {
    if (direction === 'right') {
      alert(`Match avec ${currentProfile.name} ! 💕`);
    }
    
    if (currentProfileIndex < mockProfiles.length - 1) {
      setCurrentProfileIndex(currentProfileIndex + 1);
    } else {
      setCurrentProfileIndex(0);
    }
  };

  const renderDiscover = () => (
    <div className="discover-tab">
      {currentProfile ? (
        <div className="profile-card">
          <div className="profile-image">
            <img src={currentProfile.photos[0]} alt={currentProfile.name} />
            <div className="profile-info-overlay">
              <h2>{currentProfile.name}, {currentProfile.age}</h2>
              <p>{currentProfile.city}</p>
            </div>
          </div>

          <div className="profile-details">
            <div className="detail-section">
              <h3>Profession</h3>
              <p>{currentProfile.profession}</p>
            </div>

            <div className="detail-section">
              <h3>Bio</h3>
              <p>{currentProfile.bio}</p>
            </div>

            <div className="detail-section">
              <h3>Centres d'intérêt</h3>
              <div className="interests-tags">
                {currentProfile.interests.map((interest, i) => (
                  <span key={i} className="interest-tag">{interest}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="swipe-buttons">
            <button className="swipe-btn dislike" onClick={() => handleSwipe('left')}>
              ✕
            </button>
            <button className="swipe-btn super-like" onClick={() => handleSwipe('up')}>
              ★
            </button>
            <button className="swipe-btn like" onClick={() => handleSwipe('right')}>
              ♥
            </button>
          </div>
        </div>
      ) : (
        <div className="no-profiles">
          <p>Plus de profils pour le moment</p>
        </div>
      )}
    </div>
  );

  const renderMatches = () => (
    <div className="matches-tab">
      <h2>Vos Matchs</h2>
      <div className="matches-grid">
        <div className="match-card">
          <img src="https://via.placeholder.com/100" alt="Match" />
          <p>Sophie</p>
          <span className="match-time">Il y a 2h</span>
        </div>
        <div className="match-card">
          <img src="https://via.placeholder.com/100" alt="Match" />
          <p>Emma</p>
          <span className="match-time">Hier</span>
        </div>
      </div>
      <p className="premium-hint">
        Accédez au chat avec l'option Premium pour 1,99€/jour
      </p>
      <button className="premium-btn" onClick={() => setShowPremium(true)}>
        Voir Premium
      </button>
    </div>
  );

  const renderProfile = () => (
    <div className="profile-tab">
      <h2>Mon Profil</h2>
      <div className="user-profile">
        <div className="profile-photo">
          {user.photos && user.photos[0] ? (
            <img src={user.photos[0]} alt="Profile" />
          ) : (
            <div className="placeholder-photo">
              {user.firstName?.[0]}{user.lastName?.[0]}
            </div>
          )}
        </div>
        <h3>{user.firstName} {user.lastName}, {user.birthDate ? new Date().getFullYear() - new Date(user.birthDate).getFullYear() : '?'} ans</h3>
        <p>{user.city}</p>
        {user.profession && <p className="profession">{user.profession}</p>}
        {user.bio && (
          <div className="bio-section">
            <h4>Bio</h4>
            <p>{user.bio}</p>
          </div>
        )}
        <button className="logout-btn" onClick={onLogout}>
          Déconnexion
        </button>
      </div>
    </div>
  );

  const renderPremium = () => (
    <div className="premium-modal" onClick={() => setShowPremium(false)}>
      <div className="premium-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={() => setShowPremium(false)}>×</button>
        <Logo size={80} />
        <h2>OneTwo Premium</h2>
        
        <div className="premium-options">
          <div className="premium-card">
            <h3>Premium 24h</h3>
            <div className="price">1,99€</div>
            <ul>
              <li>✓ Chat illimité pendant 24h</li>
              <li>✓ Voir qui vous a liké</li>
              <li>✓ Super likes illimités</li>
              <li>✓ Rewind illimité</li>
            </ul>
            <button className="buy-btn">Acheter</button>
          </div>

          <div className="premium-card featured">
            <div className="badge">POPULAIRE</div>
            <h3>Mise en avant</h3>
            <div className="price">99€</div>
            <ul>
              <li>✓ Profil en première position</li>
              <li>✓ Visibilité maximale pendant 30 jours</li>
              <li>✓ 10x plus de vues</li>
              <li>✓ Badge "Profil vedette"</li>
            </ul>
            <button className="buy-btn">Acheter</button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="main-app">
      <header className="app-header">
        <Logo size={40} />
        <h1>OneTwo</h1>
      </header>

      <div className="app-content">
        {currentTab === 'discover' && renderDiscover()}
        {currentTab === 'matches' && renderMatches()}
        {currentTab === 'profile' && renderProfile()}
      </div>

      <nav className="bottom-nav">
        <button 
          className={currentTab === 'discover' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setCurrentTab('discover')}
        >
          <span className="nav-icon">🔥</span>
          <span>Découvrir</span>
        </button>
        <button 
          className={currentTab === 'matches' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setCurrentTab('matches')}
        >
          <span className="nav-icon">💕</span>
          <span>Matchs</span>
        </button>
        <button 
          className={currentTab === 'profile' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setCurrentTab('profile')}
        >
          <span className="nav-icon">👤</span>
          <span>Profil</span>
        </button>
      </nav>

      {showPremium && renderPremium()}
    </div>
  );
}
