# 💕 OneTwo - Application de Rencontre Moderne

## Vue d'Ensemble

**OneTwo** est une application de rencontre nouvelle génération qui combine les meilleures fonctionnalités de Tinder et l'esthétique d'Instagram. L'application se concentre sur la mise en relation authentique basée sur des préférences détaillées et des compatibilités psychologiques.

**Statut**: ✅ Application Frontend Opérationnelle

## 🚀 Démarrage Rapide

L'application démarre automatiquement. Vous pouvez voir l'interface dans le webview sur le côté droit de votre écran Replit.

Pour redémarrer manuellement:
```bash
cd client && npm run dev
```

## ✨ Fonctionnalités Principales

### 1. Processus d'Inscription Complet (7 Étapes)

#### Étape 1: Bienvenue
- Écran d'accueil avec présentation de l'app
- Mise en avant des fonctionnalités clés
- Design moderne et attractif

#### Étape 2: Création de Compte
- **Informations personnelles requises**:
  - Genre (Homme/Femme)
  - Prénom et Nom
  - Email (avec validation)
  - Mot de passe sécurisé (min 8 caractères, majuscule, minuscule, chiffre)
  - Date de naissance (18+ uniquement)
  - Ville
  
- **Validations automatiques**:
  - Format email correct
  - Force du mot de passe
  - Âge minimum (18 ans)

#### Étape 3: Questions Psychologiques
- **Timidité**: Oui/Non
- **Introverti**: Oui/Non

#### Étape 4: Type de Relation Recherchée
- 💕 Relation sérieuse
- 🌙 Plan d'un soir  
- 💍 Je veux me marier
- 😊 Rien de sérieux
- 🎉 Me divertir

#### Étape 5: Orientation Sexuelle
- 👫 Hétérosexuel(le)
- 👭 Homosexuel(le)
- 💗 Bisexuel(le)
- 🏳️‍⚧️ Transgenre

#### Étape 6: Préférences Détaillées (Sliders 0-100%)

Chaque préférence est ajustable avec un slider de pourcentage:

1. **Tatouages**: Sans tatouage → Avec tatouages
2. **Tabac**: Non-fumeur → Fumeur
3. **Régime alimentaire**: Végétarien → Omnivore
4. **Couleur de cheveux**: Blonde → Brune/Rousse
5. **Taille**: Petite → Grande
6. **Pilosité corporelle**: Rasé → Poilu
7. **Morphologie**: Mince → Athlétique/Robuste
8. **Style vestimentaire**: Casual → Élégant

**Note**: 50% = Aucune préférence (matching plus large)

#### Étape 7: Configuration du Profil
- **Photos**: Jusqu'à 6 photos
- **Bio**: Minimum 50 caractères (max 500)
- **Profession**: Métier
- **Centres d'intérêt**: Jusqu'à 10 tags

### 2. Interface Principale (Style Instagram)

#### 🔥 Onglet Découvrir
- **Cartes de profils** avec:
  - Photo principale grande taille
  - Nom, âge, ville
  - Profession
  - Bio complète
  - Centres d'intérêt
  
- **Système de swipe** avec 3 boutons:
  - ✕ Dislike (rouge)
  - ★ Super Like (bleu)
  - ♥ Like (vert)

#### 💕 Onglet Matchs
- Grille de tous vos matchs
- Indication du temps écoulé depuis le match
- Information sur le Premium pour débloquer le chat

#### 👤 Onglet Profil
- Affichage de votre profil complet
- Photo de profil avec initiales si pas de photo
- Toutes vos informations
- Bouton de déconnexion

### 3. Système Premium

#### Option 1: Premium 24h - 1,99€
- ✓ Chat illimité pendant 24h
- ✓ Voir qui vous a liké
- ✓ Super likes illimités
- ✓ Rewind illimité

#### Option 2: Mise en Avant - 99€
- ✓ Profil en première position
- ✓ Visibilité maximale pendant 30 jours
- ✓ 10x plus de vues
- ✓ Badge "Profil vedette"

