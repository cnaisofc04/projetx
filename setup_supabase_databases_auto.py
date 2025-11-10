
#!/usr/bin/env python3
"""
Script pour créer AUTOMATIQUEMENT les tables dans Supabase via PostgreSQL
Nécessite les chaînes de connexion PostgreSQL complètes
"""
import os
import sys

try:
    import psycopg2
except ImportError:
    print("❌ psycopg2 non installé. Installation...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

# Schéma SQL
SQL_SCHEMA = """
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
  
  CONSTRAINT check_gender CHECK ((gender = 'man') OR (gender = 'woman'))
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

-- Désactiver RLS pour le développement
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;
"""

def setup_database_postgres(name, db_url):
    """Créer les tables via connexion PostgreSQL directe"""
    print(f"\n{'='*60}")
    print(f"🔧 CONFIGURATION SUPABASE {name.upper()} (PostgreSQL)")
    print(f"{'='*60}")
    
    if not db_url:
        print(f"❌ Variable DATABASE_URL_{name.upper()} non définie dans les secrets")
        print(f"   Ajoutez la chaîne de connexion PostgreSQL complète:")
        print(f"   postgres://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres")
        return False
    
    try:
        # Connexion PostgreSQL
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Exécuter le schéma SQL
        cur.execute(SQL_SCHEMA)
        
        # Vérifier la création
        cur.execute("SELECT COUNT(*) FROM profiles")
        
        print(f"✅ Table 'profiles' créée avec succès!")
        print(f"✅ Index créés")
        print(f"✅ Triggers configurés")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion PostgreSQL: {e}")
        print(f"\n💡 POUR OBTENIR L'URL PostgreSQL:")
        print(f"1. Dashboard Supabase → Settings → Database")
        print(f"2. Copiez 'Connection string' (URI)")
        print(f"3. Ajoutez dans Replit Secrets:")
        print(f"   DATABASE_URL_{name.upper()} = postgres://...")
        return False
        
    except Exception as e:
        print(f"❌ Erreur SQL: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 CRÉATION AUTOMATIQUE DES TABLES SUPABASE")
    print("="*60)
    
    # URLs PostgreSQL complètes (à ajouter dans les secrets)
    man_db_url = os.getenv('DATABASE_URL_MAN')
    woman_db_url = os.getenv('DATABASE_URL_WOMAN')
    
    results = {}
    
    if man_db_url:
        results['Hommes'] = setup_database_postgres('man', man_db_url)
    else:
        print("\n⚠️  DATABASE_URL_MAN non définie - configuration manuelle requise pour HOMMES")
        results['Hommes'] = False
    
    if woman_db_url:
        results['Femmes'] = setup_database_postgres('woman', woman_db_url)
    else:
        print("\n⚠️  DATABASE_URL_WOMAN non définie - configuration manuelle requise pour FEMMES")
        results['Femmes'] = False
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    for db, ok in results.items():
        status = "✅ Tables créées automatiquement" if ok else "⚠️  Configuration manuelle requise"
        print(f"{db}: {status}")
    
    if not any(results.values()):
        print("\n" + "="*60)
        print("📝 INSTRUCTIONS POUR CONFIGURATION MANUELLE")
        print("="*60)
        print("1. Ouvrez setup_supabase_tables.sql")
        print("2. Copiez tout le contenu")
        print("3. Dashboard Supabase → SQL Editor → New Query")
        print("4. Collez et exécutez")
        print("\nOU ajoutez les URLs PostgreSQL dans Secrets:")
        print("  DATABASE_URL_MAN=postgres://postgres:[PWD]@db.[PROJECT].supabase.co:5432/postgres")
        print("  DATABASE_URL_WOMAN=postgres://postgres:[PWD]@db.[PROJECT].supabase.co:5432/postgres")

if __name__ == '__main__':
    main()
