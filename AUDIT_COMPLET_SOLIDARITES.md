
# 🔍 AUDIT COMPLET DES SOLIDARITÉS - APPLICATION ONETWO

**Date:** 10 novembre 2025  
**Version:** 1.0  
**Statut:** Analyse complète sans modifications

---

## 📋 TABLE DES MATIÈRES

1. [Architecture Globale](#1-architecture-globale)
2. [Solidarités Frontend (React)](#2-solidarités-frontend-react)
3. [Solidarités Backend (Flask)](#3-solidarités-backend-flask)
4. [Solidarités Base de Données (Supabase)](#4-solidarités-base-de-données-supabase)
5. [Solidarités d'Authentification](#5-solidarités-dauthentification)
6. [Solidarités de Stockage (Storage)](#6-solidarités-de-stockage-storage)
7. [Solidarités des Services Externes](#7-solidarités-des-services-externes)
8. [Flux de Données Complets](#8-flux-de-données-complets)
9. [Points de Défaillance Identifiés](#9-points-de-défaillance-identifiés)
10. [Recommandations](#10-recommandations)

---

## 1. ARCHITECTURE GLOBALE

### 1.1 Structure en 3 Couches

```
┌─────────────────────────────────────┐
│   COUCHE CLIENT (React + Vite)      │
│   Port: 5173 (dev) / 80-443 (prod)  │
└──────────────┬──────────────────────┘
               │ HTTP/HTTPS
               │ fetch() API calls
               ▼
┌─────────────────────────────────────┐
│   COUCHE SERVEUR (Flask + Gunicorn) │
│   Port: 5000                         │
└──────────────┬──────────────────────┘
               │ PostgreSQL Protocol
               │ REST API calls
               ▼
┌─────────────────────────────────────┐
│   COUCHE DONNÉES (Supabase Cloud)   │
│   - PostgreSQL Database              │
│   - Storage (S3-like)                │
│   - Auth Service                     │
└─────────────────────────────────────┘
```

### 1.2 Technologies Principales

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| Frontend | React | 18.3.1 | Interface utilisateur |
| Build Tool | Vite | 5.4.10 | Bundler et dev server |
| Backend | Flask | 3.1.0 | API REST |
| Server | Gunicorn | 23.0.0 | WSGI HTTP Server |
| Database | Supabase (PostgreSQL) | Cloud | Base de données |
| Auth | Supabase Auth | Cloud | Authentification |
| Storage | Supabase Storage | Cloud | Stockage fichiers |

---

## 2. SOLIDARITÉS FRONTEND (REACT)

### 2.1 Dépendances NPM Critiques

```json
{
  "@supabase/supabase-js": "^2.80.0"  // ⚠️ SOLIDARITÉ CRITIQUE
}
```

**Impact:** Sans cette librairie, l'application ne peut pas communiquer avec Supabase.

### 2.2 Composants et Leurs Solidarités

#### 2.2.1 App.jsx → Composants Pages

```
App.jsx
├── WelcomeScreen.jsx
├── AuthChoice.jsx
├── SignupForm.jsx
│   ├── Logo.jsx
│   └── nationalities.js (data)
├── LoginForm.jsx
│   └── Logo.jsx
├── SexualOrientation.jsx
│   ├── Logo.jsx
│   └── ChipSelector.jsx
├── RelationshipType.jsx
│   ├── Logo.jsx
│   └── ChipSelector.jsx
├── Religion.jsx
│   ├── Logo.jsx
│   └── ChipSelector.jsx
├── PsychologyQuestions.jsx
│   ├── Logo.jsx
│   └── SliderPreference.jsx
├── DetailedPreferences.jsx
│   ├── Logo.jsx
│   └── SliderPreference.jsx
├── HairColor.jsx
│   ├── Logo.jsx
│   └── ChipSelector.jsx
├── EyeColor.jsx
│   ├── Logo.jsx
│   └── ChipSelector.jsx
├── BeardPreference.jsx
│   ├── Logo.jsx
│   └── SliderPreference.jsx
├── PrivacyZone.jsx
│   └── Logo.jsx
├── ProfileSetup.jsx
│   ├── Logo.jsx
│   ├── PhotoUploader.jsx
│   └── ChipSelector.jsx
└── MainApp.jsx
    └── Logo.jsx
```

**SOLIDARITÉ CRITIQUE:** Tous les composants dépendent de `Logo.jsx`

### 2.3 Composants Partagés (Shared)

#### 2.3.1 ChipSelector.jsx
- **Utilisé par:** 6 composants
- **Dépendances:** React hooks (useState)
- **Props requises:** `options`, `selected`, `onToggle`, `maxSelection`

#### 2.3.2 SliderPreference.jsx
- **Utilisé par:** 4 composants
- **Dépendances:** React hooks (useState, useEffect)
- **Props requises:** `label`, `value`, `onChange`, `leftLabel`, `rightLabel`

#### 2.3.3 PhotoUploader.jsx
- **Utilisé par:** ProfileSetup.jsx
- **Dépendances:** React hooks (useState)
- **Props requises:** `photos`, `onPhotosChange`, `maxPhotos`

### 2.4 Service Supabase Client

**Fichier:** `client/src/services/supabaseClient.js`

```javascript
// SOLIDARITÉS ENVIRONNEMENT
VITE_SUPABASE_URL         // ⚠️ CRITIQUE - Sans cela, pas de connexion
VITE_SUPABASE_ANON_KEY    // ⚠️ CRITIQUE - Clé d'authentification
```

**Fonctions exportées:**
1. `supabase` - Client Supabase initialisé
2. `saveProfile()` - Sauvegarde profil utilisateur
3. `uploadPhoto()` - Upload photos vers Storage
4. `testConnection()` - Test connexion DB

**SOLIDARITÉ CRITIQUE:** ProfileSetup.jsx dépend de ces fonctions

---

## 3. SOLIDARITÉS BACKEND (FLASK)

### 3.1 Structure des Modules

```
app.py (Point d'entrée)
├── routes/
│   ├── dashboard.py          // ⚠️ NON UTILISÉ dans le flux principal
│   ├── academy.py            // ⚠️ NON UTILISÉ dans le flux principal
│   └── testing_dashboard.py  // ⚠️ NON UTILISÉ dans le flux principal
├── modules/
│   ├── ai/openai_service.py          // ⚠️ NON UTILISÉ actuellement
│   ├── analytics/analytics_service.py // ⚠️ NON UTILISÉ actuellement
│   ├── auth/auth_service.py          // ⚠️ NON UTILISÉ actuellement
│   ├── cache/redis_service.py        // ⚠️ NON UTILISÉ actuellement
│   ├── collaboration/                // ⚠️ NON UTILISÉ actuellement
│   ├── communication/                // ⚠️ NON UTILISÉ actuellement
│   ├── geolocation/mapbox_service.py // ⚠️ NON UTILISÉ actuellement
│   ├── payments/stripe_service.py    // ⚠️ NON UTILISÉ actuellement
│   └── services/additional_services.py // ⚠️ NON UTILISÉ actuellement
└── security/api_manager.py   // ⚠️ NON UTILISÉ actuellement
```

### 3.2 Endpoint Critique: `/api/save-profile`

**Fichier:** `main.py`

**SOLIDARITÉS:**

```python
# 1. Dépendances Python
from supabase import create_client  # ⚠️ CRITIQUE
import os                           # Variables d'environnement
import base64                       # Décodage images

# 2. Variables d'environnement
URL_SUPABASE_AUTOQG        # ⚠️ CRITIQUE
api_key_secret_supabase    # ⚠️ CRITIQUE (clé secrète côté serveur)

# 3. Bucket Supabase Storage
'avatars'  # ⚠️ DOIT EXISTER dans Supabase Storage
```

**Flux de données:**

```
1. Client envoie POST /api/save-profile
   ↓
2. Backend reçoit JSON avec photos en base64
   ↓
3. Décode les photos base64
   ↓
4. Upload vers Supabase Storage (bucket 'avatars')
   ↓
5. Récupère les URLs publiques
   ↓
6. Insert dans table 'profiles' avec URLs
   ↓
7. Retourne succès/erreur au client
```

### 3.3 Test de Connexion Supabase

**Fichier:** `test_supabase_connection.py`

**SOLIDARITÉS:**
- `URL_SUPABASE_AUTOQG` (variable env)
- `api_key_secret_supabase` (variable env)
- Table `profiles` doit exister
- Bucket Storage doit exister

---

## 4. SOLIDARITÉS BASE DE DONNÉES (SUPABASE)

### 4.1 Schéma de Base de Données Requis

**Table: profiles**

```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    email TEXT,
    photos TEXT[],  -- URLs des photos depuis Storage
    professions JSONB,
    professional_status JSONB,
    interests JSONB,
    favorite_books JSONB,
    favorite_movies JSONB,
    favorite_music JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**⚠️ SOLIDARITÉ CRITIQUE:** Sans cette table, `/api/save-profile` échoue

### 4.2 Bucket Storage Requis

**Nom:** `avatars`

**Configuration requise:**
- Public: OUI (pour récupérer URLs publiques)
- Allowed MIME types: `image/png`, `image/jpeg`, `image/webp`

**Structure des fichiers:**
```
avatars/
└── [email_utilisateur]/
    ├── photo_0.png
    ├── photo_1.png
    └── ...
```

### 4.3 Policies RLS (Row Level Security)

**⚠️ ATTENTION:** Actuellement, les policies ne sont pas définies dans le code fourni.

**Policies recommandées:**

```sql
-- Lecture: tout le monde peut lire
CREATE POLICY "Profiles are viewable by everyone"
ON profiles FOR SELECT
USING (true);

-- Insertion: utilisateur authentifié peut insérer son profil
CREATE POLICY "Users can insert their own profile"
ON profiles FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Update: utilisateur peut modifier son profil
CREATE POLICY "Users can update their own profile"
ON profiles FOR UPDATE
USING (auth.uid() = user_id);
```

---

## 5. SOLIDARITÉS D'AUTHENTIFICATION

### 5.1 Variables d'Environnement

**Client (Frontend):**
- `VITE_SUPABASE_URL` - URL du projet Supabase
- `VITE_SUPABASE_ANON_KEY` - Clé publique (anon/public)

**Serveur (Backend):**
- `URL_SUPABASE_AUTOQG` - URL du projet Supabase
- `api_key_secret_supabase` - Clé secrète (service role)

**⚠️ PROBLÈME IDENTIFIÉ:** Le backend utilise `api_key_secret_supabase` mais cette clé n'est pas dans les secrets Replit actuels (voir console output du workflow).

### 5.2 Flux d'Authentification Supabase

```
1. Utilisateur s'inscrit/se connecte
   ↓
2. Supabase Auth crée un utilisateur
   ↓
3. JWT token généré
   ↓
4. Token stocké dans localStorage (client)
   ↓
5. Toutes les requêtes incluent ce token
   ↓
6. Supabase valide le token automatiquement
```

**⚠️ NON IMPLÉMENTÉ ACTUELLEMENT:** Le flux d'auth n'est pas complet dans le code fourni.

---

## 6. SOLIDARITÉS DE STOCKAGE (STORAGE)

### 6.1 Upload de Photos - Flux Complet

```
ProfileSetup.jsx (Client)
├── PhotoUploader.jsx
│   └── Convertit fichiers en base64
│       ↓
│   handleSubmit() envoie au backend
│       ↓
main.py (Backend)
├── /api/save-profile
│   ├── Décode base64
│   ├── Upload vers Supabase Storage
│   │   └── Bucket: 'avatars'
│   │       └── Path: {email}/photo_{i}.png
│   ├── Récupère URL publique
│   └── Sauvegarde URL dans table 'profiles'
```

### 6.2 Dépendances Storage

**SOLIDARITÉS CRITIQUES:**

1. **Bucket 'avatars' doit exister** dans Supabase Storage
2. **Permissions publiques** doivent être activées
3. **Storage API key** doit avoir les droits d'upload
4. **CORS** doit être configuré pour accepter les requêtes depuis Replit

---

## 7. SOLIDARITÉS DES SERVICES EXTERNES

### 7.1 Services Configurés mais Non Utilisés

**Modules présents mais inactifs:**

```python
# AI Services
OPENAI_API_KEY                    # ⚠️ Module créé mais non appelé
ANTHROPIC_API_KEY                 # ⚠️ Module créé mais non appelé

# Analytics
POSTHOG_API_KEY                   # ⚠️ Module créé mais non appelé
GOOGLE_ANALYTICS_ID               # ⚠️ Non implémenté

# Communication
TWILIO_ACCOUNT_SID               # ⚠️ Module créé mais non appelé
SENDGRID_API_KEY                 # ⚠️ Module créé mais non appelé

# Payments
STRIPE_SECRET_KEY                # ⚠️ Module créé mais non appelé

# Geolocation
MAPBOX_ACCESS_TOKEN              # ⚠️ Module créé mais non appelé

# Cache
REDIS_URL                        # ⚠️ Module créé mais non appelé
```

**IMPACT:** Ces services n'affectent pas le fonctionnement actuel de l'application de dating.

### 7.2 Services Actifs

**Supabase uniquement:**
- Database (PostgreSQL)
- Storage (S3-like)
- Auth (JWT-based)

---

## 8. FLUX DE DONNÉES COMPLETS

### 8.1 Flux Inscription Utilisateur

```
┌─────────────────────────────────────────────────────────────┐
│ 1. WelcomeScreen → AuthChoice → SignupForm                  │
│    Collecte: firstName, lastName, email, password, gender,  │
│              phone, birthdate, nationality                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SexualOrientation → RelationshipType → Religion          │
│    → PsychologyQuestions → DetailedPreferences              │
│    → HairColor → EyeColor → (BeardPreference si homme)      │
│    → PrivacyZone                                             │
│    Collecte: préférences utilisateur                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ProfileSetup                                              │
│    Collecte: photos, professions, status, interests,        │
│              books, movies, music                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼ fetch('http://0.0.0.0:5000/api/save-profile')
┌─────────────────────────────────────────────────────────────┐
│ 4. Backend Flask (/api/save-profile)                        │
│    - Reçoit toutes les données + photos base64              │
│    - Decode photos                                           │
│    - Upload photos → Supabase Storage (bucket 'avatars')    │
│    - Insert profil → Supabase DB (table 'profiles')         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. MainApp                                                   │
│    Affiche l'application principale                          │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Points de Synchronisation Critiques

**Point 1: Transition ProfileSetup → Backend**
- **Dépend de:** Backend Flask accessible sur port 5000
- **Dépend de:** Variables env Supabase configurées côté serveur
- **Risque:** CORS, network timeout

**Point 2: Backend → Supabase Storage**
- **Dépend de:** Bucket 'avatars' existe
- **Dépend de:** Permissions upload activées
- **Risque:** Quota storage dépassé, permissions RLS

**Point 3: Backend → Supabase Database**
- **Dépend de:** Table 'profiles' existe avec bon schéma
- **Dépend de:** Connexion PostgreSQL stable
- **Risque:** Schema mismatch, RLS policies

---

## 9. POINTS DE DÉFAILLANCE IDENTIFIÉS

### 9.1 Erreurs Actuelles (Console Output)

```
⚠️ Clés manquantes: api_key_secret_supabase
⚠️ Clés manquantes: PROJET_ID_APPWRITE
⚠️ Clés manquantes: POSTHOG_API_KEY
⚠️ Clés manquantes: GABRIEL_API_KEY_1
⚠️ Clés manquantes: Try_out_Your_new_API_key_NODE
```

**IMPACT CRITIQUE:** `api_key_secret_supabase` manquante = `/api/save-profile` ne peut pas fonctionner !

### 9.2 Erreur Affichée dans l'Interface

**Screenshot fourni:**
```
Erreur lors de la sauvegarde: Erreur base de données: TypeError: Load failed
```

**DIAGNOSTIC:**
1. **Cause probable:** Backend ne peut pas se connecter à Supabase (clé manquante)
2. **Alternative:** Problème CORS entre client et backend
3. **Alternative:** Bucket 'avatars' n'existe pas

### 9.3 Code d'Erreur dans ProfileSetup.jsx

```javascript
const response = await fetch('http://0.0.0.0:5000/api/save-profile', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(completeProfile)
});
```

**PROBLÈME:** Utilise `0.0.0.0` qui peut ne pas être accessible depuis le navigateur client.

**SOLUTION:** Devrait utiliser l'URL de déploiement Replit ou `window.location.origin`.

### 9.4 Modules Backend Inutilisés

**Fichiers créés mais jamais appelés:**
- `routes/dashboard.py` (143 lignes)
- `routes/academy.py` (plusieurs centaines de lignes)
- `routes/testing_dashboard.py`
- Tous les modules dans `modules/` (AI, analytics, auth, cache, etc.)
- `security/api_manager.py`

**IMPACT:** Augmente la complexité sans bénéfice, peut causer confusion.

---

## 10. RECOMMANDATIONS

### 10.1 Corrections Urgentes

#### 🔴 PRIORITÉ 1 - Ajouter la clé Supabase manquante

**Action:** Dans Replit Secrets, ajouter:
```
api_key_secret_supabase = [VOTRE_CLE_SERVICE_ROLE_SUPABASE]
```

**Où trouver cette clé:**
1. Dashboard Supabase → Settings → API
2. Copier "service_role key" (⚠️ JAMAIS la clé publique anon!)

#### 🔴 PRIORITÉ 2 - Créer le bucket Storage

**Action:** Dans Supabase Dashboard:
1. Storage → New Bucket
2. Nom: `avatars`
3. Public: ✅ OUI
4. Allowed MIME types: `image/*`

#### 🔴 PRIORITÉ 3 - Vérifier la table profiles

**Action:** SQL Editor dans Supabase:
```sql
SELECT * FROM profiles LIMIT 1;
```

Si erreur "table does not exist", créer la table (voir section 4.1).

#### 🟡 PRIORITÉ 4 - Corriger l'URL du backend

**Fichier:** `client/src/components/ProfileSetup.jsx`

```javascript
// Remplacer:
const response = await fetch('http://0.0.0.0:5000/api/save-profile', {

// Par:
const backendUrl = import.meta.env.PROD 
  ? '/api/save-profile'  // En production, même domaine
  : 'http://localhost:5000/api/save-profile';  // En dev local

const response = await fetch(backendUrl, {
```

### 10.2 Nettoyage Recommandé

#### Supprimer les fichiers inutilisés:

```bash
# Routes non utilisées
rm routes/dashboard.py
rm routes/academy.py
rm routes/testing_dashboard.py

# Templates HTML non utilisés
rm templates/dashboard.html
rm templates/academy_home.html
rm templates/api_creator.html
rm templates/learn_platform.html
rm templates/secrets_manager.html
rm templates/testing_dashboard.html

# Modules non utilisés
rm -rf modules/ai
rm -rf modules/analytics
rm -rf modules/auth
rm -rf modules/cache
rm -rf modules/collaboration
rm -rf modules/communication
rm -rf modules/geolocation
rm -rf modules/payments
rm -rf modules/services
rm -rf security
```

**GAIN:** Réduction de ~80% du code backend inutilisé.

### 10.3 Améliorations de Sécurité

#### Activer RLS (Row Level Security) sur Supabase:

```sql
-- Activer RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: lecture publique
CREATE POLICY "Profiles viewable by everyone"
ON profiles FOR SELECT
USING (true);

-- Policy: insertion utilisateur authentifié
CREATE POLICY "Users insert own profile"
ON profiles FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### 10.4 Monitoring et Logs

#### Ajouter des logs détaillés dans main.py:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    logging.info(f"📥 Received profile data from {request.remote_addr}")
    # ... reste du code
    logging.info(f"✅ Profile saved successfully for {data.get('email')}")
```

---

## 📊 RÉSUMÉ EXÉCUTIF

### État Actuel

| Composant | Statut | Criticité |
|-----------|--------|-----------|
| Frontend React | ✅ Fonctionnel | Moyenne |
| Backend Flask | ⚠️ Clé manquante | **HAUTE** |
| Supabase DB | ❓ À vérifier | **HAUTE** |
| Supabase Storage | ❓ À vérifier | **HAUTE** |
| Auth Supabase | ❌ Non implémenté | Moyenne |

### Actions Immédiates Requises

1. ✅ **Ajouter `api_key_secret_supabase` dans Replit Secrets**
2. ✅ **Créer bucket 'avatars' dans Supabase Storage**
3. ✅ **Vérifier/créer table 'profiles' dans Supabase**
4. 🔄 **Corriger l'URL du backend dans ProfileSetup.jsx**
5. 🧹 **Nettoyer les fichiers inutilisés**

### Solidarités Critiques Identifiées

```
┌─────────────────────────────────────────────┐
│  SOLIDARITÉ #1 - Variables Environnement    │
│  Frontend ↔ VITE_SUPABASE_URL              │
│  Frontend ↔ VITE_SUPABASE_ANON_KEY         │
│  Backend  ↔ URL_SUPABASE_AUTOQG           │
│  Backend  ↔ api_key_secret_supabase ⚠️    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  SOLIDARITÉ #2 - Infrastructure Supabase    │
│  Backend → Table 'profiles'                 │
│  Backend → Bucket 'avatars'                 │
│  Backend → Auth service                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  SOLIDARITÉ #3 - Communication Client/API   │
│  ProfileSetup.jsx → /api/save-profile       │
│  CORS configuration                         │
│  Network accessibility                      │
└─────────────────────────────────────────────┘
```

---

**FIN DE L'AUDIT**

_Ce document identifie toutes les solidarités (dépendances) de l'application OneTwo sans effectuer aucune modification. Il sert de base pour diagnostiquer et résoudre les problèmes actuels._
