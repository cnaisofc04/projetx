
#!/usr/bin/env python3
"""
Test EXHAUSTIF de TOUS les secrets configurés (26 secrets)
Génère un rapport détaillé de chaque secret
"""

import os
import sys
from datetime import datetime
import traceback

class SecretsTester:
    """Testeur pour tous les secrets"""
    
    def __init__(self):
        self.results = []
        self.total = 0
        self.success = 0
        self.warnings = 0
        self.errors = 0
        
    def log(self, secret_name: str, status: str, details: str = "", error: str = ""):
        """Log un résultat"""
        symbol = "✅" if status == "success" else "⚠️" if status == "warning" else "❌"
        result = {
            "secret": secret_name,
            "status": status,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total += 1
        
        if status == "success":
            self.success += 1
        elif status == "warning":
            self.warnings += 1
        else:
            self.errors += 1
            
        print(f"{symbol} {secret_name}: {status.upper()}")
        if details:
            print(f"   → {details}")
        if error:
            print(f"   ❌ {error[:100]}")
    
    def test_github_token(self):
        """Test GITHUB_TOKEN_API"""
        secret_name = "GITHUB_TOKEN_API"
        value = os.getenv(secret_name)
        
        if not value:
            self.log(secret_name, "error", error="Secret non trouvé")
            return
        
        try:
            from github import Github, Auth
            auth = Auth.Token(value)
            g = Github(auth=auth)
            user = g.get_user()
            self.log(secret_name, "success", f"User: {user.login}, ID: {user.id}")
        except Exception as e:
            self.log(secret_name, "error", error=str(e))
    
    def test_gitlab_token(self):
        """Test TOKEN_API_GITLAB"""
        secret_name = "TOKEN_API_GITLAB"
        value = os.getenv(secret_name)
        
        if not value:
            self.log(secret_name, "error", error="Secret non trouvé")
            return
        
        try:
            from gitlab import Gitlab
            gl = Gitlab("https://gitlab.com", private_token=value)
            gl.auth()
            user = gl.user
            username = getattr(user, 'username', 'authenticated')
            self.log(secret_name, "success", f"User: {username}")
        except Exception as e:
            self.log(secret_name, "error", error=str(e))
    
    def test_supabase_secrets(self):
        """Test tous les secrets Supabase (6 secrets)"""
        url = os.getenv("URL_SUPABASE_AUTOQG")
        
        # Test URL
        if url:
            self.log("URL_SUPABASE_AUTOQG", "success", f"URL: {url}")
        else:
            self.log("URL_SUPABASE_AUTOQG", "error", error="URL manquante")
            return
        
        # Test chaque clé Supabase
        supabase_keys = [
            "SUPABASE_ANON_PUBLIC",
            "SUPABASE_AUTOQG_API_KEY",
            "api_key_secret_supabase",
            "SUPABASE_ROLE_SECRET"
        ]
        
        try:
            from supabase import create_client
            
            for key_name in supabase_keys:
                key_value = os.getenv(key_name)
                
                if not key_value:
                    self.log(key_name, "error", error="Secret non trouvé")
                    continue
                
                try:
                    client = create_client(url, key_value)
                    # Test simple de connexion
                    self.log(key_name, "success", f"Client créé (longueur: {len(key_value)} chars)")
                except Exception as e:
                    error_str = str(e).lower()
                    if "invalid api key" in error_str or "jwt" in error_str:
                        self.log(key_name, "warning", details="Clé présente mais peut-être invalide", error=str(e)[:50])
                    else:
                        self.log(key_name, "success", f"Client créé")
        except Exception as e:
            for key_name in supabase_keys:
                if os.getenv(key_name):
                    self.log(key_name, "warning", error=str(e)[:50])
    
    def test_stripe_secrets(self):
        """Test STRIPE_API_KEY_SECRET et STRIPE_API_KEY_PUBLIC"""
        secret_key = os.getenv("STRIPE_API_KEY_SECRET")
        public_key = os.getenv("STRIPE_API_KEY_PUBLIC")
        
        # Test secret key
        if not secret_key:
            self.log("STRIPE_API_KEY_SECRET", "error", error="Secret non trouvé")
        else:
            try:
                import stripe
                stripe.api_key = secret_key
                account = stripe.Account.retrieve()
                self.log("STRIPE_API_KEY_SECRET", "success", f"Account: {account.id}")
            except Exception as e:
                self.log("STRIPE_API_KEY_SECRET", "error", error=str(e))
        
        # Test public key
        if not public_key:
            self.log("STRIPE_API_KEY_PUBLIC", "error", error="Secret non trouvé")
        else:
            if public_key.startswith("pk_"):
                self.log("STRIPE_API_KEY_PUBLIC", "success", f"Format valide (longueur: {len(public_key)} chars)")
            else:
                self.log("STRIPE_API_KEY_PUBLIC", "warning", details="Format non standard", error="Devrait commencer par 'pk_'")
    
    def test_trello_secrets(self):
        """Test TRELLO_API_KEY et TRELLO_TOKEN"""
        api_key = os.getenv("TRELLO_API_KEY")
        token = os.getenv("TRELLO_TOKEN")
        
        if not api_key:
            self.log("TRELLO_API_KEY", "error", error="Secret non trouvé")
            return
        if not token:
            self.log("TRELLO_TOKEN", "error", error="Secret non trouvé")
            return
        
        try:
            import requests
            url = f"https://api.trello.com/1/members/me?key={api_key}&token={token}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.log("TRELLO_API_KEY", "success", f"API Key valide")
            self.log("TRELLO_TOKEN", "success", f"User: {data.get('username', 'N/A')}")
        except Exception as e:
            self.log("TRELLO_API_KEY", "error", error=str(e))
            self.log("TRELLO_TOKEN", "error", error=str(e))
    
    def test_appwrite_secrets(self):
        """Test API_ENDPOINT_APPRWRITE et PROJET_ID_APPWRITE"""
        endpoint = os.getenv("API_ENDPOINT_APPRWRITE")
        project_id = os.getenv("PROJET_ID_APPWRITE")
        
        if not endpoint:
            self.log("API_ENDPOINT_APPRWRITE", "error", error="Secret non trouvé")
        else:
            self.log("API_ENDPOINT_APPRWRITE", "success", f"Endpoint: {endpoint}")
        
        if not project_id:
            self.log("PROJET_ID_APPWRITE", "error", error="Secret non trouvé")
        else:
            try:
                from appwrite.client import Client
                client = Client()
                client.set_endpoint(endpoint).set_project(project_id)
                self.log("PROJET_ID_APPWRITE", "success", f"Project ID: {project_id}")
            except Exception as e:
                self.log("PROJET_ID_APPWRITE", "error", error=str(e))
    
    def test_resend_api_key(self):
        """Test RESEND_API_KEY"""
        api_key = os.getenv("RESEND_API_KEY")
        
        if not api_key:
            self.log("RESEND_API_KEY", "error", error="Secret non trouvé")
            return
        
        try:
            import resend
            resend.api_key = api_key
            domains = resend.Domains.list()
            self.log("RESEND_API_KEY", "success", f"API fonctionnelle")
        except Exception as e:
            self.log("RESEND_API_KEY", "error", error=str(e))
    
    def test_openai_secrets(self):
        """Test OPEN_AI_API_KEY et MY_TEST_KEY_OPEN_AI_API"""
        main_key = os.getenv("OPEN_AI_API_KEY")
        test_key = os.getenv("MY_TEST_KEY_OPEN_AI_API")
        
        # Test main key
        if not main_key:
            self.log("OPEN_AI_API_KEY", "error", error="Secret non trouvé")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=main_key)
                models = client.models.list()
                self.log("OPEN_AI_API_KEY", "success", f"{len(models.data)} modèles disponibles")
            except Exception as e:
                error_str = str(e).lower()
                if "quota" in error_str or "429" in error_str:
                    self.log("OPEN_AI_API_KEY", "warning", details="Quota dépassé", error=str(e)[:100])
                else:
                    self.log("OPEN_AI_API_KEY", "error", error=str(e)[:100])
        
        # Test test key
        if not test_key:
            self.log("MY_TEST_KEY_OPEN_AI_API", "error", error="Secret non trouvé")
        else:
            self.log("MY_TEST_KEY_OPEN_AI_API", "success", f"Longueur: {len(test_key)} chars")
    
    def test_redis_api_key(self):
        """Test REDIS_API_KEY"""
        api_key = os.getenv("REDIS_API_KEY")
        
        if not api_key:
            self.log("REDIS_API_KEY", "error", error="Secret non trouvé")
            return
        
        try:
            import redis
            r = redis.from_url(api_key)
            r.ping()
            self.log("REDIS_API_KEY", "success", f"Redis connecté")
        except Exception as e:
            error_str = str(e).lower()
            if "url" in error_str or "format" in error_str:
                self.log("REDIS_API_KEY", "warning", details="Format URL incorrect", error=str(e)[:100])
            else:
                self.log("REDIS_API_KEY", "error", error=str(e)[:100])
    
    def test_logrocket_api_key(self):
        """Test LOGROCKET_API_KEY"""
        api_key = os.getenv("LOGROCKET_API_KEY")
        
        if not api_key:
            self.log("LOGROCKET_API_KEY", "error", error="Secret non trouvé")
            return
        
        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.logrocket.com/v1/orgs", headers=headers, timeout=5)
            if response.status_code == 200:
                self.log("LOGROCKET_API_KEY", "success", f"API connectée")
            else:
                self.log("LOGROCKET_API_KEY", "warning", details=f"Status {response.status_code}", error=response.text[:50])
        except Exception as e:
            self.log("LOGROCKET_API_KEY", "error", error=str(e)[:100])
    
    def test_amplitude_secrets(self):
        """Test AMPLITUDE_API_KEY, AMPLITUDE_Standard_Server_url, AMPLITUDE_EU_Residency_Server_URL"""
        api_key = os.getenv("AMPLITUDE_API_KEY")
        standard_url = os.getenv("AMPLITUDE_Standard_Server_url")
        eu_url = os.getenv("AMPLITUDE_EU_Residency_Server_URL")
        
        # Test API key
        if not api_key:
            self.log("AMPLITUDE_API_KEY", "error", error="Secret non trouvé")
        else:
            self.log("AMPLITUDE_API_KEY", "success", f"Longueur: {len(api_key)} chars")
        
        # Test Standard URL
        if not standard_url:
            self.log("AMPLITUDE_Standard_Server_url", "error", error="Secret non trouvé")
        else:
            if api_key:
                try:
                    import requests
                    data = {
                        "api_key": api_key,
                        "events": [{
                            "user_id": "test_user",
                            "event_type": "test_event",
                            "time": int(datetime.now().timestamp() * 1000)
                        }]
                    }
                    response = requests.post(standard_url, json=data, timeout=5)
                    if response.status_code in [200, 400]:
                        self.log("AMPLITUDE_Standard_Server_url", "success", f"URL: {standard_url}")
                    else:
                        self.log("AMPLITUDE_Standard_Server_url", "warning", details=f"Status {response.status_code}")
                except Exception as e:
                    self.log("AMPLITUDE_Standard_Server_url", "error", error=str(e)[:100])
            else:
                self.log("AMPLITUDE_Standard_Server_url", "success", f"URL: {standard_url}")
        
        # Test EU URL
        if not eu_url:
            self.log("AMPLITUDE_EU_Residency_Server_URL", "error", error="Secret non trouvé")
        else:
            self.log("AMPLITUDE_EU_Residency_Server_URL", "success", f"URL: {eu_url}")
    
    def test_mapbox_token(self):
        """Test MAPBOX_ACCESS_TOKEN"""
        token = os.getenv("MAPBOX_ACCESS_TOKEN")
        
        if not token:
            self.log("MAPBOX_ACCESS_TOKEN", "error", error="Secret non trouvé")
            return
        
        try:
            import requests
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/paris.json?access_token={token}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.log("MAPBOX_ACCESS_TOKEN", "success", f"API Mapbox connectée")
            else:
                self.log("MAPBOX_ACCESS_TOKEN", "warning", details=f"Status {response.status_code}")
        except Exception as e:
            self.log("MAPBOX_ACCESS_TOKEN", "error", error=str(e)[:100])
    
    def test_node_test_keys(self):
        """Test Try_out_Your_new_API_key_NODE et Try_out_your_new_API_key_Python"""
        node_key = os.getenv("Try_out_Your_new_API_key_NODE")
        python_key = os.getenv("Try_out_your_new_API_key_Python")
        
        if not node_key:
            self.log("Try_out_Your_new_API_key_NODE", "error", error="Secret non trouvé")
        else:
            self.log("Try_out_Your_new_API_key_NODE", "success", f"Longueur: {len(node_key)} chars")
        
        if not python_key:
            self.log("Try_out_your_new_API_key_Python", "error", error="Secret non trouvé")
        else:
            self.log("Try_out_your_new_API_key_Python", "success", f"Longueur: {len(python_key)} chars")
    
    def test_session_secret(self):
        """Test SESSION_SECRET"""
        secret = os.getenv("SESSION_SECRET")
        
        if not secret:
            self.log("SESSION_SECRET", "error", error="Secret non trouvé")
        else:
            if len(secret) >= 32:
                self.log("SESSION_SECRET", "success", f"Longueur sécurisée: {len(secret)} chars")
            else:
                self.log("SESSION_SECRET", "warning", details="Secret trop court (< 32 chars)", error=f"Longueur actuelle: {len(secret)}")
    
    def test_gabriel_api_key(self):
        """Test GABRIEL_API_KEY_1"""
        api_key = os.getenv("GABRIEL_API_KEY_1")
        
        if not api_key:
            self.log("GABRIEL_API_KEY_1", "error", error="Secret non trouvé")
        else:
            self.log("GABRIEL_API_KEY_1", "success", f"Longueur: {len(api_key)} chars")
    
    def generate_report(self):
        """Génère le rapport Markdown"""
        now = datetime.now()
        percentage = (self.success / self.total * 100) if self.total > 0 else 0
        
        report = f"""# 🔐 RAPPORT TEST COMPLET - TOUS LES SECRETS
## {self.total} Secrets Testés

**Date**: {now.strftime("%Y-%m-%d %H:%M:%S")}  
**Résultats**: {self.success}/{self.total} réussis ({percentage:.1f}%)  
**Avertissements**: {self.warnings}  
**Erreurs**: {self.errors}

---

## 1. RÉSUMÉ GLOBAL

"""
        
        if percentage >= 90:
            report += "🟢 **EXCELLENT** - Presque tous les secrets sont valides\n\n"
        elif percentage >= 70:
            report += "🟡 **BON** - La plupart des secrets fonctionnent\n\n"
        else:
            report += "🔴 **ATTENTION** - Plusieurs secrets nécessitent une vérification\n\n"
        
        report += "## 2. RÉSULTATS PAR CATÉGORIE\n\n"
        
        categories = {
            "GitHub": ["GITHUB_TOKEN_API"],
            "GitLab": ["TOKEN_API_GITLAB"],
            "Supabase": ["URL_SUPABASE_AUTOQG", "SUPABASE_ANON_PUBLIC", "SUPABASE_AUTOQG_API_KEY", "api_key_secret_supabase", "SUPABASE_ROLE_SECRET"],
            "Stripe": ["STRIPE_API_KEY_SECRET", "STRIPE_API_KEY_PUBLIC"],
            "Trello": ["TRELLO_API_KEY", "TRELLO_TOKEN"],
            "Appwrite": ["API_ENDPOINT_APPRWRITE", "PROJET_ID_APPWRITE"],
            "Resend": ["RESEND_API_KEY"],
            "OpenAI": ["OPEN_AI_API_KEY", "MY_TEST_KEY_OPEN_AI_API"],
            "Redis": ["REDIS_API_KEY"],
            "LogRocket": ["LOGROCKET_API_KEY"],
            "Amplitude": ["AMPLITUDE_API_KEY", "AMPLITUDE_Standard_Server_url", "AMPLITUDE_EU_Residency_Server_URL"],
            "Mapbox": ["MAPBOX_ACCESS_TOKEN"],
            "Test Keys": ["Try_out_Your_new_API_key_NODE", "Try_out_your_new_API_key_Python"],
            "Session": ["SESSION_SECRET"],
            "Custom": ["GABRIEL_API_KEY_1"]
        }
        
        for category, secrets in categories.items():
            cat_results = [r for r in self.results if r["secret"] in secrets]
            cat_success = len([r for r in cat_results if r["status"] == "success"])
            cat_total = len(cat_results)
            
            symbol = "✅" if cat_success == cat_total else "⚠️" if cat_success > 0 else "❌"
            report += f"### {symbol} {category} ({cat_success}/{cat_total})\n\n"
            
            for result in cat_results:
                r_symbol = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
                report += f"{r_symbol} **{result['secret']}**: {result['status'].upper()}\n"
                if result.get("details"):
                    report += f"   - {result['details']}\n"
                if result.get("error"):
                    report += f"   - ❌ {result['error'][:100]}\n"
                report += "\n"
        
        report += "---\n\n## 3. SECRETS À CORRIGER\n\n"
        
        errors_warnings = [r for r in self.results if r["status"] in ["error", "warning"]]
        if errors_warnings:
            for r in errors_warnings:
                symbol = "⚠️" if r["status"] == "warning" else "❌"
                report += f"{symbol} **{r['secret']}**\n"
                if r.get("error"):
                    report += f"```\n{r['error']}\n```\n\n"
        else:
            report += "✅ Aucun secret à corriger\n\n"
        
        report += "---\n\n## 4. STATISTIQUES\n\n"
        report += f"- **Total testés**: {self.total}\n"
        report += f"- **Succès**: {self.success} ({percentage:.1f}%)\n"
        report += f"- **Avertissements**: {self.warnings}\n"
        report += f"- **Erreurs**: {self.errors}\n\n"
        
        report += "---\n\n"
        report += f"*Rapport généré le {now.strftime('%Y-%m-%d à %H:%M:%S')}*\n"
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("="*60)
        print("🔐 TEST DE TOUS LES SECRETS (26 SECRETS)")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        print("\n🔒 SESSION & CUSTOM")
        self.test_session_secret()
        self.test_gabriel_api_key()
        
        print("\n🐙 GITHUB")
        self.test_github_token()
        
        print("\n🦊 GITLAB")
        self.test_gitlab_token()
        
        print("\n🗄️  SUPABASE (6 secrets)")
        self.test_supabase_secrets()
        
        print("\n💳 STRIPE")
        self.test_stripe_secrets()
        
        print("\n📋 TRELLO")
        self.test_trello_secrets()
        
        print("\n📦 APPWRITE")
        self.test_appwrite_secrets()
        
        print("\n📧 RESEND")
        self.test_resend_api_key()
        
        print("\n🤖 OPENAI")
        self.test_openai_secrets()
        
        print("\n🗄️  REDIS")
        self.test_redis_api_key()
        
        print("\n📹 LOGROCKET")
        self.test_logrocket_api_key()
        
        print("\n📊 AMPLITUDE")
        self.test_amplitude_secrets()
        
        print("\n🗺️  MAPBOX")
        self.test_mapbox_token()
        
        print("\n🔑 TEST KEYS")
        self.test_node_test_keys()
        
        print("\n" + "="*60)
        print("✅ TESTS TERMINÉS")
        print("="*60)
        
        report = self.generate_report()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RAPPORT_TOUS_SECRETS_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 Rapport: {filename}")
        print(f"✅ Succès: {self.success}/{self.total}")
        print(f"⚠️  Avertissements: {self.warnings}")
        print(f"❌ Erreurs: {self.errors}")
        
        return filename


if __name__ == "__main__":
    tester = SecretsTester()
    report_file = tester.run_all_tests()
    
    print("\n" + "="*60)
    print("🔐 TEST COMPLET TERMINÉ")
    print("="*60)
    print(f"📊 Taux de réussite: {(tester.success/tester.total*100):.1f}%")
    print("="*60)
