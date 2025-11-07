
-- Créer la table profiles dans Supabase
CREATE TABLE IF NOT EXISTS profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE,
  photos JSONB,
  professions JSONB,
  professional_status JSONB,
  interests JSONB,
  favorite_books JSONB,
  favorite_movies JSONB,
  favorite_music JSONB,
  gender TEXT,
  religion TEXT,
  eye_color TEXT,
  hair_color TEXT,
  beard_preference TEXT,
  relationship_type TEXT,
  sexual_orientation TEXT,
  psychology_questions JSONB,
  detailed_preferences JSONB,
  privacy_zone JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Créer un bucket pour les photos
INSERT INTO storage.buckets (id, name, public)
VALUES ('photos', 'photos', true)
ON CONFLICT DO NOTHING;

-- Permettre l'accès public aux photos
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'photos');

-- Permettre l'upload aux utilisateurs authentifiés
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'photos');
