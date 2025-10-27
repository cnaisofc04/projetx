
#!/usr/bin/env python3
"""
Script de test exhaustif pour TOUTES les nouvelles API
Teste: OpenAI, Redis, LogRocket, Amplitude + anciennes API
"""

import os
import sys
from datetime import datetime
from typing import Dict, List

# Vérifier les imports
try:
    import requests
    from github import Github, Auth
    from gitlab import Gitlab
    from supabase import create_client
    from appwrite.client import Client as AppwriteClient
    from appwrite.services.databases import Databases
    import stripe
    import resend
except ImportError as e:
    print(f"❌ Import manquant: {e}")
    print("Installation en cours...")
    sys.exit(1)


class NewAPITester:
    """Testeur pour toutes les nouvelles API"""
    
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.success_count = 0
        self.error_count = 0
        
    def log_result(self, api: str, test: str, status: str, details: str = "", error: str = ""):
        """Enregistrer un résultat de test"""
        symbol = "✅" if status == "success" else "❌" if status == "error" else "⚠️"
        result = {
            "api": api,
            "test": test,
            "status": status,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total_tests += 1
        
        if status == "success":
            self.success_count += 1
        elif status == "error":
            self.error_count += 1
            
        print(f"{symbol} {api} - {test}: {status.upper()}")
        if details:
            print(f"   → {details}")
        if error:
            print(f"   ❌ {error}")
    
    def test_openai_api(self):
        """Test de l'API OpenAI"""
        print("\n" + "="*60)
        print("🤖 OPENAI API - TESTS")
        print("="*60)
        
        api_key = os.getenv("OPEN_AI_API_KEY") or os.getenv("MY_TEST_KEY_OPEN_AI_API")
        
        if not api_key:
            self.log_result("OpenAI", "Configuration", "error", error="Clé API non trouvée")
            return False
        
        try:
            # Import OpenAI
            try:
                from openai import OpenAI
            except ImportError:
                self.log_result("OpenAI", "Import", "error", error="Package 'openai' non installé. Run: uv add openai")
                return False
            
            # Test 1: Initialisation client
            try:
                client = OpenAI(api_key=api_key)
                self.log_result("OpenAI", "Initialisation Client", "success", "Client créé")
            except Exception as e:
                self.log_result("OpenAI", "Initialisation Client", "error", error=str(e))
                return False
            
            # Test 2: Liste des modèles disponibles
            try:
                models = client.models.list()
                model_names = [m.id for m in models.data[:5]]
                self.log_result("OpenAI", "Liste Modèles", "success", f"Modèles: {', '.join(model_names[:3])}")
            except Exception as e:
                self.log_result("OpenAI", "Liste Modèles", "error", error=str(e))
            
            # Test 3: Chat Completion (GPT-3.5 pour économiser)
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant de test."},
                        {"role": "user", "content": "Réponds juste 'OK' si tu me lis."}
                    ],
                    max_tokens=10
                )
                answer = response.choices[0].message.content
                self.log_result("OpenAI", "Chat Completion", "success", f"Réponse: {answer}")
            except Exception as e:
                self.log_result("OpenAI", "Chat Completion", "error", error=str(e))
            
            return True
            
        except Exception as e:
            self.log_result("OpenAI", "Tests", "error", error=str(e))
            return False
    
    def test_redis_api(self):
        """Test de Redis (si configuré)"""
        print("\n" + "="*60)
        print("🔴 REDIS API - TESTS")
        print("="*60)
        
        api_key = os.getenv("REDIS_API_KEY")
        
        if not api_key:
            self.log_result("Redis", "Configuration", "warning", "Clé API non trouvée (optionnel)")
            return False
        
        try:
            # Import redis
            try:
                import redis
            except ImportError:
                self.log_result("Redis", "Import", "warning", "Package 'redis' non installé. Run: uv add redis")
                return False
            
            # Test 1: Connexion (si URL fournie)
            redis_url = os.getenv("REDIS_URL")
            if redis_url:
                try:
                    r = redis.from_url(redis_url)
                    r.ping()
                    self.log_result("Redis", "Connexion", "success", "Ping OK")
                except Exception as e:
                    self.log_result("Redis", "Connexion", "error", error=str(e))
            else:
                self.log_result("Redis", "Configuration URL", "warning", "REDIS_URL non configurée")
            
            return True
            
        except Exception as e:
            self.log_result("Redis", "Tests", "error", error=str(e))
            return False
    
    def test_logrocket_api(self):
        """Test de LogRocket"""
        print("\n" + "="*60)
        print("📹 LOGROCKET API - TESTS")
        print("="*60)
        
        api_key = os.getenv("LOGROCKET_API_KEY")
        
        if not api_key:
            self.log_result("LogRocket", "Configuration", "warning", "Clé API non trouvée (optionnel)")
            return False
        
        # LogRocket est principalement client-side (JavaScript)
        # On peut juste vérifier que la clé existe
        self.log_result("LogRocket", "Configuration Clé", "success", "Clé API présente (frontend JS requis)")
        
        # Test de l'API REST si disponible
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.logrocket.com/v1/orgs",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_result("LogRocket", "API REST", "success", "API accessible")
            else:
                self.log_result("LogRocket", "API REST", "warning", 
                              f"Status {response.status_code} (vérifier clé)")
        except Exception as e:
            self.log_result("LogRocket", "API REST", "warning", error=str(e))
        
        return True
    
    def test_amplitude_api(self):
        """Test de Amplitude Analytics"""
        print("\n" + "="*60)
        print("📊 AMPLITUDE API - TESTS")
        print("="*60)
        
        api_key = os.getenv("AMPLITUDE_API_KEY")
        
        if not api_key:
            self.log_result("Amplitude", "Configuration", "warning", "Clé API non trouvée (optionnel)")
            return False
        
        try:
            # Test 1: Configuration OK
            self.log_result("Amplitude", "Configuration Clé", "success", "Clé API présente")
            
            # Test 2: Envoi event de test
            try:
                event_data = {
                    "api_key": api_key,
                    "events": [{
                        "user_id": "test_user",
                        "event_type": "api_test",
                        "time": int(datetime.now().timestamp() * 1000),
                        "event_properties": {
                            "source": "audit_script"
                        }
                    }]
                }
                
                response = requests.post(
                    "https://api2.amplitude.com/2/httpapi",
                    json=event_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_result("Amplitude", "Envoi Event", "success", 
                                  f"Event envoyé: {result.get('events_ingested', 0)} ingested")
                else:
                    self.log_result("Amplitude", "Envoi Event", "warning", 
                                  f"Status {response.status_code}")
            except Exception as e:
                self.log_result("Amplitude", "Envoi Event", "error", error=str(e))
            
            return True
            
        except Exception as e:
            self.log_result("Amplitude", "Tests", "error", error=str(e))
            return False
    
    def test_existing_apis(self):
        """Test rapide des API existantes"""
        print("\n" + "="*60)
        print("🔄 VÉRIFICATION API EXISTANTES")
        print("="*60)
        
        # GitHub
        github_token = os.getenv("GITHUB_TOKEN_API")
        if github_token:
            try:
                auth = Auth.Token(github_token)
                g = Github(auth=auth)
                user = g.get_user()
                self.log_result("GitHub", "Quick Check", "success", f"User: {user.login}")
            except Exception as e:
                self.log_result("GitHub", "Quick Check", "error", error=str(e))
        
        # GitLab
        gitlab_token = os.getenv("TOKEN_API_GITLAB")
        if gitlab_token:
            try:
                gl = Gitlab("https://gitlab.com", private_token=gitlab_token)
                gl.auth()
                self.log_result("GitLab", "Quick Check", "success", "Auth OK")
            except Exception as e:
                self.log_result("GitLab", "Quick Check", "error", error=str(e))
        
        # Supabase
        supabase_url = os.getenv("URL_SUPABASE_AUTOQG")
        supabase_key = os.getenv("SUPABASE_ANON_PUBLIC")
        if supabase_url and supabase_key:
            try:
                supabase = create_client(supabase_url, supabase_key)
                self.log_result("Supabase", "Quick Check", "success", "Client créé")
            except Exception as e:
                self.log_result("Supabase", "Quick Check", "error", error=str(e))
        
        # Stripe
        stripe_key = os.getenv("STRIPE_API_KEY_SECRET")
        if stripe_key:
            try:
                stripe.api_key = stripe_key
                account = stripe.Account.retrieve()
                self.log_result("Stripe", "Quick Check", "success", f"Account: {account.id}")
            except Exception as e:
                self.log_result("Stripe", "Quick Check", "error", error=str(e))
        
        # Trello
        trello_key = os.getenv("TRELLO_API_KEY")
        trello_token = os.getenv("TRELLO_TOKEN")
        if trello_key and trello_token:
            try:
                url = f"https://api.trello.com/1/members/me?key={trello_key}&token={trello_token}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_result("Trello", "Quick Check", "success", f"User: {data.get('username')}")
            except Exception as e:
                self.log_result("Trello", "Quick Check", "error", error=str(e))
        
        # Resend
        resend_key = os.getenv("RESEND_API_KEY")
        if resend_key:
            try:
                resend.api_key = resend_key
                domains = resend.Domains.list()
                self.log_result("Resend", "Quick Check", "success", "API OK")
            except Exception as e:
                self.log_result("Resend", "Quick Check", "error", error=str(e))
    
    def generate_report(self):
        """Générer rapport Markdown"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        success_rate = (self.success_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        report = f"""# 🚀 RAPPORT TEST NOUVELLES API
**Date**: {now.strftime("%Y-%m-%d %H:%M:%S")}  
**Tests**: {self.total_tests}  
**Réussis**: {self.success_count} ({success_rate:.1f}%)  
**Échecs**: {self.error_count}

---

## 📋 RÉSUMÉ PAR API

"""
        
        # Grouper par API
        apis = {}
        for result in self.results:
            api = result["api"]
            if api not in apis:
                apis[api] = []
            apis[api].append(result)
        
        for api, tests in sorted(apis.items()):
            success = len([t for t in tests if t["status"] == "success"])
            total = len(tests)
            symbol = "✅" if success == total else "⚠️" if success > 0 else "❌"
            
            report += f"### {symbol} {api} ({success}/{total})\n\n"
            
            for test in tests:
                symbol = "✅" if test["status"] == "success" else "⚠️" if test["status"] == "warning" else "❌"
                report += f"{symbol} **{test['test']}**: {test['status'].upper()}\n"
                if test.get("details"):
                    report += f"   - {test['details']}\n"
                if test.get("error"):
                    report += f"   - ❌ `{test['error']}`\n"
                report += "\n"
        
        report += "\n---\n\n## 📊 STATISTIQUES GLOBALES\n\n"
        report += f"- **Total tests**: {self.total_tests}\n"
        report += f"- **Succès**: {self.success_count} ({success_rate:.1f}%)\n"
        report += f"- **Échecs**: {self.error_count}\n"
        report += f"- **Warnings**: {len([r for r in self.results if r['status'] == 'warning'])}\n\n"
        
        if success_rate >= 90:
            report += "🟢 **EXCELLENT** - Toutes les nouvelles API sont fonctionnelles\n\n"
        elif success_rate >= 70:
            report += "🟡 **BON** - La plupart des API fonctionnent\n\n"
        else:
            report += "🔴 **ATTENTION** - Plusieurs API nécessitent configuration\n\n"
        
        report += "---\n\n"
        report += "*Rapport généré automatiquement*\n"
        
        filename = f"RAPPORT_NOUVELLES_API_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        return filename
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 DÉMARRAGE TEST NOUVELLES API")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Nouvelles API
        self.test_openai_api()
        self.test_redis_api()
        self.test_logrocket_api()
        self.test_amplitude_api()
        
        # Vérification rapide anciennes API
        self.test_existing_apis()
        
        print("\n" + "="*60)
        print("✅ TESTS TERMINÉS")
        print("="*60)
        
        report_file = self.generate_report()
        
        print(f"\n📄 Rapport: {report_file}")
        print(f"📊 Succès: {self.success_count}/{self.total_tests}")
        print(f"❌ Échecs: {self.error_count}")
        print("="*60)


if __name__ == "__main__":
    tester = NewAPITester()
    tester.run_all_tests()
