import { useState } from 'react';
import Logo from './Logo';
import nationalities from '../data/nationalities';

export default function SignupForm({ onNext }) {
  const [formData, setFormData] = useState({
    gender: '',
    firstName: '',
    lastName: '',
    pseudonym: '',
    email: '',
    password: '',
    confirmPassword: '',
    birthDate: '',
    city: '',
    country: '',
    nationality: ''
  });

  const [errors, setErrors] = useState({});

  const alphabeticRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
  const pseudonymRegex = /^[a-zA-Z0-9_]+$/;

  const validate = () => {
    const newErrors = {};

    if (!formData.gender) newErrors.gender = 'Veuillez sélectionner votre genre';
    
    if (!formData.firstName) {
      newErrors.firstName = 'Prénom requis';
    } else if (!alphabeticRegex.test(formData.firstName)) {
      newErrors.firstName = 'Seuls les lettres, espaces et tirets sont autorisés';
    }
    
    if (!formData.lastName) {
      newErrors.lastName = 'Nom requis';
    } else if (!alphabeticRegex.test(formData.lastName)) {
      newErrors.lastName = 'Seuls les lettres, espaces et tirets sont autorisés';
    }
    
    if (!formData.pseudonym) {
      newErrors.pseudonym = 'Pseudonyme requis';
    } else if (formData.pseudonym.length < 3 || formData.pseudonym.length > 20) {
      newErrors.pseudonym = 'Entre 3 et 20 caractères';
    } else if (!pseudonymRegex.test(formData.pseudonym)) {
      newErrors.pseudonym = 'Lettres, chiffres et underscore uniquement (pas d\'espaces)';
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email) {
      newErrors.email = 'Email requis';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Email invalide';
    }

    if (!formData.password) {
      newErrors.password = 'Mot de passe requis';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Minimum 8 caractères';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Doit contenir majuscule, minuscule et chiffre';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Les mots de passe ne correspondent pas';
    }

    if (!formData.birthDate) {
      newErrors.birthDate = 'Date de naissance requise';
    } else {
      const age = new Date().getFullYear() - new Date(formData.birthDate).getFullYear();
      if (age < 18) {
        newErrors.birthDate = 'Vous devez avoir au moins 18 ans';
      }
    }

    if (!formData.city) {
      newErrors.city = 'Ville requise';
    } else if (!alphabeticRegex.test(formData.city)) {
      newErrors.city = 'Seuls les lettres, espaces et tirets sont autorisés';
    }

    if (!formData.country) {
      newErrors.country = 'Pays requis';
    } else if (!alphabeticRegex.test(formData.country)) {
      newErrors.country = 'Seuls les lettres, espaces et tirets sont autorisés';
    }

    if (!formData.nationality) {
      newErrors.nationality = 'Nationalité requise';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onNext(formData);
    }
  };

  return (
    <div className="signup-form">
      <div className="form-content">
        <Logo size={60} />
        <h2>Créer votre compte</h2>
        <p className="step-indicator">Étape 1/11</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Je suis</label>
            <div className="gender-buttons">
              <button
                type="button"
                className={formData.gender === 'man' ? 'gender-btn active' : 'gender-btn'}
                onClick={() => setFormData({...formData, gender: 'man'})}
              >
                Un homme
              </button>
              <button
                type="button"
                className={formData.gender === 'woman' ? 'gender-btn active' : 'gender-btn'}
                onClick={() => setFormData({...formData, gender: 'woman'})}
              >
                Une femme
              </button>
            </div>
            {errors.gender && <span className="error">{errors.gender}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Prénom *</label>
              <input
                type="text"
                value={formData.firstName}
                onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                placeholder="Votre prénom"
              />
              {errors.firstName && <span className="error">{errors.firstName}</span>}
            </div>

            <div className="form-group">
              <label>Nom *</label>
              <input
                type="text"
                value={formData.lastName}
                onChange={(e) => setFormData({...formData, lastName: e.target.value})}
                placeholder="Votre nom"
              />
              {errors.lastName && <span className="error">{errors.lastName}</span>}
            </div>
          </div>

          <div className="form-group">
            <label>Pseudonyme *</label>
            <input
              type="text"
              value={formData.pseudonym}
              onChange={(e) => setFormData({...formData, pseudonym: e.target.value})}
              placeholder="pseudo123 (3-20 caractères, lettres, chiffres, _)"
              maxLength={20}
            />
            {errors.pseudonym && <span className="error">{errors.pseudonym}</span>}
            <small className="help-text">Votre pseudonyme sera visible sur votre profil</small>
          </div>

          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              placeholder="votre.email@exemple.com"
            />
            {errors.email && <span className="error">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label>Mot de passe *</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              placeholder="Minimum 8 caractères"
            />
            {errors.password && <span className="error">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label>Confirmer le mot de passe *</label>
            <input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              placeholder="Répétez votre mot de passe"
            />
            {errors.confirmPassword && <span className="error">{errors.confirmPassword}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Date de naissance *</label>
              <input
                type="date"
                value={formData.birthDate}
                onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
              />
              {errors.birthDate && <span className="error">{errors.birthDate}</span>}
            </div>

            <div className="form-group">
              <label>Ville *</label>
              <input
                type="text"
                value={formData.city}
                onChange={(e) => setFormData({...formData, city: e.target.value})}
                placeholder="Paris, Lyon..."
              />
              {errors.city && <span className="error">{errors.city}</span>}
            </div>
          </div>

          <div className="form-group">
            <label>Pays *</label>
            <input
              type="text"
              value={formData.country}
              onChange={(e) => setFormData({...formData, country: e.target.value})}
              placeholder="France, Canada..."
            />
            {errors.country && <span className="error">{errors.country}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="nationality">Nationalité *</label>
            <select
              id="nationality"
              value={formData.nationality}
              onChange={(e) => setFormData({...formData, nationality: e.target.value})}
              className="nationality-select"
            >
              <option value="">Sélectionnez votre nationalité</option>
              {nationalities.map(nat => (
                <option key={nat.code} value={nat.code}>
                  {nat.flag} {nat.name}
                </option>
              ))}
            </select>
            {errors.nationality && <span className="error">{errors.nationality}</span>}
          </div>

          <button type="submit" className="primary-button">
            Continuer
          </button>
        </form>
      </div>
    </div>
  );
}
