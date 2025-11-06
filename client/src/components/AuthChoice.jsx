import Logo from './Logo';

export default function AuthChoice({ onSignup, onLogin }) {
  return (
    <div className="auth-choice">
      <div className="auth-content">
        <Logo size={80} />
        <h1>OneTwo</h1>
        <p className="subtitle">Bienvenue ! Comment souhaitez-vous continuer ?</p>

        <div className="auth-buttons">
          <button className="primary-button" onClick={onSignup}>
            Créer un compte
          </button>
          <button className="secondary-button" onClick={onLogin}>
            J'ai déjà un compte
          </button>
        </div>
      </div>
    </div>
  );
}
