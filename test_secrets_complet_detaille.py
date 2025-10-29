#!/usr/bin/env python3
"""
TEST COMPLET ET DÉTAILLÉ DE TOUS LES SECRETS
Avec tests unitaires approfondis pour chaque plateforme
"""

import os
import sys
from datetime import datetime
import traceback
import json

class TesteurSecretsComplet:
    """Testeur exhaustif avec tests unitaires pour tous les secrets"""
    
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.tests_reussis = 0
        self.tests_avertissement = 0
        self.tests_erreur = 0
        self.secrets_configures = 0
        self.secrets_manquants = 0
        
    def log_test(self, secret_name: str, test_name: str, status: str, details: str = "", error: str = ""):
        """Enregistre le résultat d'un test unitaire"""
        symbol = "✅" if status == "success" else "⚠️" if status == "warning" else "❌"
        result = {
            "secret": secret_name,
            "test": test_name,
            "status": status,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        self.total_tests += 1
        
        if status == "success":
            self.tests_reussis += 1
        elif status == "warning":
            self.tests_avertissement += 1
        else:
            self.tests_erreur += 1
            
        print(f"{symbol} {secret_name} - {test_name}: {status.upper()}")
        if details:
            print(f"   → {details}")
        if error:
            print(f"   ❌ {error[:150]}")
    
    def test_database_url_complet(self):
        """Tests unitaires complets pour DATABASE_URL"""
        secret_name = "DATABASE_URL"
        value = os.getenv(secret_name)
        
        print(f"\n{'='*60}")
        print(f"🗄️  TESTS UNITAIRES DATABASE_URL")
        print(f"{'='*60}")
        
        # Test 1: Existence
        if not value:
            self.log_test(secret_name, "1.1 Existence", "error", error="Secret DATABASE_URL non trouvé")
            self.secrets_manquants += 1
            return
        
        self.secrets_configures += 1
        self.log_test(secret_name, "1.1 Existence", "success", f"Secret trouvé")
        
        # Test 2: Format URL
        if value.startswith('postgresql://') or value.startswith('postgres://'):
            self.log_test(secret_name, "1.2 Format URL", "success", f"Format PostgreSQL valide")
        else:
            self.log_test(secret_name, "1.2 Format URL", "warning", f"Format inattendu: {value[:20]}...")
        
        # Test 3: Parsing URL
        try:
            from urllib.parse import urlparse
            parsed = urlparse(value)
            self.log_test(secret_name, "1.3 Parsing URL", "success", 
                         f"Host: {parsed.hostname}, Port: {parsed.port}, DB: {parsed.path[1:]}")
        except Exception as e:
            self.log_test(secret_name, "1.3 Parsing URL", "error", error=str(e))
        
        # Test 4: Connexion psycopg2
        try:
            import psycopg2
            conn = psycopg2.connect(value)
            conn.close()
            self.log_test(secret_name, "1.4 Connexion psycopg2", "success", "Connexion établie et fermée")
        except ImportError:
            self.log_test(secret_name, "1.4 Connexion psycopg2", "warning", 
                         details="psycopg2 non installé (normal pour ce test)")
        except Exception as e:
            self.log_test(secret_name, "1.4 Connexion psycopg2", "error", error=str(e))
        
        # Test 5: SQLAlchemy Engine
        try:
            from sqlalchemy import create_engine
            engine = create_engine(value)
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                self.log_test(secret_name, "1.5 SQLAlchemy Engine", "success", 
                             "Engine créé et requête SELECT 1 réussie")
        except ImportError:
            self.log_test(secret_name, "1.5 SQLAlchemy Engine", "warning", 
                         details="SQLAlchemy non installé")
        except Exception as e:
            self.log_test(secret_name, "1.5 SQLAlchemy Engine", "error", error=str(e))
        
        # Test 6: Version PostgreSQL
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(value)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                self.log_test(secret_name, "1.6 Version PostgreSQL", "success", 
                             f"Version: {version[:50]}...")
        except Exception as e:
            self.log_test(secret_name, "1.6 Version PostgreSQL", "warning", 
                         details="Impossible de récupérer la version", error=str(e)[:100])
        
        # Test 7: Permissions CRUD
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(value)
            with engine.connect() as conn:
                # CREATE TABLE
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS test_permissions (
                        id SERIAL PRIMARY KEY,
                        test_data VARCHAR(100)
                    )
                """))
                conn.commit()
                
                # INSERT
                conn.execute(text("INSERT INTO test_permissions (test_data) VALUES ('test')"))
                conn.commit()
                
                # SELECT
                result = conn.execute(text("SELECT COUNT(*) FROM test_permissions"))
                count = result.fetchone()[0]
                
                # UPDATE
                conn.execute(text("UPDATE test_permissions SET test_data = 'updated' WHERE test_data = 'test'"))
                conn.commit()
                
                # DELETE
                conn.execute(text("DELETE FROM test_permissions WHERE test_data = 'updated'"))
                conn.commit()
                
                # DROP
                conn.execute(text("DROP TABLE test_permissions"))
                conn.commit()
                
                self.log_test(secret_name, "1.7 Permissions CRUD", "success", 
                             "CREATE, INSERT, SELECT, UPDATE, DELETE, DROP: OK")
        except Exception as e:
            self.log_test(secret_name, "1.7 Permissions CRUD", "error", error=str(e))
        
        # Test 8: Pool de connexions
        try:
            from sqlalchemy import create_engine
            engine = create_engine(value, pool_size=5, max_overflow=10)
            self.log_test(secret_name, "1.8 Pool de connexions", "success", 
                         "Pool créé: size=5, overflow=10")
        except Exception as e:
            self.log_test(secret_name, "1.8 Pool de connexions", "error", error=str(e))
    
    def test_session_secret_complet(self):
        """Tests unitaires complets pour SESSION_SECRET"""
        secret_name = "SESSION_SECRET"
        value = os.getenv(secret_name)
        
        print(f"\n{'='*60}")
        print(f"🔐 TESTS UNITAIRES SESSION_SECRET")
        print(f"{'='*60}")
        
        # Test 1: Existence
        if not value:
            self.log_test(secret_name, "2.1 Existence", "error", error="Secret SESSION_SECRET non trouvé")
            self.secrets_manquants += 1
            return
        
        self.secrets_configures += 1
        self.log_test(secret_name, "2.1 Existence", "success", f"Secret trouvé")
        
        # Test 2: Longueur minimale (32 caractères recommandés)
        length = len(value)
        if length >= 64:
            self.log_test(secret_name, "2.2 Longueur", "success", 
                         f"Excellent: {length} caractères (≥64)")
        elif length >= 32:
            self.log_test(secret_name, "2.2 Longueur", "success", 
                         f"Bon: {length} caractères (≥32)")
        else:
            self.log_test(secret_name, "2.2 Longueur", "warning", 
                         f"Faible: {length} caractères (<32)", 
                         error="Recommandé: ≥32 caractères")
        
        # Test 3: Entropie (complexité)
        unique_chars = len(set(value))
        if unique_chars >= 20:
            self.log_test(secret_name, "2.3 Entropie", "success", 
                         f"Excellente: {unique_chars} caractères uniques")
        elif unique_chars >= 10:
            self.log_test(secret_name, "2.3 Entropie", "success", 
                         f"Bonne: {unique_chars} caractères uniques")
        else:
            self.log_test(secret_name, "2.3 Entropie", "warning", 
                         f"Faible: {unique_chars} caractères uniques")
        
        # Test 4: Types de caractères
        has_upper = any(c.isupper() for c in value)
        has_lower = any(c.islower() for c in value)
        has_digit = any(c.isdigit() for c in value)
        has_special = any(not c.isalnum() for c in value)
        
        types = sum([has_upper, has_lower, has_digit, has_special])
        if types >= 3:
            self.log_test(secret_name, "2.4 Diversité", "success", 
                         f"{types}/4 types de caractères (maj, min, chiffres, spéciaux)")
        else:
            self.log_test(secret_name, "2.4 Diversité", "warning", 
                         f"Seulement {types}/4 types de caractères")
        
        # Test 5: Utilisation avec Flask
        try:
            from flask import Flask
            app = Flask(__name__)
            app.secret_key = value
            self.log_test(secret_name, "2.5 Flask Integration", "success", 
                         "Secret_key configurée dans Flask")
        except ImportError:
            self.log_test(secret_name, "2.5 Flask Integration", "warning", 
                         details="Flask non installé")
        except Exception as e:
            self.log_test(secret_name, "2.5 Flask Integration", "error", error=str(e))
        
        # Test 6: Génération de tokens
        try:
            from itsdangerous import URLSafeTimedSerializer
            serializer = URLSafeTimedSerializer(value)
            token = serializer.dumps({'user_id': 123})
            data = serializer.loads(token, max_age=300)
            self.log_test(secret_name, "2.6 Token Generation", "success", 
                         f"Token généré et vérifié: {data}")
        except ImportError:
            self.log_test(secret_name, "2.6 Token Generation", "warning", 
                         details="itsdangerous non installé")
        except Exception as e:
            self.log_test(secret_name, "2.6 Token Generation", "error", error=str(e))
        
        # Test 7: Signing
        try:
            import hashlib
            import hmac
            message = "test_message"
            signature = hmac.new(value.encode(), message.encode(), hashlib.sha256).hexdigest()
            self.log_test(secret_name, "2.7 HMAC Signing", "success", 
                         f"Signature HMAC-SHA256 générée: {signature[:16]}...")
        except Exception as e:
            self.log_test(secret_name, "2.7 HMAC Signing", "error", error=str(e))
    
    def test_secrets_non_configures(self):
        """Teste et documente les secrets non configurés mais recommandés"""
        
        print(f"\n{'='*60}")
        print(f"📋 ANALYSE DES SECRETS NON CONFIGURÉS")
        print(f"{'='*60}")
        
        secrets_recommandes = {
            "OPENAI_API_KEY": {
                "categorie": "Intelligence Artificielle",
                "description": "Clé API OpenAI pour GPT-4, embeddings, etc.",
                "importance": "Haute",
                "use_cases": ["Chatbots", "Génération de contenu", "Analyse de texte"]
            },
            "STRIPE_SECRET_KEY": {
                "categorie": "Paiements",
                "description": "Clé secrète Stripe pour traiter les paiements",
                "importance": "Haute",
                "use_cases": ["E-commerce", "Abonnements", "Paiements en ligne"]
            },
            "STRIPE_PUBLISHABLE_KEY": {
                "categorie": "Paiements",
                "description": "Clé publique Stripe pour le frontend",
                "importance": "Haute",
                "use_cases": ["Formulaires de paiement", "Stripe Elements"]
            },
            "RESEND_API_KEY": {
                "categorie": "Email",
                "description": "API Resend pour envoi d'emails transactionnels",
                "importance": "Moyenne",
                "use_cases": ["Emails de confirmation", "Notifications", "Marketing"]
            },
            "GITHUB_TOKEN": {
                "categorie": "Intégrations Dev",
                "description": "Token GitHub pour accès aux repositories",
                "importance": "Moyenne",
                "use_cases": ["CI/CD", "Gestion de code", "Webhooks"]
            },
            "GITLAB_TOKEN": {
                "categorie": "Intégrations Dev",
                "description": "Token GitLab pour accès aux repositories",
                "importance": "Moyenne",
                "use_cases": ["CI/CD", "Gestion de code", "Webhooks"]
            },
            "SUPABASE_URL": {
                "categorie": "Backend-as-a-Service",
                "description": "URL du projet Supabase",
                "importance": "Moyenne",
                "use_cases": ["Base de données", "Auth", "Storage", "Realtime"]
            },
            "SUPABASE_KEY": {
                "categorie": "Backend-as-a-Service",
                "description": "Clé API Supabase (anon ou service)",
                "importance": "Moyenne",
                "use_cases": ["Authentification", "CRUD", "RLS"]
            },
            "REDIS_URL": {
                "categorie": "Cache & Sessions",
                "description": "URL Redis pour cache et sessions",
                "importance": "Moyenne",
                "use_cases": ["Cache", "Sessions", "Rate limiting", "Queue"]
            },
            "APPWRITE_ENDPOINT": {
                "categorie": "Backend-as-a-Service",
                "description": "Endpoint Appwrite",
                "importance": "Faible",
                "use_cases": ["Auth", "Database", "Storage", "Functions"]
            },
            "APPWRITE_PROJECT_ID": {
                "categorie": "Backend-as-a-Service",
                "description": "ID du projet Appwrite",
                "importance": "Faible",
                "use_cases": ["Identification du projet"]
            },
            "MAPBOX_ACCESS_TOKEN": {
                "categorie": "Cartes & Géolocalisation",
                "description": "Token Mapbox pour cartes interactives",
                "importance": "Faible",
                "use_cases": ["Cartes", "Géocodage", "Navigation"]
            },
            "AMPLITUDE_API_KEY": {
                "categorie": "Analytics",
                "description": "Clé API Amplitude pour analytics",
                "importance": "Faible",
                "use_cases": ["Product analytics", "User tracking", "Metrics"]
            }
        }
        
        for secret_name, info in secrets_recommandes.items():
            value = os.getenv(secret_name)
            if not value:
                self.log_test(secret_name, "3. Non configuré", "warning", 
                             f"{info['categorie']} - {info['description']}")
                self.secrets_manquants += 1
            else:
                self.log_test(secret_name, "3. Configuré", "success", 
                             f"{info['categorie']} - Présent")
                self.secrets_configures += 1
    
    def generer_rapport_markdown(self):
        """Génère un rapport Markdown détaillé et numéroté"""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        # Calculs statistiques
        taux_reussite = (self.tests_reussis / self.total_tests * 100) if self.total_tests > 0 else 0
        
        rapport = f"""# 🔐 RAPPORT NUMÉROTÉ #{timestamp}
# TEST COMPLET ET DÉTAILLÉ DE TOUS LES SECRETS

**Date de génération**: {now.strftime("%d/%m/%Y à %H:%M:%S")}  
**Version du rapport**: {timestamp}  
**Environnement**: Replit Development

---

## 📊 RÉSUMÉ EXÉCUTIF

### Statistiques Globales

| Métrique | Valeur | Détails |
|----------|--------|---------|
| **Secrets configurés** | {self.secrets_configures} | Secrets actifs dans l'environnement |
| **Secrets manquants** | {self.secrets_manquants} | Secrets recommandés non configurés |
| **Total tests exécutés** | {self.total_tests} | Tests unitaires individuels |
| **Tests réussis** | {self.tests_reussis} | {taux_reussite:.1f}% de réussite |
| **Avertissements** | {self.tests_avertissement} | Tests avec avertissements |
| **Erreurs** | {self.tests_erreur} | Tests en échec |

### Évaluation Générale

"""
        
        if taux_reussite >= 90:
            rapport += "🟢 **EXCELLENT** - Infrastructure de secrets très robuste\n\n"
        elif taux_reussite >= 70:
            rapport += "🟡 **BON** - Infrastructure de secrets fonctionnelle avec améliorations possibles\n\n"
        elif taux_reussite >= 50:
            rapport += "🟠 **MOYEN** - Infrastructure de secrets nécessite des améliorations\n\n"
        else:
            rapport += "🔴 **ATTENTION** - Infrastructure de secrets requiert une révision urgente\n\n"
        
        rapport += "---\n\n"
        
        # Section 1: Secrets configurés
        rapport += "## 1️⃣ SECRETS CONFIGURÉS - TESTS DÉTAILLÉS\n\n"
        
        secrets_configures = {}
        for result in self.results:
            if result['status'] in ['success', 'error'] and not result['test'].startswith('3.'):
                if result['secret'] not in secrets_configures:
                    secrets_configures[result['secret']] = []
                secrets_configures[result['secret']].append(result)
        
        for i, (secret, tests) in enumerate(secrets_configures.items(), 1):
            rapport += f"### 1.{i} {secret}\n\n"
            rapport += "**Tests unitaires:**\n\n"
            
            for test in tests:
                symbol = "✅" if test['status'] == "success" else "⚠️" if test['status'] == "warning" else "❌"
                rapport += f"{symbol} **{test['test']}**: {test['status'].upper()}\n"
                if test.get('details'):
                    rapport += f"   - {test['details']}\n"
                if test.get('error'):
                    rapport += f"   - ⚠️ Erreur: `{test['error'][:100]}`\n"
                rapport += "\n"
        
        # Section 2: Recommandations
        rapport += "---\n\n## 2️⃣ RECOMMANDATIONS D'INTÉGRATIONS\n\n"
        
        recommendations = {
            "🤖 Intelligence Artificielle": [
                "OPENAI_API_KEY - GPT-4, embeddings, assistants",
                "ANTHROPIC_API_KEY - Claude pour conversations avancées"
            ],
            "💳 Paiements": [
                "STRIPE_SECRET_KEY - Traitement de paiements sécurisés",
                "STRIPE_PUBLISHABLE_KEY - Frontend Stripe Elements"
            ],
            "📧 Communication": [
                "RESEND_API_KEY - Emails transactionnels modernes",
                "TWILIO_API_KEY - SMS et notifications"
            ],
            "🗄️ Backend Services": [
                "SUPABASE_URL + SUPABASE_KEY - Auth, DB, Storage",
                "REDIS_URL - Cache, sessions, rate limiting"
            ],
            "🔧 Intégrations Dev": [
                "GITHUB_TOKEN - CI/CD, webhooks",
                "GITLAB_TOKEN - Alternative GitLab"
            ],
            "📊 Analytics & Monitoring": [
                "AMPLITUDE_API_KEY - Product analytics",
                "SENTRY_DSN - Error tracking"
            ]
        }
        
        for categorie, items in recommendations.items():
            rapport += f"### {categorie}\n\n"
            for item in items:
                rapport += f"- {item}\n"
            rapport += "\n"
        
        # Section 3: Tests détaillés par résultat
        rapport += "---\n\n## 3️⃣ DÉTAILS DES TESTS PAR CATÉGORIE\n\n"
        
        # Grouper par statut
        success_tests = [r for r in self.results if r['status'] == 'success']
        warning_tests = [r for r in self.results if r['status'] == 'warning']
        error_tests = [r for r in self.results if r['status'] == 'error']
        
        rapport += f"### 3.1 Tests Réussis ({len(success_tests)})\n\n"
        for test in success_tests[:10]:  # Limiter à 10 pour la lisibilité
            rapport += f"✅ **{test['secret']}** - {test['test']}: {test.get('details', 'OK')}\n"
        if len(success_tests) > 10:
            rapport += f"\n*... et {len(success_tests) - 10} autres tests réussis*\n"
        rapport += "\n"
        
        if warning_tests:
            rapport += f"### 3.2 Avertissements ({len(warning_tests)})\n\n"
            for test in warning_tests:
                rapport += f"⚠️ **{test['secret']}** - {test['test']}\n"
                if test.get('details'):
                    rapport += f"   - {test['details']}\n"
                if test.get('error'):
                    rapport += f"   - Détail: `{test['error'][:100]}`\n"
                rapport += "\n"
        
        if error_tests:
            rapport += f"### 3.3 Erreurs ({len(error_tests)})\n\n"
            for test in error_tests:
                rapport += f"❌ **{test['secret']}** - {test['test']}\n"
                if test.get('error'):
                    rapport += f"   - Erreur: `{test['error'][:100]}`\n"
                rapport += "\n"
        
        # Section 4: Secrets manquants détaillés
        rapport += "---\n\n## 4️⃣ SECRETS MANQUANTS - ANALYSE DÉTAILLÉE\n\n"
        
        missing_tests = [r for r in self.results if r['test'].startswith('3.')]
        
        categories_manquantes = {}
        for test in missing_tests:
            if test['status'] == 'warning':  # Non configuré
                details = test.get('details', '')
                if ' - ' in details:
                    cat = details.split(' - ')[0]
                    if cat not in categories_manquantes:
                        categories_manquantes[cat] = []
                    categories_manquantes[cat].append(test)
        
        for i, (cat, tests) in enumerate(categories_manquantes.items(), 1):
            rapport += f"### 4.{i} {cat}\n\n"
            for test in tests:
                rapport += f"⚠️ **{test['secret']}**: {test['details'].split(' - ', 1)[1]}\n"
            rapport += "\n"
        
        # Section 5: Plan d'action
        rapport += "---\n\n## 5️⃣ PLAN D'ACTION RECOMMANDÉ\n\n"
        
        rapport += """### Priorité HAUTE 🔴

1. **Configurer DATABASE_URL** (si non fait)
   - Utiliser Replit PostgreSQL intégré
   - Ou configurer une instance externe

2. **Vérifier SESSION_SECRET**
   - Minimum 32 caractères
   - Caractères aléatoires complexes

### Priorité MOYENNE 🟡

3. **Paiements Stripe**
   - STRIPE_SECRET_KEY
   - STRIPE_PUBLISHABLE_KEY

4. **Intelligence Artificielle**
   - OPENAI_API_KEY pour GPT-4

5. **Emails**
   - RESEND_API_KEY pour transactionnels

### Priorité BASSE 🟢

6. **Analytics**
   - AMPLITUDE_API_KEY

7. **Cartes**
   - MAPBOX_ACCESS_TOKEN

8. **Backend Alternatif**
   - SUPABASE_URL + SUPABASE_KEY
   - REDIS_URL

"""
        
        # Section 6: Code d'exemple
        rapport += "---\n\n## 6️⃣ EXEMPLES DE CODE D'INTÉGRATION\n\n"
        
        rapport += """### Flask avec DATABASE_URL et SESSION_SECRET

```python
import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)

@app.route('/')
def index():
    session['user_id'] = 123
    return "Session configurée!"
```

### Stripe Payment

```python
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# Créer un paiement
payment = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    payment_method_types=["card"]
)
```

### OpenAI Integration

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Resend Email

```python
import resend
import os

resend.api_key = os.environ.get("RESEND_API_KEY")

email = resend.Emails.send({
    "from": "onboarding@yourdomain.com",
    "to": "user@example.com",
    "subject": "Welcome!",
    "html": "<h1>Welcome!</h1>"
})
```

"""
        
        # Footer
        rapport += "---\n\n"
        rapport += f"## 📝 MÉTADONNÉES DU RAPPORT\n\n"
        rapport += f"- **Rapport numéro**: #{timestamp}\n"
        rapport += f"- **Généré le**: {now.strftime('%d/%m/%Y à %H:%M:%S')}\n"
        rapport += f"- **Tests exécutés**: {self.total_tests}\n"
        rapport += f"- **Taux de réussite**: {taux_reussite:.1f}%\n"
        rapport += f"- **Secrets actifs**: {self.secrets_configures}\n"
        rapport += f"- **Secrets manquants**: {self.secrets_manquants}\n\n"
        
        rapport += "---\n\n"
        rapport += "*Rapport généré automatiquement par le système de test de secrets Replit*\n"
        
        return rapport, timestamp
    
    def executer_tous_les_tests(self):
        """Execute tous les tests unitaires"""
        print("="*60)
        print("🔐 TEST COMPLET ET DÉTAILLÉ DE TOUS LES SECRETS")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Tests des secrets configurés
        self.test_database_url_complet()
        self.test_session_secret_complet()
        
        # Analyse des secrets manquants
        self.test_secrets_non_configures()
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS TERMINÉS")
        print("="*60)
        
        # Générer le rapport
        rapport, timestamp = self.generer_rapport_markdown()
        filename = f"RAPPORT_SECRETS_DETAILLE_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(rapport)
        
        print(f"\n📄 Rapport: {filename}")
        print(f"✅ Tests réussis: {self.tests_reussis}/{self.total_tests}")
        print(f"⚠️  Avertissements: {self.tests_avertissement}")
        print(f"❌ Erreurs: {self.tests_erreur}")
        print(f"🔐 Secrets configurés: {self.secrets_configures}")
        print(f"⚠️  Secrets manquants: {self.secrets_manquants}")
        
        return filename


if __name__ == "__main__":
    testeur = TesteurSecretsComplet()
    rapport_file = testeur.executer_tous_les_tests()
    
    print("\n" + "="*60)
    print("🎯 RÉSUMÉ FINAL")
    print("="*60)
    taux = (testeur.tests_reussis / testeur.total_tests * 100) if testeur.total_tests > 0 else 0
    print(f"📊 Taux de réussite: {taux:.1f}%")
    print(f"📁 Rapport sauvegardé: {rapport_file}")
    print("="*60)
