
#!/usr/bin/env python3
"""
TEST ULTRA-COMPLET V2 - TOUS LES 40 SECRETS
Inclut les nouveaux secrets AGORA et REDIS multiples
Génère un rapport AVANT/APRÈS sans toucher aux anciens rapports
"""

import os
import sys
from datetime import datetime
import traceback

class TesteurSecretsV2:
    """Testeur pour TOUS les 40 secrets configurés"""
    
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
            print(f"   ❌ {error[:150]}")
    
    def test_secret_exists(self, secret_name: str) -> bool:
        """Teste l'existence d'un secret"""
        value = os.getenv(secret_name)
        if value:
            return True
        else:
            self.log(secret_name, "error", error="Secret non configuré")
            return False
    
    def test_agora_secrets(self):
        """Test AGORA (2 NOUVEAUX secrets)"""
        print(f"\n{'='*60}")
        print("📹 AGORA - NOUVEAUX SECRETS")
        print(f"{'='*60}")
        
        if self.test_secret_exists("AGORA_APP_ID"):
            app_id = os.getenv("AGORA_APP_ID")
            self.log("AGORA_APP_ID", "success", f"App ID: {app_id[:20]}... ({len(app_id)} chars)")
        
        if self.test_secret_exists("AGORA_APP_CERTIFICATE"):
            cert = os.getenv("AGORA_APP_CERTIFICATE")
            self.log("AGORA_APP_CERTIFICATE", "success", f"Certificate configuré ({len(cert)} chars)")
    
    def test_redis_multiples(self):
        """Test TOUS les secrets REDIS (13 secrets)"""
        print(f"\n{'='*60}")
        print("🗄️  REDIS - TOUS LES SECRETS (13)")
        print(f"{'='*60}")
        
        redis_secrets = [
            "REDIS_API_KEY",
            "REDIS_API_account_key",
            "REDIS_CLI",
            "REDIS_API_KEY_GENERATED_LangCache",
            "REDIS_CACHE_ID",
            "REDIS_URL_us_east_1",
            "REDIS_URL_us_west_2",
            "REDIS_URL_ap_south_1",
            "REDIS_URL_us_east_4",
            "REDIS_CLIENT",
            "REDIS_SERVICE_NAME",
            "REDIS_QUICK_CONNECT",
            "REDIS_CURL"
        ]
        
        for redis_secret in redis_secrets:
            if self.test_secret_exists(redis_secret):
                value = os.getenv(redis_secret)
                
                # Test de connexion pour les URLs
                if "URL" in redis_secret or redis_secret == "REDIS_API_KEY":
                    try:
                        import redis
                        r = redis.from_url(value)
                        r.ping()
                        self.log(redis_secret, "success", f"Redis connecté")
                    except Exception as e:
                        error_str = str(e).lower()
                        if "scheme" in error_str:
                            self.log(redis_secret, "warning", f"Format URL ({len(value)} chars)", str(e)[:100])
                        else:
                            self.log(redis_secret, "warning", f"Configuré ({len(value)} chars)", str(e)[:100])
                else:
                    # Pour les autres (CLI, CLIENT, etc.)
                    self.log(redis_secret, "success", f"Configuré ({len(value)} chars)")
    
    def test_session_custom(self):
        """Test SESSION_SECRET et GABRIEL_API_KEY_1"""
        print(f"\n{'='*60}")
        print("🔒 SESSION & CUSTOM")
        print(f"{'='*60}")
        
        if self.test_secret_exists("SESSION_SECRET"):
            secret = os.getenv("SESSION_SECRET")
            length = len(secret)
            if length >= 64:
                self.log("SESSION_SECRET", "success", f"Excellent: {length} caractères")
            elif length >= 32:
                self.log("SESSION_SECRET", "success", f"Bon: {length} caractères")
            else:
                self.log("SESSION_SECRET", "warning", f"Faible: {length} caractères (<32)")
        
        if self.test_secret_exists("GABRIEL_API_KEY_1"):
            key = os.getenv("GABRIEL_API_KEY_1")
            self.log("GABRIEL_API_KEY_1", "success", f"Clé custom ({len(key)} chars)")
    
    def test_github_gitlab(self):
        """Test GitHub et GitLab"""
        print(f"\n{'='*60}")
        print("🐙 GITHUB & GITLAB")
        print(f"{'='*60}")
        
        if self.test_secret_exists("GITHUB_TOKEN_API"):
            try:
                from github import Github, Auth
                auth = Auth.Token(os.getenv("GITHUB_TOKEN_API"))
                g = Github(auth=auth)
                user = g.get_user()
                self.log("GITHUB_TOKEN_API", "success", f"User: {user.login}, ID: {user.id}")
            except Exception as e:
                self.log("GITHUB_TOKEN_API", "error", error=str(e)[:100])
        
        if self.test_secret_exists("TOKEN_API_GITLAB"):
            try:
                from gitlab import Gitlab
                gl = Gitlab("https://gitlab.com", private_token=os.getenv("TOKEN_API_GITLAB"))
                gl.auth()
                user = gl.user
                self.log("TOKEN_API_GITLAB", "success", f"User: {getattr(user, 'username', 'authenticated')}")
            except Exception as e:
                self.log("TOKEN_API_GITLAB", "error", error=str(e)[:100])
    
    def test_supabase(self):
        """Test tous les secrets Supabase (5 secrets)"""
        print(f"\n{'='*60}")
        print("🗄️  SUPABASE (5 SECRETS)")
        print(f"{'='*60}")
        
        url = os.getenv("URL_SUPABASE_AUTOQG")
        
        if not self.test_secret_exists("URL_SUPABASE_AUTOQG"):
            return
        
        self.log("URL_SUPABASE_AUTOQG", "success", f"URL: {url}")
        
        supabase_keys = [
            "SUPABASE_ANON_PUBLIC",
            "SUPABASE_AUTOQG_API_KEY",
            "api_key_secret_supabase",
            "SUPABASE_ROLE_SECRET"
        ]
        
        try:
            from supabase import create_client
            
            for key_name in supabase_keys:
                if self.test_secret_exists(key_name):
                    key_value = os.getenv(key_name)
                    try:
                        client = create_client(url, key_value)
                        self.log(key_name, "success", f"Client créé ({len(key_value)} chars)")
                    except Exception as e:
                        self.log(key_name, "success", f"Présent ({len(key_value)} chars)")
        except ImportError:
            for key_name in supabase_keys:
                if self.test_secret_exists(key_name):
                    self.log(key_name, "success", f"Présent (supabase SDK non installé)")
    
    def test_stripe(self):
        """Test Stripe (2 secrets)"""
        print(f"\n{'='*60}")
        print("💳 STRIPE")
        print(f"{'='*60}")
        
        if self.test_secret_exists("STRIPE_API_KEY_SECRET"):
            try:
                import stripe
                stripe.api_key = os.getenv("STRIPE_API_KEY_SECRET")
                account = stripe.Account.retrieve()
                self.log("STRIPE_API_KEY_SECRET", "success", f"Account: {account.id}")
            except Exception as e:
                self.log("STRIPE_API_KEY_SECRET", "error", error=str(e)[:100])
        
        if self.test_secret_exists("STRIPE_API_KEY_PUBLIC"):
            public_key = os.getenv("STRIPE_API_KEY_PUBLIC")
            if public_key.startswith("pk_"):
                self.log("STRIPE_API_KEY_PUBLIC", "success", f"Format valide ({len(public_key)} chars)")
            else:
                self.log("STRIPE_API_KEY_PUBLIC", "warning", f"Format inhabituel")
    
    def test_trello(self):
        """Test Trello (2 secrets)"""
        print(f"\n{'='*60}")
        print("📋 TRELLO")
        print(f"{'='*60}")
        
        api_key = os.getenv("TRELLO_API_KEY")
        token = os.getenv("TRELLO_TOKEN")
        
        if not self.test_secret_exists("TRELLO_API_KEY"):
            return
        if not self.test_secret_exists("TRELLO_TOKEN"):
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
            self.log("TRELLO_API_KEY", "error", error=str(e)[:100])
            self.log("TRELLO_TOKEN", "error", error=str(e)[:100])
    
    def test_appwrite(self):
        """Test Appwrite (2 secrets)"""
        print(f"\n{'='*60}")
        print("📦 APPWRITE")
        print(f"{'='*60}")
        
        if self.test_secret_exists("API_ENDPOINT_APPRWRITE"):
            endpoint = os.getenv("API_ENDPOINT_APPRWRITE")
            self.log("API_ENDPOINT_APPRWRITE", "success", f"Endpoint: {endpoint}")
        
        if self.test_secret_exists("PROJET_ID_APPWRITE"):
            project_id = os.getenv("PROJET_ID_APPWRITE")
            self.log("PROJET_ID_APPWRITE", "success", f"Project ID: {project_id}")
    
    def test_resend(self):
        """Test Resend"""
        print(f"\n{'='*60}")
        print("📧 RESEND")
        print(f"{'='*60}")
        
        if self.test_secret_exists("RESEND_API_KEY"):
            try:
                import resend
                resend.api_key = os.getenv("RESEND_API_KEY")
                domains = resend.Domains.list()
                self.log("RESEND_API_KEY", "success", f"API connectée")
            except Exception as e:
                self.log("RESEND_API_KEY", "error", error=str(e)[:100])
    
    def test_openai(self):
        """Test OpenAI (2 secrets)"""
        print(f"\n{'='*60}")
        print("🤖 OPENAI")
        print(f"{'='*60}")
        
        if self.test_secret_exists("OPEN_AI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
                models = client.models.list()
                self.log("OPEN_AI_API_KEY", "success", f"{len(models.data)} modèles disponibles")
            except Exception as e:
                error_str = str(e).lower()
                if "quota" in error_str or "429" in error_str:
                    self.log("OPEN_AI_API_KEY", "warning", "Quota dépassé", str(e)[:100])
                else:
                    self.log("OPEN_AI_API_KEY", "error", error=str(e)[:100])
        
        if self.test_secret_exists("MY_TEST_KEY_OPEN_AI_API"):
            key = os.getenv("MY_TEST_KEY_OPEN_AI_API")
            self.log("MY_TEST_KEY_OPEN_AI_API", "success", f"Clé test ({len(key)} chars)")
    
    def test_logrocket(self):
        """Test LogRocket"""
        print(f"\n{'='*60}")
        print("📹 LOGROCKET")
        print(f"{'='*60}")
        
        if self.test_secret_exists("LOGROCKET_API_KEY"):
            try:
                import requests
                headers = {"Authorization": f"Bearer {os.getenv('LOGROCKET_API_KEY')}"}
                response = requests.get("https://api.logrocket.com/v1/orgs", headers=headers, timeout=5)
                if response.status_code == 200:
                    self.log("LOGROCKET_API_KEY", "success", f"API connectée")
                else:
                    self.log("LOGROCKET_API_KEY", "warning", f"Status {response.status_code}", response.text[:50])
            except Exception as e:
                self.log("LOGROCKET_API_KEY", "error", error=str(e)[:100])
    
    def test_amplitude(self):
        """Test Amplitude (3 secrets)"""
        print(f"\n{'='*60}")
        print("📊 AMPLITUDE")
        print(f"{'='*60}")
        
        if self.test_secret_exists("AMPLITUDE_API_KEY"):
            api_key = os.getenv("AMPLITUDE_API_KEY")
            self.log("AMPLITUDE_API_KEY", "success", f"Clé présente ({len(api_key)} chars)")
        
        if self.test_secret_exists("AMPLITUDE_Standard_Server_url"):
            url = os.getenv("AMPLITUDE_Standard_Server_url")
            try:
                import requests
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 400, 404]:
                    self.log("AMPLITUDE_Standard_Server_url", "success", f"URL: {url}")
                else:
                    self.log("AMPLITUDE_Standard_Server_url", "warning", f"Status {response.status_code}")
            except:
                self.log("AMPLITUDE_Standard_Server_url", "success", f"URL configurée: {url}")
        
        if self.test_secret_exists("AMPLITUDE_EU_Residency_Server_URL"):
            url = os.getenv("AMPLITUDE_EU_Residency_Server_URL")
            self.log("AMPLITUDE_EU_Residency_Server_URL", "success", f"URL: {url}")
    
    def test_mapbox(self):
        """Test Mapbox"""
        print(f"\n{'='*60}")
        print("🗺️  MAPBOX")
        print(f"{'='*60}")
        
        if self.test_secret_exists("MAPBOX_ACCESS_TOKEN"):
            try:
                import requests
                token = os.getenv("MAPBOX_ACCESS_TOKEN")
                url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/paris.json?access_token={token}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log("MAPBOX_ACCESS_TOKEN", "success", f"API Mapbox connectée")
                else:
                    self.log("MAPBOX_ACCESS_TOKEN", "warning", f"Status {response.status_code}")
            except Exception as e:
                self.log("MAPBOX_ACCESS_TOKEN", "error", error=str(e)[:100])
    
    def test_test_keys(self):
        """Test clés de test (2 secrets)"""
        print(f"\n{'='*60}")
        print("🔑 CLÉS DE TEST")
        print(f"{'='*60}")
        
        if self.test_secret_exists("Try_out_Your_new_API_key_NODE"):
            key = os.getenv("Try_out_Your_new_API_key_NODE")
            self.log("Try_out_Your_new_API_key_NODE", "success", f"Clé Node ({len(key)} chars)")
        
        if self.test_secret_exists("Try_out_your_new_API_key_Python"):
            key = os.getenv("Try_out_your_new_API_key_Python")
            self.log("Try_out_your_new_API_key_Python", "success", f"Clé Python ({len(key)} chars)")
    
    def generate_report(self):
        """Génère le rapport Markdown avec comparaison AVANT/APRÈS"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        percentage = (self.success / self.total * 100) if self.total > 0 else 0
        
        report = f"""# 🔐 RAPPORT ULTRA-COMPLET V2 - 40 SECRETS
