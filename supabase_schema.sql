
-- ============================================
-- SCHÉMA COMPLET SUPABASE POUR L'APPLICATION
-- ============================================

-- Supprimer la table si elle existe déjà
DROP TABLE IF EXISTS profiles CASCADE;

-- Créer la table profiles avec TOUTES les colonnes nécessaires
CREATE TABLE profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE,
  
  -- Informations de base
  email TEXT,
  first_name TEXT,
  last_name TEXT,
  birth_date DATE,
  gender TEXT,
  
  -- Apparence physique
  eye_color TEXT,
  hair_color TEXT,
  height INTEGER,
  weight INTEGER,
  
  -- Informations culturelles
  religion TEXT,
  ethnicity TEXT,
  
  -- Préférences
  beard_preference TEXT,
  relationship_type TEXT,
  sexual_orientation TEXT,
  
  -- Profil détaillé
  photos JSONB DEFAULT '[]'::jsonb,
  professions JSONB DEFAULT '[]'::jsonb,
  professional_status JSONB DEFAULT '[]'::jsonb,
  interests JSONB DEFAULT '[]'::jsonb,
  favorite_books JSONB DEFAULT '[]'::jsonb,
  favorite_movies JSONB DEFAULT '[]'::jsonb,
  favorite_music JSONB DEFAULT '[]'::jsonb,
  
  -- Questions psychologiques
  psychology_questions JSONB DEFAULT '{}'::jsonb,
  
  -- Préférences détaillées
  detailed_preferences JSONB DEFAULT '{}'::jsonb,
  
  -- Zone de confidentialité
  privacy_zone JSONB DEFAULT '{}'::jsonb,
  
  -- Métadonnées
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour optimiser les recherches
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_gender ON profiles(gender);
CREATE INDEX idx_profiles_created_at ON profiles(created_at);

-- Fonction pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour updated_at
CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- CONFIGURATION STORAGE POUR LES PHOTOS
-- ============================================

-- Créer le bucket photos s'il n'existe pas
INSERT INTO storage.buckets (id, name, public)
VALUES ('photos', 'photos', true)
ON CONFLICT (id) DO NOTHING;

-- Politique : Lecture publique des photos
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'photos');

-- Politique : Upload pour tout le monde (à restreindre en production)
DROP POLICY IF EXISTS "Anyone can upload" ON storage.objects;
CREATE POLICY "Anyone can upload"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'photos');

-- Politique : Suppression (à restreindre en production)
DROP POLICY IF EXISTS "Anyone can delete" ON storage.objects;
CREATE POLICY "Anyone can delete"
ON storage.objects FOR DELETE
USING (bucket_id = 'photos');

-- ============================================
-- RLS (Row Level Security) - DÉSACTIVÉ pour le développement
-- ============================================
-- En production, activez RLS et créez des politiques appropriées
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;

-- ============================================
-- COMMENTAIRES
-- ============================================
COMMENT ON TABLE profiles IS 'Table principale des profils utilisateurs';
COMMENT ON COLUMN profiles.user_id IS 'Identifiant unique utilisateur (email ou UUID)';
COMMENT ON COLUMN profiles.photos IS 'Array JSON des URLs de photos';
COMMENT ON COLUMN profiles.professions IS 'Array JSON des professions';
COMMENT ON COLUMN profiles.psychology_questions IS 'Object JSON des réponses psychologiques';
