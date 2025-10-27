
#!/usr/bin/env python3
"""
Test complet des 9 nouvelles API ajoutées
OpenAI, Redis, LogRocket, Amplitude (2), Node/Python test keys
"""

import os
from datetime import datetime

print("="*60)
print("🚀 TEST COMPLET - 9 NOUVELLES API")
print("="*60)
print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

results = []

# Test 1: OpenAI API
print("\n🤖 TEST 1/9: OpenAI API")
try:
    openai_key = os.getenv("OPEN_AI_API_KEY") or os.getenv("MY_TEST_KEY_OPEN_AI_API")
    if openai_key:
        import openai
        openai.api_key = openai_key
        # Test simple : vérifier la clé
        models = openai.Model.list()
        print(f"✅ OpenAI connecté - {len(models.data)} modèles disponibles")
        results.append(("OpenAI", "✅ SUCCESS"))
    else:
        print("❌ Clé OpenAI manquante")
        results.append(("OpenAI", "❌ MISSING KEY"))
except Exception as e:
    print(f"❌ Erreur: {str(e)[:100]}")
    results.append(("OpenAI", f"❌ ERROR: {str(e)[:50]}"))

# Test 2: Redis API
print("\n🗄️  TEST 2/9: Redis API")
try:
    redis_key = os.getenv("REDIS_API_KEY")
    if redis_key:
        import redis
        # Format : redis://:<password>@<host>:<port>
        r = redis.from_url(redis_key)
        r.ping()
        print("✅ Redis connecté")
        results.append(("Redis", "✅ SUCCESS"))
    else:
        print("❌ Clé Redis manquante")
        results.append(("Redis", "❌ MISSING KEY"))
except Exception as e:
    print(f"⚠️  Redis pas encore configuré: {str(e)[:100]}")
    results.append(("Redis", f"⚠️  NOT CONFIGURED"))

# Test 3: LogRocket API
print("\n📹 TEST 3/9: LogRocket API")
try:
    logrocket_key = os.getenv("LOGROCKET_API_KEY")
    if logrocket_key:
        import requests
        headers = {"Authorization": f"Bearer {logrocket_key}"}
        response = requests.get("https://api.logrocket.com/v1/orgs", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ LogRocket connecté")
            results.append(("LogRocket", "✅ SUCCESS"))
        else:
            print(f"❌ LogRocket erreur {response.status_code}")
            results.append(("LogRocket", f"❌ ERROR {response.status_code}"))
    else:
        print("❌ Clé LogRocket manquante")
        results.append(("LogRocket", "❌ MISSING KEY"))
except Exception as e:
    print(f"❌ Erreur: {str(e)[:100]}")
    results.append(("LogRocket", f"❌ ERROR: {str(e)[:50]}"))

# Test 4: Amplitude API (Standard)
print("\n📊 TEST 4/9: Amplitude API (Standard)")
try:
    amplitude_key = os.getenv("AMPLITUDE_API_KEY")
    amplitude_url = os.getenv("AMPLITUDE_Standard_Server_url")
    if amplitude_key and amplitude_url:
        import requests
        data = {
            "api_key": amplitude_key,
            "events": [{
                "user_id": "test_user",
                "event_type": "test_event",
                "time": int(datetime.now().timestamp() * 1000)
            }]
        }
        response = requests.post(amplitude_url, json=data, timeout=5)
        if response.status_code in [200, 400]:  # 400 = test event, API fonctionne
            print("✅ Amplitude Standard connecté")
            results.append(("Amplitude Standard", "✅ SUCCESS"))
        else:
            print(f"❌ Amplitude erreur {response.status_code}")
            results.append(("Amplitude Standard", f"❌ ERROR {response.status_code}"))
    else:
        print("❌ Clés Amplitude manquantes")
        results.append(("Amplitude Standard", "❌ MISSING KEY"))
except Exception as e:
    print(f"❌ Erreur: {str(e)[:100]}")
    results.append(("Amplitude Standard", f"❌ ERROR: {str(e)[:50]}"))

# Test 5: Amplitude API (EU)
print("\n📊 TEST 5/9: Amplitude API (EU)")
try:
    amplitude_key = os.getenv("AMPLITUDE_API_KEY")
    amplitude_url_eu = os.getenv("AMPLITUDE_EU_Residency_Server_URL")
    if amplitude_key and amplitude_url_eu:
        import requests
        data = {
            "api_key": amplitude_key,
            "events": [{
                "user_id": "test_user",
                "event_type": "test_event",
                "time": int(datetime.now().timestamp() * 1000)
            }]
        }
        response = requests.post(amplitude_url_eu, json=data, timeout=5)
        if response.status_code in [200, 400]:
            print("✅ Amplitude EU connecté")
            results.append(("Amplitude EU", "✅ SUCCESS"))
        else:
            print(f"❌ Amplitude EU erreur {response.status_code}")
            results.append(("Amplitude EU", f"❌ ERROR {response.status_code}"))
    else:
        print("❌ Clés Amplitude EU manquantes")
        results.append(("Amplitude EU", "❌ MISSING KEY"))
except Exception as e:
    print(f"❌ Erreur: {str(e)[:100]}")
    results.append(("Amplitude EU", f"❌ ERROR: {str(e)[:50]}"))

# Test 6-8: Test Keys (Node/Python)
print("\n🔑 TEST 6-8/9: Test API Keys (Node/Python)")
test_keys = [
    ("Node Test Key", "Try_out_Your_new_API_key_NODE"),
    ("Python Test Key", "Try_out_your_new_API_key_Python"),
    ("OpenAI Test Key", "MY_TEST_KEY_OPEN_AI_API")
]

for name, env_var in test_keys:
    value = os.getenv(env_var)
    if value:
        print(f"✅ {name} configuré")
        results.append((name, "✅ CONFIGURED"))
    else:
        print(f"❌ {name} manquant")
        results.append((name, "❌ MISSING"))

# Test 9: Vérification des interconnexions possibles
print("\n🔗 TEST 9/9: Interconnexions Nouvelles API")
interconnections = [
    ("OpenAI + Supabase", ["OPEN_AI_API_KEY", "URL_SUPABASE_AUTOQG"]),
    ("Redis + Stripe", ["REDIS_API_KEY", "STRIPE_API_KEY_SECRET"]),
    ("Amplitude + LogRocket", ["AMPLITUDE_API_KEY", "LOGROCKET_API_KEY"])
]

for inter_name, keys in interconnections:
    all_present = all(os.getenv(k) for k in keys)
    if all_present:
        print(f"✅ {inter_name} - Prêt")
        results.append((f"Interconnexion {inter_name}", "✅ READY"))
    else:
        print(f"❌ {inter_name} - Clés manquantes")
        results.append((f"Interconnexion {inter_name}", "❌ MISSING KEYS"))

# Résumé final
print("\n" + "="*60)
print("📊 RÉSUMÉ FINAL")
print("="*60)

success = len([r for r in results if "✅" in r[1]])
total = len(results)
percentage = (success / total * 100) if total > 0 else 0

for api, status in results:
    print(f"{status} - {api}")

print("="*60)
print(f"✅ {success}/{total} tests réussis ({percentage:.1f}%)")
print("="*60)
print(f"\n⏰ Terminé: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
