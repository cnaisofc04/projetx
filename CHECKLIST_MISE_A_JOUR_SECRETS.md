
# ✅ CHECKLIST - Mise à jour des Secrets

## 1️⃣ LOGROCKET ✅ PRÊT À COPIER

**Secret à éditer** : `LOG_ROCKET_API_KEY`

**Valeur à coller** :
```
cnoqnx/pjsketx/VMPFhezXu5ne2ExMl
```

**Actions** :
- [ ] Ouvrir Replit → Tools → Secrets
- [ ] Éditer `LOG_ROCKET_API_KEY`
- [ ] Coller la valeur ci-dessus
- [ ] Sauvegarder

---

## 2️⃣ AMPLITUDE ✅ PRÊT À COPIER

**Secret à éditer** : `AMPLITUDE_Standard_Server_url`

**Valeur à coller** :
```
https://api2.amplitude.com/2/httpapi
```

**Actions** :
- [ ] Ouvrir Replit → Tools → Secrets
- [ ] Éditer `AMPLITUDE_Standard_Server_url`
- [ ] Coller la valeur ci-dessus
- [ ] Sauvegarder

---

## 3️⃣ REDIS URLs ⚠️ NÉCESSITE RÉCUPÉRATION MANUELLE

**Secrets à éditer** :
- `REDIS_API_KEY`
- `REDIS_URL_us_east_1`
- `REDIS_URL_us_west_2`
- `REDIS_URL_ap_south_1`
- `REDIS_URL_us_east_4`

**Actions** :
- [ ] Aller sur https://app.redislabs.com/
- [ ] Se connecter avec vos identifiants
- [ ] Aller dans "Databases"
- [ ] Pour chaque base de données :
  - [ ] Cliquer sur la base
  - [ ] Chercher "Connect" ou "Configuration"
  - [ ] **COPIER** l'URL complète (format: `redis://default:PASSWORD@HOST:PORT`)
  - [ ] Coller dans le secret Replit correspondant

**Format attendu** :
```
redis://default:MOT_DE_PASSE@redis-12345.c123.REGION.ec2.cloud.redislabs.com:12345
```

**Voir le guide complet** : `INSTRUCTIONS_REDIS_URLS.md`

---

## 4️⃣ VÉRIFICATION FINALE

Une fois TOUS les secrets mis à jour :

**Commande à exécuter** :
```bash
python guide_recuperation_secrets.py
```

**Résultat attendu** :
```
✅ LOG_ROCKET_API_KEY - Format valide
✅ AMPLITUDE_Standard_Server_url - URL correcte
✅ REDIS_API_KEY - Connexion réussie
✅ REDIS_URL_us_east_1 - Connexion réussie
...
```

---

## 🎯 ORDRE RECOMMANDÉ

1. **Commencer par les plus simples** :
   - [x] AMPLITUDE (1 minute)
   - [x] LOGROCKET (1 minute)

2. **Finir avec Redis** (5-10 minutes) :
   - [ ] Récupérer les URLs depuis Redis Cloud Console
   - [ ] Mettre à jour les 5 secrets Redis

---

## 🆘 EN CAS DE PROBLÈME

Si après avoir tout mis à jour, certains tests échouent :

1. Lancer le diagnostic complet :
   ```bash
   python diagnostic_secrets_complet.py
   ```

2. Le rapport vous dira **EXACTEMENT** ce qui ne va pas

3. Me partager le rapport généré pour que je vous aide
