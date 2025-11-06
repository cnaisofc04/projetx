import { useState } from 'react';
import Logo from './Logo';

export default function LoginForm({ onLogin, onBack }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const savedUser = localStorage.getItem('onetwo_user');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      if (user.email === email && user.password === password) {
        onLogin(user);
      } else {
        setError('Email ou mot de passe incorrect');
      }
    } else {
      setError('Aucun compte trouvé. Veuillez créer un compte.');
    }
  };

  return (
    <div className="login-form">
      <div className="form-content">
        <Logo size={60} />
        <h2>Connexion</h2>
        <p className="subtitle">Bon retour parmi nous !</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="votre.email@exemple.com"
              required
            />
          </div>

          <div className="form-group">
            <label>Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Votre mot de passe"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="primary-button">
            Se connecter
          </button>
          
          <button type="button" className="secondary-button" onClick={onBack}>
            Retour
          </button>
        </form>
      </div>
    </div>
  );
}