## 🎨 Design & Couleurs

### Palette de Couleurs
- **Rose principal**: #FF1493 (Deep Pink)
- **Rose clair**: #FF69B4 (Hot Pink)
- **Noir**: #000000
- **Blanc**: #FFFFFF
- **Gris foncé**: #333333
- **Gris clair**: #666666

### Logo
- Design yin-yang avec deux flammes
- Couleurs: Noir, Rose et Blanc
- Symbolise l'équilibre et la passion

### Typographie
- Font: System UI (San Francisco, Segoe UI, Roboto)
- Style moderne et lisible
- Hiérarchie claire des titres

## 📁 Structure du Projet

```
.
├── client/                          # Application React Frontend
│   ├── src/
│   │   ├── components/             # Composants React
│   │   │   ├── Logo.jsx           # Logo OneTwo
│   │   │   ├── WelcomeScreen.jsx  # Écran d'accueil
│   │   │   ├── AuthChoice.jsx     # Choix inscription/connexion
│   │   │   ├── SignupForm.jsx     # Formulaire d'inscription
│   │   │   ├── LoginForm.jsx      # Formulaire de connexion
│   │   │   ├── PsychologyQuestions.jsx  # Questions psychologiques
│   │   │   ├── RelationshipType.jsx     # Type de relation
│   │   │   ├── SexualOrientation.jsx    # Orientation sexuelle
│   │   │   ├── DetailedPreferences.jsx  # Sliders de préférences
│   │   │   ├── ProfileSetup.jsx         # Configuration profil
│   │   │   └── MainApp.jsx              # App principale
│   │   ├── App.jsx                # Composant principal
│   │   ├── App.css                # Styles globaux
│   │   └── index.css              # Styles de base
│   ├── package.json               # Dépendances npm
│   └── vite.config.js             # Configuration Vite
│
├── app.py                          # Backend Flask (à connecter)
├── pyproject.toml                  # Dépendances Python
└── replit.md                       # Cette documentation
```

## 🛠️ Technologies Utilisées

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 7.2.1
- **Language**: JavaScript (JSX)
- **Styling**: CSS pur (pas de frameworks CSS)
- **État**: React useState & localStorage

### Backend (À connecter)
- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL (via Supabase)
- **Auth**: Supabase Auth
- **Payment**: Stripe
- **Email**: Resend
- **Storage**: Supabase Storage (pour photos)

### Services Externes Disponibles
- ✅ Supabase (Database & Auth)
- ✅ Stripe (Paiements Premium)
- ✅ Resend (Emails)
- ✅ Redis (Cache/Sessions)
- ✅ OpenAI (Suggestions de profils?)
- ✅ Mapbox (Géolocalisation)

## 🔗 Prochaines Étapes de Développement

### Phase 1: Backend API (Prioritaire)
1. **API d'authentification**
   - Endpoint signup
   - Endpoint login
   - Gestion JWT tokens
   - Stockage profils dans Supabase

2. **API de profils**
   - CRUD profils utilisateurs
   - Upload photos (Supabase Storage)
   - Mise à jour préférences

3. **API de matching**
   - Algorithme de compatibilité
   - Calcul score basé sur préférences
   - Génération suggestions de profils

4. **API de swipe & matchs**
   - Enregistrement likes/dislikes
   - Détection matchs mutuels
   - Notifications matchs

### Phase 2: Chat Temps Réel
1. WebSockets ou Supabase Realtime
2. Messages texte
3. Notifications temps réel
4. Historique conversations

### Phase 3: Paiement Premium
1. Intégration Stripe Checkout
2. Webhooks Stripe
3. Gestion abonnements
4. Déblocage fonctionnalités premium

### Phase 4: Fonctionnalités Avancées
1. Géolocalisation (Mapbox)
2. Filtres de recherche avancés
3. Boost de profil
4. Super likes
5. Rewind (annuler dernier swipe)
6. Voir qui vous a liké

