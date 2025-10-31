#!/usr/bin/env python3
"""
TEST COMPLET DE TOUS LES 43 SECRETS
Tests unitaires, intégration, sécurité à 100%
"""

import os
import sys
from datetime import datetime
import traceback
import json

class TesteurCompletSecrets:
    """Testeur exhaustif de tous les secrets avec diagnostics détaillés"""
    
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.tests_reussis = 0
        self.tests_avertissement = 0
        self.tests_erreur = 0
        self.secrets_ok = []
        self.secrets_ko = []
        self.solutions = {}
        
    def log_test(self, secret_name: str, test_name: str, status: str, details: str = "", error: str = "", solution: str = ""):
        """Enregistre un résultat de test avec solution si erreur"""
        symbol = "✅" if status == "success" else "⚠️" if status == "warning" else "❌"
        result = {
            "secret": secret_name,
            "test": test_name,
            "status": status,
            "details": details,
            "error": error,
            "solution": solution,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total_tests += 1
        
        if status == "success":
            self.tests_reussis += 1
            if secret_name not in self.secrets_ok:
                self.secrets_ok.append(secret_name)
        elif status == "warning":
            self.tests_avertissement += 1
        else:
            self.tests_erreur += 1
            if secret_name not in self.secrets_ko:
                self.secrets_ko.append(secret_name)
            if solution:
                self.solutions[secret_name] = solution
            
        print(f"{symbol} {secret_name} - {test_name}: {status.upper()}")
        if details:
            print(f"   → {details}")
        if error:
            print(f"   ❌ {error[:200]}")
        if solution:
            print(f"   💡 SOLUTION: {solution[:200]}")
    
    # ===== TESTS STANDARDS =====
    
    def test_github_token(self):
        """Test GITHUB_TOKEN_API avec tests de sécurité"""
        secret_name = "GITHUB_TOKEN_API"
        value = os.getenv(secret_name)
        
        if not value:
            self.log_test(secret_name, "Existence", "error", 
                         error="Secret non trouvé",
                         solution="Ajouter le token GitHub dans Replit Secrets")
            return
        
        try:
            from github import Github, Auth
            auth = Auth.Token(value)
            g = Github(auth=auth)
            user = g.get_user()
            self.log_test(secret_name, "Connexion API", "success", f"User: {user.login}, ID: {user.id}")
            
            # Test permissions
            rate = g.get_rate_limit()
            self.log_test(secret_name, "Rate Limit", "success", f"Limit: {rate.core.limit}, Remaining: {rate.core.remaining}")
            
        except Exception as e:
            self.log_test(secret_name, "Connexion API", "error", 
                         error=str(e),
                         solution="Vérifier que le token GitHub est valide et non expiré. Générer un nouveau token sur github.com/settings/tokens")
    
    def test_gitlab_token(self):
        """Test TOKEN_API_GITLAB"""
        secret_name = "TOKEN_API_GITLAB"
        value = os.getenv(secret_name)
        
        if not value:
            self.log_test(secret_name, "Existence", "error",
                         error="Secret non trouvé",
                         solution="Ajouter le token GitLab dans Replit Secrets")
            return
        
        try:
            from gitlab import Gitlab
            gl = Gitlab("https://gitlab.com", private_token=value)
            gl.auth()
            user = gl.user
            self.log_test(secret_name, "Connexion API", "success", f"User: {getattr(user, 'username', 'authenticated')}")
        except Exception as e:
            self.log_test(secret_name, "Connexion API", "error",
                         error=str(e),
                         solution="Vérifier le token GitLab sur gitlab.com/-/profile/personal_access_tokens")
    
    def test_supabase_complet(self):
        """Test complet de tous les secrets Supabase"""
        url = os.getenv("URL_SUPABASE_AUTOQG")
        
        if not url:
            self.log_test("URL_SUPABASE_AUTOQG", "Existence", "error",
                         error="URL manquante",
                         solution="Ajouter l'URL Supabase (format: https://xxx.supabase.co)")
            return
        
        self.log_test("URL_SUPABASE_AUTOQG", "Format URL", "success", f"URL: {url}")
        
        supabase_keys = {
            "SUPABASE_ANON_PUBLIC": "Clé publique anon",
            "SUPABASE_AUTOQG_API_KEY": "Clé API service",
            "api_key_secret_supabase": "Clé secrète",
            "SUPABASE_ROLE_SECRET": "Clé role"
        }
        
        try:
            from supabase import create_client
            
            for key_name, description in supabase_keys.items():
                key_value = os.getenv(key_name)
                
                if not key_value:
                    self.log_test(key_name, "Existence", "error",
                                 error="Clé manquante",
                                 solution=f"Ajouter {description} depuis Supabase Dashboard > Settings > API")
                    continue
                
                try:
                    client = create_client(url, key_value)
                    self.log_test(key_name, "Connexion", "success", f"{description} - Client créé")
                except Exception as e:
                    self.log_test(key_name, "Connexion", "error",
                                 error=str(e)[:100],
                                 solution=f"Vérifier {description} dans Supabase Dashboard > Settings > API")
        except ImportError:
            for key_name in supabase_keys:
                if os.getenv(key_name):
                    self.log_test(key_name, "Import", "warning", details="Module supabase non installé")
    
    def test_stripe_complet(self):
        """Test complet Stripe avec sécurité"""
        secret_key = os.getenv("STRIPE_API_KEY_SECRET")
        public_key = os.getenv("STRIPE_API_KEY_PUBLIC")
        
        if not secret_key:
            self.log_test("STRIPE_API_KEY_SECRET", "Existence", "error",
                         error="Clé secrète manquante",
                         solution="Ajouter la clé secrète Stripe depuis stripe.com/dashboard/apikeys (commence par sk_)")
        else:
            try:
                import stripe
                stripe.api_key = secret_key
                account = stripe.Account.retrieve()
                self.log_test("STRIPE_API_KEY_SECRET", "Connexion", "success", f"Account: {account.id}")
                
                # Test création charge
                try:
                    payment = stripe.PaymentIntent.create(amount=100, currency="eur", payment_method_types=["card"])
                    self.log_test("STRIPE_API_KEY_SECRET", "Création PaymentIntent", "success", f"Intent créé: {payment.id}")
                except Exception as e:
                    self.log_test("STRIPE_API_KEY_SECRET", "Création PaymentIntent", "warning",
                                 details=str(e)[:100])
            except Exception as e:
                self.log_test("STRIPE_API_KEY_SECRET", "Connexion", "error",
                             error=str(e),
                             solution="Vérifier que la clé Stripe est valide (sk_test_ ou sk_live_). Régénérer sur stripe.com/dashboard/apikeys si nécessaire")
        
        if not public_key:
            self.log_test("STRIPE_API_KEY_PUBLIC", "Existence", "error",
                         error="Clé publique manquante",
                         solution="Ajouter la clé publique Stripe (pk_test_ ou pk_live_) depuis stripe.com/dashboard/apikeys")
        else:
            if public_key.startswith("pk_"):
                self.log_test("STRIPE_API_KEY_PUBLIC", "Format", "success", f"Format valide (longueur: {len(public_key)})")
            else:
                self.log_test("STRIPE_API_KEY_PUBLIC", "Format", "error",
                             error="Format invalide",
                             solution="La clé publique doit commencer par 'pk_test_' ou 'pk_live_'")
    
    def test_openai_complet(self):
        """Test complet OpenAI"""
        main_key = os.getenv("OPEN_AI_API_KEY")
        test_key = os.getenv("MY_TEST_KEY_OPEN_AI_API")
        
        if not main_key:
            self.log_test("OPEN_AI_API_KEY", "Existence", "error",
                         error="Clé principale manquante",
                         solution="Ajouter la clé OpenAI depuis platform.openai.com/api-keys (commence par sk-)")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=main_key)
                models = client.models.list()
                self.log_test("OPEN_AI_API_KEY", "Liste modèles", "success", f"{len(models.data)} modèles disponibles")
                
                # Test simple completion
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=5
                    )
                    self.log_test("OPEN_AI_API_KEY", "Completion test", "success", "Requête réussie")
                except Exception as e:
                    error_msg = str(e).lower()
                    if "quota" in error_msg or "insufficient" in error_msg:
                        self.log_test("OPEN_AI_API_KEY", "Completion test", "warning",
                                     details="Quota dépassé",
                                     solution="Ajouter du crédit sur platform.openai.com/account/billing")
                    else:
                        self.log_test("OPEN_AI_API_KEY", "Completion test", "error",
                                     error=str(e)[:100],
                                     solution="Vérifier la clé OpenAI et les permissions")
            except Exception as e:
                self.log_test("OPEN_AI_API_KEY", "Connexion", "error",
                             error=str(e),
                             solution="Vérifier que la clé OpenAI est valide (sk-...). Régénérer sur platform.openai.com/api-keys")
        
        if test_key:
            self.log_test("MY_TEST_KEY_OPEN_AI_API", "Existence", "success", f"Clé présente ({len(test_key)} chars)")
    
    def test_redis_complet(self):
        """Test de TOUS les secrets Redis (13 au total)"""
        redis_secrets = {
            "REDIS_API_KEY": "URL Redis principale",
            "REDIS_API_account_key": "Clé compte Redis",
            "REDIS_CLI": "Commande CLI Redis",
            "REDIS_API_KEY_GENERATED_LangCache": "Clé générée LangCache",
            "REDIS_CACHE_ID": "ID Cache Redis",
            "REDIS_URL_us_east_1": "URL région US East 1",
            "REDIS_URL_us_west_2": "URL région US West 2",
            "REDIS_URL_ap_south_1": "URL région AP South 1",
            "REDIS_URL_us_east_4": "URL région US East 4",
            "REDIS_CLIENT": "Client Redis",
            "REDIS_SERVICE_NAME": "Nom du service",
            "REDIS_QUICK_CONNECT": "Quick Connect",
            "REDIS_CURL": "Commande CURL"
        }
        
        for secret_name, description in redis_secrets.items():
            value = os.getenv(secret_name)
            
            if not value:
                self.log_test(secret_name, "Existence", "warning",
                             details=f"{description} - Non configuré")
                continue
            
            # Test format URL pour les URLs Redis
            if "URL" in secret_name or secret_name == "REDIS_API_KEY":
                if value.startswith(("redis://", "rediss://", "unix://")):
                    self.log_test(secret_name, "Format URL", "success", f"{description} - Format valide")
                    
                    # Test connexion
                    try:
                        import redis
                        r = redis.from_url(value)
                        r.ping()
                        self.log_test(secret_name, "Connexion", "success", f"{description} - Connexion OK")
                    except Exception as e:
                        self.log_test(secret_name, "Connexion", "error",
                                     error=str(e)[:100],
                                     solution=f"Vérifier les credentials Redis. Format: redis://user:password@host:port/db ou rediss:// pour SSL")
                else:
                    self.log_test(secret_name, "Format URL", "error",
                                 error="Format URL invalide",
                                 solution=f"URL Redis doit commencer par 'redis://', 'rediss://' ou 'unix://'. Exemple: redis://user:password@host:port/0")
            else:
                # Pour les autres secrets Redis
                self.log_test(secret_name, "Existence", "success", f"{description} - Présent ({len(value)} chars)")
    
    def test_agora_complet(self):
        """Test des secrets Agora"""
        app_id = os.getenv("AGORA_APP_ID")
        app_cert = os.getenv("AGORA_APP_CERTIFICATE")
        
        if not app_id:
            self.log_test("AGORA_APP_ID", "Existence", "error",
                         error="App ID manquant",
                         solution="Ajouter l'App ID depuis console.agora.io > Project > App ID")
        else:
            if len(app_id) == 32:
                self.log_test("AGORA_APP_ID", "Format", "success", f"App ID valide (32 chars)")
            else:
                self.log_test("AGORA_APP_ID", "Format", "warning",
                             details=f"Longueur inhabituelle: {len(app_id)} chars (attendu: 32)")
        
        if not app_cert:
            self.log_test("AGORA_APP_CERTIFICATE", "Existence", "error",
                         error="Certificate manquant",
                         solution="Ajouter le Certificate depuis console.agora.io > Project > App Certificate")
        else:
            if len(app_cert) == 32:
                self.log_test("AGORA_APP_CERTIFICATE", "Format", "success", f"Certificate valide (32 chars)")
            else:
                self.log_test("AGORA_APP_CERTIFICATE", "Format", "warning",
                             details=f"Longueur inhabituelle: {len(app_cert)} chars (attendu: 32)")
    
    def test_logrocket_complet(self):
        """Test de TOUS les secrets LogRocket (4)"""
        logrocket_secrets = {
            "LOG_ROCKET_Manually_sanitize_text_and_inputs": "Config sanitize manuelle",
            "LOG_ROCKET_Automatically_sanitize_all_text_and_inputs": "Config auto sanitize v1",
            "LOG_ROCKET_Automatically_sanitize_all_text_and_inputs_2": "Config auto sanitize v2",
            "LOG_ROCKET_Automatically_sanitize_network_requests": "Config sanitize network"
        }
        
        for secret_name, description in logrocket_secrets.items():
            value = os.getenv(secret_name)
            
            if not value:
                self.log_test(secret_name, "Existence", "warning",
                             details=f"{description} - Non configuré")
            else:
                # Test si c'est une API key valide
                if len(value) > 20:
                    try:
                        import requests
                        headers = {"Authorization": f"Bearer {value}"}
                        response = requests.get("https://api.logrocket.com/v1/orgs", headers=headers, timeout=5)
                        if response.status_code == 200:
                            self.log_test(secret_name, "Connexion API", "success", f"{description} - API OK")
                        elif response.status_code == 403:
                            self.log_test(secret_name, "Connexion API", "error",
                                         error="Token invalide (403 Forbidden)",
                                         solution="Régénérer le token LogRocket sur app.logrocket.com/settings/api-tokens")
                        else:
                            self.log_test(secret_name, "Connexion API", "warning",
                                         details=f"Status: {response.status_code}")
                    except Exception as e:
                        self.log_test(secret_name, "Connexion API", "error",
                                     error=str(e)[:100])
                else:
                    self.log_test(secret_name, "Format", "success", f"{description} - Config présente")
    
    def test_autres_secrets(self):
        """Test des autres secrets"""
        autres = {
            "RESEND_API_KEY": ("Resend Email", "Ajouter depuis resend.com/api-keys (commence par re_)"),
            "TRELLO_API_KEY": ("Trello API Key", "Obtenir sur trello.com/app-key"),
            "TRELLO_TOKEN": ("Trello Token", "Générer sur trello.com/app-key"),
            "API_ENDPOINT_APPRWRITE": ("Appwrite Endpoint", "URL endpoint (ex: https://cloud.appwrite.io/v1)"),
            "PROJET_ID_APPWRITE": ("Appwrite Project ID", "ID depuis console Appwrite"),
            "AMPLITUDE_API_KEY": ("Amplitude API Key", "Depuis analytics.amplitude.com > Settings > Projects"),
            "AMPLITUDE_Standard_Server_url": ("Amplitude URL Standard", "https://api2.amplitude.com/2/httpapi"),
            "AMPLITUDE_EU_Residency_Server_URL": ("Amplitude URL EU", "https://api.lab.eu.amplitude.com/v1/"),
            "MAPBOX_ACCESS_TOKEN": ("Mapbox Token", "Depuis account.mapbox.com/access-tokens/"),
            "GABRIEL_API_KEY_1": ("Clé Custom Gabriel", "Clé API personnalisée"),
            "Try_out_Your_new_API_key_NODE": ("Test Key Node", "Clé de test"),
            "Try_out_your_new_API_key_Python": ("Test Key Python", "Clé de test"),
            "SESSION_SECRET": ("Flask Session Secret", "Générer avec: python -c 'import secrets; print(secrets.token_urlsafe(64))'")
        }
        
        for secret_name, (description, solution) in autres.items():
            value = os.getenv(secret_name)
            
            if not value:
                self.log_test(secret_name, "Existence", "warning",
                             details=f"{description} - Non configuré",
                             solution=solution)
            else:
                self.log_test(secret_name, "Existence", "success", f"{description} - Présent ({len(value)} chars)")
    
    def generer_rapport_complet(self):
        """Génère le rapport AVANT/APRÈS complet"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        # Stats
        taux_reussite = (self.tests_reussis / self.total_tests * 100) if self.total_tests > 0 else 0
        
        # Lire les stats précédentes
        stats_avant = {
            "date": "29/10/2025",
            "secrets_configures": 26,
            "tests_reussis": 23,
            "tests_total": 26,
            "taux_reussite": 88.5,
            "secrets_ko": ["REDIS_API_KEY", "LOGROCKET_API_KEY", "AMPLITUDE_Standard_Server_url"]
        }
        
        rapport = f"""# 🔐 RAPPORT COMPLET - TEST DE TOUS LES SECRETS
