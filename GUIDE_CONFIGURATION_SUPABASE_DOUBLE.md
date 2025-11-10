
# 🔧 Guide Configuration Supabase Double Instance

## Architecture

```
┌─────────────────────────────────────┐
│   APPLICATION ONETWO                │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌──────────┐      ┌──────────┐
│ SUPABASE │      │ SUPABASE │
│  HOMMES  │      │  FEMMES  │
└──────────┘      └──────────┘
      │                 │
      └────────┬────────┘
               ▼
         ┌──────────┐
         │ APPWRITE │
         │   CHAT   │
         └──────────┘
```

## 1. Configuration Supabase HOMMES

### Dashboard Supabase → Projet Hommes

1. **URL Projet**: Copiez dans `profil_man_supabase_URL`
2. **API Keys**:
   - `anon/public` → `profil_man_supabase_API_anon_public`
   - `service_role` → `profil_man_supabase_API_service_role_secret`

3. **Créer le bucket Storage**:
```sql
-- Dans Storage
Nouveau bucket: avatars-men
Public: OUI
```

4. **Créer la table profiles**:
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(10) CHECK (gender = 'man'),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    photos TEXT[],
    professions TEXT[],
    interests TEXT[],
    favorite_books TEXT[],
    favorite_movies TEXT[],
    favorite_music TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Men profiles public read"
    ON profiles FOR SELECT
    USING (true);

CREATE POLICY "Anyone can insert men profiles"
    ON profiles FOR INSERT
    WITH CHECK (gender = 'man');
```

## 2. Configuration Supabase FEMMES

### Dashboard Supabase → Projet Femmes

1. **URL Projet**: Copiez dans `profil_woman_supabase_URL`
2. **API Keys**:
   - `anon/public` → `profil_woman_supabase_API_anon_public`
   - `service_role` → `profil_woman_supabase_API_service_role_secret`

3. **Créer le bucket Storage**:
```sql
-- Dans Storage
Nouveau bucket: avatars-women
Public: OUI
```

4. **Créer la table profiles**:
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(10) CHECK (gender = 'woman'),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    photos TEXT[],
    professions TEXT[],
    interests TEXT[],
    favorite_books TEXT[],
    favorite_movies TEXT[],
    favorite_music TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Women profiles public read"
    ON profiles FOR SELECT
    USING (true);

CREATE POLICY "Anyone can insert women profiles"
    ON profiles FOR INSERT
    WITH CHECK (gender = 'woman');
```

## 3. Configuration Appwrite (Chat uniquement)

### Dashboard Appwrite

1. **Endpoint**: `https://fra.cloud.appwrite.io/v1` (déjà configuré)
2. **Project ID**: Copiez dans `PROJET_ID_APPWRITE`
3. **API Key**: Copiez dans `API__KEY_APPWRITE`

4. **Créer la Database "chat"**:
   - Collection: `messages`
   - Collection: `conversations`

## 4. Variables d'Environnement Replit

### Secrets à Ajouter/Vérifier:

```bash
# HOMMES
profil_man_supabase_URL=https://dwfyekbdnodsragtvvgn.supabase.co
profil_man_supabase_API_anon_public=[votre_cle]
profil_man_supabase_API_service_role_secret=[votre_cle]

# FEMMES
profil_woman_supabase_URL=[votre_url]
profil_woman_supabase_API_anon_public=[votre_cle]
profil_woman_supabase_API_service_role_secret=[votre_cle]

# APPWRITE (Chat)
PROJET_ID_APPWRITE=[votre_id]
API__KEY_APPWRITE=[votre_cle]
API_ENDPOINT_APPRWRITE=https://fra.cloud.appwrite.io/v1
```

## 5. Flux de Données

### Inscription Homme:
1. User remplit formulaire → `gender: 'man'`
2. Backend route vers `profil_man_supabase_URL`
3. Upload photos → bucket `avatars-men`
4. Insert profil → table `profiles` (instance hommes)

### Inscription Femme:
1. User remplit formulaire → `gender: 'woman'`
2. Backend route vers `profil_woman_supabase_URL`
3. Upload photos → bucket `avatars-women`
4. Insert profil → table `profiles` (instance femmes)

### Chat (tous):
1. Homme ↔ Femme communication
2. Appwrite gère les messages
3. Collections: `messages`, `conversations`

## 6. Vérification

Exécutez ce test:
```bash
python test_supabase_double_instance.py
```

✅ Devrait afficher:
- Connexion HOMMES: OK
- Connexion FEMMES: OK
- Connexion APPWRITE: OK