### Phase 5: Analytics & Optimisation
1. Tracking événements (Amplitude/Posthog)
2. Tests A/B
3. Optimisation algorithme matching
4. Performance monitoring

## 💾 Stockage des Données

### LocalStorage (Actuel - Temporaire)
Actuellement, les données sont stockées dans le navigateur:
- Clé: `onetwo_user`
- Données: Profil utilisateur complet
- **Limitation**: Données perdues si cache effacé

### Migration vers Backend (À faire)
Structure de base de données Supabase:

```sql
-- Table users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  birth_date DATE NOT NULL,
  city VARCHAR NOT NULL,
  gender VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table profiles
CREATE TABLE profiles (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  bio TEXT,
  profession VARCHAR,
  photos TEXT[], -- URLs des photos
  interests TEXT[],
  is_shy BOOLEAN,
  is_introverted BOOLEAN,
  relationship_type VARCHAR,
  sexual_orientation VARCHAR,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Table preferences
CREATE TABLE preferences (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  tattoos INT, -- 0-100
  smoking INT,
  diet INT,
  hair_color INT,
  height INT,
  body_hair INT,
  body_type INT,
  style INT
);

-- Table swipes
CREATE TABLE swipes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  target_user_id UUID REFERENCES users(id),
  action VARCHAR, -- 'like', 'dislike', 'super_like'
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, target_user_id)
);

-- Table matches
CREATE TABLE matches (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user1_id UUID REFERENCES users(id),
  user2_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user1_id, user2_id)
);

-- Table messages
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  match_id UUID REFERENCES matches(id),
  sender_id UUID REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table premium_subscriptions
CREATE TABLE premium_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  type VARCHAR, -- '24h', 'boost'
  stripe_payment_id VARCHAR,
  amount DECIMAL,
  starts_at TIMESTAMP,
  ends_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔐 Sécurité

### Validations Frontend
- ✅ Email format
- ✅ Mot de passe fort (8+ chars, maj, min, chiffre)
- ✅ Âge minimum 18 ans
- ✅ Champs requis

### À implémenter (Backend)
- [ ] Hash mots de passe (bcrypt)
- [ ] Tokens JWT avec expiration
- [ ] Rate limiting API
- [ ] CORS configuration
- [ ] Validation côté serveur
- [ ] Protection CSRF
- [ ] Sanitization inputs

## 📱 Responsive Design

L'application est entièrement responsive:
- **Mobile**: Design optimisé pour smartphones
- **Tablette**: Adaptation automatique
- **Desktop**: Max-width 500px pour simuler mobile

## 🎯 Public Cible

- **Âge**: 18-35 ans
- **Profil**: Utilisateurs cherchant relations authentiques
- **Niche**: Focus sur préférences détaillées et compatibilité

## 📊 Métriques de Succès (KPIs)

### Phase MVP
- [ ] 100 utilisateurs inscrits
- [ ] 50 profils complets
- [ ] 200 swipes/jour
- [ ] 20 matchs/jour

### Phase Croissance
- [ ] 1000 utilisateurs actifs
- [ ] 500 matchs/semaine
- [ ] 10% conversion Premium
- [ ] 50 conversations actives/jour

## 🚀 Lancement

### Checklist Avant Lancement
- [ ] Backend API opérationnel
- [ ] Tests de charge
- [ ] Politique de confidentialité
- [ ] Conditions d'utilisation
- [ ] Modération contenu
- [ ] Support client
- [ ] Payment processing testé
- [ ] Email notifications configurées

## 🤝 Contribution & Développement

### Workflow de Développement
1. Développement local sur Replit
2. Tests manuels sur chaque fonctionnalité
3. Validation UX/UI
4. Merge vers production

### Standards de Code
- Code en anglais (variables, fonctions)
- Commentaires en français si nécessaire
- Composants React fonctionnels
- Props clairement définies

---

**Date de création**: 2025-11-06  
**Dernière mise à jour**: 2025-11-06  
**Version**: 1.0.0  
**Statut**: ✅ Frontend Opérationnel - Backend à connecter
