# 📋 GUIDE DE MIGRATION DES SECRETS GITHUB VERS REPLIT

**Date**: 29 octobre 2025  
**Version**: 1.0

---

## 🎯 OBJECTIF

Transférer tous vos secrets stockés sur **GitHub Secrets** vers **Replit Secrets** pour les rendre accessibles dans votre environnement de développement.

---

## ⚠️ IMPORTANT: GitHub Secrets ≠ Replit Secrets

### Différences clés:

| Aspect | GitHub Secrets | Replit Secrets |
|--------|---------------|----------------|
| **Utilisation** | GitHub Actions CI/CD | Application Replit |
| **Accès** | Workflows GitHub uniquement | Code application |
| **Synchronisation** | ❌ Aucune auto-sync | Manuel |
| **Variables d'environnement** | Dans GitHub Actions | Dans l'app Replit |

**🔴 Les secrets GitHub ne sont PAS automatiquement disponibles dans Replit!**

---

## 📊 ÉTAT ACTUEL

### Secrets configurés dans Replit: **2/26**

✅ **DATABASE_URL** - Base de données PostgreSQL  
✅ **SESSION_SECRET** - Clé de session Flask

### Secrets manquants: **13 prioritaires**

#### 🤖 Intelligence Artificielle
- ❌ OPENAI_API_KEY
- ❌ OPEN_AI_API_KEY

#### 💳 Paiements
- ❌ STRIPE_SECRET_KEY
- ❌ STRIPE_PUBLISHABLE_KEY
- ❌ STRIPE_API_KEY_SECRET
- ❌ STRIPE_API_KEY_PUBLIC

#### 📧 Communication
- ❌ RESEND_API_KEY

#### 🗄️ Backend Services
- ❌ SUPABASE_URL (URL_SUPABASE_AUTOQG)
- ❌ SUPABASE_KEY (SUPABASE_ANON_PUBLIC, SUPABASE_AUTOQG_API_KEY)
- ❌ REDIS_URL (REDIS_API_KEY)

#### 🔧 Intégrations Dev
- ❌ GITHUB_TOKEN (GITHUB_TOKEN_API)
- ❌ GITLAB_TOKEN (TOKEN_API_GITLAB)

#### 📊 Analytics & Autres
- ❌ AMPLITUDE_API_KEY
- ❌ MAPBOX_ACCESS_TOKEN
- ❌ APPWRITE_ENDPOINT (API_ENDPOINT_APPRWRITE)
- ❌ APPWRITE_PROJECT_ID (PROJET_ID_APPWRITE)
- ❌ TRELLO_API_KEY
- ❌ TRELLO_TOKEN
- ❌ LOGROCKET_API_KEY

---

## 🚀 MÉTHODE DE MIGRATION

### Méthode 1: Interface Replit (RECOMMANDÉE)

#### Étape 1: Accéder aux secrets GitHub

1. Allez sur votre repository GitHub
2. Cliquez sur **Settings** → **Secrets and variables** → **Actions**
3. Vous verrez la liste de tous vos secrets (26 au total)

#### Étape 2: Copier dans Replit

1. Dans Replit, ouvrez le panneau **Tools** (🔧 à gauche)
2. Cliquez sur **Secrets** 
3. Pour chaque secret GitHub:
   - Cliquez sur **+ Add new secret**
   - **Key**: Copiez exactement le nom du secret GitHub (ex: `OPENAI_API_KEY`)
   - **Value**: Copiez la valeur du secret depuis GitHub
   - Cliquez sur **Add secret**

#### Étape 3: Vérifier

Après avoir ajouté les secrets, exécutez:

```bash
python test_secrets_complet_detaille.py
```

---

### Méthode 2: Via Replit CLI (AVANCÉE)

```bash
# Installer Replit CLI (si nécessaire)
npm install -g replit-cli

# Se connecter
replit login

# Ajouter un secret
replit secrets set OPENAI_API_KEY "votre-clé-api-ici"

# Vérifier
replit secrets list
```

---

## 📝 LISTE COMPLÈTE DES SECRETS À MIGRER

### Format: `NOM_SECRET` - Description

1. **GITHUB_TOKEN_API** - Token GitHub pour API
2. **TOKEN_API_GITLAB** - Token GitLab pour API
3. **URL_SUPABASE_AUTOQG** - URL Supabase
4. **SUPABASE_ANON_PUBLIC** - Clé publique Supabase
5. **SUPABASE_AUTOQG_API_KEY** - Clé API Supabase
6. **api_key_secret_supabase** - Clé secrète Supabase
7. **SUPABASE_ROLE_SECRET** - Clé role Supabase
8. **STRIPE_API_KEY_SECRET** - Clé secrète Stripe
9. **STRIPE_API_KEY_PUBLIC** - Clé publique Stripe
10. **TRELLO_API_KEY** - Clé API Trello
11. **TRELLO_TOKEN** - Token Trello
12. **API_ENDPOINT_APPRWRITE** - Endpoint Appwrite
13. **PROJET_ID_APPWRITE** - ID projet Appwrite
14. **RESEND_API_KEY** - Clé API Resend
15. **OPEN_AI_API_KEY** - Clé OpenAI principale
16. **MY_TEST_KEY_OPEN_AI_API** - Clé OpenAI test
17. **REDIS_API_KEY** - URL Redis
18. **LOGROCKET_API_KEY** - Clé LogRocket
19. **AMPLITUDE_API_KEY** - Clé Amplitude
20. **AMPLITUDE_Standard_Server_url** - URL serveur Amplitude
21. **AMPLITUDE_EU_Residency_Server_URL** - URL serveur EU Amplitude
22. **MAPBOX_ACCESS_TOKEN** - Token Mapbox
23. **Try_out_Your_new_API_key_NODE** - Clé test Node
24. **Try_out_your_new_API_key_Python** - Clé test Python
25. **GABRIEL_API_KEY_1** - Clé custom Gabriel