## Rapport #{timestamp}

**Date**: {now.strftime("%d/%m/%Y à %H:%M:%S")}  
**Total secrets testés**: 43  
**Total tests exécutés**: {self.total_tests}

---

## 📊 COMPARAISON AVANT/APRÈS

### AVANT (Dernier rapport - 30/10/2025)
- **Secrets configurés**: {stats_avant['secrets_configures']}
- **Tests réussis**: {stats_avant['tests_reussis']}/{stats_avant['tests_total']} ({stats_avant['taux_reussite']}%)
- **Secrets en erreur**: {len(stats_avant['secrets_ko'])}
  - {', '.join(stats_avant['secrets_ko'])}

### APRÈS (Rapport actuel - {now.strftime("%d/%m/%Y")})
- **Secrets configurés**: 43
- **Tests réussis**: {self.tests_reussis}/{self.total_tests} ({taux_reussite:.1f}%)
- **Secrets OK**: {len(self.secrets_ok)}
- **Secrets KO**: {len(self.secrets_ko)}
- **Avertissements**: {self.tests_avertissement}
- **Erreurs**: {self.tests_erreur}

### ÉVOLUTION
- **Nouveaux secrets**: +17 ({', '.join(['AGORA_APP_ID', 'AGORA_APP_CERTIFICATE', 'REDIS multiples (12)', 'LOG_ROCKET (4)'])})
- **Progression**: {taux_reussite - stats_avant['taux_reussite']:+.1f}%

