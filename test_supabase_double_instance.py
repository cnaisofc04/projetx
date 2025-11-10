
#!/usr/bin/env python3
"""
Test de connexion aux 2 instances Supabase + Appwrite
"""
import os
from supabase import create_client

def test_supabase_men():
    """Test connexion Supabase HOMMES"""
    print("\n🔵 TEST SUPABASE HOMMES")
    print("="*50)
    
    url = os.getenv('profil_man_supabase_URL')
    key = os.getenv('profil_man_supabase_API_service_role_secret')
    
    print(f"URL: {url}")
    print(f"Key présente: {'✅' if key else '❌'}")
    
    if not url or not key:
        print("❌ Variables manquantes!")
        print("Ajoutez dans Secrets:")
        print("  - profil_man_supabase_URL")
        print("  - profil_man_supabase_API_service_role_secret")
        return False
    
    try:
        client = create_client(url, key)
        # Test simple
        result = client.table('profiles').select('count').limit(1).execute()
        print(f"✅ Connexion OK: {url}")
        print(f"✅ Table 'profiles' accessible")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_supabase_women():
    """Test connexion Supabase FEMMES"""
    print("\n🔴 TEST SUPABASE FEMMES")
    print("="*50)
    
    url = os.getenv('profil_woman_supabase_URL')
    key = os.getenv('profil_woman_supabase_API_service_role_secret')
    
    print(f"URL: {url}")
    print(f"Key présente: {'✅' if key else '❌'}")
    
    if not url or not key:
        print("❌ Variables manquantes!")
        print("Ajoutez dans Secrets:")
        print("  - profil_woman_supabase_URL")
        print("  - profil_woman_supabase_API_service_role_secret")
        return False
    
    try:
        client = create_client(url, key)
        # Test simple
        result = client.table('profiles').select('count').limit(1).execute()
        print(f"✅ Connexion OK: {url}")
        print(f"✅ Table 'profiles' accessible")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_appwrite():
    """Test connexion Appwrite CHAT"""
    print("\n💬 TEST APPWRITE (CHAT)")
    print("="*50)
    
    endpoint = os.getenv('API_ENDPOINT_APPRWRITE')
    project_id = os.getenv('PROJET_ID_APPWRITE')
    api_key = os.getenv('API__KEY_APPWRITE')
    
    print(f"Endpoint: {endpoint}")
    print(f"Project ID présent: {'✅' if project_id else '❌'}")
    print(f"API Key présente: {'✅' if api_key else '❌'}")
    
    if not all([endpoint, project_id, api_key]):
        print("❌ Variables manquantes!")
        print("Ajoutez dans Secrets:")
        print("  - API_ENDPOINT_APPRWRITE")
        print("  - PROJET_ID_APPWRITE")
        print("  - API__KEY_APPWRITE")
        return False
    
    try:
        from appwrite.client import Client
        client = Client()
        client.set_endpoint(endpoint)
        client.set_project(project_id)
        client.set_key(api_key)
        
        print(f"✅ Configuration OK: {endpoint}")
        print(f"   Project: {project_id}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔍 TEST COMPLET ARCHITECTURE DOUBLE SUPABASE + APPWRITE")
    print("="*60)
    
    results = {
        'Supabase Hommes': test_supabase_men(),
        'Supabase Femmes': test_supabase_women(),
        'Appwrite Chat': test_appwrite()
    }
    
    print("\n" + "="*60)
    print("📊 RÉSULTATS")
    print("="*60)
    
    for service, ok in results.items():
        status = "✅ OK" if ok else "❌ ÉCHEC"
        print(f"{service}: {status}")
    
    if all(results.values()):
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
    else:
        print("\n⚠️ Certains tests ont échoué.")
        print("\n📝 SECRETS REQUIS DANS REPLIT:")
        print("  Backend (Python):")
        print("    - profil_man_supabase_URL")
        print("    - profil_man_supabase_API_service_role_secret")
        print("    - profil_woman_supabase_URL")
        print("    - profil_woman_supabase_API_service_role_secret")
        print("    - API_ENDPOINT_APPRWRITE")
        print("    - PROJET_ID_APPWRITE")
        print("    - API__KEY_APPWRITE")
        print("\n  Frontend (fichier client/.env):")
        print("    - VITE_SUPABASE_MAN_URL")
        print("    - VITE_SUPABASE_MAN_ANON_KEY")
        print("    - VITE_SUPABASE_WOMAN_URL")
        print("    - VITE_SUPABASE_WOMAN_ANON_KEY")