---

## ✅ CHECKLIST DE MIGRATION

Cochez au fur et à mesure de la migration:

### Essentiels
- [ ] DATABASE_URL ✅ (déjà configuré)
- [ ] SESSION_SECRET ✅ (déjà configuré)
- [ ] OPENAI_API_KEY / OPEN_AI_API_KEY
- [ ] STRIPE_API_KEY_SECRET
- [ ] STRIPE_API_KEY_PUBLIC

### Importants
- [ ] RESEND_API_KEY
- [ ] GITHUB_TOKEN_API
- [ ] TOKEN_API_GITLAB
- [ ] URL_SUPABASE_AUTOQG
- [ ] SUPABASE_ANON_PUBLIC
- [ ] REDIS_API_KEY

### Optionnels
- [ ] TRELLO_API_KEY
- [ ] TRELLO_TOKEN
- [ ] API_ENDPOINT_APPRWRITE
- [ ] PROJET_ID_APPWRITE
- [ ] AMPLITUDE_API_KEY
- [ ] MAPBOX_ACCESS_TOKEN
- [ ] LOGROCKET_API_KEY

---

## 🧪 COMMANDES DE TEST

### Tester TOUS les secrets
```bash
python test_tous_secrets.py
```

### Tester avec détails complets
```bash
python test_secrets_complet_detaille.py
```

### Tester un secret spécifique
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Affiche None si non configuré
```

---

## 🔒 BONNES PRATIQUES DE SÉCURITÉ

### ✅ À FAIRE
1. ✅ Copier les secrets manuellement un par un
2. ✅ Vérifier chaque secret après ajout
3. ✅ Ne jamais commiter les secrets dans Git
4. ✅ Utiliser des noms de secrets cohérents
5. ✅ Documenter quels secrets sont nécessaires

### ❌ À ÉVITER
1. ❌ Hardcoder les secrets dans le code
2. ❌ Partager les secrets par email/chat
3. ❌ Commiter un fichier `.env` avec secrets
4. ❌ Utiliser les mêmes secrets en dev et prod
5. ❌ Stocker les secrets en clair dans des fichiers

---

## 📊 APRÈS LA MIGRATION

### 1. Vérifier que tout fonctionne

```bash
python test_secrets_complet_detaille.py
```

Vous devriez voir:
```
✅ Tests réussis: 25+/28
🔐 Secrets configurés: 25+
```

### 2. Générer le rapport final

Le rapport sera automatiquement créé:
```
RAPPORT_SECRETS_DETAILLE_YYYYMMDD_HHMMSS.md
```

### 3. Nettoyer

- Supprimer les anciens fichiers de test si nécessaire
- Mettre à jour la documentation du projet

---

## 🆘 PROBLÈMES COURANTS

### Secret non détecté après ajout

**Solution**: Redémarrez le workflow Replit
```bash
# Le secret sera disponible après redémarrage
```

### Erreur "Secret not found"

**Vérifiez**:
1. Le nom est exactement identique (sensible à la casse)
2. Le secret est ajouté dans le bon projet Replit
3. Vous avez redémarré l'environnement

### Secret avec mauvais format

**Exemples**:
- ❌ `REDIS_API_KEY = "redis123"` → ✅ Devrait être `redis://...`
- ❌ `DATABASE_URL = "localhost"` → ✅ Devrait être `postgresql://...`

---

## 📞 SUPPORT

Si vous rencontrez des problèmes:

1. **Vérifiez les logs**: `python test_secrets_complet_detaille.py`
2. **Consultez le rapport**: Derniers fichiers `RAPPORT_SECRETS_*.md`
3. **Relancez les tests**: Après chaque modification

---

## 🎯 PROCHAINES ÉTAPES

1. [ ] Migrer les secrets prioritaires (OPENAI, STRIPE, RESEND)
2. [ ] Tester avec `python test_secrets_complet_detaille.py`
3. [ ] Vérifier le rapport généré
4. [ ] Migrer les secrets restants
5. [ ] Tester l'intégration complète
6. [ ] Mettre à jour la documentation

---

*Guide créé le 29/10/2025 pour faciliter la migration des secrets GitHub vers Replit*
