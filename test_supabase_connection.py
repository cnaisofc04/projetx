
import os
from supabase import create_client

# Test de connexion
url = os.getenv('URL_SUPABASE_AUTOQG')
key = os.getenv('api_key_secret_supabase')

print(f"🔧 URL Supabase: {url}")
print(f"🔧 Clé présente: {'✅ Oui' if key else '❌ Non'}")

try:
    supabase = create_client(url, key)
    
    # Test 1: Vérifier la connexion
    result = supabase.table('profiles').select('count').execute()
    print(f"✅ Connexion Supabase OK - {len(result.data)} profils")
    
    # Test 2: Vérifier Storage
    buckets = supabase.storage.list_buckets()
    print(f"✅ Storage OK - {len(buckets)} buckets trouvés")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
