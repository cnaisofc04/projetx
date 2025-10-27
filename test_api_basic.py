
#!/usr/bin/env python3
"""
Script de test BASIQUE pour toutes les API
Tests rapides et essentiels uniquement
"""

import os
import sys
from datetime import datetime

def test_github():
    """Test basique GitHub"""
    print("\n🐙 GITHUB")
    token = os.getenv("GITHUB_TOKEN_API")
    if not token:
        print("❌ Token manquant")
        return False
    
    try:
        from github import Github, Auth
        auth = Auth.Token(token)
        g = Github(auth=auth)
        user = g.get_user()
        print(f"✅ Connecté: {user.login}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_gitlab():
    """Test basique GitLab"""
    print("\n🦊 GITLAB")
    token = os.getenv("TOKEN_API_GITLAB")
    if not token:
        print("❌ Token manquant")
        return False
    
    try:
        from gitlab import Gitlab
        gl = Gitlab("https://gitlab.com", private_token=token)
        gl.auth()
        user = gl.user
        username = getattr(user, 'username', 'authenticated')
        print(f"✅ Connecté: {username}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_supabase():
    """Test basique Supabase"""
    print("\n🗄️  SUPABASE")
    url = os.getenv("URL_SUPABASE_AUTOQG")
    key = os.getenv("SUPABASE_ANON_PUBLIC")
    
    if not url or not key:
        print("❌ Configuration manquante")
        return False
    
    try:
        from supabase import create_client
        supabase = create_client(url, key)
        print("✅ Client créé")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_stripe():
    """Test basique Stripe"""
    print("\n💳 STRIPE")
    api_key = os.getenv("STRIPE_API_KEY_SECRET")
    if not api_key:
        print("❌ API key manquante")
        return False
    
    try:
        import stripe
        stripe.api_key = api_key
        account = stripe.Account.retrieve()
        print(f"✅ Account: {account.id}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_trello():
    """Test basique Trello"""
    print("\n📋 TRELLO")
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    
    if not api_key or not token:
        print("❌ Configuration manquante")
        return False
    
    try:
        import requests
        url = f"https://api.trello.com/1/members/me?key={api_key}&token={token}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ User: {data.get('username')}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_resend():
    """Test basique Resend"""
    print("\n📧 RESEND")
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("❌ API key manquante")
        return False
    
    try:
        import resend
        resend.api_key = api_key
        resend.Domains.list()
        print("✅ API fonctionnelle")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_openai():
    """Test basique OpenAI"""
    print("\n🤖 OPENAI")
    api_key = os.getenv("OPEN_AI_API_KEY") or os.getenv("MY_TEST_KEY_OPEN_AI_API")
    
    if not api_key:
        print("❌ API key manquante")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        print(f"✅ {len(models.data)} modèles disponibles")
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:100]}")
        return False

def test_appwrite():
    """Test basique Appwrite"""
    print("\n📦 APPWRITE")
    endpoint = os.getenv("API_ENDPOINT_APPRWRITE")
    project_id = os.getenv("PROJET_ID_APPWRITE")
    
    if not endpoint or not project_id:
        print("❌ Configuration manquante")
        return False
    
    try:
        from appwrite.client import Client
        client = Client()
        client.set_endpoint(endpoint).set_project(project_id)
        print("✅ Client créé")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Exécute tous les tests basiques"""
    print("="*60)
    print("🚀 TESTS BASIQUES - TOUTES LES API")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {
        "GitHub": test_github(),
        "GitLab": test_gitlab(),
        "Supabase": test_supabase(),
        "Stripe": test_stripe(),
        "Trello": test_trello(),
        "Resend": test_resend(),
        "OpenAI": test_openai(),
        "Appwrite": test_appwrite(),
    }
    
    print("\n" + "="*60)
    print("📊 RÉSULTATS")
    print("="*60)
    
    success = sum(1 for v in results.values() if v)
    total = len(results)
    
    for api, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {api}")
    
    print("="*60)
    print(f"Succès: {success}/{total} ({success/total*100:.1f}%)")
    print("="*60)

if __name__ == "__main__":
    main()