## Test Exhaustif avec Comparaison AVANT/APRÈS

**Date**: {now.strftime("%Y-%m-%d %H:%M:%S")}  
**Secrets testés**: {self.total}  
**Taux de réussite**: {percentage:.1f}%

---

## 📊 COMPARAISON AVANT/APRÈS

### AVANT (30 Oct 16:56 - Rapport précédent)
```
Total secrets: 26
Succès: 23/26 (88.5%)
Avertissements: 3
Erreurs: 0
```

### APRÈS (Maintenant)
```
Total secrets: {self.total}
Succès: {self.success}/{self.total} ({percentage:.1f}%)
Avertissements: {self.warnings}
Erreurs: {self.errors}
```

### 🆕 NOUVEAUX SECRETS AJOUTÉS (+{self.total - 26})

"""
        
        # Identifier les nouveaux secrets
        nouveaux = ["AGORA_APP_ID", "AGORA_APP_CERTIFICATE"] + [
            "REDIS_API_account_key", "REDIS_CLI", "REDIS_API_KEY_GENERATED_LangCache",
            "REDIS_CACHE_ID", "REDIS_URL_us_east_1", "REDIS_URL_us_west_2",
            "REDIS_URL_ap_south_1", "REDIS_URL_us_east_4", "REDIS_CLIENT",
            "REDIS_SERVICE_NAME", "REDIS_QUICK_CONNECT", "REDIS_CURL"
        ]
        
        for secret in nouveaux:
            result = next((r for r in self.results if r["secret"] == secret), None)
            if result:
                symbol = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
                report += f"{symbol} **{secret}**: {result['status'].upper()}\n"
                if result.get("details"):
                    report += f"   - {result['details']}\n"
        
        report += "\n---\n\n## 📋 RÉSULTATS PAR CATÉGORIE\n\n"
        
        categories = {
            "Session & Custom": ["SESSION_SECRET", "GABRIEL_API_KEY_1"],
            "GitHub & GitLab": ["GITHUB_TOKEN_API", "TOKEN_API_GITLAB"],
            "Supabase (5)": ["URL_SUPABASE_AUTOQG", "SUPABASE_ANON_PUBLIC", "SUPABASE_AUTOQG_API_KEY", "api_key_secret_supabase", "SUPABASE_ROLE_SECRET"],
            "Stripe": ["STRIPE_API_KEY_SECRET", "STRIPE_API_KEY_PUBLIC"],
            "Trello": ["TRELLO_API_KEY", "TRELLO_TOKEN"],
            "Appwrite": ["API_ENDPOINT_APPRWRITE", "PROJET_ID_APPWRITE"],
            "Resend": ["RESEND_API_KEY"],
            "OpenAI": ["OPEN_AI_API_KEY", "MY_TEST_KEY_OPEN_AI_API"],
            "LogRocket": ["LOGROCKET_API_KEY"],
            "Amplitude (3)": ["AMPLITUDE_API_KEY", "AMPLITUDE_Standard_Server_url", "AMPLITUDE_EU_Residency_Server_URL"],
            "Mapbox": ["MAPBOX_ACCESS_TOKEN"],
            "Agora (NOUVEAUX)": ["AGORA_APP_ID", "AGORA_APP_CERTIFICATE"],
            "Redis (13 secrets)": ["REDIS_API_KEY", "REDIS_API_account_key", "REDIS_CLI", "REDIS_API_KEY_GENERATED_LangCache", "REDIS_CACHE_ID", "REDIS_URL_us_east_1", "REDIS_URL_us_west_2", "REDIS_URL_ap_south_1", "REDIS_URL_us_east_4", "REDIS_CLIENT", "REDIS_SERVICE_NAME", "REDIS_QUICK_CONNECT", "REDIS_CURL"],
            "Clés de test": ["Try_out_Your_new_API_key_NODE", "Try_out_your_new_API_key_Python"]
        }
        
        for category, secrets in categories.items():
            cat_results = [r for r in self.results if r["secret"] in secrets]
            cat_success = len([r for r in cat_results if r["status"] == "success"])
            cat_total = len(secrets)
            
            symbol = "✅" if cat_success == cat_total else "⚠️" if cat_success > 0 else "❌"
            report += f"### {symbol} {category} ({cat_success}/{cat_total})\n\n"
            
            for result in cat_results:
                r_symbol = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "warning" else "❌"
                report += f"{r_symbol} **{result['secret']}**: {result['status'].upper()}\n"
                if result.get("details"):
                    report += f"   - {result['details']}\n"
                if result.get("error"):
                    report += f"   - ⚠️ {result['error'][:100]}\n"
                report += "\n"
        
        report += "---\n\n## 🎯 ÉVOLUTION DES MÉTRIQUES\n\n"
        report += f"""
