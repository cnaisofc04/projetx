import os
import json
import requests
from datetime import datetime

# Timeout global pour les requêtes HTTP
HTTP_TIMEOUT = 10

# === Définition des tests pour chaque secret ===
API_TESTS = {
    "OPEN_AI_API_KEY": {
        "url": "https://api.openai.com/v1/models",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    "MY_TEST_KEY_OPEN_AI_API": {
        "url": "https://api.openai.com/v1/models",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    "STRIPE_API_KEY_SECRET": {
        "url": "https://api.stripe.com/v1/balance",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    "MAPBOX_ACCESS_TOKEN": {
        "url": "https://api.mapbox.com/geocoding/v5/mapbox.places/Paris.json",
        "method": "GET",
        "params": lambda k: {"access_token": k, "limit": 1}
    },
    # Clés Supabase (non testables par requête HTTP générique)
    "SUPABASE_ANON_PUBLIC": {"url": None},
    "SUPABASE_ROLE_SECRET": {"url": None},
    "SUPABASE_AUTOQG_API_KEY": {"url": None},
    "URL_SUPABASE_AUTOQG": {"url": None},
    "api_key_secret_supabase": {"url": None},
    # Redis / LangCache
    "REDIS_API_KEY_GENERATED_LangCache": {
        "url": "https://aws-us-east-1.langcache.redis.io/v1/caches",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    # Amplitude
    "AMPLITUDE_API_KEY": {
        "url": "https://api2.amplitude.com/2/httpapi",
        "method": "POST",
        "json": lambda k: {"api_key": k, "events": [{"event_type": "test_event"}]}
    },
    # Trello
    "TRELLO_API_KEY": {
        "url": "https://api.trello.com/1/members/me",
        "method": "GET",
        "params": lambda k: {"key": k, "token": os.getenv("TRELLO_TOKEN", "")}
    },
    "TRELLO_TOKEN": {
        "url": "https://api.trello.com/1/members/me",
        "method": "GET",
        "params": lambda k: {"key": os.getenv("TRELLO_API_KEY", ""), "token": k}
    },
    # GitHub
    "GITHUB_TOKEN_API": {
        "url": "https://api.github.com/user",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}", "Accept": "application/vnd.github+json"}
    },
    # GitLab
    "TOKEN_API_GITLAB": {
        "url": "https://gitlab.com/api/v4/user",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    # Airtable
    "AIRTABLE_API_KEY": {
        "url": "https://api.airtable.com/v0/meta/whoami",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    # Resend
    "RESEND_API_KEY": {
        "url": "https://api.resend.com/emails",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    # PostHog
    "POSTHOG_API_KEY": {
        "url": "https://app.posthog.com/api/event",
        "method": "POST",
        "json": lambda k: {"api_key": k, "event": "test_event"}
    },
    # LogRocket
    "LOG_ROCKET_API_KEY": {
        "url": "https://api.logrocket.io/v1/projects",
        "method": "GET",
        "headers": lambda k: {"Authorization": f"Bearer {k}"}
    },
    # Clés non testables (liste simplifiée)
    "AGORA_APP_ID": {"url": None},
    "SESSION_SECRET": {"url": None},
    "EXPO_API_KEY": {"url": None},
}

# Helper pour exécuter les lambdas de headers / params / json
def safe_call_builder(builder, key):
    if builder is None:
        return None
    try:
        return builder(key)
    except Exception:
        return None

# Fonction principale pour tester une clé
def run_test_for(secret_name, config):
    key = os.environ.get(secret_name)
    if not key:
        return {"status": "missing", "message": "Clé manquante dans les secrets Replit"}

    url = config.get("url")
    if not url:
        return {"status": "no_test_defined", "message": "Pas de test automatique défini (clé détectée)"}

    method = config.get("method", "GET").upper()
    headers = safe_call_builder(config.get("headers"), key) or {}
    params = safe_call_builder(config.get("params"), key) or {}
    json_payload = safe_call_builder(config.get("json"), key)
    data_payload = safe_call_builder(config.get("data"), key)

    headers.setdefault("User-Agent", "replit-secret-tester/1.0")

    try:
        resp = requests.request(
            method,
            url,
            headers=headers,
            params=params if params else None,
            json=json_payload if json_payload is not None else None,
            data=data_payload if data_payload is not None else None,
            timeout=HTTP_TIMEOUT
        )
        text_snippet = (resp.text or "")[:300].replace("\n", " ")
        return {
            "status": "ok" if resp.status_code < 300 else "error",
            "http_status": resp.status_code,
            "message": "Succès" if resp.status_code < 300 else "Échec HTTP",
            "snippet": text_snippet
        }
    except requests.exceptions.RequestException as e:
        return {"status": "exception", "message": str(e)}
    except Exception as e:
        return {"status": "exception", "message": str(e)}

# Exécution des tests
report = {}
now = datetime.utcnow().isoformat() + "Z"
report_meta = {
    "generated_at": now,
    "http_timeout_seconds": HTTP_TIMEOUT,
    "secrets_tested_count": 0
}

for secret_name, config in API_TESTS.items():
    res = run_test_for(secret_name, config)
    report[secret_name] = res
    report_meta["secrets_tested_count"] += 1

# Variables d'environnement non testées explicitement
env_keys = sorted([k for k in os.environ.keys() if k not in report])
extra_env = {k: {"present": True} for k in env_keys}
report["__extra_env_detected__"] = extra_env

# Sauvegarde du rapport
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"RAPPORT_TESTS_SECRETS_COMPLET_{timestamp}.json"
full_report = {"meta": report_meta, "results": report}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(full_report, f, indent=2, ensure_ascii=False)

# Affichage synthétique
print("\n🧾 Rapport des tests :\n")
for name, result in report.items():
    if name == "__extra_env_detected__":
        continue
    status = result.get("status", "unknown")
    if status == "ok":
        print(f"{name}: ✅ Succès ({result.get('http_status')})")
    elif status == "missing":
        print(f"{name}: ❌ Clé manquante")
    elif status == "no_test_defined":
        print(f"{name}: ⚠️ Pas de test automatique défini (clé détectée)")
    elif status == "error":
        sn = result.get("snippet", "")
        print(f"{name}: ⚠️ Échec ({result.get('http_status')}) : {sn[:120]}")
    elif status == "exception":
        print(f"{name}: ❌ Erreur technique: {result.get('message')}")
    else:
        print(f"{name}: ℹ️ {status}")

print(f"\n📁 Rapport complet enregistré dans : {filename}")
print("ℹ️ Ouvre le fichier JSON dans l'arborescence pour plus de détails.")
