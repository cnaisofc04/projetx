
#!/usr/bin/env python3
"""
DIAGNOSTIC COMPLET DES SECRETS DÉFAILLANTS
Analyse approfondie avec solutions exactes
"""

import os
import sys
from datetime import datetime
import traceback

class DiagnosticSecrets:
    """Diagnostic approfondi des secrets problématiques"""
    
    def __init__(self):
        self.results = []
        
    def log(self, secret: str, status: str, probleme: str = "", solution: str = ""):
        """Log un diagnostic"""
        symbol = "🔴" if status == "error" else "🟡" if status == "warning" else "🟢"
        print(f"\n{symbol} {secret}")
        if probleme:
            print(f"   ❌ PROBLÈME: {probleme}")
        if solution:
            print(f"   ✅ SOLUTION: {solution}")
        
        self.results.append({
            "secret": secret,
            "status": status,
            "probleme": probleme,
            "solution": solution
        })
    
    def diagnostic_redis_urls(self):
        """Diagnostic des URLs Redis"""
        print("\n" + "="*80)
        print("🔴 DIAGNOSTIC: REDIS URLs (5 secrets)")
        print("="*80)
        
        redis_urls = [
            "REDIS_API_KEY",
            "REDIS_URL_us_east_1",
            "REDIS_URL_us_west_2",
            "REDIS_URL_ap_south_1",
            "REDIS_URL_us_east_4"
        ]
        
        for secret_name in redis_urls:
            value = os.getenv(secret_name)
            if not value:
                self.log(secret_name, "error", 
                        "Secret non configuré", 
                        "Ajouter le secret dans Replit Secrets")
                continue
            
            # Analyser le format
            probleme = ""
            solution = ""
            
            if not value.startswith(('redis://', 'rediss://')):
                probleme = f"Format invalide. Valeur actuelle commence par: {value[:20]}..."
                solution = f"""
1. Obtenir l'URL correcte depuis votre fournisseur Redis
2. Le format doit être: redis://:<password>@<host>:<port>
3. Exemple: redis://:abc123@redis-12345.c1.us-east-1.ec2.cloud.redislabs.com:12345
4. Aller dans Replit Secrets → Éditer {secret_name}
5. Remplacer par l'URL complète au bon format
"""
            elif '://:' not in value and '@' not in value:
                probleme = "Mot de passe manquant dans l'URL"
                solution = f"""
L'URL doit inclure le mot de passe:
Format correct: redis://:<PASSWORD>@<HOST>:<PORT>
Actuel: {value[:30]}...
"""
            else:
                # Tester la connexion
                try:
                    import redis
                    r = redis.from_url(value)
                    r.ping()
                    self.log(secret_name, "success", "", "Secret fonctionnel ✅")
                    continue
                except redis.exceptions.ConnectionError as e:
                    probleme = f"Connexion impossible: {str(e)[:100]}"
                    solution = """
Vérifier:
1. Que l'instance Redis est active (vérifier sur le dashboard du fournisseur)
2. Que l'IP de Replit est autorisée (whitelist)
3. Que le mot de passe est correct
4. Que le port est accessible
"""
                except Exception as e:
                    probleme = f"Erreur: {str(e)[:100]}"
                    solution = "Vérifier le format complet de l'URL Redis"
            
            self.log(secret_name, "error", probleme, solution)
    
    def diagnostic_redis_curl(self):
        """Diagnostic REDIS_CURL"""
        print("\n" + "="*80)
        print("🔴 DIAGNOSTIC: REDIS_CURL")
        print("="*80)
        
        value = os.getenv("REDIS_CURL")
        if not value:
            self.log("REDIS_CURL", "error",
                    "Secret non configuré",
                    "Ajouter REDIS_CURL dans Replit Secrets")
            return
        
        probleme = f"C'est une commande cURL, pas une URL Redis. Valeur: {value[:50]}..."
        solution = """
REDIS_CURL contient une commande curl, pas une URL de connexion.

OPTIONS:
1. Si vous voulez tester Redis avec curl:
   - Utiliser ce secret pour des tests manuels uniquement
   - Ne pas l'utiliser pour la connexion applicative

2. Pour la connexion applicative:
   - Utiliser REDIS_API_KEY ou les REDIS_URL_* à la place
   - Extraire l'URL de la commande curl si nécessaire
   - Format attendu: redis://:<password>@<host>:<port>
"""
        self.log("REDIS_CURL", "warning", probleme, solution)
    
    def diagnostic_logrocket(self):
        """Diagnostic LogRocket"""
        print("\n" + "="*80)
        print("🔴 DIAGNOSTIC: LOGROCKET (8 secrets)")
        print("="*80)
        
        api_key = os.getenv("LOG_ROCKET_API_KEY")
        
        if not api_key:
            self.log("LOG_ROCKET_API_KEY", "error",
                    "Clé API LogRocket manquante",
                    """
1. Aller sur https://app.logrocket.com
2. Settings → API tokens
3. Créer un nouveau token
4. Copier et ajouter dans Replit Secrets comme LOG_ROCKET_API_KEY
""")
            return
        
        # Tester l'API
        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.logrocket.com/v1/orgs", headers=headers, timeout=10)
            
            if response.status_code == 403:
                probleme = 'Erreur 403: {"detail":"token signature is invalid"}'
                solution = """
Le token est INVALIDE ou EXPIRÉ.

SOLUTION EXACTE:
1. Aller sur https://app.logrocket.com/settings/api-tokens
2. Révoquer le token actuel
3. Créer un NOUVEAU token:
   - Cliquer "Create new token"
   - Donner un nom (ex: "Replit Integration")
   - Copier le token généré
4. Dans Replit Secrets:
   - Éditer LOG_ROCKET_API_KEY
   - Coller le NOUVEAU token
   - Sauvegarder
5. Redémarrer le Repl

IMPORTANT: Le token doit être copié immédiatement après création,
il ne sera plus visible après.
"""
                self.log("LOG_ROCKET_API_KEY", "error", probleme, solution)
            elif response.status_code == 200:
                self.log("LOG_ROCKET_API_KEY", "success", "", "Token LogRocket valide ✅")
            else:
                self.log("LOG_ROCKET_API_KEY", "warning",
                        f"Status inattendu: {response.status_code}",
                        "Vérifier le token sur https://app.logrocket.com")
        except Exception as e:
            self.log("LOG_ROCKET_API_KEY", "error",
                    f"Erreur de connexion: {str(e)[:100]}",
                    "Vérifier la connexion réseau et le token")
        
        # Les autres secrets LogRocket
        logrocket_configs = [
            "LOG_ROCKET_Manually_sanitize_text_and_inputs",
            "LOG_ROCKET_Automatically_sanitize_all_text_and_inputs",
            "LOG_ROCKET_Automatically_sanitize_all_text_and_inputs_2",
            "LOG_ROCKET_Automatically_sanitize_network_requests",
            "LOG_ROCKET_Automatically_sanitize_network_responses",
            "LOG_ROCKET_Automatically_sanitize_browser_URLs",
            "LOG_ROCKET_Project_Name",
            "LOG_ROCKET_App_ID"
        ]
        
        for secret in logrocket_configs:
            value = os.getenv(secret)
            if value:
                print(f"   ✅ {secret}: Configuré")
            else:
                print(f"   ⚠️  {secret}: Non configuré (optionnel)")
    
    def diagnostic_amplitude_url(self):
        """Diagnostic Amplitude Standard URL"""
        print("\n" + "="*80)
        print("🔴 DIAGNOSTIC: AMPLITUDE_Standard_Server_url")
        print("="*80)
        
        value = os.getenv("AMPLITUDE_Standard_Server_url")
        
        if not value:
            self.log("AMPLITUDE_Standard_Server_url", "error",
                    "URL non configurée",
                    "Ajouter AMPLITUDE_Standard_Server_url dans Replit Secrets")
            return
        
        print(f"   📍 URL actuelle: {value}")
        
        try:
            import requests
            response = requests.get(value, timeout=10)
            
            if response.status_code == 404:
                probleme = "Erreur 404 - Endpoint non trouvé"
                solution = """
L'URL correcte pour Amplitude est:
https://api2.amplitude.com/2/httpapi

PAS: https://api.lab.amplitude.com/v1/

SOLUTION EXACTE:
1. Aller dans Replit Secrets
2. Éditer AMPLITUDE_Standard_Server_url
3. Remplacer par: https://api2.amplitude.com/2/httpapi
4. Sauvegarder

Pour envoyer des events:
POST https://api2.amplitude.com/2/httpapi
Headers: Content-Type: application/json
Body: {
  "api_key": "VOTRE_AMPLITUDE_API_KEY",
  "events": [{
    "user_id": "user_id",
    "event_type": "event_name"
  }]
}
"""
                self.log("AMPLITUDE_Standard_Server_url", "error", probleme, solution)
            else:
                self.log("AMPLITUDE_Standard_Server_url", "success", "", f"URL accessible (status {response.status_code})")
        except Exception as e:
            self.log("AMPLITUDE_Standard_Server_url", "warning",
                    f"Impossible de tester: {str(e)[:100]}",
                    "Vérifier l'URL manuellement")
    
    def generer_rapport(self):
        """Génère le rapport de diagnostic"""
        now = datetime.now()
        
        report = f"""# 🔧 DIAGNOSTIC COMPLET DES SECRETS DÉFAILLANTS
**Date**: {now.strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 RÉSUMÉ

"""
        
        errors = [r for r in self.results if r["status"] == "error"]
        warnings = [r for r in self.results if r["status"] == "warning"]
        success = [r for r in self.results if r["status"] == "success"]
        
        report += f"""
- 🔴 **Erreurs critiques**: {len(errors)}
- 🟡 **Avertissements**: {len(warnings)}
- 🟢 **Secrets OK**: {len(success)}

---

## 🔴 PROBLÈMES ET SOLUTIONS

"""
        
        for result in self.results:
            if result["status"] in ["error", "warning"]:
                symbol = "🔴" if result["status"] == "error" else "🟡"
                report += f"""
### {symbol} {result['secret']}

**Problème**:
```
{result['probleme']}
```

**Solution**:
```
{result['solution']}
```

---
"""
        
        return report
    
    def run(self):
        """Exécute le diagnostic complet"""
        print("="*80)
        print("🔧 DIAGNOSTIC COMPLET DES SECRETS DÉFAILLANTS")
        print("="*80)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        self.diagnostic_redis_urls()
        self.diagnostic_redis_curl()
        self.diagnostic_logrocket()
        self.diagnostic_amplitude_url()
        
        print("\n" + "="*80)
        print("📄 GÉNÉRATION DU RAPPORT")
        print("="*80)
        
        report = self.generer_rapport()
        filename = f"DIAGNOSTIC_SECRETS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ Rapport généré: {filename}")
        
        errors = len([r for r in self.results if r["status"] == "error"])
        warnings = len([r for r in self.results if r["status"] == "warning"])
        
        print(f"\n🔴 Erreurs: {errors}")
        print(f"🟡 Avertissements: {warnings}")
        print("\n" + "="*80)
        
        return filename


if __name__ == "__main__":
    diagnostic = DiagnosticSecrets()
    diagnostic.run()
