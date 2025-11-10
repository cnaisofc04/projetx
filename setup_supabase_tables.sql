
-- ============================================
-- SCHÉMA SUPABASE POUR PROFILS
-- À exécuter dans CHAQUE instance Supabase
-- ============================================

-- Supprimer la table si elle existe
DROP TABLE IF EXISTS profiles CASCADE;

-- Créer la table profiles
CREATE TABLE profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  gender TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  birth_date DATE,
  photos TEXT[] DEFAULT '{}',
  professions TEXT[] DEFAULT '{}',
  professional_status TEXT[] DEFAULT '{}',
  interests TEXT[] DEFAULT '{}',
  favorite_books TEXT[] DEFAULT '{}',
  favorite_movies TEXT[] DEFAULT '{}',
  favorite_music TEXT[] DEFAULT '{}',
  psychology_questions JSONB DEFAULT '{}'::jsonb,
  detailed_preferences JSONB DEFAULT '{}'::jsonb,
  privacy_zone JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Contrainte de genre
  CONSTRAINT check_gender CHECK (
    (gender = 'man') OR (gender = 'woman')
  )
);

-- Index pour optimiser les recherches
CREATE INDEX idx_profiles_email ON profiles(email);
CREATE INDEX idx_profiles_gender ON profiles(gender);
CREATE INDEX idx_profiles_created_at ON profiles(created_at);

-- Fonction pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour updated_at
DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;
CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- CONFIGURATION STORAGE (Buckets)
-- ============================================

-- Pour Supabase HOMMES : bucket 'avatars-men'
-- Pour Supabase FEMMES : bucket 'avatars-women'

-- Note: Créez manuellement le bucket dans Storage UI ou via cette requête:
-- INSERT INTO storage.buckets (id, name, public)
-- VALUES ('avatars-men', 'avatars-men', true)  -- Pour HOMMES
-- OU
-- VALUES ('avatars-women', 'avatars-women', true)  -- Pour FEMMES
-- ON CONFLICT (id) DO NOTHING;

-- RLS désactivé pour le développement (à activer en production)
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;

-- Commentaires
COMMENT ON TABLE profiles IS 'Profils utilisateurs pour application de dating';
COMMENT ON COLUMN profiles.gender IS 'Genre: man ou woman';
COMMENT ON COLUMN profiles.photos IS 'URLs des photos de profil';