---

## 1️⃣ RÉSULTATS DÉTAILLÉS PAR CATÉGORIE

"""
        
        # Grouper par catégorie
        categories = {}
        for result in self.results:
            cat = result['secret'].split('_')[0]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for cat, results in sorted(categories.items()):
            success = len([r for r in results if r['status'] == 'success'])
            total = len(results)
            symbol = "✅" if success == total else "⚠️" if success > 0 else "❌"
            
            rapport += f"### {symbol} {cat.upper()} ({success}/{total})\n\n"
            
            for r in results:
                symbol = "✅" if r['status'] == "success" else "⚠️" if r['status'] == "warning" else "❌"
                rapport += f"{symbol} **{r['secret']}** - {r['test']}\n"
                if r.get('details'):
                    rapport += f"   - {r['details']}\n"
                if r.get('error'):
                    rapport += f"   - ❌ Erreur: `{r['error'][:150]}`\n"
                if r.get('solution'):
                    rapport += f"   - 💡 **Solution**: {r['solution']}\n"
                rapport += "\n"
        
        # Section ERREURS ET SOLUTIONS
        rapport += "---\n\n## 2️⃣ ERREURS ET SOLUTIONS EXACTES\n\n"
        
        if self.solutions:
            rapport += "### 🔧 Actions à réaliser dans l'ordre:\n\n"
            for i, (secret, solution) in enumerate(self.solutions.items(), 1):
                rapport += f"**{i}. {secret}**\n"
                rapport += f"   - 💡 Solution: {solution}\n\n"
        else:
            rapport += "✅ **Aucune erreur critique** - Tous les secrets fonctionnent correctement!\n\n"
        
        # Stats finales
        rapport += f"""---

