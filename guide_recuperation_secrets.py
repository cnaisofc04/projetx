
#!/usr/bin/env python3
"""
GUIDE INTERACTIF - Récupération des secrets manquants
Ce script vous guide pour récupérer les bonnes valeurs
"""

import os

print("="*80)
print("🔐 GUIDE DE RÉCUPÉRATION DES SECRETS")
print("="*80)
print()

# Vérifier les secrets Redis
print("1️⃣  REDIS URLs (5 secrets)")
print("-" * 80)
redis_secrets = [
    "REDIS_API_KEY",
    "REDIS_URL_us_east_1", 
    "REDIS_URL_us_west_2",
    "REDIS_URL_ap_south_1",
    "REDIS_URL_us_east_4"
]

for secret in redis_secrets:
    value = os.getenv(secret)
    if not value or not value.startswith('redis://'):
        print(f"❌ {secret} - À CORRIGER")
        print(f"   📍 Allez sur votre dashboard Redis")
        print(f"   📋 Copiez l'URL de connexion (format: redis://:password@host:port)")
        print(f"   ✏️  Collez dans Replit Secrets → {secret}")
        print()

# Vérifier LogRocket
print("\n2️⃣  LOGROCKET")
print("-" * 80)
lr_key = os.getenv("LOG_ROCKET_API_KEY")
if not lr_key or len(lr_key) < 20:
    print("❌ LOG_ROCKET_API_KEY - À RÉGÉNÉRER")
    print("   📍 https://app.logrocket.com/settings/api-tokens")
    print("   🔄 Cliquez 'Create new token'")
    print("   📋 Copiez le token immédiatement")
    print("   ✏️  Collez dans Replit Secrets → LOG_ROCKET_API_KEY")
    print()

# Vérifier Amplitude
print("\n3️⃣  AMPLITUDE")
print("-" * 80)
amp_url = os.getenv("AMPLITUDE_Standard_Server_url")
correct_url = "https://api2.amplitude.com/2/httpapi"
if amp_url != correct_url:
    print("❌ AMPLITUDE_Standard_Server_url - À CORRIGER")
    print(f"   ❌ Valeur actuelle : {amp_url}")
    print(f"   ✅ Valeur correcte : {correct_url}")
    print(f"   ✏️  Copiez cette URL exacte dans Replit Secrets")
    print()

print("="*80)
print("✅ Une fois corrigé, relancez ce script pour vérifier")
print("="*80)
