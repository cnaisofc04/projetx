import Logo from './Logo';

export default function WelcomeScreen({ onContinue }) {
  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <Logo size={120} />
        <h1 className="app-title">OneTwo</h1>
        <p className="tagline">L'application de rencontre nouvelle génération</p>
        
        <div className="features">
          <div className="feature">
            <span className="feature-icon">💝</span>
            <h3>Connexions Authentiques</h3>
            <p>Rencontrez des personnes qui vous correspondent vraiment</p>
          </div>
          <div className="feature">
            <span className="feature-icon">🎯</span>
            <h3>Préférences Détaillées</h3>
            <p>Définissez précisément ce que vous recherchez</p>
          </div>
          <div className="feature">
            <span className="feature-icon">✨</span>
            <h3>Interface Moderne</h3>
            <p>Une expérience fluide et intuitive</p>
          </div>
        </div>

        <button className="cta-button" onClick={onContinue}>
          Commencer l'aventure
        </button>
      </div>
    </div>
  );
}