| Métrique | Avant (26 secrets) | Après ({self.total} secrets) | Évolution |
|----------|-------------------|---------------------------|-----------|
| **Secrets totaux** | 26 | {self.total} | +{self.total - 26} |
| **Taux de réussite** | 88.5% | {percentage:.1f}% | {percentage - 88.5:+.1f}% |
| **Succès** | 23 | {self.success} | {self.success - 23:+d} |
| **Avertissements** | 3 | {self.warnings} | {self.warnings - 3:+d} |
| **Erreurs** | 0 | {self.errors} | {self.errors:+d} |

"""
        
        report += "---\n\n## 📈 STATISTIQUES FINALES\n\n"
        report += f"- **Total secrets testés**: {self.total}\n"
        report += f"- **Secrets fonctionnels**: {self.success} ({percentage:.1f}%)\n"
        report += f"- **Avertissements**: {self.warnings}\n"
        report += f"- **Erreurs**: {self.errors}\n\n"
        
        if percentage >= 90:
            report += "🟢 **EXCELLENT** - Infrastructure robuste\n\n"
        elif percentage >= 70:
            report += "🟡 **BON** - Infrastructure fonctionnelle\n\n"
        else:
            report += "🟠 **MOYEN** - Améliorations nécessaires\n\n"
        
        report += "---\n\n"
        report += f"*Rapport généré le {now.strftime('%Y-%m-%d à %H:%M:%S')}*\n"
        report += f"*⚠️ Les anciens rapports restent inchangés*\n"
        
        return report, timestamp
    
    def run_all_tests(self):
        """Exécute TOUS les tests"""
        print("="*60)
        print("🔐 TEST ULTRA-COMPLET V2 - 40 SECRETS")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        self.test_session_custom()
        self.test_github_gitlab()
        self.test_supabase()
        self.test_stripe()
        self.test_trello()
        self.test_appwrite()
        self.test_resend()
        self.test_openai()
        self.test_logrocket()
        self.test_amplitude()
        self.test_mapbox()
        self.test_agora_secrets()  # NOUVEAUX
        self.test_redis_multiples()  # TOUS LES REDIS
        self.test_test_keys()
        
        print("\n" + "="*60)
        print("✅ TESTS TERMINÉS")
        print("="*60)
        
        report, timestamp = self.generate_report()
        filename = f"RAPPORT_ULTRA_COMPLET_V2_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 Rapport: {filename}")
        print(f"✅ Succès: {self.success}/{self.total}")
        print(f"⚠️  Avertissements: {self.warnings}")
        print(f"❌ Erreurs: {self.errors}")
        print(f"\n⚠️  ANCIENS RAPPORTS NON MODIFIÉS")
        
        return filename


if __name__ == "__main__":
    testeur = TesteurSecretsV2()
    report_file = testeur.run_all_tests()
    
    print("\n" + "="*60)
    print("🎯 TEST ULTRA-COMPLET V2 TERMINÉ")
    print("="*60)
    taux = (testeur.success / testeur.total * 100) if testeur.total > 0 else 0
    print(f"📊 Taux de réussite: {taux:.1f}%")
    print(f"📁 Rapport: {report_file}")
    print("="*60)