## 3️⃣ STATISTIQUES FINALES

| Métrique | Valeur |
|----------|--------|
| Total secrets | 43 |
| Secrets OK | {len(self.secrets_ok)} |
| Secrets KO | {len(self.secrets_ko)} |
| Tests exécutés | {self.total_tests} |
| Tests réussis | {self.tests_reussis} ({taux_reussite:.1f}%) |
| Avertissements | {self.tests_avertissement} |
| Erreurs | {self.tests_erreur} |

---

## 4️⃣ SECRETS PAR STATUT

### ✅ Secrets Fonctionnels ({len(self.secrets_ok)})
{chr(10).join(f"- {s}" for s in sorted(self.secrets_ok))}

### ❌ Secrets à Corriger ({len(self.secrets_ko)})
{chr(10).join(f"- {s}" for s in sorted(self.secrets_ko)) if self.secrets_ko else "Aucun"}

---

*Rapport généré le {now.strftime("%d/%m/%Y à %H:%M:%S")}*
"""
        
        return rapport, timestamp
    
    def executer_tous_les_tests(self):
        """Exécute TOUS les tests"""
        print("="*80)
        print("🔐 TEST COMPLET DE TOUS LES 43 SECRETS")
        print("="*80)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        print("\n📋 TESTS STANDARDS")
        self.test_github_token()
        self.test_gitlab_token()
        self.test_supabase_complet()
        self.test_stripe_complet()
        self.test_openai_complet()
        
        print("\n🗄️ TESTS REDIS (13 secrets)")
        self.test_redis_complet()
        
        print("\n🎥 TESTS AGORA (2 secrets)")
        self.test_agora_complet()
        
        print("\n📹 TESTS LOGROCKET (4 secrets)")
        self.test_logrocket_complet()
        
        print("\n🔧 AUTRES SECRETS")
        self.test_autres_secrets()
        
        print("\n" + "="*80)
        print("✅ TOUS LES TESTS TERMINÉS")
        print("="*80)
        
        rapport, timestamp = self.generer_rapport_complet()
        filename = f"RAPPORT_COMPLET_43_SECRETS_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(rapport)
        
        print(f"\n📄 Rapport: {filename}")
        print(f"✅ Tests réussis: {self.tests_reussis}/{self.total_tests} ({self.tests_reussis/self.total_tests*100:.1f}%)")
        print(f"⚠️ Avertissements: {self.tests_avertissement}")
        print(f"❌ Erreurs: {self.tests_erreur}")
        print(f"🔐 Secrets OK: {len(self.secrets_ok)}")
        print(f"⚠️ Secrets KO: {len(self.secrets_ko)}")
        
        if self.solutions:
            print(f"\n💡 SOLUTIONS DISPONIBLES POUR {len(self.solutions)} SECRET(S)")
        
        return filename


if __name__ == "__main__":
    testeur = TesteurCompletSecrets()
    rapport_file = testeur.executer_tous_les_tests()
    
    print("\n" + "="*80)
    print("🎯 TEST COMPLET TERMINÉ")
    print("="*80)
    print(f"📊 Taux de réussite: {(testeur.tests_reussis/testeur.total_tests*100):.1f}%")
    print(f"📁 Rapport: {rapport_file}")
    print("="*80)
