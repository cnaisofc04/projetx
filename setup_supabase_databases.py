
#!/usr/bin/env python3
"""
Script pour créer automatiquement les tables dans Supabase HOMMES et FEMMES
"""
import os
from supabase import create_client

# Schéma SQL
SQL_SCHEMA = """
-- Créer la table profiles
CREATE TABLE IF NOT EXISTS profiles (
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
  CONSTRAINT check_gender CHECK ((gender = 'man') OR (gender = 'woman'))
);

-- Index
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_gender ON profiles(gender);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON profiles(created_at);

-- Fonction trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger
DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;
CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Désactiver RLS pour dev
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;
"""

def setup_database(name, url, key):
    """Créer les tables dans une instance Supabase"""
    print(f"\n{'='*60}")
    print(f"🔧 CONFIGURATION SUPABASE {name.upper()}")
    print(f"{'='*60}")
    print(f"URL: {url}")
    
    try:
        # Connexion
        client = create_client(url, key)
        
        # Exécuter le SQL via l'API REST (contournement)
        # Note: L'API Supabase Python ne permet pas d'exécuter du SQL directement
        # Il faut utiliser l'interface Web ou psycopg2
        
        print(f"✅ Connexion établie")
        print(f"\n⚠️  ÉTAPES MANUELLES REQUISES:")
        print(f"1. Allez sur: {url.replace('https://', 'https://app.')}")
        print(f"2. Menu 'SQL Editor' → 'New Query'")
        print(f"3. Copiez le contenu de 'setup_supabase_tables.sql'")
        print(f"4. Exécutez la requête")
        print(f"\n📦 CRÉER LE BUCKET STORAGE:")
        print(f"5. Menu 'Storage' → 'New Bucket'")
        print(f"6. Nom: {'avatars-men' if 'man' in name else 'avatars-women'}")
        print(f"7. Public: ✅ Oui")
        
        # Tester la connexion
        result = client.table('profiles').select('count').limit(1).execute()
        print(f"\n✅ Table 'profiles' existe et est accessible!")
        return True
        
    except Exception as e:
        if "Could not find the table" in str(e):
            print(f"\n❌ Table 'profiles' n'existe pas encore")
            print(f"   → Suivez les étapes manuelles ci-dessus")
        else:
            print(f"❌ Erreur: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 INITIALISATION BASES DE DONNÉES SUPABASE")
    print("="*60)
    
    # Configuration Supabase HOMMES
    man_url = os.getenv('profil_man_supabase_URL')
    man_key = os.getenv('profil_man_supabase_API_service_role_secret')
    
    # Configuration Supabase FEMMES
    woman_url = os.getenv('profil_woman_supabase_URL')
    woman_key = os.getenv('profil_woman_supabase_API_service_role_secret')
    
    if not all([man_url, man_key, woman_url, woman_key]):
        print("❌ Variables d'environnement manquantes!")
        return
    
    # Setup des deux bases
    results = {
        'Hommes': setup_database('hommes', man_url, man_key),
        'Femmes': setup_database('femmes', woman_url, woman_key)
    }
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    for db, ok in results.items():
        status = "✅ Prêt" if ok else "⚠️  Configuration manuelle requise"
        print(f"{db}: {status}")
    
    print("\n💡 FICHIER SQL DISPONIBLE: setup_supabase_tables.sql")
    print("   Copiez son contenu dans l'éditeur SQL de chaque instance Supabase")

if __name__ == '__main__':
    main()
